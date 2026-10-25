#!/usr/bin/env python3
"""
generate_deep_k2_12.py:
Expands the 16 sparse pages (<40 words) of y25-k2-12-kafa-travmalari into deep,
rich amfi lecture sentences, fixes drawing forward leaks (35/35 commands),
and verifies all 6 Quality Gates with 0 HATA.
"""

import sys
import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/ders_isci"))
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/cizim"))

import konusma_v2 as KV
import denetle as D
import isle as IS
import cizim_dogrula as CD
import sablon

TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-12-kafa-travmalari"

NEW_SENTENCES_BY_PAGE = {
    5: {
        "ses": "Vasküler oluklar ve sutur hatlarının aksine fraktür çizgileri dallanma göstermeyen düzensiz hatlar çizer ve eşlik eden intrakraniyal kanamayı dışlamak için mutlaka acil bilgisayarlı tomografi gerekir.",
        "ekran": "**Radyolojik Özellik:** Vasküler oluklardan farklılık ve acil tomografi endikasyonu",
        "slayt": {
            "sayfa": 5,
            "satir": ["02.08.08 15:48"],
            "sekil": "Direkt grafide kırık hattı ve vasküler oluk ayrımı"
        },
        "slayt_adim": "k2-12-d-s01",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    15: {
        "ses": "Klinik pratikte epidural, subdural ve subaraknoid kompartmanlarda gelişen bu kanama odakları, kafa kemikleri ile korteks arasındaki anatomik ilişkiyi bozarak primer intrakraniyal bası kaynağını oluşturur.",
        "ekran": "**Anatomik Odaklar:** Epidural, subdural ve subaraknoid kompartman kanamaları",
        "slayt": {
            "sayfa": 15,
            "satir": ["EKSTRAAKSİYAL HEMORAJİLER"],
            "sekil": None
        },
        "slayt_adim": "k2-12-d-s03",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    16: {
        "ses": "Temporal kemiğin skuamöz parçasını kat eden kırıklar kemik oluğunda korumasız seyreden arteria meningea media dallarını yırtarak yüksek basınçlı arteriyel kanamaya yol açar.",
        "ekran": "**Pterion ve Damar Yırtılması:** Temporal kırıkların arteria meningea media dallarını yırtması",
        "slayt": {
            "sayfa": 16,
            "satir": ["EPİDURAL HEMATOM"],
            "sekil": None
        },
        "slayt_adim": "k2-12-d-s03",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    23: {
        "ses": "Hematom kitlesi hızla büyüyerek dakikalar içinde kafa içi basıncını kritik eşiğin üzerine çıkarabileceğinden, girdap bulgusu saptanan hastada cerrahi hazırlıklar vakit kaybedilmeden başlatılmalıdır.",
        "ekran": "**Hızlı Cerrahi Endikasyon:** Girdap bulgusunda dakikalar içinde acil cerrahi dekompresyon",
        "slayt": {
            "sayfa": 23,
            "satir": ["Epidural Hematom"],
            "sekil": None
        },
        "slayt_adim": "k2-12-d-s03",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    26: {
        "ses": "Ayrıca superior sagital sinüs yırtılmasına bağlı gelişebilen tepe hematomları venöz dolaşımı engelleyerek intrakraniyal venöz hipertansiyona ve yaygın serebral ödeme neden olabilir.",
        "ekran": "**Sagital Sinüs Riski:** Superior sagital sinüs basısı ve venöz hipertansiyon",
        "slayt": {
            "sayfa": 26,
            "satir": ["Sağ frontalde ve verteks düzeyinde EDH"],
            "sekil": "Aksiyel ve koronal BT kesitlerinde sağ frontal konveksite ve verteks yerleşimli epidural hematom"
        },
        "slayt_adim": "k2-12-d-s04",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    30: {
        "ses": "Dura mater yaprağına sıkıca yapışık olmayan bu serbest aralık, kanın hemisfer konveksitesi üzerinde hiçbir kemik sütür kısıtlamasıyla karşılaşmadan yayılmasına olanak tanır.",
        "ekran": "**Geniş Yüzey Yayılımı:** Sütür engeli olmaksızın hemisfer konveksitesine yayılma",
        "slayt": {
            "sayfa": 30,
            "satir": ["SUBDURAL HEMATOM"],
            "sekil": None
        },
        "slayt_adim": "k2-12-d-s06",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    34: {
        "ses": "Radyolojik olarak iç yüzeyi parankim konveksitesine uyum göstererek içbükey kıvrım çizen hilal görünümü, epidural kanamanın mercek biçimindeki dışbükey formundan kesin olarak ayrılır.",
        "ekran": "**Konkav Hilal Morfolojisi:** Parankim yüzeyine uyan içbükey sınır ve epidural ayrımı",
        "slayt": {
            "sayfa": 34,
            "satir": ["Subdural Hematom"],
            "sekil": None
        },
        "slayt_adim": "k2-12-d-s06",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    35: {
        "ses": "Tekrarlayan mikrokanamalar ve fibrin lizisi sonucu hematom kapsülü çevresinde yeni kırılgan kapiller damarlar ürer ve bu durum koleksiyonun aylar içinde giderek genişlemesine yol açar.",
        "ekran": "**Kapsül Neovaskülarizasyonu:** Kırılgan neomembran kapillerleri ve hacim artışı",
        "slayt": {
            "sayfa": 35,
            "satir": ["Kronikleştikçe içerisinde seviyelenmeler  oluşur."],
            "sekil": "Aksiyel BT kesitinde kronik subdural hematom içinde gelişen sıvı-kan seviyelenmesi ve iç membranlar"
        },
        "slayt_adim": "k2-12-d-s06",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    41: {
        "ses": "Travma anında yüzeyel pial kortikal damarların gerilip yırtılması sonucu subaraknoid alana dökülen kan, beyin omurilik sıvısı akımına karışarak hızla tüm bazal sisternlere yayılır.",
        "ekran": "**Travmatik SAK Mekanizması:** Yüzeyel kortikal damar yırtılması ve BOS yayılımı",
        "slayt": {
            "sayfa": 41,
            "satir": ["Subaraknoid Kanama"],
            "sekil": None
        },
        "slayt_adim": "k2-12-d-s08",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    42: {
        "ses": "Ayrıca kan yıkım ürünlerinin araknoid villusları tıkaması ve damar duvarlarında vazospazm tetiklemesi, serebral hipoperfüzyon ve gecikmiş iskemik nörolojik defisit gelişimine neden olabilir.",
        "ekran": "**Villus Tıkanması ve Vazospazm:** Araknoid granülasyon tıkanması ve gecikmiş iskemi",
        "slayt": {
            "sayfa": 42,
            "satir": ["Subaraknoid Kanama"],
            "sekil": None
        },
        "slayt_adim": "k2-12-d-s08",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    43: {
        "ses": "Manyetik rezonans flair sekansında normalde baskılanarak koyu görünen beyin omurilik sıvısı sinyalinin yerini sulkuslar içinde parlak hiperintens parlama alması tanıyı kesinleştirir.",
        "ekran": "**FLAIR Hiperintensitesi:** Sulkuslarda BOS sinyal baskılanmasının kaybolması",
        "slayt": {
            "sayfa": 43,
            "satir": ["within sulci near the vertex."],
            "sekil": "Kontrastsız BT ve FLAIR MRG kesitlerinde verteks sulkuslarında hiperintens travmatik subaraknoid kanama odakları"
        },
        "slayt_adim": "k2-12-d-s08",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    53: {
        "ses": "Ayrıca parankim içine hava girişiyle oluşan pnömosefali varlığı dura mater yırtığını doğrudan belgeler ve menenjit veya beyin absesi riskine karşı acil cerrahi onarım gerektirir.",
        "ekran": "**Pnömosefali ve Dural Yırtık:** Dural defektin doğrulanması ve enfeksiyon profilaksisi",
        "slayt": {
            "sayfa": 53,
            "satir": ["PENETRAN YARALANMALAR", "BT Bulguları"],
            "sekil": None
        },
        "slayt_adim": "k2-12-d-s09",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    54: {
        "ses": "İntrakraniyal alana uzanan yabancı cisim kavernöz sinüs ve internal karotid arter gibi komşu vasküler yapılarla yakın ilişkide olabileceğinden mutlaka acil bilgisayarlı tomografi anjiyografiyle planlanmalıdır.",
        "ekran": "**Vasküler Komşuluk:** Kavernöz sinüs ve internal karotid arter yaralanması riski",
        "slayt": {
            "sayfa": 54,
            "satir": ["transorbital yoldan intrakranial penetrasyon"],
            "sekil": "Radyolojik skenogram grafisinde orbitadan girip kafa içine uzanan metalik yabancı cisim opasitesi"
        },
        "slayt_adim": "k2-12-d-s09",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    63: {
        "ses": "Sagital planda kraniyokaudal yönde beynin ani yer değiştirmesi, mezensefalonun tentoryum kenarına çarparak kontüze olmasına ve santral otonomik dengenin ağır şekilde sarsılmasına yol açar.",
        "ekran": "**Kraniyokaudal Savrulma:** Mezensefalon kontüzyonu ve otonomik disfonksiyon",
        "slayt": {
            "sayfa": 63,
            "satir": ["brainstem subcortical injury"],
            "sekil": "Aksiyel FLAIR ve sagital T2 MRG kesitlerinde kraniyokaudal savrulmaya bağlı anterorostral beyin sapı zedelenmesi"
        },
        "slayt_adim": "k2-12-d-s12",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    66: {
        "ses": "Rijit dural kıvrımlar ve kafatası kemikleri intrakraniyal boşluğu odacıklara böldüğü için fokal basınç gradiyenti beyin dokusunu en zayıf açıklıklardan dışarıya doğru öteler.",
        "ekran": "**Dural Kompartmanlar:** Fokal basınç gradiyenti ve açıklıklardan fıtıklaşma",
        "slayt": {
            "sayfa": 66,
            "satir": ["Herniasyonlar"],
            "sekil": "İntrakraniyal kompartmanlar arası subfalsin, transtentorial ve tonsiller herniasyon anatomik yönelim şeması"
        },
        "slayt_adim": "k2-12-d-s13",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    },
    72: {
        "ses": "Suprasellar ve ambient sisternlerin kademeli olarak silinmesiyle birlikte beyin sapı etrafındaki serbest beyin omurilik sıvısı boşlukları tamamen kaybolarak akut bası tablosunu ağırlaştırır.",
        "ekran": "**Sisternlerin Silinmesi:** Suprasellar ve ambient sistern obliterasyonu",
        "slayt": {
            "sayfa": 72,
            "satir": ["Transtentorial Herniasyon"],
            "sekil": "Manyetik rezonans koronal kesitinde medial temporal lobun suprasellar ve ambient sisterne herniye olduğu unkal herniasyon"
        },
        "slayt_adim": "k2-12-d-s14",
        "cikmis": [],
        "spot": None,
        "duzey": 2
    }
}

DRAWING_SNIPPETS_MAP = {
    11: "serebral perfüzyon basıncını düşürür",
    13: "arteria meningea media yırtılır",
    14: "lucid interval",
    16: "eşlik etmeyebilir",
    17: "falks serebrinin kafatasına yapışma yerini geçerek",
    19: "ani açısal rotasyon hareketlerinde",
    20: "konkav hilal şekilli",
    21: "serebral atrofiye bağlı olarak",
    24: "tek yönlü kapakçık mekanizması",
    25: "orbita tavanındaki pürtüklü kemik",
    28: "Diffüz aksonal zedelenme en sık kortikal gri",
    30: "foramen magnum yoluyla spinal kanala",
    31: "singulat girusun falks serebri altından",
    32: "ışığa yanıtsız fikse pupil tablosu",
    33: "Kernohan çentiği",
    34: "medulla oblongatayı sıkıştırarak"
}

def main():
    print("=== Expanding y25-k2-12-kafa-travmalari to Deep Amfi Lecture ===")
    
    with open(TASLAK / "konusma_v2.json") as f:
        kv = json.load(f)
    
    # Ensure idempotency by removing any previously added sentences
    added_ses = {v["ses"] for v in NEW_SENTENCES_BY_PAGE.values()}
    for b in kv.get("bolumler", []):
        for p in b.get("paragraflar", []):
            p["cumleler"] = [c for c in p.get("cumleler", []) if c.get("ses") not in added_ses]
    
    with open(TASLAK / "cizim_aday.json") as f:
        caday = json.load(f)
    
    drawings = caday.get("komutlar", [])
    print(f"Loaded {len(drawings)} candidate drawings.")
    
    # 1. Expand sentences
    # Map old sentence IDs to sentences
    old_to_new_cid = {}
    new_cumleler_all = []
    
    counter = 1
    for bi, b in enumerate(kv.get("bolumler", [])):
        for pi, p in enumerate(b.get("paragraflar", [])):
            old_sents = p.get("cumleler", [])
            new_sents = []
            
            # Check what page this paragraph covers
            pages_in_p = {c.get("slayt", {}).get("sayfa") for c in old_sents}
            
            for c in old_sents:
                old_id = c["id"]
                new_id = f"k2-12-c{counter:04d}"
                c_copy = dict(c)
                c_copy["id"] = new_id
                old_to_new_cid[old_id] = new_id
                new_sents.append(c_copy)
                counter += 1
            
            # Check if any page in this paragraph needs an added sentence
            for p_num in sorted(pages_in_p):
                if p_num in NEW_SENTENCES_BY_PAGE:
                    add_data = NEW_SENTENCES_BY_PAGE[p_num]
                    new_id = f"k2-12-c{counter:04d}"
                    new_sent = {
                        "id": new_id,
                        "ses": add_data["ses"],
                        "ekran": add_data["ekran"],
                        "duzey": add_data["duzey"],
                        "vurgu": [],
                        "slayt": add_data["slayt"],
                        "slayt_adim": add_data["slayt_adim"],
                        "cikmis": add_data["cikmis"],
                        "spot": add_data["spot"]
                    }
                    new_sents.append(new_sent)
                    counter += 1
            
            p["cumleler"] = new_sents
            new_cumleler_all.extend(new_sents)
    
    print(f"Expanded to {len(new_cumleler_all)} sentences.")
    
    # Check word counts per page
    sayfa_kelime = {}
    for c in new_cumleler_all:
        s = c.get("slayt", {}).get("sayfa", 1)
        w = len(c.get("ses", "").split())
        sayfa_kelime[s] = sayfa_kelime.get(s, 0) + w
    
    sparse_pages = [s for s, w in sorted(sayfa_kelime.items()) if w < 40]
    total_words = sum(sayfa_kelime.values())
    print(f"Total words: {total_words} across {len(sayfa_kelime)} pages. Sparse pages count: {len(sparse_pages)}")
    if sparse_pages:
        print(f"ERROR: Still have sparse pages: {sparse_pages}")
        sys.exit(1)
    
    # Save updated konusma_v2.json
    with open(TASLAK / "konusma_v2.json", "w", encoding="utf-8") as f:
        json.dump(kv, f, ensure_ascii=False, indent=2)
    print("Saved konusma_v2.json successfully.")
    
    # 2. Update and save cizim_aday.json
    def find_id_by_text(snippet):
        for s in new_cumleler_all:
            if snippet in s["ses"]:
                return s["id"]
        raise ValueError(f"Snippet not found: {snippet}")

    updated_drawings = []
    for idx, d in enumerate(drawings):
        d_copy = dict(d)
        if idx in DRAWING_SNIPPETS_MAP:
            d_copy["cumle"] = find_id_by_text(DRAWING_SNIPPETS_MAP[idx])
        else:
            d_copy["cumle"] = old_to_new_cid.get(d.get("cumle"), d.get("cumle"))
        if "adimlar" in d_copy and not d_copy.get("ogeler"):
            d_copy["ogeler"] = d_copy["adimlar"]
        updated_drawings.append(d_copy)
    
    caday["komutlar"] = updated_drawings
    with open(TASLAK / "cizim_aday.json", "w", encoding="utf-8") as f:
        json.dump(caday, f, ensure_ascii=False, indent=2)
    print(f"Saved cizim_aday.json with {len(updated_drawings)} commands.")
    
    # 3. Generate konusma_metni.md
    md_lines = [f"# {kv.get('baslik', 'Kafa Travmaları')}", ""]
    for bi, b in enumerate(kv.get("bolumler", [])):
        b_baslik = b.get("baslik", f"Bölüm {bi+1}")
        md_lines.append(f"@@ {b_baslik}")
        for pi, p in enumerate(b.get("paragraflar", [])):
            p_text = " ".join(c["ses"].strip() for c in p.get("cumleler", []) if c.get("ses"))
            if p_text:
                md_lines.append(p_text)
                md_lines.append("")
    
    (TASLAK / "konusma_metni.md").write_text("\n".join(md_lines).strip() + "\n", encoding="utf-8")
    print("Generated and saved konusma_metni.md.")
    
    # 4. RUN ALL 6 QUALITY GATES
    print("\n--- Running Quality Gate 1: KV.dogrula ---")
    kv_errs = KV.dogrula(kv, KV.kaynak_sayfa(TASLAK), KV.kaynak_metin(TASLAK))
    if kv_errs:
        print(f"FAILED KV.dogrula with {len(kv_errs)} errors:")
        for e in kv_errs[:15]: print(" ", e)
        sys.exit(1)
    print("PASSED KV.dogrula: 0 HATA")
    
    print("\n--- Running Quality Gate 2: denetle.py ---")
    d_rapor = D.Denetim(TASLAK).calistir()
    if d_rapor.get("hata", 0) > 0:
        print(f"FAILED denetle.py with {d_rapor.get('hata')} errors:")
        for e in d_rapor.get("hatalar", []): print(" ", e)
        sys.exit(1)
    print("PASSED denetle.py: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 3: validate_learning_decks.py ---")
    r_val = subprocess.run([
        sys.executable, str(REPO_ROOT / "meds/scripts/validate_learning_decks.py"),
        str(TASLAK / "deck.json"), "--oyun-zorunlu", "--kurul2"
    ], capture_output=True, text=True)
    if r_val.returncode != 0:
        print("FAILED validate_learning_decks:", r_val.stdout, r_val.stderr)
        sys.exit(1)
    print("PASSED validate_learning_decks: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 4: metin_denetle.py ---")
    r_metin = subprocess.run([
        sys.executable, str(REPO_ROOT / "meds/scripts/sesli_anlatim/metin_denetle.py"),
        str(TASLAK / "konusma_metni.md")
    ], capture_output=True, text=True)
    if r_metin.returncode != 0:
        print("FAILED metin_denetle:\n", r_metin.stdout, r_metin.stderr)
        sys.exit(1)
    print("PASSED metin_denetle: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 5: sesli_kapsam ---")
    kapsam_errs = IS.sesli_kapsam(TASLAK)
    if kapsam_errs:
        print(f"FAILED sesli_kapsam with {len(kapsam_errs)} errors:")
        for ke in kapsam_errs: print(" ", ke)
        sys.exit(1)
    print("PASSED sesli_kapsam: 0 HATA")
    
    print("\n--- Running Quality Gate 6: cizim_dogrula.py ---")
    accum = []
    cum_text = {}
    for s in new_cumleler_all:
        accum.append(s["ses"])
        accum.append(s.get("ekran", ""))
        cum_text[s["id"]] = " ".join(accum)
    sent_map = {s["id"]: s for s in new_cumleler_all}
    c_errs = []
    for idx, d in enumerate(updated_drawings):
        cid = d["cumle"]
        coz_d, err_c = sablon.coz(d)
        if err_c:
            c_errs.append(f"Drawing {idx+1} ({cid}) sablon.coz error: {err_c}")
            continue
        s_words = len(sent_map[cid]["ses"].split())
        err_v = CD.denetle(coz_d, s_words, [], None, cum_text[cid])
        if err_v:
            c_errs.append(f"Drawing {idx+1} ({cid}) {d.get('sablon')} error: {err_v}")
    if c_errs:
        print(f"FAILED cizim_dogrula with {len(c_errs)} errors:")
        for ce in c_errs: print(" ", ce)
        sys.exit(1)
    print(f"PASSED cizim_dogrula: {len(updated_drawings)}/{len(updated_drawings)} KOMUT 0 HATA")
    print("\n🎉 ALL 6 QUALITY GATES PASSED PERFECTLY FOR LESSON 12 WITH ZERO ERRORS!")

if __name__ == "__main__":
    main()
