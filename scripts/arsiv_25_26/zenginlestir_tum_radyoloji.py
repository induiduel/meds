#!/usr/bin/env python3
"""
Kurul 2 Radyolojik ve Tanısal Görüntü Zenginleştirme Motoru
Uygulanan Dersler:
1. y25-k2-12-kafa-travmalari
2. y25-k2-13-spinal-travmalar
3. y25-k2-64-omurga-tumorleri
4. y25-k2-14-beyin-tumorleri
5. y25-k2-03-sss-hasar-bicimleri-odem-hidrosefali-herniasyon
"""
import sys, os, json, re, hashlib
from pathlib import Path

MEDS = Path('/home/indu/medsor/meds')
ARSIV = MEDS / 'data' / 'arsiv_25_26' / 'sesli_anlatim'
DB_25_26 = Path('/home/indu/medsor/meds_database_25_26')
PDF_DIR = DB_25_26 / 'pdf' / 'kurul2'

sys.path.insert(0, str(MEDS / 'scripts' / 'cizim'))
import cizim_dogrula as CD

def sha1_text(md: str) -> str:
    satirlar = md.splitlines()
    paragraflar = []
    bolumBasi = True
    bolumBaslik = ''
    tampon = []
    def bitir():
        nonlocal bolumBasi, tampon
        t = '\n'.join(tampon)
        t = re.sub(r'[ \t]+', ' ', t).strip()
        if t:
            paragraflar.append(t)
            bolumBasi = False
        tampon = []
    for s in satirlar:
        if s.startswith('# '): continue
        if s.startswith('@@'):
            bitir()
            bolumBasi = True
            bolumBaslik = s[2:].strip()
            continue
        if not s.strip(): bitir()
        else: tampon.append(s.strip())
    bitir()
    return hashlib.sha1('\n'.join(paragraflar).encode('utf-8')).hexdigest()

# ==============================================================================
# RADYOLOJİK ÇİZİM VE ANLATIM REÇETELERİ
# ==============================================================================

RADYOLOJI_TANIMLARI = {
    "y25-k2-12-kafa-travmalari": [
        {
            "slide": 16, "pi": "15", "ci": 0,
            "odak": [0.575, 0.20, 0.995, 0.875],
            "etiket": "Bikonveks lens hiperdansitesi (Epidural hematom)",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Slaytın sağındaki aksiyel beyin tomografisinde sol temporoparietal alanda dura ile kafatası iç tabulası arasında sınırları belirgin, bikonveks hiperdens lens şeklindeki epidural hematom alanını izliyoruz. Sütür hatlarını geçmediğine ve ventriküle bası yaparak orta hat şifti oluşturduğuna dikkat edin."
        },
        {
            "slide": 18, "pi": "17", "ci": 0,
            "odak": [0.697, 0.05, 0.99, 0.479],
            "etiket": "Temporal kemik kırığı ve epidural hematom",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Bilgisayarlı tomografi kemik penceresinde temporal kemik skuamöz kırık hattı ve hemen altında gelişen arteriyel hematom net olarak ayırt edilir."
        },
        {
            "slide": 20, "pi": "19", "ci": 0,
            "odak": [0.634, 0.468, 0.995, 0.932],
            "etiket": "Karakteristik bikonveks hiperdens kitle etkisi",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Aksiyel tomografide hematomun iki taraflı dışbükey lens formasyonu ve orta hat yapılarını karşı tarafa iten belirgin kitle etkisi açıkça izlenmektedir."
        },
        {
            "slide": 21, "pi": "20", "ci": 0,
            "odak": [0.61, 0.081, 0.954, 0.647],
            "etiket": "Venöz sinüs yırtığı epidural hematomu",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Tomografi kesitinde transvers ve sigmoid sinüs komşuluğunda arka çukurda yerleşen venöz kaynaklı epidural hematom alanı görülmektedir."
        },
        {
            "slide": 22, "pi": "21", "ci": 0,
            "odak": [0.051, 0.258, 0.5, 0.857],
            "etiket": "İç tabula - dura arası hiperdens kitle etkisi",
            "etiket_konum": [0.52, 0.86],
            "narration_insert": " Tomografi kesitinde temporal iç tabula ile dura arasında genişleyen hematomun lateral ventrikül frontal boynuzunu basılayarak orta hat şiftine yol açtığı izlenir."
        },
        {
            "slide": 26, "pi": "25", "ci": 0,
            "odak": [0.099, 0.122, 0.909, 0.794],
            "etiket": "Sağ frontal ve verteks epidural hematomu",
            "etiket_konum": [0.10, 0.82],
            "narration_insert": " Tomografi kesitlerinde sağ frontal bölgede ve verteks düzeyinde superior sagital sinüse bası yapan epidural hematom koleksiyonu izlenmektedir."
        },
        {
            "slide": 30, "pi": "29", "ci": 0,
            "odak": [0.54, 0.258, 0.98, 0.792],
            "etiket": "Hilal biçimli kresentik kanama (Subdural hematom)",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Aksiyel BT kesitinde hemisfer konveksitesi boyunca hilal şeklinde uzanan, sütür hatlarını rahatça aşarak tüm hemisferi kaplayan akut hiperdens subdural hematomu görüyoruz. Kitle etkisine bağlı ipsilateral ventrikül basılanmış ve orta hat sola doğru itilmiştir."
        },
        {
            "slide": 32, "pi": "31", "ci": 0,
            "odak": [0.106, 0.206, 0.918, 0.932],
            "etiket": "Epidural (bikonveks lens) vs Subdural (hilal) ayrımı",
            "etiket_konum": [0.15, 0.12],
            "narration_insert": " Yan yana sunulan tomografi kesitlerinde soldaki epidural hematomun sütür aşmayan bikonveks lens şekli ile sağdaki subdural hematomun tüm hemisferi saran kresentik hilal formu arasındaki temel radyolojik fark net olarak karşılaştırılmaktadır."
        },
        {
            "slide": 33, "pi": "32", "ci": 0,
            "odak": [0.575, 0.237, 1.0, 0.772],
            "etiket": "Yaşlı hastada kitle etkisi ve ventrikül basısı",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Tomografi kesitinde serebral atrofi zemininde gelişen geniş subdural hematomun ventrikül basısı ve sulkus silinmesiyle oluşturduğu bası etkisi izlenmektedir."
        },
        {
            "slide": 35, "pi": "34", "ci": 0,
            "odak": [0.067, 0.249, 0.905, 0.871],
            "etiket": "Kronik hematomda hematokrit seviyelenmesi",
            "etiket_konum": [0.10, 0.16],
            "narration_insert": " Kronik subdural hematom tomografisinde çöken hücresel elemanların yerçekimi etkisiyle altta hiperdens, üstte ise plazmanın hipodens seviyelenme oluşturduğu tipik hematokrit etkisi görülmektedir."
        },
        {
            "slide": 36, "pi": "35", "ci": 0,
            "odak": [0.626, 0.269, 1.0, 0.832],
            "etiket": "Parankimle aynı dansitede izodens subdural hematom",
            "etiket_konum": [0.08, 0.85],
            "narration_insert": " Subakut evredeki izodens subdural hematomda kan beyin dokusuyla aynı gri tonda olduğundan doğrudan görünmez; ancak sulkusların içe itilmesi ve ventrikül kompresyonuyla varlığı saptanır."
        },
        {
            "slide": 41, "pi": "40", "ci": 0,
            "odak": [0.531, 0.468, 0.903, 0.975],
            "etiket": "Sulkus ve sisternlerde hiperdens kan göllenmesi (SAK)",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Aksiyel beyin tomografisinde subaraknoid kanamanın tipik görünümü izlenmektedir: Kan sulkusların arasına ve bazal sisternalara yayılarak karakteristik hiperdens yıldızsı patern oluşturmuştur."
        },
        {
            "slide": 43, "pi": "42", "ci": 0,
            "odak": [0.066, 0.247, 0.931, 0.91],
            "etiket": "Verteks sulkuslarında yaygın subaraknoid kanama",
            "etiket_konum": [0.10, 0.16],
            "narration_insert": " Aksiyel kesitlerde konveksite sulkusları boyunca lineer hiperdens çizgilenmeler şeklinde dağılan travmatik subaraknoid kanama alanları net olarak ayırt edilir."
        },
        {
            "slide": 47, "pi": "46", "ci": 0,
            "odak": [0.642, 0.417, 1.0, 1.0],
            "etiket": "Frontal ve temporal tabanda tuz-biber kontüzyon",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Hemorajik kontüzyon tomografisinde frontal ve temporal lob bazallerinde gri-beyaz cevher bileşkesinde 'tuz-biber' görünümündeki alacalı peteşiyal hiperdens odaklar açıkça izlenmektedir."
        },
        {
            "slide": 50, "pi": "49", "ci": 0,
            "odak": [0.208, 0.217, 0.783, 0.899],
            "etiket": "Kup (darbe tarafı) ve kontrkup (karşı lezyon)",
            "etiket_konum": [0.10, 0.14],
            "narration_insert": " Tomografi incelemesinde darbe tarafındaki lineer kafatası çatlağı altında kup lezyonu, deselerasyonla karşı kutupta gelişen masif hemorajik kontrkup lezyonu ile birlikte görülür."
        },
        {
            "slide": 58, "pi": "57", "ci": 0,
            "odak": [0.662, 0.269, 1.0, 0.857],
            "etiket": "Korpus kallozumda mikrogiriş DAH odakları",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Diffüz aksonal yaralanmada tomografi ve MRG kesitlerinde korpus kallozum ve gri-beyaz cevher sınırında mikrogiriş peteşiyal hiperdansiteler izlenir."
        },
        {
            "slide": 67, "pi": "66", "ci": 0,
            "odak": [0.626, 0.417, 0.975, 0.894],
            "etiket": "Singulat girusun faks altından karşıya şifti",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Subfalsin herniasyon aksiyel tomografisinde singulat girusun faks serebri altından karşı tarafa itildiği ve foramen Monro basısına yol açtığı izlenir."
        },
        {
            "slide": 71, "pi": "70", "ci": 0,
            "odak": [0.115, 0.61, 0.905, 1.0],
            "etiket": "Unkus herniasyonu ve mezensefalon basısı",
            "etiket_konum": [0.10, 0.52],
            "narration_insert": " Transtentoryal herniasyon kesitinde medial temporal lob unkusunun tentoryum kenarından aşağı kayarak mezensefalonu basıladığı ve ambiyens sisterni sildiği görülmektedir."
        },
        {
            "slide": 75, "pi": "74", "ci": 0,
            "odak": [0.57, 0.311, 1.0, 1.0],
            "etiket": "Tonsiller herniasyon (foramen magnum)",
            "etiket_konum": [0.08, 0.82],
            "narration_insert": " Sagital MRG kesitinde serebellar tonsillerin foramen magnum çizgisinin beş milimetreden fazla altına sarkarak medulla oblangatayı sıkıştırdığı açıkça izlenmektedir."
        }
    ],

    "y25-k2-13-spinal-travmalar": [
        {
            "slide": 19, "pi": "18", "ci": 0,
            "odak": [0.016, 0.551, 0.628, 0.979],
            "etiket": "Atlas (C1) Jefferson patlama kırığı ve lateral kitle taşması",
            "etiket_konum": [0.05, 0.46],
            "narration_insert": " Açık ağız grafisi ve aksiyel tomografide birinci boyun omuru olan atlasın hem ön hem arka arkının parçalandığı ve lateral kitlelerin odontoid üzerinden dışarı taştığı görülür."
        },
        {
            "slide": 20, "pi": "19", "ci": 0,
            "odak": [0.487, 0.028, 0.959, 0.969],
            "etiket": "Tip II odontoid kırık hattı (boyun bileşkesi)",
            "etiket_konum": [0.05, 0.85],
            "narration_insert": " Lateral radyografi ve tomografide odontoid çıkıntının gövde ile birleştiği zayıf boyun bölgesinden ayrıldığı tip iki fraktür hattı net olarak izlenmektedir."
        },
        {
            "slide": 21, "pi": "20", "ci": 0,
            "odak": [0.366, 0.078, 0.975, 0.89],
            "etiket": "Odontoid kırık tipleri (Tip I apeks, Tip II boyun, Tip III korpus)",
            "etiket_konum": [0.05, 0.88],
            "narration_insert": " Tomografi rekonstrüksiyonlarında odontoid fraktürlerinin apeks, korpus-dens bileşkesi ve korpus içine uzanan anatomik hatları karşılaştırmalı olarak gösterilmektedir."
        },
        {
            "slide": 23, "pi": "22", "ci": 0,
            "odak": [0.0, 0.525, 0.99, 0.992],
            "etiket": "Hangman kırığı (C2 pars interartikülaris iki taraflı kırığı)",
            "etiket_konum": [0.05, 0.44],
            "narration_insert": " Lateral grafide hiperekstansiyon ve distraksiyon travmasıyla ikinci servikal omurun pars interartikülarislerinde oluşan iki taraflı kırık ve aksis korpusunun öne kayması izlenir."
        },
        {
            "slide": 24, "pi": "23", "ci": 0,
            "odak": [0.438, 0.183, 0.899, 1.0],
            "etiket": "Asılan adam kırığı evrelemesi ve C2-C3 açılanması",
            "etiket_konum": [0.05, 0.88],
            "narration_insert": " Radyografide kırık parçaları arasındaki ayrılma miktarı, angülasyon derecesi ve faset eklem kilitlenmesiyle Hangman kırığının cerrahi evresi saptanır."
        },
        {
            "slide": 29, "pi": "28", "ci": 0,
            "odak": [0.0, 0.0, 0.415, 1.0],
            "etiket": "C5-C6 anterior dislokasyon ve faset kilitlenmesi",
            "etiket_konum": [0.45, 0.82],
            "narration_insert": " Lateral servikal radyografide beşinci ve altıncı boyun omurları arasındaki faset eklemlerin kayarak kilitlendiği ve omurga diziliminin ileri derecede bozulduğu izlenmektedir."
        },
        {
            "slide": 30, "pi": "29", "ci": 0,
            "odak": [0.03, 0.031, 0.401, 0.846],
            "etiket": "C2 anteroinferior teardrop (gözyaşı) kırığı",
            "etiket_konum": [0.45, 0.82],
            "narration_insert": " Grafide hiperekstansiyon travması sonucu ön boyuna bağın gerilerek aksis gövdesinin ön-alt köşesinden kopardığı karakteristik üçgen gözyaşı kemik fragmanı izlenir."
        },
        {
            "slide": 31, "pi": "30", "ci": 0,
            "odak": [0.027, 0.053, 0.322, 0.858],
            "etiket": "C4 burst patlama kırığı ve spinal kanal retropulsiyonu",
            "etiket_konum": [0.40, 0.82],
            "narration_insert": " Bilgisayarlı tomografide dördüncü servikal omur korpusunun aksiyel yüklenmeyle parçalandığı ve arka duvar parçasının omurilik kanalına doğru retropulse olduğu görülür."
        },
        {
            "slide": 32, "pi": "31", "ci": 0,
            "odak": [0.045, 0.039, 0.346, 0.901],
            "etiket": "Postoperatif anterior plak-vida ve kafes füzyonu",
            "etiket_konum": [0.40, 0.82],
            "narration_insert": " Postoperatif lateral kontrolde parçalanan korpusun cerrahi korpektomiyle boşaltılıp yerine kafes ve anterior titanyum plak-vida yerleştirilerek kanalın açıldığı görülmektedir."
        },
        {
            "slide": 33, "pi": "32", "ci": 0,
            "odak": [0.069, 0.099, 0.32, 0.842],
            "etiket": "Sagital T2 MRG: Omurilik basısı ve miyelomalazi",
            "etiket_konum": [0.38, 0.82],
            "narration_insert": " Manyetik rezonans görüntülemede disloke omurların omuriliği sıkıştırdığı seviyede kord içinde parlak beyaz T2 sinyali şeklinde travmatik miyelomalazi ve ödem alanı izlenir."
        },
        {
            "slide": 39, "pi": "38", "ci": 0,
            "odak": [0.0, 0.0, 0.669, 1.0],
            "etiket": "Alt torakal kama (wedge) kompresyon kırığı",
            "etiket_konum": [0.68, 0.82],
            "narration_insert": " Lateral torakal grafide omurga gövdesinin ön yüksekliğinin ezilerek çöktüğü, arka yüksekliğin korunduğu tipik anterior kama kompresyon kırığı izlenmektedir."
        },
        {
            "slide": 45, "pi": "44", "ci": 0,
            "odak": [0.402, 0.157, 1.0, 0.921],
            "etiket": "Aksiyel BT: Burst fraktürü arka kolon kemik fragmanı",
            "etiket_konum": [0.05, 0.82],
            "narration_insert": " Aksiyel tomografi kesitinde patlayan vertebra korpus arka duvar kemik fragmanının spinal kanalı yüzde elliden fazla daraltarak omuriliği sıkıştırdığı görülmektedir."
        },
        {
            "slide": 51, "pi": "50", "ci": 0,
            "odak": [0.0, 0.0, 0.458, 0.6],
            "etiket": "3B BT: Deplase Tip II odontoid kırığı",
            "etiket_konum": [0.50, 0.82],
            "narration_insert": " Üç boyutlu rekonstrüksiyon kesitinde odontoid çıkıntının gövdeden tamamen ayrılıp arkaya doğru deplase olduğu cerrahi kırık hattı açıkça izlenmektedir."
        }
    ],

    "y25-k2-64-omurga-tumorleri": [
        {
            "slide": 6, "pi": "5", "ci": 0,
            "odak": [0.10, 0.20, 0.90, 0.90],
            "etiket": "Pedikül erozyonu: Göz Kırpan Baykuş (Winking Owl) belirtisi",
            "etiket_konum": [0.10, 0.12],
            "narration_insert": " Ön-arka omurga radyografisinde metastatik tümörün vertebra pedikülünü eritmesi sonucu normalde iki göz gibi görünen pediküllerden birinin kaybolduğu 'Göz Kırpan Baykuş' belirtisi izlenmektedir."
        },
        {
            "slide": 8, "pi": "7", "ci": 0,
            "odak": [0.10, 0.20, 0.90, 0.90],
            "etiket": "Vertebra korpus patolojik çökmesi ve epidural bası",
            "etiket_konum": [0.10, 0.12],
            "narration_insert": " Sagital MRG kesitinde metastazla zayıflayan vertebra gövdesinin patolojik olarak çöktüğü ve epidural alana taşan tümör dokusunun spinal kordu sıkıştırdığı görülmektedir."
        },
        {
            "slide": 10, "pi": "9", "ci": 0,
            "odak": [0.10, 0.20, 0.90, 0.90],
            "etiket": "Sklerotik/blastik metastaz (fildişi vertebra) ve litik lezyon",
            "etiket_konum": [0.10, 0.12],
            "narration_insert": " Radyolojik incelemede prostat kanseri metastazında bembeyaz sklerotik 'fildişi vertebra', meme ve akciğer metastazında ise kemiği eriten koyu litik lezyonlar ayırt edilir."
        }
    ],

    "y25-k2-14-beyin-tumorleri": [
        {
            "slide": 10, "pi": "9", "ci": 0,
            "odak": [0.10, 0.15, 0.90, 0.90],
            "etiket": "Glioblastom: Halka kontrastlanması, santral nekroz ve ödem",
            "etiket_konum": [0.10, 0.10],
            "narration_insert": " T1 kontrastlı kranial MRG'de glioblastoma multiformenin kalın ve düzensiz halkasal kontrast tutulumu, ortasındaki santral nekroz ve çevresindeki yaygın parankim ödemi izlenmektedir."
        },
        {
            "slide": 20, "pi": "19", "ci": 0,
            "odak": [0.10, 0.15, 0.90, 0.90],
            "etiket": "Menenjiom: Homojen parlak kontrastlanma ve dural kuyruk",
            "etiket_konum": [0.10, 0.10],
            "narration_insert": " Kontrastlı MRG incelemesinde menenjiomun ekstra-aksiyel, homojen ve yoğun parlak boyandığı, komşu dura boyunca uzanan patognomonik 'dural kuyruk' belirtisi açıkça görülmektedir."
        },
        {
            "slide": 30, "pi": "29", "ci": 0,
            "odak": [0.10, 0.15, 0.90, 0.90],
            "etiket": "Vestibüler Schwannom: Serebellopontin köşe ve İAM genişlemesi",
            "etiket_konum": [0.10, 0.10],
            "narration_insert": " Kranial MRG aksiyel kesitinde serebellopontin köşeyi dolduran ve iç kulak kanalını genişleterek dondurma külahı görünümü oluşturan vestibüler schwannom kitlesi izlenir."
        },
        {
            "slide": 40, "pi": "39", "ci": 0,
            "odak": [0.10, 0.15, 0.90, 0.90],
            "etiket": "Hipofiz Adenomu: Sellar genişleme ve optik kiyazma basısı",
            "etiket_konum": [0.10, 0.10],
            "narration_insert": " Koronal ve sagital T1 kontrastlı MRG'de sella tursikayı genişletip yukarıya suprasellar alana doğru taşan ve kiyazma optikumu yukarı iten hipofiz makroadenomu izlenmektedir."
        }
    ],

    "y25-k2-03-sss-hasar-bicimleri-odem-hidrosefali-herniasyon": [
        {
            "slide": 14, "pi": "13", "ci": 0,
            "odak": [0.10, 0.20, 0.90, 0.90],
            "etiket": "Unkal ve subfalsin herniasyon (orta hat şifti)",
            "etiket_konum": [0.10, 0.12],
            "narration_insert": " Aksiyel BT kesitinde masif ödem ve kitle etkisine bağlı singulat girusun faks altına, unkusun ise tentoryum kenarından aşağıya fıtıklaştığı herniasyon hatları görülür."
        },
        {
            "slide": 18, "pi": "17", "ci": 0,
            "odak": [0.10, 0.20, 0.90, 0.90],
            "etiket": "Hidrosefali: Ventrikülomegali ve transependimal sızıntı",
            "etiket_konum": [0.10, 0.12],
            "narration_insert": " Tomografi incelemesinde BOS dolaşımının tıkanmasıyla lateral ventriküllerin ileri derecede genişlediği ve periventriküler beyaz cevherde transependimal hipodansite oluştuğu izlenir."
        }
    ]
}

def is_valid_drawing(z, n_words):
    # validate z dict
    res = CD.denetle(z, n_words, [z.get('odak') or [0,0,1,1]], None, "tıbbi terminoloji ve anatomi")
    return res is None

def zenginlestir_ders(key: str):
    print(f"\n=======================================================")
    print(f"Ders Zenginleştiriliyor: {key}")
    print(f"=======================================================")

    receteler = RADYOLOJI_TANIMLARI.get(key, [])
    if not receteler:
        print(f"Reçete tanımlanmamış: {key}")
        return

    metin_file = ARSIV / 'metin' / f'{key}.md'
    isaret_file = ARSIV / 'isaret' / f'{key}.json'
    cizim_file = ARSIV / 'cizim' / f'{key}.json'
    v2_file = ARSIV / 'v2' / f'{key}.json'

    if not metin_file.exists():
        print(f"Metin dosyası yok: {metin_file}")
        return

    text = metin_file.read_text(encoding='utf-8')
    pars = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip() and not p.strip().startswith('#')]
    # also preserve titles / headers
    raw_blocks = [b.strip() for b in re.split(r'\n\s*\n', text) if b.strip()]

    # Load existing cizim
    cz_data = {"surum": 1, "metinHash": "", "p": {}, "rapor": {}}
    if cizim_file.exists():
        try:
            cz_data = json.loads(cizim_file.read_text(encoding='utf-8'))
        except:
            pass
    if "p" not in cz_data:
        cz_data["p"] = {}

    # Load existing isaret
    is_data = json.loads(isaret_file.read_text(encoding='utf-8')) if isaret_file.exists() else {"surum": 1, "metinHash": "", "c": {}}

    # Load existing v2
    v2_data = json.loads(v2_file.read_text(encoding='utf-8')) if v2_file.exists() else {}

    # Apply narration additions and cizim additions
    modified_pars = False
    added_drawings = 0

    # Map par index to raw block index
    p_to_raw = {}
    p_counter = 0
    for bi, blk in enumerate(raw_blocks):
        if not blk.startswith('#'):
            p_to_raw[p_counter] = bi
            p_counter += 1

    for rec in receteler:
        pi = int(rec["pi"])
        ci = int(rec["ci"])
        slide = rec["slide"]
        odak = rec["odak"]
        etiket = rec["etiket"]
        etiket_konum = rec.get("etiket_konum", [0.10, 0.85])
        narr_ins = rec.get("narration_insert", "")

        # Check if narration needs updating
        if pi in p_to_raw and narr_ins:
            raw_idx = p_to_raw[pi]
            cur_text = raw_blocks[raw_idx]
            # Don't duplicate if already added
            if narr_ins.strip()[:30] not in cur_text:
                raw_blocks[raw_idx] = cur_text.strip() + narr_ins
                modified_pars = True

        # Now construct the Drawing Command
        # Calculate character range k for the sentence
        k_range = [0, 80]

        # Draw odak + akis
        new_z = {
            "tur": "akis",
            "s": slide,
            "k": k_range,
            "odak": odak,
            "etiket": etiket,
            "etiket_konum": etiket_konum,
            "etiket_genislik": 0.45,
            "bas": 0,
            "son": 15
        }

        pi_str = str(pi)
        ci_str = str(ci)
        if pi_str not in cz_data["p"]:
            cz_data["p"][pi_str] = {}
        if ci_str not in cz_data["p"][pi_str]:
            cz_data["p"][pi_str][ci_str] = []

        # Replace or prepend the new drawing command
        # remove old sema if it was duplicate or keep
        cz_data["p"][pi_str][ci_str] = [new_z] + [z for z in cz_data["p"][pi_str][ci_str] if z.get("tur") != "akis"]
        added_drawings += 1

    if modified_pars:
        new_text = '\n\n'.join(raw_blocks) + '\n'
        metin_file.write_text(new_text, encoding='utf-8')
        print(f"  Metin güncellendi ({len(receteler)} radyoloji rehberi eklendi)")
    else:
        new_text = text

    # Recompute metinHash
    new_h = sha1_text(new_text)
    cz_data["metinHash"] = new_h
    is_data["metinHash"] = new_h

    # Ensure all sentences on that slide have marks and drawing attached in isaret
    for pi_str, cs_dict in cz_data["p"].items():
        if pi_str in is_data.get("c", {}):
            cs_list = is_data["c"][pi_str]
            for ci_str, zlist in cs_dict.items():
                c_idx = int(ci_str)
                if c_idx < len(cs_list) and cs_list[c_idx]:
                    cs_list[c_idx]["z"] = zlist
                    # if t was sayfa and no l, ensure it has proper structure
                    if cs_list[c_idx].get("t") == "sayfa" and not cs_list[c_idx].get("l"):
                        cs_list[c_idx]["l"] = [zlist[0]["odak"]]

    # Save cizim
    cizim_file.write_text(json.dumps(cz_data, ensure_ascii=False, indent=2), encoding='utf-8')
    # Save isaret
    isaret_file.write_text(json.dumps(is_data, ensure_ascii=False, indent=2), encoding='utf-8')

    # Also persist to taslak / cizim_aday.json so arsiv_yayinla keeps them
    taslak_aday = DB_25_26 / "taslak" / key / "cizim_aday.json"
    if taslak_aday.exists():
        try:
            aday_data = json.loads(taslak_aday.read_text(encoding='utf-8'))
            var_komutlar = aday_data.get("komutlar", [])
            for rec in receteler:
                pi = rec["pi"]
                ci = rec["ci"]
                new_cmd = {
                    "sayfa": rec["slide"],
                    "tur": "akis",
                    "odak": rec["odak"],
                    "etiket": rec["etiket"],
                    "etiket_konum": rec.get("etiket_konum", [0.10, 0.85]),
                    "etiket_genislik": 0.45,
                    "bas": 0,
                    "son": 15,
                    "cumle": f"P{pi}.C{ci}"
                }
                # replace or add
                var_komutlar = [new_cmd] + [k for k in var_komutlar if not (k.get("sayfa") == rec["slide"] and k.get("tur") == "akis")]
            aday_data["komutlar"] = var_komutlar
            taslak_aday.write_text(json.dumps(aday_data, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"  Taslak cizim_aday.json güncellendi: {taslak_aday}")
        except Exception as e:
            print(f"  Taslak cizim_aday.json yazılamadı: {e}")

    print(f"  Cizim ve Isaret kaydedildi ({added_drawings} yeni radyoloji hat ve odak çizimi eklendi)")
    print(f"  Yeni metinHash: {new_h}")

def main():
    for key in RADYOLOJI_TANIMLARI.keys():
        zenginlestir_ders(key)

if __name__ == '__main__':
    main()
