import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import (
    make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz
)
from meds.scripts.apply_generated_deck import apply_deck

# Import all sections
from sec1 import get_sec1
from sec2 import get_sec2
from sec3 import get_sec3
from sec4 import get_sec4
from sec5 import get_sec5
from sec6 import get_sec6
from sec7 import get_sec7
from sec8 import get_sec8
from sec9 import get_sec9
from sec10 import get_sec10

DECK_ID = "k1p-k1-50-sifilis"

# Flashcards definition
def get_deck_50_flashcards():
    return [
        {"id": "fc-k1-50-001", "front": "Treponema pallidum'un mikroskobik morfolojisi ve Gram boyanma özelliği nedir?", "back": "İnce spiral şekilli bir spirokettir; Gram negatif benzeri duvarı olmasına rağmen standart Gram ile boyanmaz, karanlık saha ile görülür."},
        {"id": "fc-k1-50-002", "front": "Treponema'ların karakteristik tirbüşon (burgu) hareketini sağlayan yapı nedir?", "back": "Dış membran ile hücre duvarı arasındaki periplazmik aralıkta yer alan aksiyel flajelladır."},
        {"id": "fc-k1-50-003", "front": "Yaws, bejel ve pinta hastalıklarının etkeni olan Treponema türleri hangileridir?", "back": "Yaws: T. pallidum pertenue; Bejel: T. pallidum endemicum; Pinta: T. carateum."},
        {"id": "fc-k1-50-004", "front": "T. carateum'un (pinta) diğer treponemal hastalıklardan temel klinik farkı nedir?", "back": "Sadece cilt tutulumu yapar; kemik tutulumu kesinlikle görülmez."},
        {"id": "fc-k1-50-005", "front": "Sifilizin ortalama inkübasyon süresi ne kadardır?", "back": "3 ila 90 gün arasındadır; ortalama genellikle 3 haftadır (21 gün)."},
        {"id": "fc-k1-50-006", "front": "Primer sifilizin kardinal lezyonu nedir ve ağrılı mıdır?", "back": "Şankr adı verilen sert tabanlı, temiz ülserdir; tipik olarak tamamen ağrısızdır."},
        {"id": "fc-k1-50-007", "front": "Primer sifiliz şankrının bulaştırıcılık özelliği nasıldır?", "back": "Bol miktarda canlı spiroket içerdiğinden son derece bulaştırıcıdır."},
        {"id": "fc-k1-50-008", "front": "Primer şankra eşlik eden bölgesel lenfadenopatinin karakteri nasıldır?", "back": "Şankrdan yaklaşık 1 hafta sonra ortaya çıkan, ağrısız, sert ve lastik kıvamında LAP'tır."},
        {"id": "fc-k1-50-009", "front": "Primer şankr tedavi edilmediğinde doğal seyri nasıldır?", "back": "Tedavisiz kalsa dahi yaklaşık 3-6 hafta (yaklaşık 1 ay) içinde kendiliğinden iz bırakmadan iyileşir."},
        {"id": "fc-k1-50-010", "front": "Sekonder sifiliz tablosu şankrın ortaya çıkışından ne kadar süre sonra gelişir?", "back": "Genellikle şankrdan 2 ila 8 hafta sonra (bazen 24 haftaya kadar uzayabilir) ortaya çıkar."},
        {"id": "fc-k1-50-011", "front": "Sekonder sifilizin kutanöz döküntülerinin en tipik morfolojik özellikleri nelerdir?", "back": "Kaşıntısız, bilateral, simetrik, makülopapüler döküntülerdir; el içi ve ayak tabanında görülmesi patognomoniktir."},
        {"id": "fc-k1-50-012", "front": "Kondiloma lata nedir ve hangi sifiliz evresinde görülür?", "back": "Sekonder sifilizde nemli kıvrım bölgelerinde (perine, vulva) görülen gri-beyaz, yüksek oranda bulaştırıcı plaklardır."},
        {"id": "fc-k1-50-013", "front": "Sekonder sifilizde muayenede saptandığında sifilizi özellikle akla getiren lenf bezi tutulumu nedir?", "back": "Epitroklear lenfadenopatidir (dirsek iç yüzü LAP)."},
        {"id": "fc-k1-50-014", "front": "Sekonder sifilizde görülen saç dökülmesine ne ad verilir ve nasıldır?", "back": "Güve yeniği manzarası oluşturan toksik alopesidir; kaşların dış kısımları da dökülebilir."},
        {"id": "fc-k1-50-015", "front": "Latent sifiliz neyi ifade eder?", "back": "Sekonder bulguların kaybolmasından tersiyer bulgulara kadar geçen, serolojinin pozitif fakat klinik semptomun olmadığı dönemdir."},
        {"id": "fc-k1-50-016", "front": "Erken latent dönem ile geç latent dönem arasındaki zaman sınırı nedir?", "back": "İlk 1 yıl erken latent dönem; 1 yıldan sonrası ise geç latent dönemdir."},
        {"id": "fc-k1-50-017", "front": "Latent dönemde sekonder relapslar en sık ne zaman gerçekleşir?", "back": "Hastalığın ilk 1-4 yılında; relapsların %75-90'ı ilk yıl içinde meydana gelir."},
        {"id": "fc-k1-50-018", "front": "Tersiyer sifilizin lezyonları bulaştırıcı mıdır?", "back": "Hayır, tersiyer sifiliz lezyonları (gomlar, anevrizmalar) kural olarak bulaştırıcı değildir."},
        {"id": "fc-k1-50-019", "front": "Tersiyer sifilizde görülen gom (gumma) lezyonunun immünopatolojik mekanizması nedir?", "back": "Bakteri içermeyen veya çok az içeren, Tip IV gecikmiş tip hücresel aşırı duyarlılık sonucu oluşan granülomatöz lezyondur."},
        {"id": "fc-k1-50-020", "front": "Gom lezyonlarının vücutta en sık yerleştiği dokular hangileridir?", "back": "Cilt, kemikler (tibia, fibula, klavikula, kraniyum) ve karaciğerdir."},
        {"id": "fc-k1-50-021", "front": "Kronik nörosifilizin en sık görülen klinik formu hangisidir?", "back": "Asemptomatik nörosifilizdir (BOS anomalisi vardır fakat hasta yakınmasızdır)."},
        {"id": "fc-k1-50-022", "front": "Tabes dorsalis tablosunda omuriliğin hangi anatomik bölgesi dejenere olur?", "back": "Spinal kordun arka kordonları (dorsal kolonlar) ve dorsal kök gangliyonları dejenere olur."},
        {"id": "fc-k1-50-023", "front": "Tabes dorsalis'in kardinal nörolojik klinik triad bulguları nelerdir?", "back": "Propriyosepsiyon kaybı (duyusal ataksi), pozitif Romberg testi, şimşek çakar tarzda bacak ağrıları ve arefleksidir."},
        {"id": "fc-k1-50-024", "front": "Argyll Robertson pupilinin karakteristik nörolojik muayene yanıtı nedir?", "back": "Işığa yanıtsız (refleks yok), ancak akomodasyona normal yanıt veren (uyum sağlayan) pupilladır."},
        {"id": "fc-k1-50-025", "front": "Kardiyovasküler sifilizin altta yatan temel vasküler histopatolojisi nedir?", "back": "Aorta adventisyasındaki vaza vazorumların obliteratif endarteritidir (endarteritis obliterans)."},
        {"id": "fc-k1-50-026", "front": "Obliteratif endarteritin aortta yol açtığı majör klinik patolojiler nelerdir?", "back": "Çıkan aortta anevrizma (aortik anevrizma), aort kapak yetmezliği ve koroner ostium darlığıdır."},
        {"id": "fc-k1-50-027", "front": "Nontreponemal (spesifik olmayan) serolojik testler (VDRL, RPR) hangi antijeni tespit eder?", "back": "Doku hasarıyla salınan kardiyolipin-lesitin-kolesterol antijenine karşı oluşan antikorları (reagin) saptar."},
        {"id": "fc-k1-50-028", "front": "VDRL ve RPR testlerinin tedavi takibindeki yeri ve negatifleşme süresi nasıldır?", "back": "Tedavi takibinde titre düşüşüyle kullanılır; başarılı tedavi sonrası 1 ila 2 yılda tamamen negatifleşir."},
        {"id": "fc-k1-50-029", "front": "Treponemal spesifik testlerin (TPHA, FTA-ABS) temel klinik ve serolojik özelliği nedir?", "back": "En erken pozitifleşen ve en spesifik testlerdir; başarılı tedaviye rağmen ömür boyu pozitif kalırlar, tedavi takibinde kullanılmazlar."},
        {"id": "fc-k1-50-030", "front": "Primer, sekonder ve erken latent sifilizin standart küratif tedavisi nedir?", "back": "Tek doz Benzatin Penisilin G 2,4 milyon ünite intramusküler (IM) enjeksiyondur."}
    ]

if __name__ == "__main__":
    print("Building Deck 50 full...")
    all_slides = []
    all_slides.extend(get_sec1())
    all_slides.extend(get_sec2())
    all_slides.extend(get_sec3())
    all_slides.extend(get_sec4())
    all_slides.extend(get_sec5())
    all_slides.extend(get_sec6())
    all_slides.extend(get_sec7())
    all_slides.extend(get_sec8())
    all_slides.extend(get_sec9())
    all_slides.extend(get_sec10())
    
    flashcards = get_deck_50_flashcards()
    
    deck_path = "/home/indu/medsor/meds/src/data/decks/items/k1p-k1-50-sifilis.json"
    with open(deck_path, "r", encoding="utf-8") as f:
        deck = json.load(f)
        
    deck["slides"] = all_slides
    deck["flashcards"] = flashcards
    deck["totalSlides"] = len(all_slides)
    
    apply_deck(deck)
    print(f"Successfully applied {len(all_slides)} slides to {DECK_ID}")
