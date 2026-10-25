#!/usr/bin/env python3
"""Generate a complete, deep amfi-level lecture for Lesson 55: Panik Bozukluk ve Fobik Bozukluklar.

Covers all 38 pages without skipping any page or bullet point.
Generates ~180-220 sentences, ~3,500-4,200 spoken words (~28-33 minutes of deep amfi audio).
Includes all 5 verbal past exam citations and 12-15 verified drawing commands.
Strictly adheres to Turkish style standard and zero forward leak rule.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-55-panik-bozukluk"
KAYNAK_MD = TASLAK / "kaynak.md"

kaynak_txt = KAYNAK_MD.read_text(encoding="utf-8")

# Parse pages and non-empty lines from kaynak.md
pages_lines = {}
for p in re.split(r'=== SAYFA (\d+) ===', kaynak_txt)[1:]:
    if p.isdigit():
        curr_p = int(p)
    else:
        ll = []
        for line in p.strip().splitlines():
            cl = line.strip(' ✓\t').strip()
            cl = re.sub(r'^[✓\s\-*•o❑➢]+', '', cl).strip()
            if len(cl) > 3 and not cl.isdigit() and not cl.startswith('==='):
                ll.append(cl)
        pages_lines[curr_p] = ll

def find_satir(pno, pattern=None, idx=0):
    lines = pages_lines.get(pno, [])
    if not lines:
        return "Panik Bozukluk ve Fobik Bozukluklar"
    if pattern:
        for l in lines:
            if pattern.casefold() in l.casefold():
                return l
    if idx < len(lines):
        return lines[idx]
    return lines[-1]

c_counter = 1

def make_sentence(ekran, ses, pno, satir_pattern=None, satir_idx=0, cikmis=None, highlight_word=None, sekil=None):
    global c_counter
    cid = f"k2-55-c{c_counter:04d}"
    c_counter += 1
    
    satir = find_satir(pno, satir_pattern, satir_idx)
    clean_ekran = ekran.replace("**", "").replace("*", "")
    
    vurgular = []
    if cikmis and highlight_word:
        m = re.search(re.escape(highlight_word), clean_ekran, re.IGNORECASE)
        if m:
            vurgular.append({"tur": "cikmis", "metin": m.group(0)})
        else:
            vurgular.append({"tur": "cikmis", "metin": clean_ekran[:30]})
    elif highlight_word:
        m = re.search(re.escape(highlight_word), clean_ekran, re.IGNORECASE)
        if m:
            vurgular.append({"tur": "terim", "metin": m.group(0)})
        else:
            first_w = clean_ekran.split(":")[0] if ":" in clean_ekran else clean_ekran.split()[0]
            vurgular.append({"tur": "terim", "metin": first_w})
    else:
        bolds = re.findall(r'\*\*([^*]+)\*\*', ekran)
        if bolds:
            vurgular.append({"tur": "terim", "metin": bolds[0]})
        else:
            first_w = clean_ekran.split(":")[0] if ":" in clean_ekran else clean_ekran.split()[0]
            vurgular.append({"tur": "terim", "metin": first_w})
            
    c_obj = {
        "id": cid,
        "ses": ses,
        "ekran": ekran,
        "duzey": 1 if cikmis else 0,
        "slayt": {
            "sayfa": pno,
            "satir": [satir],
            "sekil": sekil
        },
        "vurgu": vurgular
    }
    if cikmis:
        c_obj["cikmis"] = [cikmis] if isinstance(cikmis, str) else list(cikmis)
    return c_obj

PD = {}

# ==============================================================================
# BÖLÜM 1: Panik Atak ve Panik Bozukluk Kavramı (Sayfa 1 - 4)
# ==============================================================================

PD[1] = [
    ("**Panik Bozukluk ve Fobik Bozukluklar:** Giriş ve klinik kapsam.",
     "Ruh sağlığı ve hastalıkları anabilim dalı klinik dersimiz kapsamında panik bozukluk, agorafobi, özgül fobiler ve sosyal kaygı bozukluğunu tüm klinik, tanısal ve sağaltım yönleriyle ele alacağız.",
     "PANİK BOZUKLUK", 0, None, "Panik Bozukluk", None),
    ("Dersimiz Doktor Öğretim Üyesi **Zuhal Koç Apaydın** tarafından tıp fakültesi amfi kurulu için hazırlanmıştır.",
     "Dersimiz Karabük Üniversitesi Tıp Fakültesi Ruh Sağlığı ve Hastalıkları Anabilim Dalından Doktor Öğretim Üyesi Zuhal Koç Apaydın tarafından hazırlanmıştır.",
     "Zuhal KOÇ APAYDIN", 1, None, "Zuhal Koç Apaydın", None),
    ("Anksiyete bozukluklarının ayırıcı tanısında **otonomik belirtiler** ile bilişsel çarpıtmaları doğru ayrıştırmak esastır.",
     "Genel hekimlik pratiğinde ve acil servislerde anksiyete bozukluklarının ayırıcı tanısını yaparken otonomik belirtiler ile bilişsel çarpıtmaları doğru ayrıştırmak hastaya yaklaşımın temelini oluşturur.",
     "Ruh Sağlığı", 2, None, "otonomik belirtiler", None)
]

PD[2] = [
    ("**Panik Atak:** Aniden başlayan ve dakikalar içinde şiddetlenen yoğun korku ve sıkıntı nöbetidir.",
     "Panik atak aniden başlayan ve dakikalar içinde hızla şiddetlenen, çoğu zaman şiddetli bir tehlike hissi veya öleceği hissinin eşlik ettiği yoğun korku ya da sıkıntı nöbetidir.",
     "PANİK ATAK", 1, None, "yoğun korku ve sıkıntı", None),
    ("Panik atağının **belli bir başlangıcı** ve dakikalar içinde sönen belirgin bir bitişi bulunur.",
     "Panik atağının dakikalarla sınırlı belirgin bir başlangıcı, kısa sürede ulaştığı bir doruk noktası ve yatışma evresi bulunur.",
     "belli bir başlangıcı", 2, None, "başlangıcı ve bitişi", None),
    ("Klinik pratikte önemle vurgulanan bir kural olarak: **Panik atak tek başına** bir psikiyatrik hastalık veya tanı değildir!",
     "Klinik pratikte önemle vurgulanan bir kural olarak: Panik atak tek başına bir psikiyatrik hastalık veya nozolojik tanı değildir, pek çok ruhsal bozuklukta ve tıbbi tabloda görülebilen bir klinik semptomdur.",
     "tanı değildir", 3, None, "tek başına tanı değildir", None),
    ("Panik ataklar depresyonda, travma sonrası stres bozukluğunda veya **genel tıbbi durumlarda** da tetiklenebilir.",
     "Nitekim panik ataklar majör depresyonda, travma sonrası stres bozukluğunda, madde kullanımında veya hipertiroidi gibi genel tıbbi durumlarda da karşımıza çıkabilmektedir.",
     "sıkıntı nöbetidir", 3, None, "genel tıbbi durumlarda", None)
]

PD[3] = [
    ("Bu bilgi çıkmış sınavda sorulmuştur: **Panik Bozukluk**, beklenmedik anlarda gelen ve yineleyen panik nöbetleri ile karakterizedir.",
     "Bu bilgi çıkmış sınavda sorulmuştur: Panik bozukluk beklenmedik anlarda kendiliğinden gelen, yineleyici panik atakları ve bu atakların doğurduğu kronik kaygılar ile karakterize bağımsız bir anksiyete bozukluğudur.",
     "Beklenmeden gelen", 1, "d3-k2-psi-015", "Panik Bozukluk", None),
    ("Hasta kriz sırasında **kontrolünü kaybedeceği**, çıldıracağı ya da kalp krizi geçireceği korkusuna kapılır.",
     "Hasta nöbet anında kalp krizi geçirip öleceği, felç kalacağı, kontrolünü tamamen kaybedeceği ya da aklını yitirip çıldıracağı yönünde derin ve katastrofik bir dehşet yaşar.",
     "kalp krizi geçireceği", 2, None, "kontrolünü kaybedeceği", None),
    ("Ataklar sonrasında hastada sürekli bir **beklenti anksiyetesi** yerleşir.",
     "Panik atağı yaşayan bireyde ataklar geçtikten sonra dahi her an yeni bir atağın geleceğine ilişkin kesintisiz ve yıpratıcı bir beklenti anksiyetesi gelişir.",
     "sürekli endişe", 3, None, "beklenti anksiyetesi", None),
    ("Kişi panik atak geçirebileceği ortamlardan kaçınarak belirgin **davranış değişiklikleri** sergiler.",
     "Kişi yeni bir panik atak geçirebileceğini veya yardım alamayacağını düşündüğü ortamlardan kaçınma şeklinde uyum bozucu davranış değişiklikleri göstermeye başlar.",
     "davranış değişiklikleri", 4, None, "kaçınma davranışı", None),
    ("Diğer anksiyete bozukluklarının aksine panik bozukluktaki nöbetler **kendiliğinden ve beklenmedik** biçimde patlak verir.",
     "Panik nöbetleri diğer fobik bozukluklarda belirli bir nesneyle karşılaşınca ortaya çıkarken, panik bozuklukta nöbetler hiçbir dış uyaran yokken tamamen beklenmedik biçimde patlak verir.",
     "beklenmedik panik nöbetleri", 5, None, "beklenmedik nöbetler", None)
]

PD[4] = [
    ("Toplumda tek bir panik atak geçirme sıklığı **yılda yüzde on** civarındadır.",
     "Epidemiyolojik çalışmalara göre genel toplumda ömür boyu en az bir kez tekil panik atak geçirme sıklığı yılda yaklaşık yüzde on düzeyindedir.",
     "görülme sıklığı yılda %10", 1, None, "yılda yüzde on", None),
    ("Panik bozukluğun yaşam boyu prevalansı ise **yüzde bir buçuk ile beş** arasında değişir.",
     "Düzenli tanı kriterlerini dolduran panik bozukluğun yaşam boyu yaygınlığı ise genel popülasyonda yüzde bir buçuk ile beş arasında değişkenlik gösterir.",
     "prevelansı %1,5-5", 2, None, "yüzde bir buçuk ile beş", None),
    ("Kadınlarda bozukluğun görülme oranı erkeklere kıyasla **iki ila üç kat** daha fazladır.",
     "Cinsiyet dağılımına bakıldığında kadınlarda panik bozukluk görülme oranı erkeklere kıyasla iki ila üç kat daha yüksek olarak saptanmaktadır.",
     "2-3 kat  fazladır", 3, None, "iki ila üç kat", None),
    ("Hastalık çoğunlukla **yirmili yaşlarda** başlar ve hastaların yüzde sekseninde başlangıç otuz yaş öncesidir.",
     "Hastalık her yaşta gelişebilmekle birlikte tipik olarak yirmili yaşlarda başlar ve her on hastanın sekizinde ilk atak otuz yaşından önce ortaya çıkar.",
     "20’li yaşlarda başlar", 4, None, "yirmili yaşlar", None)
]

# ==============================================================================
# BÖLÜM 2: Panik Bozukluk Etiyolojisi ve Nörobiyolojisi (Sayfa 5 - 6)
# ==============================================================================

PD[5] = [
    ("**Biyolojik Kuramlar:** Merkezi sinir sisteminde katekolamin düzeylerinde belirgin artış izlenir.",
     "Panik bozukluğun biyolojik etiyolojisinde merkezi sinir sisteminde katekolamin düzeylerinde artış ve aşırı otonomik uyarılabilirlik temel faktördür.",
     "katekolamin düzeylerinde", 1, None, "katekolamin düzeylerinde artış", None),
    ("Beyin sapındaki **lokus seruleus** nükleusunda artmış noradrenerjik aktivite panik alarmını tetikler.",
     "Beyin sapında yer alan ve vücudun temel noradrenalin merkezi olan lokus seruleus nükleusundaki hiperaktivite ani panik alarmını başlatan en kritik nörobiyolojik odaktır.",
     "Locus seruleusta", 2, None, "lokus seruleus", None),
    ("Beyin sapı **kemoreseptörlerinin duyarlılığındaki artış** karbondioksit birikimini boğulma tehdidi olarak algılar.",
     "Klein tarafından öne sürülen boğulma yanlış alarmı teorisine göre beyin sapı kemoreseptörlerinin karbondioksite aşırı duyarlılığı panik atağını alevlendirir.",
     "kemoreseptörlerinin duyarlılığında", 3, None, "kemoreseptör duyarlılığı", None),
    ("GABA ve **benzodiazepin reseptör** kompleksindeki yetersizlik baskılayıcı mekanizmayı zayıflatır.",
     "Merkezi sinir sisteminin temel inhibitör sistemi olan gaba nörotransmitter sistemindeki ve benzodiazepin reseptörlerindeki düzensizlik hastanın anksiyeteyi kontrol etmesini engeller.",
     "GABA nörotransmitter", 4, None, "GABA düzensizliği", None),
    ("Genetik çalışmalarda panik bozukluğu olanların **birinci derece akrabalarında** risk dört ila sekiz kat artmıştır.",
     "Genetik geçiş incelendiğinde panik bozukluk hastalarının birinci derece akrabalarında bozukluğun ortaya çıkma riski genel topluma göre dört ila sekiz kat daha fazladır.",
     "Birinci derece yakınlarında", 5, None, "dört ila sekiz kat artış", None),
    ("Psikodinamik kurama göre kaygı uyandırıcı dürtülere karşı **savunma düzenekleri** yetersiz kalmaktadır.",
     "Psikososyal kuramlardan psikodinamik görüşe göre bilinçdışı kaygı uyandırıcı dürtülere karşı ego savunma mekanizmalarının başarısız kalması somatik panik patlamalarına yol açar.",
     "savunma", 7, None, "savunma mekanizmaları", None)
]

PD[6] = [
    ("**Bilişsel Davranışçı Model:** Bedensel duyumların felaketleştirici biçimde yanlış yorumlanmasıdır.",
     "Bilişsel davranışçı modele göre panik bozukluğun merkezinde içsel veya dışsal uyaranların oluşturduğu fizyolojik duyumların felaketleştirilerek yorumlanması yer alır.",
     "Bilişsel", 0, None, "Bilişsel Davranışçı Model", None),
    ("Hafif bir çarpıntı veya nefes darlığı gibi **tetikleyici duyumlar** zihinde bir tehdit olarak algılanır.",
     "Merdiven çıkma veya stres gibi durumlarda gelişen hafif bir taşikardi veya terleme gibi zararsız fizyolojik duyumlar hasta tarafından doğrudan bir ölüm tehdidi olarak kodlanır.",
     "Tetikleyici", 5, None, "tehdit algısı", None),
    ("Bu duyumların 'kalp krizi geçiriyorum' veya 'ölüyorum' şeklinde **katastrofize edilmesi** korkuyu tırmandırır.",
     "Bu duyumların kalp krizi geçiriyorum, beynime kan gitmiyor veya aklımı kaçırıyorum şeklinde katastrofize edilmesi yani felaketleştirilmesi sempatik sistemi daha da kamçılar.",
     "katastrofize", 4, None, "katastrofize edilmesi", None),
    ("Artan korku sempatik deşarjı büyüterek **kendi kendini besleyen** tam bir panik kısır döngüsü kurar.",
     "Tırmanan korku hissi lokus seruleusu ve böbrek üstü bezlerini daha fazla uyararak bedensel belirtileri katlar ve hasta kendi kendini besleyen bir panik döngüsüne hapsolur.",
     "Korku", 2, None, "panik kısır döngüsü", None)
]

# ==============================================================================
# BÖLÜM 3: Panik Atağın Semptomatolojisi ve DSM-5 Kriterleri (Sayfa 7 - 11)
# ==============================================================================

PD[7] = [
    ("**Kardinal Belirtiler 1-3:** Çarpıntı, kalp hızında artış, terleme ve titreme nöbeti görülür.",
     "Panik atağın ilk ve en sık somatik belirtisi çarpıntı, kalbin küt küt atması, nabzın fırlaması, bol soğuk terleme ve tüm gövdede kontrolsüz titreme veya sarsılmadır.",
     "çarpıntı", 1, None, "çarpıntı ve terleme", None),
    ("**Solunumsal Belirtiler 4-5:** Nefes darlığı, boğuluyor gibi olma ve hava açlığı hissi yaşanır.",
     "Solunum sisteminde hastanın soluğunun kesilmesi, havanın akciğerlerine yetmediği duygusu ve boğazında düğümlenmeyle boğuluyormuş gibi hissetmesi belirgindir.",
     "boğuluyor gibi olma", 4, None, "nefes darlığı ve boğulma", None),
    ("**Göğüs ve Karın Belirtileri 6-7:** Göğüs ağrısı, göğüste baskı, bulantı ve karın ağrısı eşlik eder.",
     "Göğüs kafesinde sol kola yayılan bir koroner ağrıyı andıran göğüs sıkışması hissi, midede kramp tarzı ağrılar ve kusacakmış gibi şiddetli bulantı tabloya eklenir.",
     "göğüste sıkıntı hissi", 6, None, "göğüs ağrısı ve baskı", None),
    ("**Santral Belirti 8:** Baş dönmesi, sersemlik hissi, ayakta duramama ve düşecekmiş gibi olmadır.",
     "Santral sinir sistemi perfüzyonundaki hiperventilasyona bağlı değişikliklerle baş dönmesi, sarhoşluk hissi, dengesizlik, sersemlik ve bayılacakmış gibi olma hissi ortaya çıkar.",
     "bayılacakmış gibi olma", 8, None, "baş dönmesi ve sersemlik", None)
]

PD[8] = [
    ("**Dissosiyatif Belirti 9:** Derealizasyon ya da depersonalizasyon yaşanır.",
     "Hastanın çevredeki nesneleri ve ortamı sanki bir rüyadaymış gibi gerçek dışı algılamasına derealizasyon, kendi bedenine ve ellerine yabancılaşmasına depersonalizasyon adı verilir.",
     "derealizasyon", 1, None, "derealizasyon ve depersonalizasyon", None),
    ("**Bilişsel Belirtiler 10-11:** Kontrolünü kaybedeceği, çıldıracağı ve öleceği korkusu yaşanır.",
     "Nöbet esnasında hastanın zihnini kaplayan en dehşet verici düşünce özdenetimini tümden yitirip çıldıracağı, delireceği ya da o an derhal öleceği korkusudur.",
     "çıldıracağı korkusu", 2, None, "çıldırma ve ölüm korkusu", None),
    ("**Duyusal Belirtiler 12-13:** Paresteziler, uyuşmalar, üşüme, ürperme veya ani ateş basmalarıdır.",
     "Ekstremitelerde, dudak çevresinde ve parmak uçlarında uyuşma ve karıncalanma şeklindeki paresteziler ile vücutta ürperme, donma veya alev alev ateş basması hisleri yaşanır.",
     "paresteziler", 4, None, "paresteziler ve uyuşma", None)
]

PD[9] = [
    ("**Genel Görünüm:** Panik nöbeti olmadığı zamanlarda hastanın genel muayenesinde belirgin bir fark yoktur.",
     "Panik bozukluğu olan hastaların nöbet dışı dönemlerde genel görünüm, davranış ve motor aktiviteleri tamamen normal sınırlardadır.",
     "Genel görünüm", 1, None, "genel görünüm normal", None),
    ("Ancak panik nöbetleri esnasında hasta **ileri derecede endişeli**, tedirgin ve telaşlıdır.",
     "Buna karşın panik nöbeti patladığı anda hasta dehşet içinde çırpınan, soluk soluğa kalmış, aşırı tedirgin ve telaşlı bir görünüm sergiler.",
     "ileri derecede endişeli", 2, None, "endişeli ve telaşlı", None),
    ("Konuşma ve ilişki kurma muayenesinde hastanın **sesi titrer** ve hekimle sağlıklı iletişim güçleşir.",
     "Nöbet anında hasta kesik kesik konuşur, soluksuz kalır, sesi titrer ve içinde bulunduğu ölüm korkusu nedeniyle hekimle sakin bir iletişim kurmak güçleşebilir.",
     "sesi titrer", 4, None, "konuşma ve ilişki güçlüğü", None),
    ("Bu bilgi çıkmış sınavda sorulmuştur: **Beklenti anksiyetesi** panik atağın bilişsel belirtileri arasında yer almaz!",
     "Bu bilgi çıkmış sınavda sorulmuştur: Panik atağın bilişsel kognitif belirtileri çıldırma, kontrolü kaybetme ve ölüm korkusudur; beklenti anksiyetesi ise ataklar arası dönemde süregiden duygulanımsal bir kaygıdır.",
     "Duygulanım", 5, "past-1790877044855-217832", "bilişsel belirtiler", None)
]

PD[10] = [
    ("**Bilişsel Yetiler:** Nöbetler dışında hastanın algılama, yönelim ve bellek işlevleri tamdır.",
     "Hastanın bilişsel yetileri değerlendirildiğinde yönelim, bellek, konsantrasyon ve soyutlama yetisi nöbetler haricinde tamamen korunmuştur.",
     "Bilişsel yetiler", 1, None, "bilişsel yetiler tam", None),
    ("Bu bilgi çıkmış sınavda sorulmuştur: Nöbet esnasında öze yabancılaşma yani **depersonalizasyon** ve gerçekdışılaşma yani **derealizasyon** gelişebilir.",
     "Bu bilgi çıkmış sınavda sorulmuştur: Panik nöbetleri esnasında öze yabancılaşma ve gerçekdışılaşma gibi geçici algı bozuklukları belirgindir ve atağın ardından sürekli beklenti kaygısı yaşanır.",
     "Öze yabancılaşma", 2, "q-KURUL_2_C_IKMIS__3-46", "depersonalizasyon", None),
    ("Düşünce içeriğinde sürekli nöbet tekrarlarsa kendisine **ne olacağı yönündeki kaygılar** yer alır.",
     "Hastanın düşünce içeriğini derinlemesine incelediğimizde zihninin tamamen bir sonraki nöbetin nerede geleceği ve bedenine ne zarar vereceği endişesiyle dolu olduğu saptanır.",
     "Düşünce süreci", 3, None, "düşünce içeriği", None),
    ("Bedensel belirtiler otonom sinir sisteminin sempatik kolunun **şiddetli kamçılanması** sonucudur.",
     "Tüm bu somatik ve viseral fırtına, otonom sinir sisteminin sempatik deşarjının aniden en yüksek seviyeye fırlamasının doğrudan bir sonucudur.",
     "kamçılanışına bağlı", 4, None, "sempatik deşarj", None)
]

PD[11] = [
    ("**DSM-5 Tanı Kriteri A:** Yineleyen, beklenmedik panik ataklarının varlığı zorunludur.",
     "Amerikan Psikiyatri Birliği de se me beş tanı sistemine göre birinci temel kriter, kendiliğinden başlayan yineleyen beklenmedik panik ataklarının varlığıdır.",
     "DSM-5 tanı kriterleri", 0, None, "yineleyen beklenmedik ataklar", None),
    ("Bir panik atağında dakikalar içinde doruğa çıkan **on üç belirtiden en az dördü** bulunmalıdır.",
     "Tanı konabilmesi için krizin dakikalar içinde doruk noktaya ulaşması ve sayılan on üç kardinal belirtiden en az dördünün ya da daha fazlasının tabloya eşlik etmesi şarttır.",
     "dördünün veya daha fazlasının", 2, None, "en az dört belirti", None),
    ("Kültüre özgü kulak çınlaması veya baş ağrısı gibi yakınmalar bu **dört belirtiden biri** sayılmaz.",
     "Kılavuzda önemle vurgulandığı üzere kulak çınlaması, ense ağrısı veya kontrolsüz ağlama gibi kültüre özgü semptomlar gereken dört temel belirti arasında sayılamaz.",
     "dört belirtiden biri sayılmamalıdır", 16, None, "kültüre özgü belirtiler", None),
    ("**DSM-5 Tanı Kriteri B:** Ataklardan sonra en az bir ay süren beklenti kaygısı veya uyum bozucu davranış gelişmelidir.",
     "İkinci tanı kriteri uyarınca atakların ardından en az bir ay ya da daha uzun süreyle başka atakların olacağına ilişkin sürekli bir kaygı duyulmalı veya uyum bozucu kaçınma davranışı sergilenmelidir.",
     "bir ay ya da daha uzun", 17, None, "en az bir ay süre", None),
    ("Amfi derslerimizde ve klinik sınavlarda sıkça vurgulanan bir kural olarak **beklenti kaygısı** atağın kendisinden farklıdır.",
     "Amfi derslerimizde ve klinik sınavlarda sıkça vurgulanan bir kural olarak beklenti kaygısı atağın kendisinden farklı olup iki nöbet arasındaki sürece yayılır.",
     "endişelenme", 18, None, "beklenti kaygısı", None),
    ("**Dışlama Ölçütü:** Bozukluk bir maddenin veya hipertiroidi gibi tıbbi durumun etkisine bağlanamaz.",
     "Son tanı ölçütlerine göre klinik tablo tiroit hormonu fazlalığı, feokromositoma veya madde kullanımı gibi organik bir duruma bağlanamamalı ve başka bir ruhsal hastalıkla daha iyi açıklanamamalıdır.",
     "bir maddenin", 20, None, "dışlama ölçütleri", None)
]

# ==============================================================================
# BÖLÜM 4: Ayırıcı Tanı, Gidiş ve Panik Bozukluk Tedavisi (Sayfa 12 - 15)
# ==============================================================================

PD[12] = [
    ("**Tıbbi Ayırıcı Tanı:** Endokrin bozukluklar, özellikle hipertiroidizm ve feokromositoma dışlanmalıdır.",
     "Panik bozukluğu tanısı koymadan önce benzer sempatik fırtına oluşturan hipertiroidizm, feokromositoma, hipoglisemi ve paratiroid hastalıkları laboratuvarla mutlaka ekarte edilmelidir.",
     "Hipertiroidizm", 2, None, "endokrin hastalıklar", None),
    ("Kardiyak hastalıklardan **paroksismal aritmiler** ve mitral kapak prolapsusu titizlikle taranmalıdır.",
     "Kardiyolojik açıdan paroksismal supraventriküler aritmiler, koroner yetersizlik ve özellikle genç kadınlarda mitral kapak prolapsusu ayırıcı tanıda ön planda incelenmelidir.",
     "Mitral kapak prolapsusu", 3, None, "kardiyak aritmiler", None),
    ("Alkol ve sedatif ilaçların **yoksunluk sendromları** ile kafein intoksikasyonu panik atağı kusursuz taklit eder.",
     "Alkol veya benzodiazepin kesilmesine bağlı yoksunluk sendromları ile aşırı kafein ya da amfetamin intoksikasyonları panik atağı kusursuz biçimde taklit edebilmektedir.",
     "Alkol,ilaç yoksunluk", 5, None, "madde yoksunluğu", None),
    ("Ruhsal hastalıklardan sosyal fobi, özgül fobi, travma sonrası stres bozukluğu ve **yaygın anksiyete** ayrılmalıdır.",
     "Ruhsal hastalıklar cephesinde ise sosyal fobi, özgül fobi, obsesif kompulsif bozukluk, travma sonrası stres bozukluğu ve yaygın anksiyete bozukluğu dikkatle ayrıştırılmalıdır.",
     "travma sonrası stres bozukluğu", 8, None, "ruhsal ayırıcı tanı", None)
]

PD[13] = [
    ("**Gidiş ve Sonlanış:** Panik bozukluk dalgalı gidişli, alevlenmeler ve remisyonlarla seyreden kronik bir hastalıktır.",
     "Panik bozukluk yaşam boyu dalgalı bir seyir izleyen, zaman zaman alevlenmeler ve iyilik dönemleriyle karakterize kronik seyirli bir tablodur.",
     "dalgalı gidişli kronik", 1, None, "dalgalı kronik gidiş", None),
    ("Hastaların **yüzde elli ila yetmişinde** uygun tedaviyle klinik açıdan tam veya belirgin iyilik sağlanır.",
     "Modern farmakoterapi ve bilişsel davranışçı tedavilerle hastaların yüzde elli ila yetmişinde belirgin ve kalıcı klinik iyilik elde edilebilmektedir.",
     "tedaviyle önemli iyilik", 2, None, "yüzde elli ila yetmiş iyilik", None),
    ("Panik bozukluğu olan bireylerde **intihar riski** genel topluma oranla belirgin düzeyde yüksektir.",
     "Çaresizlik ve tükenmişlik hissinin derinleşmesi nedeniyle panik bozukluk olgularında intihar riski normal popülasyona kıyasla anlamlı derecede yüksektir.",
     "İntihar riski", 3, None, "intihar riski", None),
    ("En sık eşlik eden komplikasyonlar **yüzde elli oranında majör depresyon** ve yüzde yirmi oranında alkol bağımlılığıdır.",
     "Hastalığa en sık eklenen komplikasyon olguların yarısında izlenen majör depresyon ile hastaların beşte birinde anksiyeteyi kendi kendine yatıştırma amacıyla gelişen alkol ve madde bağımlılığıdır.",
     "depresyon ve alkol-madde", 4, None, "depresyon ve alkol bağımlılığı", None)
]

PD[14] = [
    ("**Farmakoterapi:** Birinci basamak temel tedavi seçici serotonin geri alım inhibitörleridir.",
     "Panik bozukluğun farmakoterapisinde birinci basamak altın standart seçenek seçici serotonin geri alım inhibitörleri yani se se re ı grubu antidepresanlardır.",
     "seçici serotonin geri alım", 2, None, "SSRI grubu", None),
    ("Sitalopram, essitalopram, fluoksetin, sertralin ve **paroksetin** ruhsatlı temel ajanlardır.",
     "Klinik uygulamada sitalopram, essitalopram, fluoksetin, fluvoksamin, paroksetin ve sertralin en yüksek kanıt düzeyine sahip serotonin geri alım inhibitörleridir.",
     "sertralin", 3, None, "antidepresan ajanlar", None),
    ("Ayrıca serotonin noradrenalin geri alım inhibitörü **venlafaksin** de yüksek etkinliğe sahiptir.",
     "Serotonin ve noradrenalin geri alımını birlikte bloke eden venlafaksin de panik bozukluk tedavisinde güçlü bir diğer seçenektir.",
     "venlafaksin", 4, None, "venlafaksin", None),
    ("Akut krizlerde ve tedavinin ilk haftalarında **alprazolam veya klonazepam** gibi benzodiazepinler kısa süreli köprü olarak verilebilir.",
     "Antidepresanların terapötik etkisi iki ila dört haftada başladığından, ilk haftalardaki şiddetli krizleri ve anksiyete alevlenmesini yatıştırmak için kısa süreli alprazolam veya klonazepam köprüsü kurulabilir.",
     "benzodiazepinler", 5, None, "benzodiazepin köprüsü", None),
    ("Dirençli olgularda klomipramin veya imipramin gibi **trisiklik antidepresanlar** tercih edilir.",
     "Tedaviye dirençli olgularda klomipramin gibi güçlü trisiklik antidepresanlar veya monoamino oksidaz inhibitörleri devreye sokulabilir.",
     "trisiklik antidepresanlar", 6, None, "trisiklik antidepresanlar", None)
]

PD[15] = [
    ("**Psikoterapi:** Bilişsel davranışçı terapi panik bozuklukta etkinliği en yüksek terapi yöntemidir.",
     "Panik bozukluk tedavisinde psikoterapötik müdahalelerin temel taşını kanıta dayalı bilişsel davranışçı terapiler oluşturmaktadır.",
     "bilişsel-davranışçı terapiler", 1, None, "bilişsel davranışçı terapi", None),
    ("Hastanın felaketleştirici düşüncelerinin **bilişsel olarak yeniden yapılandırılması** hedeflenir.",
     "Terapide hastaya psiko-eğitim verilerek kalbin hızlı çarpmasının kalp krizi anlamına gelmediği öğretilir ve katastrofik ölüm düşünceleri yeniden yapılandırılır.",
     "yeniden yapılandırılması", 2, None, "yeniden yapılandırma", None),
    ("Diyafram nefes egzersizleri ve **progresif kas gevşetme** teknikleri ile sempatik tonus düşürülür.",
     "Hastaya doğru diyafram nefesi alma ve kas gevşeme teknikleri öğretilerek kriz anındaki hiperventilasyon ve sempatik aktivite artışı güvenle kontrol altına alınır.",
     "kas gevşeme yöntemleri", 3, None, "nefes ve kas gevşeme", None),
    ("Zorlu hiperventilasyon gibi **interoseptif maruz bırakma** egzersizleri ile bedensel duyumların zararsızlığı kanıtlanır.",
     "Seans sırasında zorlu hızlı nefes alıp verdirilerek yapay baş dönmesi ve taşikardi oluşturulur; hastanın bu somatik duyumlar nedeniyle ölmediğini bizzat deneyimlemesi sağlanarak duyarsızlaşma elde edilir.",
     "zorlu hiperventilasyon", 4, None, "interoseptif maruz bırakma", None)
]

# ==============================================================================
# BÖLÜM 5: Agorafobi: Tanı Kriterleri, Ayırıcı Tanı ve Tedavi (Sayfa 16 - 21)
# ==============================================================================

PD[16] = [
    ("**Agorafobi:** Toplumsal yerlere ve kaçmanın güç olabileceği ortamlara yalnız girmekten korkmadır.",
     "Agorafobi terimi köken olarak pazar yeri korkusu anlamına gelmekte olup bireyin panik benzeri belirtiler yaşadığında kaçamayacağı veya yardım alamayacağı ortamlardan korkmasını tanımlar.",
     "Toplumsal yerlere yalnız", 1, None, "Agorafobi tanımı", None),
    ("Agorafobinin yaşam boyu yaygınlığı toplumda **yüzde iki ila altı** arasında değişmektedir.",
     "Toplum tabanlı epidemiyolojik araştırmalarda agorafobinin yaşam boyu yaygınlığının yüzde iki ila altı arasında olduğu bildirilmektedir.",
     "yaygınlığı %2-6", 2, None, "yüzde iki ila altı", None),
    ("Klinik sınavlarda ve amfi derslerinde önemle vurgulandığı üzere: Agorafobili olguların **dörtte üçüne panik bozukluk** eşlik etmektedir!",
     "Klinik sınavlarda ve amfi derslerinde önemle vurgulandığı üzere: Psikiyatri kliniklerine başvuran agorafobik olguların yaklaşık dörtte üçünde altta yatan tetikleyici antite panik bozukluk tablosudur.",
     "panik bozukluk eşlik", 3, None, "panik bozukluk birlikteliği", None),
    ("Pek çok olguda agorafobik kaçınmanın başlangıcını **travmatik bir yaşam olayı** tetiklemektedir.",
     "Hastalık öyküsü ayrıntılandırıldığında agorafobik kaçınmanın ilk kez sokakta geçirilen ağır bir panik krizi veya travmatik bir kayıp sonrasında patladığı görülür.",
     "travmatik bir olay", 4, None, "travmatik başlangıç", None)
]

PD[17] = [
    ("**DSM-5 Agorafobi Tanı Kriteri A:** Beş temel durumdan en az ikisinde belirgin korku veya kaygı duyulmalıdır.",
     "De se me beş kriterlerine göre agorafobi tanısı için tanımlanan beş karakteristik yaşam durumundan en az ikisi veya daha fazlasında belirgin korku ya da kaygı bulunması şarttır.",
     "beş durumdan ikisi", 2, None, "beş durumdan ikisi", None),
    ("**Durum 1:** Otobüs, tren, vapur veya uçak gibi **toplu taşıma araçlarını** kullanma korkusudur.",
     "Birinci durum otobüs, metro, tren, vapur veya uçak gibi kapalı ve hareket halindeki toplu taşıma araçlarını kullanırken kapana kısılma korkusudur.",
     "Toplu taşıma", 3, None, "toplu taşıma araçları", None),
    ("**Durum 2 ve 3:** Otopark ve köprü gibi **açık alanlar** ile mağaza ve sinema gibi **kapalı yerlerde** bulunmadır.",
     "İkinci durum otopark, pazar yeri ve köprü gibi açık alanlarda bulunmak; üçüncü durum ise alışveriş merkezleri, tiyatro ve sinema gibi kapalı mekanlarda bulunmaktır.",
     "Açık yerlerde bulunma", 4, None, "açık ve kapalı alanlar", None),
    ("**Durum 4 ve 5:** Kalabalıkta sırada bekleme ve **tek başına evin dışında** bulunma korkusudur.",
     "Dördüncü durum banka ya da market kuyruğunda beklemek, beşinci durum ise güvenli liman olan evin dışında tek başına bulunma korkusudur.",
     "Sırada bekleme", 6, None, "sıra bekleme ve ev dışı", None),
    ("Kişi fenalaştığında **kaçmanın güç olacağı** ya da yardım alamayacağı düşüncesiyle bu ortamlardan kaçınır.",
     "Kişinin bu ortamlardan dehşetle kaçınmasının altında yatan temel bilişsel mekanizma fenalaşırsa kaçamayacağı veya kimsenin kendisine yardım edemeyeceği düşüncesidir.",
     "kaçmanın güç olabileceği", 8, None, "yardım alamama korkusu", None)
]

PD[18] = [
    ("Agorafobik durumlar neredeyse her zaman **anında korku ya da kaygı** doğurur.",
     "Kişi söz konusu fobik mekanlarla karşılaştığında veya bu ortamlara gireceğini düşündüğünde neredeyse her seferinde doğrudan anksiyete yanıtı açığa çıkar.",
     "Agorafobik durumlar", 0, None, "anında kaygı doğurma", None),
    ("Hasta bu durumlardan kaçınır, yanına **güvenli bir refakatçi** alır ya da yoğun ıstırapla katlanır.",
     "Hasta bu ortamlardan tamamen kaçınır, yalnız gidemeyip mutlaka yanına eşini veya yakınını refakatçi alır ya da yoğun bir içsel ıstırap içinde bu duruma katlanır.",
     "eşlik edene gereksinim", 1, None, "refakatçi gereksinimi", None),
    ("Duyulan korku çevrenin yarattığı **gerçek tehlikeye göre orantısız** düzeydedir.",
     "Hastanın hissettiği felaket beklentisi ve dehşet, sosyokültürel bağlamda ortamın barındırdığı objektif ve gerçek tehlikeye kıyasla tamamen orantısızdır.",
     "gerçek tehlikeye göre", 2, None, "orantısız korku", None),
    ("Tanı konabilmesi için korku ve kaçınmanın sürekli olması ve **en az altı ay sürmesi** şarttır.",
     "Tanısal açıdan geçici durumlardan ayrılabilmesi için korku, kaygı ve kaçınma örüntüsünün en az altı ay ya da daha uzun süredir kesintisiz devam ediyor olması zorunludur.",
     "altı ay ya da daha uzun", 3, None, "en az altı ay kuralı", None),
    ("Korku ve kaçınma hastanın mesleki, sosyal ve **ailevi işlevselliğinde belirgin çöküşe** yol açar.",
     "Süregiden bu kaçınmalar bireyin işe gitmesini, sokağa çıkmasını ve sosyal ilişki kurmasını engelleyerek mesleki ve ailesel alanlarda ağır işlev kaybı yaratır.",
     "işlevsellikte düşmeye", 4, None, "işlev kaybı", None)
]

PD[19] = [
    ("**Agorafobide Ayırıcı Tanı:** Depresyon, şizofreni ve kişilik bozuklukları dikkatle dışlanmalıdır.",
     "Agorafobi ayırıcı tanısında hastayı eve kapatabilecek majör depresyon, agorafobik hezeyanlar içeren şizofreni ve kişilik bozuklukları ekarte edilmelidir.",
     "Ayırıcı tanı", 0, None, "Agorafobi ayırıcı tanı", None),
    ("Çekingen kişilik bozukluğunda hasta **eleştirilme ve reddedilme korkusuyla** insanlardan kaçınır.",
     "Çekingen kişilik bozukluğunda birey panik nöbeti korkusuyla değil, başkaları tarafından yetersiz bulunma, eleştirilme ve aşağılanma korkusuyla toplumsal temaslardan çekinir.",
     "Çekingen kişilik", 4, None, "çekingen kişilik", None),
    ("Bağımlı kişilik bozukluğunda ise kişi **kendi başına karar alamadığı** için bir refakatçiye bağlanır.",
     "Bağımlı kişilik bozukluğunda ise kişi kendi başına hayatını idame ettiremeyeceğine inandığı için sürekli bir eşlikçiye yapışır ancak agorafobik panik korkusu taşımaz.",
     "Bağımlı kişilik", 5, None, "bağımlı kişilik", None)
]

PD[20] = [
    ("**Gidiş ve Prognoz:** Panik bozukluğa bağlı agorafobide panik tedavi edildiğinde agorafobi de düzelir.",
     "Eğer agorafobi panik bozukluğun bir komplikasyonu olarak gelişmişse, panik ataklar başarılı biçimde tedavi edildiğinde agorafobik kaçınma da büyük oranda çözülür.",
     "panik bozukluk tedavi", 1, None, "panik tedavisiyle düzelme", None),
    ("Buna karşın panik bozukluğun eşlik etmediği **saf agorafobi** son derece kısıtlayıcı ve kroniktir.",
     "Buna karşılık altta panik atakların bulunmadığı primer saf agorafobi klinik olarak çok daha inatçı, tedaviye dirençli ve hastayı eve hapseden kronik bir gidiş gösterir.",
     "kroniktir", 2, None, "saf agorafobi kronikliği", None),
    ("Tabloya **depresyon ve alkol kullanım bozukluğunun** eklenmesi prognozu ağırlaştırır.",
     "Hastalığın kronikleştiği olgularda sekonder majör depresyon ve alkolle kendini uyuşturma çabası klinik gidişatı son derece komplike ve karanlık hale getirir.",
     "alkol kullanım bozukluğu", 3, None, "depresyon ve alkol", None)
]

PD[21] = [
    ("**Agorafobi Tedavisi:** Farmakoterapide SSRI antidepresanlar ve benzodiazepinler kullanılır.",
     "Agorafobinin farmakolojik tedavisinde panik bozuklukta olduğu gibi seçici serotonin geri alım inhibitörleri ve kriz anlarında kontrollü benzodiazepinler reçete edilir.",
     "Farmakoterapi", 1, None, "Agorafobi farmakoterapi", None),
    ("Psikoterapide davranışçı maruz bırakma ve **kademeli in vivo alıştırma** temel yöntemdir.",
     "Psikoterapide en yüksek başarıyı sağlayan yöntem kaçınılan ortamlara kolaydan zora doğru aşamalı olarak adım atılmasını sağlayan in vivo yani gerçek yaşamda maruz bırakmadır.",
     "Davranışçı Terapi", 7, None, "maruz bırakma", None),
    ("Son yıllarda bilgisayar destekli **sanal gerçeklik terapisi** de maruziyeti kolaylaştırmaktadır.",
     "Son yıllarda sanal gerçeklik gözlükleri ve simülasyonlar kullanılarak hastanın güvenli klinik ortamında fobik mekanlara sanal olarak maruz bırakılması tedavi uyumunu belirgin biçimde artırmıştır.",
     "Sanal Terapi", 9, None, "sanal gerçeklik terapisi", None)
]

# ==============================================================================
# BÖLÜM 6: Fobik Bozukluklar ve Özgül Fobi (Sayfa 22 - 29)
# ==============================================================================

PD[22] = [
    ("**Fobik Bozukluk:** Belirli nesne, durum ya da aktivitelere karşı akılcı olmayan aşırı korku halidir.",
     "Fobi terimi bireyin belirli bir nesne, canlı, doğal durum ya da eylemle karşılaştığında hissettiği akıl dışı, gerçek tehditle orantısız ve aşırı korku reaksiyonunu tanımlar.",
     "Fobik Bozukluk", 0, None, "fobi tanımı", None),
    ("Fobik bozukluklar temel olarak **özgül fobi** ve **sosyal fobi** olmak üzere iki ana gruba ayrılır.",
     "Klinik psikiyatride fobik bozukluklar özgül bir duruma yönelik olan özgül fobi ve başkalarının önünde küçük düşme kaygısı taşıyan sosyal fobi şeklinde iki ana sınıfa ayrılır.",
     "özgül fobi ve sosyal", 1, None, "özgül ve sosyal fobi", None),
    ("Özgül fobide kedi, köpek, örümcek, yükseklik veya **uçak yolculuğu** gibi nesne ve durumlar korku üretir.",
     "Özgül fobide kedi, köpek, örümcek gibi hayvanlar, kan görme, iğne yapılması veya uçak ve asansör gibi özgül durumlara karşı orantısız panik reaksiyonu ortaya çıkar.",
     "durumun(uçak yolculuğu", 2, None, "fobik nesneler", None),
    ("Sosyal fobide ise kişi toplum karşısında konuşma veya yemek yeme gibi eylemlerde **küçük düşme korkusu** yaşar.",
     "Sosyal fobide ise birey yabancılarla tanışırken, topluluk önünde sunum yaparken ya da başkalarının bakışları altında yemek yerken rezil olacağı ve küçük düşeceği korkusunu yaşar.",
     "küçük duruma düşeceği", 3, None, "küçük düşme korkusu", None)
]

PD[23] = [
    ("**Fobilerin Epidemiyolojisi:** Özgül fobinin yaşam boyu görülme sıklığı yüzde on bir civarındadır.",
     "Epidemiyolojik çalışmalarda özgül fobinin toplumda yaşam boyu görülme sıklığının yüzde on bir gibi oldukça yüksek bir orana ulaştığı gösterilmiştir.",
     "yaşam boyu görülme olasılığının %11", 1, None, "yüzde on bir prevalans", None),
    ("Sosyal fobinin yaşam boyu yaygınlığı ise **yüzde üç ila on üç** arasında bildirilmektedir.",
     "Toplumsal kaygı bozukluğu yani sosyal fobinin yaygınlığı ise farklı toplumlarda yüzde üç ila on üç arasında geniş bir aralık sergilemektedir.",
     "sosyal fobinin ise %3-13", 1, None, "sosyal fobi prevalansı", None),
    ("Özgül fobiler sıklıkla **çocukluk yaşlarında** başlar ve kadınlarda erkeklere göre iki kat fazladır.",
     "Özgül fobiler genellikle çocukluk çağında başlangıç gösterir ve kadınlarda erkeklere kıyasla iki kat daha sık karşımıza çıkar.",
     "çocukluk yaşlarında başlar", 2, None, "çocukluk başlangıcı", None),
    ("Sosyal fobi ise çoğunlukla **ergenlik yıllarında** başlar ve kadın ile erkeklerde eşit oranda görülür.",
     "Sosyal fobi ise kimlik gelişiminin ve akran ilişkilerinin ön plana çıktığı ergenlik döneminde başlar ve özgül fobinin aksine kadın ve erkeklerde eşit oranda görülür.",
     "ergenlik yıllarında başlar", 3, None, "ergenlik başlangıcı", None)
]

PD[24] = [
    ("**Davranışsal Etiyoloji:** Klasik koşullanma ve meşhur Küçük Albert deneyi modelidir.",
     "Özgül fobilerin davranışçı etiyolojisinde Watson tarafından yürütülen meşhur Küçük Albert deneyindeki klasik koşullanma ve pekiştirme ilkeleri yer alır.",
     "Küçük Albert Deneyi", 2, None, "Küçük Albert Deneyi", None),
    ("Psikanalitik kurama göre yasaklı dürtüler **yer değiştirme ve sembolizasyon** ile nesneye aktarılır.",
     "Psikanalitik kuramda id kaynaklı kabul edilemez bilinçdışı dürtülerin yarattığı anksiyete, yer değiştirme mekanizmasıyla dış dünyadaki simgesel bir nesneye aktarılır.",
     "yer değiştirme", 4, None, "yer değiştirme ve sembolizasyon", None),
    ("Genetik faktörler incelendiğinde **kan, enjeksiyon ve yaralanma** tipi fobi çok yüksek ailesel yatkınlığa sahiptir.",
     "Genetik faktörler değerlendirildiğinde özellikle kan, enjeksiyon ve yaralanma tipi fobisi olan bireylerin ailelerinde benzer tablonun görülme oranı son derece yüksektir.",
     "kan-enjeksiyon-yaralanma tipi", 6, None, "kan enjeksiyon genetiği", None)
]

PD[25] = [
    ("**DSM-5 Özgül Fobi Kriterleri:** Özgül bir nesne ya da durumla ilgili belirgin korku veya kaygı duyulmalıdır.",
     "De se me beş kriterlerine göre özgül fobi tanısı için belirli bir nesne, canlı veya durumla karşılaşma ya da karşılaşma beklentisiyle anında korku doğması şarttır.",
     "Özgül bir nesne", 2, None, "özgül nesne korkusu", None),
    ("Çocuklarda bu korku ağlama, **bağırıp çağırma, tepinme**, donakalma ya da sıkıca sarılma ile kendini gösterir.",
     "Klinik pratikte çocuk hastalar korkularını sözel olarak ifade edemeyebilir; ağlama krizleri, öfke patlamaları, donakalma ya da ebeveyne sımsıkı yapışma ile dışa vururlar.",
     "bağırıp çağırarak tepinme", 3, None, "çocuklarda klinik dışavurum", None),
    ("Fobik nesne neredeyse her zaman doğrudan kaygı doğurur ve durumdan **etkin biçimde kaçınılır**.",
     "Fobi kaynağı uyaran her temas edildiğinde kaçınılmaz bir dehşet üretir ve hasta bu nesneyle karşılaşmamak için hayatını kısıtlayıcı önlemler alır.",
     "etkin bir biçimde kaçınılır", 5, None, "etkin kaçınma", None),
    ("Tanı için korkunun sürekli olması, **en az altı ay sürmesi** ve belirgin işlev kaybı yaratması zorunludur.",
     "Tanı konabilmesi için bu korku ve kaçınmanın sürekli olması, en az altı ay devam etmesi ve hastanın günlük yaşamında belirgin işlevsellik kaybı yaratması gereklidir.",
     "sürekli bir durumdur", 7, None, "en az altı ay sürmesi", None),
    ("Fobi türleri **hayvan, doğal çevre**, kan-enjeksiyon-yaralanma ve durumsal olmak üzere kodlanır.",
     "Özgül fobiler klinik olarak hayvan tipi, fırtına ve yükseklik gibi doğal çevre tipi, kan-enjeksiyon-yaralanma tipi ve uçak veya asansör gibi durumsal tip olarak kodlanır.",
     "kodlanır: hayvan", 9, None, "fobi alt tipleri", None)
]

PD[26] = [
    ("Özgül fobi uyarısıyla karşılaşan bireylerde taşikardi, terleme ve kas gerginliği gibi **sempatik aktivite artışı** olur.",
     "Hayvan veya yükseklik gibi tipik bir fobik uyaranla yüzleşen kişide akut kaç ya da savaş refleksi devreye girerek taşikardi, takipne, terleme ve kas sertliği gelişir.",
     "sempatik aktivitede artış", 2, None, "sempatik aktivite artışı", None),
    ("Klinik sınavlarda ve amfi derslerinde önemle vurgulandığı üzere: **Kan-enjeksiyon tipinde farklı olarak bifazik tepki** gelişir!",
     "Klinik sınavlarda ve amfi derslerinde önemle vurgulandığı üzere: Kan, enjeksiyon ve yaralanma fobisinde diğer tüm fobilerden farklı olarak önce kısa süreli bir taşikardi, hemen ardından derin bir bradikardi ile seyreden bifazik tepki gelişir.",
     "bifazik tepki gelişir", 3, None, "bifazik tepki", None),
    ("Sempatik aktiviteyi hızla takip eden **vazovagal deşarj ve bradikardi**, baygınlık hissi ve senkopla sonuçlanır.",
     "Bu bifazik yanıtta ani vagal tonus artışı ve vazodilatasyon kan basıncını düşürür, serebral perfüzyonu azaltarak hastada klasik vazovagal bayılma yani senkop oluşturur.",
     "vazovagal bayılma", 3, None, "vazovagal senkop", None),
    ("Özgül fobiye hastaların **yüzde elli ila sekseninde** başka bir anksiyete veya duygudurum bozukluğu eşlik eder.",
     "Klinik veriler özgül fobisi olan bireylerin yüzde elli ila sekseninde diğer anksiyete bozuklukları, majör depresyon veya madde kötüye kullanımı bulunduğunu göstermektedir.",
     "birlikte görülme oranı %50-80", 4, None, "komorbidite sıklığı", None)
]

PD[27] = [
    ("**Gidiş ve Sonlanış:** Özgül fobi dalgalanma göstermeyen, kronik ve sabit seyirli bir bozukluktur.",
     "Diğer anksiyete bozukluklarının alevlenip yatışan dalgalı klinik tablosunun aksine özgül fobiler yıllar boyu oldukça sabit ve kronik bir klinik seyir gösterir.",
     "Kronik seyirli", 1, None, "kronik sabit seyir", None),
    ("Hayvan, doğal çevre ve kan fobileri çocuklukta; **durumsal fobiler erken erişkinlikte** tepe yapar.",
     "Başlangıç yaşı açısından bimodal bir dağılım söz konusudur: Hayvan ve kan fobileri erken çocuklukta patlarken, uçak ve araba gibi durumsal fobiler yirmili yaşlarda tepe yapar.",
     "bimodal bir başlangıç", 2, None, "bimodal başlangıç", None),
    ("Tedavi edilmeyen özgül fobiler **kendiliğinden düzelme göstermez** ve ömür boyu sebat eder.",
     "Kendi haline bırakılan özgül fobilerde kendiliğinden remisyon oranı son derece düşüktür; tedavi edilmediği takdirde bireyin tüm erişkinlik yaşamı boyunca devam eder.",
     "sabit bir klinik gidiş", 3, None, "spontan düzelmeme", None)
]

PD[28] = [
    ("**Ayırıcı Tanı:** Panik bozukluk, travma sonrası stres bozukluğu, OKB ve hipokondriyazis ayrılmalıdır.",
     "Özgül fobi ayırıcı tanısında panik bozukluk, travma sonrası stres bozukluğu, obsesif kompulsif bozukluk ve hipokondriyazis yani hastalık kaygısı bozukluğu dışlanmalıdır.",
     "Ayırıcı Tanı", 0, None, "Özgül fobi ayırıcı tanı", None),
    ("Panik bozuklukta nöbetler beklenmedik anlarda gelirken, fobi nöbeti **yalnızca fobik nesneyle** tetiklenir.",
     "Panik bozuklukta nöbetler tamamen öngörülemez ve kendiliğinden patlarken, özgül fobide anksiyete reaksiyonu yalnız ve ancak fobi kaynağı spesifik nesneyle karşılaşınca başlar.",
     "panik bozukluğu", 1, None, "panik bozukluk ayrımı", None),
    ("Travma sonrası stres bozukluğunda ise kaçınma **yaşanmış ağır bir travmanın** hatırlatıcılarına yöneliktir.",
     "Travma sonrası stres bozukluğundaki kaçınmalar genel bir nesneye değil, hastanın bizzat maruz kaldığı kaza veya saldırı gibi yaşamsal travmanın anımsatıcılarına karşıdır.",
     "travma sonrası stres", 2, None, "TSSB ayrımı", None)
]

PD[29] = [
    ("**Özgül Fobide İlaç Tedavisi:** Bu bozukluğun tedavisinde etkinliği kanıtlanmış hiçbir psikotropik ilaç yoktur!",
     "Sınavlarda ve klinik pratikte çok önemli bir kural olarak özgül fobinin primer tedavisinde etkinliği bilimsel olarak kanıtlanmış hiçbir psikotropik ilaç bulunmamaktadır.",
     "etkinliği kanıtlanmış", 1, None, "ilaç tedavisinin olmaması", None),
    ("**Psikoterapi:** Bilişsel davranışçı terapi ve aşamalı maruz bırakma altın standart tedavi yöntemidir.",
     "Özgül fobinin tartışmasız altın standart ve kesin tedavi yöntemi bilişsel davranışçı terapi ve hastanın korkulan nesneyle aşamalı olarak yüzleştirildiği maruz bırakma protokolüdür.",
     "Bilişsel-davranışçı terapi", 3, None, "BDT altın standart", None),
    ("Kan ve enjeksiyon fobisinde bayılmayı önlemek amacıyla **uygulamalı kas germe** tekniği uygulanır.",
     "Vazovagal senkop riski taşıyan kan ve iğne fobilerinde kan basıncının aniden çakılmasını engellemek için büyük kas gruplarının ritmik kasılmasını içeren uygulamalı kas germe öğretilir.",
     "Psikoterapi", 2, None, "uygulamalı kas germe", None)
]

# ==============================================================================
# BÖLÜM 7: Sosyal Fobi (Toplumsal Kaygı Bozukluğu) (Sayfa 30 - 36)
# ==============================================================================

PD[30] = [
    ("**Sosyal Fobi:** Yabancılarla teması ve dikkatle incelenmeyi içeren toplumsal durumlardan belirgin korkudur.",
     "Sosyal fobi diğer adıyla toplumsal kaygı bozukluğu, bireyin yabancılarla karşılaşabileceği veya başkalarının dikkatli bakışlarına maruz kalacağı sosyal durumlardan belirgin dehşet duymasıdır.",
     "Sosyal Fobi", 0, None, "Sosyal Fobi tanımı", None),
    ("Bu kişiler toplumsal ortamlarda **küçük duruma düşmekten ve utanmaktan** aşırı derecede korkarlar.",
     "Hastalar topluluk önünde konuşurken, resmi toplantılarda veya yeni biriyle tanışırken ellerinin titreyeceği, seslerinin kısılacağı, rezil olup küçük duruma düşecekleri dehşeti yaşarlar.",
     "utanmalarının korkusu", 2, None, "utanma ve küçük düşme", None),
    ("Korkulan eylemler arasında **başkalarıyla yemek yemek** veya karşılıklı yazı yazmak gibi sıradan durumlar da bulunur.",
     "Korkulan durumlar yalnızca kürsüde sunum yapmaktan ibaret olmayıp restoranda başkalarının gözü önünde yemek yemek, bir form doldururken yazı yazmak gibi eylemleri de kapsar.",
     "toplumsal durumlardan", 1, None, "sıradan sosyal durumlar", None)
]

PD[31] = [
    ("**Nörokimyasal Etiyoloji:** Performans fobisi olanlarda artmış norepinefrin ve epinefrin salınımı izlenir.",
     "Sosyal fobinin nörobiyolojisinde adrenerjik sistem hiperaktivitesi, artmış norepinefrin ve epinefrin salınımı ile periferik reseptörlerin aşırı duyarlılığı rol oynamaktadır.",
     "Nörokimyasal Etkenler", 1, None, "artmış katekolaminler", None),
    ("Ayrıca striatal ve mezokortikal devrelerde **dopaminerjik işlev bozukluğu** mevcuttur.",
     "Sosyal ödül ve motivasyon devrelerini yöneten dopaminerjik yollardaki işlev bozukluğunun da sosyal kaygının kronikleşmesinde etkili olduğu gösterilmiştir.",
     "dopaminerjik işlev bozukluğu", 3, None, "dopaminerjik işlev bozukluğu", None),
    ("Genetik faktörler incelendiğinde hastaların **birinci derece akrabalarında üç kat fazla** risk saptanır.",
     "Aile ve ikiz çalışmaları sosyal fobisi bulunan bireylerin birinci derece akrabalarında toplumsal kaygı bozukluğu riskinin genel topluma göre üç kat arttığını ortaya koymaktadır.",
     "Birinci derece akrabalarda 3 kat", 5, None, "üç kat artmış risk", None)
]

PD[32] = [
    ("**Bilişsel Davranışçı Kuram:** Sosyal ortama girince otomatik olumsuz düşünceler hızla aktive olur.",
     "Sosyal fobinin bilişsel modeline göre kişi toplumsal bir ortama girdiğinde zihninde ne kadar sıkıcı ve yetersiz birisi olduğumu düşünecekler şeklinde otomatik inançlar devreye girer.",
     "Otomatik düşüncelerin", 2, None, "otomatik düşünceler", None),
    ("Birey ortamı doğrudan bir **sosyal tehlike alanı** olarak algılar ve sempatik kaç ya da savaş yanıtı patlar.",
     "Bu olumsuz düşünceler ortamı bir tehdit alanına dönüştürerek çarpıntı, takipne, terleme ve yüz kızarması ile giden sempatik otonomik alarmı ateşler.",
     "Sosyal tehlike algısı", 4, None, "sosyal tehlike algısı", None),
    ("Dikkatin tamamen **kendine odaklanması** ve başkalarının gözüyle kendine bakış kaygıyı tırmandırır.",
     "Hasta dikkatini dış dünyaya ve sohbete vermek yerine tamamen kendi bedensel kusurlarına, kalp atışına ve ses tonuna odaklayarak dışarıdan ne kadar acınası göründüğünü kurgular.",
     "Kendine odaklanma", 6, None, "kendine odaklanma", None),
    ("Göz temasından kaçınma ve sessiz kalma gibi **güvenlik sağlayıcı davranışlar** patolojiyi pekiştirir.",
     "Kaygıyı gizlemek amacıyla göz temasını kesme, bir köşeye saklanma veya suskun kalma gibi güvenlik sağlayıcı davranışlar hastanın performansını bozarak kısır döngüyü sürdürür.",
     "güvenlik sağlayıcı", 7, None, "güvenlik sağlayıcı davranışlar", None)
]

PD[33] = [
    ("**DSM-5 Sosyal Fobi Kriterleri:** Başkalarınca değerlendirilebilecek toplumsal durumlarda belirgin korku duyulmalıdır.",
     "De se me beş kriterlerine göre bireyin başkaları tarafından değerlendirilme, eleştirilme veya gözlenme olasılığı bulunan toplumsal ortamlarda belirgin dehşet duyması şarttır.",
     "başkalarınca değerlendirilebilecek", 2, None, "değerlendirilme korkusu", None),
    ("Kişi olumsuz değerlendirilecek, **küçük düşecek veya başkalarını kıracak** biçimde davranmaktan korkar.",
     "Hasta terleyerek, titreyerek veya kekeleyerek yetersizliğinin ortaya çıkmasından, rezil olmaktan, alay edilmekten ya da dışlanmaktan derin bir utançla korkar.",
     "olumsuz olarak değerlendirilecek", 3, None, "olumsuz değerlendirilme", None),
    ("Söz konusu sosyal ortamlardan etkin biçimde kaçınılır ya da **yoğun korku ile katlanılır**.",
     "Kişi toplantılardan, sunumlardan ve davetlerden bütünüyle kaçınır veya kaçamadığı zorunlu durumlara dayanılmaz bir içsel panik ve korku eşliğinde katlanır.",
     "yoğun bir korku ya da kaygı ile", 5, None, "kaçınma ve katlanma", None),
    ("Tanı için korku ve kaçınmanın sürekli olması, **en az altı ay sürmesi** ve belirgin işlev kaybı yapması gerekir.",
     "Tanı konabilmesi için fobik kaçınmaların süreğen olması, en az altı ay devam etmesi ve hastanın okul, iş veya arkadaşlık ilişkilerinde belirgin çöküşe yol açması şarttır.",
     "altı ay ya da daha uzun", 7, None, "en az altı ay", None),
    ("Korku bir maddenin etkisine, panik bozukluğa ya da **Parkinson veya yanık** gibi organik bir duruma bağlanamaz.",
     "Dışlama kriterleri uyarınca sosyal çekiniklik bir maddeye, panik nöbetlerine ya da Parkinson veya yüzde yanık izi gibi organik biçim bozukluklarının yarattığı sıkıntıya bağlanamamalıdır.",
     "parkinson,yanık", 9, None, "dışlama kriterleri", None)
]

PD[34] = [
    ("**Klinik Tipler:** Birçok sosyal durumdan korkan olgularda **yaygın tip sosyal fobi** tanımlanır.",
     "Klinik pratikte eğer hasta hem konuşmaktan hem yemekten hem de yabancılarla tanışmaktan kaçınıyorsa bu tabloya yaygın tip sosyal fobi adı verilir.",
     "yaygın tipte sosyal fobi", 4, None, "yaygın tip sosyal fobi", None),
    ("Yaygın tip sosyal fobi klinik pratikte çoğunlukla **çekingen kişilik bozukluğu** ile birlikte görülür.",
     "Yaygın tip sosyal fobi olgularının çok büyük bir kısmı yaşam boyu süregiden ve derin bir aşağılık kompleksi içeren çekingen kişilik bozukluğu ile iç içe geçmiştir.",
     "çekingen kişilik bozukluğu ile", 6, None, "çekingen kişilik birlikteliği", None),
    ("Sosyal fobiye en sık **diğer anksiyete bozuklukları, depresyon**, alkol bağımlılığı ve bulimia nervoza eşlik eder.",
     "Eşlik eden psikiyatrik komorbiditeler incelendiğinde depresif bozukluklar, diğer anksiyete tabloları, kaygıyı baskılamak için sığınılan alkol bağımlılığı ve bulimia nervoza başı çeker.",
     "diğer anksiyete bozuklukları", 5, None, "komorbidite yelpazesi", None)
]

PD[35] = [
    ("**Sosyal Fobide Ayırıcı Tanı:** Agorafobi, panik bozukluk, çekingen ve şizoid kişilik bozuklukları ayrılmalıdır.",
     "Ayırıcı tanıda agorafobi, panik bozukluk, majör depresyon, çekingen kişilik bozukluğu ve şizoid kişilik bozukluğu dikkatle ayrıştırılmalıdır.",
     "Ayırıcı Tanı", 0, None, "Sosyal fobi ayırıcı tanı", None),
    ("Agorafobide temel korku **panik anında yardım alamamaktır**; sosyal fobide ise temel korku **rezil olmaktır**.",
     "Klinik ayrımdaki en zarif kural şudur: Agorafobide hasta fenalaştığında ortamdan kaçamayacağından ve yardım bulamayacağından korkarken, sosyal fobide insanların gözünde rezil olmaktan korkar.",
     "Agorafobi", 1, None, "Agorafobi ayrımı", None),
    ("Şizoid kişilik bozukluğunda hasta **sosyal ilişki kurmak istemez**; sosyal fobide ise hasta ilişki ister ama korkar.",
     "Şizoid kişilik bozukluğundaki birey insan ilişkilerine karşı tamamen kayıtsızdır ve sosyalleşmeyi istemez; oysa sosyal fobik birey insanlarla yakın bağ kurmayı çok ister ama utanç ve korkusu nedeniyle yaklaşamaz.",
     "Şizoid KB", 5, None, "Şizoid ayrımı", None)
]

PD[36] = [
    ("**Gidiş ve Sonlanış:** Sosyal fobi erken yaşta başlayan ve ömür boyu işlevselliği kısıtlayan kronik bir hastalıktır.",
     "Sosyal fobi tedavi edilmediği takdirde bireyin kariyerini, evliliğini ve akademik başarısını derinden baltalayan ömür boyu kronik seyirli bir tablodur.",
     "kronik seyir gösteren", 1, None, "kronik gidiş", None),
    ("Kötü prognoz ölçütleri bozukluğun **on bir yaşından önce başlaması** ve ek psikiyatrik hastalığın bulunmasıdır.",
     "Klinik araştırmalarda kötü gidiş göstergeleri hastalığın on bir yaşından önce erken patlaması, ek psikiyatrik tanıların bulunması ve düşük sosyoekonomik eğitim düzeyidir.",
     "11 yaşından önce başlaması", 3, None, "on bir yaş öncesi başlangıç", None),
    ("Tedavi edilmeyen olgularda **kronik işsizlik ve yalnızlık** yaşam boyu kaçınılmaz hale gelmektedir.",
     "Sağaltım uygulanmayan hastalarda üniversiteyi bırakma, meslek edinememe, işsiz kalma ve yapayalnız bir hayata mahkum olma riski son derece yüksektir.",
     "önemli işlev kayıplarına", 2, None, "işlev kaybı ve yalnızlık", None)
]

# ==============================================================================
# BÖLÜM 8: Fobik Bozukluklarda Tedavi ve Psikoterapi Modaliteleri (Sayfa 37 - 38)
# ==============================================================================

PD[37] = [
    ("**Sosyal Fobide Farmakoterapi:** Yaygın tipte birinci basamak tedavi seçici serotonin geri alım inhibitörleridir.",
     "Yaygın tip sosyal fobinin farmakolojik tedavisinde ilk basamak tercih seçici serotonin geri alım inhibitörleri olan essitalopram, fluoksetin, sertralin ve paroksetindir.",
     "seçici serotonin geri alım inhibitörleri", 1, None, "SSRI farmakoterapisi", None),
    ("Ayrıca serotonin noradrenalin geri alım inhibitörü **venlafaksin** ve MAO-A inhibitörü **moklobemid** kullanılır.",
     "İkinci basamak farmakoterapide venlafaksin gibi ajanlar ile tersinir bir monoamino oksidaz a inhibitörü olan moklobemid yüksek klinik etkinlikle tercih edilebilir.",
     "moklobemid", 2, None, "venlafaksin ve moklobemid", None),
    ("Klinik sınavlarda ve amfi derslerinde önemle vurgulandığı üzere: **Performans kaygısında durumsal beta blokerler** kullanılır!",
     "Klinik sınavlarda ve amfi derslerinde önemle vurgulandığı üzere: Yalnızca topluluk önünde konuşma veya müzik dinletisi gibi kısıtlı performans anksiyetesi olan olgularda eylemden kırk beş dakika önce alınan propranolol gibi beta blokerler taşikardi ve el titremesini önlemede son derece etkilidir.",
     "α-adrenerjik blokerler", 4, None, "beta blokerler", None),
    ("İlaç tedavisinin yanı sıra **bilişsel davranışçı terapi** sosyal fobinin kalıcı tedavisinde vazgeçilmezdir.",
     "Farmakolojik kontrol sağlandıktan sonra nükslerin kalıcı olarak engellenmesi için hastanın mutlaka bilişsel davranışçı terapi sürecinden geçirilmesi gerekir.",
     "Bilişsel-davranışçı tedavi", 6, None, "BDT tedavisi", None)
]

PD[38] = [
    ("**Psikoterapi Teknikleri:** Fobik bozuklukların tedavisinde bilişsel davranışçı terapiler en etkili yaklaşımdır.",
     "Tüm fobik bozuklukların tedavisinde hem özgül hem sosyal fobide uzun vadeli başarısı kanıtlanmış en güçlü yaklaşım bilişsel davranışçı terapidir.",
     "bilişsel-davranışçı terapiler en etkili", 0, None, "BDT etkinliği", None),
    ("Fobik nesneye aşamalı olarak maruz bırakma yani **sistematik desensitizasyon** ile duyarsızlaşma sağlanır.",
     "Korku hiyerarşisinde en hafif basamaktan başlanarak hastanın korkulan nesneyle kontrollü ve kademeli biçimde yüzleştirilmesine maruz bırakma ve sistematik desensitizasyon adı verilir.",
     "sistematik desentisizasyon", 1, None, "sistematik desensitizasyon", None),
    ("Hastanın doğrudan en yüksek korku uyaranıyla yüzleştirilip beklenmesine ise **taşırma yani flooding** denir.",
     "Kademeli alıştırma yerine hastanın tolere edebildiği en son noktadaki yoğun fobik uyaranla aniden karşılaştırılıp kaygı sönene dek tutulması yöntemine ise taşırma yani flooding adı verilir.",
     "flooding", 1, None, "taşırma flooding", None),
    ("Sosyal fobide maruziyetin yanı sıra **sosyal beceri eğitimi** ve bilişsel yeniden yapılanma uygulanır.",
     "Sosyal fobiye özel olarak maruz bırakmanın yanına göz teması kurma ve sohbete başlama gibi sosyal beceri eğitimleri ile yetersiz benlik algısını düzelten bilişsel yeniden yapılanma eklenir.",
     "sosyal beceri eğitimi", 2, None, "sosyal beceri eğitimi", None),
    ("Dersimizi tamamlarken anksiyete bozukluklarında doğru tanı, **erken maruz bırakma ve hedefe yönelik sağaltımın** hastanın hayatını geri kazandırdığını unutmuyoruz.",
     "Böylece panik bozukluk ve fobik bozukluklar dersimizi tamamlarken doğru tanısal ayrımın, erken psikoeğitimin ve hedefe yönelik tedavinin hastanın yaşam kalitesini eksiksiz geri kazandırdığını bir kez daha vurguluyoruz.",
     "bilişsel yeniden yapılanma", 2, None, "ders özeti", None)
]

def main():
    print(f"Building clean_k2 structure for y25-k2-55 across all 38 pages...")
    
    bolum_def = [
        ("Bölüm 1: Panik Atak ve Panik Bozukluk Kavramı", [1, 2, 3, 4]),
        ("Bölüm 2: Panik Bozukluk Etiyolojisi ve Nörobiyolojisi", [5, 6]),
        ("Bölüm 3: Panik Atağın Semptomatolojisi ve DSM-5 Kriterleri", [7, 8, 9, 10, 11]),
        ("Bölüm 4: Ayırıcı Tanı, Gidiş ve Panik Bozukluk Tedavisi", [12, 13, 14, 15]),
        ("Bölüm 5: Agorafobi: Tanı Kriterleri, Ayırıcı Tanı ve Tedavi", [16, 17, 18, 19, 20, 21]),
        ("Bölüm 6: Fobik Bozukluklar ve Özgül Fobi", [22, 23, 24, 25, 26, 27, 28, 29]),
        ("Bölüm 7: Sosyal Fobi (Toplumsal Kaygı Bozukluğu)", [30, 31, 32, 33, 34, 35, 36]),
        ("Bölüm 8: Fobik Bozukluklarda Tedavi ve Psikoterapi Modaliteleri", [37, 38])
    ]
    
    clean_k2 = {
        "ders_id": "k2-55",
        "surum": 2,
        "bolumler": []
    }
    
    sents = []
    
    p_counter = 1
    for b_idx, (b_title, p_nums) in enumerate(bolum_def, 1):
        b_obj = {
            "id": f"k2-55-b{b_idx:02d}",
            "baslik": b_title,
            "paragraflar": []
        }
        for pno in p_nums:
            items = PD.get(pno, [])
            p_sents = []
            for item in items:
                ekran, ses, spat, sidx, cik, hw, sekil = item
                s_obj = make_sentence(ekran, ses, pno, spat, sidx, cik, hw, sekil)
                p_sents.append(s_obj)
                sents.append(s_obj)
            b_obj["paragraflar"].append({
                "id": f"k2-55-p{p_counter:03d}",
                "sayfa": pno,
                "cumleler": p_sents
            })
            p_counter += 1
        clean_k2["bolumler"].append(b_obj)
        
    total_words = sum(len(s["ses"].split()) for s in sents)
    print(f"Total sentences: {len(sents)}, Total words: {total_words} (~{total_words/130:.1f} minutes)")

    # 12-15 Clean Semantic Drawing Commands
    # Vocabulary verified directly against spoken sentences!
    drawings = [
        {
            "cumle": "k2-55-c0007", "bas": 0, "son": 5, "sayfa": 2,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Panik Atak Özellikleri",
            "ogeler": [
                "Aniden başlayan yoğun korku ve sıkıntı",
                "Dakikalar içinde hızla şiddetlenen nöbet",
                "Tek başına bir hastalık veya tanı değildir"
            ]
        },
        {
            "cumle": "k2-55-c0012", "bas": 0, "son": 5, "sayfa": 3,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Panik Bozukluk Tablosu",
            "ogeler": [
                "Beklenmedik yineleyici panik atakları",
                "Kalp krizi ve çıldırma katastrofik korkusu",
                "Sürekli yıpratıcı beklenti anksiyetesi"
            ]
        },
        {
            "cumle": "k2-55-c0022", "bas": 0, "son": 5, "sayfa": 5,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Nörobiyolojik Kuramlar",
            "ogeler": [
                "Lokus seruleus noradrenerjik hiperaktivitesi",
                "Kemoreseptör karbondioksit aşırı duyarlılığı",
                "GABA baskılayıcı düzenleme bozukluğu"
            ]
        },
        {
            "cumle": "k2-55-c0026", "bas": 0, "son": 5, "sayfa": 6,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Bilişsel Model Döngüsü",
            "ogeler": [
                "Fizyolojik bedensel duyumların algılanması",
                "Kalp krizi şeklinde felaketleştirici yorum",
                "Korkunun artması ve panik döngüsü"
            ]
        },
        {
            "cumle": "k2-55-c0030", "bas": 0, "son": 5, "sayfa": 7,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Somatik Belirtiler",
            "ogeler": [
                "Çarpıntı ve kalbin küt küt atması hissi",
                "Soluğun kesilmesi ve boğulma hissi",
                "Göğüs sıkışması ve baş dönmesi sersemlik"
            ]
        },
        {
            "cumle": "k2-55-c0034", "bas": 0, "son": 5, "sayfa": 8,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Algısal ve Bilişsel Belirtiler",
            "ogeler": [
                "Derealizasyon: çevrenin gerçek dışı gelmesi",
                "Depersonalizasyon: kendi bedenine yabancılaşma",
                "Özdenetimini yitirip çıldırma ve ölüm korkusu"
            ]
        },
        {
            "cumle": "k2-55-c0045", "bas": 0, "son": 5, "sayfa": 11,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Tanı Kriterleri",
            "ogeler": [
                "Yineleyen beklenmedik panik atakları",
                "Kardinal belirtilerden en az dördü",
                "En az bir ay süren kaygı veya kaçınma"
            ]
        },
        {
            "cumle": "k2-55-c0050", "bas": 0, "son": 5, "sayfa": 12,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Tıbbi Ayırıcı Tanı",
            "ogeler": [
                "Hipertiroidizm ve feokromositoma taraması",
                "Paroksismal aritmiler ve mitral prolapsus",
                "Alkol kesilmesi ve kafein intoksikasyonu"
            ]
        },
        {
            "cumle": "k2-55-c0059", "bas": 0, "son": 5, "sayfa": 14,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Farmakoterapi Seçenekleri",
            "ogeler": [
                "Seçici serotonin geri alım inhibitörleri",
                "Venlafaksin ve serotonin noradrenalin",
                "İlk haftalarda kısa süreli alprazolam köprüsü"
            ]
        },
        {
            "cumle": "k2-55-c0068", "bas": 0, "son": 5, "sayfa": 16,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Agorafobi Özellikleri",
            "ogeler": [
                "Kaçmanın güç olacağı ortamlardan korkma",
                "Olguların dörtte üçünde panik bozukluk birlikteliği",
                "Travmatik bir yaşam olayı ile tetiklenme"
            ]
        },
        {
            "cumle": "k2-55-c0073", "bas": 0, "son": 5, "sayfa": 17,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Agorafobi Tanı Alanları",
            "ogeler": [
                "Toplu taşıma araçlarını kullanma korkusu",
                "Açık alanlar ve kapalı mekanlarda bulunma",
                "Sırada bekleme ya da tek başına ev dışı kalma"
            ]
        },
        {
            "cumle": "k2-55-c0091", "bas": 0, "son": 5, "sayfa": 22,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Fobik Bozukluk Sınıflaması",
            "ogeler": [
                "Özgül fobi: belirli nesne ve durumlardan korkma",
                "Sosyal fobi: toplumsal ortamlarda küçük düşme",
                "Gerçek tehditle orantısız ve aşırı korku"
            ]
        },
        {
            "cumle": "k2-55-c0106", "bas": 0, "son": 5, "sayfa": 26,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Kan-Enjeksiyon Fobisi",
            "ogeler": [
                "Diğer tüm fobilerden farklı bifazik tepki",
                "Kısa süreli taşikardiyi derin bradikardi izler",
                "Vazovagal senkop ve bayılma gelişir"
            ]
        },
        {
            "cumle": "k2-55-c0115", "bas": 0, "son": 5, "sayfa": 29,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Özgül Fobide Tedavi",
            "ogeler": [
                "Etkinliği kanıtlanmış hiçbir psikotropik ilaç yoktur",
                "Bilişsel davranışçı terapi tartışmasız altın standart",
                "Aşamalı yüzleştirme ve maruz bırakma protokolü"
            ]
        },
        {
            "cumle": "k2-55-c0147", "bas": 0, "son": 5, "sayfa": 37,
            "tur": "sema", "sablon": "siniflama",
            "baslik": "Sosyal Fobide Sağaltım",
            "ogeler": [
                "Yaygın tip: düzenli serotonin geri alım ilaçları",
                "Performans kaygısı: durumsal beta bloker propranolol",
                "Kalıcı düzelme için bilişsel davranışçı terapi"
            ]
        }
    ]

    # Write files
    (TASLAK / "konusma_v2.json").write_text(json.dumps(clean_k2, ensure_ascii=False, indent=2), encoding="utf-8")
    (TASLAK / "cizim_aday.json").write_text(json.dumps({"komutlar": drawings}, ensure_ascii=False, indent=2), encoding="utf-8")

    sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
    import konusma_v2 as KV
    md_txt, sayfalar_l = KV.turet(clean_k2)
    (TASLAK / "konusma_metni.md").write_text(md_txt, encoding="utf-8")
    (TASLAK / "konusma_sayfalari.json").write_text(json.dumps(sayfalar_l), encoding="utf-8")
    (TASLAK / "konusma_capalari.json").write_text(json.dumps(KV.capalar(clean_k2), ensure_ascii=False), encoding="utf-8")
    
    print("Files successfully written to taslak.")
    
    # Run all quality gates
    print("\n--- Running Quality Gate 1: KV.dogrula ---")
    kv_errs = KV.dogrula(clean_k2, KV.kaynak_sayfa(TASLAK), KV.kaynak_metin(TASLAK))
    if kv_errs:
        print(f"FAILED KV.dogrula with {len(kv_errs)} errors:")
        for e in kv_errs[:10]: print(" ", e)
        sys.exit(1)
    print("PASSED KV.dogrula: 0 HATA")
    
    print("\n--- Running Quality Gate 2: denetle.py ---")
    sys.path.insert(0, str(REPO_ROOT / "meds/scripts/ders_isci"))
    import denetle as D
    d_rapor = D.Denetim(TASLAK).calistir()
    if d_rapor.get("hata", 0) > 0:
        print(f"FAILED denetle.py with {d_rapor.get('hata')} errors:")
        for e in d_rapor.get("hatalar", [])[:10]: print(" ", e)
        sys.exit(1)
    print("PASSED denetle.py: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 3: validate_learning_decks.py ---")
    import subprocess
    r_deck = subprocess.run([
        sys.executable, str(REPO_ROOT / "meds/scripts/validate_learning_decks.py"),
        str(TASLAK / "deck.json"), "--oyun-zorunlu", "--kurul2"
    ], capture_output=True, text=True)
    if r_deck.returncode != 0:
        print("FAILED validate_learning_decks:", r_deck.stdout, r_deck.stderr)
        sys.exit(1)
    print("PASSED validate_learning_decks: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 4: metin_denetle.py ---")
    r_metin = subprocess.run([
        sys.executable, str(REPO_ROOT / "meds/scripts/sesli_anlatim/metin_denetle.py"),
        str(TASLAK / "konusma_metni.md")
    ], capture_output=True, text=True)
    if r_metin.returncode != 0:
        print("FAILED metin_denetle:", r_metin.stdout, r_metin.stderr)
        sys.exit(1)
    print("PASSED metin_denetle: 0 HATA · 0 UYARI")
    
    print("\n--- Running Quality Gate 5: sesli_kapsam ---")
    import isle as IS
    kapsam_errs = IS.sesli_kapsam(TASLAK)
    if kapsam_errs:
        print(f"FAILED sesli_kapsam with {len(kapsam_errs)} errors:")
        for e in kapsam_errs: print(" ", e)
        sys.exit(1)
    print("PASSED sesli_kapsam: 0 HATA")
    
    print("\n--- Running Quality Gate 6: cizim_dogrula.py ---")
    sys.path.insert(0, str(REPO_ROOT / "meds/scripts/cizim"))
    import cizim_dogrula as CD
    import sablon
    cum_text = {}
    accum = []
    for s in sents:
        accum.append(s["ses"])
        cum_text[s["id"]] = " ".join(accum)
    sent_map = {s["id"]: s for s in sents}
    c_errs = []
    for idx, d in enumerate(drawings):
        cid = d["cumle"]
        coz_d, err_c = sablon.coz(d)
        if err_c:
            c_errs.append(f"Drawing {idx+1} coz error: {err_c}")
            continue
        s_words = len(sent_map[cid]["ses"].split())
        err_v = CD.denetle(coz_d, s_words, [], None, cum_text[cid])
        if err_v:
            c_errs.append(f"Drawing {idx+1} ({cid}) error: {err_v}")
    if c_errs:
        print(f"FAILED cizim_dogrula with {len(c_errs)} errors:")
        for e in c_errs: print(" ", e)
        sys.exit(1)
    print(f"PASSED cizim_dogrula: {len(drawings)}/{len(drawings)} KOMUT 0 HATA")

if __name__ == "__main__":
    main()
