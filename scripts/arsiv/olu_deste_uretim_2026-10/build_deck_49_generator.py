import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide

DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

# Let's verify we can generate flashcards
def get_deck_49_flashcards():
    return [
        {"id": "fc-k1-49-001", "front": "Servisit tablosunda en sık karşılaşılan klinik başvuru yakınması nedir?", "back": "Lökore olarak adlandırılan irinli veya mukopürülan vajinal akıntıdır."},
        {"id": "fc-k1-49-002", "front": "Cinsel yolla bulaşan servisit olgularında en sık saptanan bakteriyel patojen hangisidir?", "back": "Chlamydia trachomatis'tir; CYBH kliniklerinde olguların yaklaşık %40'ından sorumludur."},
        {"id": "fc-k1-49-003", "front": "Normal vajinal florada tesadüfi olarak saptanabilen mikroorganizmalar hangileridir?", "back": "Aerob ve anaerob bakteriler, Streptococcus, Staphylococcus, Enterococcus, Escherichia coli ve Candida türleridir."},
        {"id": "fc-k1-49-004", "front": "Lökore teriminin klinik ve jinekolojik tanımı nedir?", "back": "Normalden farklı renk, koku veya kıvamda, genellikle beyaz veya sarımsı tonlarda izlenen vajinal akıntıdır."},
        {"id": "fc-k1-49-005", "front": "Genital herpes (HSV-2) enfeksiyonunun yenidoğan dönemindeki en tehlikeli riski nedir?", "back": "Doğum kanalından geçiş sırasında bulaşarak yenidoğanda ağır ve ölümcül sistemik herpes tablosuna yol açmasıdır."},
        {"id": "fc-k1-49-006", "front": "Servisit tanısında mikrobiyal etkeni kesinleştirmek için kullanılan en duyarlı moleküler yöntem nedir?", "back": "Vajinal/servikal sürüntüde nükleik asit amplifikasyon testleridir (NAAT / PCR)."},
        {"id": "fc-k1-49-007", "front": "Endoservikal polipin histopatolojik yapısı ve malign potansiyeli nasıldır?", "back": "Fibröz stroma ve mukus salgılayan endoservikal bezlerden oluşur; tamamen benign olup malign potansiyeli yoktur."},
        {"id": "fc-k1-49-008", "front": "Endoservikal poliplerin klinik olarak karsinom şüphesi yaratmasının ana sebebi nedir?", "back": "Yüzeyel ülserasyon ve kanama sonucu düzensiz vajinal kanamaya (metroraji) yol açmalarıdır."},
        {"id": "fc-k1-49-009", "front": "Endoservikal polip tedavisinde uygulanan standart yaklaşım nedir?", "back": "Polipektomi (basit cerrahi eksizyon veya küretaj) ve maligniteyi dışlamak için histolojik incelemedir."},
        {"id": "fc-k1-49-010", "front": "Endoserviks ile ektoserviksin normal epitelyal döşemeleri nasıldır?", "back": "Endoserviks tek katlı mukus salgılayan kolumnar epitel; ektoserviks çok katlı keratinize olmayan yassı epitel ile döşelidir."},
        {"id": "fc-k1-49-011", "front": "Ergenlikte eversiyon sonucu açığa çıkan kolumnar epitelde ne tür bir hücresel değişim gerçekleşir?", "back": "Vajinal asidik ortama yanıt olarak koruyucu skuamöz metaplazi gelişir."},
        {"id": "fc-k1-49-012", "front": "Servikste transformasyon bölgesi (TZ) neden karsinogenez için en kritik anatomik alandır?", "back": "Hızla bölünen olgunlaşmamış metaplastik skuamöz hücrelerden oluşur ve onkojenik HPV enfeksiyonuna en duyarlı alandır."},
        {"id": "fc-k1-49-013", "front": "Human Papilloma Virus'ün (HPV) temel virolojik yapısı nedir?", "back": "Zarsız, çift iplikli dairesel DNA virüsüdür."},
        {"id": "fc-k1-49-014", "front": "Serviks karsinogenezinde en kritik tek etiyolojik risk faktörü nedir?", "back": "Yüksek riskli HPV tipleriyle (özellikle HPV 16 ve 18) persistan (kalıcı) enfeksiyondur."},
        {"id": "fc-k1-49-015", "front": "Toplumda saptanan HPV enfeksiyonlarının büyük çoğunluğunun doğal seyri nasıldır?", "back": "Enfeksiyonların %80-90'ı geçicidir ve aylar/yıllar içinde immün sistem tarafından kendiliğinden temizlenir."},
        {"id": "fc-k1-49-016", "front": "Yüksek riskli HPV onkoproteini E6'nın karsinogenezdeki temel moleküler hedefi nedir?", "back": "Tümör baskılayıcı p53 proteinini bağlayıp ubikitin-proteazom yoluyla yıkar ve telomerazı aktive ederek apoptozu engeller."},
        {"id": "fc-k1-49-017", "front": "Yüksek riskli HPV onkoproteini E7'nin karsinogenezdeki temel moleküler hedefi nedir?", "back": "Retinoblastoma (RB) proteinine bağlanarak E2F transkripsiyon faktörünü serbest bırakır ve G1/S hücre döngüsü kontrolünü bozar."},
        {"id": "fc-k1-49-018", "front": "Düşük riskli HPV tipleri (6 ve 11) ile yüksek riskli tipler (16 ve 18) arasındaki temel genomik fark nedir?", "back": "Düşük riskli tiplerin DNA'sı episomal kalır; yüksek riskli tipler konak genomuna entegre olarak E6/E7 regülasyonunu bozar."},
        {"id": "fc-k1-49-019", "front": "Servikal karsinom ve CIN lezyonlarının yaklaşık %70'inden sorumlu iki spesifik HPV genotipi hangileridir?", "back": "HPV tip 16 ve HPV tip 18'dir."},
        {"id": "fc-k1-49-020", "front": "LSIL (CIN 1) lezyonunun epitel içindeki tutulum derinliği ve histopatolojik ayırt edici bulgusu nedir?", "back": "Epitelin alt 1/3'ü tutulur; yüzeysel ve orta katmanlarda belirgin koilositik değişiklik (perinükleer halo) izlenir."},
        {"id": "fc-k1-49-021", "front": "LSIL (CIN 1) lezyonlarının doğal seyrinde gerileme (regresyon) oranı kaçtır?", "back": "Olguların yaklaşık %60'ı spontan olarak tamamen geriler; bu nedenle prekanseröz kabul edilmez."},
        {"id": "fc-k1-49-022", "front": "HSIL lezyonlarının (CIN 2 ve CIN 3) epitel içindeki tutulum sınırları nasıldır?", "back": "CIN 2 epitelin alt 2/3'ünü tutarken; CIN 3 epitelin tam kalınlığını tutar (karsinoma in situ)."},
        {"id": "fc-k1-49-023", "front": "Koilosit hücre morfolojisinin tipik ışık mikroskobisi özellikleri nelerdir?", "back": "Hiperkromatik, düzensiz nükleus etrafında geniş şeffaf perinükleer halo ve kalınlaşmış sitoplazma kenarıdır."},
        {"id": "fc-k1-49-024", "front": "SIL insidansının zirve yaptığı yaş ile invaziv serviks kanseri yaş zirvesi nasıldır?", "back": "SIL insidansı ~30 yaşta zirve yaparken; invaziv karsinom 10-15 yıl sonra ~45 yaş civarında zirve yapar."},
        {"id": "fc-k1-49-025", "front": "Kolposkopik incelemede servikal displazik alanların beyaz görünmesini (asetobeyaz reaksiyon) sağlayan kimyasal solüsyon nedir?", "back": "%3-5'lik asetik asit solüsyonudur; artmış nükleer proteinleri çökelterek opak beyaz görünüm verir."},
        {"id": "fc-k1-49-026", "front": "Pap smear taramasının serviks kanseri mortalitesi üzerindeki halk sağlığı etkisi nedir?", "back": "Mortalite oranında yaklaşık %75 azalma sağlamış ve hastalığı önde gelen ölüm nedenleri arasından çıkarmıştır."},
        {"id": "fc-k1-49-027", "front": "Rutin servikal kanser taramasında HPV DNA testinin en değerli olduğu yaş grubu hangisidir?", "back": "30 yaş ve üzeridir; negatif çıktığında izleyen 5 yıl içinde neoplazi riski son derece düşüktür."},
        {"id": "fc-k1-49-028", "front": "İnvaziv serviks karsinomlarının en sık görülen histolojik tipi ve görülme oranı nedir?", "back": "Skuamöz hücreli karsinomdur (SCC) ve tüm serviks kanserlerinin yaklaşık %80'ini oluşturur."},
        {"id": "fc-k1-49-029", "front": "'Fıçı serviks' (barrel-shaped cervix) klinik morfolojisi neyi ifade eder?", "back": "Tümörün serviksi çepeçevre sararak stromaya derin invazyon yapması sonucu serviksin kalın, sert ve rijit bir silindir halini almasıdır."},
        {"id": "fc-k1-49-030", "front": "İleri evre invaziv serviks kanserli hastalarda en sık görülen ölüm nedeni nedir ve nasıl gelişir?", "back": "Tümörün parametriumlara ve üreterlere bası yaparak bilateral hidronefroz ve terminal üremiye yol açmasıdır."}
    ]

print("30 flashcards defined successfully.")
