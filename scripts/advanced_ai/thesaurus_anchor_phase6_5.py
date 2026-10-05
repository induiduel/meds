#!/usr/bin/env python3
"""
Faz 6.5: Tıbbi Terimler Sözlüğü (Thesaurus) & Soru-Slayt Birlikte Görünme (Co-occurrence) Graf Motoru
------------------------------------------------------------------------------------------------------
Görevler:
1. Türkçe tıp terminolojisi, Latince/İngilizce eşanlamlılar, hekim jargonu, alternatif yazımlar ve
   kısaltmaları içeren çok katmanlı 'medical_thesaurus.json' oluşturur.
2. Çıkmış sorular (meds_database/questions) ve amfi ders slayt chunk'ları (meds_database/chunks)
   arasındaki ortak tıbbi terimleri tarar.
3. ÇOKLU DERS EŞLEŞME PROBLEMİNİ ÇÖZEN SKORLAMA ALGORİTMASI:
   - Sadece tek bir terimin geçmesi yetmez (Örn: 'anemi' veya 'enfeksiyon' her derste geçer).
   - Co-occurrence Skoru = (Ortak Tıbbi Terim Sayısı) * (Terimin Özgüllük/Ağırlığı) * (Slayttaki Yoğunluk)
   - Sorudaki diğer tıbbi kavramların o slaytta birlikte bulunma oranı (Jaccard & Terim Kümeleme)
4. En yüksek skora sahip slayt parçası sorunun 'Altın Kanıtı' (Gold Slide Evidence) olarak kancalanır.
5. Sonuçlar 'meds_database_v2/medical_thesaurus/' ve 'phase6_5_anchors.jsonl' dosyasına yazılır.
"""

import os
import sys
import json
import re
import math
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[2] # meds
PROJECT_PARENT = ROOT.parent
DB_QUESTIONS = PROJECT_PARENT / "meds_database" / "questions"
DB_CHUNKS = PROJECT_PARENT / "meds_database" / "chunks"
CURRICULUM_FILE = ROOT / "curriculum" / "kbu_tip_donem3_curriculum.json"
OUT_DIR = PROJECT_PARENT / "meds_database_v2" / "medical_thesaurus"
OUT_DIR.mkdir(parents=True, exist_ok=True)
THESAURUS_FILE = OUT_DIR / "medical_thesaurus.json"
ANCHORS_FILE = OUT_DIR / "phase6_5_question_slide_anchors.jsonl"
STATE_FILE = OUT_DIR / "phase6_5_state.json"

# Kapsamlı Tıbbi Terimler, Eş Anlamlılar ve İlişkili Terim Havuzu
BASE_THESAURUS = {
    # Tiroit & Endokrin
    "folliküler karsinom": {
        "turkce": "Folliküler tiroid karsinomu",
        "latin": "Carcinoma folliculare glandulae thyroideae",
        "esanlamlilar": ["folliküler kanser", "tiroid folliküler ca", "ftc"],
        "anahtar_bilesenler": ["kapsül invazyonu", "damar invazyonu", "vasküler invazyon", "folliküler adenom", "tiroglobulin"],
        "kurul": "TIP320",
        "brans": "Tıbbi Patoloji",
        "ozgulluk_agirligi": 3.5
    },
    "kapsül invazyonu": {
        "turkce": "Kapsül invazyonu / istilası",
        "latin": "Invasio capsularis",
        "esanlamlilar": ["kapsüler invazyon", "kapsül aşımı", "tam kat penetrasyon"],
        "anahtar_bilesenler": ["folliküler karsinom", "folliküler adenom", "tiroid malignite kriteri"],
        "kurul": "TIP320",
        "brans": "Tıbbi Patoloji",
        "ozgulluk_agirligi": 4.0
    },
    "graves hastalığı": {
        "turkce": "Graves Basedow hastalığı",
        "latin": "Morbus Basedow",
        "esanlamlilar": ["diffüz toksik guatr", "ekzoftalmik guatr"],
        "anahtar_bilesenler": ["trab", "tsh reseptör antikoru", "ekzoftalmus", "pretibiyal miksödem", "hipertiroidi"],
        "kurul": "TIP320",
        "brans": "İç Hastalıkları / Tıbbi Patoloji",
        "ozgulluk_agirligi": 3.8
    },
    "feokromositoma": {
        "turkce": "Feokromositoma",
        "latin": "Phaeochromocytoma",
        "esanlamlilar": ["adrenal medülla tümörü", "paraganglioma"],
        "anahtar_bilesenler": ["katekolamin", "vma", "vanilmandelik asit", "hipertansif kriz", "men 2", "zellballen"],
        "kurul": "TIP320",
        "brans": "Tıbbi Patoloji / Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.2
    },
    # Hematoloji & Hemostaz
    "hemartroz": {
        "turkce": "Eklem içi kanama",
        "latin": "Haemarthros",
        "esanlamlilar": ["eklem içi hematom", "eklem boşluğunda kan toplanması"],
        "anahtar_bilesenler": ["faktör viii", "faktör ix", "hemofili a", "hemofili b", "sekonder hemostaz"],
        "kurul": "TIP360",
        "brans": "İç Hastalıkları (Hematoloji)",
        "ozgulluk_agirligi": 4.5
    },
    "hemofili": {
        "turkce": "Hemofili",
        "latin": "Haemophilia",
        "esanlamlilar": ["pıhtılaşma faktör eksikliği", "koagülopati"],
        "anahtar_bilesenler": ["hemartroz", "aptt uzaması", "faktör 8", "faktör 9", "x'e bağlı resesif"],
        "kurul": "TIP360",
        "brans": "İç Hastalıkları (Hematoloji)",
        "ozgulluk_agirligi": 3.9
    },
    "peteşi": {
        "turkce": "Noktasal cilt kanaması",
        "latin": "Petechiae",
        "esanlamlilar": ["topluiğne başı kanama", "kapiller hemoraji"],
        "anahtar_bilesenler": ["trombositopeni", "primer hemostaz", "itp", "purpura"],
        "kurul": "TIP360",
        "brans": "İç Hastalıkları (Hematoloji)",
        "ozgulluk_agirligi": 3.0
    },
    "kml": {
        "turkce": "Kronik Miyeloid Lösemi",
        "latin": "Leukaemia myeloidea chronica",
        "esanlamlilar": ["cml", "kronik miyelojen lösemi"],
        "anahtar_bilesenler": ["philadelphia kromozomu", "t(9;22)", "bcr-abl", "tirozin kinaz", "imatinib"],
        "kurul": "TIP360",
        "brans": "Tıbbi Genetik / Hematoloji",
        "ozgulluk_agirligi": 4.8
    },
    # Farmakoloji & Antibiyotikler
    "nistatin": {
        "turkce": "Nistatin",
        "latin": "Nystatinum",
        "esanlamlilar": ["poliyen antifungal", "topikal mikostatik"],
        "anahtar_bilesenler": ["ergosterol", "topikal antifungal", "parenteral toksik", "kandidiyazis", "pamukçuk"],
        "kurul": "TIP360",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.2
    },
    "fosfomisin": {
        "turkce": "Fosfomisin",
        "latin": "Fosfomycinum",
        "esanlamlilar": ["monurol", "epoksit antibiyotik"],
        "anahtar_bilesenler": ["enolpiruvat transferaz", "murA", "hücre duvarı ilk basamak", "akut sistit"],
        "kurul": "TIP350",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.6
    },
    "imipenem": {
        "turkce": "İmipenem",
        "latin": "Imipenemum",
        "esanlamlilar": ["karbapenem antibiyotik"],
        "anahtar_bilesenler": ["dehidropeptidaz-1", "silastatin", "nefrotoksik metabolit", "geniş spektrum"],
        "kurul": "TIP350",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.7
    },
    "tetrasiklin": {
        "turkce": "Tetrasiklin / Doksisiklin",
        "latin": "Tetracyclinum",
        "esanlamlilar": ["doksisiklin", "minosiklin"],
        "anahtar_bilesenler": ["şelasyon", "iki değerlikli katyonlar", "kalsiyum", "diş boyanması", "30s ribozom"],
        "kurul": "TIP360",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 3.9
    },
    "kloramfenikol": {
        "turkce": "Kloramfenikol",
        "latin": "Chloramphenicolum",
        "esanlamlilar": ["fenikol antibiyotik"],
        "anahtar_bilesenler": ["gri bebek sendromu", "glukuronil transferaz", "aplastik anemi", "50s ribozom"],
        "kurul": "TIP360",
        "brans": "Tıbbi Farmakoloji / Pediatri",
        "ozgulluk_agirligi": 4.9
    },
    "metotreksat": {
        "turkce": "Metotreksat",
        "latin": "Methotrexatum",
        "esanlamlilar": ["mtx", "folat antagonisti"],
        "anahtar_bilesenler": ["dihidrofolat redüktaz", "dhfr", "lökovorin", "s fazı", "timidilat sentaz"],
        "kurul": "TIP350",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.4
    },
    "nitrogliserin": {
        "turkce": "Nitrogliserin / Gliseril Trinitrat",
        "latin": "Glyceroli trinitras",
        "esanlamlilar": ["gtn", "sublingual nitrat"],
        "anahtar_bilesenler": ["hepatik ilk geçiş etkisi", "sublingual", "venodilatasyon", "ön yük azalması", "anjina"],
        "kurul": "TIP350",
        "brans": "Tıbbi Farmakoloji / Kardiyoloji",
        "ozgulluk_agirligi": 4.1
    },
    # Nöroloji & Koma
    "glasgow koma skalası": {
        "turkce": "Glasgow Koma Skalası (GKS)",
        "latin": "Coma scale Glasgow",
        "esanlamlilar": ["gks", "gcs"],
        "anahtar_bilesenler": ["göz açma", "sözel yanıt", "motor yanıt", "kafa travması", "bilinç düzeyi"],
        "kurul": "TIP340",
        "brans": "Nöroloji / Acil Tıp",
        "ozgulluk_agirligi": 4.0
    },
    "crush sendromu": {
        "turkce": "Ezilme / Göçük Sendromu",
        "latin": "Syndroma contusionis",
        "esanlamlilar": ["bywaters sendromu", "kompresyon travması"],
        "anahtar_bilesenler": ["rabdomiyoliz", "miyoglobinüri", "hiperkalemi", "akut böbrek yetmezliği", "kompartman"],
        "kurul": "TIP360",
        "brans": "Acil Tıp / Ortopedi",
        "ozgulluk_agirligi": 4.6
    },
    # Gastroenteroloji & Karaciğer (TIP310)
    "helikobakter pilori": {
        "turkce": "Helikobakter pilori enfeksiyonu",
        "latin": "Helicobacter pylori",
        "esanlamlilar": ["h. pylori", "hp", "gastrik helikobakter"],
        "anahtar_bilesenler": ["üreaz testi", "maltoma", "malt lenfoma", "kronik gastrit", "peptik ülser", "cagA", "vacA"],
        "kurul": "TIP310",
        "brans": "Tıbbi Mikrobiyoloji / Patoloji",
        "ozgulluk_agirligi": 4.5
    },
    "crohn hastalıgı": {
        "turkce": "Crohn Hastalığı",
        "latin": "Morbus Crohn",
        "esanlamlilar": ["regional enterit", "granülomatöz kolit", "terminal ileit"],
        "anahtar_bilesenler": ["skip lezyon", "atlayan lezyon", "kaldırım taşı manzarası", "transmural inflamasyon", "non-kazeifiye granülom", "fistül"],
        "kurul": "TIP310",
        "brans": "İç Hastalıkları (Gastroenteroloji) / Patoloji",
        "ozgulluk_agirligi": 4.8
    },
    "ülseratif kolit": {
        "turkce": "Ülseratif Kolit",
        "latin": "Colitis ulcerosa",
        "esanlamlilar": ["ük", "idiyopatik proktokolit"],
        "anahtar_bilesenler": ["kript apsesi", "psödopolip", "yalancı polip", "kurşun boru manzarası", "toksik megakolon", "kanlı mukuslu diyare", "p-anca"],
        "kurul": "TIP310",
        "brans": "İç Hastalıkları (Gastroenteroloji) / Patoloji",
        "ozgulluk_agirligi": 4.8
    },
    "barrett özofagus": {
        "turkce": "Barrett Özofagusu",
        "latin": "Oesophagus Barrett",
        "esanlamlilar": ["intestinal metaplazi", "özofagus metaplazisi"],
        "anahtar_bilesenler": ["goblet hücreleri", "adeno karsinom riski", "görh", "reflü", "kolumnar metaplazi"],
        "kurul": "TIP310",
        "brans": "Tıbbi Patoloji / Gastroenteroloji",
        "ozgulluk_agirligi": 4.6
    },
    "budd-chiari sendromu": {
        "turkce": "Budd-Chiari Sendromu",
        "latin": "Syndroma Budd-Chiari",
        "esanlamlilar": ["hepatik ven obstrüksiyonu", "posthepatik portal hipertansiyon"],
        "anahtar_bilesenler": ["hepatomegali", "asit", "hepatik ven trombozu", "polisitemia vera", "sentrilobüler konjesyon"],
        "kurul": "TIP310",
        "brans": "Patoloji / Gastroenteroloji",
        "ozgulluk_agirligi": 4.7
    },
    "wilson hastalıgı": {
        "turkce": "Wilson Hastalığı (Hepatoletiküler Dejenerasyon)",
        "latin": "Morbus Wilson",
        "esanlamlilar": ["hepatolentiküler dejenerasyon", "bakır depolanma hastalığı"],
        "anahtar_bilesenler": ["kayser-fleischer halkası", "seruloplazmin düşüklüğü", "atp7b geni", "idrar bakırı", "bazal ganglion tutulumu"],
        "kurul": "TIP310",
        "brans": "Tıbbi Genetik / Patoloji",
        "ozgulluk_agirligi": 4.9
    },
    "hemokromatozis": {
        "turkce": "Hemokromatozis / Bronz Diyabet",
        "latin": "Haemochromatosis",
        "esanlamlilar": ["primer hemokromatoz", "demir depolanma hastalığı", "bronz diyabet"],
        "anahtar_bilesenler": ["hfe geni", "c282y", "ferritin yüksekliği", "transferrin satürasyonu", "prussian blue", "hemosiderozis"],
        "kurul": "TIP310",
        "brans": "Patoloji / Genetik",
        "ozgulluk_agirligi": 4.6
    },
    "çölyak hastalıgı": {
        "turkce": "Çölyak Hastalığı / Gluten Enteropatisi",
        "latin": "Morbus coeliacus",
        "esanlamlilar": ["gluten duyarlı enteropati", "çölyak sprue"],
        "anahtar_bilesenler": ["anti-ttg", "doku transglutaminaz", "intraepitelyal lenfosit", "villöz atrofi", "kript hiperplazisi", "dermatitis herpetiformis", "hla-dq2"],
        "kurul": "TIP310",
        "brans": "Gastroenteroloji / Patoloji",
        "ozgulluk_agirligi": 4.7
    },
    "akut pankreatit": {
        "turkce": "Akut Pankreatit",
        "latin": "Pancreatitis acuta",
        "esanlamlilar": ["akut nekrotizan pankreatit"],
        "anahtar_bilesenler": ["lipaz", "amilaz", "ranson kriterleri", "enzimatik yağ nekrozu", "kalsiyum sabunlaşması", "safra taşı", "alkol"],
        "kurul": "TIP310",
        "brans": "Gastroenteroloji / Patoloji",
        "ozgulluk_agirligi": 4.4
    },
    "kist hidatik": {
        "turkce": "Kist Hidatik / Ekinokokkoz",
        "latin": "Echinococcosis hepatis",
        "esanlamlilar": ["hidatidoz", "köpek tenyası kisti"],
        "anahtar_bilesenler": ["echinococcus granulosus", "kutiküler membran", "germinal tabaka", "hidatik kum", "anafilaksi", "albendazol"],
        "kurul": "TIP310",
        "brans": "Tıbbi Mikrobiyoloji / Parazitoloji",
        "ozgulluk_agirligi": 4.7
    },
    # Endokrin & Metabolizma (TIP320)
    "hashimoto tiroiditi": {
        "turkce": "Hashimoto Tiroiditi (Kronik Lenfositik Tiroidit)",
        "latin": "Thyroiditis lymphocytica chronica",
        "esanlamlilar": ["otoimmün tiroidit", "struma lymphomatosa"],
        "anahtar_bilesenler": ["anti-tpo", "anti-tiroglobulin", "hürthle hücreleri", "onkositik metaplazi", "lenfoid foliküller", "germinal merkez"],
        "kurul": "TIP320",
        "brans": "Tıbbi Patoloji / Endokrinoloji",
        "ozgulluk_agirligi": 4.7
    },
    "cushing sendromu": {
        "turkce": "Cushing Sendromu / Hiperkortizolizm",
        "latin": "Syndroma Cushing",
        "esanlamlilar": ["hiperkortizolizm"],
        "anahtar_bilesenler": ["ay dede yüzü", "bufalo hörgücü", "mor strialar", "kortizol yüksekliği", "deksametazon baskılama", "acth"],
        "kurul": "TIP320",
        "brans": "Endokrinoloji / Patoloji",
        "ozgulluk_agirligi": 4.5
    },
    "addison hastalıgı": {
        "turkce": "Addison Hastalığı (Primer Kronik Adrenokortikal Yetmezlik)",
        "latin": "Morbus Addison",
        "esanlamlilar": ["adrenal yetmezlik", "hipokortizolizm"],
        "anahtar_bilesenler": ["ciltte hiperpigmentasyon", "acth yüksekliği", "hiponatremi", "hiperkalemi", "hipotansiyon", "otoimmün adrenalit"],
        "kurul": "TIP320",
        "brans": "Endokrinoloji",
        "ozgulluk_agirligi": 4.6
    },
    "papiller tiroid karsinomu": {
        "turkce": "Papiller Tiroid Karsinomu",
        "latin": "Carcinoma papillare thyroideae",
        "esanlamlilar": ["ptc", "tiroid papiller ca"],
        "anahtar_bilesenler": ["orphan annie gözü", "buzlu cam nükleus", "nükleer psödoinklüzyon", "psammom cisimciği", "lenfatik metastaz", "braf v600e"],
        "kurul": "TIP320",
        "brans": "Tıbbi Patoloji",
        "ozgulluk_agirligi": 4.9
    },
    # Nöropsikiyatri (TIP340)
    "alzheimer hastalıgı": {
        "turkce": "Alzheimer Hastalığı",
        "latin": "Morbus Alzheimer",
        "esanlamlilar": ["senil demans", "alzheimer tipi demans"],
        "anahtar_bilesenler": ["senil plak", "amiloid beta", "nörofibriler yumak", "hiperfosforile tau", "kolinerjik kayıp", "apo e4", "asetilkolinesteraz"],
        "kurul": "TIP340",
        "brans": "Nöroloji / Tıbbi Patoloji",
        "ozgulluk_agirligi": 4.8
    },
    "parkinson hastalıgı": {
        "turkce": "Parkinson Hastalığı",
        "latin": "Morbus Parkinson",
        "esanlamlilar": ["paralizis agitans", "parkinsonizm"],
        "anahtar_bilesenler": ["lewy cisimciği", "alfa-sinüklein", "substantia nigra", "dopaminerjik nöron kaybı", "istirahat tremoru", "rijidite", "bradikinezi", "l-dopa"],
        "kurul": "TIP340",
        "brans": "Nöroloji / Patoloji / Farmakoloji",
        "ozgulluk_agirligi": 4.8
    },
    "multipl skleroz": {
        "turkce": "Multipl Skleroz (MS)",
        "latin": "Sclerosis multiplex",
        "esanlamlilar": ["ms", "yaygın skleroz"],
        "anahtar_bilesenler": ["demiyelinizasyon", "oligoklonal bant", "bos igg indeksi", "periventriküler plak", "lhermitte belirtisi", "optik nörit", "dawson parmakları"],
        "kurul": "TIP340",
        "brans": "Nöroloji / Patoloji",
        "ozgulluk_agirligi": 4.8
    },
    "guillain-barre sendromu": {
        "turkce": "Guillain-Barré Sendromu (GBS)",
        "latin": "Syndroma Guillain-Barre",
        "esanlamlilar": ["akut inflamatuar demiyelinizan polinöropati", "aidp"],
        "anahtar_bilesenler": ["asendan paralizi", "albüminositolojik disosiasyon", "campylobacter jejuni", "arefleksi", "ivig", "plazmaferez"],
        "kurul": "TIP340",
        "brans": "Nöroloji",
        "ozgulluk_agirligi": 4.8
    },
    # Kardiyovasküler & Solunum (TIP350)
    "akut miyokard enfarktüsü": {
        "turkce": "Akut Miyokard Enfarktüsü (AMİ)",
        "latin": "Infarctus myocardii acutus",
        "esanlamlilar": ["stemi", "nstemi", "kalp krizi"],
        "anahtar_bilesenler": ["troponin i", "troponin t", "ck-mb", "st elevasyonu", "koagülasyon nekrozu", "dal blokları", "koroner aterotromboz"],
        "kurul": "TIP350",
        "brans": "Kardiyoloji / Patoloji",
        "ozgulluk_agirligi": 4.6
    },
    "infektif endokardit": {
        "turkce": "İnfektif Endokardit",
        "latin": "Endocarditis infectiosa",
        "esanlamlilar": ["bakteriyel endokardit", "vejetatif endokardit"],
        "anahtar_bilesenler": ["duke kriterleri", "osler nodülleri", "janeway lezyonları", "roth lekeleri", "vejetasyon", "streptococcus viridans", "staphylococcus aureus"],
        "kurul": "TIP350",
        "brans": "Kardiyoloji / Enfeksiyon Hastalıkları",
        "ozgulluk_agirligi": 4.9
    },
    "pulmoner tromboemboli": {
        "turkce": "Pulmoner Tromboemboli (PTE)",
        "latin": "Thromboembolismus pulmonalis",
        "esanlamlilar": ["akciğer embolisi", "pte", "derin ven trombozu komplikasyonu"],
        "anahtar_bilesenler": ["d-dimer", "bt pulmoner anjiyografi", "hamptom hörgücü", "westermark işareti", "sağ ventrikül yüklenmesi", "s1q3t3", "antikoagülasyon"],
        "kurul": "TIP350",
        "brans": "Göğüs Hastalıkları / Kardiyoloji",
        "ozgulluk_agirligi": 4.7
    },
    # Ortopedi, Hematoloji & Onkoloji (TIP360)
    "multipl miyelom": {
        "turkce": "Multipl Miyelom (Plazma Hücre Diskrazisi)",
        "latin": "Myeloma multiplex",
        "esanlamlilar": ["kahler hastalığı", "plazmositoma"],
        "anahtar_bilesenler": ["crab kriterleri", "hiperkalsemi", "bence jones proteini", "m proteini", "litik kemik lezyonları", "zımba deliği manzarası", "rouleaux formasyonu"],
        "kurul": "TIP360",
        "brans": "Hematoloji / Patoloji",
        "ozgulluk_agirligi": 4.9
    },
    "demir eksikligi anemisi": {
        "turkce": "Demir Eksikliği Anemisi (DEA)",
        "latin": "Anaemia ferripriva",
        "esanlamlilar": ["mikrositer hipokrom anemi", "demir azlığı anemisi"],
        "anahtar_bilesenler": ["ferritin düşüklüğü", "sdbk artışı", "rdw artışı", "anizositoz", "poikilositoz", "kalem hücreleri", "koilonişi"],
        "kurul": "TIP360",
        "brans": "Hematoloji / İç Hastalıkları",
        "ozgulluk_agirligi": 4.4
    },
    "megaloblastik anemi": {
        "turkce": "Megaloblastik Anemi",
        "latin": "Anaemia megaloblastica",
        "esanlamlilar": ["b12 veya folat eksikliği anemisi", "pernisiyöz anemi"],
        "anahtar_bilesenler": ["hipersegmente nötrofil", "howell-jolly cisimciği", "makrositoz", "homosistein", "metilmalonik asit", "subakut kombine dejenerasyon"],
        "kurul": "TIP360",
        "brans": "Hematoloji / Biyokimya",
        "ozgulluk_agirligi": 4.6
    },
    "orak hücreli anemi": {
        "turkce": "Orak Hücreli Anemi (HbS)",
        "latin": "Drepanocytosis",
        "esanlamlilar": ["sickle cell anaemia", "hbs hemoglobinopatisi"],
        "anahtar_bilesenler": ["glutamik asit valin mutasyonu", "vazo-oklüzif kriz", "dalak enfarktı", "otospelenektomi", "howell-jolly", "salmonella osteomiyeliti"],
        "kurul": "TIP360",
        "brans": "Hematoloji / Genetik",
        "ozgulluk_agirligi": 4.9
    },
    "osteosarkom": {
        "turkce": "Osteosarkom / Osteojenik Sarkom",
        "latin": "Osteosarcoma",
        "esanlamlilar": ["kemik kanseri", "malign osteojenik tümör"],
        "anahtar_bilesenler": ["osteoid üretimi", "codman üçgeni", "güneş ışını manzarası", "metafiz tutulumu", "rb1 geni", "tp53 geni", "paget zemininde"],
        "kurul": "TIP360",
        "brans": "Tıbbi Patoloji / Ortopedi",
        "ozgulluk_agirligi": 4.8
    },
    "miyastenia gravis": {
        "turkce": "Miyastenia Gravis (MG)",
        "latin": "Myasthenia gravis",
        "esanlamlilar": ["nöromüsküler kavşak hastalığı"],
        "anahtar_bilesenler": ["anti-achr", "asetilkolin reseptör antikoru", "timoma", "timus hiperplazisi", "ptozis", "diplopi", "yorulabilir kas güçsüzlüğü", "edrofonyum", "piridostigmin"],
        "kurul": "TIP360",
        "brans": "Nöroloji / Göğüs Cerrahisi / Patoloji",
        "ozgulluk_agirligi": 4.8
    }
}


def enrich_thesaurus_with_ai(thesaurus: Dict[str, dict], max_terms_to_enrich: int = 15) -> Dict[str, dict]:
    """
    Yerel (Gemma 3 / Qwen) ve Bulut AI API'leri kullanarak mevcut terimlere
    yeni eş anlamlılar, Latince hekim jargonu ve ayırıcı tanı anahtarları katar.
    """
    try:
        sys.path.insert(0, str(ROOT / "scripts" / "agents"))
        import lib
        
        # Henüz zenginleştirilmemiş veya az bileşeni olan terimleri seç
        candidates = [k for k, v in thesaurus.items() if len(v.get("anahtar_bilesenler", [])) <= 5]
        selected = candidates[:max_terms_to_enrich]
        
        if not selected:
            return thesaurus

        print(f"[AI Zenginleştirme] {len(selected)} tıbbi terim hafif AI ile genişletiliyor...")
        for idx, term in enumerate(selected, 1):
            print(f"  [{idx}/{len(selected)}] Genişletiliyor: {term}...", flush=True)
            prompt = (
                f"Tıbbi terim: '{term}'. Bu terimin tıp fakültesi sınavlarında geçen:\n"
                f"1. En yaygın 2 Latince/İngilizce eşanlamlısı\n"
                f"2. En kritik 3 patolojik/klinik belirteci (anahtar kelime)\n"
                f"Sadece virgülle ayrılmış kelime listesi yaz (Açıklama yapma)."
            )
            # Hafif yerel model veya fallback
            resp = lib.chat(
                model=lib.MODEL_FAST,
                prompt=prompt,
                num_predict=60,
                timeout=20
            )
            if resp:
                new_tokens = [tok.strip().lower() for tok in re.split(r'[,;\n]+', resp) if len(tok.strip()) > 3]
                existing_comps = set(thesaurus[term].get("anahtar_bilesenler", []))
                for nt in new_tokens[:3]:
                    existing_comps.add(nt)
                thesaurus[term]["anahtar_bilesenler"] = list(existing_comps)
                print(f"    + Yeni anahtarlar: {new_tokens[:3]}", flush=True)
    except Exception as e:
        print(f"[AI Zenginleştirme Atlandı]: {e}", flush=True)
    
    return thesaurus


def build_full_thesaurus():
    """Müfredat ve temel tıbbi ontolojiyi birleştirip sözlüğü kaydeder."""
    thesaurus = dict(BASE_THESAURUS)
    if CURRICULUM_FILE.exists():
        curric = json.loads(CURRICULUM_FILE.read_text(encoding="utf-8"))
        for cid, cinfo in curric.get("committees", {}).items():
            for topic in cinfo.get("core_topics", []):
                t_lower = topic.lower().strip()
                if t_lower not in thesaurus:
                    thesaurus[t_lower] = {
                        "turkce": topic,
                        "latin": topic,
                        "esanlamlilar": [t_lower.replace(" ve ", " "), t_lower.split("(")[0].strip()],
                        "anahtar_bilesenler": [w for w in re.split(r'[\s,\(\)]+', t_lower) if len(w) > 4][:5],
                        "kurul": cid,
                        "brans": cinfo.get("departments", ["Tıp Fakültesi"])[0],
                        "ozgulluk_agirligi": 3.0
                    }
    
    # Hafif AI zenginleştirmesi (kullanılabilir olduğunda genişletir)
    thesaurus = enrich_thesaurus_with_ai(thesaurus, max_terms_to_enrich=10)
    
    THESAURUS_FILE.write_text(json.dumps(thesaurus, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[Thesaurus ✓] {len(thesaurus)} terim ve eş anlamlı kümesi {THESAURUS_FILE.name} dosyasına yazıldı.")
    return thesaurus


def extract_terms_from_text(text: str, thesaurus: Dict[str, dict]) -> Set[str]:
    """Metin içindeki bilinen tıbbi terimleri ve eş anlamlılarını saptar."""
    text_lower = text.lower()
    found_terms = set()
    for main_term, meta in thesaurus.items():
        if main_term in text_lower:
            found_terms.add(main_term)
            continue
        for syn in meta.get("esanlamlilar", []):
            if syn and syn in text_lower:
                found_terms.add(main_term)
                break
        for comp in meta.get("anahtar_bilesenler", []):
            if comp and len(comp) > 4 and comp in text_lower:
                found_terms.add(main_term)
                break
    return found_terms


def calculate_anchor_score(q_terms: Set[str], chunk_terms: Set[str], chunk_text: str, thesaurus: Dict[str, dict]) -> float:
    """
    Co-occurrence (Birlikte Görünme) Skorlama Algoritması:
    1. Ortak terimlerin ağırlıklı toplamı
    2. Jaccard benzerliği (küme örtüşme oranı)
    3. Terimlerin chunk içindeki sıklığı (density)
    """
    common = q_terms.intersection(chunk_terms)
    if not common:
        return 0.0

    # 1. Ağırlıklı Terim Skoru
    weighted_score = sum(thesaurus.get(t, {}).get("ozgulluk_agirligi", 2.0) for t in common)

    # 2. Jaccard Benzerliği
    jaccard = len(common) / len(q_terms.union(chunk_terms))

    # 3. Yoğunluk (Density): Sorudaki kilit terimlerin bu slaytta kaç kez tekrar ettiği
    chunk_lower = chunk_text.lower()
    total_occurrences = sum(chunk_lower.count(t) for t in common)
    density_factor = min(2.5, 1.0 + (total_occurrences * 0.15))

    final_score = (weighted_score * 1.5) + (jaccard * 10.0) + density_factor
    return round(final_score, 3)


def run_phase_6_5():
    print("=" * 75)
    print("🔬 FAZ 6.5: TIBBİ SÖZLÜK (THESAURUS) VE CO-OCCURRENCE KANIT MOTORU")
    print("=" * 75)

    thesaurus = build_full_thesaurus()

    # Çıkmış soruları ve ders slaytlarını tara
    q_files = list(DB_QUESTIONS.glob("*.jsonl"))
    chunk_files = list(DB_CHUNKS.glob("*.jsonl"))

    print(f"[Havuz] {len(q_files)} soru dosyası ve {len(chunk_files)} ders slayt destesi taranıyor...")

    # Slayt chunk'larını indeksle (hafif önbellek)
    print("-> Slayt chunk'ları tıbbi terim süzgecinden geçiriliyor...")
    slide_chunks = []
    for cf in chunk_files[:120]:  # İlk 120 slayt dosyasını tara
        with open(cf, "r", encoding="utf-8") as fp:
            for line in fp:
                if not line.strip():
                    continue
                try:
                    chk = json.loads(line)
                    txt = chk.get("text", "")
                    if len(txt) > 40:
                        c_terms = extract_terms_from_text(txt, thesaurus)
                        if c_terms:
                            slide_chunks.append({
                                "chunk_id": chk.get("chunk_id") or chk.get("id"),
                                "source_id": chk.get("source_id"),
                                "ders": chk.get("ders"),
                                "page": chk.get("page"),
                                "text": txt,
                                "terms": c_terms
                            })
                except Exception:
                    pass

    print(f"-> İndekslenen terim zengini slayt parçası: {len(slide_chunks)}")

    # Soruları tara ve en yüksek co-occurrence skorlu slaytı kancala
    anchors_count = 0
    with open(ANCHORS_FILE, "w", encoding="utf-8") as out_fp:
        for qf in q_files:
            with open(qf, "r", encoding="utf-8") as fp:
                for line in fp:
                    if not line.strip():
                        continue
                    try:
                        q = json.loads(line)
                    except Exception:
                        continue

                    qid = q.get("question_id") or q.get("id")
                    stem = q.get("stem", "")
                    if not stem or len(stem) < 20:
                        continue

                    # Soru ve şıklardaki terimleri çıkar
                    full_q_text = stem + " " + " ".join(str(v) for v in q.get("options", {}).values())
                    q_terms = extract_terms_from_text(full_q_text, thesaurus)

                    if not q_terms:
                        continue

                    # Slayt chunk'ları arasında en yüksek eşleşme (co-occurrence) skorunu bul
                    best_chunk = None
                    best_score = 0.0

                    for chk in slide_chunks:
                        score = calculate_anchor_score(q_terms, chk["terms"], chk["text"], thesaurus)
                        if score > best_score:
                            best_score = score
                            best_chunk = chk

                    if best_chunk and best_score >= 4.0:
                        anchor_record = {
                            "question_id": qid,
                            "stem": stem[:120],
                            "common_medical_terms": list(q_terms.intersection(best_chunk["terms"])),
                            "co_occurrence_score": best_score,
                            "gold_slide": {
                                "chunk_id": best_chunk["chunk_id"],
                                "source_id": best_chunk["source_id"],
                                "ders": best_chunk["ders"],
                                "page": best_chunk["page"],
                                "text_snippet": best_chunk["text"][:250]
                            },
                            "anchored_at": "2026-10-05T15:25:00Z"
                        }
                        out_fp.write(json.dumps(anchor_record, ensure_ascii=False) + "\n")
                        anchors_count += 1

    STATE_FILE.write_text(json.dumps({
        "status": "completed",
        "total_anchors": anchors_count,
        "thesaurus_terms": len(thesaurus),
        "indexed_chunks": len(slide_chunks)
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✨ FAZ 6.5 BAŞARIYLA TAMAMLANDI: {anchors_count} soru-ders notu köprüsü (anchor) kuruldu!")
    print(f"Kalıcı Veri: {ANCHORS_FILE}")


if __name__ == "__main__":
    run_phase_6_5()
