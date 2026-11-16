# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 22: Bebek Beslenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 4: Vitamin Desteği ve Özel Beslenme Riskleri (Slayt 31 - 40)
Checkpoint 4: Slayt 39
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_4_slides():
    slides = []

    # Slayt 31: Yenidoğanda D Vitamini Zorunluluğu ve Profilaksi Protokolü
    slides.append({
        "id": "k1-22-s31",
        "title": "Yenidoğanda D Vitamini Zorunluluğu ve Profilaksi Protokolü",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 31,
        "narrative": (
            "Anne sütü biyolojik olarak mucizevi bir içeriğe sahip olmakla birlikte, modern kapalı yaşam koşullarında "
            "bebeğin kemik sağlığı için yetersiz kalan **tek mikro besin ögesi D vitaminidir** (ortalama 20-40 IU/L). "
            "Bebeğin güneş ışığına doğrudan ve güvenli maruziyeti ise kış mevsimi, hava kirliliği ve cilt kanseri riski nedeniyle kısıtlıdır. "
            "**Sağlık Bakanlığı Ulusal D Vitamini Profilaksi Protokolü:** "
            "Türkiye'de doğan tüm bebeklere, doğum şekline ve beslenme türüne (anne sütü veya mama) bakılmaksızın "
            "**doğumdan itibaren (ilk haftadan başlayarak) en az 1 yaşına kadar günlük 400 IU (3 damla)** D vitamini desteği ücretsiz verilir. "
            "D vitamini verilmezse kalsiyum emilimi çöker; kraniyotabes (kafatası kemiğinde penguen yumurtası hissi), "
            "epifiz genişlemesi, raşitik rozari (kaburga boncuklaşması) ve O-bacak/X-bacak deformiteleriyle karakterize **Raşitizm (Rickets)** gelişir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de tüm bebeklere raşitizmi önlemek amacıyla doğumdan itibaren günlük 400 IU D vitamini desteği verilmesi zorunludur.",
                "400 IU",
                "Günlük üç damlaya denk gelen standart uluslararası profilaksi ünitesi dozu"
            ),
            make_causal_chain(
                "D Vitamini Eksikliğinde Raşitizm Patofizyolojisi",
                [
                    "1. Yetersiz Alım: Anne sütündeki düşük kalsiferol nedeniyle bağırsaktan Ca emilimi duraklar.",
                    "2. Sekonder Hiperparatiroidi: Düşen kalsiyumu yükseltmek için paratiroid bezi PTH salgılar.",
                    "3. Fosfatüri ve Demineralizasyon: PTH böbrekten fosforu atar; kemik osteoid dokusu mineralize olamaz.",
                    "4. İskelet Deformiteleri: Kraniyotabes, el bileğinde genişleme ve yürümeyle bacaklarda eğrilme belirir."
                ]
            ),
            make_active_recall(
                "Anne sütü alan sağlıklı bir bebeğe D vitamini desteği verilmemesi durumunda gelişen iskelet hastalığı hangisidir?",
                "Raşitizm (Rickets) tablosudur; kalsiyum ve fosfor kemik matrisine çökelemediğinden osteoid doku yumuşak kalır.",
                "Bebeklik çağı kemik mineralizasyon bozukluğu"
            )
        ]
    })

    # Slayt 32: K Vitamini ve Yenidoğanın Hemorajik Hastalığı
    slides.append({
        "id": "k1-22-s32",
        "title": "K Vitamini ve Yenidoğanın Hemorajik Hastalığı",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 32,
        "narrative": (
            "Yenidoğan bebekler pıhtılaşma sistemi açısından ciddi bir kanama riskiyle doğarlar: "
            "1. K vitamini plasentayı çok zayıf geçer (fetal depolar minimaldir). "
            "2. Yenidoğan bağırsağı doğduğunda sterildir; K vitamini sentezleyen bağırsak bakterileri henüz kolonize olmamıştır. "
            "3. Anne sütündeki K vitamini konsantrasyonu düşüktür. "
            "Bu üç faktör bir araya geldiğinde karaciğerde K vitaminine bağımlı pıhtılaşma faktörleri (**Faktör II, VII, IX, X**) sentezlenemez. "
            "Sonuçta yaşamın ilk günlerinde veya haftalarında göbek kanaması, melena, hematüri ve en ölümcülü "
            "**İntrakraniyal (Beyin İçi) Kanama** ile seyreden **Yenidoğanın Hemorajik Hastalığı** patlak verir. "
            "**Hayat Kurtaran Rutin:** Tüm dünyada ve Türkiye'de doğan her bebeğe doğum odasında **1 mg tek doz intramüsküler K1 vitamini** uygulanması mutlak standarttır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Yenidoğanın hemorajik hastalığını ve beyin kanamasını önlemek için doğumu takiben 1 mg intramüsküler K vitamini uygulanır.",
                "1 mg intramüsküler",
                "Doğum odasında uygulanan tek doz kas içi enjeksiyon miktarı"
            ),
            make_before_after(
                "K Vitamini Profilaksisi Yapılan ile Yapılmayan Bebek Kıyası",
                "Profilaksi Yapılmayan Bebek (Yüksek Risk)",
                "Faktör II, VII, IX ve X çöker; PT ve aPTT uzar; ölümcül kafa içi kanama ve kalıcı nörolojik sekel riski doğar.",
                "1 mg İM K1 Alan Bebek (Korunan)",
                "Karaciğer mikrozomal karboksilaz aktive olur; pıhtılaşma faktörleri hızla tamamlanır; kanama riski sıfırlanır.",
                "Ölümcül infantil intrakraniyal kanama riski ile doğumda tek enjeksiyonla tam koruma ayrımı"
            ),
            make_micro_quiz(
                "Yenidoğan bebeğe doğumda K vitamini uygulanmaması durumunda karaciğerde hangi faktörlerin sentezi bozulur?",
                {
                    "A": "Faktör I (Fibrinojen) ve Faktör VIII",
                    "B": "Faktör II (Protrombin), Faktör VII, Faktör IX ve Faktör X",
                    "C": "Faktör V ve Faktör XIII",
                    "D": "Yalnızca Doku Faktörü",
                    "E": "Trombosit granülleri ve von Willebrand Faktör"
                },
                "B",
                "Doğru cevap B'dir: K vitamini karaciğerde Faktör II, VII, IX, X ile Protein C ve S'in gama-karboksilasyonu için zorunlu kofaktördür; eksikliğinde bu 4 kritik prokoagülan faktör üretilemez ve ağır kanama tablosu gelişir."
            )
        ]
    })

    # Slayt 33: C Vitamini ve Suda Eriyen Vitaminler
    slides.append({
        "id": "k1-22-s33",
        "title": "C Vitamini ve Suda Eriyen Vitaminler",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 33,
        "narrative": (
            "Suda eriyen vitaminler vücutta depolanamaz ve sürekli besinlerle alınmak zorundadır: "
            "- **C Vitamini (Askorbik Asit):** "
            "Anne sütü C vitamini açısından zengindir ve iyi beslenen bir annenin sütü term bebeğin ilk 6 aydaki tüm C vitamini ihtiyacını fazlasıyla karşılar. "
            "Buna karşın **kaynatılmış inek sütü ve süt tozunda C vitamini neredeyse tamamen tahrip olur**! "
            "İnek sütüyle beslenen bebeklere dışarıdan C vitamini veya turunçgil suları verilmezse kollajen sentezi bozulur ve "
            "kemik zarı altı kanamalar, diş eti şişlikleri ve psödoparalizi ile seyreden **Skorbüt (Scorbutus)** gelişir. "
            "- **Maternal Beslenmenin Rolü:** "
            "Anne sütündeki B ve C vitamini konsantrasyonu annenin günlük beslenmesini birebir yansıtır; "
            "annenin dengeli taze sebze, meyve ve protein tüketmesi sütün kalitesini doğrudan artırır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütü ilk 6 ay için yeterli C vitamini sağlarken kaynatılmış inek sütü ve süt tozu C vitamininden son derece fakirdir.",
                "C vitamininden",
                "Kollajen sentezi ve askorbik asit aktivitesinden sorumlu bileşik"
            ),
            make_table(
                "Süt Türlerinde Suda Eriyen Vitamin Profili",
                ["Vitamin Türü", "Anne Sütündeki Durumu", "İnek Sütü / Süt Tozundaki Durumu", "Klinik Eksiklik Tablosu"],
                [
                    [
                        "C Vitamini",
                        "İlk 6 ay tam yeterli",
                        {"text": "Isıyla tahrip olur (Çok az)", "isMasked": True, "hint": "Pastörizasyon ve kaynatmayla yok olan vitamin içeriği"},
                        "Skorbüt (Subperiostal kanama)"
                    ],
                    ["Tiamin (B1)", "Maternal diyete bağlı yeterli", "Yeterli", "İnfantil Beriberi (Kalp yetmezliği)"],
                    ["Riboflavin (B2)", "Yeterli", "Yüksek", "Ariboflavinoz (Keilozis, glossit)"],
                    ["B6 Vitamini", "Yeterli", "Yeterli", "Piridoksin bağımlı konvülsiyonlar"]
                ]
            ),
            make_active_recall(
                "Kaynatılmış inek sütü ile beslenen bir bebekte kollajen hidroksilasyonunun bozulması sonucu gelişen klasik vitamin eksikliği hastalığı nedir?",
                "Skorbüt (Scorbutus / C vitamini eksikliği) hastalığıdır; subperiostal kanamalar ve kemik ağrısı nedeniyle bebek bacaklarını oynatamaz (psödoparalizi).",
                "Askorbik asit eksikliği ve kanama tablosu"
            )
        ]
    })

    # Slayt 34: B12 Vitamini Eksikliği: Vejetaryen Annelerin Bebekleri
    slides.append({
        "id": "k1-22-s34",
        "title": "B12 Vitamini Eksikliği: Vejetaryen Annelerin Bebekleri",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 34,
        "narrative": (
            "B12 vitamini (Kobalamin) doğada yalnızca hayvansal gıdalarda (et, süt, yumurta, karaciğer) bulunur. "
            "Uzun süredir katı **vejetaryen veya vegan beslenen annelerde** ya da teşhis edilmemiş pernisiyöz anemisi olan kadınlarda "
            "vücut B12 depoları tükenmiştir; dolayısıyla sütlerindeki B12 konsantrasyonu sıfıra yakındır. "
            "Bu annelerin sadece anne sütüyle beslenen bebeklerinde yaşamın 4 ila 8. aylarında sinsi ve dramatik bir tablo başlar: "
            "1. **Nörolojik Yıkım:** Baş kontrolünün kaybı, çevreye ilgisizlik (apati), hipotoni, irritabilite, tremor ve geri dönüşümsüz beyin atrofisi. "
            "2. **Hematolojik Çöküş:** Kemik iliğinde DNA sentezi duraklar ve **Megaloblastik Anemi** (pansitopeni ile birlikte) gelişir. "
            "3. **Metabolik Birikim:** İdrarda metilmalonik asit ve kanda homosistein tavan yapar. "
            "Bu nedenle katı vegan/vejetaryen emziren annelere ve bebeklerine doğumdan itibaren düzenli B12 desteği zorunludur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Katı vejetaryen annelerin sadece anne sütü alan bebeklerinde nörolojik gerileme ve megaloblastik anemi ile seyreden B12 vitamini eksikliği gelişir.",
                "B12 vitamini",
                "Yalnızca hayvansal besinlerde bulunan kobalamin türevi"
            ),
            make_causal_chain(
                "Maternal Vegan Beslenmeden İnfantil Nörolojik Hasara Gidiş",
                [
                    "1. Maternal Eksiklik: Hayvansal gıda tüketmeyen annenin sütünde B12 konsantrasyonu düşer.",
                    "2. Fetal/Neonatal Depo Kaybı: Bebeğin karaciğer B12 rezervi ilk 4 ayda tamamen tükenir.",
                    "3. Miyelin Defekti: Metilmalonil-KoA birikimiyle santral sinir sistemi miyelin kılıfı parçalanır.",
                    "4. Nörogelişimsel Kayıp: Bebek kazandığı motor becerileri kaybeder; apati ve konvülsiyon başlar."
                ]
            ),
            make_branching_logic(
                "6 aylık bir bebek başını tutamama, gülümsememe, kaslarda gevşeklik (hipotoni) ve solukluk şikayetiyle getiriliyor. Annenin 5 yıldır katı vegan olduğu ve bebeğin sadece anne sütü aldığı öğreniliyor. Tam kan sayımında MCV 108 fL (makrositoz) saptanıyor. En olası tanı ve acil tedavi adımı nedir?",
                [
                    {
                        "text": "B12 Vitamini (Kobalamin) eksikliğidir; kalıcı beyin hasarını önlemek için bebeğe ve anneye acilen parenteral/oral B12 vitamini tedavisi başlanmalıdır.",
                        "isCorrect": True,
                        "explanation": "Doğru. Katı vegan annelerin sütünde B12 bulunmaz; bebekte 4-8. aylarda hipotoni, motor beceri kaybı ve megaloblastik anemi tablosuyla patlak verir. Tedavi gecikirse nörolojik hasar kalıcı olur."
                    },
                    {
                        "text": "D Vitamini eksikliğidir; acilen yüksek doz kalsiyum ve D vitamini verilmelidir.",
                        "isCorrect": False,
                        "explanation": "Yanlış. D vitamini eksikliği raşitizm yapar, makrositer megaloblastik anemi ve hipotoni/apati yapmaz."
                    },
                    {
                        "text": "Fizyolojik bir büyüme atağıdır, hiçbir tedaviye gerek yoktur.",
                        "isCorrect": False,
                        "explanation": "Yanlış. Baş tutamama ve MCV 108 fL ağır patolojik tablolardır."
                    }
                ]
            )
        ]
    })

    # Slayt 35: İnek Sütü ve Süt Tozu Riskleri
    slides.append({
        "id": "k1-22-s35",
        "title": "İnek Sütü ve Süt Tozu Riskleri",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 35,
        "narrative": (
            "Geleneksel toplumlarda yapılan en büyük hatalardan biri, anne sütü yetmediğinde hemen inek sütü veya "
            "hazır süt tozu sulandırmalarına başvurulmasıdır. "
            "Bir yaşından küçük bebeklerde inek sütü ve süt tozu kullanımı hekimler tarafından **kesinlikle yasaklanmıştır**: "
            "1. **C Vitamini Yoksunluğu:** İnek sütünde C vitamini yok denecek kadar azdır; kaynatma işlemi kalan izleri de yok eder. "
            "2. **Aşırı Protein ve Yüksek Solüt:** 3 kat fazla protein ve üre yükü immatür böbreği tüketir, susuzluğa ve hipernatremiye sokar. "
            "3. **Mikrokanamalar ve Ağır Demir Eksikliği Anemisi:** İnek sütündeki kazein ve sığır albümini bebek bağırsağında "
            "subklinik inflamasyon ve kapiller kanamalara yol açar; dışkıyla kronik gizli kan kaybı derin anemi yaratır. "
            "4. **Fosfor Yüksekliği:** Hipokalsemik tetani nöbetlerini tetikler. "
            "Süt tozu ise steril olmayan sularla hazırlandığında veya yanlış konsantrasyonda sulandırıldığında ölümcül ishal ve hiperozmolar dehidratasyon yapar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "İnek sütü bebek bağırsağında alerjik mikrokanamalara yol açarak kronik demir kaybına ve derin anemiye zemin hazırlar.",
                "demir kaybına",
                "Gastrointestinal gizli hemoraji sonucu tükenen mineral rezervi"
            ),
            make_before_after(
                "İnek Sütü Zararları ve Anne Sütü Güvenliği Kıyaslaması",
                "İnek Sütü Verilen Bebek (1 Yaş Altı)",
                "C vitamini sıfırdır, aşırı protein böbreği yorar, bağırsakta mikrokanama ve derin demir eksikliği anemisi gelişir.",
                "Anne Sütü Alan Bebek",
                "C vitamini zengindir, protein idealdir (%6-7), bağırsak mukozasını korur ve demiri %50-60 emdirir.",
                "GİS kanaması ve solüt yükü yaratan inek sütü ile mukozayı koruyan anne sütü ayrımı"
            ),
            make_active_recall(
                "1 yaşından küçük bebeklere inek sütü verilmesinin gastrointestinal sistemdeki en tehlikeli kanamalı komplikasyonu nedir?",
                "Bağırsak mukozasında alerjik inflamasyona yol açarak dışkıyla gizli kan kaybına (mikrokanama) ve tedaviye dirençli ağır demir eksikliği anemisine yol açmasıdır.",
                "Gizli kan kaybı ve anemi mekanizması"
            )
        ]
    })

    # Slayt 36: Keçi Sütü Tehlikesi: Ağır Megaloblastik Anemi
    slides.append({
        "id": "k1-22-s36",
        "title": "Keçi Sütü Tehlikesi: Ağır Megaloblastik Anemi",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 36,
        "narrative": (
            "Halk arasında 'anne sütüne en yakın süt' olarak tanıtılan keçi sütü, aslında bebek beslenmesinde "
            "**en tehlikeli tuzaklardan biridir**. "
            "Bilimsel gerçekler keçi sütünün 1 yaşından önce verilmesinin ağır riskler taşıdığını gösterir: "
            "1. **Folik Asit (Folat) Yoksunluğu:** Keçi sütünde folik asit konsantrasyonu son derece düşüktür. "
            "Yalnızca keçi sütüyle beslenen bebeklerde birkaç ay içinde kemik iliğinde DNA sentezi durur ve "
            "ağır **'Keçi Sütü Megaloblastik Anemisi' (Goat's Milk Anemia)** tablosu gelişir! "
            "2. **B12, C ve D Vitamini Yetersizliği:** Keçi sütü bu hayati vitaminlerden de yoksundur. "
            "3. **Yüksek Renal Solüt Yükü:** Tıpkı inek sütü gibi yüksek mineral ve protein içeriğiyle bebek böbreğini zorlar. "
            "Bu nedenlerle modifiye edilmemiş doğal keçi sütü ilk 1 yaşta bebek beslenmesinde asla tek başına kullanılamaz."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Keçi sütü folik asit ve B12 vitamininden son derece fakir olduğundan bebeklerde ağır megaloblastik anemi tablosuna yol açar.",
                "folik asit",
                "Keçi sütünde neredeyse hiç bulunmayan B grubu hematopoetik vitamin"
            ),
            make_table(
                "Keçi Sütünün Pediatrik Beslenmedeki Kritik Eksiklikleri",
                ["Besin Öğesi / Parametre", "Keçi Sütündeki Durumu", "Yarattığı Klinik Patoloji"],
                [
                    [
                        "Folik Asit (Folat)",
                        {"text": "Aşırı düşüktür (Eksik)", "isMasked": True, "hint": "Keçi sütünün en meşhur vitamin yoksunluğu"},
                        "Keçi sütü megaloblastik anemisi ve pansitopeni"
                    ],
                    ["B12 Vitamini", "Yetersiz düzeyde", "Nörolojik gelişme geriliği ve apati"],
                    ["C ve D Vitamini", "Çok düşüktür", "Skorbüt ve ağır raşitizm kemik deformiteleri"],
                    ["Renal Solüt Yükü", "Çok yüksek (Protein/mineral fazla)", "Böbrek tübüler hasarı ve dehidratasyon"]
                ]
            ),
            make_micro_quiz(
                "Yalnızca taze keçi sütü ile beslenen 8 aylık bir bebekte solukluk, halsizlik ve dilde büyüme saptanıyor. Bu bebekte gelişen aneminin en temel biyokimyasal nedeni hangisidir?",
                {
                    "A": "Keçi sütünün aşırı demir içermesi sonucu demir zehirlenmesi",
                    "B": "Keçi sütünün folik asit ve B12 vitamininden son derece fakir olması",
                    "C": "Keçi sütündeki aşırı C vitamininin folatı parçalaması",
                    "D": "Keçi sütünün kalsiyum içermemesi",
                    "E": "Keçi sütündeki laktozun eritrositleri eritmesi"
                },
                "B",
                "Doğru cevap B'dir: Keçi sütü folik asit açısından son derece yetersizdir ve tek başına verildiğinde tipik olarak 'keçi sütü megaloblastik anemisi' oluşturur. Ayrıca C ve D vitamininden de fakirdir."
            )
        ]
    })

    # Slayt 37: İnfantil Botulizm Tehlikesi: 1 Yaşından Önce Bal Yasağı
    slides.append({
        "id": "k1-22-s37",
        "title": "İnfantil Botulizm Tehlikesi: 1 Yaşından Önce Bal Yasağı",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 37,
        "narrative": (
            "Pediatri pratiğinde en kesin ve tavizsiz kurallardan biri: **1 yaşından küçük hiçbir bebeğe BAL ve MISIR ŞURUBU VERİLEMEZ**! "
            "Bunun nedeni toksin değil, doğrudan **Clostridium botulinum sporlarıdır**. "
            "Arılar polen toplarken çevredeki toprak ve tozdan C. botulinum sporlarını bala taşırlar. "
            "- **Yetişkinlerde:** Mide asiditesi kuvvetlidir ve normal bağırsak mikrobiyotası sporların çimlenmesine izin vermez. "
            "- **Bebeklerde (1 Yaş Altı):** Mide asidi düşüktür ve normal bağırsak florası henüz tam oturmamıştır. "
            "Yutulan bal sporları bebek bağırsağında kolayca çimlenir, vejetatif bakteriye dönüşür ve in vivo ortamda "
            "ölümcül **Botulinum Nörotoksinini** üretir (**İnfantil Botulizm**). "
            "**Klinik Tablo:** İlk belirti inatçı kabızlıktır (konstipasyon). Ardından emme zayıflığı, ptozis (göz kapağı düşmesi), "
            "başını tutamama, gevşek bez bebek görünümü (floppy infant) ve diyafram felciyle ani solunum arresti ve ölüm gelişir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Bal Clostridium botulinum sporları içerebildiğinden infantil botulizm ve solunum felcini önlemek için 1 yaşından önce kesinlikle verilmez.",
                "Clostridium botulinum",
                "Gevşek felç yapan anaerop sporlu basil cinsi"
            ),
            make_causal_chain(
                "İnfantil Botulizm Patofizyolojik Kaskadı",
                [
                    "1. Bal Tüketimi: Bebeğe bal veya mısır şurubu ile C. botulinum sporları yutturulur.",
                    "2. Bağırsakta Çimlenme: Düşük asit ve immatür flora ortamında sporlar vejetatif basile döner.",
                    "3. Nörotoksin Salınımı: Bakteri bağırsak lümeninde botulinum nörotoksinini kana verir.",
                    "4. Kolinerjik Blok: Periferik nöromüsküler kavşakta asetilkolin salınımı durur.",
                    "5. Gevşek Felç (Floppy Baby): İnatçı kabızlığı takiben yukarıdan aşağıya inen flask paralizi ve solunum arresti gelişir."
                ]
            ),
            make_active_recall(
                "İnfantil botulizm tablosunda motor felç başlamadan günler önce beliren en erken ve tipik klinik öncü belirti nedir?",
                "İnatçı kabızlık (konstipasyon) tablosudur; bağırsak otonomik sinir uçlarında asetilkolin blokajına bağlı peristaltizm felcidir.",
                "GİS motilite kaybı ve dışkılayamama öncü belirtisi"
            )
        ]
    })

    # Slayt 38: Ev Yapımı Mamaların Riskleri
    slides.append({
        "id": "k1-22-s38",
        "title": "Ev Yapımı Mamaların Riskleri",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 38,
        "narrative": (
            "Ekonomik zorluklar veya yanlış inanışlar nedeniyle ailelerin evde un, pirinç unu, şeker, nişasta ve inek sütünü "
            "karıştırarak hazırladıkları **ev yapımı mamalar (un çorbaları, şekerli pirinç unu muhallebileri)** bebek sağlığı için büyük tehlikedir: "
            "1. **Besin Yoğunluğu Dengesizliği:** Bu mamalar boş karbonhidrat ve saf kaloriden ibarettir; protein kalitesi düşüktür, "
            "esansiyel yağ asitleri (linoleik asit), demir, çinko, A, C ve D vitaminlerini içermez. "
            "Uzun süre bu mamalarla beslenen bebeklerde şişman ancak ağır anemik ve ödemli **Kvaşiorkor** tablosu gelişir. "
            "2. **Yanlış Konsantrasyon:** Koyu hazırlanan mamalar hipertonik solüt yükü bindirerek hipernatremik dehidratasyona yol açar; "
            "aşırı sulu hazırlananlar ise su zehirlenmesi, hiponatremi ve beyin ödemi yapar. "
            "3. **Mikrobiyal Bulaş:** Ev ortamında pişen ve bekletilen karışımlar hızla patojen bakterilerle kontamine olur. "
            "Anne sütü yokluğunda formül mamalar haricinde ev yapımı karışımlarla besleme kesinlikle onaylanmaz."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Evde hazırlanan pirinç unlu ve şekerli mamalar protein ve mikro besinden fakir olduğundan ödemli malnütrisyon olan kvaşiorkor tablosuna yol açar.",
                "kvaşiorkor",
                "Saf protein açlığında beliren ödemli pediatrik tablo"
            ),
            make_before_after(
                "Ev Yapımı Karışımlar ile Standart Beslenme Ayrımı",
                "Ev Yapımı Unlu Karışımlar",
                "Boş karbonhidrattır; demir, çinko ve vitamin yoktur; mikrobiyal bulaş ve hiperozmolarite riski yüksektir.",
                "Anne Sütü / Standart Formül",
                "Tüm makro ve mikro besinler fizyolojik orandadır; biyoyararlanımı tamdır ve organları korur.",
                "Yetersiz dengesiz ev karışımları ile tam donanımlı bebek beslenmesi ayrımı"
            ),
            make_active_recall(
                "Yalnızca şekerli pirinç unu muhallebisiyle beslenen bir bebekte kalori yeterli olmasına rağmen neden bacaklarda ödem ve karaciğer yağlanması gelişir?",
                "Diyetin proteinden yoksun olması nedeniyle karaciğerde albümin ve apolipoprotein sentezlenemez; onkotik basınç düşerek ödem (kvaşiorkor) ve VLDL taşınamadığı için karaciğer yağlanması oluşur.",
                "Kvaşiorkor patofizyolojisi ve protein yoksunluğu"
            )
        ]
    })

    # Slayt 39: [TEKRAR SAYFASI - CHECKPOINT 4] Vitamin Profilaksisi ve Yasaklı Besinler
    slides.append({
        "id": "k1-22-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Vitamin Profilaksisi ve Yasaklı Besinler",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 39,
        "narrative": (
            "Bu dördüncü checkpoint sayfasında, bebeklik dönemindeki hayati vitamin profilaksilerini ve "
            "kesin yasaklı besinleri kilitliyoruz: "
            "1. **D Vitamini:** Doğumdan itibaren her bebeğe günlük 400 IU (3 damla) zorunludur; raşitizmi önler. "
            "2. **K Vitamini:** Doğumda 1 mg intramüsküler yapılır; yenidoğanın hemorajik hastalığını ve intrakraniyal kanamayı engeller. "
            "3. **B12 Vitamini:** Vegan/vejetaryen annelerin sütünde B12 yoktur; bebekte hipotoni, apati ve megaloblastik anemi yapar. "
            "4. **İnek Sütü Yasağı:** 1 yaşından önce verilmez; mikrokanamalarla demir eksikliği ve aşırı renal solüt yükü oluşturur. "
            "5. **Keçi Sütü Tehlikesi:** Folik asit ve B12 fakiridir; keçi sütü megaloblastik anemisine neden olur. "
            "6. **Bal Yasağı:** 1 yaşından önce C. botulinum sporları riski nedeniyle kesinlikle yasaktır; gevşek felç (botulizm) yapar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "k1-22-fc-10",
                "Yenidoğanın hemorajik hastalığını ve ölümcül kafa içi kanamaları önlemek amacıyla tüm yenidoğanlara doğumdan hemen sonra hangi profilaksi uygulanır?",
                "1 mg intramüsküler K1 vitamini",
                "Pıhtılaşma faktörlerinin karaciğerde sentezini başlatan tek doz doğum enjeksiyonu",
                "Profilaksi"
            ),
            make_flashcard(
                "k1-22-fc-11",
                "Bebeklerde Clostridium botulinum sporları içererek flask paralizi ve solunum durmasına (infantil botulizm) yol açabileceği için 1 yaşından önce kesinlikle yasak olan besin nedir?",
                "Bal (ve mısır şurubu)",
                "Arıların ürettiği tatlı besin maddesi",
                "Yasak Besinler"
            ),
            make_flashcard(
                "k1-22-fc-12",
                "Bebek beslenmesinde tek başına kullanıldığında folik asit, B12, C ve D vitamini eksikliğine bağlı ağır megaloblastik anemi tablosuna yol açan hayvan sütü hangisidir?",
                "Keçi sütü",
                "Folik asitten son derece fakir olan küçükbaş hayvan salgısı",
                "Yasak Besinler"
            )
        ]
    })

    # Slayt 40: Bölüm Özeti: Besin Kısıtlamalarından Altın Standart Anne Sütüne Geçiş
    slides.append({
        "id": "k1-22-s40",
        "title": "Bölüm Özeti: Besin Kısıtlamalarından Altın Standart Anne Sütüne Geçiş",
        "section": "Vitamin Desteği ve Özel Beslenme Riskleri",
        "slideNumber": 40,
        "narrative": (
            "Dışarıdan verilen inek sütü, keçi sütü, bal ve ev yapımı mamaların taşıdığı ölümcül riskleri gördükten sonra, "
            "anne sütünün neden eşsiz ve taklit edilemez bir altın standart olduğu çok daha berrak biçimde anlaşılmaktadır. "
            "Anne sütü sadece su, yağ, protein ve karbonhidrattan oluşan bir gıda değildir; "
            "aynı zamanda yaşayan canlı hücreler, büyüme faktörleri, enzimler ve antikorlar içeren biyolojik bir dokudur. "
            "Beşinci bölümümüzde, anne sütünün ilk 6 aydaki %100 kapsayıcılığı, sekretuvar IgA (sIgA) mukozal kalkanı, "
            "laktoferrin ve lizozimin antibakteriyel gücü, anne sütü oligosakkaritleri (HMO) ve uzun dönemli metabolik koruma "
            "tüm immünolojik derinliğiyle incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Bebek Beslenmesi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Anne sütü sadece pasif bir gıda olmayıp canlı hücreler ve antikorlar barındıran dinamik biyolojik bir doku niteliğindedir.",
                "biyolojik bir doku",
                "Canlı lökosit ve kök hücre içeren fonksiyonel yapı tanımı"
            ),
            make_causal_chain(
                "Anne Sütü Biyolojisinin Koruyucu Mimarisi",
                [
                    "1. Mukozal Koruma: Sekretuvar IgA bağırsak epitelini zırh gibi kaplayarak mikrop tutunmasını engeller.",
                    "2. Enzimatik Güç: Laktoferrin demiri bağlayarak bakterileri aç bırakır; lizozim hücre duvarını eritir.",
                    "3. Prebiyotik Flora: HMO oligosakkaritleri yararlı bifidobakterileri besleyerek kolon pH'sını asitleştirir.",
                    "4. Sistemik Olgunlaşma: EGF ve hormonlar bağırsak villuslarını hızla olgunlaştırarak emilimi mükemmelleştirir."
                ]
            ),
            make_active_recall(
                "Anne sütünü formül mamalardan ve hayvan sütlerinden ayıran en temel biyolojik ve immünolojik üstünlük nedir?",
                "Anne sütünün canlı lenfosit ve makrofajlar, sekretuvar IgA antikorları, lizozim, laktoferrin ve büyüme faktörleri içeren canlı dinamik bir biyolojik doku olmasıdır.",
                "Canlı hücre ve aktif antikor içeren biyolojik doku niteliği"
            )
        ]
    })

    return slides
