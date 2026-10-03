# -*- coding: utf-8 -*-
"""
Enrich Medical Glossary and Encyclopedia with detailed Apoptosis & Bcl-2 Family entries
(Bax, Bak, Intrinsic Pathway, Extrinsic Pathway, Apoptosome, Smac/DIABLO, etc.)
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

GLOSSARY_PATH = 'src/data/medical_glossary.json'
ENCYCLOPEDIA_PATH = 'src/data/medical_encyclopedia.json'

with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
    glossary = json.load(f)

with open(ENCYCLOPEDIA_PATH, 'r', encoding='utf-8') as f:
    encyclopedia = json.load(f)

# 1. New Glossary Entries
new_glossary = {
    "bak proteini": {
        "term": "Bak Proteini (Bcl-2 Homologous Antagonist/Killer)",
        "meaning": "Mitokondri dış membranında yerleşik, pro-apoptotik Bcl-2 ailesi üyesidir. Bax ile birlikte oligomerleşerek sitokrom c salınımını ve kaspaz aktivasyonunu tetikler.",
        "category": "Patoloji",
        "description": "Bak proteini normal koşullarda mitokondri dış membranında Bcl-2 ve Bcl-xL tarafından inaktif tutulur. DNA hasarı veya büyüme faktörü yokluğunda BH3-only proteinleri (Bid, Bim, Puma) tarafından aktive edilir. Aktive olan Bak, Bax ile birlikte MOMP (Mitochondrial Outer Membrane Permeabilization) porlarını oluşturarak mitokondriler arası mesafeden sitokrom c'nin sitoplazmaya çıkışını sağlar.",
        "examBadge": "🔴 PRO-APOPTOTİK EFEKTÖR",
        "aliases": ["bak", "bcl2l7", "bak1"]
    },
    "bax proteini": {
        "term": "Bax Proteini (Bcl-2-Associated X Protein)",
        "meaning": "Sitozolde inaktif bulunan, p53 uyarısıyla aktive olup mitokondriye transloke olarak por açan ana pro-apoptotik proteindir.",
        "category": "Patoloji",
        "description": "Bax normalde sitoplazmada monomerik halde bulunur. Hücresel stres ve p53 aktivasyonu sonrasında mitokondri dış zarına göç eder, oligomerleşir ve Bak ile por kanalları açar. Anti-apoptotik Bcl-2 tarafından inhibe edilir; Bax/Bcl-2 oranı hücrenin yaşam veya ölüm kararını belirleyen ana biyokimyasal terazi görevi görür.",
        "examBadge": "🔵 TUS / KOMİTE SORUSU",
        "aliases": ["bax", "bcl2l4"]
    },
    "intrensek apoptoz yolagi": {
        "term": "İntrensek (Mitokondriyal) Apoptoz Yolağı",
        "meaning": "Hücre içi hasar ve stres sinyalleriyle mitokondriden sitokrom c salınımı ve kaspaz-9 aktivasyonu ile yürütülen programlı ölüm yolağıdır.",
        "category": "Patoloji",
        "description": "DNA hasarı, hipoksi, serbest radikaller veya büyüme faktörü yoksunluğu ile başlar. BH3-only proteinleri (Bim, Bid, Bad, Puma, Noxa) sensör olarak algılar -> Bax ve Bak aktive olur -> MOMP oluşur ve sitokrom c sitoplazmaya salınır -> Sitokrom c + Apaf-1 + dATP birleşerek Apoptozom kompleksini oluşturur -> İnisiyatör prokaspaz-9 aktive olur -> Yürütücü kaspazlar (kaspaz-3 ve kaspaz-6) kesilerek apoptoz tamamlanır.",
        "examBadge": "🔴 MİTOKONDRİYAL KASPAS KASKADI",
        "aliases": ["mitokondriyal apoptoz", "intrensek yolak", "apoptoz mitokondriyal yol"]
    },
    "ekstrensek apoptoz yolagi": {
        "term": "Ekstrensek (Ölüm Reseptörü) Apoptoz Yolağı",
        "meaning": "Hücre yüzeyindeki ölüm reseptörlerine (Fas/CD95, TNFR1) ligand bağlanmasıyla kaspaz-8 üzerinden yürütülen ölüm yolağıdır.",
        "category": "Patoloji",
        "description": "Sitotoksik T lenfositleri (CTL) ve NK hücreleri tarafından kullanılır. FasL'ın Fas (CD95) reseptörüne bağlanmasıyla hücre içinde FADD adaptör proteini toplanır ve DISC (Death-Inducing Signaling Complex) oluşur. Bu kompleks prokaspaz-8'i otokatalitik olarak keserek kaspaz-8'i aktive eder. Kaspaz-8 doğrudan kaspaz-3'ü uyarabildiği gibi, Bid proteinini tBid haline getirerek intrensek mitokondriyal yolakla da çapraz bağlantı (cross-talk) kurar. FLIP proteini prokaspaz-8'e bağlanarak bu yolağı inhibe eder.",
        "examBadge": "🔵 FAS-FASL / KASPAZ-8",
        "aliases": ["ekstrensek yolak", "ölüm reseptörü yolağı", "fas yolağı"]
    },
    "apoptozom": {
        "term": "Apoptozom (Apoptosome Kompleksi)",
        "meaning": "Sitokrom c, Apaf-1 ve dATP'nin sitozolde birleşmesiyle oluşan, prokaspaz-9'u aktive eden tekerlek benzeri heptamerik ölüm kompleksidir.",
        "category": "Patoloji / Biyokimya",
        "description": "Mitokondriden çıkan sitokrom c sitozolde Apaf-1 (Apoptotic Protease Activating Factor-1) molekülüne bağlanır. dATP hidrolizi ile 7 adet Apaf-1/Sitokrom c ünitesi birleşerek heptamerik 'apoptozom' tekerlek yapısını kurar. Ortadaki CARD domainleri prokaspaz-9 moleküllerini toplar ve proteolitik aktivasyonunu sağlar.",
        "examBadge": "🔴 HEPTAMERİK KOMPLEKS",
        "aliases": ["apoptosome", "apaf-1 kompleksi"]
    },
    "smac diablo": {
        "term": "Smac / DIABLO Proteini",
        "meaning": "Mitokondriden sitokrom c ile birlikte salınan ve IAP'leri (apoptoz inhibitörlerini) bloke ederek kaspazların çalışmasını serbest bırakan proteindir.",
        "category": "Patoloji",
        "description": "Hücre içinde kaspaz aktivasyonunu frenleyen en güçlü moleküller IAP (Inhibitor of Apoptosis Proteins / XIAP) ailesidir. Mitokondri membran geçirgenliği bozulduğunda sitoplazmaya sızan Smac/DIABLO, doğrudan IAP'lere bağlanarak onları nötralize eder ve kaspaz aktivasyonunun kesintisiz ilerlemesini güvenceye alır.",
        "examBadge": "🔵 IAP İNHİBİTÖRÜ",
        "aliases": ["smac", "diablo", "smac-diablo"]
    }
}

for k, v in new_glossary.items():
    glossary[k] = v

with open(GLOSSARY_PATH, 'w', encoding='utf-8') as f:
    json.dump(glossary, f, ensure_ascii=False, indent=2)

print(f"Glossary güncellendi! Toplam terim: {len(glossary)}")

# 2. New Encyclopedia Entries
new_encyclopedia_items = [
    {
        "id": "encyc-bak-protein",
        "term": "Bak Proteini (Bcl-2 Homologous Antagonist/Killer)",
        "latinName": "Bcl-2 Antagonist/Killer 1",
        "aliases": ["Bak", "BAK1", "BCL2L7"],
        "category": "Patoloji & Moleküler Biyoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Patoloji Kürsüsü - Robbins Temel Patoloji",
        "definition": "Mitokondri dış membranında yerleşik bulunan, çok alanlı (BH1-BH3) pro-apoptotik Bcl-2 ailesi proteinidir. Bax ile iş birliği yaparak mitokondri geçirgenlik geçiş porlarını açar ve apoptozu başlatır.",
        "lectureContextNotes": "Hücre fizyolojisinde apoptozun intrensek mitokondriyal yolağında yürütücü efektör görevi görür. Sitoplazmadaki Bax'tan farklı olarak Bak doğrudan mitokondri dış zarına ankrajlıdır.",
        "morphologyOrMechanism": "1. Normal durumda mitokondri zarında anti-apoptotik Bcl-2 ve Bcl-xL ile kompleks halinde tutularak inaktive edilir.\n2. DNA hasarı, büyüme faktörü yoksunluğu veya mikrotübül stresi oluştuğunda BH3-only proteinleri (Bid, Bim, Puma) Bcl-2'yi bloke eder.\n3. Serbest kalan Bak molekülleri kendi aralarında ve Bax ile oligomerize olarak mitokondri dış membranında yüksek geçirgenlikli por kanalları (MOMP) oluşturur.\n4. Bu porlardan sitokrom c ve Smac/DIABLO sitoplazmaya dökülerek kaspaz-9 ve kaspaz-3 kaskadını tetikler.",
        "differentialDiagnosis": "Bax sitozolik olup aktivasyonla zora göç eder; Bak ise zaten zarda yerleşiktir. Bcl-2 ve Bcl-xL ise anti-apoptotiktir ve Bak'ı baskılar.",
        "examSpotPearls": [
            "🔴 Bak proteini mitokondri dış zarında yerleşiktir ve Bax ile birlikte pro-apoptotik gözenekleri (MOMP) açar.",
            "🔵 Komite sorusu: Apoptozun mitokondriyal yolağında sitokrom c salınımını doğrudan sağlayan efektör pro-apoptotik proteinler Bax ve Bak'tır."
        ],
        "pitfallsAndWarnings": "Bax ve Bak'ın her ikisinin birden silindiği (knock-out) hücreler intrensek apoptotik uyarılara karşı tamamen dirençlidir.",
        "relatedItems": ["Bax Proteini", "İntrensek Apoptoz Yolağı", "Bcl-2 Proteini", "Sitokrom c"],
        "aiAudit": {"verified": True, "date": "2026-10-03"}
    },
    {
        "id": "encyc-bax-protein",
        "term": "Bax Proteini (Bcl-2-Associated X Protein)",
        "latinName": "Bcl-2-Associated X Protein",
        "aliases": ["Bax", "BCL2L4"],
        "category": "Patoloji & Onkoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Patoloji Kürsüsü - Robbins Patoloji",
        "definition": "Normalde sitozolde inaktif monomer halinde bulunan, apoptotik sinyaller ve p53 etkisiyle mitokondri dış zarına transloke olarak por açan temel pro-apoptotik Bcl-2 ailesi proteinidir.",
        "lectureContextNotes": "Tümör baskılayıcı p53 geninin en kritik transkripsiyonel hedeflerinden biridir. p53 DNA hasarı saptadığında onarılamıyorsa Bax genini transkribe ederek hücreyi apoptoza yönlendirir.",
        "morphologyOrMechanism": "1. p53 veya BH3-only sinyalleri ile konformasyonel değişikliğe uğrar.\n2. Sitozolden mitokondri dış zarına yerleşir ve Bak ile hetero-oligomerler kurar.\n3. Sitokrom c çıkışına izin veren MOMP kanallarını açar.\n4. Foliküler lenfomada t(14;18) ile Bcl-2 aşırı üretildiğinde Bax dimerleri nötralize edilir ve apoptoz engellenir.",
        "differentialDiagnosis": "Bcl-2 (Anti-apoptotik) vs Bax (Pro-apoptotik). Bax/Bcl-2 oranı yüksekse hücre ölür; Bcl-2 yüksekse hücre hayatta kalır.",
        "examSpotPearls": [
            "🔴 Bax sentezi doğrudan tümör süpresör p53 tarafından uyarılır; p53 mutasyonunda Bax üretilemez ve tümör hücreleri apoptozdan kaçar.",
            "🔵 Çıkmış TUS: Mitokondri geçirgenliğini artırarak apoptozu başlatan pro-apoptotik molekül Bax'tır."
        ],
        "pitfallsAndWarnings": "Bax tek başına değil, Bak ile iş birliği yaparak delik açar. İkisinin yokluğunda intrensek yol çalışmaz.",
        "relatedItems": ["Bak Proteini", "p53 Geni", "Bcl-2 Proteini", "Apoptozom"],
        "aiAudit": {"verified": True, "date": "2026-10-03"}
    },
    {
        "id": "encyc-intrinsic-apoptosis",
        "term": "İntrensek (Mitokondriyal) Apoptoz Yolağı",
        "latinName": "Intrinsic Pathway of Apoptosis",
        "aliases": ["Mitokondriyal Yolak", "Mitokondriyal Apoptoz"],
        "category": "Patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Robbins ve Cotran Hastalığın Patolojik Temeli",
        "definition": "Hücre içi stres, DNA hasarı, hipoksi ve büyüme faktörü yokluğu sonucu mitokondri dış zar geçirgenliğinin bozulması ve sitokrom c salınımıyla tetiklenen ana programlı hücre ölümü yoludur.",
        "lectureContextNotes": "Memeli hücrelerinde fizyolojik ve patolojik apoptozun en sık kullanılan yoludur. Büyüme faktörü kesilmesi, radyasyon, kemoterapi ve yanlış katlanmış protein stresi bu yolu tetikler.",
        "morphologyOrMechanism": "1. Sensör Evresi: Hücre içi stres BH3-only proteinlerini (Bim, Bid, Bad, Puma, Noxa) uyarır.\n2. Efektör Evresi: BH3-only molekülleri Bcl-2 ve Bcl-xL'i inhibe ederken, Bax ve Bak'ı aktive eder.\n3. Zardan Kaçış: Bax/Bak oligomerleri MOMP açar; sitokrom c ve Smac/DIABLO sitozole sızar.\n4. Apoptozom Oluşumu: Sitokrom c + Apaf-1 + dATP birleşerek heptamerik apoptozom çarkını kurar.\n5. İnisiyatör Kaspaz: Apoptozom Prokaspaz-9'u keserek aktif Kaspaz-9 üretir.\n6. Yürütücü Kaspazlar: Kaspaz-9, yürütücü Kaspaz-3 ve Kaspaz-6'yı uyarır; hücre içi sitoskeleton ve nükleus laminleri parçalanır.",
        "differentialDiagnosis": "İntrensek yolda inisiyatör kaspaz KASPAZ-9'dur. Ekstrensek yolda ise inisiyatör kaspaz KASPAZ-8'dir. Her iki yolun birleştiği ortak yürütücü kaspaz KASPAZ-3'tür.",
        "examSpotPearls": [
            "🔴 İntrensek yolağın inisiyatör kaspazı Kaspaz-9; yürütücü kaspazı Kaspaz-3'tür.",
            "🔵 Sınav Klasörü: Sitokrom c + Apaf-1 + dATP = Apoptozom kompleksidir ve Prokaspaz-9'u aktive eder."
        ],
        "pitfallsAndWarnings": "Apoptozda membran bütünlüğü korunur, hücresel içerik dışarı sızmaz ve ENFLAMASYON OLUŞMAZ (nekrozdan temel farkı).",
        "relatedItems": ["Bax", "Bak", "Apoptozom", "Kaspaz-9", "Kaspaz-3"],
        "aiAudit": {"verified": True, "date": "2026-10-03"}
    },
    {
        "id": "encyc-extrinsic-apoptosis",
        "term": "Ekstrensek (Ölüm Reseptörü) Apoptoz Yolağı",
        "latinName": "Extrinsic Pathway of Apoptosis",
        "aliases": ["Ölüm Reseptörü Yolağı", "Fas/CD95 Yolağı", "DISC Kompleksi"],
        "category": "Patoloji & İmmünoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Robbins Patoloji & Kuby İmmünoloji",
        "definition": "Hücre zarı yüzeyinde bulunan TNF reseptör ailesine ait ölüm reseptörlerinin (Fas/CD95, TNFR1) ligandları ile uyarılması sonucu kaspaz-8 aktivasyonuyla ilerleyen apoptoz mekanizmasıdır.",
        "lectureContextNotes": "Bağışıklık sisteminde otoreaktif lenfositlerin klonal delesyonunda (negatif seleksiyon) ve sitotoksik T lenfositlerinin virüsle enfekte veya tümör hücrelerini öldürmesinde temel mekanizmadır.",
        "morphologyOrMechanism": "1. Reseptör Ligand Bağlanması: FasL veya TNF-alfa, hücre yüzeyindeki Fas (CD95) veya TNFR1 reseptörlerini trimerize eder.\n2. Adaptör Toplanması: Reseptörün sitoplazmik ölüm alanlarına (Death Domain - DD) FADD adaptör proteini bağlanır.\n3. DISC Oluşumu: FADD'ın DED (Death Effector Domain) bölgesi prokaspaz-8 moleküllerini çekerek DISC (Death-Inducing Signaling Complex) oluşturur.\n4. Kaspaz Aktivasyonu: Prokaspaz-8 otokatalitik olarak aktif Kaspaz-8'e dönüşür.\n5. Çapraz Bağlantı: Kaspaz-8 ya doğrudan Kaspaz-3'ü uyarır (Tip 1 hücre) ya da Bid proteinini kesip tBid yaparak mitokondriyal yolağı da devreye sokar (Tip 2 hücre).\n6. Doğal Fren: FLIP proteini prokaspaz-8 taklidi yaparak DISC'e bağlanır ve yolağı inhibe eder.",
        "differentialDiagnosis": "Ekstrensek yolun inisiyatörü KASPAZ-8 ve KASPAZ-10'dur; intrensek yolun inisiyatörü KASPAZ-9'dur. İnhibitörü FLIP'tir.",
        "examSpotPearls": [
            "🔴 Ekstrensek yolağın inisiyatör kaspazı Kaspaz-8'dir.",
            "🔵 Çıkmış TUS: Ekstrensek yolağı mitokondriyal intrensek yolağa bağlayan çapraz köprü molekülü Kaspaz-8 tarafından kesilen Bid proteinidir (tBid)."
        ],
        "pitfallsAndWarnings": "Bazı virüsler (örneğin herpes virüsleri) viral FLIP üreterek CTL kaynaklı ekstrensek apoptozdan kaçarlar.",
        "relatedItems": ["Fas/CD95", "Kaspaz-8", "DISC Kompleksi", "Bid Proteini", "FLIP"],
        "aiAudit": {"verified": True, "date": "2026-10-03"}
    }
]

# Mevcut olanları güncelle veya ekle
existing_ids = {item['id']: idx for idx, item in enumerate(encyclopedia)}
for new_item in new_encyclopedia_items:
    if new_item['id'] in existing_ids:
        encyclopedia[existing_ids[new_item['id']]] = new_item
    else:
        encyclopedia.append(new_item)

with open(ENCYCLOPEDIA_PATH, 'w', encoding='utf-8') as f:
    json.dump(encyclopedia, f, ensure_ascii=False, indent=2)

print(f"Ansiklopedi güncellendi! Toplam madde: {len(encyclopedia)}")
