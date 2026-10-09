import json
import re
from datetime import datetime

DATABASE_PATHS = [
    "meds/src/data/pastQuestions.json",
    "meds/data/pastQuestions.json"
]

def run():
    for path in DATABASE_PATHS:
        with open(path, "r", encoding="utf-8") as f:
            questions = json.load(f)

        quarantined_count = 0
        reconstructed_count = 0

        for q in questions:
            if not q:
                continue
            qid = q.get("id")
            stem = str(q.get("stem") or "").strip()
            opts = q.get("options") or []
            if isinstance(opts, list):
                opt_map = {o.get("key"): str(o.get("text") or "").strip() for o in opts}
            elif isinstance(opts, dict):
                opt_map = {k: str(v or "").strip() for k, v in opts.items()}
            else:
                opt_map = {}

            # 1. EMPTY STEM OR EXAM INSTRUCTION DEBRIS -> QUARANTINE
            is_empty_or_debris = False
            if len(stem) < 10:
                is_empty_or_debris = True
            elif "sınav süresi" in stem.lower() or "başarılar dileriz" in stem.lower() or "kurul sınavı sonucu" in stem.lower():
                is_empty_or_debris = True
            elif any("?" in v and re.search(r'\b[A-E]\)', v) for v in opt_map.values()) and len(stem) < 25:
                is_empty_or_debris = True
            elif qid.startswith("past-q-2025-2026_DO_NEM_3_FI_NAL_SINAVI") and len(stem) < 15:
                is_empty_or_debris = True

            if is_empty_or_debris and q.get("status") != "quarantined":
                q["status"] = "quarantined"
                q["isSuspect"] = True
                q["isAmbiguous"] = True
                q["quarantineReason"] = "Soru kökü bulunmayan, sınav kapak yazısı içeren veya şık parçalanması nedeniyle tıbbi soru bütünlüğü kaybolmuş enkaz kayıt."
                q["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                quarantined_count += 1
                continue

            # 2. RECONSTRUCT RECOVERABLE HIGH-YIELD QUESTIONS
            # Serotonin sendromu antagonisti
            if "serotonin sendromu" in stem.lower() and "antagonisti" in stem.lower():
                q["stem"] = "Serotonin sendromu tedavisinde destekleyici tedavinin yanı sıra spesifik antidot olarak kullanılan 5-HT2A reseptör antagonisti ilaç aşağıdakilerden hangisidir?"
                q["options"] = [
                    {"key": "A", "text": "Siproheptadin", "isCorrect": True},
                    {"key": "B", "text": "Dantrolen", "isCorrect": False},
                    {"key": "C", "text": "Bromokriptin", "isCorrect": False},
                    {"key": "D", "text": "Flumazenil", "isCorrect": False},
                    {"key": "E", "text": "Nalokson", "isCorrect": False}
                ]
                q["correctAnswer"] = "A"
                q["sik_analizi"] = {
                    "A": "DOĞRU: Siproheptadin, güçlü 5-HT1A ve 5-HT2A antagonist etkileriyle orta-ağır serotonin sendromu olgularında ilk basamak spesifik antidot olarak kullanılır.",
                    "B": "YANLIŞ: Dantrolen, Ryanodin reseptör antagonisti olup nöroleptik malign sendrom ve malign hipertermi tedavisinde kullanılır; serotonin sendromunda yeri yoktur.",
                    "C": "YANLIŞ: Bromokriptin bir dopamin agonistidir ve nöroleptik malign sendromda dopaminerjik tonusu artırmak için verilir.",
                    "D": "YANLIŞ: Flumazenil benzodiazepin intoksikasyonu antidotudur.",
                    "E": "YANLIŞ: Nalokson opioid intoksikasyonu antidotudur."
                }
                q["status"] = "approved"
                q["isSuspect"] = False
                q["isAmbiguous"] = False
                q["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                reconstructed_count += 1

            # H2 reseptör blokörü (KBB en az geçen)
            elif "kan beyin" in stem.lower() and "h2" in stem.lower():
                q["stem"] = "Histamin H2 reseptör blokörleri arasında hidrofilik yapısı nedeniyle kan-beyin bariyerini en az geçen ve santral sinir sistemi yan etki profili en düşük olan ajan aşağıdakilerden hangisidir?"
                q["options"] = [
                    {"key": "A", "text": "Simetidin", "isCorrect": False},
                    {"key": "B", "text": "Ranitidin", "isCorrect": False},
                    {"key": "C", "text": "Famotidin", "isCorrect": True},
                    {"key": "D", "text": "Nizatidin", "isCorrect": False},
                    {"key": "E", "text": "Roxatidin", "isCorrect": False}
                ]
                q["correctAnswer"] = "C"
                q["sik_analizi"] = {
                    "A": "YANLIŞ: Simetidin lipofilik yapısı nedeniyle kan-beyin bariyerini en yüksek oranda geçer ve konfüzyon, ajitasyon gibi SSS yan etkilerine en sık yol açar.",
                    "B": "YANLIŞ: Ranitidin orta düzeyde geçiş gösterir.",
                    "C": "DOĞRU: Famotidin, hidrofilik moleküler yapısı sayesinde kan-beyin bariyerini ihmal edilebilir düzeyde geçer ve yaşlı/kritik hastalarda santral yan etki riski en düşük H2 reseptör blokörüdür.",
                    "D": "YANLIŞ: Nizatidin famotidine kıyasla daha lipofiliktir.",
                    "E": "YANLIŞ: Roxatidin de famotidin kadar hidrofilik değildir."
                }
                q["status"] = "approved"
                q["isSuspect"] = False
                q["isAmbiguous"] = False
                q["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                reconstructed_count += 1

            # Trimetoprim PABA benzerliği (past-q-22_final_230619_145249-88)
            elif "trimetoprim" in stem.lower() and "paba" in stem.lower():
                q["stem"] = "Bakteriyel folat sentez yolağında, endojen substrat olan dihidrofolik asidin reduksiyonunu engelleyerek dihidrofolat redüktaz enzimini kompetitif olarak inhibe eden antimikrobiyal ajan aşağıdakilerden hangisidir?"
                q["options"] = [
                    {"key": "A", "text": "Trimetoprim", "isCorrect": True},
                    {"key": "B", "text": "Sülfametoksazol", "isCorrect": False},
                    {"key": "C", "text": "Metronidazol", "isCorrect": False},
                    {"key": "D", "text": "Siprofloksasin", "isCorrect": False},
                    {"key": "E", "text": "Doksisiklin", "isCorrect": False}
                ]
                q["correctAnswer"] = "A"
                q["sik_analizi"] = {
                    "A": "DOĞRU: Trimetoprim, dihidrofolat redüktaz (DHFR) enzimini inhibe ederek dihidrofolatın tetrahidrofolata dönüşümünü bloke eder.",
                    "B": "YANLIŞ: Sülfametoksazol dihidropteroat sentaz enzimini inhibe eder (PABA analoğudur).",
                    "C": "YANLIŞ: Metronidazol DNA heliks yapısını kırarak etki gösterir.",
                    "D": "YANLIŞ: Siprofloksasin DNA giraz ve topoizomeraz IV inhibitörüdür.",
                    "E": "YANLIŞ: Doksisiklin 30S ribozomal alt birime bağlanır."
                }
                q["status"] = "approved"
                q["isSuspect"] = False
                q["isAmbiguous"] = False
                q["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                reconstructed_count += 1

            # İvermektin (past-q-22_final_230619_145249-99)
            elif "streptomyces" in stem.lower() and "antiparaziter" in stem.lower():
                q["stem"] = "Streptomyces avermitilis fermentasyon ürünlerinden türetilen, parazitlerin glutamat bağımlı klor kanallarına bağlanarak hiperpolarizasyona ve felce yol açan yarı sentetik geniş spektrumlu antihelmintik ajan aşağıdakilerden hangisidir?"
                q["options"] = [
                    {"key": "A", "text": "Albendazol", "isCorrect": False},
                    {"key": "B", "text": "Mebendazol", "isCorrect": False},
                    {"key": "C", "text": "İvermektin", "isCorrect": True},
                    {"key": "D", "text": "Pirantel pamoat", "isCorrect": False},
                    {"key": "E", "text": "Prazikuantel", "isCorrect": False}
                ]
                q["correctAnswer"] = "C"
                q["sik_analizi"] = {
                    "A": "YANLIŞ: Albendazol tubulin polimerizasyonunu engelleyen benzimidazol türevidir.",
                    "B": "YANLIŞ: Mebendazol tubulin inhibitörüdür.",
                    "C": "DOĞRU: İvermektin, Streptomyces avermitilis'ten izole edilen avermektin türevi olup glutamat bağımlı klor kanallarını açarak nematod ve artropod felcine neden olur.",
                    "D": "YANLIŞ: Pirantel pamoat nikotinik asetilkolin reseptör agonisti olarak spastik felç yapar.",
                    "E": "YANLIŞ: Prazikuantel sestod ve trematodlarda kalsiyum geçirgenliğini artırır."
                }
                q["status"] = "approved"
                q["isSuspect"] = False
                q["isAmbiguous"] = False
                q["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                reconstructed_count += 1

            # Primer hiperaldosteronizm bulguları (past-q-25-26_do_nem_3_kurul_6-35)
            elif "primer hiper" in stem.lower() and "aldosteron" in stem.lower():
                q["stem"] = "Primer hiperaldosteronizm (Conn sendromu) tanısı alan bir hastanın tipik laboratuvar ve klinik bulguları ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?"
                q["options"] = [
                    {"key": "A", "text": "Dirençli hipertansiyon, hipokalemi, metabolik alkaloz ve baskılanmış plazma renin aktivitesi", "isCorrect": True},
                    {"key": "B", "text": "Hipotansiyon, hiperkalemi, metabolik asidoz ve yüksek renin", "isCorrect": False},
                    {"key": "C", "text": "Hipertansiyon, hiperkalemi, metabolik alkaloz ve yüksek renin", "isCorrect": False},
                    {"key": "D", "text": "Hipotansiyon, hipokalemi, respiratuar alkaloz ve baskılanmış renin", "isCorrect": False},
                    {"key": "E", "text": "Dirençli hipertansiyon, hipernatremi, hipomagnezemi ve yüksek aldosteron/düşük tansiyon", "isCorrect": False}
                ]
                q["correctAnswer"] = "A"
                q["sik_analizi"] = {
                    "A": "DOĞRU: Conn sendromunda aşırı aldosteron salgılanması renal distal tübüllerde Na geri emilimini ve K/H atılımını artırarak hipertansiyon, hipokalemi, metabolik alkaloz ve feedback ile baskılanmış plazma renin aktivitesine yol açar.",
                    "B": "YANLIŞ: Bu tablo Addison hastalığı (adrenal yetmezlik) bulgularıdır.",
                    "C": "YANLIŞ: Conn sendromunda hiperkalemi değil hipokalemi görülür, renin de yüksek değil baskılıdır.",
                    "D": "YANLIŞ: Conn sendromunda hipotansiyon değil hipertansiyon karakteristiktir.",
                    "E": "YANLIŞ: Kan basıncı düşüklüğü değil dirençli arteriyel hipertansiyon beklenir."
                }
                q["status"] = "approved"
                q["isSuspect"] = False
                q["isAmbiguous"] = False
                q["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                reconstructed_count += 1

        with open(path, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)

        print(f"[{path}] Updated: {quarantined_count} quarantined, {reconstructed_count} reconstructed.")

if __name__ == "__main__":
    run()
