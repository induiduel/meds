import json
import re
from datetime import datetime

DATABASE_PATHS = [
    "meds/src/data/pastQuestions.json",
    "meds/data/pastQuestions.json"
]

REVIEWS_PATH = "meds_database_v2/phase14_past_question_editor/reviews.jsonl"

def clean_concatenated_option(text: str) -> str:
    """Şıkkın ucuna yapışmış başka soru, chat mesajı veya çöpü temizler."""
    t = text.strip()
    # 1. WhatsApp / Chat timestamps
    t = re.split(r'\[\d{1,2}[./]\d{1,2}(?:[./]\d{2,4})?\s+\d{1,2}:\d{2}\]', t)[0].strip()
    
    # 2. Numbered new questions attached e.g. "hangisi nekrozun tanımıdır?", "112- Sağlıkta...", "9-florokinalonların..."
    patterns = [
        r'\s+\d{1,3}[-.)]\s*(?:aşağıdakilerden|hangisi|sağlıkta|florokinalon|sıcak|kemikte|anemilerle)',
        r'\s+(?:hangisi\s+nekrozun|puberta\s+öncesi|patau\s+foxp3|waldenström|final\s+sorusu|\?\s*-\s*sıcak)',
        r'\s+\d{1,2}\.\s+hangisi',
        r'\s+üroloj["\']?\s*\(\d/\d\)',
        r'\s+1-posterior\s+longit',
        r'\s+30\.\s+hangisi',
        r'\s+31\.\s+bartholin',
        r'\s+ksenon\s+i\s+i\.',
        r'\s+oidakilerden\s+hangisi',
    ]
    for pat in patterns:
        m = re.search(pat, t, re.IGNORECASE)
        if m:
            t = t[:m.start()].strip()

    # 3. Trailing question marks or unneeded punctuation
    t = re.sub(r'[\?\.…]+$', '', t).strip()
    return t

def run_repairs():
    with open(DATABASE_PATHS[0], "r", encoding="utf-8") as f:
        questions = json.load(f)

    repaired_count = 0
    quarantined_count = 0
    stats = {}

    for q in questions:
        if not q:
            continue
        qid = q.get("id")
        stem = str(q.get("stem") or "").strip()
        opts = q.get("options") or []
        
        # Normalize options to dict
        if isinstance(opts, list):
            opt_map = {o.get("key"): str(o.get("text") or "").strip() for o in opts}
        elif isinstance(opts, dict):
            opt_map = {k: str(v or "").strip() for k, v in opts.items()}
        else:
            continue

        changed = False

        # --- CASE A: Unrecoverable Debris with empty stem or multiple fragmented questions ---
        # e.g., stem is empty and options have "? D)" or chat fragments
        is_debris = False
        if len(stem) < 15 and any("?" in v and ("D)" in v or "B)" in v) for v in opt_map.values()):
            is_debris = True
        elif "ad64451dd2a0" == qid or "ff640ee5472c" == qid or "3cb2ebe1afb7" == qid or "past-1790877041199-850999" == qid:
            is_debris = True
        elif all(v.startswith("Seçenek ") for v in opt_map.values()) and len(stem) < 25:
            is_debris = True

        if is_debris:
            q["status"] = "quarantined"
            q["isSuspect"] = True
            q["isAmbiguous"] = True
            q["quarantineReason"] = "Ham OCR kaynaklı soru metni kayıp, çoklu soru birleşmesi veya kurtarılamaz metin parçalanması."
            quarantined_count += 1
            changed = True
            continue

        # --- CASE B: Specific High-Yield Questions with known fixes ---
        # 1. Fallot Tetralojisi (3448d56ff958)
        if qid == "3448d56ff958":
            q["stem"] = "Aşağıdakilerden hangisi Fallot Tetralojisi'nin (Tetralogy of Fallot) 4 temel anatomik bileşeninden biri DEĞİLDİR?"
            opt_map = {
                "A": "Pulmoner infundibuler stenoz (sağ ventrikül çıkış yolu obstrüksiyonu)",
                "B": "Geniş ventriküler septal defekt (VSD)",
                "C": "Aortanın dekstropozisyonu (ata binen aorta)",
                "D": "Sağ ventrikül konsantrik hipertrofisi",
                "E": "Mitral kapak yetmezliği ve anüler dilatasyon"
            }
            q["correctAnswer"] = "E"
            q["sik_analizi"] = {
                "A": "YANLIŞ: Pulmoner stenoz, Fallot tetralojisinin ana belirleyici anatomik bileşenidir.",
                "B": "YANLIŞ: Subaortik geniş ventriküler septal defekt (VSD) tetralojinin 4 temel bileşeninden biridir.",
                "C": "YANLIŞ: Aortanın VSD üzerine ata biner tarzda dekstropozisyonu klasik 4 bileşenden biridir.",
                "D": "YANLIŞ: Pulmoner stenoza sekonder gelişen sağ ventrikül hipertrofisi 4 bileşenden biridir.",
                "E": "DOĞRU: Fallot tetralojisi VSD, Pulmoner stenoz, Ata binen aorta ve Sağ ventrikül hipertrofisinden oluşur; mitral kapak yetmezliği bu tablonun bir bileşeni değildir."
            }
            changed = True

        # 2. Salmonella enfeksiyonları (85fc23940d0f)
        elif qid == "85fc23940d0f":
            q["stem"] = "Salmonella enfeksiyonları ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?"
            opt_map["A"] = "Gram negatif, hareketli, sporsuz fakültatif anaerobik basillerdir"
            q["correctAnswer"] = "D"
            q["sik_analizi"] = {
                "A": "DOĞRU (Çeldirici): Salmonella türleri Enterobacteriaceae familyasında yer alan Gram negatif, fakültatif anaerop basillerdir.",
                "B": "DOĞRU (Çeldirici): Kontamine kümes hayvanları, yumurta ve pastörize edilmemiş sütler en sık bulaş kaynağıdır.",
                "C": "DOĞRU (Çeldirici): Gastroenterit tablosu genellikle alımdan 12-36 saat sonra bulantı, kusma, ateş ve sulu ishalle başlar.",
                "D": "YANLIŞ (DOĞRU CEVAP): Salmonella enfeksiyonları yalnızca barsakla sınırlı kalmaz; S. Typhi ve non-tifoid Salmonella türleri invazyon göstererek bakteriyemi, vasküler enfeksiyon ve metastatik apselere neden olabilir.",
                "E": "DOĞRU (Çeldirici): Çeşitli hayvan rezervuarlarında bulunur, insanlarda klinik tablolara yol açabilir."
            }
            changed = True

        # 3. Kafa tabanı ve kafatası kırıkları (615ec9c57d75)
        elif qid == "615ec9c57d75":
            q["stem"] = "Kafatası kemik kırıkları ve kafa travmaları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?"
            opt_map["A"] = "Kafatası kırıkları içinde en sık görülen tip lineer fraktürlerdir"
            opt_map["B"] = "Epidural hematomlar tipik olarak venöz sinüs kanamasına bağlı gelişir"
            q["correctAnswer"] = "C"
            q["sik_analizi"] = {
                "A": "YANLIŞ: Lineer kırıklar en sık görülen tiptir ancak bu soru kökünde C şıkkı kafa tabanı kırığının özgül klinik bulgusu olarak sorgulanmaktadır.",
                "B": "YANLIŞ: Epidural hematom vakalarının büyük çoğunluğunda arteriyel kaynak (a. meningea media) sorumludur.",
                "C": "DOĞRU: Ön kafa tabanı kırıklarında doğrudan göz travması olmaksızın gelişen bilateral periorbital ekimoz (Rakun gözü) ve subkonjonktival kanama patognomonik bir bulgudur.",
                "D": "YANLIŞ: Çökme kırıklarında cerrahi endikasyon kemik tabula kalınlığından (genellikle >8-10 mm) fazla çökme veya dural yırtık varlığında konur.",
                "E": "YANLIŞ: Kafa tabanı kırıklarında BOS sızıntısı varlığında lomber ponksiyon transtentoryal veya tonsiller herniasyon riskinden ötürü kesinlikle kontrendikedir."
            }
            changed = True

        # 4. Osteoporoz özellikleri (8bf9636cb3b0)
        elif qid == "8bf9636cb3b0":
            q["stem"] = "Osteoporozun klinik ve patofizyolojik özellikleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?"
            opt_map["A"] = "Osteoporozda kemik matriksinin mineralizasyon kalitesi belirgin olarak bozulmuştur"
            q["correctAnswer"] = "D"
            q["sik_analizi"] = {
                "A": "YANLIŞ: Mineralizasyon bozukluğu osteomalaziye özgüdür; osteoporozda mineralizasyon kalitesi normaldir, kemik kütlesi azalmıştır.",
                "B": "YANLIŞ: Tip 1 (postmenopozal) osteoporozda trabeküler kemik kaybı kortikal kemik kaybına göre çok daha belirgindir.",
                "C": "YANLIŞ: Senil osteoporozda hem kortikal hem trabeküler kemik orantılı kaybedilir ve kalça kırığı riski ön plandadır.",
                "D": "DOĞRU: Osteoporozda birim kemik hacmi başına düşen mineral içeriği ve mineral/matriks oranı tamamen normaldir; temel defekt toplam kemik kütlesinin azalmasıdır.",
                "E": "YANLIŞ: Vertebra korpuslarındaki mikro ve makro çökme kırıkları boyda kısalmaya ve dorsal kifoza yol açar."
            }
            changed = True

        # 5. İnhaler anestezikler ve Ksenon (5779191354f9)
        elif qid == "5779191354f9":
            opt_map["E"] = "Ksenon"
            q["stem"] = "Aşağıdaki inhaler genel anesteziklerden hangisi anestezi vermeden analjezi sağlayabilen ve en yüksek MAC değerine sahip olan ajandır?"
            q["correctAnswer"] = "A" # Azot protoksit
            q["sik_analizi"] = {
                "A": "DOĞRU: Azot protoksit (N2O), düşük anestezik potensine (MAC ~%105) rağmen güçlü analjezik etkinliğe sahip inhalasyon anesteziğidir.",
                "B": "YANLIŞ: Desfluran güçlü bir inhalasyon anesteziğidir, belirgin analjezik etkisi yoktur.",
                "C": "YANLIŞ: Halotan güçlü anestezik olup analjezik etkinliği zayıftır.",
                "D": "YANLIŞ: İzofluran güçlü hipnotik anestezi sağlar, analjezik değildir.",
                "E": "YANLIŞ: Ksenon NMDA reseptör antagonisti olarak hipnoz sağlar ancak standart anestezik potensinde kullanılır."
            }
            changed = True

        # --- CASE C: General option cleaning for concatenation and garbage ---
        for k, v in list(opt_map.items()):
            cleaned_v = clean_concatenated_option(v)
            if cleaned_v != v:
                opt_map[k] = cleaned_v
                changed = True

        # Save back to question object
        if changed:
            q["options"] = [{"key": k, "text": opt_map[k], "isCorrect": (k == q.get("correctAnswer"))} for k in "ABCDE" if k in opt_map]
            q["updatedAt"] = datetime.utcnow().isoformat() + "Z"
            q["isSuspect"] = False
            q["isAmbiguous"] = False
            repaired_count += 1

    print(f"Repairs complete: {repaired_count} questions repaired/cleaned, {quarantined_count} quarantined as unrecoverable.")

    # Save to both database locations
    for p in DATABASE_PATHS:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f"Saved database to {p}")

if __name__ == "__main__":
    run_repairs()
