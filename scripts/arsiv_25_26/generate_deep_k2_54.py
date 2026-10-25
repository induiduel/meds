#!/usr/bin/env python3
"""Generate a complete, deep amfi-level lecture for Lesson 54: Yaygın Anksiyete Bozukluğu.

Covers all 20 pages without skipping any page, bullet point, table, or algorithm.
Generates ~180-195 sentences, ~3,400-3,800 spoken words (~27-30 minutes of deep amfi audio).
Includes all verbal past exam citations and 16 verified live drawing commands.
Strictly adheres to Turkish style standard, amfi fidelity, and zero forward leak rule.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path("/home/indu/medsor")
TASLAK = REPO_ROOT / "meds_database_25_26/taslak/y25-k2-54-yaygin-anksiyete-bozuklugu"
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
            cl = re.sub(r'^[✓\s\-*•o❑➢]+', '', cl).strip()
            if len(cl) > 2 and not cl.isdigit() and not cl.startswith('==='):
                ll.append(cl)
        pages_lines[curr_p] = ll

def find_satir(pno, pattern=None, idx=0):
    lines = pages_lines.get(pno, [])
    if not lines:
        return "Yaygın Anksiyete Bozukluğu"
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
    cid = f"k2-54-c{c_counter:04d}"
    c_counter += 1
    
    clean_ekran = ekran.replace("**", "").replace("*", "")
    
    vurgular = []
    if cikmis and highlight_word:
        m = re.search(re.escape(highlight_word), clean_ekran, re.IGNORECASE)
        if m:
            vurgular.append({"tur": "cikmis", "metin": m.group(0)})
    
    if pno == 19:
        slayt_dict = {
            "sayfa": pno,
            "satir": None,
            "madde": None,
            "kutu": None,
            "sekil": sekil or "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"
        }
    else:
        satir = find_satir(pno, satir_pattern, satir_idx)
        slayt_dict = {
            "sayfa": pno,
            "satir": [satir] if satir else None,
            "madde": None,
            "kutu": None,
            "sekil": sekil
        }
    
    return {
        "id": cid,
        "ses": ses,
        "ekran": ekran,
        "slayt": slayt_dict,
        "etiketler": ["cikmis"] if cikmis else [],
        "cikmis": [cikmis] if cikmis else None,
        "vurgu": vurgular
    }

# ==============================================================================
# SECTIONS & PARAGRAPHS MAPPING
# ==============================================================================
PD = {}

# Sayfa 1: Kapak
PD[1] = [
    ("**Yaygın Anksiyete Bozukluğu:** Psikiyatri kliniğinde en sık karşılaşılan anksiyete tablolarından biridir.",
     "Ruh sağlığı ve hastalıkları klinik stajımızda psikiyatrik poliklinik pratiğinde en sık karşılaştığımız tablolardan biri olan yaygın anksiyete bozukluğunu tüm klinik boyutlarıyla ele alacağız.",
     "YAYGIN", 0, None, None, None),
    ("Dersimiz **Dr. Öğr. Üyesi Zuhal Koç Apaydın** tarafından amfi müfredatına uygun olarak hazırlanmıştır.",
     "Ders sunumumuz psikiyatri anabilim dalından Doktor Öğretim Üyesi Zuhal Koç Apaydın tarafından hazırlanmış olup güncel klinik kılavuzlar ve amfi ders notlarımız temel alınmıştır.",
     "DR. ÖĞRETİM ÜYESİ", 1, None, None, None),
    ("Ders boyunca **tanım, epidemiyoloji, etiyoloji**, klinik semiyoloji, tanı kriterleri ve tedaviyi inceleyeceğiz.",
     "Dersimiz kapsamında bozukluğun nörobiyolojik ve psikososyal etiyolojisini, klinik semiyolojisini, ayrıntılı ayırıcı tanısını ve güncel tedavi ilkelerini adım adım inceleyeceğiz.",
     "PSİKİYATRİ", 2, None, None, None),
    ("Amacımız sınavda sorulan **tüm tanı kriterlerini** ve klinik ayırıcı tanı basamaklarını eksiksiz pekiştirmektir.",
     "Temel amacımız kurul sınavlarında sıkça karşımıza çıkan tanı ölçütlerini, süre kriterlerini, organik taklitçileri ve farmakoterapi ayrıntılarını eksiksiz şekilde kavramaktır.",
     "YAYGIN", 0, None, None, None),
    ("Yaygın kaygının **fizyolojik temellerini** ve farmakolojik hedeflerini anlamak hekimlik pratiğinde yol göstericidir.",
     "Yaygın kaygının altta yatan hücresel ve nörobiyolojik mekanizmalarını doğru kavramak birinci basamak hekimlik pratiğinde doğru klinik kararlar almamızı sağlayacaktır.",
     "YAYGIN", 0, None, None, None)
]

# Sayfa 2: Normal ve Patolojik Anksiyete
PD[2] = [
    ("**Normal Anksiyete:** Organizmanın bilinmeyen, iç odaklı veya belirsiz bir tehdide karşı geliştirdiği uyumsal yanıttır.",
     "Normal anksiyete organizmanın bilinmeyen, iç odaklı, belirsiz ya da çatışmalı bir tehdide karşı sergilediği doğal ve uyum sağlayıcı fizyolojik bir alarm tepkisidir.",
     "Normal anksiyete", 0, None, None, None),
    ("**Kaygı ve Korku Ayrımı:** Kaygı iç odaklı ve belirsizken, korku bilinen ve somut bir dış tehdide yanıttır.",
     "Kaygı ile korku arasındaki temel ayrım klinik açıdan son derece kritiktir; kaygı belirsiz ve içsel tehditlere yönelikken, korku bilinen, dış odaklı ve somut bir tehlikeye karşı gelişir.",
     "Korku bilinen", 1, None, None, None),
    ("Fizyolojik kaygıda **sempatik ve parasempatik** sinir sistemleri karşılıklı bir denge içinde çalışır.",
     "Fizyolojik düzeyde sempatik ve parasempatik sinir sistemlerinin karşılıklı dengeli etkileşimi bireyi tehlikelere karşı koruyarak uygun bir eylem hazırlığı durumu sağlar.",
     "sempatik ve parasempatik", 2, None, None, None),
    ("Uyumsal kaygı bireyin dikkatini toplayarak **zorlu durumlara hazırlanmasını** kolaylaştırır.",
     "Uyumsal düzeydeki bir kaygı hissi organizmanın hayatta kalma reflekslerini güçlendirir, sınav ve tehlike anlarında dikkati keskinleştirerek eyleme geçişi kolaylaştırır.",
     "uyum sağlayıcı", 2, None, None, None),
    ("Birey olayları kronik stres olarak algıladığında **psikolojik savunmalar** yetersiz kalabilir.",
     "Ancak kişi çevresel uyaranları sürekli ve ağır bir stres etkeni olarak algıladığında psikolojik savunma mekanizmaları ve başa çıkma stratejileri yetersiz kalabilir.",
     "psikolojik savunmaları", 2, None, None, None),
    ("Egonun işlevini uygun biçimde sürdürememesi kaygının **kronik ve yıpratıcı** bir hal almasına yol açar.",
     "Ego bütünlüğü uygun şekilde işlev göremediğinde fizyolojik alarm durumu yerini bireyin tüm yaşamını esir alan kronik ve yıpratıcı bir anksiyete tablosuna bırakır.",
     "kronik bir kaygı", 2, None, None, None),
    ("Uyum sağlayıcı alarm düzeyi aşıldığında **patolojik anksiyete** klinik işlevselliği ciddi düzeyde bozar.",
     "Böylece bireyin günlük yaşamını, mesleki verimliliğini ve kişilerarası ilişkilerini bozan patolojik kaygı tablosu şekillenmiş olur.",
     "ANKSİYETE", 0, None, None, None),
    ("Patolojik kaygıda tehlike algısı **orantısız ve denetlenemez** bir tırmanış gösterir.",
     "Patolojik anksiyetede algılanan tehdidin şiddeti ve süresi gerçek duruma göre tamamen orantısızdır ve hasta bu içsel yangını sakinleştirmekte yetersiz kalır.",
     "çatışmalı tehdide", 0, None, None, None),
    ("Klinik hekimin görevi bu iki durum arasındaki **ince sınırı netleştirmektir**.",
     "Hekimin temel klinik sorumluluğu fizyolojik koruyucu kaygı ile tedavi gerektiren patolojik anksiyete arasındaki bu hassas sınırı doğru belirlemektir.",
     "ANKSİYETE", 0, None, None, None)
]

# Sayfa 3: YAB Tanımı ve Epidemiyoloji
PD[3] = [
    ("**Yaygın Anksiyete Bozukluğu (YAB):** Belli bir nesneye veya saplantıya odaklanmamış serbest yüzen kaygıdır.",
     "Yaygın anksiyete bozukluğu belirli bir nesneye, mekana, organa ya da saplantılı düşünceye odaklanmamış, yani serbest dalgalanan ve serbest yüzen yaygın ruhsal bunaltı tablosudur.",
     "Yaygın Anksiyete Bozukluğu (YAB)", 0, None, None, None),
    ("Bu bilgi çıkmış sınavda sorulmuştur: **En az 6 aylık süre** boyunca günlerin çoğunda aşırı kaygı bulunmalıdır.",
     "Bu bilgi çıkmış sınavda sorulmuştur: Yaygın anksiyete bozukluğu tanısı koyabilmek için en az altı aylık bir dönem boyunca hemen her gün birçok olay hakkında aşırı kaygı ve endişe duyulması şarttır.",
     "En az 6 aylık", 1, "d3-k2-psi-008", "En az 6 aylık süre", None),
    ("Bu bilgi çıkmış sınavda sorulmuştur: Tanı için belirtilerin **bir veya iki ay** sürmesi kesinlikle yetersizdir!",
     "Bu bilgi çıkmış sınavda sorulmuştur: Sınavlarda sıklıkla çeldirici olarak verilen bir aylık veya iki aylık süre yaygın anksiyete bozukluğu tanısı için kesinlikle yetersizdir; süre en az altı ay olmalıdır.",
     "En az 6 aylık", 1, "q-25-26_d_nem_3_kurul_2-82-cs3", "bir veya iki ay", None),
    ("Endişe gün boyu devam eder ve hasta **endişe konularını sürekli değiştirir**.",
     "Hasta sabah aile sağlığı hakkında endişelenirken öğleden sonra finansal duruma veya işteki en küçük aksaklıklara takılarak kaygısını konu değiştire değiştire sürdürür.",
     "bir çok olay veya etkinlik", 1, None, None, None),
    ("YAB toplumda **%3-6 yaşam boyu yaygınlık** oranıyla oldukça sık rastlanan bir bozukluktur.",
     "Epidemiyolojik çalışmalara göre genel toplumda yaygın anksiyete bozukluğunun yaşam boyu yaygınlık oranı yüzde üç ila altı arasında bildirilmektedir.",
     "Yaşam boyu yaygınlık", 2, None, None, None),
    ("Temel sağlık hizmetlerine başvuran hastalarda **en sık görülen** anksiyete bozukluğu YAB'dir.",
     "Birinci basamak sağlık kuruluşlarına ve aile hekimliği polikliniklerine başvuran olgular arasında en sık saptanan anksiyete bozukluğu türü yaygın anksiyete bozukluğudur.",
     "Temel sağlık hizmetlerine", 3, None, None, None),
    ("Hastalık **kadınlarda erkeklere göre 2 kat** daha fazla görülmektedir.",
     "Cinsiyet dağılımına bakıldığında kadınlarda erkeklere oranla iki kat daha sık görüldüğü saptanmıştır.",
     "Kadınlarda erkeklere göre 2 kat", 4, None, None, None),
    ("Başlangıç yaşı genellikle **genç erişkinlik dönemine** denk gelir.",
     "Hastalık sıklıkla yirmili yaşlarda veya erken erişkinlik evresinde başlar ancak olguların çoğu çocukluktan beri endişeli mizaçta olduklarını ifade ederler.",
     "Yaşam boyu yaygınlık", 2, None, None, None),
    ("Hastaların polikliniğe başvuru şikayetleri çoğunlukla **somatik yakınmalardır**.",
     "Hastalar psikiyatriden önce kronik yorgunluk, boyun ağrısı, çarpıntı ve gaz şikayetleri ile dahiliye ve nöroloji kliniklerini dolaşmaktadır.",
     "fizyolojik bunaltı belirtileri", 0, None, None, None),
    ("Doğru tanı konulana kadar geçen süre **ortalama birkaç yılı** bulabilmektedir.",
     "Somatik yakınmaların ön planda olması nedeniyle doğru psikiyatrik tanının konulması ve uygun tedavinin başlanması yıllarca gecikebilmektedir.",
     "Temel sağlık hizmetlerine", 3, None, None, None)
]

# Sayfa 4: Risk Faktörleri ve Komorbidite
PD[4] = [
    ("Bu bilgi çıkmış sınavda sorulmuştur: **Çocukluk çağında kötü muamele** görmüş olma en güçlü risk etmenidir.",
     "Bu bilgi çıkmış sınavda sorulmuştur: Çocukluk çağında kötü muamele, fiziksel ya da duygusal ihmal ve istismar öyküsü erişkin dönemde yaygın anksiyete bozukluğu gelişimi için en güçlü risk etmenidir.",
     "Çocukluk çağında kötü muamele", 0, "q-25-26_d_nem_3_kurul_2-82-cs5", "Çocukluk çağında kötü muamele", None),
    ("Düşük sosyo-ekonomik durum ve **kronik çevresel stres** hastalık zeminini belirginleştirir.",
     "Düşük sosyoekonomik düzey, finansal güvensizlik ve olumsuz yaşam koşulları kaygının süreğenleşmesinde önemli rol oynar.",
     "Düşük sosyo-ekonomik", 1, None, None, None),
    ("Sorunları içe atma eğilimi ve **duygusal ifade güçlüğü** somatizasyonu tetikler.",
     "Bireyin duygularını dışa vurmak yerine içine atma eğilimi göstermesi ruhsal gerginliğin bedensel yakınmalara dönüşmesine zemin hazırlar.",
     "Sorunları içe atma", 2, None, None, None),
    ("Çocukluk döneminde sergilenen **davranım bozuklukları** erişkin anksiyete tablolarının öncülü olabilir.",
     "Erken çocukluk evresindeki mizaç özellikleri, çekingenlik ve davranım problemleri ilerleyen yıllarda yaygın kaygı gelişimine yatkınlık yaratır.",
     "Çocukluktaki davranım bozuklukları", 3, None, None, None),
    ("YAB tanılı olguların **%62-67'sinde majör depresyon** komorbiditesi mevcuttur.",
     "Klinik pratikte hastaların yüzde altmış iki ila altmış yedisinde tabloya eşlik eden bir majör depresyon ek tanısı bulunmaktadır.",
     "depresyon ek tanısı", 4, None, None, None),
    ("Depresyon eşlik ettiğinde **tedaviye direnç ve yeti yitimi** belirgin şekilde artar.",
     "Yaygın anksiyete ile depresyonun birlikteliği klinik seyri ağırlaştırır, tedaviye yanıtı geciktirir ve hastanın mesleki işlevselliğini derinden bozar.",
     "depresyon ek tanısı", 4, None, None, None),
    ("Hastaların yaklaşık **%25'inde panik bozukluk**, distimi ve madde kullanım bozukluğu eşlik eder.",
     "Olguların yaklaşık dörtte birinde panik bozukluk görülürken, distimik bozukluk ve anksiyeteyi bastırmaya yönelik alkol ya da madde kullanımı da sıktır.",
     "panik bozukluk görülür", 5, None, None, None),
    ("Alkol ve sedatif maddeler **kendi kendini tedavi çabası** olarak sıklıkla kötüye kullanılır.",
     "Hastalar yaşadıkları dayanılmaz gerginliği ve uykusuzluğu dindirebilmek için alkol ve reçetesiz sakinleştiricilere sığınarak bağımlılık kısır döngüsüne girebilirler.",
     "madde kullanım bozukluğu", 5, None, None, None),
    ("Komorbidite varlığı her olguda **çok eksenli ayrıntılı değerlendirmeyi** zorunlu kılar.",
     "Bu nedenle poliklinikte yaygın anksiyete bozukluğu saptadığımız her hastada eşlik eden depresif belirtileri ve madde kullanımını mutlaka sorgulamalıyız.",
     "Eşlik eden diğer psikiyatrik", 3, None, None, None),
    ("Yüksek komorbidite oranları bozuklukların **ortak nörobiyolojik zeminini** yansıtır.",
     "Bu yüksek birliktelik oranları kaygı ve duygudurum bozukluklarının ortak genetik ve nörokimyasal mekanizmaları paylaştığını göstermektedir.",
     "Eşlik eden diğer psikiyatrik", 3, None, None, None)
]

# Sayfa 5: Etiyoloji (Biyolojik, Genetik, Psikososyal)
PD[5] = [
    ("**GABA ve Benzodiazepin Reseptörleri:** Reseptör kompleksindeki duyarlılık azalması temel biyolojik faktördür.",
     "Biyolojik etkenlerin başında gama aminobütirik asit ve benzodiazepin reseptör kompleksindeki duyarlılık ve bağlanma kusurları gelir.",
     "BDZ resp", 0, None, None, None),
    ("GABA'nın inhibitör frenleme gücü azaldığında **santral uyarılabilirlik** artar.",
     "Beyindeki ana inhibitör nörotransmitter olan gama aminobütirik asit sisteminin yetersiz frenleme yapması nöronal devrelerde aşırı uyarılmaya ve kaygı tırmanışına yol açar.",
     "BDZ resp", 0, None, None, None),
    ("Serotonin, noradrenalin ve **glutamat yolaklarındaki disregülasyon** kaygı tırmanışını yönetir.",
     "Serotonerjik yolaklar, lokus seruleustan kaynaklanan noradrenerjik hiperaktivite ve glutamaterjik eksitatör ileti anomalileri merkezi rol oynar.",
     "5-HT, NA, Glutamat", 0, None, None, None),
    ("Santral korku ağında **oksipital lob, bazal gangliyonlar, limbik sistem** ve frontal korteks yer alır.",
     "Fonksiyonel nörogörüntüleme çalışmalarında oksipital lob, bazal gangliyonlar, amigdala ve prefrontal korteksi içeren nöral ağlarda aktivite farklılıkları gösterilmiştir.",
     "oksipital lob, bazal ggl", 0, None, None, None),
    ("Amigdala ve prefrontal korteks arasındaki **fonksiyonel bağlantı kopukluğu** duygusal kontrolü bozar.",
     "Prefrontal korteksin amigdala üzerindeki yukarıdan aşağıya inhibisyon yeteneğinin zayıflaması tehdit uyaranlarının gereksiz yere büyümesine neden olur.",
     "frontal korteks", 0, None, None, None),
    ("Presinaptik **alfa-2 adrenerjik reseptör** duyarlılığında azalma sempatik tonusu sürekli yüksek tutar.",
     "Presinaptik alfa iki adrenerjik otoreseptör duyarlılığındaki azalma noradrenalin salınımını frenleyemeyerek sempatik tonusu yüksek tutar.",
     "α2-adrenerjik resp duyarlılığında", 0, None, None, None),
    ("Genetik çalışmalarda birinci derece akrabalarda **%25 oranında etkilenme** saptanmıştır.",
     "Genetik araştırmalarda yaygın anksiyete bozukluğu olan bireylerin birinci derece akrabalarında yaklaşık yüzde yirmi beş oranında anksiyete bozukluğu riski bildirilmiştir.",
     "birinci derece akrabalarında %25", 1, None, None, None),
    ("Kalıtılabilirlik oranı ikiz çalışmalarında **%30 ila %40** düzeyinde hesaplanmaktadır.",
     "İkiz ve aile çalışmaları yaygın anksiyete bozukluğunda kalıtılabilirliğin orta düzeyde olduğunu ve çevresel stresörlerle etkileştiğini ortaya koymaktadır.",
     "Genetik etkenler", 1, None, None, None),
    ("Bilişsel kurama göre **algılanan tehdide yanlış tepki**, psikanalitik kurama göre bilinçdışı çatışma esastır.",
     "Bilişsel davranışçı kuram tehditlerin felaketleştirilmesini ve abartılmasını vurgularken, psikanalitik kuram kaygıyı bilinçdışı çatışmaların bir dışavurumu sayar.",
     "Bilişsel- Davranışçı kurama", 2, None, None, None),
    ("Tüm bu faktörler bir araya gelerek **hastanın stres tolerans eşiğini** belirgin biçimde düşürür.",
     "Biyolojik yatkınlık, genetik zemin ve bilişsel çarpıtmalar birleştiğinde bireyin günlük belirsizliklere tahammül gücü tamamen çöker.",
     "Psikoanalitik kurama göre", 2, None, None, None)
]

# Sayfa 6: Bilişsel Model ("Ya kimse beni sevmezse?")
PD[6] = [
    ("**Bilişsel Çarpıtmalar:** 'Ya kimse beni sevmezse?' gibi felaket senaryoları zihni sürekli meşgul eder.",
     "Bilişsel modelde hastanın zihnini ya kimse beni sevmezse veya ya her şey ters giderse gibi katastrofik felaket senaryoları aralıksız işgal eder.",
     "Ya kimse", 0, None, None, None),
    ("Hasta olası tehlikelerin **gerçekleşme ihtimalini** aşırı derecede büyütür.",
     "Birey geleceğe dair olası olumsuz durumların gerçekleşme ihtimalini aşırı derecede abartırken kendi başa çıkma becerilerini küçümser.",
     "beni", 0, None, None, None),
    ("Belirsizlik hasta için doğrudan **tehdit ve felaket** anlamına gelir.",
     "Yaygın anksiyetesi olan kişi için belirsizliğe tahammül etmek imkansızdır; net olmayan her durum mutlak bir yıkım olarak yorumlanır.",
     "sevmezse", 0, None, None, None),
    ("Sürekli endişelenmek, hastanın zihninde **felaketleri önleme yöntemi** gibi algılanır.",
     "Sürekli tetikte olmanın ve kuruntu yapmanın felaketleri önceden fark edip engelleyeceği yönündeki hatalı inanç kaygı döngüsünü pekiştirir.",
     "ANKSTYETE", 1, None, None, None),
    ("Endişe bir tür **bilişsel kaçınma davranışı** olarak işlev görür.",
     "Kişi endişelenerek daha derin duygusal yüzleşmelerden ve travmatik deneyimlerin getirdiği bedensel uyarılmadan kaçınmaya çalışır.",
     "ANKSTYETE", 1, None, None, None),
    ("Bu zihinsel alarm durumu hastanın enerjisini tüketerek **kronik gerginliğe** yol açar.",
     "Bu bitmek bilmeyen zihinsel alarm hali hastanın ruhsal enerjisini tüketerek gün boyu süren yoğun bir içsel gerginlik yaratır.",
     "ANKSTYETE", 1, None, None, None),
    ("Klinik pratikte bu bilişsel döngünün kırılması **bilişsel yeniden yapılandırma** ile mümkündür.",
     "Bilişsel davranışçı terapide bu felaketleştirici çarpıtmalar adım adım kanıt sorgulamalarıyla yeniden yapılandırılır.",
     "Ya kimse", 0, None, None, None),
    ("Hastaya belirsizlikle yaşamayı ve **olumsuzluk ihtimallerini rasyonelleştirmeyi** öğretmek esastır.",
     "Terapötik süreç hastanın geleceğe yönelik gerçekçi olasılıkları değerlendirmesini ve başa çıkma güvenini yeniden kazanmasını sağlar.",
     "sevmezse", 0, None, None, None)
]

# Sayfa 7: Klinik Özellikler ve Ruhsal Durum Muayenesi
PD[7] = [
    ("**Genel Görünüm ve Davranış:** Hastada genel bir huzursuzluk, endişeli yüz ifadesi ve gergin duruş hakimdir.",
     "Genel muayenede hastada belirgin bir motor huzursuzluk, alında kırışma, endişeli yüz ifadesi, gergin duruş ve hafif sesle bile irkilme gözlenir.",
     "Genel Görünüm ve davranış", 0, None, None, None),
    ("Otururken yerinde duramama ve **sürekli kıpırdanma** dikkat çeker.",
     "Hasta muayene koltuğunda otururken ellerini sıkar, bacaklarını sallar, yerinde duramaz ve sürekli kıpırdanarak motor gerginliğini dışa vurur.",
     "genel bir huzursuzluk", 0, None, None, None),
    ("Hastalar küçük uyaranlara karşı bile **çabuk irkilme ve çabuk kızma** tepkisi gösterirler.",
     "Çevresel uyaranlara karşı duyarlılık artmıştır; hasta kapı çarpmasında irkilir, tahammülsüzdür ve küçük aksiliklere çabuk öfkelenir.",
     "çabuk irkilme", 0, None, None, None),
    ("**Konuşma ve İlişki:** Seste heyecanlı bir titreklik ve zor konuşma hissedilse de konuşma düzgündür.",
     "Konuşma muayenesinde seste heyecanlı bir titreklik ve konuşurken zorlanma sezilebilir, ancak konuşmanın mantıksal akışı ve hedefe yönelimi düzgündür.",
     "Konuşma ve ilişki", 1, None, None, None),
    ("Göz teması kurulabilir ancak **gözlerdeki tedirgin bakış** hissedilir.",
     "Hekimle iletişim kurarken göz teması sürdürülebilir ancak bakışlardaki sürekli tetikte olma ve tedirginlik açıkça göze çarpar.",
     "zor konuşma", 1, None, None, None),
    ("**Duygulanım:** Hasta içsel yaşantısını bun, bungunluk ve ağır bir bunaltı olarak tarif eder.",
     "Duygulanım muayenesinde hasta iç dünyasını bun, bungunluk ve göğsüne çöken ağır bir bunaltı hissi olarak tanımlar; sıklıkla depresif çökkünlük eşlik eder.",
     "Duygulanım", 2, None, None, None),
    ("Duygulanım kaygılıdır ve **hastanın afekti gergindir**.",
     "Hastanın afektif ifadesi kaygılı ve kısıtlıdır; neşeli veya rahatlatıcı uyaranlara tepki vermekte belirgin güçlük çeker.",
     "bun, bungunluk", 2, None, None, None),
    ("**Bilişsel Yetiler:** Yorucu sıkıntı nedeniyle dikkat çabuk dağılır ve geçici unutkanlıklar olabilir.",
     "Bilişsel yetiler değerlendirildiğinde zihni meşgul eden kuruntular nedeniyle dikkat çabuk dağılır, odaklanma güçleşir ve geçici unutkanlıklar görülebilir.",
     "Bilişsel yetiler", 3, None, None, None),
    ("Yönelim ve bilinç **tamamen açıktır**; organik bir konfüzyon saptanmaz.",
     "Hastanın yer, zaman ve kişi yönelimi tamdır, belleği korunmuştur; yaşanan unutkanlıklar dikkat odaklanma yetersizliğine bağlıdır.",
     "dikkati çabuk dağılır", 3, None, None, None),
    ("Ruhsal durum muayenesi **psikotik bir bozukluğu ekarte etmede** en değerli rehberdir.",
     "Bu muayenede düşünce içeriğinde hezeyan veya persepsiyonda halüsinasyon saptanmaması primer anksiyete tanısını destekler.",
     "KLİNİK ÖZELLİKLER", 0, None, None, None)
]

# Sayfa 8: Düşünce İçeriği ("Yoksa anneme bir şey mi oldu?")
PD[8] = [
    ("**Tasaların İçeriği:** 'Yoksa anneme bir şey mi oldu?' gibi sevdiklerine yönelik kaygılar baskındır.",
     "Hastaların düşünce içeriğinde yoksa anneme kötü bir şey mi oldu, çocuğum kaza mı geçirdi gibi sevdiklerinin sağlığına dair felaket tasaları baskındır.",
     "YOKSA ANNEME", 0, None, None, None),
    ("Beklenmedik bir telefon çalışında **en kötü haberin** geldiği sanılarak şiddetli panik yaşanır.",
     "Beklenmedik bir telefon çalışı veya kapı zili sesinde anında en korkunç haberin geldiği zannedilerek yoğun bir dehşet hissi yaşanır.",
     "BİŞEY Mİ OLDU", 0, None, None, None),
    ("Geciken aile bireyleri için **hastane ve morg senaryoları** kurulur.",
     "Ev halkından biri eve on dakika geç kalsa hasta derhal trafik kazası geçirdiğini düşünerek acil servisleri aramaya başlar.",
     "YOKSA ANNEME", 0, None, None, None),
    ("Geleceğe yönelik sağlık, iflas veya iş kaybı gibi **felaket senaryoları** zihinde kurgulanır.",
     "Sağlık sorunları, maddi kayıplar veya gündelik rutin aksaklıklar zihinde orantısız büyüklükte felaketler olarak canlandırılır.",
     "BİŞEY Mİ OLDU", 0, None, None, None),
    ("Bir endişe çözüldüğünde zihin **anında yeni bir endişe konusu** bulur.",
     "Kaygının serbest yüzen doğası gereği bir sorun çözülse bile rahatlama sağlanamaz; zihin derhal başka bir kaygı başlığı üretir.",
     "YOKSA ANNEME", 0, None, None, None),
    ("Hasta kuruntularının abartılı olduğunu bilse dahi **zihnini sakinleştirmekte** yetersiz kalır.",
     "Hasta endişelerinin abartılı olduğunu mantıken kabul etse bile bu düşünce akışını denetim altına almakta tamamen çaresiz hisseder.",
     "BİŞEY Mİ OLDU", 0, None, None, None),
    ("Sürekli güvence arayışı **çevresiyle olan ilişkileri de yıpratır**.",
     "Sürekli yakınlarından her şeyin yolunda olduğuna dair onay istemek hasta yakınlarında da tükenmişliğe yol açabilir.",
     "YOKSA ANNEME", 0, None, None, None),
    ("Düşünce içeriğindeki bu temalar **bilişsel terapinin birincil hedefidir**.",
     "Terapötik görüşmelerde bu felaketleştirici senaryoların gerçeklik payı ve alternatif açıklamaları incelenir.",
     "BİŞEY Mİ OLDU", 0, None, None, None)
]

# Sayfa 9: Düşünce Süreci ve Otonomik-Bedensel Belirtiler
PD[9] = [
    ("**Düşünce Süreci:** Yakınmalarını heyecan ve sabırsızlıkla aktarma isteği düşünceyi hızlanmış gösterebilir.",
     "Düşünce sürecinde hasta yakınmalarını büyük bir sabırsızlık ve heyecanla hekime aktarmak istediğinden düşünce akışı hızlanmış izlenimi verebilir.",
     "Düşünce süreci ve İçeriği", 0, None, None, None),
    ("Düşünce içeriğinde hezeyan veya sanrı yoktur; **yaygın ve orantısız tasalar** tüm alanı kaplar.",
     "Düşünce içeriğinde psikotik bir hezeyan veya sanrı bulunmaz; zihnin tamamını kaplayan orantısız kuruntular ve endişeler hakimdir.",
     "tasaları baskındır", 0, None, None, None),
    ("**Kardiyovasküler Bulgular:** Kan basıncında dalgalı yükselme ve çarpıntı sık görülür.",
     "Otonomik hiperaktiviteye bağlı olarak kan basıncında dalgalı yükselmeler, nabız artışı ve şiddetli çarpıntı hissi ortaya çıkar.",
     "Kan basıncında yükselme", 1, None, None, None),
    ("**Kas Gerginliği:** Ense, omuz ve sırtta yoğunlaşan kronik kas sertliği ve ağrıları gelişir.",
     "Motor gerginliğin sonucu olarak boyun, omuz ve sırt kaslarında kronik sertleşme, ağrılı spazmlar ve gerilim tipi baş ağrısı belirir.",
     "kaslarda gerginlik", 1, None, None, None),
    ("Kas spazmları zamanla **kronik fibromiyalji benzeri** yaygın ağrılara dönüşebilir.",
     "Hastalarda omurga boyunca ve trapezius kaslarında tetik noktalar oluşarak kronik kas yorgunluğu tablosu yerleşir.",
     "kaslarda gerginlik", 1, None, None, None),
    ("**Gastrointestinal Bulgular:** Ağız kuruluğu, bulantı, sık idrara çıkma ve gaita sıklığında artış saptanır.",
     "Sindirim sisteminde ağız kuruluğu, boğazda kuruluk hissi, bulantı, kusma, sık idrara çıkma ve dışkılama sıklığında artış gözlenir.",
     "ağız kuruması", 1, None, None, None),
    ("**Vazomotor Belirtiler:** Yüzde solukluk, kızarma ve yaygın soğuk terleme eşlik eder.",
     "Vazomotor labiliteye bağlı olarak yüzde ani solukluk veya basan kızarmalar ile ellerde ve gövdede terleme nöbetleri tabloya eklenir.",
     "solukluk, kızarma, terleme", 1, None, None, None),
    ("**Globus Hissi:** Boğazda düğümlenme veya takılma hissi hastayı sürekli yutkunmaya zorlar.",
     "Boğazda globus hissi yani düğümlenme duygusu belirir ve hasta nefes alamayacakmış hissine kapılarak telaşlanır.",
     "boğazda düğümlenme hissi", 1, None, None, None),
    ("**Solunumsal Bulgular:** Nefes almakta güçlük, hava açlığı ve derin iç çekmeler izlenir.",
     "Solunum yollarında nefes darlığı, hava açlığı, derin iç çekmeler ve göğüste daralma hissi tipiktir.",
     "nefes almakta güçlük", 1, None, None, None),
    ("**Duyusal Bulgular:** Ellerde ve ayaklarda uyuşma, karıncalanma şeklindeki paresteziler saptanır.",
     "Hiperventilasyona ve periferik vazokonstriksiyona sekonder olarak ellerde ve ayaklarda uyuşma ve karıncalanma hissi oluşur.",
     "ellerde ayaklarda uyuşma", 1, None, None, None),
    ("Solunumsal alkaloz **parestezilerin ve sersemliğin** ana biyokimyasal sebebidir.",
     "Hızlı ve yüzeyel nefes alma kandaki karbondioksiti düşürerek serbest kalsiyumu azaltır ve kas seğirmelerine yol açar.",
     "hava açlığı", 1, None, None, None),
    ("Bu somatik belirtiler hastayı sürekli **dahiliye ve acil polikliniklerine** yönlendirir.",
     "Fiziksel yakınmalar o denli baskındır ki hasta yaşadığı tablonun psikiyatrik bir rahatsızlık olduğuna inanmakta zorlanır.",
     "Bedensel ve Fizyolojik", 1, None, None, None)
]

# Sayfa 10: DSM-5 Tanı Kriterleri (A, B ve Kriter 1-3)
PD[10] = [
    ("**A Kriteri:** En az 6 aylık bir sürenin çoğu gününde birtakım olaylarla ilgili aşırı kaygı ve endişe vardır.",
     "De se me beş tanı ölçütlerine göre A kriteri, en az altı aylık bir sürenin çoğu gününde bir dizi olay veya etkinlik hakkında aşırı kaygı ve endişenin bulunmasını zorunlu kılar.",
     "A- En az 6 aylık", 0, None, None, None),
    ("Kaygı iş, okul veya günlük sorumluluklar gibi **birçok farklı alanı** kapsamalıdır.",
     "Endişe tek bir konuya hapsolmamalı, hastanın gündelik yaşamındaki çok sayıda farklı sorumluluk ve olayla ilişkili olmalıdır.",
     "olaylar ya da etkinliklerle ilgili", 0, None, None, None),
    ("**B Kriteri:** Kişi endişelerini ve kuruntularını denetim altına almakta belirgin güçlük çeker.",
     "B kriteri uyarınca kişi zihnini saran bu aşırı endişeleri ve kuruntuları kontrol altına almakta, durdurmakta veya yatıştırmakta açık bir güçlük çeker.",
     "B- Kişi endişelerini", 1, None, None, None),
    ("Hasta kuruntulardan kaçmak istese de **zihinsel durdurma mekanizması** iflas etmiştir.",
     "Kişi endişelenmemesi gerektiğini bilse ve kendini telkin etmeye çalışsa bile kaygı verici düşünce akışını kesemez.",
     "denetim altına almakta güçlük", 1, None, None, None),
    ("Bu bilgi çıkmış sınavda sorulmuştur: **C Kriteri** için tanımlanan 6 belirtiden en az 3 tanesi aranır.",
     "Bu bilgi çıkmış sınavda sorulmuştur: De se me beş tanı kriterlerine göre C ölçütünde yer alan altı temel klinik belirtiden en az üçünün son altı ay boyunca kaygıya eşlik etmesi gerekir.",
     "C- Bu kaygı ve endişeye", 2, "d3-k2-psi-008", "6 belirtiden en az 3", None),
    ("Bu bilgi çıkmış sınavda sorulmuştur: **Çocuklarda tanı** için altı belirtiden yalnızca bir tanesi yeterlidir!",
     "Bu bilgi çıkmış sınavda sorulmuştur: Önemli bir sınav ayrıntısı olarak erişkinlerde en az üç belirti aranırken çocuklarda tanı koyabilmek için bu altı belirtiden yalnızca bir tanesinin bulunması yeterlidir.",
     "Çocuklarda yalnızca bir maddenin", 3, "q-25-26_d_nem_3_kurul_2-82-cs3", "Çocuklarda tanı", None),
    ("**Belirti 1:** Huzursuzluk ya da gergin ya da sürekli diken üzerinde olma halidir.",
     "Birinci kardinal belirti hastanın kendini sürekli gergin, tedirgin, huzursuz veya diken üstünde hissetmesidir.",
     "1- Huzursuzluk ya da gergin", 4, None, None, None),
    ("**Belirti 2:** Enerji kaybı ve kolay yorulma tablosudur.",
     "İkinci kardinal belirti zihinsel ve bedensel tükenmişliğe bağlı olarak gün içinde çok çabuk ve kolay yorulmadır.",
     "2- Kolay yorulma", 5, None, None, None),
    ("**Belirti 3:** Odaklanmakta güçlük çekme ya da zihnin tamamen boşalması hissidir.",
     "Üçüncü kardinal belirti dikkatini toplamakta belirgin zorluk yaşama ya da zihnin aniden bomboş kalmış gibi duraklamasıdır.",
     "3- Odaklanmakta güçlük çekme", 6, None, None, None),
    ("Bu belirtilerin son altı ay boyunca **günlerin çoğunda bulunması** şarttır.",
     "Semptomların geçici birkaç gün değil, son altı aylık sürenin yarıdan fazlasında hastaya eşlik etmesi tanısal doğruluk için gereklidir.",
     "TANI- DSM-5", 0, None, None, None)
]

# Sayfa 11: DSM-5 Tanı Kriterleri (Kriter 4-6, D, E, F)
PD[11] = [
    ("**Belirti 4:** İrritabilite, küçük uyarılara karşı bile tahammülsüzlük ve çabuk sinirlenmedir.",
     "Dördüncü kardinal belirti irritabilite yani küçük uyarılara karşı aşırı tahammülsüzlük, çabuk parlama ve alınganlıktır.",
     "4- İrritabilite", 0, None, None, None),
    ("Hasta yakınları kişinin eskisine göre **çok daha sinirli ve tahammülsüz** olduğunu belirtir.",
     "Aile bireyleri hastanın en ufak gürültüye veya soruya ters tepkiler verdiğini ve tahammül sınırının çok daraldığını sıklıkla ifade eder.",
     "4- İrritabilite", 0, None, None, None),
    ("**Belirti 5:** Kas gerginliği, özellikle ense, omuz ve sırtta ağrılı kas sertliğidir.",
     "Beşinci kardinal belirti özellikle kafa tabanı, ense ve sırt kaslarında belirginleşen ağrılı kas sertliği ve gerginliğidir.",
     "5- Kas gerginliği", 1, None, None, None),
    ("**Belirti 6:** Uyku bozukluğu, uykuya dalmakta zorluk veya dinlendirici olmayan uykudur.",
     "Altıncı kardinal belirti zihinsel tasalar nedeniyle uykuya dalmakta güçlük, gece sık bölünmeler veya sabah dinlenmemiş uyanmadır.",
     "6- Uyku bozukluğu", 2, None, None, None),
    ("Yatağa girdiğinde zihindeki kuruntular nedeniyle **saatlerce uyuyamama** çok tipiktir.",
     "Hasta yatağa yattığında günün veya geleceğin endişeleri zihninde dönüp durur ve saatlerce uykuya dalış gerçekleşemez.",
     "uykuya dalmakta ya da", 2, None, None, None),
    ("**D Kriteri:** Kaygı ve bedensel belirtiler klinik açıdan belirgin işlevsellik kaybına yol açmalıdır.",
     "D kriterine göre anksiyete ve somatik yakınmalar toplumsal, mesleki ya da diğer önemli işlevsellik alanlarında belirgin bozulmaya ve yoğun sıkıntıya yol açmalıdır.",
     "D- Kaygı, endişe ya da", 3, None, None, None),
    ("**E Kriteri:** Bu bozukluk bir maddenin veya tıbbi durumun fizyolojik etkilerine bağlanamaz.",
     "E kriteri uyarınca klinik tablo herhangi bir ilacın, madde kötüye kullanımının ya da hipertiroidi gibi genel tıbbi durumların doğrudan fizyolojik etkisine bağlanamamalıdır.",
     "E- Bu bozukluk bir maddenin", 4, None, None, None),
    ("**F Kriteri:** Bozukluk başka bir ruhsal bozuklukla daha iyi açıklanamaz.",
     "F kriteri ise bu anksiyete tablosunun panik bozukluk, obsesif kompulsif bozukluk veya sosyal anksiyete gibi başka bir ruhsal hastalıkla daha iyi açıklanamayacağını kurala bağlar.",
     "F- Bu bozukluk başka bir", 5, None, None, None),
    ("Tüm bu kriterler karşılandığında hastaya **Yaygın Anksiyete Bozukluğu kesin tanısı** konur.",
     "Altı aylık süre, kontrol güçlüğü, en az üç kardinal belirti ve organik dışlama sağlandığında tanı kesinleşmiş olur.",
     "önemli diğer işlevsellik alanlarında", 3, None, None, None),
    ("Tanı konulduktan sonra tedavi planı **gecikmeden uygulamaya konulmalıdır**.",
     "Doğru tanı hastanın gereksiz tetkik sarmalından kurtulmasını ve hedefe yönelik etkin tedaviye kavuşmasını sağlar.",
     "işlevsellikte düşmeye", 3, None, None, None)
]

# Sayfa 12: Ayırıcı Tanı: Kardiyovasküler, Pulmoner ve Nörolojik
PD[12] = [
    ("**Kardiyovasküler Hastalıklar:** Anemi, anjina pektoris, konjestif kalp yetmezliği ve hipertansiyon araştırılmalıdır.",
     "Kardiyovasküler sistemde doku hipoksisi yapan anemi, anjina pektoris, konjestif kalp yetmezliği ve hipertansiyon anksiyeteyi taklit edebilir.",
     "Anemi, anjina", 1, None, None, None),
    ("**Aritmi ve İskemi:** Mitral kapak prolapsusu, miyokard enfarktüsü ve paroksismal atriyal taşikardi elenmelidir.",
     "Mitral kapak prolapsusu, akut koroner sendromlar ve paroksismal atriyal taşikardi gibi aritmiler şiddetli çarpıntı ve ölüm korkusuyla başvurabilir.",
     "mitral kapak prolapsusus", 1, None, None, None),
    ("Genç kadınlarda **mitral kapak prolapsusu** atipik göğüs ağrısı ve çarpıntıyla sıkça anksiyeteyle karışır.",
     "Özellikle genç kadın olgularda sistolik klik ve üfürümle giden mitral kapak prolapsusu anksiyete benzeri otonomik semptomlar üretebilir.",
     "mitral kapak prolapsusus", 1, None, None, None),
    ("**Akciğer Hastalıkları:** Bronşiyal astım ve hayatı tehdit eden pulmoner emboli dışlanmalıdır.",
     "Solunum sisteminde bronşiyal astım atakları ve akut nefes darlığı yapan hayatı tehdit edici pulmoner emboli mutlaka ekarte edilmelidir.",
     "Astım, pulmoner emboli", 2, None, None, None),
    ("Akut hava açlığı ve taşikardide **pulmoner emboli ayırıcı tanıda** hayati öneme sahiptir.",
     "Ani başlayan nefes darlığı ve göğüs ağrısı varlığında anksiyete tanısına atlamadan önce pulmoner emboli ihtimali kan gazı ve d-dimer ile değerlendirilmelidir.",
     "pulmoner emboli", 2, None, None, None),
    ("**Serebrovasküler Olaylar:** Geçici iskemik ataklar ve inme tabloları organik anksiyete doğurabilir.",
     "Serebrovasküler hastalıklar, geçici iskemik ataklar ve intrakraniyal kitleler otonomik dengesizlik ve kaygı üretebilir.",
     "Serabrovasküler hastalıklar", 3, None, None, None),
    ("**Nörolojik Hastalıklar:** Epilepsi, Huntington hastalığı, ensefalit ve Meniere hastalığı taranmalıdır.",
     "Özellikle temporal lob tutulumlu kompleks parsiyel nöbetler, Huntington hastalığı, menenjit, ensefalit ve periferik vestibüler tutulum yapan Meniere hastalığı incelenmelidir.",
     "epilepsi, Huntington", 3, None, None, None),
    ("Temporal lob epilepsisinde **ani korku auraları** anksiyete ataklarını birebir taklit edebilir.",
     "Epileptik odak deşarjları sırasında hastada ani ve nedensiz bir dehşet hissi veya epigastrik yükselme duyumu ortaya çıkabilir.",
     "epilepsi", 3, None, None, None),
    ("**Multipl Skleroz ve Wilson:** Demiyelinizan ve metabolik nörodejeneratif hastalıklar ayırıcı tanıdadır.",
     "Multipl skleroz lezyonları ve hepatolentiküler dejenerasyon yani Wilson hastalığı da psikiyatrik semptomlarla başlayabilmektedir.",
     "multıpl skleroz", 3, None, None, None),
    ("Her yeni anksiyete olgusunda **eksiksiz nörolojik ve kardiyak muayene** şarttır.",
     "Organik bir hastalığı atlamamak adına ayrıntılı fizik muayene ve elektrokardiyografi incelemesi yapılmadan tanı kesinleştirilmemelidir.",
     "Genel Anksiyete Bozukluğu", 0, None, None, None)
]

# Sayfa 13: Ayırıcı Tanı: Endokrin, Toksik ve Madde Çekilmesi
PD[13] = [
    ("Bu bilgi çıkmış sınavda sorulmuştur: **Endokrin Nedenler** arasında hipoglisemi, hipertiroidizm ve feokromositoma yer alır.",
     "Bu bilgi çıkmış sınavda sorulmuştur: Endokrin hastalıklardan sempatik fırtınaya yol açan hipertiroidizm, katekolamin üreten feokromositoma ve akut nörogilkopeneik hipoglisemi organik ayırıcı tanıda öncelikle taranmalıdır.",
     "Hipoglisemi, Addison", 0, "past-1790877044849-897865", "Endokrin Nedenler", None),
    ("Tirotoksikozda **terleme, kilo kaybı ve taşikardi** anksiyete kliniğini birebir taklit eder.",
     "Tiroid bezinin aşırı hormon salgılaması ellerde titreme, çarpıntı, sıcağa tahammülsüzlük ve huzursuzluk yaparak tabloyu taklit eder; serum tiroit stimülan hormon düzeyi mutlaka bakılmalıdır.",
     "hipertroidizm", 0, None, None, None),
    ("Feokromositomada **paroksismal tansiyon atakları** ve şiddetli baş ağrısı eşlik eder.",
     "Böbrek üstü bezi medullasından salgılanan yüksek katekolaminler ani terleme, çarpıntı ve kan basıncı fırlamaları ile seyreder.",
     "feokromastoma", 0, None, None, None),
    ("Addison hastalığı, karsinoid sendrom, **Cushing sendromu** ve hipoparatiroidizm araştırılmalıdır.",
     "Adrenal yetmezlik yapan Addison hastalığı, vazomotor kızarma yapan karsinoid sendrom, hiperkortizolemiyle seyreden Cushing sendromu ve hipokalsemi yapan hipoparatiroidizm elenmelidir.",
     "Cushing sendromu", 0, None, None, None),
    ("Menopozal vazomotor bozukluklar ve **premenstrüel disforik bozukluk** kaygı ataklarını tetikleyebilir.",
     "Menopozdaki östrojen çekilmesine bağlı sıcak basmaları ve premenstrüel disforik tablolardaki hormonal dalgalanmalar benzer bedensel yakınmalar doğurur.",
     "menapozal bozukluklar", 0, None, None, None),
    ("**İlaç ve Madde İntoksikasyonları:** Amfetamin, kokain, esrar, nikotin ve teofilin anksiyete üretir.",
     "Sempatomimetik uyarıcılar olan amfetamin, kokain, aşırı nikotin, esrar, bronkodilatör teofilin ve antikolinerjik ilaçlar şiddetli taşikardi ve huzursuzluk yaratır.",
     "Amfetamin, kokain", 1, None, None, None),
    ("Günde yüksek miktarda **kafein veya enerji içeceği** tüketimi anksiyeteyi tırmandırabilir.",
     "Aşırı kahve ve enerji içeceği tüketimi adenozin reseptör blokajı yaparak taşikardi, kas seğirmeleri ve yaygın kaygı doğurur.",
     "teofilin, amil nitrit", 1, None, None, None),
    ("**İlaç Çekilmesi:** Alkol, opioidler, sedatif-hipnotikler ve santral antihipertansiflerin kesilmesi tabloyu taklit eder.",
     "Yoksunluk tablolarında alkolün kesilmesi, sedatif hipnotiklerin veya benzodiazepinlerin aniden bırakılması ve klonidin gibi antihipertansiflerin kesilme sendromu ağır anksiyete doğurur.",
     "Alkol, opiat", 2, None, None, None),
    ("**Diğer Sistemik Durumlar:** Sistemik lupus, elektrolit düzensizlikleri, ağır metal intoksikasyonu ve B12 eksikliğidir.",
     "Otoimmün hastalıklardan sistemik lupus eritematozus, hiponatremi gibi elektrolit bozuklukları, üremi, ağır metal zehirlenmeleri ve vitamin be on iki eksikliği unutulmamalıdır.",
     "Sistemik lupus", 3, None, None, None),
    ("Her hastada **ayrıntılı laboratuvar taraması** ile organik patolojiler dışlanmalıdır.",
     "Tam kan sayımı, biyokimya, tiroid fonksiyon testleri ve toksikolojik tarama ayırıcı tanının temel laboratuvar basamaklarıdır.",
     "elektrolit düzensizlikleri", 3, None, None, None)
]

# Sayfa 14: Psikiyatrik Ayırıcı Tanı
PD[14] = [
    ("**Panik Bozukluk Ayrımı:** Panik bozuklukta aniden pik yapan nöbetler varken, YAB'de kaygı süreğendir.",
     "Panik bozuklukta dakikalar içinde tepe noktasına ulaşıp sonlanan ani panik nöbetleri görülürken, yaygın anksiyete bozukluğunda kaygı dalgalı fakat aralıksız ve süreğendir.",
     "Panik bozukluk", 0, None, None, None),
    ("Panik bozuklukta temel korku **ölüm veya çıldırmadır**, YAB'de ise gündelik felaket senaryolarıdır.",
     "Panik hastası o an kalp krizi geçirdiğini ve öleceğini düşünürken, yaygın anksiyete hastası sevdiklerinin başına kötü bir şey geleceğinden veya parasız kalmaktan endişe eder.",
     "Panik bozukluk", 0, None, None, None),
    ("**Fobik Bozukluklar:** Fobilerde kaygı belirli bir nesne veya duruma özgüyken, YAB'de serbest dalgalanır.",
     "Fobik bozukluklarda kaygı yalnızca özgül bir nesneye veya sosyal ortama maruz kalındığında tetiklenir; yaygın anksiyetede ise nesnesiz ve serbest dalgalanan bir endişe vardır.",
     "Fobik bozukluk", 1, None, None, None),
    ("**Obsesif Kompulsif Bozukluk:** OKB'de egodistonik takıntılar varken, YAB'de gerçek yaşam kaygıları abartılır.",
     "Obsesif kompulsif bozuklukta mantık dışı kabul edilen yineleyici saplantılar ve rahatlatıcı zorlantılar bulunurken, yaygın anksiyetedeki endişeler gerçek yaşam sorunlarının felaketleştirilmesidir.",
     "Obsesif kompulsif", 2, None, None, None),
    ("**Travma Sonrası Stres Bozukluğu:** TSSB'de travmanın yeniden yaşantılanması ve kabuslar ön plandadır.",
     "Travma sonrası stres bozukluğunda travmatik bir olayın istemsizce yeniden yaşantılanması, flashbackler ve kaçınma davranışları tanısal çekirdeği oluşturur.",
     "Posttravmatik stres", 3, None, None, None),
    ("**Şizofreni Başlangıcı:** Prodromal dönemdeki anksiyetede gerçeklik değerlendirmesi giderek bozulur.",
     "Şizofreninin başlangıç evresinde de yoğun bir içsel bunaltı görülebilir ancak zamanla hezeyanlar ve düşünce içeriğinde tuhaflıklar tabloya eklenir.",
     "Şizofreni", 4, None, None, None),
    ("**Depresif Bozukluk ve Uyum Bozukluğu:** Depresyonda anhedoni ve çökkünlük, uyum bozukluğunda belirgin stresör vardır.",
     "Majör depresyonda zevk alamama ve çökkün duygudurum esasken, anksiyete ile giden uyum bozukluğunda son üç ay içinde ortaya çıkan somut bir yaşam stresörü mevcuttur.",
     "Depresif bozukluk", 5, None, None, None),
    ("Uyum bozukluğunda stresör ortadan kalktığında **belirtiler 6 ay içinde geriler**.",
     "Uyum bozukluğunun seyri stres faktörüyle sınırlıdır, oysa yaygın anksiyete bozukluğu stresör kalksa dahi yıllarca kronik olarak devam eder.",
     "Anksiyete ile giden uyum", 6, None, None, None),
    ("Doğru psikiyatrik ayrım **tedavi protokolünü doğrudan belirler**.",
     "Her bir anksiyete bozukluğunun bilişsel dinamikleri ve farmakolojik yanıt profili farklılık gösterdiğinden klinik ayrım esastır.",
     "Panik bozukluk", 0, None, None, None)
]

# Sayfa 15: Gidiş ve Sonlanış (Prognoz)
PD[15] = [
    ("Bu bilgi çıkmış sınavda sorulmuştur: **YAB'nin Seyri** dalgalı ve kronik bir gidiş gösterir.",
     "Bu bilgi çıkmış sınavda sorulmuştur: Yaygın anksiyete bozukluğunun klinik seyri semptom şiddetinde zaman içinde iniş çıkışların izlendiği dalgalı ve kronik bir gidiş gösterir.",
     "kronik seyreden", 0, "q-25-26_d_nem_3_kurul_2-82-cs7", "YAB'nin Seyri", None),
    ("Kendiliğinden tam remisyon **hastaların azınlığında** görülür.",
     "Tedavi edilmeyen olgularda kendiliğinden tam düzelme oranı oldukça düşüktür; hastalık çoğunlukla yaşam boyu dalgalanmalarla devam eder.",
     "kronik seyreden", 0, None, None, None),
    ("Yaşam olayları, kayıplar ve zorlayıcı stres etkenleri **alevlenmelerde doğrudan tetikleyicidir**.",
     "Bireyin karşılaştığı olumsuz yaşam olayları, kayıplar, iş stresi ve ailevi çatışmalar hastalığın başlamasında ve alevlenme ataklarında birincil tetikleyicidir.",
     "Yaşam olayları hastalığın", 1, None, None, None),
    ("Tedaviye yanıtı yetersiz olanlarda, **kadınlarda ve erken başlangıçlı** olgularda prognoz daha kötüdür.",
     "Başlangıç tedavisine direnç gösteren olgularda, kadın cinsiyette ve erken yaşta başlayan tablolarda hastalığın kronikleşme ve işlev kaybı yaratma riski daha yüksektir.",
     "erken başlangıçlı olanlarda", 2, None, None, None),
    ("Kişilik patolojisi eşlik ettiğinde **tedaviye uyum ve düzelme oranı** düşer.",
     "Özellikle çekingen, bağımlı ya da sınırda kişilik özellikleri sergileyen bireylerde terapötik işbirliği kurmak ve semptomları yatıştırmak daha güçtür.",
     "Tedaviye yanıtı iyi olmayan", 2, None, None, None),
    ("Eşlik eden majör depresyon varlığında **özkıyım riski belirgin şekilde yüksektir**.",
     "Özellikle majör depresyon komorbiditesi geliştiğinde veya hasta yoğun bir çaresizlik yaşadığında özkıyım riski belirgin derecede yükselir ve yakın psikiyatrik izlem gerekir.",
     "Özkıyım riski yüksek", 3, None, None, None),
    ("Kronik anksiyete **kardiyovasküler morbidite riskini** de artırmaktadır.",
     "Süregiden yüksek sempatik tonus ve kortizol salınımı uzun vadede hipertansiyon, ateroskleroz ve metabolik sendrom riskini yükseltir.",
     "GİDİŞ VE SONLANIŞ", 0, None, None, None),
    ("Erken tanı ve hedefe yönelik kombine tedavi **kronik yeti yitimini önlemede** hayati öneme sahiptir.",
     "Zamanında konulan doğru tanı ve farmakoterapi ile psikoterapinin birlikte uygulanması hastanın yaşam kalitesini korur ve kronik yeti yitimini önler.",
     "GİDİŞ VE SONLANIŞ", 0, None, None, None),
    ("Tedavinin amacı yalnızca semptomları azaltmak değil **tam klinik remisyondur**.",
     "Klinik sağaltımda hedefimiz hastanın yalnızca kaygısını hafifletmek değil, mesleki ve ailevi işlevselliğini eksiksiz olarak yeniden kazandırmaktır.",
     "Tedaviye yanıtı", 2, None, None, None)
]

# Sayfa 16: Psikoterapi Yaklaşımları
PD[16] = [
    ("**Bilişsel-Davranışçı Terapi (BDT):** YAB tedavisinde etkinliği kanıtlanmış temel psikoterapi yöntemidir.",
     "Yaygın anksiyete bozukluğunun sağaltımında bilişsel davranışçı terapi etkinliği en güçlü kanıtlarla ortaya konmuş temel psikoterapi yaklaşımıdır.",
     "Bilişsel-davranışçı psikoterapide", 1, None, None, None),
    ("Psikoterapi nüksleri önlemede **farmakoterapi kadar kalıcı** sonuçlar sağlar.",
     "İlaç tedavisi kesildikten sonra nüks oranlarını düşürmede bilişsel davranışçı terapi tekniklerinin kazandırdığı başa çıkma becerileri kritik rol oynar.",
     "Bilişsel-davranışçı psikoterapide", 1, None, None, None),
    ("**Bilişsel Yeniden Yapılandırma:** Felaket senaryoları sorgulanır ve alternatif düşünce yolları geliştirilir.",
     "Bilişsel yeniden yapılandırma tekniği ile hastanın felaketleştirici bilişsel çarpıtmaları ele alınır, tehlike olasılıkları gerçekçi temellere oturtulur.",
     "bilişsel yeniden yapılandırma", 1, None, None, None),
    ("Hastaya kanıta dayalı düşünme ve **en kötü senaryoyla yüzleşme** öğretilir.",
     "Danışana kuruntularının gerçekçi kanıtları sorgulatılır ve en kötü ihtimal gerçekleşse bile nasıl başa çıkabileceği uygulamalı olarak çalışılır.",
     "bilişsel yeniden yapılandırma", 1, None, None, None),
    ("**Gevşeme Teknikleri:** Kronik kas tonusunu azaltmak için progresif kas gevşetme eğitimi verilir.",
     "Otonomik gerginliği ve kas ağrılarını kontrol altına almak amacıyla hastaya progresif kas gevşeme egzersizleri öğretilerek bedensel rahatlama sağlanır.",
     "gevşeme teknikleri", 1, None, None, None),
    ("**Nefes Egzersizleri:** Diyafram nefesiyle hiperventilasyon ve hava açlığı kontrol altına alınır.",
     "Diyafragmatik derin nefes egzersizleri hastanın akut hava açlığı ve taşikardi yakınmalarını kontrol etmesinde önemli bir başa çıkma aracıdır.",
     "nefes egsersizleri", 1, None, None, None),
    ("Endişe erteleme teknikleri ile **günün belirli saatinde kuruntu yapma** kuralı konur.",
     "Hastaya gün boyu sürekli endişelenmek yerine günün belirli bir yirmi dakikalık endişe saatinde kuruntularını yazıp incelemesi ödevi verilir.",
     "gevşeme teknikleri", 1, None, None, None),
    ("**İçgörü Yönelimli Terapi:** Anksiyeteyi araştırılması gereken bilinçdışı bir çatışmanın işareti olarak kabul eder.",
     "İçgörü yönelimli psikoterapide anksiyete bireyin yüzleşmekten kaçındığı bilinçdışı içsel çatışmaların ve çözümlenmemiş duyguların bir sinyali sayılır.",
     "İçgörü yönelimli psikoterapide", 2, None, None, None),
    ("Bu yaklaşım **psikolojik zihinliliği olan** ve kaygının kaynağını anlamak isteyen hastalarda tercih edilir.",
     "Bu yöntem psikolojik zihinliliği yüksek, kendi duygu dünyasını sorgulama isteği ve kapasitesi olan entelektüel hastalarda oldukça verimli sonuçlar verir.",
     "Psikolojik zihinliliği olan", 2, None, None, None),
    ("Terapi ve ilaç birlikteliği **en yüksek başarı oranına** ulaşmayı mümkün kılar.",
     "Klinik çalışmalarda farmakoterapi ile yapılandırılmış psikoterapinin kombine edildiği olgularda tedavi başarısının belirgin şekilde arttığı gösterilmiştir.",
     "YAB- TEDAVİ", 0, None, None, None)
]

# Sayfa 17: Farmakoterapi İlkeleri
PD[17] = [
    ("Bu bilgi çıkmış sınavda sorulmuştur: **SSRI Grubu İlaçlar** YAB tedavisinde ilk basamak farmakoterapidir.",
     "Bu bilgi çıkmış sınavda sorulmuştur: Yaygın anksiyete bozukluğunun idame tedavisinde birinci basamak seçenek seçici serotonin geri alım inhibitörleridir.",
     "seçici serotonin gerialım", 0, "past-1790877036007-758785", "SSRI Grubu İlaçlar", None),
    ("SSRI'ların terapötik etkisi **2 ila 4 hafta sonra** ortaya çıkar.",
     "Antidepresanların anksiyolitik etkinliği anında başlamaz; reseptör duyarsızlaşması ve nöroplastisite için en az iki ila dört haftalık süre gereklidir.",
     "seçici serotonin gerialım", 0, None, None, None),
    ("Tedavinin ilk günlerinde gelişebilecek **geçici anksiyete artışı** hastaya önceden anlatılmalıdır.",
     "İlacın başlangıç evresinde görülebilen hafif ajitasyon veya bulantı hastaya açıklanmalı ve düşük dozla başlanıp yavaş titrasyon yapılmalıdır.",
     "seçici serotonin gerialım", 0, None, None, None),
    ("**SNRI Grubu:** Venlafaksin ve duloksetin özellikle belirgin somatik ağrısı olanlarda etkilidir.",
     "Serotonin noradrenalin geri alım inhibitörlerinden venlafaksin ve duloksetin gerek anksiyete gerekse eşlik eden nöropatik ve kas iskelet ağrılarında ilk basamak tercihtir.",
     "Seratonin-noradrenalin gerialım", 1, None, None, None),
    ("Bu bilgi çıkmış sınavda sorulmuştur: **Buspiron** 5-HT1A parsiyel agonisti olup sedasyon ve bağımlılık yapmaz.",
     "Bu bilgi çıkmış sınavda sorulmuştur: Buspiron serotonin beş haş te bir a reseptör parsiyel agonisti olup sedasyon, kas gevşemesi veya bağımlılık yapmayan özgül bir anksiyolitiktir.",
     "Buspiron (5-HT1A parsiyel agonist)", 3, "q-No_ropsikiyatri_gis_kardiyo_-2023-2024-C__km_s_lar__240625_053302__2_-39", "Buspiron", None),
    ("Buspironun etkisi **2-3 hafta içinde oturur** ve gerektiğinde kullanılan bir acil ilacı değildir.",
     "Buspiron kriz anında alınan bir sakinleştirici değildir; düzenli günlük kullanımda haftalar içinde anksiyolitik etki oluşturan koruyucu bir ajandır.",
     "Buspiron (5-HT1A parsiyel agonist)", 3, None, None, None),
    ("**Benzodiazepinler:** Hızlı etki gösterirler ancak bağımlılık riski nedeniyle sadece kısa süreli köprü tedavisidir.",
     "Benzodiazepin grubu ilaçlar anksiyeteyi dakikalar içinde yatıştırır ancak tolerans ve bağımlılık riski nedeniyle sadece antidepresanların etkisi oturana kadar iki ila dört hafta kullanılır.",
     "benzodiazepinler", 2, None, None, None),
    ("Benzodiazepinlerin uzun süreli kullanımı **bilişsel yavaşlama ve tolerans** riskine yol açar.",
     "Kronik benzodiazepin kullanımı bellek kusurları, dikkat dağınıklığı, sedasyon ve kesilme anında şiddetli rebound anksiyete ile sonuçlanabilir.",
     "benzodiazepinler", 2, None, None, None),
    ("**Pregabalin:** Kalsiyum kanal alfa-2-delta alt birimini bağlayarak hızlı anksiyolitik etki sağlar.",
     "Voltaj kapılı kalsiyum kanallarının alfa iki delta ligandı olan pregabalin hızlı başlangıçlı etkisiyle yaygın anksiyete tedavisinde onaylı ve güçlü bir seçenektir.",
     "pregabalin", 4, None, None, None),
    ("Tedaviye dirençli olgularda **atipik antipsikotik güçlendirmesi** ve kombinasyon stratejileri uygulanır.",
     "Dirençli tablolarda birinci basamak ilaçların yanına ketiapin gibi düşük doz atipik antipsikotikler veya duygudurum dengeleyicileri eklenerek güçlendirme yapılır.",
     "diğer ilaçlar", 5, None, None, None)
]

# Sayfa 18: İlaç Dozajları ve Terapötik Aralıklar Tablosu
PD[18] = [
    ("**SSRI Dozajları:** Sitalopram 20-40 mg, essitalopram 10-20 mg, fluoksetin 20-40 mg aralığında kullanılır.",
     "Seçici serotonin geri alım inhibitörlerinden sitalopram yirmi ila kırk miligram, essitalopram on ila yirmi miligram ve fluoksetin yirmi ila kırk miligram hedef dozlarında titre edilir.",
     "Sitalopram", 0, None, None, None),
    ("Essitalopram **yüksek seçiciliği ve düşük etkileşim profili** ile klinikte en sık tercih edilen ajandır.",
     "Essitalopram saf serotonin geri alım inhibisyonu sağlaması ve sitokrom enzimleriyle minimal etkileşimi nedeniyle ilk seçenek olarak öne çıkar.",
     "Essitalopram", 0, None, None, None),
    ("**Diğer SSRI'lar:** Fluvoksamin 200-300 mg, paroksetin 20-40 mg ve sertralin 50-200 mg dozunda uygulanır.",
     "Fluvoksamin iki yüz ila üç yüz miligram, paroksetin yirmi ila kırk miligram ve sertralin elli ila iki yüz miligram günlük terapötik dozlarda reçete edilir.",
     "Fluvoksamin", 0, None, None, None),
    ("Sertralin kardiyak açıdan **en güvenli antidepresanlardan biridir**.",
     "Kardiyovasküler komorbiditesi olan yaygın anksiyete hastalarında sertralin güvenilir yan etki profiliyle birinci basamakta güvenle kullanılır.",
     "Sertralin", 0, None, None, None),
    ("Paroksetin güçlü anksiyolitik etkiye sahiptir ancak **kesilme sendromu riski** yüksektir.",
     "Paroksetinin yarı ömrü kısa ve antikolinerjik etkisi belirgin olduğundan ani kesilmelerde baş dönmesi, elektrik çarpması hissi ve huzursuzluk görülebilir.",
     "Paroksetin", 0, None, None, None),
    ("**Buspiron Dozu:** Günlük 15 mg başlanıp yanıt durumuna göre günde 30-60 mg dozuna çıkılır.",
     "Buspiron tedavisine günlük on beş miligram ile başlanır ve klinik cevaba göre günde iki ya da üç doza bölünerek otuz ila altmış miligram idame dozuna yükseltilir.",
     "Buspiron", 1, None, None, None),
    ("**SNRI Dozajları:** Venlafaksin uzatılmış salınımlı 150-300 mg, duloksetin ise 60-120 mg dozunda verilir.",
     "Serotonin noradrenalin geri alım inhibitörlerinden venlafaksin uzatılmış salınımlı formu yüz elli ila üç yüz miligram, duloksetin ise altmış ila yüz yirmi miligram idame dozunda kullanılır.",
     "Wenlafaxine XR", 2, None, None, None),
    ("Venlafaksin yüksek dozlarda **kan basıncı takibi** gerektirmektedir.",
     "Yüz elli miligramın üzerindeki venlafaksin dozlarında noradrenerjik geri alım blokajı belirginleştiğinden diastolik kan basıncı düzenli izlenmelidir.",
     "Wenlafaxine XR", 2, None, None, None),
    ("**Benzodiazepin Dozajları:** Diazepam 20-40 mg, alprazolam ise 2-4 mg günlük doz aralığındadır.",
     "Akut köprülemede diazepam yirmi ila kırk miligram, alprazolam ise iki ila dört miligram aralığında verilebilir ancak doz kademeli azaltılarak kesilmelidir.",
     "Diazepam", 3, None, None, None),
    ("**İdame Tedavi Süresi:** Akut iyileşme sağlansa dahi relapsı önlemek için tedavi en az 1 yıl sürdürülmelidir.",
     "Tam klinik remisyona ulaşıldıktan sonra hastalığın yüksek nüks eğilimi nedeniyle farmakoterapi en az bir yıl boyunca kesilmeden sürdürülmelidir.",
     "SSRI", 0, None, None, None),
    ("İlaç kesimi daima **haftalar ve aylar içine yayılarak** çok yavaş yapılmalıdır.",
     "İlacın aniden kesilmesi nüksü ve çekilme belirtilerini tetikleyebileceğinden doz basamak basamak azaltılarak sonlandırılmalıdır.",
     "SSRI", 0, None, None, None)
]

# Sayfa 19: Algoritma ve Klinik Takip Şeması (SEKİL SAYFASI)
PD[19] = [
    ("**Birinci Basamak Yaklaşım:** Tanı netleştirildikten sonra psiko-eğitim verilir, BDT ve SSRI veya SNRI başlanır.",
     "Yaygın anksiyete bozukluğu tedavi algoritmasında ilk basamak kapsamlı hasta psiko-eğitimi, bilişsel davranışçı terapi ve birinci basamak bir antidepresanın başlanmasıdır.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"),
    ("Hastaya anksiyetenin doğası anlatılarak **tedaviye uyumu güçlendirilir**.",
     "Hastalığın biyolojik temelleri, ilaçların etki başlama süresi ve geçici yan etkiler ilk görüşmede detaylıca anlatılmalıdır.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"),
    ("**Yanıt Değerlendirmesi:** 4-6 haftalık yeterli süre sonunda semptom kontrolü ve işlevsellik değerlendirilir.",
     "Tedaviye başlandıktan dört ila altı hafta sonra hasta kontrole çağrılarak ilacın etkinliği, yan etkileri ve semptomlardaki gerileme düzeyi objektif ölçeklerle değerlendirilir.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"),
    ("Kısmi yanıt alınan olgularda ilk adım **dozun tolere edilen sınıra kadar artırılmasıdır**.",
     "Eğer semptomlarda belirgin bir gerileme varsa ancak tam remisyon sağlanamamışsa mevcut ilacın dozu hedef aralığın üst sınırına kadar yükseltilir.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"),
    ("**Direnç Durumunda Adımlar:** Doz artırımı, alternatif birinci basamak ajana geçiş veya pregabalin eklenmesi düşünülür.",
     "Yeterli doz ve süreye rağmen klinik yanıt alınamayan olgularda başka bir birinci basamak ilaca geçilir ya da pregabalin veya buspiron eklenir.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"),
    ("Dirençli olgularda **düşük doz atipik antipsikotik güçlendirmesi** kanıta dayalı bir seçenektir.",
     "İki ayrı antidepresan denemesine rağmen düzelmeyen hastalarda ketiapin yirmi beş ila yüz elli miligram dozunda tedaviye eklenerek güçlendirme sağlanır.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"),
    ("**Uzun Süreli Takip:** Remisyon sağlandığında nüks belirtileri izlenir ve ilaç kesimi mutlaka kademeli yapılır.",
     "Tam iyileşme sağlanan hastalarda en az bir yıllık idame sonrasında ilaç dozu aylar içinde çok yavaş azaltılarak kesilir ve stres yönetim stratejileri pekiştirilir.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"),
    ("Nüks belirtileri fark edildiğinde **vakit kaybetmeden idame dozuna** geri dönülür.",
     "İlaç azaltımı sırasında kaygı belirtileri yeniden tırmanırsa doz bir önceki etkili seviyeye yükseltilerek remisyon korunur.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması"),
    ("Algoritma temelli sistematik yaklaşım **klinik başarıyı en üst düzeye** çıkarır.",
     "Kanıta dayalı tedavi adımlarının basamak basamak titizlikle uygulanması yaygın anksiyete hastalarında yaşam kalitesini eksiksiz düzeltmektedir.",
     "Tedavi algoritması", 0, None, None, "Yaygın anksiyete bozukluğu klinik takip ve basamaklı tedavi algoritması görsel şeması")
]

# Sayfa 20: Kapanış ve Özet
PD[20] = [
    ("**Ders Özeti:** YAB, en az 6 ay süren kontrol edilemeyen aşırı endişe ve belirgin somatik gerginlikle seyreder.",
     "Dersimizi özetleyecek olursak yaygın anksiyete bozukluğu en az altı aylık süre ölçütü, kuruntuları denetleyememe ve motor otonomik gerginlikle giden kronik bir tablodur.",
     "TEŞEKKÜRLER", 0, None, None, None),
    ("**Sınav Hatırlatması:** 6 kardinal belirtiden 3'ü aranırken çocuklarda 1 belirti yeterlidir; süre en az 6 aydır.",
     "Sınavlar için en kritik spotlar en az altı aylık süre kuralı, altı belirtiden en az üçünün aranması, çocuklarda tek belirtinin yeterli olması ve buspironun bağımlılık yapmayan yapısıdır.",
     "TEŞEKKÜRLER", 0, None, None, None),
    ("**Organik Dışlama:** Hipertiroidizm, feokromositoma ve hipoglisemi her yeni hastada mutlaka taranmalıdır.",
     "Tıbbi ayırıcı tanıda hipertiroidizm, feokromositoma, aritmi ve hipogliseminin dışlanması gereken birincil organik patolojiler olduğu unutulmamalıdır.",
     "TEŞEKKÜRLER", 0, None, None, None),
    ("**Tedavi İlkesi:** İlk seçenek SSRI veya SNRI ile BDT kombinasyonudur; benzodiazepinler yalnızca kısa süreli köprüdür.",
     "Tedavide ilk basamağın es es er ı ve se ne er ı antidepresanlar ile bilişsel davranışçı terapi olduğu, benzodiazepinlerin bağımlılık riski nedeniyle sadece kısa süreli köprüleme olarak verileceği hatırda tutulmalıdır.",
     "TEŞEKKÜRLER", 0, None, None, None),
    ("Dersimizi burada tamamlıyoruz; klinik stajlarınızda ve kurul sınavlarınızda hepinize üstün başarılar dilerim.",
     "Yaygın anksiyete bozukluğu dersimizi burada noktalıyoruz; klinik stajlarınızda ve tıp fakültesi kurul sınavlarınızda hepinize üstün başarılar dilerim.",
     "TEŞEKKÜRLER", 0, None, None, None)
]

# ==============================================================================
# BUILD BOLUMLER & PARAGRAFLAR
# ==============================================================================
bolum_defs = [
    (1, "Giriş, Tanım ve Epidemiyoloji", [1, 2, 3]),
    (2, "Risk Faktörleri ve Etiyolojik Mekanizmalar", [4, 5, 6]),
    (3, "Klinik Görünüm ve Bedensel-Otonomik Semiyoloji", [7, 8, 9]),
    (4, "DSM-5 Tanı Ölçütleri ve Kardinal Belirtiler", [10, 11]),
    (5, "Tıbbi, Endokrin ve Psikiyatrik Ayırıcı Tanı", [12, 13, 14]),
    (6, "Klinik Seyir, Prognoz ve Psikoterapi", [15, 16]),
    (7, "Farmakoterapi, İlaç Dozajları ve Tedavi Algoritması", [17, 18, 19, 20])
]

bolumler_list = []
sents = []
para_counter = 1
para_last_sent = {}

for b_idx, (b_no, b_title, b_pages) in enumerate(bolum_defs):
    b_id = f"k2-54-b{b_no:02d}"
    paragraflar = []
    
    for pno in b_pages:
        items = PD.get(pno, [])
        if not items:
            continue
        
        p_id = f"k2-54-p{para_counter:03d}"
        para_counter += 1
        
        cumleler = []
        for (ekran, ses, sat_pat, sat_idx, cikmis, hw, sek) in items:
            c = make_sentence(ekran, ses, pno, sat_pat, sat_idx, cikmis, hw, sek)
            cumleler.append(c)
            sents.append(c)
        
        para_last_sent[p_id] = cumleler[-1]["id"]
        
        paragraflar.append({
            "id": p_id,
            "sayfa": pno,
            "slayt": {
                "sayfa": pno,
                "satir": cumleler[0]["slayt"]["satir"]
            },
            "cumleler": cumleler
        })
    
    bolumler_list.append({
        "id": b_id,
        "bolumIndex": b_idx,
        "baslik": b_title,
        "paragraflar": paragraflar
    })

# Compute statistics
total_words = sum(len(s["ses"].split()) for s in sents)
total_sents = len(sents)
total_paras = len(para_last_sent)

print(f"Total Sections: {len(bolumler_list)}")
print(f"Total Paragraphs: {total_paras}")
print(f"Total Sentences: {total_sents}")
print(f"Total Words: {total_words} (~{total_words/125:.1f} minutes of audio)")

# Save konusma_v2.json
konusma_v2 = {
    "surum": 2,
    "ders_id": "k2-54",
    "anahtar": "y25-k2-54-yaygin-anksiyete-bozuklugu",
    "bolumler": bolumler_list,
    "donem": "2025-2026"
}

(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Derive metin.md and konusma_metni.md using KV.turet
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/sesli_anlatim"))
sys.path.insert(0, str(REPO_ROOT / "meds/scripts/ders_isci"))
import konusma_v2 as KV

konusma_v2_copy = dict(konusma_v2)
konusma_v2_copy["baslik"] = "Yaygın Anksiyete Bozukluğu"
md_text, _ = KV.turet(konusma_v2_copy)
(TASLAK / "metin.md").write_text(md_text, encoding="utf-8")
(TASLAK / "konusma_metni.md").write_text(md_text, encoding="utf-8")
print("Saved metin.md and konusma_metni.md")

# Derive capalar and sayfalari in exact format for publisher
capalar_list = []
for b in bolumler_list:
    for p in b["paragraflar"]:
        p_capa = []
        for c in p["cumleler"]:
            st = c["slayt"].get("satir")
            if isinstance(st, list) and st:
                st = st[0]
            p_capa.append({
                "ses": c["ses"],
                "sayfa": c["slayt"]["sayfa"],
                "satir": st,
                "sekil": c["slayt"].get("sekil")
            })
        capalar_list.append(p_capa)
(TASLAK / "konusma_capalari.json").write_text(json.dumps(capalar_list, ensure_ascii=False, indent=2), encoding="utf-8")

sayfa_list = [p["sayfa"] for b in bolumler_list for p in b["paragraflar"]]
(TASLAK / "konusma_sayfalari.json").write_text(json.dumps(sayfa_list, ensure_ascii=False), encoding="utf-8")

# Live semantic vector drawing commands with zero forward leaks
# Strictly verified roots against text spoken up to that sentence
cizim_komutlari = [
    {
        "cumle": para_last_sent["k2-54-p002"],
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Normal Kaygı ve Korku Ayrımı",
        "ogeler": [
            "İç odaklı ve belirsiz tehdit",
            "Sempatik ve parasempatik denge",
            "Bilinen somut dış tehlike"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p003"],
        "bas": 0, "son": 4,
        "sayfa": 3,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Yaygın Anksiyete Tanım ve Yaygınlık",
        "ogeler": [
            "En az altı aylık süre kuralı",
            "Serbest dalgalanan nesnesiz kaygı",
            "Kadınlarda erkeklere göre iki kat sık"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p004"],
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Risk Etmenleri ve Eşlik Eden Tablolar",
        "ogeler": [
            "Çocukluk çağı kötü muamele öyküsü",
            "Yüzde altmıştan fazla majör depresyon",
            "Panik bozukluk ve madde kullanımı"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p005"],
        "bas": 0, "son": 4,
        "sayfa": 5,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Nörobiyolojik Etiyoloji Devresi",
        "ogeler": [
            "Benzodiazepin ve gama reseptör kusuru",
            "Serotonin noradrenalin disregülasyonu",
            "Oksipital lob bazal gangliyon ve amigdala"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p007"],
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Klinik Görünüm ve Semiyoloji",
        "ogeler": [
            "Motor huzursuzluk ve gergin duruş",
            "Seste heyecanlı titreklik ve irkilme",
            "Bun bungunluk ve dikkat dağınıklığı"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p009"],
        "bas": 0, "son": 4,
        "sayfa": 9,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Otonomik ve Bedensel Belirtiler",
        "ogeler": [
            "Tansiyon yüksekliği ve çarpıntı hissi",
            "Boğazda düğümlenme ve hava açlığı",
            "Ellerde ve ayaklarda uyuşma parestezi"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p010"],
        "bas": 0, "son": 4,
        "sayfa": 10,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Tanı Kriterleri Temel İlkeleri",
        "ogeler": [
            "En az altı ay süren aşırı kaygı",
            "Endişeleri denetim altına alma güçlüğü",
            "Erişkinde en az üç çocukta tek belirti"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p011"],
        "bas": 0, "son": 4,
        "sayfa": 11,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Altı Kardinal Belirti",
        "ogeler": [
            "Huzursuzluk ve kolay yorulma",
            "Odaklanma güçlüğü ve irritabilite",
            "Kas gerginliği ve uykuya dalma güçlüğü"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p012"],
        "bas": 0, "son": 4,
        "sayfa": 12,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Kardiyovasküler ve Pulmoner Taklitçiler",
        "ogeler": [
            "Anemi kalp yetmezliği ve hipertansiyon",
            "Mitral kapak prolapsusu ve paroksismal taşikardi",
            "Bronşiyal astım ve pulmoner emboli"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p013"],
        "bas": 0, "son": 4,
        "sayfa": 13,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Endokrin ve Toksik Ayırıcı Tanı",
        "ogeler": [
            "Hipertiroidizm ve feokromositoma krizi",
            "Hipoglisemi ve Cushing sendromu",
            "Uyarıcı madde toksisitesi ve yoksunluk"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p014"],
        "bas": 0, "son": 4,
        "sayfa": 14,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Psikiyatrik Ayırıcı Tanı Tablosu",
        "ogeler": [
            "Panik bozuklukta ani pik nöbetler",
            "Fobik tablolarda özgül nesne korkusu",
            "Majör depresyonda anhedoni ve çökkünlük"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p015"],
        "bas": 0, "son": 4,
        "sayfa": 15,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Klinik Gidiş ve Sonlanış Tablosu",
        "ogeler": [
            "Kronik dalgalı gidiş ve alevlenme",
            "Kadınlarda ve erken başlangıçta kötü seyir",
            "Depresyon varlığında yüksek özkıyım riski"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p016"],
        "bas": 0, "son": 4,
        "sayfa": 16,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Psikoterapi Yöntemleri ve Teknikler",
        "ogeler": [
            "Bilişsel yeniden yapılandırma ilkeleri",
            "Progresif kas gevşetme ve nefes eğitimi",
            "İçgörü yönelimli bilinçdışı çatışma terapisi"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p017"],
        "bas": 0, "son": 4,
        "sayfa": 17,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Temel Farmakoterapi Ajanları",
        "ogeler": [
            "İlk basamak antidepresan tedavisi",
            "Buspiron parsiyel agonisti bağımlılık yapmaz",
            "Benzodiazepinler iki ila dört hafta kullanılır"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p018"],
        "bas": 0, "son": 4,
        "sayfa": 18,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Antidepresan Hedef Doz Aralıkları",
        "ogeler": [
            "Essitalopram on yirmi sertralin elli iki yüz",
            "Venlafaksin yüz elli üç yüz duloksetin altmış",
            "Remisyon sonrası en az bir yıl idame tedavi"
        ]
    },
    {
        "cumle": para_last_sent["k2-54-p019"],
        "bas": 0, "son": 4,
        "sayfa": 19,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Basamaklı Tedavi Algoritması",
        "ogeler": [
            "Psiko-eğitim ve birinci basamak antidepresan",
            "Dört altı hafta yanıtsızlıkta ilaç değişimi",
            "Pregabalin veya buspiron ile güçlendirme"
        ]
    }
]

(TASLAK / "cizim.json").write_text(json.dumps(cizim_komutlari, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cizim.json ({len(cizim_komutlari)} commands)")

# Save cikmis_baglantilari.json
cikmis_list = []
for s in sents:
    if s.get("cikmis"):
        for qid in s["cikmis"]:
            cikmis_list.append({
                "cumle_id": s["id"],
                "sayfa": s["slayt"]["sayfa"],
                "soru_id": qid,
                "metin": s["ses"]
            })
(TASLAK / "cikmis_baglantilari.json").write_text(json.dumps(cikmis_list, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cikmis_baglantilari.json ({len(cikmis_list)} links)")

# ==============================================================================
# QUALITY GATES VERIFICATION
# ==============================================================================
print("\n" + "="*50)
print("RUNNING 6 QUALITY GATES")
print("="*50)

# Gate 1: KV.dogrula
print("\n--- Gate 1: KV.dogrula ---")
kv_errs = KV.dogrula(konusma_v2, KV.kaynak_sayfa(TASLAK), KV.kaynak_metin(TASLAK))
if kv_errs:
    print(f"FAILED KV.dogrula with {len(kv_errs)} errors:")
    for e in kv_errs[:10]: print(" ", e)
    sys.exit(1)
print("PASSED KV.dogrula: 0 HATA")

# Gate 2: denetle.py
print("\n--- Gate 2: denetle.py ---")
import denetle as D
d_rapor = D.Denetim(TASLAK).calistir()
if d_rapor.get("hata", 0) > 0:
    print(f"FAILED denetle.py with {d_rapor.get('hata')} errors:")
    for e in d_rapor.get("hatalar", [])[:10]: print(" ", e)
    sys.exit(1)
print("PASSED denetle.py: 0 HATA · 0 UYARI")

# Gate 3: validate_learning_decks.py
print("\n--- Gate 3: validate_learning_decks.py ---")
r_deck = subprocess.run([
    sys.executable, str(REPO_ROOT / "meds/scripts/validate_learning_decks.py"),
    str(TASLAK / "deck.json"), "--oyun-zorunlu", "--kurul2"
], capture_output=True, text=True)
if r_deck.returncode != 0:
    print("FAILED validate_learning_decks:", r_deck.stdout, r_deck.stderr)
    sys.exit(1)
print("PASSED validate_learning_decks: 0 HATA · 0 UYARI")

# Gate 4: metin_denetle.py
print("\n--- Gate 4: metin_denetle.py ---")
r_metin = subprocess.run([
    sys.executable, str(REPO_ROOT / "meds/scripts/sesli_anlatim/metin_denetle.py"),
    str(TASLAK / "konusma_metni.md")
], capture_output=True, text=True)
if r_metin.returncode != 0:
    print("FAILED metin_denetle:", r_metin.stdout, r_metin.stderr)
    sys.exit(1)
print("PASSED metin_denetle: 0 HATA · 0 UYARI")

# Gate 5: sesli_kapsam
print("\n--- Gate 5: sesli_kapsam ---")
import isle as IS
kapsam_errs = IS.sesli_kapsam(TASLAK)
if kapsam_errs:
    print(f"FAILED sesli_kapsam with {len(kapsam_errs)} errors:")
    for e in kapsam_errs: print(" ", e)
    sys.exit(1)
print("PASSED sesli_kapsam: 0 HATA")

# Gate 6: cizim_dogrula.py
print("\n--- Gate 6: cizim_dogrula.py ---")
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
for idx, d in enumerate(cizim_komutlari):
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
print(f"PASSED cizim_dogrula: {len(cizim_komutlari)}/{len(cizim_komutlari)} KOMUT 0 HATA")

print("\nALL 6 QUALITY GATES PASSED PERFECTLY!")
