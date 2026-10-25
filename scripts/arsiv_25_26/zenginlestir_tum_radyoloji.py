#!/usr/bin/env python3
"""
Kurul 2 Radyolojik ve Tanısal Görüntü Zenginleştirme Motoru (Lezyon Odaklı & Hassas İşaretleme)
Resmin tamamını değil; lezyonun, kırık hattının, hematomun veya kitlenin kendisini doğrudan işaretler.
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
# LEZYON ODAKLI RADYOLOJİK ÇİZİM VE ANLATIM REÇETELERİ
# odak: Resmin tümünü değil, doğrudan lezyonu saran dar çerçeve
# a -> b: Boş alandan lezyon merkezine yönelen hedefleyici ok
# ==============================================================================

RADYOLOJI_TANIMLARI = {
    "y25-k2-12-kafa-travmalari": [
        {
            "slide": 16, "pi": "15", "ci": 0,
            "odak": [0.78, 0.38, 0.92, 0.66],
            "a": [0.66, 0.52], "b": [0.82, 0.52],
            "etiket": "Bikonveks lens hiperdansitesi (Epidural hematom)",
            "etiket_konum": [0.52, 0.32], "etiket_genislik": 0.42,
            "narration_insert": " Aksiyel beyin tomografisinde sol temporoparietal kalvaryum altında dura ile kafatası iç tabulası arasında sınırları belirgin, bikonveks hiperdens lens şeklindeki epidural hematom alanını izliyoruz. Sütür hatlarını geçmediğine ve ventriküle bası yaparak orta hat şifti oluşturduğuna dikkat edin."
        },
        {
            "slide": 18, "pi": "17", "ci": 0,
            "odak": [0.76, 0.16, 0.90, 0.36],
            "a": [0.68, 0.26], "b": [0.80, 0.26],
            "etiket": "Temporal kemik kırık hattı ve arteriyel EDH",
            "etiket_konum": [0.52, 0.10], "etiket_genislik": 0.42,
            "narration_insert": " Bilgisayarlı tomografi kemik penceresinde temporal kemik skuamöz kırık hattı ve hemen altında gelişen arteriyel hematom net olarak ayırt edilir."
        },
        {
            "slide": 20, "pi": "19", "ci": 0,
            "odak": [0.72, 0.52, 0.86, 0.74],
            "a": [0.62, 0.63], "b": [0.76, 0.63],
            "etiket": "Dışbükey lens kitle etkisi ve ventrikül basısı",
            "etiket_konum": [0.52, 0.44], "etiket_genislik": 0.42,
            "narration_insert": " Aksiyel tomografide hematomun iki taraflı dışbükey lens formasyonu ve orta hat yapılarını karşı tarafa iten belirgin kitle etkisi açıkça izlenmektedir."
        },
        {
            "slide": 21, "pi": "20", "ci": 0,
            "odak": [0.68, 0.26, 0.88, 0.48],
            "a": [0.62, 0.37], "b": [0.75, 0.37],
            "etiket": "Transvers-sigmoid sinüs komşuluğu venöz EDH",
            "etiket_konum": [0.52, 0.18], "etiket_genislik": 0.42,
            "narration_insert": " Tomografi kesitinde transvers ve sigmoid sinüs komşuluğunda arka çukurda yerleşen venöz kaynaklı epidural hematom alanı görülmektedir."
        },
        {
            "slide": 22, "pi": "21", "ci": 0,
            "odak": [0.22, 0.42, 0.38, 0.68],
            "a": [0.10, 0.55], "b": [0.26, 0.55],
            "etiket": "İç tabula - dura arası hiperdens EDH",
            "etiket_konum": [0.06, 0.32], "etiket_genislik": 0.40,
            "narration_insert": " Tomografi kesitinde temporal iç tabula ile dura arasında genişleyen hematomun lateral ventrikül frontal boynuzunu basılayarak orta hat şiftine yol açtığı izlenir."
        },
        {
            "slide": 23, "pi": "22", "ci": 0,
            "odak": [0.72, 0.54, 0.88, 0.78],
            "a": [0.64, 0.66], "b": [0.78, 0.66],
            "etiket": "Verteks düzeyinde hiperdens EDH",
            "etiket_konum": [0.52, 0.44], "etiket_genislik": 0.42,
            "narration_insert": " Tomografi kesitlerinde verteks düzeyinde superior sagital sinüse bası yapan epidural hematom koleksiyonu izlenmektedir."
        },
        {
            "slide": 26, "pi": "25", "ci": 0,
            "odak": [0.22, 0.24, 0.42, 0.52],
            "a": [0.12, 0.38], "b": [0.28, 0.38],
            "etiket": "Sağ frontal kalvaryal bikonveks EDH",
            "etiket_konum": [0.08, 0.16], "etiket_genislik": 0.40,
            "narration_insert": " Tomografi kesitlerinde sağ frontal bölgede iç tabuladan ayrışan bikonveks epidural hematom koleksiyonu izlenmektedir."
        },
        {
            "slide": 30, "pi": "29", "ci": 0,
            "odak": [0.58, 0.34, 0.72, 0.68],
            "a": [0.78, 0.51], "b": [0.65, 0.51],
            "etiket": "Hilal biçimli kresentik kanama (Akut SDH)",
            "etiket_konum": [0.52, 0.26], "etiket_genislik": 0.42,
            "narration_insert": " Aksiyel BT kesitinde hemisfer konveksitesi boyunca hilal şeklinde uzanan, sütür hatlarını rahatça aşarak tüm hemisferi kaplayan akut hiperdens subdural hematomu görüyoruz. Kitle etkisine bağlı ipsilateral ventrikül basılanmış ve orta hat sola doğru itilmiştir."
        },
        {
            "slide": 32, "pi": "31", "ci": 0,
            "odak": [0.20, 0.40, 0.34, 0.64],
            "a": [0.10, 0.52], "b": [0.24, 0.52],
            "etiket": "Epidural: Bikonveks lens (sutürü geçmez)",
            "etiket_konum": [0.08, 0.30], "etiket_genislik": 0.42,
            "narration_insert": " Yan yana sunulan tomografi kesitlerinde soldaki epidural hematomun sütür aşmayan bikonveks lens şekli ile sağdaki subdural hematomun tüm hemisferi saran kresentik hilal formu arasındaki temel radyolojik fark net olarak karşılaştırılmaktadır."
        },
        {
            "slide": 33, "pi": "32", "ci": 0,
            "odak": [0.62, 0.32, 0.76, 0.66],
            "a": [0.82, 0.49], "b": [0.68, 0.49],
            "etiket": "Tüm hemisferi saran kresentik SDH",
            "etiket_konum": [0.52, 0.24], "etiket_genislik": 0.42,
            "narration_insert": " Tomografi kesitinde serebral atrofi zemininde gelişen geniş subdural hematomun ventrikül basısı ve sulkus silinmesiyle oluşturduğu bası etkisi izlenmektedir."
        },
        {
            "slide": 35, "pi": "34", "ci": 0,
            "odak": [0.36, 0.45, 0.64, 0.68],
            "a": [0.50, 0.36], "b": [0.50, 0.52],
            "etiket": "Hematokrit seviyelenmesi (Akut/Kronik faz)",
            "etiket_konum": [0.26, 0.28], "etiket_genislik": 0.44,
            "narration_insert": " Kronik subdural hematom tomografisinde çöken hücresel elemanların yerçekimi etkisiyle altta hiperdens, üstte ise plazmanın hipodens seviyelenme oluşturduğu tipik hematokrit etkisi görülmektedir."
        },
        {
            "slide": 36, "pi": "35", "ci": 0,
            "odak": [0.68, 0.38, 0.84, 0.68],
            "a": [0.60, 0.53], "b": [0.72, 0.53],
            "etiket": "Sulkus silinmesi ve izodens kitle etkisi",
            "etiket_konum": [0.52, 0.28], "etiket_genislik": 0.42,
            "narration_insert": " Subakut evredeki izodens subdural hematomda kan beyin dokusuyla aynı gri tonda olduğundan doğrudan görünmez; ancak sulkusların içe itilmesi ve ventrikül kompresyonuyla varlığı saptanır."
        },
        {
            "slide": 41, "pi": "40", "ci": 0,
            "odak": [0.64, 0.62, 0.80, 0.82],
            "a": [0.56, 0.72], "b": [0.68, 0.72],
            "etiket": "Silviyan ve sulkal hiperdansite (SAH)",
            "etiket_konum": [0.50, 0.52], "etiket_genislik": 0.42,
            "narration_insert": " Aksiyel beyin tomografisinde subaraknoid kanamanın tipik görünümü izlenmektedir: Kan sulkusların arasına ve bazal sisternalara yayılarak karakteristik hiperdens yıldızsı patern oluşturmuştur."
        },
        {
            "slide": 47, "pi": "46", "ci": 0,
            "odak": [0.72, 0.58, 0.88, 0.78],
            "a": [0.64, 0.68], "b": [0.76, 0.68],
            "etiket": "Kortikal mikrokanamalar (Tuz-biber paterni)",
            "etiket_konum": [0.52, 0.48], "etiket_genislik": 0.42,
            "narration_insert": " Hemorajik kontüzyon tomografisinde frontal ve temporal lob bazallerinde gri-beyaz cevher bileşkesinde 'tuz-biber' görünümündeki alacalı peteşiyal hiperdens odaklar açıkça izlenmektedir."
        },
        {
            "slide": 48, "pi": "47", "ci": 0,
            "odak": [0.15, 0.56, 0.35, 0.78],
            "a": [0.06, 0.67], "b": [0.20, 0.67],
            "etiket": "Kup lezyonu: Darbe altı kontüzyon",
            "etiket_konum": [0.05, 0.46], "etiket_genislik": 0.40,
            "narration_insert": " Tomografi incelemesinde darbe tarafındaki lineer kafatası çatlağı altında kup lezyonu, deselerasyonla karşı kutupta gelişen masif hemorajik kontrkup lezyonu ile birlikte görülür."
        },
        {
            "slide": 67, "pi": "66", "ci": 0,
            "odak": [0.74, 0.54, 0.86, 0.72],
            "a": [0.65, 0.63], "b": [0.77, 0.63],
            "etiket": "Septum pellusidum orta hat şifti (Subfalsin)",
            "etiket_konum": [0.52, 0.45], "etiket_genislik": 0.42,
            "narration_insert": " Subfalsin herniasyon aksiyel tomografisinde singulat girusun faks serebri altından karşı tarafa itildiği ve foramen Monro basısına yol açtığı izlenir."
        },
        {
            "slide": 71, "pi": "70", "ci": 0,
            "odak": [0.44, 0.70, 0.60, 0.88],
            "a": [0.34, 0.79], "b": [0.48, 0.79],
            "etiket": "Mezensefalon pedinkül basısı (Unkal herniasyon)",
            "etiket_konum": [0.15, 0.64], "etiket_genislik": 0.44,
            "narration_insert": " Transtentoryal herniasyon kesitinde medial temporal lob unkusunun tentoryum kenarından aşağı kayarak mezensefalonu basıladığı ve ambiyens sisterni sildiği görülmektedir."
        },
        {
            "slide": 75, "pi": "74", "ci": 0,
            "odak": [0.70, 0.58, 0.86, 0.80],
            "a": [0.60, 0.69], "b": [0.74, 0.69],
            "etiket": "Foramen magnum altına tonsil herniasyonu",
            "etiket_konum": [0.52, 0.35], "etiket_genislik": 0.42,
            "narration_insert": " Sagital MRG kesitinde serebellar tonsillerin foramen magnum çizgisinin beş milimetreden fazla altına sarkarak medulla oblangatayı sıkıştırdığı açıkça izlenmektedir."
        }
    ],

    "y25-k2-13-spinal-travmalar": [
        {
            "slide": 16, "pi": "15", "ci": 0,
            "odak": [0.10, 0.28, 0.26, 0.48],
            "a": [0.04, 0.38], "b": [0.16, 0.38],
            "etiket": "Oksipitoservikal bileşke ayrışması",
            "etiket_konum": [0.04, 0.18], "etiket_genislik": 0.38,
            "narration_insert": " Radyografide oksipital kondil ve kraniyoservikal bileşke anatomik hatlarının yer değiştirdiği izlenmektedir."
        },
        {
            "slide": 17, "pi": "16", "ci": 0,
            "odak": [0.10, 0.38, 0.26, 0.58],
            "a": [0.04, 0.48], "b": [0.15, 0.48],
            "etiket": "C1 lateral kitle taşması (Jefferson kırığı)",
            "etiket_konum": [0.04, 0.24], "etiket_genislik": 0.40,
            "narration_insert": " Açık ağız grafisinde C1 lateral kitlelerinin odontoid prosesin iki yanına doğru taştığı Jefferson patlama kırığı izlenir."
        },
        {
            "slide": 24, "pi": "23", "ci": 0,
            "odak": [0.60, 0.44, 0.76, 0.64],
            "a": [0.48, 0.54], "b": [0.64, 0.54],
            "etiket": "C2 pars interartikülaris fraktürü (Hangman)",
            "etiket_konum": [0.46, 0.32], "etiket_genislik": 0.42,
            "narration_insert": " Lateral grafide hiperekstansiyon travmasıyla aksisin pars interartikülarislerinde oluşan iki taraflı kırık ve anterior listezis izlenir."
        },
        {
            "slide": 25, "pi": "24", "ci": 0,
            "odak": [0.34, 0.38, 0.54, 0.60],
            "a": [0.24, 0.49], "b": [0.39, 0.49],
            "etiket": "Tip 2 odontoid bazis ayrışma hattı (İnstabil)",
            "etiket_konum": [0.18, 0.28], "etiket_genislik": 0.42,
            "narration_insert": " Tomografide odontoid çıkıntının gövde ile birleştiği zayıf bazis boyun bölgesinden ayrıldığı instabil tip iki fraktür hattı net olarak görülür."
        },
        {
            "slide": 30, "pi": "29", "ci": 0,
            "odak": [0.12, 0.30, 0.26, 0.48],
            "a": [0.32, 0.39], "b": [0.20, 0.39],
            "etiket": "Anteroinferior damla (Teardrop) kemik fragmanı",
            "etiket_konum": [0.12, 0.18], "etiket_genislik": 0.42,
            "narration_insert": " Grafide hiperekstansiyon travması sonucu ön-alt köşeden kopan karakteristik üçgen damla kemik fragmanı izlenir."
        },
        {
            "slide": 31, "pi": "30", "ci": 0,
            "odak": [0.10, 0.34, 0.24, 0.52],
            "a": [0.28, 0.43], "b": [0.16, 0.43],
            "etiket": "C4 patlama kırığı ve spinal kanala retropülsiyon",
            "etiket_konum": [0.10, 0.22], "etiket_genislik": 0.42,
            "narration_insert": " Bilgisayarlı tomografide servikal omur korpusunun parçalandığı ve arka duvar parçasının omurilik kanalına doğru retropulse olduğu görülür."
        },
        {
            "slide": 33, "pi": "32", "ci": 0,
            "odak": [0.13, 0.38, 0.24, 0.56],
            "a": [0.28, 0.47], "b": [0.17, 0.47],
            "etiket": "İntramedüller parlak T2 sinyali (Miyelomalazi)",
            "etiket_konum": [0.08, 0.26], "etiket_genislik": 0.42,
            "narration_insert": " Manyetik rezonans görüntülemede disloke omurların omuriliği sıkıştırdığı seviyede kord içinde parlak beyaz T2 sinyali şeklinde travmatik miyelomalazi ve ödem alanı izlenir."
        },
        {
            "slide": 34, "pi": "33", "ci": 0,
            "odak": [0.10, 0.34, 0.22, 0.50],
            "a": [0.26, 0.42], "b": [0.15, 0.42],
            "etiket": "Travmatik ekstrüde disk ve kord basısı",
            "etiket_konum": [0.06, 0.22], "etiket_genislik": 0.40,
            "narration_insert": " Sagittal MRG'de yırtılan posterior longitudinal ligaman arasından spinal kanala fıtıklaşan travmatik disk dokusu korda bası yapmaktadır."
        }
    ],

    "y25-k2-64-omurga-tumorleri": [
        {
            "slide": 6, "pi": "5", "ci": 0,
            "odak": [0.46, 0.36, 0.58, 0.52],
            "a": [0.64, 0.44], "b": [0.52, 0.44],
            "etiket": "Arka eleman nidus ve sklerotik rim (Osteoblastom)",
            "etiket_konum": [0.40, 0.24], "etiket_genislik": 0.44,
            "narration_insert": " Aksiyel BT kesitinde omurganın arka elemanlarına yerleşen, çevresi yoğun sklerotik kemikle sarılı osteoblastom nidusu net olarak seçilmektedir."
        },
        {
            "slide": 8, "pi": "7", "ci": 0,
            "odak": [0.68, 0.54, 0.90, 0.80],
            "a": [0.58, 0.67], "b": [0.74, 0.67],
            "etiket": "Vertebra korpus ekspansil litik destrüksiyonu",
            "etiket_konum": [0.50, 0.42], "etiket_genislik": 0.44,
            "narration_insert": " Radyografide vertebra korpusunu tutan, kemik korteksini inceltip dışarı doğru genişleten sabun köpüğü manzaralı dev hücreli tümör lezyonu izlenir."
        },
        {
            "slide": 16, "pi": "15", "ci": 0,
            "odak": [0.68, 0.46, 0.86, 0.68],
            "a": [0.58, 0.57], "b": [0.72, 0.57],
            "etiket": "Pedikül erozyonu: Göz Kırpan Baykuş (Winking Owl)",
            "etiket_konum": [0.50, 0.36], "etiket_genislik": 0.44,
            "narration_insert": " Ön-arka omurga grafisinde metastazın tek taraflı pedikülü destrükte etmesiyle oluşan 'Göz Kırpan Baykuş' belirtisi açıkça izlenmektedir."
        }
    ],

    "y25-k2-14-beyin-tumorleri": [
        {
            "slide": 17, "pi": "16", "ci": 0,
            "odak": [0.36, 0.42, 0.64, 0.70],
            "a": [0.24, 0.56], "b": [0.44, 0.56],
            "etiket": "Santral nekroz ve kalın halkasal kontrastlanma (GBM)",
            "etiket_konum": [0.18, 0.30], "etiket_genislik": 0.46,
            "narration_insert": " Kontrastlı T1 MRG kesitinde glioblastomun kalın ve düzensiz halkasal kontrast tutulumu, santral hipointens nekrozu ve geniş çevre ödemi izlenmektedir."
        },
        {
            "slide": 43, "pi": "42", "ci": 0,
            "odak": [0.34, 0.32, 0.62, 0.60],
            "a": [0.22, 0.46], "b": [0.42, 0.46],
            "etiket": "Homojen kontrastlanma ve Dural Kuyruk (Dural Tail)",
            "etiket_konum": [0.16, 0.20], "etiket_genislik": 0.46,
            "narration_insert": " Menenjiom MRG kesitinde homojen parlak boyanan ekstra-aksiyel kitle ve komşu durada kalınlaşma şeklinde uzanan dural kuyruk işareti görülür."
        },
        {
            "slide": 46, "pi": "45", "ci": 0,
            "odak": [0.38, 0.46, 0.60, 0.68],
            "a": [0.26, 0.57], "b": [0.44, 0.57],
            "etiket": "Serebellopontin köşe kitlesi (Akustik nörinom)",
            "etiket_konum": [0.18, 0.34], "etiket_genislik": 0.44,
            "narration_insert": " Aksiyel MRG'de pontoserebellar köşeyi dolduran ve iç kulak yoluna uzanarak genişleten vestibüler schwannom kitlesi izlenmektedir."
        },
        {
            "slide": 55, "pi": "54", "ci": 0,
            "odak": [0.36, 0.38, 0.58, 0.62],
            "a": [0.24, 0.50], "b": [0.42, 0.50],
            "etiket": "Sellar genişleme ve kiazma optikum süperior basısı",
            "etiket_konum": [0.18, 0.26], "etiket_genislik": 0.46,
            "narration_insert": " Koronal MRG'de sella tursikayı genişletip yukarıya suprasellar alana taşan ve optik kiazmayı yukarı iten hipofiz makroadenomu izlenir."
        }
    ],

    "y25-k2-03-sss-hasar-bicimleri-odem-hidrosefali-herniasyon": [
        {
            "slide": 18, "pi": "17", "ci": 0,
            "odak": [0.38, 0.34, 0.62, 0.62],
            "a": [0.26, 0.48], "b": [0.44, 0.48],
            "etiket": "Ventrikülomegali ve transependimal BOS sızıntısı",
            "etiket_konum": [0.18, 0.22], "etiket_genislik": 0.44,
            "narration_insert": " Aksiyel tomografide lateral ventriküllerin ileri derecede genişlediği ve periventriküler beyaz cevherde transependimal BOS sızıntısı hipodansitesi izlenir."
        },
        {
            "slide": 26, "pi": "25", "ci": 0,
            "odak": [0.42, 0.32, 0.60, 0.56],
            "a": [0.28, 0.44], "b": [0.46, 0.44],
            "etiket": "Fals altına singulat girus herniasyonu ve şift",
            "etiket_konum": [0.20, 0.20], "etiket_genislik": 0.44,
            "narration_insert": " Herniasyon kesitinde kitle etkisiyle singulat girusun falks altından karşıya itildiği subfalsin herniasyon hattı görülmektedir."
        }
    ]
}

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

    # Apply narration additions and cizim additions
    modified_pars = False
    added_drawings = 0

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
        a_nokta = rec["a"]
        b_nokta = rec["b"]
        etiket = rec["etiket"]
        etiket_konum = rec.get("etiket_konum", [0.10, 0.85])
        narr_ins = rec.get("narration_insert", "")

        # Check if narration needs updating
        if pi in p_to_raw and narr_ins:
            raw_idx = p_to_raw[pi]
            cur_text = raw_blocks[raw_idx]
            if narr_ins.strip()[:30] not in cur_text:
                raw_blocks[raw_idx] = cur_text.strip() + narr_ins
                modified_pars = True

        # Construct Drawing Command with TIGHT ODAK + ARROW directly pointing to lesion
        k_range = [0, 80]
        new_z = {
            "tur": "akis",
            "s": slide,
            "k": k_range,
            "odak": odak,
            "a": a_nokta,
            "b": b_nokta,
            "iliski": "aktive",
            "etiket": etiket,
            "etiket_konum": etiket_konum,
            "etiket_genislik": rec.get("etiket_genislik", 0.42),
            "bas": 0,
            "son": 2
        }

        pi_str = str(pi)
        ci_str = str(ci)
        if pi_str not in cz_data["p"]:
            cz_data["p"][pi_str] = {}
        if ci_str not in cz_data["p"][pi_str]:
            cz_data["p"][pi_str][ci_str] = []

        # Replace or prepend the new drawing command
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
                    "a": rec["a"],
                    "b": rec["b"],
                    "iliski": "aktive",
                    "etiket": rec["etiket"],
                    "etiket_konum": rec.get("etiket_konum", [0.10, 0.85]),
                    "etiket_genislik": rec.get("etiket_genislik", 0.42),
                    "bas": 0,
                    "son": 2,
                    "cumle": f"P{pi}.C{ci}"
                }
                var_komutlar = [new_cmd] + [k for k in var_komutlar if not (k.get("sayfa") == rec["slide"] and k.get("tur") == "akis")]
            aday_data["komutlar"] = var_komutlar
            taslak_aday.write_text(json.dumps(aday_data, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"  Taslak cizim_aday.json güncellendi: {taslak_aday}")
        except Exception as e:
            print(f"  Taslak cizim_aday.json yazılamadı: {e}")

    print(f"  Cizim ve Isaret kaydedildi ({added_drawings} yeni hassas lezyon çizimi eklendi)")
    print(f"  Yeni metinHash: {new_h}")

def main():
    for key in RADYOLOJI_TANIMLARI.keys():
        zenginlestir_ders(key)

if __name__ == '__main__':
    main()
