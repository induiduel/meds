import json
from datetime import datetime

DATABASE_PATHS = [
    "meds/src/data/pastQuestions.json",
    "meds/data/pastQuestions.json"
]

for path in DATABASE_PATHS:
    with open(path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    for q in questions:
        if not q:
            continue
        qid = q.get("id")

        # 1. Üriner sistem obstrüksiyonu (past-1790877041335-49659)
        if qid == "past-1790877041335-49659":
            q["stem"] = "Üriner sistem obstrüksiyonu ortadan kaldırılan bir böbrekte (postobstrüktif diürez dönemi) aşağıdakilerden hangisi GÖZLENMEZ?"
            q["options"] = [
                {"key": "A", "text": "İdrar konsantrasyon yeteneğinde yetmezlik", "isCorrect": False},
                {"key": "B", "text": "Glomerüler filtrasyon değerinde (GFR) kademeli artış", "isCorrect": False},
                {"key": "C", "text": "Hidrojen ve potasyum sekresyonunda bozulma (renal tübüler asidoz)", "isCorrect": False},
                {"key": "D", "text": "Tübüler sodyum geri emiliminde bozulma ve natriürez", "isCorrect": False},
                {"key": "E", "text": "Renal kan akımında kalıcı azalma", "isCorrect": True}
            ]
            q["correctAnswer"] = "E"
            q["sik_analizi"] = {
                "A": "YANLIŞ: Obstrüksiyon sonrası tübüler medüller gradiyent bozulduğundan idrarı konsantre etme yeteneği geçici olarak bozulur.",
                "B": "YANLIŞ: Basınç kalktığında GFR toparlanmaya ve artmaya başlar.",
                "C": "YANLIŞ: Distal nefron hasarına bağlı olarak geçici H+ ve K+ atılım defektleri görülebilir.",
                "D": "YANLIŞ: Toplayıcı kanallarda ANP ve birikmiş ürenin ozmotik etkisiyle natriürez ve poliüri (postobstrüktif diürez) gelişir.",
                "E": "DOĞRU: Obstrüksiyonun erken döneminde vazodilatasyon, sonrasında vazokonstriksiyon görülse de tıkanıklık kalktıktan sonra renal kan akımında kalıcı bir azalma beklenmez; perfüzyon kademeli olarak normale döner."
            }
            q["status"] = "approved"
            q["isSuspect"] = False
            q["isAmbiguous"] = False
            q["updatedAt"] = datetime.utcnow().isoformat() + "Z"

        # 2. Tüberküloz basili bulaş yolu (past-1790877041068-651148)
        elif qid == "past-1790877041068-651148":
            q["stem"] = "Mycobacterium tuberculosis (tüberküloz basili) insanlara en sık ve temel olarak hangi yolla bulaşır?"
            q["options"] = [
                {"key": "A", "text": "Doğrudan temas ve kontamine fomitler", "isCorrect": False},
                {"key": "B", "text": "Solunum yoluyla aerosol damlacık çekirdeklerinin inhalasyonu", "isCorrect": True},
                {"key": "C", "text": "Vücut sıvıları ve kan transfüzyonu", "isCorrect": False},
                {"key": "D", "text": "Fekal-oral yol", "isCorrect": False},
                {"key": "E", "text": "Vektör aracılı inokülasyon", "isCorrect": False}
            ]
            q["correctAnswer"] = "B"
            q["sik_analizi"] = {
                "A": "YANLIŞ: Tüberküloz cansız yüzeyler veya doğrudan temasla bulaşmaz.",
                "B": "DOĞRU: Mycobacterium tuberculosis, aktif akciğer veya larenks tüberkülozu olan hastaların öksürme/hapşırmasıyla havaya yayılan 1-5 mikron boyutundaki damlacık çekirdeklerinin (aerosol) inhalasyonu ile alveollere ulaşarak bulaşır.",
                "C": "YANLIŞ: Kan transfüzyonu veya vücut sıvıları rutin tüberküloz bulaş yolu değildir.",
                "D": "YANLIŞ: M. tuberculosis fekal-oral yolla bulaşmaz (M. bovis kontamine sütle GIS'ten bulaşabilir).",
                "E": "YANLIŞ: Tüberkülozun artropod veya böcek vektörü yoktur."
            }
            q["status"] = "approved"
            q["isSuspect"] = False
            q["isAmbiguous"] = False
            q["updatedAt"] = datetime.utcnow().isoformat() + "Z"

        # 3. Familyal kolorektal kanser sendromları (past-1790877041130-401298)
        elif qid == "past-1790877041130-401298":
            q["stem"] = "Aşağıdakilerden hangisi kalıtsal / familyal kolorektal kanser predispozisyon sendromları veya ilişkili genetik patolojiler arasında YER ALMAZ?"
            q["options"] = [
                {"key": "A", "text": "Familyal Adenomatöz Polipozis (FAP / APC mutasyonu)", "isCorrect": False},
                {"key": "B", "text": "Nörofibromatozis Tip 1 (NF1)", "isCorrect": True},
                {"key": "C", "text": "Herediter Non-Polipozis Kolorektal Kanser (HNPCC / Lynch Sendromu)", "isCorrect": False},
                {"key": "D", "text": "MUTYH İlişkili Polipozis (MAP)", "isCorrect": False},
                {"key": "E", "text": "Hamartomatöz Polipozis Sendromları (Peutz-Jeghers, Jüvenil Polipozis)", "isCorrect": False}
            ]
            q["correctAnswer"] = "B"
            q["sik_analizi"] = {
                "A": "YANLIŞ (Çeldirici): FAP, 5q21 lokusundaki APC tümör baskılayıcı gen mutasyonu sonucu yüzlerce adenomla seyreden ve %100 kolorektal kanser riski taşıyan klasik sendromdur.",
                "B": "DOĞRU: Nörofibromatozis Tip 1 (von Recklinghausen hastalığı), 17q11.2 lokusundaki nörofibromin gen mutasyonu sonucu kutanöz nörofibromlar, Lisch nodülleri ve optik gliomlarla seyreder; familyal kolorektal kanser sendromları arasında yer almaz.",
                "C": "YANLIŞ (Çeldirici): Lynch sendromu, DNA mismatch repair (MMR: MLH1, MSH2, MSH6, PMS2) gen mutasyonları ile kolorektal kanser riskini belirgin artıran sendromdur.",
                "D": "YANLIŞ (Çeldirici): MAP, baz eksizyon onarım geni MUTYH mutasyonu ile ilişkili otozomal resesif kolorektal kanser sendromudur.",
                "E": "YANLIŞ (Çeldirici): Peutz-Jeghers (STK11) ve Jüvenil polipozis (SMAD4/BMPR1A) hamartomatöz polipozis sendromları olup gastrointestinal kanser riskini artırır."
            }
            q["status"] = "approved"
            q["isSuspect"] = False
            q["isAmbiguous"] = False
            q["updatedAt"] = datetime.utcnow().isoformat() + "Z"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

print("Successfully cleaned the final 3 questions!")
