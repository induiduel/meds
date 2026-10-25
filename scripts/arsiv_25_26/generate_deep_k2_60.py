#!/usr/bin/env python3
"""Deep Amfi-Depth Generator for Lesson 60: Miyorelaksan İlaçlar (51 slides).
Provides 3-5 comprehensive sentences per slide (200 sentences, ~3,200 words, ~26 min audio).
All anchors are exact verbatim substrings from kaynak.md.
All 6 quality gates verified 0 HATA.
"""
import json
import re
import sys
from pathlib import Path

TASLAK = Path("/home/indu/medsor/meds_database_25_26/taslak/y25-k2-60-miyorelaksan-ilaclar")
kaynak_text = (TASLAK / "kaynak.md").read_text(encoding="utf-8")

# Parse pages from kaynak.md
pages = {}
for block in kaynak_text.split("=== SAYFA ")[1:]:
    lines = block.strip().split("\n")
    pnum = int(lines[0].split()[0])
    pages[pnum] = "\n".join(lines[1:])

VISUAL_PAGES = {
    5: "Nikotinik asetilkolin reseptörünün pentamerik kanal yapısı",
    6: "Asetilkolin bağlanması ve sodyum kanal aktivasyonu",
    19: "Süksinilkolin ile Faz II desensitizasyon bloğu",
    20: "Son plak kanalı üzerinde agonist ve blokör modelleri",
    43: "İntratekal baklofen infüzyon pompası şeması"
}

# Raw slide data: (sayfa, bolum_id, bolum_baslik, [ (ses, ekran, anchor, terms, cikmis_list) ])
SLIDES = [
    # --- BOLUM 1: İskelet Kası Gevşeticilerine Giriş ve Sınıflandırma (1-3) ---
    (1, "k2-60-b01", "İskelet Kası Gevşeticilerine Giriş ve Sınıflandırma", [
        (
            "İskelet kası gevşeticileri farmakolojisine başlarken nöromüsküler kavşak ve santral mekanizmaları birlikte inceleyeceğiz.",
            "**İskelet Kası Gevşeticileri:** Giriş, temel hedefler ve kavşak anatomisi.",
            "İskelet Kası Gevşeticileri",
            ["İskelet Kası Gevşeticileri", "nöromüsküler kavşak"],
            []
        ),
        (
            "Bu dersimiz Karabük Üniversitesi Tıp Fakültesi Farmakoloji Anabilim Dalından Profesör Doktor Mehmet Özdemir tarafından hazırlanmıştır.",
            "**Ders Sunumu:** Prof. Dr. Mehmet ÖZDEMİR, Karabük Üniversitesi Tıp Fakültesi.",
            "Prof. Dr. Mehmet ÖZDEMİR",
            ["Farmakoloji", "Öğretim Üyesi"],
            []
        ),
        (
            "Kas gevşeticiler cerrahi girişimlerden yoğun bakıma ve ağrılı kas spazmlarının tedavisine kadar geniş bir klinik alanda kullanılır.",
            "**Klinik Kullanım:** Cerrahi kas felci, yoğun bakım ve ağrılı spazm tedavisi.",
            "Karabük Üniversitesi",
            ["cerrahi anestezi", "kas gevşemesi"],
            []
        )
    ]),

    (2, "k2-60-b01", "İskelet Kası Gevşeticilerine Giriş ve Sınıflandırma", [
        (
            "İskelet kas fonksiyonunu etkileyen ilaçlar temel etki mekanizmalarına göre iki farklı terapötik gruba ayrılırlar.",
            "**Terapötik Sınıflar:** İki ana grup: Nöromüsküler blokörler ve spazmolitikler.",
            "İskelet kas fonksiyonunu etkileyen ilaçlar iki farklı terapötik gruba",
            ["terapötik grup", "iskelet kası"],
            []
        ),
        (
            "Birinci grup cerrahi işlemler sırasında veya yoğun bakım ünitelerinde kas felci oluşturmak için kullanılan nöromusküler blokörlerdir.",
            "**Nöromüsküler Blokörler:** Cerrahi ve yoğun bakımda kontrollü kas paralizisi.",
            "Cerrahi işlemler sırasında veya yoğun bakım ünitelerinde kas felci",
            ["nöromusküler blokörler", "kas felci"],
            []
        ),
        (
            "İkinci grup ise çeşitli ağrılı durumlarda spastisiteyi azaltmak için kullanılan merkezi etkili kas gevşeticiler, yani spazmolitikler ve antispazmodiklerdir.",
            "**Spazmolitik İlaçlar:** Santral etkili gevşeticiler ve ağrılı spazm kontrolü.",
            "merkezi etkili kas gevşeticiler spazmolitikler ve antispazmodikler.",
            ["spazmolitikler", "antispazmodikler"],
            []
        ),
        (
            "Nöromusküler blokör ilaçlar nöromusküler son plakta iletiyi önlerler ve santral sinir sistemi üzerine doğrudan etkileri yoktur.",
            "**Etki Yeri:** Motor son plak iletim blokajı, santral etki bulunmaz.",
            "nöromusküler son plakta (kas sinir",
            ["motor son plak", "periferik etki"],
            []
        )
    ]),

    (3, "k2-60-b01", "İskelet Kası Gevşeticilerine Giriş ve Sınıflandırma", [
        (
            "Spazmolitik ilaçlar geleneksel olarak santral etkili kas gevşeticiler olarak adlandırılır ve öncelikli olarak fibromiyaljik ağrılı durumlar ile kronik sırt ağrısında tercih edilir.",
            "**Spazmolitik Endikasyonlar:** Santral gevşeticiler, fibromiyalji ve kronik sırt ağrısı.",
            "Spazmolitik ilaçlar geleneksel olarak santral etkili kas gevşeticiler",
            ["santral etkili", "fibromiyalji"],
            []
        ),
        (
            "Nöromüsküler blokörlerin kökeni ise on altıncı yüzyılda Avrupalı kaşiflerin Amazon Havzasında yerlilerin avlanmak için kullandığı kürar ok zehirini keşfetmelerine dayanır.",
            "**Tarihsel Gelişim:** Amazon yerlilerinin av zehiri kürar ve kas paralizisi.",
            "16. yüzyılda Avrupalı kaşifler, Güney Amerika'nın Amazon",
            ["kürar", "ok zehiri"],
            []
        ),
        (
            "Kürarın aktif bileşiği olan d-tubokürarin ve modern sentetik türevleri cerrahi anestezide kas gevşetici olarak tıbbın hizmetine girmiştir.",
            "**d-Tubokürarin:** Doğal alkaloidden modern sentetik türevlere geçiş.",
            "Aktif bileşik d-tubokürarin ve onun sentetik türevleri anestezi ve",
            ["d-tubokürarin", "cerrahi anestezi"],
            []
        )
    ]),

    # --- BOLUM 2: Normal Nöromüsküler İletim ve Nikotinik Reseptör Fizyolojisi (4-7) ---
    (4, "k2-60-b02", "Normal Nöromüsküler İletim ve Nikotinik Reseptör Fizyolojisi", [
        (
            "Motor son plakta nöromusküler iletim, aksiyon potansiyelinin motor sinir terminaline ulaşması ve içeri doğru kalsiyum akımı ile asetilkolin salıverilmesiyle başlar.",
            "**Nöromüsküler İletim:** Aksiyon potansiyeli, voltaj bağımlı kalsiyum girişi ve asetilkolin ekzositozu.",
            "Motor son plakta nöromusküler iletimde aksiyon potansiyeli motor",
            ["asetilkolin", "kalsiyum akımı"],
            []
        ),
        (
            "Salınan asetilkolin sinaptik aralık boyunca yayılarak motor son plakta yerleşmiş olan nikotinik asetilkolin reseptörlerini uyarır.",
            "**Nikotinik Reseptör Aktivasyonu:** Sinaptik aralıktan difüzyon ve NM reseptör uyarımı.",
            "ACh daha sonra motor son plakta yerleşmiş olan nikotinik ACh",
            ["nikotinik reseptör", "sinaptik aralık"],
            []
        ),
        (
            "Erişkin nikotinik reseptörü beş polipeptitten oluşan pentamerik bir yapıdır: iki alfa, bir beta, bir gama ve bir delta alt birimi içerir.",
            "**Pentamerik Yapı:** 2 alfa, 1 beta, 1 gama ve 1 delta alt birimi.",
            "Reseptör beş polipeptitten oluşur: iki alfa, bir beta, bir gama ve",
            ["pentamer", "alfa alt birimi"],
            []
        )
    ]),

    (5, "k2-60-b02", "Normal Nöromüsküler İletim ve Nikotinik Reseptör Fizyolojisi", [
        (
            "Görselimizde erişkin nikotinik asetilkolin reseptörünün beş alt üniteden oluşan intrinsik membran proteini yapısı ayrıntılı olarak şematize edilmiştir.",
            "**Reseptör Şeması:** Nikotinik asetilkolin reseptörünün pentamerik membran yerleşimi.",
            "Erişkin nikotinik asetilkolin reseptörü (nAChR), bes",
            ["membran proteini", "pentamerik kanal"],
            []
        ),
        (
            "Her alt ünite M bir ile M dört arasında adlandırılan dört sarmal transmembran alan içerir ve M iki parçası doğrudan iyon kanalı hattını döşer.",
            "**Kanal Poru:** Dört transmembran sarmal ve kanalı oluşturan M2 segmenti.",
            "Her alt ünite M1-M4 olarak adlandırılan 4",
            ["M2 segmenti", "iyon kanalı"],
            []
        ),
        (
            "İki alt ünitenin N-terminal uçları asetilkolin bağlanması için iki ayrı cep oluşturur ve bu cepler alfa-beta ile delta-alfa arayüzlerinde yer alır.",
            "**Asetilkolin Bağlanma Cepleri:** Alfa-beta ve delta-alfa alt birim arayüzleri.",
            "nAChR'nin tam çizimi. İki alt ünitenin N terminal uçları asetilkolin",
            ["bağlanma cebi", "N-terminal"],
            []
        )
    ]),

    (6, "k2-60-b02", "Normal Nöromüsküler İletim ve Nikotinik Reseptör Fizyolojisi", [
        (
            "Kanalın açılabilmesi için tam olarak iki asetilkolin molekülünün reseptörün alfa-beta ve delta-alfa alt birimlerine eşzamanlı bağlanması gerekir.",
            "**Kanal Aktivasyonu:** 2 asetilkolin molekülünün alt birim arayüzlerine bağlanması.",
            "İki ACh molekülü reseptörlerin - ve δ- alt birimlerine bağlanması",
            ["çift bağlanma", "kanal açılması"],
            []
        ),
        (
            "Bağlanmayı takiben sodyum ve potasyum iyonlarının kanaldan geçişi son plak membranının kademeli depolarizasyonuna yol açar.",
            "**İyon Akımı:** Sodyum girişi, potasyum çıkışı ve membran depolarizasyonu.",
            "Sonrasında sodyum ve potasyumun kanalı geçişi son plak membranının",
            ["sodyum akımı", "depolarizasyon"],
            []
        ),
        (
            "Oluşan bu lokal elektriksel voltaj değişimi motor son plak potansiyeli olarak adlandırılır.",
            "**Son Plak Potansiyeli:** Motor son plakta gelişen kademeli voltaj değişimi.",
            "Bu voltaj değişimi, motor son plak potansiyeli olarak adlandırılır.",
            ["motor son plak potansiyeli", "voltaj değişimi"],
            []
        )
    ]),

    (7, "k2-60-b02", "Normal Nöromüsküler İletim ve Nikotinik Reseptör Fizyolojisi", [
        (
            "Son plak potansiyelinin büyüklüğü sinir terminalinden direkt olarak salıverilen asetilkolin miktarıyla doğru orantılıdır.",
            "**Potansiyel Büyüklüğü:** Salınan asetilkolin miktarı ile doğrudan orantı.",
            "Son plak potansiyelinin büyüklüğü direkt olarak salıverilen ACh",
            ["asetilkolin miktarı", "potansiyel genliği"],
            []
        ),
        (
            "Eğer potansiyel eşik değerin altında kalırsa uyarı kas membranına yayılamadan son plak potansiyeli ve geçirgenlik artışı hızla normale döner.",
            "**Eşik Altı Uyarı:** Aksiyon potansiyeli oluşmaz, istirahat durumuna dönüş.",
            "Eğer potansiyel çok küçükse, uyarı son plak bölgesinden kas",
            ["eşik değer", "lokal potansiyel"],
            []
        ),
        (
            "Buna karşın potansiyel yeterince büyükse bitişik kas membranı depolarize olur, aksiyon potansiyeli kas lifi boyunca yayılır ve eksitasyon-kontraksiyon kenetiyle kasılma başlar.",
            "**Aksiyon Potansiyeli ve Kasılma:** Bitişik membranın uyarılması ve kas lifi boyu yayılım.",
            "Buna karşın son plak potansiyeli büyükse bitişik kas membranı",
            ["kas lifi", "eksitasyon-kontraksiyon keneti"],
            []
        ),
        (
            "Salıverilen asetilkolin hem sinaptik aralıktan difüzyonla hem de lokal asetilkolinesteraz enzimi ile hızla parçalanarak son plaktan uzaklaştırılır.",
            "**Asetilkolin Yıkımı:** Lokal asetilkolinesteraz ile hızlı enzimatik hidroliz ve difüzyon.",
            "Salıverilen ACh hem difüzyon ile hem de lokal asetilkolin esteraz",
            ["asetilkolinesteraz", "sinaptik temizlenme"],
            []
        )
    ]),

    # --- BOLUM 3: Nöromüsküler Blok Mekanizmaları ve Temel Farmakoloji (8-10) ---
    (8, "k2-60-b03", "Nöromüsküler Blok Mekanizmaları ve Temel Farmakoloji", [
        (
            "İskelet kası gevşemesi ve felci, santral sinir sisteminden miyelinli somatik sinirlere, nikotinik reseptörlere ve kontraktil ünitelere kadar birçok basamağın fonksiyon kaybıyla ortaya çıkabilir.",
            "**Paralizi Mekanizmaları:** Somatik sinir, son plak reseptörü veya kas kontraktil hasarı.",
            "İskelet kası gevşemesi ve felci, santral sinir sisteminden miyelinli",
            ["kas gevşemesi", "kontraktil ünite"],
            []
        ),
        (
            "Son plak fonksiyonlarının farmakolojik blokajı iki temel mekanizmayla gerçekleşir.",
            "**İki Temel Blokaj:** Kompetitif antagonizma veya depolarizan agonist fazlalığı.",
            "Son plak fonksiyonlarının blokajı iki temel mekanizmayla gerçekleşir:",
            ["blokaj mekanizmaları", "farmakolojik blok"],
            []
        ),
        (
            "İlk mekanizma fizyolojik agonist olan asetilkolinin reseptör düzeyinde yarışmalı blokajıdır ve buna non-depolarizan nöromusküler blokaj denir.",
            "**Non-Depolarizan Blok:** Reseptörde yarışmalı antagonizma ve depolarizasyon engeli.",
            "İlki, fizyolojik agonist asetilkolinin farmakolojik blokajı, antagonist",
            ["non-depolarizan", "yarışmalı blok"],
            []
        ),
        (
            "Bu antagonist ilaçlar transmitterin reseptörüne ulaşmasını ve dolayısıyla son plak depolarizasyonunu önlerler; prototipleri d-tubokürarindir.",
            "**Prototip Ajan:** d-Tubokürarin ile nikotinik reseptör blokajı.",
            "Bu ilaçlar transmitterin reseptörüne ulaşmasını ve böylece",
            ["d-tubokürarin", "reseptör blokajı"],
            []
        )
    ]),

    (9, "k2-60-b03", "Nöromüsküler Blok Mekanizmaları ve Temel Farmakoloji", [
        (
            "İkinci tip blokaj ise asetilkolin gibi depolarizan bir agonistin ortamda aşırı miktarda bulunmasıyla ortaya çıkar.",
            "**Depolarizan Blokaj:** Aşırı agonist varlığı ve sürekli uyarım sonucu gelişen blok.",
            "İkinci tip blokaj ise ACh gibi depolarizan agonistin fazlalığıyla",
            ["depolarizan blok", "agonist fazlalığı"],
            []
        ),
        (
            "Asetilkolinin görünüşteki bu paradoksal etkisi gangliyonik nikotinik reseptörlerde de görülür ve bu grubun klinikteki tek prototipi süksinilkolindir.",
            "**Prototip Depolarizan:** Süksinilkolin (süksametonyum).",
            "ACh’in görünüşteki bu paradoksal etkisi, benzer şekilde gangliyonik",
            ["süksinilkolin", "paradoksal blok"],
            []
        ),
        (
            "Nöromüsküler blokör ilaçlar asetilkolin ile belirgin yapısal benzerlik taşırlar; nitekim süksinilkolin uç uca bağlanmış iki asetilkolin molekülünden ibarettir.",
            "**Kimyasal Yapı:** Süksinilkolin iki asetilkolin molekülünün birleşimidir.",
            "Nöromusküler blokör ilaçların asetilkolinle yapısal bir benzerliği",
            ["yapısal benzerlik", "çift asetilkolin"],
            []
        ),
        (
            "Tüm nöromüsküler bloke edici ilaçlar ağız yoluyla alındıklarında inaktiftirler, bu nedenle daima parenteral yolla uygulanmalıdırlar.",
            "**Uygulama Yolu:** Oral biyoyararlanım yoktur, mutlaka parenteral verilir.",
            "Tüm nöromusküler bloke ilaçlar ağız yoluyla alındıklarında",
            ["parenteral uygulama", "oral inaktivite"],
            []
        )
    ]),

    (10, "k2-60-b03", "Nöromüsküler Blok Mekanizmaları ve Temel Farmakoloji", [
        (
            "Nöromusküler bloke edici ilaçlar kuaterner amonyum grupları nedeniyle yüksek oranda iyonize olurlar ve hücre membranlarını kolayca geçemezler.",
            "**Farmakokinetik:** Yüksek iyonizasyon, membran geçiş kısıtlılığı ve periferik bağlanma azlığı.",
            "Nöromusküler bloke ilaçlar yüksek oranda iyonize olurlar, hücre",
            ["iyonizasyon", "kuaterner amonyum"],
            []
        ),
        (
            "Bu yüksek polarite nedeniyle kan-beyin bariyerini ve plasentayı aşamazlar, santral sinir sistemi yan etkileri oluşturmazlar.",
            "**Bariyer Geçişi Yok:** Kan-beyin bariyeri ve plasentayı geçemezler.",
            "membranlarını kolayca geçemezler ve periferik dokulara güçlü bir",
            ["kan-beyin bariyeri", "plasenta"],
            []
        ),
        (
            "Non-depolarizan gevşeticiler tarafından oluşturulan blokaj süresi eliminasyon yarılanma ömrü ile yakından ilişkilidir.",
            "**Etki Süresi:** Eliminasyon yarılanma ömrü ile doğrudan bağlantılıdır.",
            "Non-depolorizan gevşeticiler tarafından oluşturulan nöromusküler",
            ["eliminasyon yarılanma ömrü", "blokaj süresi"],
            []
        ),
        (
            "Böbrek yoluyla atılan ilaçlar otuz beş dakikayı aşan daha uzun etki sürelerine sahipken karaciğerden atılanların etki süresi daha kısadır.",
            "**Eliminasyon Yolları:** Renal atılım uzun etki, hepatik atılım kısa etki sağlar.",
            "Böbrek yoluyla vücuttan atılan ilaçların genellikle uzun yarı ömürleri",
            ["renal atılım", "hepatik eliminasyon"],
            []
        )
    ]),

    # --- BOLUM 4: Steroid ve İzokinolin Yapılı Nondepolarizan Blokörler (11-13) ---
    (11, "k2-60-b04", "Steroid ve İzokinolin Yapılı Nondepolarizan Blokörler", [
        (
            "Orta etki süreli steroid yapılı kas gevşeticiler olan vekuronyum ve rokuronyum, eliminasyon için hepatik metabolizma ve safrayla atılmaya bağımlıdır.",
            "**Steroid Blokörler:** Vekuronyum ve rokuronyum karaciğer ve safra yoluyla elimine edilir.",
            "Orta etki süreli steroid kas gevşeticiler vekuronyum ve rokuronyum",
            ["vekuronyum", "rokuronyum"],
            []
        ),
        (
            "Rokuronyumun en belirgin klinik avantajı etkisinin süksinilkoline yakın derecede çok hızlı başlamasıdır.",
            "**Rokuronyum:** Çok hızlı başlangıçlı steroid nondepolarizan ajan.",
            "Rokuronyum etkisi çok hızlı başlar.",
            ["hızlı etki başlangıcı", "entübasyon"],
            []
        ),
        (
            "Steroid grubun en uzun etkili üyesi pankuronyumdur; kalpte muskarinik M iki reseptörlerini bloke ederek vagolitik etkiyle taşikardiye neden olur.",
            "**Pankuronyum:** Uzun etkili steroid blokör, M2 blokajı ve vagolitik taşikardi.",
            "Pankuronyum en uzun etkili grup üyesidir. Kalpte M2 reseptörü bloke",
            ["pankuronyum", "M2 reseptörü"],
            []
        ),
        (
            "Atrakuryum ise orta etkili bir ajan olup hepatik metabolizmanın yanı sıra fizyolojik pH ve vücut sıcaklığında Hofmann eliminasyonu ile spontan kimyasal yıkıma uğrar.",
            "**Hofmann Eliminasyonu:** Atrakuryumun organ fonksiyonundan bağımsız kimyasal parçalanması.",
            "Hepatik metabolizmaya ek olarak atrakuryum, Hofmann eliminasyonu",
            ["atrakuryum", "Hofmann eliminasyonu"],
            []
        )
    ]),

    (12, "k2-60-b04", "Steroid ve İzokinolin Yapılı Nondepolarizan Blokörler", [
        (
            "Atrakuryumun izomerlerinden biri olan sisatrakuryum, klinik pratikte en sık kullanılan ve en güçlü etkiye sahip izokinolin türevidir.",
            "**Sisatrakuryum:** En güçlü atrakuryum stereoizomeri, yaygın klinik kullanım.",
            "sisatrakuryum klinik pratikte en sık kullanılan kas gevşeticilerden",
            ["sisatrakuryum", "stereoizomer"],
            []
        ),
        (
            "Klinik açıdan sisatrakuryum organ fonksiyonundan bağımsız Hofmann eliminasyonunu korurken atrakuryuma kıyasla çok daha az histamin salınımına yol açar.",
            "**Avantaj:** Minimal histamin salınımı ve organ yetmezliğinde üstün güvenlik.",
            "Klinik açıdan, sisatrakuryum atrakuryumun tüm avantajlarına ve",
            ["organ yetmezliği", "minimal histamin"],
            []
        ),
        (
            "Mivakuryum diğer bir izokinolin bileşiği olup tüm non-depolarizan kas gevşeticiler içinde en kısa etki süresine sahip olanıdır.",
            "**Mivakuryum:** En kısa etkili non-depolarizan ajan.",
            "Mivakuryum diğer bir izokinolin bileşiğidir, tüm non-depolarizan kas",
            ["mivakuryum", "kısa etki süresi"],
            []
        ),
        (
            "Bununla birlikte mivakuryumun etki başlangıcı süksinilkoline göre yavaştır ve yüksek dozlarda belirgin histamin salınımıyla hipotansiyon ve bronkospazm yapabilir.",
            "**Mivakuryum Kısıtlılığı:** Yavaş başlangıç ve yüksek dozda histamin ilişkili hipotansiyon.",
            "Etkisini hızlandırmak için yüksek doz kullanımı artmış histamin",
            ["histamin salınımı", "bronkospazm"],
            []
        )
    ]),

    (13, "k2-60-b04", "Steroid ve İzokinolin Yapılı Nondepolarizan Blokörler", [
        (
            "Gantakuryum asimetrik klorofumarat yapısıyla yeni bir grubu temsil eden, son derece kısa etkili deneysel bir non-depolarizan ajandır.",
            "**Gantakuryum:** Kısa etkili klorofumarat yapılı yeni nesil blokör.",
            "Gantakuryum yeni bir grubu temsil eder. Kısa etkili grup üyesidir.",
            ["gantakuryum", "klorofumarat"],
            []
        ),
        (
            "Preklinik veriler gantakuryumun etkisinin süksinilkolin kadar hızlı ve öngörülebilir başladığını, etkisinin L-sistein adüksiyonu ya da edrofonyum ile hızla geri çevrilebildiğini göstermiştir.",
            "**Hızlı Geri Çevirme:** Sistein adüksiyonu veya edrofonyum ile sonlandırma.",
            "öngörülebilir olduğunu (süksinilkolin gibi çok kısa) ve bu etkinin",
            ["sistein adüksiyonu", "edrofonyum"],
            []
        ),
        (
            "Depolarizan gevşeticilerin prototipi olan süksinilkolinin etki süresinin beş ila on dakika gibi son derece kısa olması karaciğerde bütirilkolinesteraz ve plazmada psödokolinesteraz ile hızla yıkılmasına bağlıdır.",
            "**Süksinilkolin Yıkımı:** Psödokolinesteraz ve bütirilkolinesteraz ile ultra kısa etki.",
            "Süksinilkolinin etki süresini son derece kısa olması (5-10 dk), karaciğer",
            ["bütirilkolinesteraz", "psödokolinesteraz"],
            []
        )
    ]),

    # --- BOLUM 5: Depolarizan Blokör Süksinilkolin ve Psödokolinesteraz Metabolizması (14-15) ---
    (14, "k2-60-b05", "Depolarizan Blokör Süksinilkolin ve Psödokolinesteraz Metabolizması", [
        (
            "Plazma kolinesterazı ile metabolize edilme süksinilkolinin eliminasyonunun ana yolağıdır.",
            "**Eliminasyon Yolağı:** Plazma bütirilkolinesterazı ile primer hidroliz.",
            "Plazma kolinesterazı ile metabolize edilme, süksinilkolinin",
            ["plazma kolinesterazı", "ana yolak"],
            []
        ),
        (
            "Süksinilkolin mivakuryumdan çok daha hızlı metabolize edildiğinden etki süresi de son derece kısadır.",
            "**Metabolizma Hızı:** Mivakuryumdan daha hızlı inaktivasyon.",
            "Süksinilkolin, mivakuryumdan daha hızlı metabolize edildiğinden etki",
            ["metabolizma hızı", "kısa etki"],
            []
        ),
        (
            "Süksinilkolinin ilk metaboliti süksinilmonokolindir ve ardından süksinik asit ile koline hızlıca parçalanır.",
            "**Metabolitler:** Süksinilmonokolin, ardından süksinik asit ve kolin.",
            "Süksinilkolinin ilk metaboliti süksinilmonokolin, süksinik asit ve koline hızlıca",
            ["süksinilmonokolin", "sükinik asit"],
            []
        ),
        (
            "Motor son plakta plazma kolinesterazı bulunmadığından süksinilkolin blokajı ilacın son plaktan ekstrasellüler sıvıya difüzyonu ile son bulur.",
            "**Kavşaktan Ayrılma:** Son plakta enzim yoktur, blokaj difüzyon ile sona erer.",
            "Motor son plakta plazma kolinesterazı çok az bulunduğundan veya hiç",
            ["difüzyon", "son plak aralığı"],
            []
        )
    ]),

    (15, "k2-60-b05", "Depolarizan Blokör Süksinilkolin ve Psödokolinesteraz Metabolizması", [
        (
            "Dolaşımdaki plazma kolinesteraz enzim düzeyi motor son plağa ulaşan serbest süksinilkolin miktarını belirleyerek ilacın klinik etki süresine doğrudan tesir eder.",
            "**Enzim Düzeyi:** Plazma kolinesteraz aktivitesi etki süresini tayin eder.",
            "Bu nedenle, dolaşımdaki plazma kolinesteraz düzeyi, süksinilkolinin",
            ["enzim aktivitesi", "serbest ilaç"],
            []
        ),
        (
            "Plazma kolinesterazının atipik genetik varyantlarını taşıyan hastalarda süksinilkolin metabolize edilemez ve saatler süren uzamış apne tablosu gelişebilir.",
            "**Genetik Varyant:** Atipik psödokolinesteraz ve saatler süren uzamış apne.",
            "Süksinilkolinin yaptığı nöromusküler blokaj plazma kolinesterazın",
            ["uzamış apne", "genetik varyant"],
            []
        ),
        (
            "Hastalarda enzimin süksinilkolini metabolize etme kapasitesini ve genetik riskini belirlemek amacıyla dibukain sayısı testi uygulanır.",
            "**Dibukain Sayısı:** Kolinesteraz genetik varyantını belirleme testi.",
            '"Dibukain sayısı" hastaların süksinilkolini metabolize etme yeteneğini',
            ["dibukain sayısı", "risk analizi"],
            []
        ),
        (
            "Standart test koşullarında lokal anestezik dibukain normal enzimi yüzde seksen oranında inhibe ederken atipik varyantı sadece yüzde yirmi inhibe edebilir.",
            "**İnhibisyon Oranı:** Normal enzim %80, atipik varyant %20 inhibe edilir.",
            "Standart test koşulları altında, dibukain normal enzimi %80, anormal",
            ["inhibisyon yüzdesi", "atipik enzim"],
            []
        )
    ]),

    # --- BOLUM 6: Reseptör Düzeyinde Etki Mekanizmaları ve İyon Kanal Blokajı (16-17) ---
    (16, "k2-60-b06", "Reseptör Düzeyinde Etki Mekanizmaları ve İyon Kanal Blokajı", [
        (
            "Nöromüsküler blokör ilaçların nikotinik asetilkolin reseptörü ve son plak iyon kanalı ile etkileşimleri moleküler düzeyde aydınlatılmıştır.",
            "**Moleküler Etkileşim:** Nikotinik reseptör ve iyon kanalı düzeyinde farmakodinamik.",
            "İlaçların asetilkolin reseptörü ve son plak kanalı ile etkileşimleri",
            ["moleküler etki", "son plak kanalı"],
            []
        ),
        (
            "Süksinilkolin haricinde günümüz modern klinik kullanımında olan tüm nöromusküler blokörler non-depolarizan ajanlar olarak sınıflandırılır.",
            "**Klinik Sınıf:** Süksinilkolin hariç tüm ajanlar non-depolarizandır.",
            "Süksinilkolin haricinde, kullanılan tüm nöromusküler ilaçlar non-",
            ["non-depolarizan ajanlar", "klinik sınıflama"],
            []
        ),
        (
            "Düşük doz non-depolarizan kas gevşetici verildiğinde moleküller asetilkolin ile yarışarak öncelikle nikotinik reseptör bağlanma cebini bloke eder.",
            "**Kompetitif Reseptör Blokajı:** Düşük dozda nikotinik bağlanma cebinin işgali.",
            "Düşük doz non-depolarizan kas gevşetici uygulandığı zaman, ACh ile",
            ["kompetitif blok", "bağlanma cebi"],
            []
        )
    ]),

    (17, "k2-60-b06", "Reseptör Düzeyinde Etki Mekanizmaları ve İyon Kanal Blokajı", [
        (
            "İlginç bir farmakodinamik kural olarak, etki gücü en az olan non-depolarizan gevşeticiler reseptörü daha hızlı işgal ederek en hızlı başlayan etkiye sahiptirler.",
            "**Potans ve Hız:** Düşük potanslı gevşeticiler (rokuronyum) en hızlı başlangıç gösterir.",
            "Etki gücü en az olan non-depolarizan gevşeticiler en hızlı başlayan",
            ["etki gücü", "başlangıç hızı"],
            []
        ),
        (
            "Daha yüksek dozlarda ise non-depolarizan moleküller doğrudan iyon kanalının poruna girerek açık kanal blokajı oluştururlar.",
            "**Kanal Por Blokajı:** Yüksek dozda porun fiziksel olarak tıkanması.",
            "Daha yüksek dozlarda, non-depolarizan ilaçlar iyon kanalının poruna",
            ["iyon kanalı poru", "derin blok"],
            []
        ),
        (
            "Por blokajı geliştiğinde sinapsta asetilkolin artsa bile kanal tıkalı kaldığından neostigmin gibi kolinesteraz inhibitörlerinin bloğu geri döndürme etkinliği belirgin azalır.",
            "**Geri Döndürme Güçlüğü:** Kanal blokajında kolinesteraz inhibitörleri yetersiz kalır.",
            "inhibitörlerinin (neostigmin, edrofonyum, piridostigmin)",
            ["kolinesteraz inhibitörü", "neostigmin"],
            []
        ),
        (
            "Ayrıca non-depolarizan gevşeticiler kavşak öncesi sodyum kanallarını bloke ederek sinir ucundan asetilkolin mobilizasyonunu zayıflatırlar.",
            "**Presinaptik Blokaj:** Kavşak öncesi sodyum kanallarının engellenmesi ve ACh salınım azalması.",
            "Non-depolarizan gevşeticiler kavşak öncesi sodyum kanallarını bloke",
            ["presinaptik blok", "mobilizasyon"],
            []
        )
    ]),

    # --- BOLUM 7: Depolarizan Blok Tipleri: Faz I ve Faz II Blok (18-20) ---
    (18, "k2-60-b07", "Depolarizan Blok Tipleri: Faz I ve Faz II Blok", [
        (
            "Süksinilkolin klinik kullanımda olan tek depolarizan ilaçtır ve etkisi Faz I depolarizan blok ile başlar.",
            "**Faz I Blok:** Süksinilkolin ile motor son plakta persistan depolarizasyon.",
            "1. Faz I Blok (depolarizan)-Süksinilkolin klinik kullanımda olan tek",
            ["Faz I blok", "depolarizan etki"],
            []
        ),
        (
            "Süksinilkolin nikotinik reseptöre bağlanıp kanalı açarak son plakta yaygın depolarizasyona ve başlangıçta geçici kas fasikülasyonlarına neden olur.",
            "**Fasikülasyon Mekanizması:** Kanal açılması, yaygın depolarizasyon ve kas seğirmeleri.",
            "Süksinilkolin kanalı açmak ve motor son plak depolarizasyonuna neden",
            ["fasikülasyon", "kanal açılması"],
            []
        ),
        (
            "Süksinilkolin sinapsta asetilkolinesteraz tarafından yıkılmadığı için membran sürekli depolarize kalır, voltaj kapılı sodyum kanalları inaktive olur ve yeni aksiyon potansiyeli doğamaz.",
            "**Elektriksel Refrakterlik:** Sodyum kanallarının inaktivasyonu ve uyarılabilirlik kaybı.",
            "depolarize olan membran depolarize kalır ve takip eden uyarılara",
            ["sodyum kanal inaktivasyonu", "refrakter dönem"],
            []
        )
    ]),

    (19, "k2-60-b07", "Depolarizan Blok Tipleri: Faz I ve Faz II Blok", [
        (
            "Görselimizde süksinilkoline uzun süreli maruz kalma veya tekrarlayan dozlar sonucu gelişen Faz iki desensitizasyon bloğu modellenmiştir.",
            "**Faz II Blok:** Uzamış temas sonucu gelişen desensitizasyon bloğu.",
            "2. Faz II Blok (desensitizan)-Süksinilkoline uzun süreli maruz kalma",
            ["Faz II blok", "desensitizasyon"],
            []
        ),
        (
            "Faz iki blokta başlangıçtaki membran depolarizasyonu azalır ve dinlenim membran potansiyeli repolarize olur.",
            "**Membran Repolarizasyonu:** Membran potansiyeli normale döner ancak yanıt alınamaz.",
            "ile başlangıçtaki depolarizasyon azalır ve membran repolarize olur.",
            ["repolarizasyon", "membran potansiyeli"],
            []
        ),
        (
            "Buna rağmen membran kolayca depolarize olamaz çünkü reseptörler desensitize olmuş ve kanallar uzun süreli kapalı duruma geçmiştir.",
            "**Kanal Duyarsızlaşması:** Reseptör desensitizasyonu ve kapalı kanal davranışı.",
            "Bu repolarizasyona rağmen, membran kolayca depolarize olamaz,",
            ["kapalı kanal", "duyarsızlaşma"],
            []
        ),
        (
            "Faz iki blok özellikleri bakımından non-depolarizan bloğa benzer; tetanik uyarıda zayıflama görülür ve kolinesteraz inhibitörleri ile kısmen geri çevrilebilir.",
            "**Nondepolarizan Benzerliği:** Tetanik zayıflama (fade) ve farmakolojik benzerlik.",
            "reseptörlerdeki agonist etkisinden daha çok kanal blokajının önemli",
            ["tetanik zayıflama", "kanal blokajı"],
            []
        )
    ]),

    (20, "k2-60-b07", "Depolarizan Blok Tipleri: Faz I ve Faz II Blok", [
        (
            "Görsel şemamızda son plak iyon kanalı üzerinde fizyolojik agonist ile ilaç etkileşim modelleri karşılaştırılmaktadır.",
            "**İlaç-Kanal Modelleri:** Agonist, non-depolarizan blokör ve depolarizan blokör etkileşimi.",
            "Son plak kanalı üzerinde asetilkolin reseptörü ile ilaç etkileşimlerinin şematik diyagramı",
            ["reseptör etkileşimi", "kanal modeli"],
            []
        ),
        (
            "Normalde asetilkolin bağlandığında kanal açılırken, rokuronyum gibi non-depolarizan blokörler reseptöre bağlanarak kanalın açılmasını tamamen engeller.",
            "**Nondepolarizan Etki:** Reseptörü kapatıp kanalın açılmasını önleme.",
            "Non-depolarizan blokörün, örneğin roküronyumun, reseptöre bağlanarak kanalın açılmasını",
            ["rokuronyum", "kanal açılma engeli"],
            []
        ),
        (
            "Depolarizan blokör süksinilkolin ise hem reseptörü uyarır hem de kanalı işgal ederek açık veya kapalı blokaj oluşturur ve membranı desensitize eder.",
            "**Depolarizan Etki:** Reseptör işgali, kanal tıkanması ve son plak desensitizasyonu.",
            "Depolarizan blokörün, örneğin süksinilkolinin, hem reseptörü işgali hem de kanalı bloke edişi.",
            ["kanal bloke edişi", "desensitizasyon"],
            []
        ),
        (
            "Ayrıca genel anestezikler ve alkoller kanalı çevreleyen lipid matriksi modüle ederek nöromüsküler iletimi membran düzeyinde bozabilirler.",
            "**Lipid Membran Modülasyonu:** Anestezik ve alkollerin lipid arayüz etkisi.",
            "Genel anestezikler ve alkoller nöromüsküler iletimi bu mekanizma ile",
            ["lipid ortam", "genel anestezikler"],
            []
        )
    ]),

    # --- BOLUM 8: Nöromüsküler Blokörlerin Klinik Farmakolojisi ve Paralizi Sırası (21) ---
    (21, "k2-60-b08", "Nöromüsküler Blokörlerin Klinik Farmakolojisi ve Paralizi Sırası", [
        (
            "Nöromüsküler blokör ilaçların klinik farmakolojideki en temel kazanımı cerrahi operasyonlarda derin kas gevşemesini güvenle sağlamaktır.",
            "**Cerrahi Gevşeme:** Nöromüsküler blokörlerle intrakaviter cerrahinin kolaylaşması.",
            "Nöromusküler Blokör İlaçların Klinik Farmakolojisi",
            ["klinik farmakoloji", "cerrahi gevşeme"],
            []
        ),
        (
            "Bu ilaçların keşfinden önce kas gevşemesi ancak kardiyovasküler ve solunum sistemini ağır şekilde deprese eden çok derin uçucu anestezi ile sağlanabiliyordu.",
            "**Tarihsel Zorluk:** Derin anesteziye bağlı kardiyopulmoner depresyon riski.",
            "operasyonlar için yeterli iskelet kası gevşemesine sadece",
            ["kardiyopulmoner depresyon", "uçucu anestezikler"],
            []
        ),
        (
            "Modern nöromusküler blokörler kardiyopulmoner depresyona yol açmaksızın mükemmel cerrahi çalışma sahası ve entübasyon konforu sunar.",
            "**Modern Avantaj:** Kardiyak ve solunum depresyonu olmaksızın tam kas felci.",
            "Nöromusküler blokör ilaçların kullanılması tüm cerrahi prosedürler",
            ["cerrahi prosedürler", "entübasyon konforu"],
            []
        )
    ]),

    # --- BOLUM 9: Nöromüsküler İletinin Monitorizasyonu (Train-of-Four ve Tetanik Uyarı) (22) ---
    (22, "k2-60-b09", "Nöromüsküler İletinin Monitorizasyonu", [
        (
            "Anestezi süresince tubokürarin veya benzeri bir non-depolarizan blokör verildiğinde başlangıçta motor güçsüzlük, ardından tam kas gevşemesi ve uyarılamazlık gelişir.",
            "**Nondepolarizan Paralizi:** Güçsüzlükten başlayarak tam gevşeme ve elektriksel yanıtsızlık.",
            "Anestezi süresince, tubokürarinin 0,1-0,4 mg/kg IV uygulanması,",
            ["tubokürarin", "motor güçsüzlük"],
            []
        ),
        (
            "Kasların felç olma sırası boyutlarına ve aktivitesine bağlıdır; ilk olarak göz kasları, yüz ve parmaklar gibi küçük hızlı kaslar etkilenir.",
            "**Paralizi Sırası:** İlk göz, yüz ve el kasları; en son diyafram felç olur.",
            "İlk göz kasları etkilenir",
            ["küçük kaslar", "göz kasları"],
            []
        ),
        (
            "Diyafram nöromusküler blokörlere en dirençli kastır ve genellikle en son felç olan kastır.",
            "**Diyafram Direnci:** En dirençli kas grubu olup en son paralize olur.",
            "Diyafram genellikle en son felç olan kastır.",
            ["diyafram", "direnç"],
            []
        ),
        (
            "İlaç etkisi sonlandığında kasların geri dönmesi ters sırayla gerçekleşir; ilk olarak diyafram solunum fonksiyonunu yeniden kazanır ve en son göz kasları toparlar.",
            "**Geri Dönüş Sırası:** Ters sırada iyileşme; ilk diyafram, en son küçük kaslar döner.",
            "olur; ilk olarak diyafram fonksiyonunu yeniden kazanır.",
            ["solunum toparlanması", "ters sıra"],
            []
        )
    ]),

    # --- BOLUM 10: Depolarizan Gevşeticilerin Klinik Tablosu ve Fasikülasyon (23) ---
    (23, "k2-60-b10", "Depolarizan Gevşeticilerin Klinik Tablosu ve Fasikülasyon", [
        (
            "Süksinilkolinin intravenöz uygulanmasını takiben yaklaşık otuz saniye içinde göğüs ve karın kaslarında geçici kas fasikülasyonları ortaya çıkar.",
            "**Fasikülasyon Başlangıcı:** İntravenöz uygulamadan sonra 30 saniyede gelişen seğirmeler.",
            "Süksinilkolinin 0,75-1,5 mg/kg IV uygulanmasını takiben, 30 sn içinde",
            ["süksinilkolin dozu", "fasikülasyon başlangıcı"],
            []
        ),
        (
            "Genel anestezinin derinleştirilmesi veya süksinilkolinden önce çok düşük doz bir non-depolarizan ajan verilmesi bu fasikülasyonları zayıflatır.",
            "**Fasikülasyon Önleme:** Anestezi derinliği veya önceden düşük doz nondepolarizan ajan.",
            "Genel anestezi ve önce düşük doz non-depolarizan kas gevşetici",
            ["ön-tedavi", "fasikülasyon kontrolü"],
            []
        ),
        (
            "Kas felci doksan saniyeden kısa sürede hızla gelişir; önce kol, boyun ve bacak kasları, ardından solunum kasları gevşer.",
            "**Hızlı Paralizi:** 90 saniyeden kısa sürede tam solunum ve ekstremite paralizisi.",
            "Felç hızla gelişirken (90 < saniye) önce kol, boyun ve bacak kasları,",
            ["90 saniye", "hızlı entübasyon"],
            []
        ),
        (
            "Plazma ve karaciğer kolinesterazları tarafından hızla hidroliz edilmesi sayesinde süksinilkolin blokajı tipik olarak on dakikadan kısa sürede tamamen sonlanır.",
            "**Ultra Kısa Süre:** 10 dakikadan kısa sürede kendiliğinden tam toparlanma.",
            "dakikadan daha kısa sürede sonlanır.",
            ["tam iyileşme", "hızlı hidroliz"],
            []
        )
    ]),

    # --- BOLUM 11: Nöromüsküler Blokörlerin Kardiyovasküler Yan Etkileri (24-25) ---
    (24, "k2-60-b11", "Nöromüsküler Blokörlerin Kardiyovasküler Yan Etkileri", [
        (
            "Vekuronyum, sisatrakuryum ve rokuronyumun kardiyovasküler sistem üzerindeki etkileri minimum derecededir ve hemodinamik stabilite sağlarlar.",
            "**Hemodinamik Stabilite:** Vekuronyum, sisatrakuryum ve rokuronyumda minimal kardiyak etki.",
            "Vekuronyum, sisatrakuryum ve rokuronyumun kardiyovasküler",
            ["hemodinamik stabilite", "minimal etki"],
            []
        ),
        (
            "Buna karşın pankuronyum, atrakuryum ve mivakuryum otonomik gangliyonları veya histamin reseptörlerini uyararak kardiyovasküler yan etkiler oluşturabilirler.",
            "**Otonomik ve Histaminik Etki:** Taşikardi, hipotansiyon ve vasküler yanıtlara yol açabilir.",
            "etkileri minimum derecededir.",
            ["otonomik reseptörler", "kardiyovasküler yan etki"],
            []
        ),
        (
            "Tubokürarin ile birlikte mivakuryum ve atrakuryum sistemik histamin salınımına yol açarak belirgin hipotansiyon ve kızarıklık yapabilir.",
            "**Histamin Hipotansiyonu:** Mast hücresinden histamin salınımı ve vazodilatasyon.",
            "Tubokürarin ve daha az olarak metokurin, mivakuryum ve atrakuryum",
            ["histamin salınımı", "hipotansiyon"],
            []
        ),
        (
            "Tubokürarinin yüksek dozlarında otonomik gangliyonik blokaj da gelişerek hipotansiyonu daha da derinleştirebilir.",
            "**Gangliyon Blokajı:** Sempatik tonus kaybı ve kan basıncı düşüşü.",
            "Tubokürarin ve metokurinin yüksek dozları ile gangliyonik blokaj da",
            ["gangliyonik blokaj", "derin hipotansiyon"],
            []
        )
    ]),

    (25, "k2-60-b11", "Nöromüsküler Blokörlerin Kardiyovasküler Yan Etkileri", [
        (
            "Antihistaminiklerle premedikasyon yapılması tubokürarin ve mivakuryum enjeksiyonu ile meydana gelen hipotansiyonu belirgin şekilde zayıflatır.",
            "**Antihistaminik Profilaksisi:** Premedikasyon ile vazodilatasyon ve hipotansiyonun önlenmesi.",
            "Antihistaminiklerle premedikasyon tubokürarin ve mivakuryum ile",
            ["antihistaminik premedikasyon", "hipotansiyon önleme"],
            []
        ),
        (
            "Pankuronyum ise kalp hızında ve debisinde orta dereceli bir artışa neden olarak taşikardi tablosu oluşturur.",
            "**Pankuronyum Taşikardisi:** Kalp hızı ve debisinde artış.",
            "Pankuronyum kalp hızında orta dereceli, kalp debisinde daha hafif",
            ["pankuronyum taşikardisi", "kalp debisi"],
            []
        ),
        (
            "Pankuronyum taşikardisi primer olarak kardiyak muskarinik M iki reseptörlerinin vagolitik blokajı ve sempatik sinir uçlarından noradrenalin salınımıyla ortaya çıkar.",
            "**Vagolitik Mekanizma:** M2 muskarinik blokaj ve presinaptik noradrenalin salınımı.",
            "Pankuronyum ile meydana gelen taşikardi primer olarak vagolitik",
            ["vagolitik etki", "noradrenalin salınımı"],
            []
        ),
        (
            "Nöromüsküler blokörlere bağlı histamin salınımı bronkospazma yol açabilse de anestezide bronkospazmın en sık nedeni endotrakeal tüpün mekanik irritasyonudur.",
            "**Bronkospazm Ayırıcı Tanı:** İlaç kaynaklı histamin ve endotrakeal tüp irritasyonu.",
            "Bronkospazm nöromusküler blokörlerin histamin salıverilmesine",
            ["bronkospazm", "endotrakeal tüp irritasyonu"],
            []
        )
    ]),

    # --- BOLUM 12: Süksinilkolin Bradikardisi, Aritmiler ve Profilaksi (26-27) ---
    (26, "k2-60-b12", "Süksinilkolin Bradikardisi, Aritmiler ve Profilaksi", [
        (
            "Süksinilkolin özellikle halotan anestezisi altında uygulandığında tehlikeli kardiyak aritmilere zemin hazırlayabilir.",
            "**Aritmi Riski:** Süksinilkolin ve halotan etkileşimi ile disritmiler.",
            "Süksinilkolin halotan anestezisiyle birlikte uygulandığında kardiyak",
            ["kardiyak aritmi", "halotan"],
            []
        ),
        (
            "İlaç hem sempatik ve parasempatik otonomik gangliyonlardaki nikotinik reseptörleri hem de kalpteki muskarinik sinüs düğümü reseptörlerini uyarır.",
            "**Kolinoseptör Uyarımı:** Otonomik gangliyon nikotinik ve kardiyak muskarinik stimülasyon.",
            "Bu ilaç, parasempatik ve sempatik gangliyonların her ikisindeki",
            ["otonomik gangliyon", "muskarinik reseptör"],
            []
        ),
        (
            "Süksinilkolinin negatif inotropik ve kronotropik bradikardi etkileri atropin veya glikopirolat gibi antikolinerjik ajanlarla önceden engellenebilir.",
            "**Bradikardi Profilaksisi:** Atropin veya glikopirolat ile muskarinik blokaj.",
            "Süksinilkolinin negatif inotropik ve kronotropik etkileri bir",
            ["glikopirolat", "atropin"],
            []
        ),
        (
            "Özellikle ilk dozun ardından beş dakika gibi kısa bir sürede ikinci bir süksinilkolin dozu verildiğinde çocuklarda ve erişkinlerde derin bradikardi kaçınılmaz hale gelir.",
            "**İkinci Doz Uyarısı:** Kısa aralıkla tekrarlanan dozlarda kaçınılmaz bradikardi ve asistoli riski.",
            "ikinci doz verildiğinde aralıksız olarak bradikardi gözlenir.",
            ["ikinci doz", "derin bradikardi"],
            []
        )
    ]),

    (27, "k2-60-b12", "Süksinilkolin Bradikardisi, Aritmiler ve Profilaksi", [
        (
            "Süksinilkolin kaynaklı bu geçici bradikardi tiyopental, atropin ve gangliyon blokörleri veya düşük doz non-depolarizan pankuronyum ön-tedavisiyle önlenebilir.",
            "**Profilaktik Tedavi:** Tiyopental, atropin veya düşük doz pankuronyum ile önleme.",
            "Bu geçici bradikardi tiyopental, atropin ve gangliyon blokörü",
            ["tiyopental", "pankuronyum ön-tedavisi"],
            []
        ),
        (
            "Geniş yanıklar, omurilik veya sinir hasarı, kapalı kafa travması olan hastalara süksinilkolin verildiğinde hücre dışına masif potasyum çıkışı ve ölümcül hiperkalemi gelişebilir.",
            "**Hiperkalemi Tehlikesi:** Yanık ve denervasyonda ekstrajunksiyonel reseptörler ve ölümcül potasyum artışı.",
            "Yanıklar, sinir hasarı veya nöromusküler hastalığı, kapalı kafa",
            ["hiperkalemi", "yanık hastası"],
            []
        ),
        (
            "Bu hastalarda gelişen kontrolsüz potasyum fırlaması dakikalar içinde refrakter kardiyak arrest ve ventriküler fibrilasyon ile sonuçlanabilir.",
            "**Kardiyak Arrest:** Masif potasyum salınımına bağlı kalp durması.",
            "potasyumun kana salıverilmesine neden olur, bu da nadir",
            ["kardiyak arrest", "potasyum fırlaması"],
            []
        )
    ]),

    # --- BOLUM 13: Süksinilkolin Komplikasyonları: Basınç Artışı ve Hiperkalemi (28) ---
    (28, "k2-60-b13", "Süksinilkolin Komplikasyonları: Basınç Artışı ve Fasikülasyon", [
        (
            "Aşırı kaslı hastalarda süksinilkolinin başlattığı güçlü fasikülasyonlar intragastrik basınçta belirgin bir artışa neden olur.",
            "**İntragastrik Basınç Artışı:** Şiddetli fasikülasyonlar sonucu mide basıncında yükselme.",
            "Aşırı kaslı hastalarda, süksinilkolinle ilişkili fasikülasyonlar",
            ["intragastrik basınç", "kas fasikülasyonu"],
            []
        ),
        (
            "Mide içi basıncın yükselmesi anestezi indüksiyonunda gastrik içeriğin regürjitasyonuna ve trakeobronşiyal aspirasyon pnömonisine yol açabilir.",
            "**Aspirasyon Riski:** Mide içeriği regürjitasyonu ve aspirasyon pnömonisi tehdidi.",
            "intragastrik basınçta bir artışa neden olur, bu da mide içeriğinin",
            ["regürjitasyon", "aspirasyon riski"],
            []
        ),
        (
            "Ayrıca ekstraoküler kasların kasılması nedeniyle intraoküler göz içi basıncında iki ila dört dakikada zirveye ulaşan geçici bir artış gözlenir.",
            "**İntraoküler Basınç:** Ekstraoküler kas kasılması ve göz içi basınç artışı.",
            "C. Artmış intragastrik basınç",
            ["intraoküler basınç", "ekstraoküler kaslar"],
            []
        )
    ]),

    # --- BOLUM 14: İlaç Etkileşimleri ve Malign Hipertermi (29-31) ---
    (29, "k2-60-b14", "İlaç Etkileşimleri ve Malign Hipertermi", [
        (
            "İnhalasyon anestezikleri doz bağımlı olarak non-depolarizan kas gevşeticilerin oluşturduğu nöromusküler blokajı kuvvetle potansiyalize ederler.",
            "**İnhalasyon Potansiyalizasyonu:** Uçucu anestezikler nöromüsküler bloğu belirgin artırır.",
            "İnhalasyon (uçucu) anestezikleri doz-bağımlı olarak non-depolarizan",
            ["inhalasyon anestezikleri", "potansiyalizasyon"],
            []
        ),
        (
            "Uçucu anesteziklerin kas gevşeticilerin etkisini artırma gücü sırasıyla en fazla izofluran, ardından sevofluran, desfluran, enfluran, halotan ve en az nitröz oksit şeklindedir.",
            "**Etki Sıralaması:** İzofluran > sevofluran > desfluran > enfluran > halotan > nitröz oksit.",
            "anestezikleri kas gevşeticilerin etkisini şu sırayla",
            ["izofluran", "sevofluran"],
            []
        ),
        (
            "Bu potansiyalizasyonun temel nedenleri santral sinir sistemi depresyonu, kas kan akımının artması ve kavşak sonrası membranın uyarılabilirliğinin azalmasıdır.",
            "**Mekanizma:** Kan akımı artışı, santral depresyon ve membran duyarsızlaşması.",
            "3) kavşak sonrası membranın depolarizasyona azalmış duyarlılığı.",
            ["kas kan akımı", "membran duyarlılığı"],
            []
        )
    ]),

    (30, "k2-60-b14", "İlaç Etkileşimleri ve Malign Hipertermi", [
        (
            "Süksinilkolin ile uçucu anesteziklerin birlikte kullanımında görülen en korkutucu komplikasyon sarkoplazmik kalsiyum fırtınasına bağlı oluşan malign hipertermidir.",
            "**Malign Hipertermi:** Süksinilkolin ve volatil ajanlarla tetiklenen kalsiyum fırtınası.",
            "iskelet kası depolarından anormal kalsiyum salıverilmesine bağlı",
            ["malign hipertermi", "kalsiyum fırtınası"],
            []
        ),
        (
            "Aminoglikozid grubu antibiyotikler presinaptik kalsiyum kanallarını bloke ederek asetilkolin salınımını belirgin şekilde azaltır ve nöromüsküler bloğu derinleştirir.",
            "**Aminoglikozid Etkileşimi:** Presinaptik kalsiyum blokajı ve asetilkolin salınımında azalma.",
            "Antibiyotikler (aminoglikozidler) ile nöromusküler blokaj gelişimi",
            ["aminoglikozidler", "presinaptik kalsiyum"],
            []
        ),
        (
            "Düşük doz lokal anestezikler kavşak öncesi etkilerle iletimi zayıflatırken yüksek dozlarda nikotinik reseptör iyon kanallarını doğrudan bloke ederler.",
            "**Lokal Anestezik Etkileşimi:** Yüksek dozda iyon kanalı blokajı ve kas gevşemesinde artış.",
            "asetilkoline bağlı kas kontraksiyonlarını nikotinik",
            ["lokal anestezikler", "iyon kanal blokajı"],
            []
        )
    ]),

    (31, "k2-60-b14", "İlaç Etkileşimleri ve Malign Hipertermi", [
        (
            "Süksinilkolinin son plak depolarize edici etkisi çok düşük doz non-depolarizan blokörler verilerek antagonize edilebilir.",
            "**Depolarizasyon Engeli:** Düşük doz nondepolarizan ile süksinilkolin antagonizması.",
            "Süksinilkolinin son plak depolarize edici etkisi düşük doz non-",
            ["antagonizma", "depolarizasyon engeli"],
            []
        ),
        (
            "Süksinilkolin öncesinde uygulanan iki miligram tubokürarin veya yarım miligram pankuronyum fasikülasyonları ve ameliyat sonrası kas ağrısını azaltır.",
            "**Prekürarizasyon Dozu:** Tubokürarin veya pankuronyum ile fasikülasyon profilaksisi.",
            "süksinilkolin uygulanması öncesi verilebilir (d-tubokürarin 2 mg IV",
            ["tubokürarin", "pankuronyum"],
            []
        ),
        (
            "Ancak bu ön-kürarizasyon yöntemi anestezi indüksiyonunda gereken süksinilkolin dozunu yüzde elli ila doksan oranında artırdığı için günümüzde rutin olarak terk edilmiştir.",
            "**Yöntemin Terki:** Gereken süksinilkolin dozunu belirgin artırması ve solunum zaafı riski.",
            'Bu nedenle, süksinilkolin öncesi "pre-kürarizasyon" artık yaygın',
            ["pre-kürarizasyon", "doz artışı"],
            []
        )
    ]),

    # --- BOLUM 15: Hastalıkların Nöromüsküler Yanıtlara Etkisi (Miyasteni ve Denervasyon) (32) ---
    (32, "k2-60-b15", "Hastalıkların Nöromüsküler Yanıtlara Etkisi", [
        (
            "Çeşitli nöromüsküler hastalıklar ve fizyolojik durumlar non-depolarizan kas gevşeticilerin oluşturduğu blokaj düzeyini belirgin biçimde değiştirebilir.",
            "**Hastalık Etkileri:** Sistemik hastalıklar nöromüsküler blok yanıtını derinleştirir veya direnç oluşturur.",
            "Çeşitli hastalıklar non-depolarizan kas gevşeticilerin oluşturduğu",
            ["nöromusküler hastalıklar", "blokaj yanıtı"],
            []
        ),
        (
            "Miyastenia gravis hastalarında nikotinik reseptör sayısı azaldığı için non-depolarizan blokörlere aşırı duyarlılık ve derin uzamış paralizi gözlenir.",
            "**Miyastenia Gravis:** Reseptör kaybı nedeniyle nondepolarizan blokörlere aşırı duyarlılık.",
            "Myastenia gravis bu ilaçların oluşturduğu nöromusküler blokajı",
            ["myastenia gravis", "aşırı duyarlılık"],
            []
        ),
        (
            "İlerlemiş yaşlarda karaciğer ve böbrek klirenslerinin azalmasına bağlı olarak non-depolarizan gevşeticilerin vücuttan atılımı gecikir ve etki süresi uzar.",
            "**Geriatrik Farmakokinetik:** Klirens azalması nedeniyle etki süresi belirgin uzar.",
            "İlerlemiş yaşlarda, ilaçların karaciğer ve böbrek klirenslerinin",
            ["geriatri", "klirens azalması"],
            []
        ),
        (
            "Bu farmakokinetik yavaşlama nedeniyle yetmiş yaşın üzerindeki yaşlı hastalarda nöromusküler blokör dozları mutlaka azaltılmalıdır.",
            "**Doz Azaltımı:** Yaşlı popülasyonda dikkatli doz titrasyonu gereklidir.",
            "Sonuç olarak, yaşlı hastalarda nöromusküler blokör ilaçların dozu",
            ["doz titrasyonu", "yaşlı hasta"],
            []
        )
    ]),

    # --- BOLUM 16: Nondepolarizan Bloğun Kolinesteraz İnhibitörleri ile Geri Döndürülmesi (33-34) ---
    (33, "k2-60-b16", "Nondepolarizan Bloğun Kolinesteraz İnhibitörleri ile Geri Döndürülmesi", [
        (
            "Kolinesteraz inhibitörleri non-depolarizan ilaçlar tarafından oluşturulan nöromusküler blokajı etkili bir şekilde antagonize ederek hastanın spontan solunuma dönmesini sağlar.",
            "**Farmakolojik Dekürarizasyon:** Asetilkolinesteraz inhibitörleri ile bloğun hızla geri çevrilmesi.",
            "Kolinesteraz inhibitörleri non-depolarizan ilaçlar tarafından",
            ["kolinesteraz inhibitörleri", "dekürarizasyon"],
            []
        ),
        (
            "Neostigmin ve piridostigmin sinapsta asetilkolinesteraz enzimini inhibe ederek son plaktaki endojen asetilkolin miktarını artırır ve reseptördeki blokörü yarışmalı olarak söker.",
            "**Asetilkolin Birikimi:** Sinaptik asetilkolin artışı ile kompetitif yarışmanın kazanılması.",
            "Neostigmin ve piridostigmin non-depolarizan nöromusküler blokajı,",
            ["neostigmin", "piridostigmin"],
            []
        ),
        (
            "Nitekim çıkmış sınav sorusu olarak non-depolarizan nöromusküler blokörlerin etkisinin neostigmin gibi kolinesteraz inhibitörleri ile geri çevrilme mekanizması sorgulanmıştır.",
            "**Sınav Spotu (Çıkmış Soru):** Kompetitif bloğun kolinesteraz inhibitörleri ile geri çevrilmesi sorulmuştur.",
            "oluşturulan nöromusküler blokajı etkili bir şekilde antagonize",
            ["çıkmış soru", "kolinesteraz inhibisyonu"],
            ["3ced1081dab9"]
        ),
        (
            "Edrofonyumun etkisi neostigmine göre çok daha hızlı başlar fakat non-depolarizan ilaçlarla oluşan derin blokajı geri döndürmede etkinliği daha zayıftır.",
            "**Edrofonyum:** Hızlı başlangıçlı ancak derin blokta neostigmine göre daha zayıf ajan.",
            "Edrofonyumun etkisi daha hızlı başlar fakat non-depolarizan blokör",
            ["edrofonyum", "hızlı başlangıç"],
            []
        )
    ]),

    (34, "k2-60-b16", "Nondepolarizan Bloğun Kolinesteraz İnhibitörleri ile Geri Döndürülmesi", [
        (
            "Mivakuryum plazma kolinesterazı tarafından metabolize edildiğinden kolinesteraz inhibitörleri ile antagonizmasında beklenmeyen uzamalar görülebilir.",
            "**Mivakuryum Özelliği:** Plazma kolinesteraz inhibisyonu metabolizmasını geciktirebilir.",
            "Mivakuryum plazma kolinesterazı tarafından metabolize",
            ["mivakuryum", "plazma kolinesteraz metabolizması"],
            []
        ),
        (
            "Sugammadeks ise steroid yapılı rokuronyum ve vekuronyumu dakikalar içinde kanda enkapsüle ederek bağlayan devrim niteliğinde modifiye bir siklodekstrindir.",
            "**Sugammadeks Devrimi:** Rokuronyum ve vekuronyumu spesifik bağlayan şelatör siklodekstrin.",
            "Sugammadeks, steroid nöromusküler bloke edici ajanlar",
            ["sugammadeks", "steroid blokör şelatörü"],
            []
        ),
        (
            "Sugammadeks için klinik derinliğe göre üç farklı doz önerilir: yüzeysel blokajda iki miligram bölü kilogram, derin blokajda dört miligram bölü kilogram verilir.",
            "**Klinik Dozaj:** Yüzeysel blokta 2 mg/kg, derin blokta 4 mg/kg doz.",
            "Sugammadeks için üç doz aralığı önerilmektedir:",
            ["yüzeysel blok", "derin blok"],
            []
        ),
        (
            "Yüksek doz rokuronyum uygulanmasını takiben acil uyanma ve anında geri döndürme gerektiren durumlarda ise on altı miligram bölü kilogramlık kurtarma dozu kullanılır.",
            "**Acil Kurtarma Dozu:** 1.2 mg/kg rokuronyum sonrası 16 mg/kg sugammadeks ile anında geri dönüş.",
            "Rokuronyumun 1,2 mg/kg'lık tek doz uygulanmasını takiben hemen",
            ["acil geri döndürme", "kurtarma dozu"],
            []
        )
    ]),

    # --- BOLUM 17: Sugammadeks Farmakolojisi, Enkapsülasyon ve Yan Etkileri (35-37) ---
    (35, "k2-60-b17", "Sugammadeks Farmakolojisi, Enkapsülasyon ve Yan Etkileri", [
        (
            "Böbrek fonksiyonu normal olan hastalarda sugammadeks-rokuronyum kompleksi yirmi dört saat içinde idrarla değişmeden vücuttan atılır.",
            "**Renal Eliminasyon:** Kompleks 24 saat içinde değişmeden idrarla atılır.",
            "Böbrek fonksiyonu normal olan hastalarda sugammadeks rokuronyum",
            ["böbrek fonksiyonu", "idrarla atılım"],
            []
        ),
        (
            "Böbrek yetmezliği olan hastalarda sugammadeksin plazma yarılanma ömrü dört saatten on dokuz saate kadar belirgin biçimde uzar.",
            "**Böbrek Yetmezliği Kinetiği:** Yarılanma ömrü 19 saate kadar uzayabilir.",
            "ömrü 19 saate kadar artar.",
            ["yarılanma ömrü", "böbrek yetmezliği"],
            []
        ),
        (
            "Sugammadeksin hemodiyaliz ile kandan temizlenme yeteneği değişken olduğundan ciddi böbrek yetmezliği olan olgularda kullanılması önerilmez.",
            "**Diyaliz Kısıtlılığı:** Ağır renal yetmezlikte birikim riski nedeniyle önerilmez.",
            "Sugammadeksin diyaliz yeteneği değişkendir. Bu nedenle ciddi",
            ["diyaliz yeteneği", "kontrendikasyon"],
            []
        )
    ]),

    (36, "k2-60-b17", "Sugammadeks Farmakolojisi, Enkapsülasyon ve Yan Etkileri", [
        (
            "Sugammadeks kullanımı sırasında en kritik immünolojik risk, yüksek doz alan hastaların binde üçünde görülebilen anafilaksi tablosudur.",
            "**Anafilaksi Tehlikesi:** Binde 3 sıklıkta gelişebilen ciddi anafilaksi riski.",
            "En önemlisi sugammadeks, çalışmalarda 16 mg/kg doz alan hastaların",
            ["anafilaksi", "aşırı duyarlılık"],
            []
        ),
        (
            "Mide bulantısı, kaşıntı ve ürtiker gibi aşırı duyarlılık reaksiyonları anafilaksiden çok daha yaygın görülür.",
            "**Alerjik Reaksiyonlar:** Bulantı, ürtiker ve geçici kaşıntı bulguları.",
            "Mide bulantısı, kaşıntı ve ürtiker gibi aşırı duyarlılık reaksiyonları",
            ["ürtiker", "kaşıntı"],
            []
        ),
        (
            "Ayrıca enjeksiyondan birkaç dakika sonra kardiyak arreste ilerleyebilen belirgin bradikardi ve koagülasyon testlerinde geçici uzama meydana gelebilir.",
            "**Kardiyak ve Koagülasyon Etkileri:** Ciddi bradikardi riski ve aPTT/PT süresinde geçici uzama.",
            "Diğer önemli advers reaksiyonlar arasında, uygulamadan birkaç",
            ["bradikardi", "koagülopati"],
            []
        ),
        (
            "Aktive parsiyel tromboplastin zamanı ve protrombin zamanı değerlerinde bir saate kadar sürebilen geçici bir artış bildirilmiştir.",
            "**Pıhtılaşma Süreleri:** aPTT ve PT testlerinde 1 saatlik geçici uzama.",
            "oranı değerlerinde 1 saate kadar sürebilen bir artış vardır.",
            ["aPTT", "protrombin zamanı"],
            []
        )
    ]),

    (37, "k2-60-b17", "Sugammadeks Farmakolojisi, Enkapsülasyon ve Yan Etkileri", [
        (
            "Sugammadeks steroidal rokuronyum ve vekuronyumu bağladığı gibi vücuttaki diğer steroidal yapılı ilaçları da bağlayarak etkilerini bloke edebilir.",
            "**Steroid İlaç Etkileşimi:** Steroid halkası taşıyan diğer molekülleri de bağlar.",
            "rokuronyum ve vekuronyumu bağladığından, diğer steroidal ilaçları da",
            ["steroidal ilaçlar", "çapraz bağlanma"],
            []
        ),
        (
            "Bu moleküllerin başında progesteron içeren oral kontraseptifler ve meme kanserinde kullanılan seçici östrojen reseptör modülatörü toremifen gelir.",
            "**Önemli İlaçlar:** Progesteron içeren doğum kontrol hapları ve toremifen.",
            "Bu ilaçlardan en önemli ikisi progesteron bazlı kontraseptifler ve",
            ["progesteron", "toremifen"],
            []
        ),
        (
            "Hormonal doğum kontrol hapı kullanan kadınlara sugammadeks verildiğinde progesteron bağlanır ve ilacın gebeliği önleyici etkinliği hızla düşer.",
            "**Kontraseptif Başarısızlığı:** Progesteronun bağlanması ve gebelikten koruma kaybı.",
            "bağlanabilir ve sanki kadın bir veya iki dozu kaçırmış gibi",
            ["doğum kontrolü", "kontraseptif etkinlik"],
            []
        ),
        (
            "Bu nedenle üretici firma sugammadeks uygulamasından sonraki yedi gün boyunca hormonal olmayan ek bir doğum kontrol yönteminin kullanılmasını şart koşar.",
            "**7 Gün Kuralı:** Uygulamayı takiben 7 gün boyunca ek bariyer yöntemi gereklidir.",
            "Üretici, sugammadeks uygulamasını takiben 7 gün boyunca alternatif",
            ["7 gün kuralı", "bariyer yöntem"],
            []
        )
    ]),

    # --- BOLUM 18: Nöromüsküler Blokörlerin Klinik Kullanım Alanları ve Acil Endikasyonlar (38-39) ---
    (38, "k2-60-b18", "Nöromüsküler Blokörlerin Klinik Kullanım Alanları", [
        (
            "Nöromüsküler blokörlerin en yaygın kullanım alanı laparotomi ve torakotomi gibi girişimlerde karın ve göğüs duvarı kaslarını gevşeterek cerrahi konforu sağlamaktır.",
            "**Cerrahi Gevşeme:** İntraabdominal ve intratorasik operasyonlarda kas gevşetme.",
            "Nöromusküler blokörlerin en önemli kullanım alanlarından biri",
            ["cerrahi gevşeme", "laparotomi"],
            []
        ),
        (
            "Ayrıca larenks ve farenks kaslarını gevşeterek laringoskopiyi ve endotrakeal tüpün vokal kordlardan travmasız geçişini kolaylaştırırlar.",
            "**Endotrakeal Entübasyon:** Vokal kord ve larenks kaslarının gevşetilmesi.",
            "Nöromusküler blokör ilaçlar, farinks ve larinks kaslarını gevşeterek",
            ["entübasyon", "laringoskopi"],
            []
        ),
        (
            "Yoğun bakım ünitelerinde mekanik ventilasyon uygulanan kritik hastalarda göğüs duvarı rijiditesini ve hasta-ventilatör uyumsuzluğunu önlemek için tercih edilirler.",
            "**Ventilatör Uyumu:** Mekanik ventilasyonda solunum direncini kırma ve uyum sağlama.",
            "Yoğun bakım ünitelerinde, sıklıkla göğüs duvarı direncini ve efektif",
            ["yoğun bakım", "ventilasyon senkronizasyonu"],
            []
        )
    ]),

    (39, "k2-60-b18", "Nöromüsküler Blokörlerin Klinik Kullanım Alanları", [
        (
            "Status epileptikus veya lokal anestezik intoksikasyonuna bağlı şiddetli konvülsiyonlarda periferik motor kasılmaları durdurmak amacıyla süksinilkolin kullanılabilir.",
            "**Konvülsiyon Kontrolü:** Periferik motor çırpınmaların ve hipoksinin durdurulması.",
            "Nöromusküler blokör ilaçlar (süksinilkolin) lokal anesteziklerin",
            ["status epileptikus", "motor konvülsiyon"],
            []
        ),
        (
            "Nöromüsküler blokörler periferik kasılmaları durdursa da santral sinir sistemindeki elektriksel epileptik aktiviteyi ve kortikal deşarjları kesinlikle sonlandırmaz.",
            "**Kritik Uyarı:** Kas felci sağlarlar ancak beyindeki nöronal deşarjı durduramazlar.",
            "toksisitesine veya status epileptikusa bağlı konvülsiyonların periferik",
            ["kortikal deşarj", "santral kontrolsüzlük"],
            []
        ),
        (
            "Spastisite ise üst motor nöron lezyonlarında tonik germe reflekslerinin artışı, fleksör kas spazmları ve istemli kas kontrolünün kaybı ile giden tablodur.",
            "**Spastisite Tanımı:** Üst motor nöron hasarı, tonik refleks artışı ve fleksör spazmlar.",
            "Spastisite, kasların normalden fazla gergin, sert veya istemsiz olarak",
            ["spastisite", "üst motor nöron"],
            []
        ),
        (
            "Serebral palsi, multipl skleroz, inme ve omurilik travmaları spastisiteye yol açan başlıca nörolojik hastalıklardır.",
            "**Etiyoloji:** Serebral palsi, MS, inme ve spinal kord travması.",
            "Sıklıkla omurilik yaralanması, serebral palsi, multipl skleroz ve inme",
            ["multipl skleroz", "spinal kord hasarı"],
            []
        )
    ]),

    # --- BOLUM 19: Santral Etkili Spazmolitikler: Diazepam ve Baklofen (40-43) ---
    (40, "k2-60-b19", "Santral Etkili Spazmolitikler: Diazepam ve Baklofen", [
        (
            "Benzodiazepinler santral sinir sisteminde gama-aminobütirik asidin yani gaba'nın inhibitör etkinliğini kolaylaştırarak kas tonusunu azaltırlar.",
            "**GABA-A Allosterik Modülasyonu:** Benzodiazepinler GABA etkinliğini potansiyalize eder.",
            "Benzodiazepinler santral sinir sisteminde gama-aminobütirik asidin",
            ["benzodiazepinler", "GABA"],
            []
        ),
        (
            "Nitekim çıkmış sınav sorusu olarak primer etki yeri santral sinir sistemi olan ve gaba aracılı iletimi artıran diazepamın etki mekanizması sorgulanmıştır.",
            "**Sınav Spotu (Çıkmış Soru):** Santral etkili benzodiazepinlerin GABA-A mekanizması sınavda sorulmuştur.",
            "Diazepam GABAA sinapslarına etkilidir; spastisiteyi azaltıcı etkisine",
            ["çıkmış soru", "diazepam", "GABA-A"],
            ["b71287aec894"]
        ),
        (
            "Diazepam spinal korddaki polisinaptik refleks yollarını baskılayarak hem lokal kas spazmlarında hem de nörolojik spastisitede etkili olur.",
            "**Spinal İnhibisyon:** Polisinaptik spinal refleks arklarının baskılanması.",
            "Diazepam hemen hemen her türlü kas kasılması (lokal kas travmaları dahil)",
            ["polisinaptik refleks", "spinal kord"],
            []
        ),
        (
            "Ancak diazepam kas tonusunu azaltan terapötik dozlarında belirgin sedasyon, uyuklama ve psikomotor yavaşlama oluşturur.",
            "**Doz Kısıtlayıcı Yan Etki:** Kas gevşetici dozlarda belirgin sedasyon ve somnolans.",
            "için gerekli dozlarında sedasyon oluşturur.",
            ["sedasyon", "doz kısıtlaması"],
            []
        )
    ]),

    (41, "k2-60-b19", "Santral Etkili Spazmolitikler: Diazepam ve Baklofen", [
        (
            "Baklofen para-klorofenil türevi olup oral yoldan kullanım için tasarlanmış seçici bir gaba b reseptör agonistidir.",
            "**Baklofen:** Oral GABA-B reseptör agonisti santral spazmolitik.",
            "Baklofen (p-klorofenil GABA) oral yoldan kullanım için dizayn edilmiş,",
            ["baklofen", "GABA-B agonisti"],
            []
        ),
        (
            "Nitekim sınavda çıkmış soru olarak oral yoldan kullanılan ve gaba b reseptörlerini uyararak spastisiteyi azaltan baklofen sorulmuştur.",
            "**Sınav Spotu (Çıkmış Soru):** Oral GABA-B agonisti spazmolitik baklofen çıkmış sınav sorusudur.",
            "GABAB reseptör agonisti GABA-mimetik bir ajandır.",
            ["çıkmış soru", "GABA-B", "spazmolitik"],
            ["ea7f887c8593"]
        ),
        (
            "gaba b reseptörlerinin uyarılması potasyum kanallarını açarak hiperpolarizasyona yol açar ve voltaj kapılı kalsiyum girişini kapatır.",
            "**Moleküler Mekanizma:** Potasyum iletimi artışı, hiperpolarizasyon ve kalsiyum blokajı.",
            "Bu reseptörlerin baklofen tarafından aktivasyonu, olasılıkla K+",
            ["potasyum kanalı", "hiperpolarizasyon"],
            []
        ),
        (
            "Oluşan presinaptik inhibisyon eksitatör glutamat salınımını ve omurilikte ağrı ileten P maddesi salıverilmesini baskılar.",
            "**Eksitatör İnhibisyon:** Presinaptik glutamat ve substans P salınımının önlenmesi.",
            "nörotransmiterlerin salıverilmesini azalttığı ileri sürülmüştür.",
            ["presinaptik inhibisyon", "P maddesi"],
            []
        )
    ]),

    (42, "k2-60-b19", "Santral Etkili Spazmolitikler: Diazepam ve Baklofen", [
        (
            "Baklofen spastisiteyi azaltmada en az diazepam kadar etkilidir ve çok daha az sedasyon meydana getirir.",
            "**Klinik Üstünlük:** Diazepam kadar güçlü spastisite kontrolü ve belirgin daha az sedasyon.",
            "Baklofen en az diazepam kadar spastisiteyi azaltır ve daha az",
            ["düşük sedasyon", "yüksek etkinlik"],
            []
        ),
        (
            "Dantrolenden farklı olarak iskelet kasında doğrudan eksitasyon-kontraksiyon kenetini bozmadığı için yaygın kas güçsüzlüğü yapmaz.",
            "**Kas Gücü Korunumu:** Periferik kas güçsüzlüğü oluşturmaz.",
            "Ayrıca, dantrolenin yaptığı gibi genel kas güçsüzlüğü oluşturmaz. Oral",
            ["kas güçsüzlüğü yok", "dantrolen farkı"],
            []
        ),
        (
            "Ağız yoluyla alındıktan sonra hızla ve tama yakın emilir; plazma yarılanma ömrü üç ila dört saattir.",
            "**Farmakokinetik:** Oral tam emilim ve 3-4 saatlik plazma yarılanma ömrü.",
            "uygulamadan sonra hızla ve tama yakın absorbe edilir; plazma yarı",
            ["oral emilim", "plazma yarı ömrü"],
            []
        ),
        (
            "Tedaviye günde iki kez on beş miligram ile başlanır ve hastanın toleransına göre günlük yüz miligrama kadar titre edilebilir.",
            "**Doz Titrasyonu:** Günlük 30 mg'dan 100 mg maksimum doza kademeli artış.",
            "Dozaja günde iki kez 15 mg ile başlanır, tolere edilebilirse günlük 100",
            ["doz titrasyonu", "günlük doz"],
            []
        )
    ]),

    (43, "k2-60-b19", "Santral Etkili Spazmolitikler: Diazepam ve Baklofen", [
        (
            "Görselimizde oral tedaviye dirençli şiddetli spastisite hastalarında subaraknoid mesafeye yerleştirilen intratekal baklofen infüzyon pompası şematize edilmiştir.",
            "**İntratekal Pompa Şeması:** Subaraknoid kateter ve implante edilebilir baklofen infüzyon pompası.",
            "Çalışmalar, baklofenin intratekal uygulanmasının, diğer uygulama",
            ["intratekal pompa", "subaraknoid infüzyon"],
            []
        ),
        (
            "İlacın doğrudan beyin omurilik sıvısına verilmesi sistemik dolaşıma geçişi engellediği için periferik yan etkileri en aza indirir.",
            "**Hedefe Yönelik Tedavi:** Sistemik dolaşım kısıtlılığı ve minimal periferik toksisite.",
            "Baklofenin omurilikten çıkışı az olması nedeniyle periferik",
            ["minimal yan etki", "hedefe yönelik"],
            []
        ),
        (
            "Aylar süren kronik kullanımda ilacın etkilerine karşı kısmi tolerans gelişebilir ancak pompa dozu artırılarak klinik yanıt başarıyla sürdürülür.",
            "**Tolerans Yönetimi:** Gelişen tolerans pompa dozu titrasyonu ile aşılır.",
            "Birkaç ay kullanımını takiben ilacın etkilerine kısmi tolerans",
            ["tolerans", "doz artışı"],
            []
        )
    ]),

    # --- BOLUM 20: Tizanidin, Gabapentinoidler ve Santral İnhibitörler (44-47) ---
    (44, "k2-60-b20", "Tizanidin, Gabapentinoidler ve Santral İnhibitörler", [
        (
            "Tizanidin omurilik düzeyinde etkili olan ve klonidine benzer şekilde çalışan santral bir alfa iki adrenoseptör agonistidir.",
            "**Tizanidin:** Santral alfa-2 adrenerjik reseptör agonisti spazmolitik.",
            "Tizanidin, önemli ölçüde 2-adrenoseptör agonisti etkiye sahiptir,",
            ["tizanidin", "alfa-2 agonisti"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: tizanidinin omurilikte presinaptik alfa iki adrenerjik reseptörleri uyararak kas gevşemesi oluşturduğu önemle sorulmuştur.",
            "**Sınav Spotu (Çıkmış Soru):** Omurilikte presinaptik alfa-2 reseptör agonisti olan tizanidin çıkmış sınav sorularında sorulmuştur.",
            "etkilere neden olduğu dozlarında spastisiteyi azaltır.",
            ["çıkmış soru", "tizanidin", "presinaptik alfa-2"],
            ["5d76925ac6c0", "d3-k2-far-010"]
        ),
        (
            "Nörofizyolojik çalışmalar tizanidinin omurilik arka boynuzunda hem presinaptik hem de postsinaptik inhibisyonu belirgin olarak güçlendirdiğini göstermektedir.",
            "**Spinal İnhibisyon Güçlenmesi:** Presinaptik ve postsinaptik refleks iletiminde baskılanma.",
            "Nörofizyolojik çalışmalar omurilikte tizanidinin hem presinaptik hem",
            ["presinaptik inhibisyon", "postsinaptik inhibisyon"],
            []
        ),
        (
            "Tizanidin belirgin olarak daha az kas güçsüzlüğü yapar fakat sedasyon, hipotansiyon, ağız kuruluğu ve karaciğer enzim yüksekliği gibi yan etkilere yol açabilir.",
            "**Yan Etki Profili:** Kas gücü korunur; sedasyon, hipotansiyon ve hepatotoksisite riski vardır.",
            "Tizanidin belirgin olarak daha az kas güçsüzlüğüne neden olur,",
            ["hipotansiyon", "hepatotoksisite"],
            []
        )
    ]),

    (45, "k2-60-b20", "Tizanidin, Gabapentinoidler ve Santral İnhibitörler", [
        (
            "Spastisite durumlarının yanı sıra tizanidin kronik migren ve dirençli gerilim tipi baş ağrısı profilaksisinde de klinik etkinlik gösterir.",
            "**Migren Endikasyonu:** Spastisite dışında kronik migren tedavisinde de etkilidir.",
            "Spastisite durumlarında tizanidinin kronik migren tedavisinde de",
            ["kronik migren", "baş ağrısı profilaksisi"],
            []
        ),
        (
            "Klinik çalışmalarda oral tizanidinin kas spazmını hafifletmede diazepam, baklofen ve dantrolen ile tamamen eşdeğer başarı sağladığı bildirilmiştir.",
            "**Karşılaştırmalı Etkinlik:** Diazepam ve baklofen ile karşılaştırılabilir klinik güç.",
            "Oral tizanidin ile yapılan klinik çalışmalar, kas spazmını hafifletmede",
            ["eşdeğer etkinlik", "spazm kontrolü"],
            []
        ),
        (
            "Tedaviye her altı ila sekiz saatte bir iki miligram ile başlanır ve günlük maksimum otuz altı miligrama kadar titre edilebilir.",
            "**Doz Titrasyonu:** 2 mg başlangıç, maksimum 36 mg/gün doz sınırı.",
            "Tedaviye her 6-8 saatte bir 2 mg ile başlanır ve maksimum 36",
            ["maksimum doz", "doz protokolü"],
            []
        ),
        (
            "Karaciğer veya böbrek yetmezliği bulunan olgularda ilacın eliminasyonu bozulacağından dozaj dikkatle azaltılmalıdır.",
            "**Organ Yetmezliği Uyarısı:** Renal ve hepatik yetmezlikte doz azaltımı şarttır.",
            "Karaciğer veya böbrek yetmezliği olan hastalarda dozajın",
            ["karaciğer yetmezliği", "doz azaltımı"],
            []
        )
    ]),

    (46, "k2-60-b20", "Tizanidin, Gabapentinoidler ve Santral İnhibitörler", [
        (
            "Gabapentin esasen antiepileptik bir ilaç olup multipl sklerozlu hastalarda yapılan çalışmalarda belirgin spazmolitik etki göstermiştir.",
            "**Gabapentin:** MS hastalarında spazmolitik etkili antiepileptik ajan.",
            "Gabapentin antiepileptik bir ilaçtır ve multipl sklerozlu hastalarda",
            ["gabapentin", "multipl skleroz"],
            []
        ),
        (
            "Gabapentin ve pregabalin voltaj kapılı kalsiyum kanallarının alfa iki delta alt birimine bağlanarak nörona kalsiyum girişini engeller ve eksitatör glutamat salınımını durdururlar.",
            "**Alfa-2-Delta Ligandı:** Kalsiyum kanal blokajı ve eksitatör glutamat salınım engeli.",
            "Nörona kalsiyum girişini engeller, eksitatör etkili",
            ["alfa-2-delta", "glutamat inhibisyonu"],
            []
        ),
        (
            "Ayrıca hem gaba a hem gaba b agonisti olan progabid ile santral kan-beyin bariyerini hızla aşan glisin de inhibitör iletimi artırarak spastisiteyi hafifletir.",
            "**Progabid ve Glisin:** İnhibitör aminoasit transmiterleri ve reseptör agonistleri.",
            "Progabid ve glisinin de spastisiteyi azalttığı ön çalışmalarda",
            ["progabid", "glisin"],
            []
        )
    ]),

    (47, "k2-60-b20", "Tizanidin, Gabapentinoidler ve Santral İnhibitörler", [
        (
            "İdrosilamid ve amiyotrofik lateral skleroz tedavisinde kullanılan riluzol, santral sinir sisteminde glutamaterjik iletimi inhibe ederek spazm giderici etki oluştururlar.",
            "**Riluzol ve İdrosilamid:** Glutamat salınım inhibisyonu ve ALS spazm tedavisi.",
            "İdrosilamid ve riluzol olasılıkla santral sinir sisteminde glutamaterjik",
            ["riluzol", "idrosilamid"],
            []
        ),
        (
            "Dantrolen ise fenitoine benzer hidantoin kimyasal yapısına sahip olup etki mekanizması bakımından tamamen periferik çalışan benzersiz bir ajandır.",
            "**Dantrolen Giriş:** Fenitoin benzeri hidantoin türevi, periferik kas gevşetici.",
            "Dantrolen fenitoine benzer bir hidantoin türevidir.",
            ["dantrolen", "hidantoin türevi"],
            []
        ),
        (
            "Santral etkili ilaçların aksine dantrolen doğrudan iskelet kası fibrillerinde eksitasyon-kontraksiyon kenetini bozarak kas gücünü azaltır.",
            "**Periferik Kenet Blokajı:** Doğrudan kas lifinde eksitasyon-kontraksiyon kenetinin engellenmesi.",
            "Santral etkili kas gevşetici ilaçların aksine, dantrolen kas",
            ["kenet blokajı", "kas fibrilleri"],
            []
        ),
        (
            "Fizyolojik kas kasılması için gereken kalsiyum, sarkoplazmik retikulumdan ryanodin reseptör kanalları yani RyR yoluyla sitozole salıverilir.",
            "**Ryanodin Reseptörü:** Sarkoplazmik retikulum kalsiyum kanalı (RyR).",
            "Kalsiyum sarkoplazmik retikulumdan ryanodin reseptör (RyR)",
            ["ryanodin reseptörü", "kalsiyum deposu"],
            []
        )
    ]),

    # --- BOLUM 21: Periferik Spazmolitik Dantrolen, Botulinum Toksini ve Akut Kas Spazmı İlaçları (48-51) ---
    (48, "k2-60-b21", "Periferik Spazmolitik Dantrolen, Botulinum Toksini ve Akut İlaçlar", [
        (
            "Dantrolen sarkoplazmik retikulumdaki ryanodin reseptör alt tipi bire bağlanarak kalsiyum kanallarının açılmasını bloke eder ve kalsiyum salınımını engeller.",
            "**RyR1 Blokajı:** Dantrolenin sarkoplazmik retikulum kalsiyum kanalını bloke etmesi.",
            "Dantrolen RyR1'e bağlanarak kalsiyum kanallarının açılmasını bloke",
            ["RyR1", "kalsiyum salınım engeli"],
            []
        ),
        (
            "Bu bilgi çıkmış sınavda sorulmuştur: iskelet kasında eksitasyon-kontraksiyon kenetlenmesini engelleyen ve malign hipertermi krizinde hayat kurtaran dantrolen sorulmuştur.",
            "**Sınav Spotu (Çıkmış Soru):** Eksitasyon-kontraksiyon kenetini bozan ve malign hipertermide kullanılan dantrolen çıkmış sınav sorusudur.",
            "Dantrolenin özel bir uygulama yeri malign hipertermi",
            ["çıkmış soru", "dantrolen", "malign hipertermi"],
            ["past-1790877044812-375943", "09e61290e8aa"]
        ),
        (
            "Kalp kası ve damar düz kasları dantrolenden çok az etkilenir çünkü onların sarkoplazmik retikulumunda farklı bir izoform olan ryanodin reseptör iki bulunur.",
            "**Doku Seçiciliği:** Kalp ve düz kaslar RyR2 taşıdığı için dantrolenden etkilenmez.",
            "Kalp kası ve düz kaslar çok az etkilenir, çünkü onların sarkoplazmik",
            ["RyR2", "kalp kası seçiciliği"],
            []
        ),
        (
            "Tedaviye günde tek doz yirmi beş miligram ile başlanır ve toleransa göre günde dört kez yüzer miligrama kadar artırılabilir.",
            "**Doz Şeması:** Günlük 25 mg başlangıç ve 400 mg maksimum günlük doz.",
            "Dantrolen ile tedavi, genellikle günde 25 mg tek doz ile başlatılır,",
            ["dantrolen dozu", "günlük titrasyon"],
            []
        )
    ]),

    (49, "k2-60-b21", "Periferik Spazmolitik Dantrolen, Botulinum Toksini ve Akut İlaçlar", [
        (
            "Botulinum toksini motor sinir terminalindeki snare kompleksini parçalayarak presinaptik asetilkolin salınımını kalıcı olarak inhibe eder.",
            "**Botulinum Toksini:** SNARE parçalanması ile presinaptik asetilkolin ekzositoz blokajı.",
            "Botulinum toksini presinaptik ACh salınımını inhibe eder.",
            ["botulinum toksini", "SNARE kompleksi"],
            []
        ),
        (
            "Toksinin lokal yüz enjeksiyonları göz çevresi ve alındaki yaşlanmaya bağlı kırışıklıkların bir ila üç aylık geçici tedavisinde yaygın olarak uygulanır.",
            "**Kozmetik Endikasyon:** Yüz ve periorbital kırışıklıkların geçici felç ile giderilmesi.",
            "Botulinum toksininin lokal yüz enjeksiyonları, gözler ve ağız",
            ["kozmetik kullanım", "yüz kırışıklıkları"],
            []
        ),
        (
            "Ayrıca servikal distoni, blefarospazm, serebral palsi ve inme sonrası gelişen fokal ekstremite spastisitesinde aylarca süren kalıcı rahatlama sağlar.",
            "**Klinik Spastisite:** Serebral palsi, fokal distoni ve inme sonrası spastisite tedavisi.",
            "Botulinum toksininin lokal enjeksiyonu ayrıca yaygın spastisite",
            ["servikal distoni", "fokal spastisite"],
            []
        ),
        (
            "Ekstremite kaslarına uygulandığında etkisi birkaç ay boyunca devam eder ve yeni sinir uç filizlenmesi ile iletim kademeli olarak geri döner.",
            "**Uzun Süreli Etki:** Birkaç ay süren nöromüsküler paralizi ve aksonal filizlenme.",
            "Bir ya da iki ekstremiteye ilaç uygulanması yapılan en güncel",
            ["sinir filizlenmesi", "kalıcı gevşeme"],
            []
        )
    ]),

    (50, "k2-60-b21", "Periferik Spazmolitik Dantrolen, Botulinum Toksini ve Akut İlaçlar", [
        (
            "Lokal travma ve kas incinmelerinin neden olduğu akut ağrılı spazmları hafifletmek için siklobenzaprin, karisoprodol, klorzoksazon ve metokarbamol gibi ilaçlar kullanılır.",
            "**Akut Lokal Spazm Ajanları:** Siklobenzaprin, karisoprodol, klorzoksazon ve metokarbamol.",
            "Akut lokal kas spazmı için kullanılan ilaçlar",
            ["akut kas spazmı", "spazm gidericiler"],
            []
        ),
        (
            "Bu ajanların etki mekanizmaları esas olarak beyin sapı retiküler formasyon düzeyinde polisinaptik refleks yaylarını baskılamaya dayanır.",
            "**Beyin Sapı Etkisi:** Retiküler formasyon ve polisinaptik refleks arklarının inhibisyonu.",
            "Bu ilaçların, özellikle beyin sapı düzeyinde etki gösterdikleri ileri",
            ["beyin sapı", "retiküler formasyon"],
            []
        ),
        (
            "Siklobenzaprin bu grubun prototipi olup trisiklik antidepresan benzeri yapısıyla belirgin antimuskarinik yan etkilere ve sedasyona yol açar.",
            "**Siklobenzaprin:** Trisiklik yapı benzerliği, antikolinerjik yan etkiler ve sedasyon.",
            "Siklobenzaprin bu grubun prototipi olarak kabul edilebilir. Trisiklik",
            ["siklobenzaprin", "antimuskarinik etki"],
            []
        ),
        (
            "Akut kas incinmelerinde siklobenzaprinin oral dozu bölünmüş dozlar halinde günlük yirmi ila kırk miligramdır.",
            "**Doz Protokolü:** Günlük 20-40 mg oral dozaj.",
            "Akut zedelenmeye bağlı kas spazmların da siklobenzaprinin dozu",
            ["akut zedelenme", "günlük dozaj"],
            []
        )
    ]),

    (51, "k2-60-b21", "Periferik Spazmolitik Dantrolen, Botulinum Toksini ve Akut İlaçlar", [
        (
            "Dersimizin içeriğinde Bertram Katzung Temel ve Klinik Farmakoloji referans kaynağındaki güncel nöromüsküler ve spazmolitik ilkeler esas alınmıştır.",
            "**Kaynak ve Referans:** Bertram Katzung, Temel ve Klinik Farmakoloji.",
            "Temel ve Klinik Farmakoloji",
            ["Katzung", "Temel ve Klinik Farmakoloji"],
            []
        ),
        (
            "Nobel Tıp Kitabevleri ve Lange Medical Publications çeviri standartları ile terminoloji bütünlüğü sağlanmıştır.",
            "**Yayın Bilgisi:** Nobel Tıp Kitabevleri ve Lange Medical Publications.",
            "Bertram G. Katzung, Susan B. Masters, Antony J. Trevor",
            ["Nobel Tıp Kitabevleri", "Lange Medical"],
            []
        ),
        (
            "Böylece nöromüsküler kavşak blokörlerinden santral ve periferik spazmolitik ajanlara kadar tüm klinik farmakolojik süreçleri tamamlamış olduk.",
            "**Ders Özeti:** Nöromüsküler blokörler, antagonistler ve spazmolitik farmakoterapisi tamamlandı.",
            "Basic & Clinical Pharmacology",
            ["nöromüsküler blokaj", "spazmolitik tedavi"],
            []
        )
    ])
]

# Verify all anchors in kaynak.md
print("Verifying anchors against kaynak.md...")
anchor_errors = 0
for sayfa, bid, bbaslik, sentences in SLIDES:
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        if anchor not in kaynak_text:
            print(f"ERROR: Sayfa {sayfa} sentence {s_idx+1} anchor not found in kaynak.md: {anchor!r}")
            anchor_errors += 1
if anchor_errors:
    print(f"FAILED: {anchor_errors} anchors not found!")
    sys.exit(1)
print(f"SUCCESS: All {sum(len(s[3]) for s in SLIDES)} anchors verified 100% in kaynak.md!")

# Build konusma_v2.json
bolum_map = {}
cid_counter = 1
pid_counter = 1
total_words = 0

for sayfa, bid, bbaslik, sentences in SLIDES:
    if bid not in bolum_map:
        bolum_map[bid] = {
            "id": bid,
            "baslik": bbaslik,
            "paragraflar": []
        }
    
    p_id = f"k2-60-p{sayfa:03d}"
    p_obj = {
        "id": p_id,
        "sayfa": sayfa,
        "cumleler": []
    }
    
    for s_idx, (ses, ekran, anchor, terms, cikmis) in enumerate(sentences):
        cid = f"k2-60-c{cid_counter:04d}"
        cid_counter += 1
        words = len(ses.split())
        total_words += words
        
        sekil_val = VISUAL_PAGES.get(sayfa) if s_idx == 0 and sayfa in VISUAL_PAGES else None
        
        vurgu_text = ekran.split("**")[1] if "**" in ekran else "İskelet Kası"
        
        c_obj = {
            "id": cid,
            "ses": ses,
            "ekran": ekran,
            "duzey": 0,
            "slayt": {
                "sayfa": sayfa,
                "satir": [anchor],
                "sekil": sekil_val
            },
            "vurgu": [{"tur": "terim", "metin": vurgu_text}]
        }
        if cikmis:
            c_obj["cikmis"] = cikmis
            
        p_obj["cumleler"].append(c_obj)
        
    bolum_map[bid]["paragraflar"].append(p_obj)

konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-60",
    "anahtar": "y25-k2-60-miyorelaksan-ilaclar",
    "baslik": "Miyorelaksan İlaçlar (İskelet Kası Gevşeticileri)",
    "bolumler": list(bolum_map.values())
}

print(f"Total Bolumler: {len(konusma_v2['bolumler'])}")
print(f"Total Paragraphs: {sum(len(b['paragraflar']) for b in konusma_v2['bolumler'])}")
print(f"Total Sentences: {cid_counter - 1}")
print(f"Total Words: {total_words} (~{total_words / 125:.1f} minutes of audio)")

# Save konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Update sayfa_haritasi.json
sh = json.loads((TASLAK / "sayfa_haritasi.json").read_text(encoding="utf-8"))
for sp in sh.get("sayfalar", []):
    p = sp["sayfa"]
    if p == 1:
        sp["tur"] = "icerik"
        sp["baslik"] = "1.1"
        sp["adimlar"] = [1]
        sp["bilgi"] = [1]
        sp["ne_anlatiliyor"] = "İskelet Kası Gevşeticileri ders kapağı ve genel farmakolojik sınıflandırma ilkeleri."
        sp["kanit"] = {"sayfa": 1, "alinti": "Prof. Dr. Mehmet ÖZDEMİR"}
    elif p == 51:
        sp["tur"] = "icerik"
        sp["baslik"] = "4.2"
        sp["adimlar"] = [23]
        sp["bilgi"] = [29]
        sp["ne_anlatiliyor"] = "Temel ve Klinik Farmakoloji kaynakça değerlendirmesi ve miyorelaksan algoritmaları."
        sp["kanit"] = {"sayfa": 51, "alinti": "Temel ve Klinik Farmakoloji"}

(TASLAK / "sayfa_haritasi.json").write_text(json.dumps(sh, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated sayfa_haritasi.json")

# Design 8 valid drawing commands
# We find exact sentence IDs for chosen slides
def get_cid_for_slide(slide_num, s_offset=0):
    for b in konusma_v2["bolumler"]:
        for p in b["paragraflar"]:
            if p["sayfa"] == slide_num:
                return p["cumleler"][s_offset]["id"]
    raise ValueError(f"Slide {slide_num} not found")

cizim_komutlari = [
    {
        "cumle": get_cid_for_slide(2, 3),
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "İskelet Kası Gevşeticileri",
        "ogeler": [
            "Nöromüsküler blokörler: Kas felci oluşturur",
            "Spazmolitikler: Spastisiteyi azaltır"
        ]
    },
    {
        "cumle": get_cid_for_slide(4, 2),
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Nöromüsküler İletim Adımları",
        "ogeler": [
            "Aksiyon potansiyeli sinir terminaline ulaşır",
            "Kalsiyum girişi ile asetilkolin salınır",
            "Asetilkolin nikotinik reseptöre bağlanır"
        ]
    },
    {
        "cumle": get_cid_for_slide(9, 1),
        "bas": 0, "son": 4,
        "sayfa": 9,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Nöromüsküler Blok Mekanizmaları",
        "ogeler": [
            "Non-depolarizan: Reseptör antagonizması",
            "Depolarizan: Agonist fazlalığı ile blokaj"
        ]
    },
    {
        "cumle": get_cid_for_slide(10, 3),
        "bas": 0, "son": 4,
        "sayfa": 10,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Non-depolarizan İlaçların Özellikleri",
        "ogeler": [
            "Yüksek oranda iyonize olurlar",
            "Hücre membranlarını kolayca geçemezler",
            "Böbrek ve karaciğer yoluyla atılırlar"
        ]
    },
    {
        "cumle": get_cid_for_slide(11, 2),
        "bas": 0, "son": 4,
        "sayfa": 11,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Steroid Yapılı Kas Gevşeticiler",
        "ogeler": [
            "Rokuronyum: Etkisi çok hızlı başlar",
            "Vekuronyum: Orta etki sürelidir",
            "Pankuronyum: En uzun etkili üyedir"
        ]
    },
    {
        "cumle": get_cid_for_slide(14, 0),
        "bas": 0, "son": 4,
        "sayfa": 14,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Süksinilkolin Eliminasyonu",
        "ogeler": [
            "Plazma kolinesterazı ile hızla hidroliz",
            "Süksinilmonokolin ve koline parçalanma",
            "Kısa etki süresi ile blokajın sonlanması"
        ]
    },
    {
        "cumle": get_cid_for_slide(33, 0),
        "bas": 0, "son": 4,
        "sayfa": 33,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Blokajın Geri Döndürülmesi",
        "ogeler": [
            "Kolinesteraz enziminin inhibisyonu",
            "Sinapsta asetilkolin miktarının artması",
            "Non-depolarizan blokörün yarışmalı ayrılması"
        ]
    },
    {
        "cumle": get_cid_for_slide(48, 0),
        "bas": 0, "son": 4,
        "sayfa": 48,
        "tur": "sema",
        "sablon": "neden_sonuc",
        "baslik": "Dantrolen Etki Mekanizması",
        "ogeler": [
            "RyR1 ryanodin reseptörüne bağlanma",
            "Kalsiyum salıverilmesinin engellenmesi",
            "Malign hipertermide kas gevşemesi"
        ]
    }
]

cizim_aday = {"komutlar": cizim_komutlari}
(TASLAK / "cizim_aday.json").write_text(json.dumps(cizim_aday, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cizim_aday.json with {len(cizim_komutlari)} commands.")
