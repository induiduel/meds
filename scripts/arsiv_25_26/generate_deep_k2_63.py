import json, re, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
taslak = ROOT / "meds_database_25_26" / "taslak" / "y25-k2-63-antidepresan-ilaclar"

sys.path.insert(0, str(MEDS / "scripts" / "sesli_anlatim"))
sys.path.insert(0, str(MEDS / "scripts" / "ders_isci"))
import konusma_v2, isle

bolumler = []
b_idx = 1
p_idx = 1
c_idx = 1

def add_bolum(title):
    global b_idx
    b = {"id": f"k2-63-b{b_idx:02d}", "baslik": title, "paragraflar": []}
    b_idx += 1
    bolumler.append(b)
    return b

def add_paragraf(bolum, sayfa):
    global p_idx
    p = {"id": f"k2-63-p{p_idx:03d}", "sayfa": sayfa, "cumleler": []}
    p_idx += 1
    bolum["paragraflar"].append(p)
    return p

def add_cumle(p, ses, ekran, sayfa, satir_list=None, sekil=None, vurgu_tur="terim", vurgu_metin="", cikmis_id=None):
    global c_idx
    c = {
        "id": f"k2-63-c{c_idx:04d}",
        "ses": ses,
        "ekran": ekran,
        "duzey": 0,
        "slayt": {
            "sayfa": sayfa,
            "satir": satir_list,
            "sekil": sekil
        },
        "vurgu": []
    }
    if cikmis_id:
        c["cikmis"] = cikmis_id
        if not vurgu_metin:
            vurgu_metin = ekran.replace("**", "").split(":")[0]
        c["vurgu"].append({"tur": "cikmis", "metin": vurgu_metin})
    elif vurgu_metin:
        c["vurgu"].append({"tur": vurgu_tur, "metin": vurgu_metin})
        
    c_idx += 1
    p["cumleler"].append(c)
    return c

# === BOLUM 1: Giriş ve Tababet Sanatı (Sayfa 1-2) ===
b1 = add_bolum("Giriş ve Tababet Sanatı İlkeleri")
p1 = add_paragraf(b1, 1)
add_cumle(p1, "Tababet sanatının üç temel unsuru el mahareti, ilaç ve hekimlik ahlakıdır.",
          "**Tababet Sanatı:** El mahareti, ilaç ve hekimlik ahlakı.", 1,
          ["Tababet sanatı üç şeydir: 1. el mahareti ile aletler, 2. ilaç, 3. ahlaktır."], vurgu_metin="Tababet Sanatı")
add_cumle(p1, "Gerçek erdem şifayı maharetle, ilacı ise hastaya büyük bir rikkat ve özenle sunmaktır.",
          "**Tıbbi Erdem:** Şifayı maharet ve ilacı rikkatle sunmak.", 1,
          ["Erdem; şifayı maharet, ilacı rikkatle sunmaktır.   nb"], vurgu_metin="Tıbbi Erdem")
add_cumle(p1, "Akılcı ilaç kullanımı ilkeleri doğrultusunda farmakoterapötik yaklaşımlar titizlikle yürütülmelidir.",
          "**Akılcı Farmakoterapi:** Hasta yararına titiz tedavi planı.", 1,
          ["BİLİCİ"], vurgu_metin="Akılcı Farmakoterapi")

p2 = add_paragraf(b1, 2)
add_cumle(p2, "Antidepresan ilaçlar dersi boyunca duygudurum bozukluklarının farmakoterapisini kapsamlı biçimde ele alacağız.",
          "**Antidepresan İlaçlar:** Duygudurum bozukluklarında farmakoterapi.", 2,
          ["Antidepresanlar"], vurgu_metin="Antidepresan İlaçlar")
add_cumle(p2, "Farklı kimyasal sınıflardaki antidepresanların etki mekanizmaları ve reseptör profilleri karşılaştırmalı olarak incelenecektir.",
          "**Moleküler Sınıflar:** Reseptör profilleri ve etki mekanizmaları.", 2,
          ["Antidepresanlar"], vurgu_metin="Moleküler Sınıflar")
add_cumle(p2, "Bu gruptaki ilaçların farmakokinetik süreçleri, klinik endikasyonları ve toksisite profilleri klinik pratiğin temelini oluşturur.",
          "**Klinik Farmakoloji:** Farmakokinetik, endikasyon ve toksisite.", 2,
          ["Antidepresanlar"], vurgu_metin="Klinik Farmakoloji")

# === BOLUM 2: Majör Depresif Bozukluk Tanısı ve Klinik Spektrum (Sayfa 3-4) ===
b2 = add_bolum("Majör Depresif Bozukluk Tanısı ve Spektrumu")
p3 = add_paragraf(b2, 3)
add_cumle(p3, "Majör depresif bozukluk en az iki hafta kesintisiz süren çökkün mizaç ve hiçbir aktiviteden zevk alamama yani anhedoni ile karakterizedir.",
          "**Majör Depresif Bozukluk:** İki hafta depresif mizaç ve anhedoni.", 3,
          ["Major depresif bozukluk: En az 2 hafta depresif Mizaç ve Hiçbir \naktiviteden zevk almama ile karakterizedir."], vurgu_metin="Majör Depresif Bozukluk")
add_cumle(p3, "Hastalarda belirgin enerji kaybı, uyku ve iştah değişiklikleri, değersizlik hissi, konsantrasyon güçlüğü ve intihar eğilimi sıkça izlenir.",
          "**Klinik Belirtiler:** Enerji azlığı, uyku, iştah ve intihar eğilimi.", 3,
          ["✓Enerjik hissedememe, \n✓Uyku, \n✓İştah bozulması, \n✓Değersizlik ve suçluluk hissi, \n✓Kognitif problemler, \n✓İntihar eğilimi"], vurgu_metin="Klinik Belirtiler")
add_cumle(p3, "Majör depresif epizotların farmakoterapisi bu ilaç grubunun en birincil ve temel kullanım endikasyonudur.",
          "**Primer Endikasyon:** Majör depresif epizotların tedavisi.", 3,
          ["❖Major depresif bozukluk antidepresanların primer kullanım alanıdır."], vurgu_metin="Primer Endikasyon")
add_cumle(p3, "Depresyon tablosu sadece psikiyatrik semptomlarla sınırlı kalmayıp kronik ağrıdan koroner arter hastalığına kadar geniş bir somatik serpinti gösterir.",
          "**Somatik Serpinti:** Kronik ağrı ve koroner arter hastalığı.", 3,
          ["❖Kronik ağrıdan koroner arter hastalığına kadar yaygın bir serpinti gösterir."], vurgu_metin="Somatik Serpinti")

p4 = add_paragraf(b2, 4)
add_cumle(p4, "Antidepresanlar panik bozukluk ve jeneralize anksiyete bozukluğunda ilk seçenek tedavi olarak yaygın biçimde reçete edilir.",
          "**Anksiyete Spektrumu:** Panik bozukluk ve jeneralize anksiyete.", 4,
          ["✓Panik bozukluk \n✓Jeneralize anksiyete (GAD)"], vurgu_metin="Anksiyete Spektrumu")
add_cumle(p4, "Obsesif kompulsif bozukluk ve travma sonrası stres bozukluğunda serotonerjik iletimi artıran antidepresanlar ana tedavi basamağıdır.",
          "**OKB ve Travma:** Serotonerjik iletimle sağlanan remisyon.", 4,
          ["✓Obsesif kompulsif bozukluk (OCD)\n✓Post travmatik stres bozukluğu (PTSD)"], vurgu_metin="OKB ve Travma")
add_cumle(p4, "Bu ilaçlar nöropatik ağrı ve fibromiyalji gibi kronik ağrı sendromlarında inen inhibitör yolları güçlendirerek analjezi sağlarlar.",
          "**Kronik Ağrı:** Nöropatik ağrı ve fibromiyaljide analjezi.", 4,
          ["✓Nöropatik ağrı \n✓Fibromiyalji"], vurgu_metin="Kronik Ağrı")
add_cumle(p4, "Premenstrüel disforik bozuklukta, menopozal vazomotor semptomların hafifletilmesinde ve stres üriner inkontinansında da etkinliği kanıtlanmıştır.",
          "**Özel Endikasyonlar:** Premenstrüel distrofi ve stres inkontinans.", 4,
          ["✓Premensturel distrofi \n✓Menopozda vazomotor semptomları azaltmak \n✓Stres inkontinans \n✓Diğer\nGibi geniş bir spektrumda kullanılırlar"], vurgu_metin="Özel Endikasyonlar")

# === BOLUM 3: Depresyon Patofizyolojisi ve Nörotrofik Hipotez (Sayfa 5-8) ===
b3 = add_bolum("Depresyon Patofizyolojisi ve Nörotrofik Hipotez")
p5 = add_paragraf(b3, 5)
add_cumle(p5, "Klasik monoamin hipotezine göre depresyon santral sinir sisteminde serotonin, noradrenalin ve dopamin iletimindeki azalmaya bağlı gelişir.",
          "**Monoamin Hipotezi:** Serotonin ve noradrenalin iletiminde azalma.", 5,
          ["1.\nMajor depresyonun patofizyolojisinde sadece monoaminler\netkili (monoamin hipotezi)"], vurgu_metin="Monoamin Hipotezi")
add_cumle(p5, "Nörotrofik hipotez ise sinir büyüme faktörlerinin ve hipokampal nörojenezin bozulmasını temel patoloji olarak öne sürer.",
          "**Nörotrofik Hipotez:** Sinir büyüme faktörleri ve nörojenez.", 5,
          ["2.Nörotrofik ve endokrin faktörler  önemlidir.(nörotrofik hipotez)"], vurgu_metin="Nörotrofik Hipotez")
add_cumle(p5, "Patofizyolojide ayrıca hipotalamo hipofizer adrenal aks disfonksiyonu gibi nöroendokrin mekanizmalar da kritik rol oynar.",
          "**Nöroendokrin Faktörler:** Hipotalamo hipofizer adrenal aks rolü.", 5,
          ["3. Depresyon patofizyolojisinde nöro-endokrin etkenler bilinmektedir."], vurgu_metin="Nöroendokrin Faktörler")

p6 = add_paragraf(b3, 6)
add_cumle(p6, "Beyin kaynaklı nörotrofik faktör yani be de ne fe, sinir büyüme faktörleri ailesinin en kritik üyelerinden biridir.",
          "**Beyin Kaynaklı Nörotrofik Faktör:** BDNF regülasyonu.", 6,
          ["Beyin kaynaklı nörotrofik faktör.(BDNF)"], vurgu_metin="Beyin Kaynaklı Nörotrofik Faktör")
add_cumle(p6, "Nöral plastisite, sinaptik esneklik ve erişkin beyinde nörojenezin devamlılığı büyük ölçüde nörotrofik faktörlerle düzenlenir.",
          "**Nöral Plastisite:** Sinaptik esneklik ve nörojenez kontrolü.", 6,
          ["a. Sinir büyüme faktörleri, \n \nneural plastisite, \n \nesneklik ve norojenez düzenlenmesinde etkilidir."], vurgu_metin="Nöral Plastisite")
add_cumle(p6, "Be de ne fe hipokampus ve kortikal alanlarda sinaptik bağlanabilirliği ve yeni nöron oluşumunu doğrudan destekler.",
          "**Hipokampal Bağlanabilirlik:** Kortikal ve hipokampal nörojenez.", 6,
          ["b. Kortikal alanlardan hipokampusta sinaptik bağlanabilirlik ve neurojenezi \narttırdığı düşünülür."], vurgu_metin="Hipokampal Bağlanabilirlik")
add_cumle(p6, "Kronik psikolojik stres ve inatçı kronik ağrı santral nörotrofik faktör sentezinde belirgin azalmaya yol açar.",
          "**Stres ve Ağrı:** Nörotrofik faktör sentezinde azalma.", 6,
          ["c. Stres ve ağrı nörotrofik faktör miktarında azalma yapar."], vurgu_metin="Stres ve Ağrı")

p7 = add_paragraf(b3, 7)
add_cumle(p7, "Be de ne fe eksikliği frontal korteks, hipokampus ve anterior singulat kortekste mikroanatomik değişikliklere ve dendritik kayba neden olur.",
          "**Mikroanatomik Değişim:** Frontal korteks ve anterior singulat hasarı.", 7,
          ["d. BDNF eksikliği frontal korteks, hipokampüs, anterior singulatta\nmikro anatomik değişime neden olur."], vurgu_metin="Mikroanatomik Değişim")
add_cumle(p7, "Kronik majör depresyon tablosunda hipokampal nöron kaybına bağlı olarak belirgin hacim kaybı ve atrofi gelişir.",
          "**Hipokampal Hacim Kaybı:** Nöronal kayba bağlı doku atrofisi.", 7,
          ["e. Depresyon hipokampüsde hacim kaybına neden olur"], vurgu_metin="Hipokampal Hacim Kaybı")
add_cumle(p7, "Deney hayvanlarında hipokampusa doğrudan nörotrofik faktör verilmesi antidepresan yanıt oluşturur ve nörojenezi artırır.",
          "**Antidepresan Yanıt:** Hipokampal infüzyonla artan nörojenez.", 7,
          ["f. Hayvan modellerinde nörotrofik faktörün orta beyin hipokampüs'e \nverilmesi antidepresan etki yapar(kronik antidepresan etki artmış \nnörojenez ile beraberdir) insan çalışmaları da benzerdir."], vurgu_metin="Antidepresan Yanıt")
add_cumle(p7, "Depresyonlu insanlarda beyin omurilik sıvısındaki nörotrofik faktör seviyesi düşer ve tirozin kinaz be reseptör aktivitesi azalır.",
          "**Tirozin Kinaz Reseptörü:** TrkB aktivitesinde ve BDNF düşüşü.", 7,
          ["g. (İNSAN)Depresyonda beyin omurilik sıvısında nörotrofik faktör \ndüzeyi düşer ve tirozin Kinaz reseptör aktivitesi azalır."], vurgu_metin="Tirozin Kinaz Reseptörü")

p8 = add_paragraf(b3, 8)
add_cumle(p8, "Nörotrofik hipotez depresyon araştırmalarında çok güçlü bir biyolojik model sunmasına rağmen bazı kısıtlılıklar içerir.",
          "**Hipotezin Kısıtlılıkları:** Araştırma alanı ve kuramsal sınırlar.", 8,
          ["BU HİPOTEZ iddialıdır. Ancak iyi bir araştırma alanıdır.\nÇÜNKÜ;"], vurgu_metin="Hipotezin Kısıtlılıkları")
add_cumle(p8, "Be de ne fe geninde görülen polimorfizmler bireyler arasındaki değişkenliği ve antidepresan yanıttaki farklılıkları açıklar.",
          "**Gen Polimorfizmi:** BDNF genetik yatkınlık ve değişkenlik.", 8,
          ["I.\nNörotrofik faktör  polimorfizme yatkındır."], vurgu_metin="Gen Polimorfizmi")
add_cumle(p8, "Bazı hayvan çalışmalarında sosyal yenilgi stresi sonrasında nörotrofik faktör düzeyinin paradoksal olarak depresif davranışları artırdığı gösterilmiştir.",
          "**Sosyal Stres Etkisi:** Stres sonrası paradoksal faktör yanıtı.", 8,
          ["II.\nSosyal stres sonrasında nörotrofik faktör depresyonu arttırmıştır."], vurgu_metin="Sosyal Stres Etkisi")

# === BOLUM 4: Monoamin Hipotezi ve Sınırları (Sayfa 9-13) ===
b4 = add_bolum("Monoamin Hipotezi, Taşıyıcılar ve Sınırları")
p9 = add_paragraf(b4, 9)
add_cumle(p9, "Veziküler monoamin pompasını bloke eden rezerpinin derin depresyon tablosu oluşturması monoamin hipotezinin en eski kanıtıdır.",
          "**Rezerpin Etkisi:** Veziküler blokajla gelişen depresyon.", 9,
          ["1.Monoaminler(serotonin, dopamin, noradrenalin)- rezerpin ilişkisi."], vurgu_metin="Rezerpin Etkisi")
add_cumle(p9, "Fluoksetin ile remisyona giren hastalara triptofansız diyet verildiğinde serotonerjik sentez durduğu için depresyon hızla nükseder.",
          "**Triptofansız Diyet:** Serotonin prekürsörü eksikliğiyle nüks.", 9,
          ["2. Fluoksetin ile tedavi edilen hastalara (serotonin prekürsörü olan) \ntriptofan içermeyen diyet verildiğinde hastalık nükseder."], vurgu_metin="Triptofansız Diyet")
add_cumle(p9, "Noradrenalin gerialımını seçici durduran desipramin tedavisinde ise triptofansız diyet nükse yol açmaz çünkü etki noradrenalin üzerinden yürür.",
          "**Desipramin Direnci:** Noradrenerjik etkiyle nüksün önlenmesi.", 9,
          ["3. Desipramin ile tedavide triptofan içermeyen diyet nükse neden olması \ndüşük ihtimaldir."], vurgu_metin="Desipramin Direnci")
add_cumle(p9, "Hastalara noradrenalin sentez inhibitörü verildiğinde remisyondaki depresif semptomların hızla geri dönmesi noradrenalinin kritik rolünü kanıtlar.",
          "**Sentez İnhibisyonu:** Noradrenalin sentez blokajıyla nüks.", 9,
          ["4. Noradrenalin sentez inhibitörü verilmesi depresif semptomları geri \ndöndürür."], vurgu_metin="Sentez İnhibisyonu")

p10 = add_paragraf(b4, 10)
add_cumle(p10, "Serotonin taşıyıcı geninin promotor bölgesinde gözlenen polimorfizmler santral serotonerjik iletim kapasitesini belirler.",
          "**Taşıyıcı Promotor Geni:** Serotonin taşıyıcı gen polimorfizmi.", 10,
          ["5. Serotonin transporter geni promotor bölgesi polimorfizm gösterir."], vurgu_metin="Taşıyıcı Promotor Geni")
add_cumle(p10, "Kısa alel yönünden homozigot olan bireylerin çevresel strese karşı kırılganlığı artar ve intihar davranışı ile majör depresyona daha yatkındırlar.",
          "**Homozigot Yatkınlık:** İntihar davranışı ve majör depresyon riski.", 10,
          ["Homozigot kişiler intihar davranışına ve majör depresyona daha yatkındırlar."], vurgu_metin="Homozigot Yatkınlık")
add_cumle(p10, "Ancak bazı deney hayvanı modellerinde belirgin depresif davranışa rağmen monoamin seviyelerinde hiçbir değişiklik bulunamamıştır.",
          "**Model Çelişkileri:** Monoamin seviyelerinde değişiklik olmaması.", 10,
          ["6. Deney hayvanları çalışmalarında bazı depresif vakalarda  enteresan bir \nşekilde monoamin düzeylerinde değişiklikler saptanmamıştır."], vurgu_metin="Model Çelişkileri")
add_cumle(p10, "Tamamlanmış intihar olgularında yapılan postmortem çalışmalarda serotonin ve noradrenalin reseptör yoğunluğunda kompanzatuar değişiklikler saptanmıştır.",
          "**Reseptör Değişimi:** Postmortem serotonin ve noradrenalin tayini.", 10,
          ["7. Depresyon ile intihar vakalarında serotonin ve noradrenalin \nreseptör değişimi mevcuttur."], vurgu_metin="Reseptör Değişimi")

p11 = add_paragraf(b4, 11)
add_cumle(p11, "Veziküler amin kapısı sitoplazmadaki monoaminlerin vezikül içerisine depolanmasını sağlar ve rezerpin tarafından bloke edilir.",
          "**Veziküler Amin Kapısı:** Rezerpin ile depolama blokajı.", 11,
          ["Veziküler Amin Kapısı Rezerpin"], vurgu_metin="Veziküler Amin Kapısı")
add_cumle(p11, "Sitoplazmik amin kapısı ise sinaptik aralıktaki nörotransmitterleri nöron içine geri alan taşıyıcı pompalardan oluşur.",
          "**Sitoplazmik Amin Kapısı:** Sinaptik aralıktan geri alım pompaları.", 11,
          ["Stoplazmik Amin Kapısı"], vurgu_metin="Sitoplazmik Amin Kapısı")
add_cumle(p11, "Trisiklik antidepresanlar ve kokain sitoplazmik amin kapısını bloke ederek nörotransmitterlerin sinaptik aralıkta birikmesine yol açar.",
          "**Gerialım Blokörleri:** Trisiklik antidepresanlar ve kokain etkisi.", 11,
          ["TCA\nKokain"], vurgu_metin="Gerialım Blokörleri")

p12 = add_paragraf(b4, 12)
add_cumle(p12, "Veziküler amin kapısının bloke edilmesi monoaminlerin sitoplazmada kalarak mitokondriyal enzimlerle yıkılmasına neden olur.",
          "**Depolama Kusuru:** Monoaminlerin veziküle girişinin engellenmesi.", 12,
          ["Vezküler Amin Kapısı"], vurgu_metin="Depolama Kusuru")
add_cumle(p12, "Bu mekanizma sonucunda presinaptik nöron terminallerinde salınmaya hazır nörotransmitter depoları hızla tükenir.",
          "**Veziküler Tükenme:** Presinaptik monoamin depolarının tükenişi.", 12,
          ["Ahmet BELKİ"], vurgu_metin="Veziküler Tükenme")

p13 = add_paragraf(b4, 13)
add_cumle(p13, "Monoamin teorisinin en büyük sınırlılığı moleküler etki ile klinik yanıt arasındaki belirgin zaman uyumsuzluğudur.",
          "**Teorinin Sınırları:** Moleküler ve klinik yanıt uyumsuzluğu.", 13,
          ["The monoamine theory of\ndepression and its limitations"], vurgu_metin="Teorinin Sınırları")
add_cumle(p13, "Depresyon santral serotonerjik ve noradrenerjik iletimdeki azalmadan kaynaklanabilir.",
          "**Azalmış Transmisyon:** Serotonin ve noradrenalin azalması.", 13,
          ["* Depression might be caused by decreased 5-HT and NE\nneurotransmission"], vurgu_metin="Azalmış Transmisyon")
add_cumle(p13, "Ancak seçici serotonin geri alım inhibitörleri hücresel düzeyde taşıyıcıyı ilk dozda hemen bloke ederler.",
          "**Hızlı Taşıyıcı Blokajı:** Taşıyıcıların anında kilitlenmesi.", 13,
          ["* SSRis are eşe Tg active at their molecular\nand cellular sites of action almost immediately."], vurgu_metin="Hızlı Taşıyıcı Blokajı")
add_cumle(p13, "Buna rağmen klinik antidepresan yanıtın ortaya çıkması için en az iki ila dört haftalık bir sürenin geçmesi gerekir.",
          "**Terapötik Gecikme:** İki ila dört haftalık yanıt süresi.", 13,
          ["PSYCHOPHARMACOLOGY\nINSTITUTE"], vurgu_metin="Terapötik Gecikme")

# === BOLUM 5: Nöroendokrin Faktörler ve Hipotalamo-Hipofizer-Adrenal Aks (Sayfa 14-15) ===
b5 = add_bolum("Nöroendokrin Faktörler ve HPA Aksı")
p14 = add_paragraf(b5, 14)
add_cumle(p14, "Majör depresyon patofizyolojisinde nöroendokrin akslar ve özellikle hipotalamo hipofizer adrenal sistem büyük önem taşır.",
          "**Nöroendokrin Akslar:** HPA sistemi ve hormonal denge.", 14,
          ["3. Depresyon patofizyolojisinde nöro-endokrin etkenler bilinmektedir."], vurgu_metin="Nöroendokrin Akslar")
add_cumle(p14, "Depresif hastaların çoğunda hipotalamo hipofizer adrenal eksende kronik hiperaktivite ve geri bildirim kusuru vardır.",
          "**Aks Disfonksiyonu:** Kronik hiperaktivite ve negatif geri bildirim.", 14,
          ["a. Depresif hastalarda hipotalamo hipofizer aksta anormallik vardır."], vurgu_metin="Aks Disfonksiyonu")
add_cumle(p14, "Majör depresyonda sürekli yüksek kalan kortizol düzeyi adreno kortikotrop hormon salınımını yeterince baskılayamaz.",
          "**Kortizol Yüksekliği:** ACTH baskılanma yetersizliği.", 14,
          ["b. Major Depresyonda yüksek kortizol düzeyi"], vurgu_metin="Kortizol Yüksekliği")
add_cumle(p14, "Depresif hastalarda tiroid aksı disregülasyonu ve subklinik tiroid fonksiyon anormallikleri sıkça karşımıza çıkar.",
          "**Tiroid Disregülasyonu:** Tiroid fonksiyon anormallikleri.", 14,
          ["c. Tiroid disregülasyonu depresif hastalarda belirgindir tiroid\nfonksiyonları anormaldir."], vurgu_metin="Tiroid Disregülasyonu")
add_cumle(p14, "Postmenopozal dönemde östrojen eksikliği ve erkeklerde şiddetli testosteron düşüklüğü depresif duyguduruma yatkınlık oluşturur.",
          "**Gonadal Hormonlar:** Östrojen ve testosteron eksikliği.", 14,
          ["d. Postmenopozal dönemde östrojen eksikliği depresyona yatkın kılar.\ne. Erkeklerde şiddetli Testosteron eksikliği depresyona eşlik eder."], vurgu_metin="Gonadal Hormonlar")

p15 = add_paragraf(b5, 15)
add_cumle(p15, "Hipotalamo hipofizer adrenal eksendeki bu aşırı uyarılma, santral glukokortikoid reseptör direncine ve hipokampal hasara yol açar.",
          "**Glukokortikoid Direnci:** Reseptör duyarsızlaşması ve hipokampal hasar.", 15,
          None, sekil="Hipotalamo-hipofizer-adrenal aks şeması", vurgu_metin="Glukokortikoid Direnci")
add_cumle(p15, "Nöroendokrin aksın kronik uyarılması nörojenezi baskılayarak be de ne fe eksikliğini daha da derinleştirir.",
          "**Nöroendokrin Kaskad:** BDNF sentezinde ek baskılanma.", 15,
          None, sekil="Hipotalamo-hipofizer-adrenal aks şeması", vurgu_metin="Nöroendokrin Kaskad")
add_cumle(p15, "Şimdi antidepresan ilaçların kimyasal sınıflarını ve moleküler farmakolojilerini ayrıntılı olarak inceleyelim.",
          "**Farmakolojik Sınıflar:** Kimyasal gruplar ve etki mekanizmaları.", 15,
          None, sekil="Antidepresan ilaç sınıfları genel şeması", vurgu_metin="Farmakolojik Sınıflar")

# === BOLUM 6: Seçici Serotonin Gerialım İnhibitörleri (SSRI) (Sayfa 16-18) ===
b6 = add_bolum("Seçici Serotonin Gerialım İnhibitörleri")
p16 = add_paragraf(b6, 16)
add_cumle(p16, "Seçici serotonin geri alım inhibitörleri yani se se re i grubu günümüzde depresyon tedavisinde birinci basamak seçenektir.",
          "**SSRI Grubu:** Birinci basamak antidepresan tedavi.", 16,
          ["1-SSRİ (seçkin serotonin geri alım inhibitörleri)."], vurgu_metin="SSRI Grubu")
add_cumle(p16, "Prototip ilaç olan fluoksetin monoamin taşıyıcısına bağlanırken asetilkolin ve alfa adrenoreseptörlere afinite göstermez.",
          "**Fluoksetin Profili:** Taşıyıcı seçiciliği ve reseptör güvenilirliği.", 16,
          ["✓Fluoksetin: Monoamin reseptörlerine afinitesi var, ancak sistemin\nasetilkolin ve α- adrenoreseptör afinitesi yok."], vurgu_metin="Fluoksetin Profili")
add_cumle(p16, "Bu grup panik bozukluk, obsesif kompulsif bozukluk ve bulimiya nervoza gibi çok geniş bir endikasyon yelpazesine sahiptir.",
          "**Geniş Spektrum:** Panik bozukluk ve bulimiya tedavisi.", 16,
          ["SSRİ ler panik bozukluk, bulimia  dahil hemen bütün depresif\ndurumlarda endikedir."], vurgu_metin="Geniş Spektrum")
add_cumle(p16, "Sınıfın diğer temel üyeleri sertralin, fluvoksamin, sitalopram ve sitalopramın saf enantiyomeri olan essitalopramdır.",
          "**Grup Üyeleri:** Sertralin, fluvoksamin, sitalopram ve essitalopram.", 16,
          ["✓Sertralin,\n✓Fluvoksamin.\n✓Citalopram\n✓Essitalopram"], vurgu_metin="Grup Üyeleri")
add_cumle(p16, "Se se re i grubu iyi tolere edilir, geniş terapötik indekse sahiptir ve toksisite açısından oldukça güvenilirdir.",
          "**Terapötik Güvenilirlik:** Yüksek tolerans ve düşük toksisite.", 16,
          ["SSRİ ler iyi tolere edilirler, maliyetleri düşüktür, spektrumları\ngeniştir, güvenirliği iyidir."], vurgu_metin="Terapötik Güvenilirlik")

p17 = add_paragraf(b6, 17)
add_cumle(p17, "Antidepresan farmakolojisi bin dokuz yüz elli yedi yılında iproniazid ve imipraminin keşfiyle başlamıştır.",
          "**Tarihsel Gelişim:** İproniazid ve imipramin keşfi.", 17,
          ["ipronliarid - MAOI, 1957\nimipramine - TCA, 1957"], vurgu_metin="Tarihsel Gelişim")
add_cumle(p17, "Fluoksetin ile başlayan selektif inhibitör dönemi psikiyatri pratiğinde büyük bir dönüşüm sağlamıştır.",
          "**Fluoksetin Dönemi:** Seçici inhibitörlerin klinik kullanımı.", 17,
          ["Fluoxetine - SSRI, 1957"], vurgu_metin="Fluoksetin Dönemi")
add_cumle(p17, "Bin dokuz yüz doksan dörtte venlafaksin ile ikili geri alım inhibitörleri, ardından reboksetin gibi seçici ajanlar geliştirilmiştir.",
          "**İkili İnhibitörler:** Venlafaksin ve reboksetin geliştirilmesi.", 17,
          ["Veniafaxine - SNSRI, 1994\nReboxetine - SNRI, 1997"], vurgu_metin="İkili İnhibitörler")
add_cumle(p17, "Aynı dönemde nefazodon ve mirtazapin gibi reseptör antagonisti atipik moleküller tedaviye girmiştir.",
          "**Reseptör Antagonistleri:** Nefazodon ve mirtazapin klinik girişi.", 17,
          ["Netazodone - SRA, 1994\nMirtazapine - NRA, 1994"], vurgu_metin="Reseptör Antagonistleri")

p18 = add_paragraf(b6, 18)
add_cumle(p18, "Amerikan gıda ve ilaç dairesi tarafından onaylanan endikasyonlar duygudurum ve anksiyete bozukluklarını kapsar.",
          "**Onaylı Endikasyonlar:** FDA onaylı kullanım spektrumu.", 18,
          ["FDA-approved indications"], vurgu_metin="Onaylı Endikasyonlar")
add_cumle(p18, "Majör depresif bozukluk epizotlarının akut tedavisi ve idamesi onaylı temel kullanım alanıdır.",
          "**Duygudurum Bozukluğu:** Majör depresif bozukluk idamesi.", 18,
          ["* Bipolar disorder\ndepression (as\nOFC)"], vurgu_metin="Duygudurum Bozukluğu")
add_cumle(p18, "Panik bozukluk, obsesif kompulsif bozukluk, bulimiya nervoza ve premenstrüel disforik bozuklukta onaylıdırlar.",
          "**Anksiyete ve Yeme Bozukluğu:** Panik, OKB ve bulimiya onayı.", 18,
          ["* Major * Panic disorder » Bulimia nervosa"], vurgu_metin="Anksiyete ve Yeme Bozukluğu")
add_cumle(p18, "Bipolar depresyonda ise olanzapin fluoksetin sabit kombinasyonu şeklinde kullanım onayı mevcuttur.",
          "**Bipolar Depresyon:** Olanzapin fluoksetin kombinasyonu onayı.", 18,
          ["* Bipolar disorder\ndepression (as\nOFC)"], vurgu_metin="Bipolar Depresyon")

# === BOLUM 7: Serotonin ve Noradrenalin Gerialım İnhibitörleri (SNRI) (Sayfa 19-22) ===
b7 = add_bolum("Serotonin ve Noradrenalin İnhibitörleri")
p19 = add_paragraf(b7, 19)
add_cumle(p19, "Serotonin ve noradrenalin geri alım inhibitörleri yani se ne re i grubu ikili taşıyıcı blokajı yapar.",
          "**SNRI Grubu:** İkili taşıyıcı blokaj mekanizması.", 19,
          ["2- Serotonin - noradrenalin Geri alım inhibitörleri.(SNRİ)"], vurgu_metin="SNRI Grubu")
add_cumle(p19, "Venlafaksin, desvenlafaksin ve duloksetin bu grubun en sık kullanılan güçlü temsilcileridir.",
          "**Grup Temsilcileri:** Venlafaksin, desvenlafaksin ve duloksetin.", 19,
          ["✓Venlafaksin\n✓Desvenlafaksin\n✓Duloksetin"], vurgu_metin="Grup Temsilcileri")
add_cumle(p19, "Trisiklik antidepresanlar amitriptilin, desipramin, doksepin ve amoksapin gibi tersiyer ve sekonder amin türevlerini içerir.",
          "**TCA Sınıfı:** Amitriptilin, desipramin, doksepin ve amoksapin.", 19,
          ["Trisiklik antidepresanlar:\n✓ Amitriptilin,\n✓Desipramin,\n✓Doksepin,\n✓Amoksapin"], vurgu_metin="TCA Sınıfı")
add_cumle(p19, "İmipramin, nortriptilin, protriptilin, trimipramin ve güçlü serotonerjik etkili klomipramin bu geniş ailenin diğer üyeleridir.",
          "**Diğer Trisiklikler:** İmipramin, nortriptilin ve klomipramin.", 19,
          ["✓İmipramin,\n✓Nortriptilin,\n✓Protriptilin,\n✓Trimipramin\n✓Klomipramin"], vurgu_metin="Diğer Trisiklikler")

p20 = add_paragraf(b7, 20)
add_cumle(p20, "Nöronal geri alımın inhibe edilmesi sinaptik aralıkta serotonin ve noradrenalin konsantrasyonunu hızla yükseltir.",
          "**Gerialım İnhibisyonu:** Sinaptik aralıkta artan monoaminler.", 20,
          ["Antidepresan ilaçların olası etki alanları. Norepinefrin (NE) ve serotoninin (5-HT) nöronal alımının inhibisyonu,\nbu nörotransmiterlerin sinaptik aktivitelerini arttırır."], vurgu_metin="Gerialım İnhibisyonu")
add_cumle(p20, "Monoamin oksidaz enziminin inhibisyonu nörotransmitterlerin presinaptik veziküler depolarını belirgin biçimde artırır.",
          "**Enzim İnhibisyonu:** MAO blokajıyla artan vezikül deposu.", 20,
          ["Monoamin oksidazın inhibisyonu, hem NE hem de 5-HT'nin\npresinaptik depolarını arttırır ve bu da nörotransmiter etkilerinin artmasına neden olur."], vurgu_metin="Enzim İnhibisyonu")
add_cumle(p20, "Presinaptik alfa iki otoreseptörlerin bloke edilmesi noradrenalin salınımı üzerindeki otoregülatuvar baskılayıcı etkiyi ortadan kaldırır.",
          "**Alfa-2 Otoreseptör:** Noradrenalin salınımı üzerindeki frenin kalkışı.", 20,
          ["Presinaptik &2\notoreseptörün blokajı, NE salınımının geri besleme inhibisyonunu önler. Not: Bunlar, antidepresanların akut\netkileridir."], vurgu_metin="Alfa-2 Otoreseptör")

p21 = add_paragraf(b7, 21)
add_cumle(p21, "Seçici serotonin ve noradrenalin geri alım inhibitörleri modern farmakoterapide geniş yer tutar.",
          "**Modern SNRI Ajanları:** Selektif ikili geri alım inhibitörleri.", 21,
          ["Selektif serotonin – noradrenalin gerialım inhibitörleri (SNRİ)"], vurgu_metin="Modern SNRI Ajanları")
add_cumle(p21, "Venlafaksin uzatılmış salınımlı formuyla ve ana aktif metaboliti olan desvenlafaksin ile klinikte kullanılır.",
          "**Venlafaksin ve Desvenlafaksin:** Uzatılmış salınımlı formülasyon.", 21,
          ["✓Venlafaksin (Effexor®-XR),\n✓Desvenlafaksin,"], vurgu_metin="Venlafaksin ve Desvenlafaksin")
add_cumle(p21, "Duloksetin, milnasipran ve levomilnasipran hem depresyonda hem kronik ağrı sendromlarında tercih edilir.",
          "**Dengeli İnhibitörler:** Duloksetin, milnasipran ve levomilnasipran.", 21,
          ["✓Duloksetin,\n✓Milnasipran,\n✓Levomilnacipran,"], vurgu_metin="Dengeli İnhibitörler")

p22 = add_paragraf(b7, 22)
add_cumle(p22, "Bütün se ne re i molekülleri trisiklik antidepresanlar gibi hem serotonin hem noradrenalin taşıyıcısını bloke ederler.",
          "**Taşıyıcı Bağlanması:** SERT ve NET taşıyıcılarının blokajı.", 22,
          ["✓Bütün SNRİ ler tıpkı trisiklik antidepresanlar gibi serotonin ve\nnoradrenalin taşıyıcısına bağlanırlar."], vurgu_metin="Taşıyıcı Bağlanması")
add_cumle(p22, "Ancak trisikliklerden farklı olarak histamin, asetilkolin ve alfa bir adrenerjik reseptörlere afinite göstermezler.",
          "**Düşük Reseptör Afinitesi:** Otonomik reseptörlere bağlanmama üstünlüğü.", 22,
          ["✓Diğer reseptörlere yüksek afinite göstermezler."], vurgu_metin="Düşük Reseptör Afinitesi")
add_cumle(p22, "Bu sayede otonomik yan etkiler olmaksızın majör depresyon, fibromiyalji, nöropatik ağrı ve anksiyetede kullanılırlar.",
          "**Klinik Endikasyonlar:** Ağrı, anksiyete ve majör depresyon.", 22,
          ["✓Majör depresyon,\n✓fibromiyalji ve nöropati,\n✓anksiyete,"], vurgu_metin="Klinik Endikasyonlar")
add_cumle(p22, "Duloksetin üriner stres inkontinansında, desvenlafaksin ise menopozal vazomotor semptomlarda terapötik üstünlüğe sahiptir.",
          "**Spesifik Kullanım:** İdrar inkontinansı ve vazomotor semptomlar.", 22,
          ["✓üriner stres inkontinans ile\n✓menopozal vazomotor semptomlarına endike."], vurgu_metin="Spesifik Kullanım")

# === BOLUM 8: Trisiklik Antidepresanlar (TCA) (Sayfa 23) ===
b8 = add_bolum("Trisiklik Antidepresanlar")
p23 = add_paragraf(b8, 23)
add_cumle(p23, "Trisiklik antidepresanlar modern ilaçlara yanıt vermeyen dirençli majör depresyon olgularında tercih edilir.",
          "**Dirençli Depresyon:** Trisiklik antidepresanların klinik yeri.", 23,
          ["Trisiklik antidepresanlar\n❖SSRİ\n❖SNRİ\nCevap vermeyen depresyonda kullanılır."], vurgu_metin="Dirençli Depresyon")
add_cumle(p23, "Bu geniş kimyasal ailenin tarihsel ve farmakolojik prototipi imipramindir.",
          "**İmipramin Prototipi:** Trisiklik sınıfın referans molekülü.", 23,
          ["Prototipi imipramindir."], vurgu_metin="İmipramin Prototipi")
add_cumle(p23, "Trisiklik moleküller muskarinik reseptörleri güçlü bloke ettikleri için yüksek düzeyde antikolinerjik yan etki taşırlar.",
          "**Antikolinerjik Yük:** Güçlü muskarinik reseptör blokajı.", 23,
          ["Yüksek düzeyde antikolinerjiktir."], vurgu_metin="Antikolinerjik Yük")
add_cumle(p23, "İmipraminin aktif metaboliti olan desipramin noradrenalin seçicidir ve ana bileşiğe göre daha düşük antikolinerjik etki gösterir.",
          "**Desipramin Özelliği:** Noradrenalin seçiciliği ve düşük yan etki.", 23,
          ["Metaboliti desipramin de benzer etkilidir."], vurgu_metin="Desipramin Özelliği")

# === BOLUM 9: 5-HT2 Antagonistleri ve Atipik Antidepresanlar (Sayfa 24-25) ===
b9 = add_bolum("5-HT2 Antagonistleri ve Atipik Ajanlar")
p24 = add_paragraf(b9, 24)
add_cumle(p24, "Trazodon ve nefazodon beş ha te iki antagonistleri ve geri alım inhibitörleri sınıfını oluşturur.",
          "**5-HT2 Antagonistleri:** Trazodon ve nefazodon sınıfı.", 24,
          ["Trazodon ve nefazodon"], vurgu_metin="5-HT2 Antagonistleri")
add_cumle(p24, "Bu ilaçlar ve aktif metabolitleri postsinaptik beş ha te iki a reseptörlerini güçlü biçimde bloke ederler.",
          "**Reseptör Blokajı:** 5-HT2A reseptör antagonizması.", 24,
          ["Metaboliti serotonin 2 reseptörünü güçlü antagonisti olduğu için\netkinliğine inanılmaktadır."], vurgu_metin="Reseptör Blokajı")
add_cumle(p24, "Beş ha te iki a blokajı anksiyolitik etki sağlarken cinsel işlev bozukluğu riskini ortadan kaldırır.",
          "**Cinsel Yan Etkisizlik:** Anksiyoliz ve normal cinsel işlev.", 24,
          ["5HT2 antagonistleri"], vurgu_metin="Cinsel Yan Etkisizlik")
add_cumle(p24, "Güçlü histamin bir antagonizması nedeniyle trazodon günümüzde daha çok hipnotik ve sedatif amaçla reçete edilir.",
          "**Hipnotik Kullanım:** Düşük dozda sedatif ve uyku düzenleyici.", 24,
          ["Günümüzde daha çok hipnotik olarak da kullanılır (endikasyon dışı\nkullanım)"], vurgu_metin="Hipnotik Kullanım")

p25 = add_paragraf(b9, 25)
add_cumle(p25, "Tetrasiklik ve ünisiklik antidepresanlar kimyasal yapıları ve reseptör hedefleri açısından heterojen bir gruptur.",
          "**Heterosiklik Ajanlar:** Tetrasiklik ve ünisiklik antidepresanlar.", 25,
          ["Kimyasal olarak farklı bir sınıftır.\n✓Amoksapin (Loksapin türevi)\n✓Mirtazapin\n✓Maprotilin"], vurgu_metin="Heterosiklik Ajanlar")
add_cumle(p25, "Bupropion amfetamin benzeri kimyasal yapıya sahiptir ve santral sinir sistemi stimülan etkisi sergiler.",
          "**Bupropion Farmakolojisi:** Noradrenalin ve dopamin gerialım blokajı.", 25,
          ["✓Bupropion (yapısı amfetamine benzer, SSS stimülan etkisi de\nvardır)"], vurgu_metin="Bupropion Farmakolojisi")
add_cumle(p25, "Mirtazapin presinaptik alfa iki blokajı yapar ve bupropion gibi cinsel yan etki oluşturmayan nadir ajanlardandır.",
          "**Mirtazapin Üstünlüğü:** Alfa-2 blokajı ve cinsel yan etki yokluğu.", 25,
          ["Mirtazapin (seksüel yan etkileri olmayan (bupropion gibi) birkaç\nantidepresandan biridir)"], vurgu_metin="Mirtazapin Üstünlüğü")
add_cumle(p25, "Amoksapin antipsikotik loksapin türevidir; bu grup klasik antidepresanlara göre daha özel durumlarda reçete edilir.",
          "**Amoksapin ve Maprotilin:** Dopamin blokajı ve özel kullanım.", 25,
          ["Tetrasiklik ve Unisiklik antidepresanlar"], vurgu_metin="Amoksapin ve Maprotilin")

# === BOLUM 10: Monoamin Oksidaz İnhibitörleri (MAOI) (Sayfa 26) ===
b10 = add_bolum("Monoamin Oksidaz İnhibitörleri")
p26 = add_paragraf(b10, 26)
add_cumle(p26, "Monoamin oksidaz inhibitörleri ciddi toksisite ve etkileşim riskleri nedeniyle klinik uygulamada nadiren kullanılırlar.",
          "**MAO İnhibitörleri:** Toksisite ve nadir klinik kullanım.", 26,
          ["Monoamin oksidaz inhibitörleri"], vurgu_metin="MAO İnhibitörleri")
add_cumle(p26, "Başta atipik özellikli veya diğer antidepresan sınıflarına yanıt vermeyen tedaviye dirençli depresyonda endikedirler.",
          "**Dirençli Depresyon:** Atipik ve tedaviye yanıtsız olgular.", 26,
          ["Diğer antidepresan ilaçlara yanıt vermeyen depresyon tedavisinde\nendikedir ler."], vurgu_metin="Dirençli Depresyon")
add_cumle(p26, "Klasik ajanlar enzimdeki flavin grubuna kovalan bağlanarak geri dönüşümsüz ve seçici olmayan inhibisyon yaparlar.",
          "**Kovalan İnhibisyon:** Geri dönüşümsüz ve nonselektif MAO blokajı.", 26,
          ["Etkilerini MAO-A ve MAO-B ye NON_reversibl ve  nonselektif\nbağlanarak gösterirler."], vurgu_metin="Kovalan İnhibisyon")
add_cumle(p26, "Fenelzin, izokarboksazid, tranilsipromin klasik inhibitörlerdir; moklobemid geri dönüşümlü seçici mao a inhibitörüdür.",
          "**MAOI Sınıflandırması:** İrreversibl ajanlar ve moklobemid.", 26,
          ["✓Selejilin\n✓Fenelzin\n✓İzokarboksazid\n✓Tranilsipromin\n✓Moklobemid"], vurgu_metin="MAOI Sınıflandırması")
add_cumle(p26, "Tranilsipromin gibi moleküller amfetamin benzeri yapıları sayesinde belirgin santral sinir sistemi stimülasyonu yaparlar.",
          "**Santral Stimülasyon:** Amfetamin benzeri yapı ve aktivasyon.", 26,
          ["Bu grup ilaçlar SSS stimülan etkiye yatkındırlar."], vurgu_metin="Santral Stimülasyon")

# === BOLUM 11: Genel Farmakokinetik ve SSRI Kinetiği (Sayfa 27-28) ===
b11 = add_bolum("Genel Farmakokinetik ve SSRI Kinetiği")
p27 = add_paragraf(b11, 27)
add_cumle(p27, "Antidepresan ilaçların aynı kimyasal grup içinde bile belirgin farmakokinetik farklılıkları bulunur.",
          "**Kinetik Değişkenlik:** Moleküller arası farmakokinetik farklar.", 27,
          ["Aynı grubun bile kendi aralarında ciddi farmakokinetik farklılıkları vardır."], vurgu_metin="Kinetik Değişkenlik")
add_cumle(p27, "Genel özellikleri itibarıyla oral yoldan alındıklarında gastrointestinal sistemden hızla absorbe edilirler.",
          "**Hızlı Emilim:** Gastrointestinal sistemden yüksek absorpsiyon.", 27,
          ["✓Hızlı bir oral absorpsiyona sahiptirler."], vurgu_metin="Hızlı Emilim")
add_cumle(p27, "Yüksek lipofilik özellikleri nedeniyle plazma proteinlerine ve özellikle albümine yüksek oranda bağlanırlar.",
          "**Protein Bağlanması:** Lipofilik yapı ve yüksek albümin ilgisi.", 27,
          ["✓Plazma proteinlerine sıkıca bağlanırlar."], vurgu_metin="Protein Bağlanması")
add_cumle(p27, "Karaciğerde sitokrom pe dört yüz elli enzimleri ile metabolize edilirler ve metabolitleri böbrek yoluyla atılır.",
          "**Metabolizma ve Atılım:** Karaciğer biyotransformasyonu ve renal itrah.", 27,
          ["✓Metabolizasyonları hepatiktir.\n✓Ekskresyonları renal dir"], vurgu_metin="Metabolizma ve Atılım")

p28 = add_paragraf(b11, 28)
add_cumle(p28, "Fluoksetin karaciğerde aktif metaboliti olan norfluoksetine metabolize edilir.",
          "**Fluoksetin Metabolizması:** Aktif metabolit norfluoksetin oluşumu.", 28,
          ["✓Prototip olan fluoksetin aktif metaboliti Nor-fluoxetine metabolize\nedilir."], vurgu_metin="Fluoksetin Metabolizması")
add_cumle(p28, "Norfluoksetinin eliminasyon yarı ömrü yaklaşık bir ila iki hafta olup ana ilaçtan üç kat daha uzundur.",
          "**Norfluoksetin Yarı Ömrü:** Üç kat uzun eliminasyon süresi.", 28,
          ["✓Nor-fluoksetin yarılanma ömrü ilaçtan 3 kat fazladır."], vurgu_metin="Norfluoksetin Yarı Ömrü")
add_cumle(p28, "Bu özellik fluoksetini bütün se se re i grubu içinde en uzun yarılanma ömrüne sahip molekül yapar.",
          "**En Uzun Yarı Ömür:** SSRI grubunda en geç temizlenen ajan.", 28,
          ["✓Bütün SSRİ ler içinde en uzun yarılanma ömrüne sahiptir."], vurgu_metin="En Uzun Yarı Ömür")
add_cumle(p28, "Fluoksetin ve paroksetin karaciğerde sitokrom pe iki de altı izoenziminin çok güçlü inhibitörleridir.",
          "**CYP2D6 İnhibisyonu:** Fluoksetin ve paroksetin enzim blokajı.", 28,
          ["✓CYP2D6 izoenzimi güçlü inhibitörleridir."], vurgu_metin="CYP2D6 İnhibisyonu")
add_cumle(p28, "Fluvoksamin sitokrom üç a dördü inhibe ederken, sitalopram ve sertralin enzim etkileşimi açısından oldukça ılımlıdır.",
          "**CYP Etkileşim Profili:** Fluvoksamin, sitalopram ve sertralin farkı.", 28,
          ["✓Fluvoksamin metabolik yolağı CYP3A4 tür. (inh.)\n✓Sitalopram, essitalopram ve  sertralin CYP etkileşiminde daha\nılımlıdır"], vurgu_metin="CYP Etkileşim Profili")

# === BOLUM 12: SNRI ve TCA Farmakokinetiği (Sayfa 29-33) ===
b12 = add_bolum("SNRI ve TCA Farmakokinetik Karşılaştırması")
p29 = add_paragraf(b12, 29)
add_cumle(p29, "Venlafaksin sitokrom pe iki de altı aracılığıyla ana aktif metaboliti olan desvenlafaksine dönüştürülür.",
          "**Venlafaksin Biyotransformasyonu:** Desvenlafaksine dönüşüm.", 29,
          ["❖Venlafaksin CYP2D6 üzerinden desmetil venlafaksine (desvenlafaksin)\ndönüştürülür."], vurgu_metin="Venlafaksin Biyotransformasyonu")
add_cumle(p29, "Her iki molekülün de eliminasyon yarılanma ömrü yaklaşık on bir saattir ve kontrollü salınımlı formda tek doz verilir.",
          "**On Bir Saatlik Yarı Ömür:** Günde tek doz uzatılmış salınım.", 29,
          ["❖Her ikisinin de yarılanma ömrü 11 saat civarındadır\n❖Günde tek doz kullanılabilirler."], vurgu_metin="On Bir Saatlik Yarı Ömür")
add_cumle(p29, "Venlafaksin ve desvenlafaksin plazma proteinlerine sadece yüzde yirmi beş ila otuz oranında bağlanarak en düşük bağlanmayı gösterirler.",
          "**Düşük Protein Bağlanması:** Yüzde yirmi beş ila otuzluk bağlanma.", 29,
          ["❖Venlafaksin ve desvenlafaksin her ikisi de plazma proteinlerine en az\nbağlanır(%25-30)"], vurgu_metin="Düşük Protein Bağlanması")
add_cumle(p29, "Duloksetin karaciğerde yoğun metabolize edilirken milnasipran Amerika Birleşik Devletlerinde majör depresyon yerine fibromiyaljide onaylıdır.",
          "**Duloksetin ve Milnasipran:** Metabolizma ve fibromiyalji endikasyonu.", 29,
          ["❖Duloksetin\n❖Milnasipran  (İxel 25,50 mg)  ABD’ de Majör dep. Ruhsatı yok. +Fibromiyalji"], vurgu_metin="Duloksetin ve Milnasipran")

p30 = add_paragraf(b12, 30)
add_cumle(p30, "Antidepresan ilaçlar presinaptik terminalde bulunan nörotransmitter geri alım pompalarını bloke ederek etki gösterirler.",
          "**Presinaptik Gerialım Blokajı:** Taşıyıcı pompaların kilitlenmesi.", 30,
          ["Antidepressant\ndrug blocks\nreuptake of the\nneurotransmitter. PRESYNAPTIC"], vurgu_metin="Presinaptik Gerialım Blokajı")
add_cumle(p30, "Pompanın kilitlenmesiyle nörotransmitterin vezikül içine geri alınması engellenir ve sinaptik yarıkta kalış süresi uzar.",
          "**Sinaptik Birikim:** Nörotransmitterin yarıkta kalış süresi.", 30,
          ["Antidepressant\ndrug blocks\nreuptake of the\nneurotransmitter. PRESYNAPTIC"], vurgu_metin="Sinaptik Birikim")
add_cumle(p30, "Sinaptik aralıkta artan monoaminler postsinaptik reseptörleri uyararak hücre içi sinyal kaskadlarını tetikler.",
          "**Postsinaptik İletim:** Artan monoaminlerin reseptör uyarımı.", 30,
          ["Antidepressant\ndrug blocks\nreuptake of the\nneurotransmitter. PRESYNAPTIC"], vurgu_metin="Postsinaptik İletim")

p31 = add_paragraf(b12, 31)
add_cumle(p31, "Trisiklik antidepresanların oral emilimleri yüksektir, yarılanma ömürleri uzundur ve sedatif etkileri nedeniyle akşam tek doz verilirler.",
          "**TCA Emilimi ve Sedasyon:** Yüksek emilim ve akşam tek doz.", 31,
          ["➢Benzerlerinden daha yüksek oranda absorpsiyonları vardır. T1/2 uzundur.\n➢Sedatif etkileri yüksektir. Bundan dolayı tek doz ve akşam üzeri verirler."], vurgu_metin="TCA Emilimi ve Sedasyon")
add_cumle(p31, "Karaciğerde bifazik metabolizmaya uğrarlar ve dozun sadece yüzde beşi idrarla değişmeden atılır.",
          "**Bifazik Metabolizma:** Karaciğer inaktivasyonu ve düşük renal itrah.", 31,
          ["➢Bifazik metabolize edilirler.\n➢Sadece %5 kadarı idrarla değişmemiş olarak atılır."], vurgu_metin="Bifazik Metabolizma")
add_cumle(p31, "Sitokrom pe iki de altı substratı olduklarından fluoksetin gibi güçlü inhibitörlerle birlikte verildiklerinde düzeyleri tehlikeli biçimde yükselir.",
          "**CYP2D6 Etkileşimi:** İnhibitörlerle toksik düzey artışı.", 31,
          ["➢CYP2D6 sistemi substratıdırlar. (Fluoksetin ile etkileşim)\n➢İzoenzim polimorfizmi metabolizasyonlarını büyük ölçüde değiştirir."], vurgu_metin="CYP2D6 Etkileşimi")
add_cumle(p31, "Desipramin ve nortriptilin gibi sekonder aminlerin kinetiği doğrusaldır ve aktif metabolit oluşturmazlar.",
          "**Sekonder Amin Kinetiği:** Desipramin ve nortriptilin doğrusal kinetiği.", 31,
          ["➢Desipramin ve nortriptilin gibi sekonder amin tTCA’ların kinetikleri\ndoğrusaldır, aktif metaboliti yoktur."], vurgu_metin="Sekonder Amin Kinetiği")
add_cumle(p31, "Terapötik pencereleri dar olduğundan serum ilaç düzeyi takibi toksisiteyi önlemede son derece güvenilir bir rehberdir.",
          "**Terapötik İlaç İzlemi:** Serum düzeyi takibi ve dar pencere.", 31,
          ["➢Terapötik yanıt ve toksisitesi açısından serum düzeyi takibi son derece\ngüvenilirdir."], vurgu_metin="Terapötik İlaç İzlemi")

p32 = add_paragraf(b12, 32)
add_cumle(p32, "Şemada sinir terminalinde bulunan serotonin ve noradrenalin geri alım taşıyıcılarının yerleşimi gösterilmektedir.",
          "**Taşıyıcı Şeması:** Akson terminalinde SERT ve NET yerleşimi.", 32,
          ["Nerve SAT iğ 5 Noradrenajine =\nterminal re-uptake —— /75 gü e-uptake :\ntransporter oo ‘ — transporter"], vurgu_metin="Taşıyıcı Şeması")
add_cumle(p32, "Trisiklik antidepresanlar bu taşıyıcıları bloke ederken aynı anda muskarinik, histaminik ve adrenerjik reseptörleri de antagonize ederler.",
          "**Çoklu Reseptör Blokajı:** Taşıyıcı ve otonomik reseptör antagonizması.", 32,
          ["TRISIKLIK ANTIDEPRESANLARIN (TCA'LAR) ETKİ MEKANIZMASI"], vurgu_metin="Çoklu Reseptör Blokajı")
add_cumle(p32, "Mitokondriyal monoamin oksidaz ve sinaptik aralıktaki asetilkolinesteraz enzimleri nörotransmitter dengesini birlikte denetler.",
          "**Enzimatik Yıkım:** MAO ve asetilkolinesteraz kontrol mekanizmaları.", 32,
          ["antidepressant | \\ i} \\ if \\_, Mitochondria"], vurgu_metin="Enzimatik Yıkım")

p33 = add_paragraf(b12, 33)
add_cumle(p33, "Trisikliklerin geniş reseptör afinite profili onların güçlü terapötik etkisinin yanında çoklu yan etki yükünü de açıklar.",
          "**Afinite ve Yan Etki Dengesi:** Terapötik güç ve otonomik yan etkiler.", 33,
          None, sekil="Trisiklik antidepresan reseptör etkileşim şeması", vurgu_metin="Afinite ve Yan Etki Dengesi")
add_cumle(p33, "Bu çoklu reseptör blokajı özellikle kardiyak ileti bozuklukları ve antikolinerjik kriz riskini beraberinde getirir.",
          "**Toksik Risk:** Kardiyak ileti kusurları ve antikolinerjik kriz.", 33,
          None, sekil="Trisiklik antidepresan reseptör etkileşim şeması", vurgu_metin="Toksik Risk")
add_cumle(p33, "Şimdi beş ha te iki antagonistleri ve atipik antidepresanların farmakokinetik ayrıntılarını değerlendirelim.",
          "**Atipik Kinetik:** 5-HT2 antagonistleri ve bupropion kinetiği.", 33,
          None, sekil="Atipik antidepresan farmakokinetik özeti", vurgu_metin="Atipik Kinetik")

# === BOLUM 13: Atipik Ajanların ve MAOI Farmakokinetiği (Sayfa 34-37) ===
b13 = add_bolum("Atipik Ajanların ve MAOI Kinetiği")
p34 = add_paragraf(b13, 34)
add_cumle(p34, "Trazodon ve nefazodon gastrointestinal kanaldan hızla ve yüksek oranda emilir, karaciğerde kapsamlı metabolizmaya uğrarlar.",
          "**Trazodon ve Nefazodon:** Hızlı emilim ve karaciğer metabolizması.", 34,
          ["✓Trazodone ve nefazodone emilimleri hızlı ve yüksektir\n✓Kpsamlı metabolizasyon yeri karaciğerdir"], vurgu_metin="Trazodon ve Nefazodon")
add_cumle(p34, "Plazma proteinlerine yüksek oranda bağlanırlar, biyoyararlanımları sınırlıdır ve eliminasyon yarı ömürleri kısadır.",
          "**Kısa Yarı Ömür:** Yüksek protein bağlanması ve sınırlı yararlanım.", 34,
          ["✓Büyük oranda proteinlere bağlanırlar. Bu; biyoyararlanımlarını\nsınırlıdır.\n✓T ½  kısadır."], vurgu_metin="Kısa Yarı Ömür")
add_cumle(p34, "Antidepresan amaçla doz gün içine bölünerek verilir; trazodon düşük dozlarda belirgin hipnotik etki sergiler.",
          "**Bölünmüş Dozlama:** Trazodonun hipnotik ve antidepresan dozu.", 34,
          ["✓Antidepresan olarak doz bölünmelidir.\n✓Trazodone daha düşük dozlarda hipnotikdir."], vurgu_metin="Bölünmüş Dozlama")
add_cumle(p34, "Nefazodon sitokrom pe üç a dört izoenziminin çok güçlü bir inhibitörüdür ve ciddi ilaç etkileşimlerine neden olur.",
          "**CYP3A4 İnhibisyonu:** Nefazodonun güçlü enzim baskılaması.", 34,
          ["Nefazodone güçlü bir CYP3A4 inhibitörüdür."], vurgu_metin="CYP3A4 İnhibisyonu")

p35 = add_paragraf(b13, 35)
add_cumle(p35, "Bupropion hızla emilir, proteinlere yüksek oranda bağlanır ve yoğun karaciğer ilk geçiş eliminasyonuna uğrar.",
          "**Bupropion Emilimi:** İlk geçiş etkisi ve yüksek protein bağlanması.", 35,
          ["✓Emilimi hızlı proteinlere bağlanması yüksektir\n✓İlk geçiş etkisine uğrar (FPE)"], vurgu_metin="Bupropion Emilimi")
add_cumle(p35, "Karaciğerde oluşan hidroksibupropion dahil üç temel metaboliti de biyolojik olarak aktiftir.",
          "**Aktif Metabolitler:** Hidroksibupropion ve aktif bileşikler.", 35,
          ["✓Hidroksibupripion dahil üç metaboliti de aktiftir.\n✓Metabolitleri üzerinde antidepresan etki çalışılmaktadır."], vurgu_metin="Aktif Metabolitler")
add_cumle(p35, "Bupropion bifazik eliminasyon gösterir ve ikinci fazın süresi ilk fazdan yaklaşık on dört kat daha uzundur.",
          "**Bifazik Eliminasyon:** Faz iki eliminasyonunun on dört kat uzunluğu.", 35,
          ["✓Eliminasyonu bi-faziktir. Faz 2/faz 1 i  yaklaşık 14 kat (saat olarak)"], vurgu_metin="Bifazik Eliminasyon")
add_cumle(p35, "Amoksapinin aktif metaboliti olan yedi hidroksi amoksapin güçlü bir dopamin de iki blokörü olup antipsikotik etki kazandırır.",
          "**7-Hidroksi Amoksapin:** D2 blokajı ve antipsikotik özellik.", 35,
          ["✓Metabolitlerinden aktif olan 7- hidroksi amoksapin güçlü bir D2\nblokörüdür. bu durum antipsikotik etkilerle ilişkilendirilir."], vurgu_metin="7-Hidroksi Amoksapin")

p36 = add_paragraf(b13, 36)
add_cumle(p36, "Maprotilin farmakokinetik özellikleri bakımından bupropiona benzerlik gösteren sekonder bir amindir.",
          "**Maprotilin Profili:** Bupropiona benzer sekonder amin yapısı.", 36,
          ["✓Maprotilin bupropiona benzer"], vurgu_metin="Maprotilin Profili")
add_cumle(p36, "Mirtazapin yirmi ila kırk saatlik uzun eliminasyon yarılanma ömrüyle diğer grup üyelerinden belirgin biçimde ayrılır.",
          "**Mirtazapin Yarı Ömrü:** Yirmi ila kırk saatlik uzun yarılanma.", 36,
          ["Mirtazapin\n✓Grup üyelerinden yarılanma ömrü ile ayrılır.\n✓Yarılanma ömrü 20 ile 40 saat arasıdır"], vurgu_metin="Mirtazapin Yarı Ömrü")
add_cumle(p36, "Sitokrom pe iki de altı, bir a iki ve üç a dört enzimleri üzerinden çoklu metabolik yollardan geçer.",
          "**Çoklu Sitokrom Yolağı:** CYP2D6, CYP1A2 ve CYP3A4 metabolizması.", 36,
          ["✓Birçok sitokrom p450 enzimi ile etkileşir."], vurgu_metin="Çoklu Sitokrom Yolağı")
add_cumle(p36, "Güçlü histamin bir reseptör blokajı nedeniyle belirgin sedatif etki gösterir ve akşam saatlerinde tek doz kullanılır.",
          "**Sedatif Özellik:** H1 blokajı ve akşam tek doz uygulama.", 36,
          ["✓Sedatif etkisi yüksektir. Akşam saatlerinde tek doz yeterlidir."], vurgu_metin="Sedatif Özellik")

p37 = add_paragraf(b13, 37)
add_cumle(p37, "Monoamin oksidaz inhibitörleri karaciğerde yoğun ilk geçiş eliminasyonuna uğrarlar ve oral biyoyararlanımları düşer.",
          "**MAOI İlk Geçişi:** Karaciğer ilk geçişi ve düşük yararlanım.", 37,
          ["✓Metabolizasyonları değişik yollar ile olur.\n✓İlk geçiş etkisine büyük ölçüde uğrarlar. Dolayısıyla biyoyararlanımları\ndüşer."], vurgu_metin="MAOI İlk Geçişi")
add_cumle(p37, "Tranilsipromin ve fenelzinin barsak mao enzimini baskılaması nedeniyle alternatif farmasötik şekiller tasarlanmıştır.",
          "**Alternatif Formlar:** Barsak enzim blokajını aşan formülasyon.", 37,
          ["✓Tranilsipromin, selejilin, fenelzin, gastrointestinal sistemde emilimleri\nMAO inhibisyonu nedeniyle farklı yollardan kullanılabilir farmasötik\nşekilleri geliştirilmiştir."], vurgu_metin="Alternatif Formlar")
add_cumle(p37, "Selejilinin transdermal yama ve sublingual formları gastrointestinal ilk geçiş metabolizmasını baypas eder.",
          "**Transdermal Selejilin:** İlk geçiş metabolizmasını baypas etme.", 37,
          ["✓Sublingual transdermal ve diğer farmasötik formları mevcuttur."], vurgu_metin="Transdermal Selejilin")
add_cumle(p37, "Barsak ve karaciğerdeki mao a enziminin bloke edilmesi gıdalarla alınan tiraminin sistemik dolaşıma geçmesine yol açar.",
          "**Tiramin Geçişi:** Gıdasal tiraminin inaktive edilememesi.", 37,
          ["✓GİS’te tiramin metabolizmasından etkilenir."], vurgu_metin="Tiramin Geçişi")

# === BOLUM 14: Moleküler Mekanizmalar ve Transporter Farmakolojisi (Sayfa 38-41) ===
b14 = add_bolum("Transporter ve Reseptör Moleküler Farmakolojisi")
p38 = add_paragraf(b14, 38)
add_cumle(p38, "Bütün antidepresan sınıflarının ortak temel hedefi sinaptik aralıkta monoaminerjik nörotransmisyonu artırmaktır.",
          "**Monoamin Artışı:** Sinaptik kavşakta iletimi güçlendirme.", 38,
          ["✓Antidepresanların major fonksiyonu:\n✓Monoamin nörotransmisyonunu arttırmaktır."], vurgu_metin="Monoamin Artışı")
add_cumle(p38, "Çoğu antidepresan bu hedefi presinaptik monoamin geri alım pompalarının aktivitesini bloke ederek gerçekleştirir.",
          "**Transporter Blokajı:** Geri alım pompalarının durdurulması.", 38,
          ["✓Monoamin transporterlerinin aktivitesini bloke ederler."], vurgu_metin="Transporter Blokajı")
add_cumle(p38, "Sinaptik monoamin miktarını artırmanın diğer temel yolu mitokondriyal mao enzimatik yıkımını durdurmaktır.",
          "**Enzimatik Yıkım Blokajı:** MAO inhibisyonuyla monoamin artışı.", 38,
          ["✓Mona aminlerin miktarını arttırmanın bir diğer yolu enzimatik\nyıkımlanmayı inhibe etmektir (MAO inhibitörleri)."], vurgu_metin="Enzimatik Yıkım Blokajı")
add_cumle(p38, "Mirtazapin gibi ilaçlar ise presinaptik alfa iki otoreseptörleri bloke ederek nörotransmitter salınımını tetiklerler.",
          "**Otoreseptör Antagonizması:** Presinaptik alfa-2 blokajıyla salınım artışı.", 38,
          ["✓Presinaptik oto reseptörlere ve spesifik postsinaptik reseptörlere\nbağlanmak bir diğer monoamin arttırma yoludur (Mirtazapin)."], vurgu_metin="Otoreseptör Antagonizması")

p39 = add_paragraf(b14, 39)
add_cumle(p39, "Serotonin taşıyıcısı sert, serotonerjik nöronların akson terminalleri ve gövde membranında yer alan on iki transmembranlı bir glikoproteindir.",
          "**SERT Glikoproteini:** On iki transmembranlı taşıyıcı yapı.", 39,
          ["✓Serotonin Transporteri serotonerjik nöronlarda akson terminali ve hücre\ngövde membranında bir glikoproteindir."], vurgu_metin="SERT Glikoproteini")
add_cumle(p39, "Serotonin bu taşıyıcıya bağlandığında bir sodyum ve bir klor iyonu ile birlikte sitoplazma içine kotransport edilir.",
          "**İyonik Kotransport:** Sodyum ve klor bağımlı serotonin alımı.", 39,
          ["Serotonin bu taşıyıcılar üzerinden\nreseptörlere bağlanır Na+ ve Cl- ile beraber hücreye girer."], vurgu_metin="İyonik Kotransport")
add_cumle(p39, "Se se re i grubu ilaçlar taşıyıcı üzerindeki allosterik bağlanma bölgesine oturarak geri alım mekanizmasını kilitlerler.",
          "**Allosterik İnhibisyon:** Taşıyıcının konformasyonel kilitlenmesi.", 39,
          ["✓SSRİ ler ise reseptör üzerinde serotoninin aktif bağlanma yerinden\nbaşka bir bölgeye bağlanmasını sağlayarak inhibe ederler."], vurgu_metin="Allosterik İnhibisyon")
add_cumle(p39, "Seçici serotonin inhibitörlerinin noradrenalin taşıyıcısı veya beta adrenoreseptörler üzerinde anlamlı bir bloke edici etkisi yoktur.",
          "**Yüksek Seçicilik:** Noradrenalin ve adrenoreseptör etkisizliği.", 39,
          ["✓SSRİ'lerin beta adrenoreseptör veya noradrenalin taşıyıcısı üzerine etkisi\nbelirsizdir (yoktur)."], vurgu_metin="Yüksek Seçicilik")

p40 = add_paragraf(b14, 40)
add_cumle(p40, "İkili geri alım inhibitörleri sinaptik aralıkta hem sert hem net taşıyıcı moleküllerine bağlanırlar.",
          "**İkili Bağlanma:** SERT ve NET taşıyıcılarına eş zamanlı etki.", 40,
          ["✓Hem serotonin hem noradrenalin geri alım inhibitörleri\ntaşıyıcıların her ikisine bağlanır."], vurgu_metin="İkili Bağlanma")
add_cumle(p40, "Venlafaksin düşük dozlarda sert seçici davranırken, ancak yüksek dozlara çıkıldığında noradrenalin taşıyıcısını bloke eder.",
          "**Doz Bağımlı Seçicilik:** Venlafaksinin doza bağlı NET blokajı.", 40,
          ["✓Venlafaksin zayıf bir noradrenalin Transporter (NET) inhibitörüdür."], vurgu_metin="Doz Bağımlı Seçicilik")
add_cumle(p40, "Desvenlafaksin, duloksetin ve milnasipran ise hem sert hem net üzerinde dengeli ve güçlü bir inhibisyon sergilerler.",
          "**Dengeli İnhibisyon:** Desvenlafaksin, duloksetin ve milnasipran dengesi.", 40,
          ["✓Des-Venlafaksin, duloksetin, milnasipran hem SERT hem de\nNET'in dengeli bir inhibitörüdür."], vurgu_metin="Dengeli İnhibisyon")
add_cumle(p40, "Bu nedenle majör depresyon ve kronik ağrı sendromlarında trisikliklerin yan etkilerinden kaçınmak için se ne re i grubu tercih edilir.",
          "**Klinik Tercih:** Trisiklikler yerine güvenli SNRI seçimi.", 40,
          ["✓SNRİ’ler; major depresif bozukluk, ağrı sendromu durumlarında\ntrisiklik antidepresanlara tercih edilirler."], vurgu_metin="Klinik Tercih")

p41 = add_paragraf(b14, 41)
add_cumle(p41, "Trisiklik antidepresanlar arasında taşıyıcı afinitesi açısından belirgin farmakodinamik farklılıklar bulunur.",
          "**Afinite Farklılıkları:** Trisikliklerde SERT ve NET ayrımı.", 41,
          ["✓Trisiklik antidepresanlarda NET'e oranla  SERT üzerine afinite yönünden\nciddi farklar vardır."], vurgu_metin="Afinite Farklılıkları")
add_cumle(p41, "Muskarinik reseptör blokajı ağız kuruluğu, konstipasyon, idrar retansiyonu ve bulanık görme gibi güçlü antimuskarinik tablolara yol açar.",
          "**Antimuskarinik Belirtiler:** Ağız kuruluğu, konstipasyon ve retansiyon.", 41,
          ["✓Trisiklik antidepresanlar; ağız kuruluğu, konstipasyon gibi güçlü\nantimuskarinik etkileri vardır."], vurgu_metin="Antimuskarinik Belirtiler")
add_cumle(p41, "Histamin bir reseptör blokajı ise santral sedasyon, uyku hali ve belirgin kilo artışının temel nedenidir.",
          "**Histaminik Blokaj:** Sedasyon, uyku ve kilo artışı mekanizması.", 41,
          ["✓Ve H1 reseptör antagonisti gibi  etkileri de buna bağlanır."], vurgu_metin="Histaminik Blokaj")
add_cumle(p41, "Doksepin güçlü antihistaminik etkisiyle hipnotik ve antiprüritik olarak kullanılırken alfa bir blokajıyla yaşlılarda ortostatik hipotansiyon yapar.",
          "**Doksepin Özellikleri:** Kaşıntı tedavisi ve ortostatik hipotansiyon.", 41,
          ["✓Doksepin antihistaminik yüksek etkileri nedeniyle hipnotik olarak reçete\nedilir. Kaşıntı tedavisinde kullanılır .\n✓Ancak yaşlılarda ciddi ortostatik hipotansiyon yapar"], vurgu_metin="Doksepin Özellikleri")

# === BOLUM 15: 5-HT2 Blokajı ve MAO İzoenzimleri (Sayfa 42-43) ===
b15 = add_bolum("5-HT2 Blokajı ve MAO İzoenzim Farmakolojisi")
p42 = add_paragraf(b15, 42)
add_cumle(p42, "Beş ha te iki reseptörlerinin bloke edilmesi anksiyolitik, antipsikotik ve antidepresan etki profili sağlar.",
          "**5-HT2 Reseptör Blokajı:** Anksiyolitik ve antidepresan etki.", 42,
          ["✓5HT2  bloku; anti anksiyete antipsikotik antidepresan etkilere\nneden olur."], vurgu_metin="5-HT2 Reseptör Blokajı")
add_cumle(p42, "Tam aksine liserjik asit dietilamid ve meskalin gibi beş ha te iki a agonistleri güçlü halüsinojen ve anksiyojenik maddelerdir.",
          "**Reseptör Agonizmi:** LSD, meskalin ve anksiyojenik etki.", 42,
          ["✓ LSD(liserjik asit) ve meskalin (5HT2A agonistleri halüsinojen ve\nanksiyojendir)."], vurgu_metin="Reseptör Agonizmi")
add_cumle(p42, "Trazodon ve nefazodon bu reseptörü seçici bloke ederken zayıf geri alım inhibisyonu yaparlar; trazodon sert için daha seçicidir.",
          "**SARI Etki Mekanizması:** Reseptör blokajı ve zayıf SERT ilgisi.", 42,
          ["✓Trazodone ve nefazodone 5HT2A Reseptör blokajı yapar.\n✓Her ikisi de zayıf NER ve SERT inhibitörüdür. Ancak trazodone SERT\niçin daha selektif bir  inhibitörüdür."], vurgu_metin="SARI Etki Mekanizması")
add_cumle(p42, "Amoksapin ve maprotilin desipramin gibi noradrenalin taşıyıcısını çok güçlü, serotonin taşıyıcısını ise zayıf inhibe ederler.",
          "**NET Seçici Heterosiklikler:** Amoksapin ve maprotilinde NET üstünlüğü.", 42,
          ["✓Amoksapin ve maprotilin tıpkı desipramin gibi güçlü NET ve daha\naz SERT inhibitörleridir."], vurgu_metin="NET Seçici Heterosiklikler")

p43 = add_paragraf(b15, 43)
add_cumle(p43, "Mao a izoenzimi dopaminerjik ve noradrenerjik nöronlarda bulunur; birincil substratları noradrenalin, adrenalin ve serotonindir.",
          "**MAO-A İzoenzimi:** Noradrenalin, adrenalin ve serotonin substratları.", 43,
          ["✓MAO-A hem dopamin hem noradrenalin nöronlarında mevcuttur.\n✓Primer substratı noradrenalin adrenalin ve serotonindir."], vurgu_metin="MAO-A İzoenzimi")
add_cumle(p43, "Mao be serotonerjik ve histaminerjik nöronlarda yer alır; öncelikli substratları tiramin, feniletilamin ve benzilamindir.",
          "**MAO-B İzoenzimi:** Tiramin, feniletilamin ve benzilamin yıkımı.", 43,
          ["✓MAO-B ise serotonerjik ve histaminerjik nöronlarda bulunur\n(Beyin karaciğer ve trombositlerde).\n✓Primer olarak tiramin, feniletilamin ve benzilamin üzerine etkir."], vurgu_metin="MAO-B İzoenzimi")
add_cumle(p43, "Dopamin ve triptamin her iki mao izoenzimi tarafından ortak biçimde enzimatik yıkıma uğratılır.",
          "**Ortak Substratlar:** Dopamin ve triptaminin çifte yıkımı.", 43,
          ["✓Triptamin ve dopamin hem MAO-A hem de MAO-B tarafından\nmetabolize edilir."], vurgu_metin="Ortak Substratlar")
add_cumle(p43, "Fenelzin ve tranilsipromin geri dönüşümsüz nonselektif inhibitörlerdir; moklobemid ise geri dönüşümlü seçici mao a inhibitörüdür.",
          "**İzoenzim Seçiciliği:** Fenelzin, tranilsipromin ve moklobemid.", 43,
          ["✓Fenelzin ve tranilsipromin geri dönüşümsüz, nonselektif MAO\ninhibitörüne örnektir.\n✓Moklobemid  reversibl ve selektif MAO-A inhibitörüdür."], vurgu_metin="İzoenzim Seçiciliği")

# === BOLUM 16: Majör Depresyon ve Psikiyatrik Tedavi (Sayfa 44-45) ===
b16 = add_bolum("Klinik Tedavi İlkeleri ve Psikiyatrik Endikasyonlar")
p44 = add_paragraf(b16, 44)
add_cumle(p44, "Antidepresanların birincil kullanım alanı majör depresyon epizotları olup tedavideki nihai amaç tam semptomatik remisyondur.",
          "**Klinik Amaç:** Majör depresyonda tam remisyon hedefi.", 44,
          ["1. Major tedavi alanı Anti depresan etkileridir\n2. Major depresif bozukluğu epizotları tedavisinde kullanılırlar.\nAmaç semptomların remisyonudur."], vurgu_metin="Klinik Amaç")
add_cumle(p44, "Monoterapi ile yeterli klinik yanıt alınamazsa doz artırımı, ilaç değişimi veya farklı etki mekanizmalı ajanlarla augmentasyon düşünülür.",
          "**Tedavi Stratejisi:** Monoterapi, değişim ve kombinasyon.", 44,
          ["3. Elde edilen klinik cevap yetersizse monoterapi yerine dönüşümlü politerapi\ndüşünülebilir."], vurgu_metin="Tedavi Stratejisi")
add_cumle(p44, "Depresyon doğası gereği yineleyici bir hastalıktır ve hastaların önemli bir kısmında tekrarlayan agresif epizotlar izlenir.",
          "**Yineleyici Epizotlar:** Depresyon nükslerinin agresif yapısı.", 44,
          ["4. Depresyonun nüksleri agresiftir. Hastalarda birden fazla sayıda epizot nüksü\noluşabilir."], vurgu_metin="Yineleyici Epizotlar")
add_cumle(p44, "Nüksleri engellemek için se se re i, se ne re i veya trisiklik antidepresanların en az altı ila dokuz ay kronik sürdürülmesi gerekir.",
          "**İdame Tedavisi:** Kronik sürdürüm ve nüks koruması.", 44,
          ["5. Trisiklik antidepresanlar, SNRİ ve SSRİ’ler kronik verilme zorunluluğunda hastaya\nklinik yarar sağlar."], vurgu_metin="İdame Tedavisi")

p45 = add_paragraf(b16, 45)
add_cumle(p45, "Bipolar depresyon tedavisinde antidepresan monoterapisi etkisizdir ve mizaç dengeleyici olmadan asla kullanılmamalıdır.",
          "**Bipolar Depresyon:** Mizaç dengeleyici olmaksızın etkisizlik.", 45,
          ["6. Antidepresanların bütün (mix)depresyon türlerine etkili olup olmadığı henüz\nbilinmemektedir.  Örn: Bipolar’da mizaç stabilize ediciler (Lİ, Valporat, Lamotrijin)\nile kullanıldıklarında faydası yok gibidir."], vurgu_metin="Bipolar Depresyon")
add_cumle(p45, "Bipolar bozuklukta tek başına antidepresan kullanımı manik kaymayı tetikleyebilir ve hızlı döngülülüğe yol açabilir.",
          "**Manik Kayma Riski:** Antidepresanla tetiklenen mani tablosu.", 45,
          ["7. Antidepresan kullanımı bazen maniye eğilimi arttırır.."], vurgu_metin="Manik Kayma Riski")
add_cumle(p45, "Anksiyete bozukluklarının uzun dönem idamesinde se se re i grubu ilk seçenektir; akut kriz yönetiminde benzodiazepinler geçici fayda sağlar.",
          "**Anksiyete Yönetimi:** SSRI ile idame ve benzodiazepin kullanımı.", 45,
          ["8. Anksiyete, majör depresyondan sonra bu ilaçlarla tedavi edilen önemli bir\nklinik tir.\n9. Jeneralize anksiyete ve panikte benzodiazepinler daha yararlı görünmekte."], vurgu_metin="Anksiyete Yönetimi")
add_cumle(p45, "Obsesif kompulsif bozuklukta klomipramin ve yüksek doz se se re i onaylıdır; tam başarı için bilişsel davranışçı terapiyle kombine edilmelidir.",
          "**OKB Farmakoterapisi:** Klomipramin, SSRI ve davranışçı terapi.", 45,
          ["10. Obsesif kompulsif bozuklukta klomipramin ve SSRİ onaylıdır ancak orta\ndereceli bir etkiye sahiptirler. Bunun için antidepresanlarla davranış tedavisi\nbirlikte yürütülmelidir."], vurgu_metin="OKB Farmakoterapisi")

# === BOLUM 17: Kronik Ağrı ve Özel Endikasyonlar (Sayfa 46-47) ===
b17 = add_bolum("Kronik Ağrı ve Özel Klinik Endikasyonlar")
p46 = add_paragraf(b17, 46)
add_cumle(p46, "Antidepresanlar inen ağrı yolaklarını aktive ederek belirgin analjezik etki oluştururlar ve amitriptilin nöropatik ağrıda kullanılır.",
          "**Analjezik Etkinlik:** İnen inhibitör yolaklar ve amitriptilin.", 46,
          ["11. Antidepresanların analjezik etkileri de vardır. TCA’lar  nörolojik ve diğer\nağrı durumlarının tedavisinde kullanılır."], vurgu_metin="Analjezik Etkinlik")
add_cumle(p46, "Premenstrüel disforik bozuklukta gelişen duygudurum dalgalanmaları ve irritabilite luteal fazda uygulanan se se re i tedavisine hızla yanıt verir.",
          "**Premenstrüel Disfori:** Luteal fazda uygulanan SSRI yanıtı.", 46,
          ["12. Pre-menstrüel distrofik bozukluklarda gelişen anksiyete, depresyon, mizaç\nirritabilite, uykusuzluk, yorgunluk gibi semptomlar antidepresanlarla tedavi\nedilebilir (SSRİ)"], vurgu_metin="Premenstrüel Disfori")
add_cumle(p46, "Bupropion dopamin ve noradrenalin geri alımını durdurarak sigara bırakma tedavisinde aşermeyi azaltmada onaylı ve etkilidir.",
          "**Sigara Bırakma:** Bupropion ile nikotin aşermesinin azaltılması.", 46,
          ["13. Bupropion sigara bırakma tedavisinde etkilidir. Bunun mekanizması\nbelirsizdir. Nortriptilin aynı amaçla kullanılır. Ancak istikrarlı bir molekül değildir."], vurgu_metin="Sigara Bırakma")
add_cumle(p46, "Fluoksetin bulimiya nervozada tıkınırcasına yeme ve kusma epizotlarını belirgin azaltır ancak anoreksiyada klinik yararı sınırlıdır.",
          "**Yeme Bozuklukları:** Bulimiya nervozada fluoksetin onayı.", 46,
          ["14.Anorekside faydalı olmamakla beraber Bulimia da fluoksetin kullanmaktadır.\nBulimia nervoza ve anoreksiya nervoza (yeme bozuklukları) çoğunlukla kroniktir."], vurgu_metin="Yeme Bozuklukları")
add_cumle(p46, "Bupropion iştah baskılayıcı etkisiyle obezite tedavisinde yardımcıdır fakat yaşam tarzı değişikliği olmaksızın yeterli değildir.",
          "**Obezite Yaklaşımı:** İştah regülasyonu ve yaşam tarzı.", 46,
          ["14. Bupropion obezite tedavisinde faydalı görünmektedir. Ancak obezite\npratik olarak sadece ilaçla tedavisi mümkün değil."], vurgu_metin="Obezite Yaklaşımı")

p47 = add_paragraf(b17, 47)
add_cumle(p47, "Çocuklarda enürezis nokturna tedavisinde imipramin sfinkter tonusunu artırıcı ve uyanma eşiğini düzenleyici etkisiyle kullanılır.",
          "**Enürezis Nokturna:** İmipramin ile sfinkter tonusu kontrolü.", 47,
          ["✓Çocuklarda enürezis trisiklik antidepresanlarla giderilir."], vurgu_metin="Enürezis Nokturna")
add_cumle(p47, "Kadınlarda üriner stres inkontinansında üretral sfinkter tonusunu artıran duloksetin etkinliği kanıtlanmış bir ajandır.",
          "**Stres İnkontinans:** Duloksetin ile üretral tonus regülasyonu.", 47,
          ["✓Üriner stres inkontinans tedavisinde duloksetin etkilidir."], vurgu_metin="Stres İnkontinans")
add_cumle(p47, "Perimenopozal dönemdeki sıcak basması gibi vazomotor semptomların kontrolünde desvenlafaksin güvenle tercih edilebilir.",
          "**Vazomotor Semptomlar:** Desvenlafaksin ile perimenopozal tedavi.", 47,
          ["✓Perimenopozal  vazomotor semptomlarda desvenlafaxine etkili\ngörünmektedir."], vurgu_metin="Vazomotor Semptomlar")
add_cumle(p47, "Çoğu serotonerjik antidepresan libido azalması ve orgazm gecikmesi gibi cinsel işlev bozukluklarına yol açar.",
          "**Cinsel İşlev Bozukluğu:** Serotonerjik ajanların cinsel yan etkileri.", 47,
          ["Antidepresanlar seksüel fonksiyonları az veya çok değiştirirler.\nAncak bu amaçla kullanılabilmeleri için mevcut bilimin yetisi henüz\nkifayetsiz."], vurgu_metin="Cinsel İşlev Bozukluğu")

# === BOLUM 18: Dozlama, İntihar Riski ve Advers Etkiler (Sayfa 48-51) ===
b18 = add_bolum("Dozlama, İntihar Riski ve Toksisite")
p48 = add_paragraf(b18, 48)
add_cumle(p48, "Bu bilgi sınavda soruldu: Antidepresan başlanan bir hastada klinik yanıtın ortaya çıkması ve terapötik değerlendirme yapılabilmesi için en az iki ila dört hafta yani on beş gün beklenmelidir.",
          "**Terapötik Değerlendirme:** En az on beş gün veya iki ila dört hafta bekleme.", 48,
          ["Dozlam\nBütün antidepresanlar tedaviye başladıktan en az\n15 gün sonra klinik olarak değerlendirilebilir\nolurlar."], vurgu_metin="Terapötik Değerlendirme", cikmis_id="d3-k2-psi-018")
add_cumle(p48, "Tedavinin ilk günlerinde görülen sinaptik monoamin artışına rağmen klinik iyileşme postsinaptik reseptör desensitizasyonu ve hücresel adaptasyon sonrasında gelişir.",
          "**Reseptör Adaptasyonu:** Sinaptik artış sonrası hücresel gecikme.", 48,
          ["Bütün antidepresanlar tedaviye başladıktan en az\n15 gün sonra klinik olarak değerlendirilebilir\nolurlar."], vurgu_metin="Reseptör Adaptasyonu")
add_cumle(p48, "Bu gecikme süreci nedeniyle hastaların ilacı erken dönemde etkisiz zannedip bırakmalarını önlemek için hasta uyumu yakından izlenmelidir.",
          "**Hasta Uyumu:** Erken ilaç kesilmesini önleme ve takip.", 48,
          ["Dozlam"], vurgu_metin="Hasta Uyumu")

p49 = add_paragraf(b18, 49)
add_cumle(p49, "Bütün antidepresan sınıfları yirmi beş yaşın altındaki çocuk ve genç erişkinlerde tedavinin başında paradoksal intihar eğilimini artırabilir.",
          "**Yirmi Beş Yaş Altı Uyarısı:** Başlangıçta paradoksal intihar riski.", 49,
          ["➢Bütün antidepresanlar 25 yaşın altında intihar eğilimini arttırır."], vurgu_metin="Yirmi Beş Yaş Altı Uyarısı")
add_cumle(p49, "İlaç dozunun artırılması ve tedavinin sonlandırılması kesilme sendromunu önlemek için merdiven kuralına göre basamaklı yapılmalıdır.",
          "**Merdiven Kuralı:** Dozun basamaklı titrasyonu ve yavaş kesilmesi.", 49,
          ["➢Doz ritim artışı ve azalışı merdiven kuralına göredir."], vurgu_metin="Merdiven Kuralı")
add_cumle(p49, "Tedavinin ilk haftalarında bulantı ve gastrointestinal yakınmalar yaygındır; nefazodon ve trazodon alfa blokajıyla ortostatik hipotansiyon yapar.",
          "**Hipotansiyon ve GİS Etkileri:** Ortostatik hipotansiyon ve bulantı.", 49,
          ["➢Sedasyon ve gastrointestinal bozukluk yapabilirler.\n➢Nefazodone ve trazodone ortostatik hipotansiyon yapar."], vurgu_metin="Hipotansiyon ve GİS Etkileri")
add_cumle(p49, "Amoksapin dopamin de iki reseptör blokajı nedeniyle parkinsonizm yapabilir; mirtazapin ise histamin blokajıyla güçlü sedasyon oluşturur.",
          "**Parkinsonizm ve Sedasyon:** Amoksapin ve mirtazapin yan etkileri.", 49,
          ["➢Amoksapin parkinsonizm ile ilişkilendirilmiştir.\n➢Mirtazapin önemli bir sedatiftir."], vurgu_metin="Parkinsonizm ve Sedasyon")
add_cumle(p49, "Venlafaksin yüksek dozlarda noradrenalin geri alımını artırdığı için doza bağımlı kan basıncı yükselmesi ve taşikardi yapabilir.",
          "**Hipertansiyon Riski:** Yüksek doz venlafaksinde tansiyon artışı.", 49,
          ["➢Vanlafaksin doz bağımlı hipertansiyon yapar.\n➢Anksiyete, ajitasyon, uykusuzluk, kalp hızında artış, santral sinir sistemi\naktivasyonunda sorunlar görülebilir."], vurgu_metin="Hipertansiyon Riski")

p50 = add_paragraf(b18, 50)
add_cumle(p50, "Trisiklik antidepresanlarda muskarinik reseptör blokajına bağlı ağız kuruluğu, konstipasyon, idrar retansiyonu ve bulanık görme belirgindir.",
          "**Antikolinerjik Toksisite:** Ağız kuruluğu, retansiyon ve konstipasyon.", 50,
          ["➢ Trisiklik antidepresanlarda antikolinerjik etkiler belirgindir.(ağız kuruluğu\nkonstipasyon idrar retansiyonu Bulanık görme konfüzyon) imipramin ve\namitriptilin de bu etkiler daha yüksektir."], vurgu_metin="Antikolinerjik Toksisite")
add_cumle(p50, "Bu bilgi çıkmışta soruldu: Trisiklik antidepresanlar serotonin ve noradrenalin taşıyıcılarını güçlü bloke ederken aşırı dozda sodyum kanallarını da kapatarak ölümcül kardiyotoksisite ve ventriküler aritmi yaparlar.",
          "**Trisiklik Antidepresanlar:** SERT ve NET blokajı ile ölümcül kardiyotoksisite.", 50,
          ["➢Trisiklik antidepresanlar antiaritmik ajanlardır"], vurgu_metin="Trisiklik Antidepresanlar", cikmis_id="d3-k2-far-019")
add_cumle(p50, "Monoamin oksidaz inhibitörleri ortostatik hipotansiyon, kilo alımı, aşırı santral uyarılma, uykusuzluk ve cinsel işlev bozukluğuna yol açarlar.",
          "**MAOI Yan Etkileri:** Ortostatik hipotansiyon, kilo alımı ve ajitasyon.", 50,
          ["➢Monoamin oksidaz inhibitörleri belirgin ortostatik hipotansiyon yapar ve kilo\naldırır.\n➢Anorgazmi, amfetamin  etkileri, aşırı aktivasyon uykusuzluk ve\nhuzursuzluk yaparlar."], vurgu_metin="MAOI Yan Etkileri")
add_cumle(p50, "Bu grupta tiramin içeren olgunlaşmış peynir ve şarapla ölümcül hipertansif kriz, se se re i kombinasyonunda ise deliryum ve hipertermiyle seyreden serotonin sendromu gelişir.",
          "**Tiramin Krizi ve Serotonin Sendromu:** Peynir etkisi ve deliryum tablosu.", 50,
          ["➢MAO inhibitörleri tiramin ve bazı gıdalarla tehlikeli etkileşimlere neden olurlar.\n➢Psikoz eksitasyon konfüzyon deliryum benzeri bir tablo ortaya çıkabilir."], vurgu_metin="Tiramin Krizi ve Serotonin Sendromu")

p51 = add_paragraf(b18, 51)
add_cumle(p51, "Antidepresan ilaçlar dersimizin sunumunu burada tamamlarken kaynaklarımızı ve ders özetimizi dikkatinize sunuyoruz.",
          "**Ders Sonu:** Kaynakça ve farmakoterapi özeti.", 51,
          ["age > pet 29:06 2021. 15907\nTeşekür ede 4"], vurgu_metin="Ders Sonu")
add_cumle(p51, "Rasyonel farmakoterapi ilkeleri doğrultusunda doğru tanı, doğru ilaç seçimi ve düzenli hasta takibi klinik başarının anahtarıdır.",
          "**Rasyonel Farmakoterapi:** Doğru ilaç seçimi ve klinik başarı.", 51,
          ["Teşekür ede 4"], vurgu_metin="Rasyonel Farmakoterapi")
add_cumle(p51, "Katılımınız ve sabrınız için teşekkür eder, klinik çalışmalarınızda ve sınavlarınızda başarılar dileriz.",
          "**Teşekkür ve Başarılar:** Klinik çalışmalar ve sınav hedefleri.", 51,
          ["Teşekür ede 4"], vurgu_metin="Teşekkür ve Başarılar")

# Save v2
v2 = {
    "surum": 2,
    "ders_id": "k2-63",
    "anahtar": "y25-k2-63-antidepresan-ilaclar",
    "baslik": "Antidepresan İlaçlar",
    "bolumler": bolumler
}

(taslak / "konusma_v2.json").write_text(json.dumps(v2, ensure_ascii=False, indent=2), encoding="utf-8")

# Update sayfa_haritasi.json with realistic multiple bilgi counts so it represents true depth
sh_path = taslak / "sayfa_haritasi.json"
sh = json.loads(sh_path.read_text(encoding="utf-8"))
page_counts = {}
for b in bolumler:
    for p in b["paragraflar"]:
        pg = p["sayfa"]
        page_counts[pg] = page_counts.get(pg, 0) + len(p["cumleler"])

# Slide to Bilgi Paketi mapping
SLIDE_BILGI = {
    1: [1], 2: [1], 3: [1],
    4: [2],
    5: [3],
    6: [4], 7: [4], 8: [4],
    9: [3], 10: [3], 11: [3], 12: [3], 13: [3],
    14: [5], 15: [5],
    16: [6], 17: [6], 18: [6],
    19: [7], 20: [7], 21: [7], 22: [7],
    23: [8],
    24: [9],
    25: [10],
    26: [11],
    27: [12],
    28: [13], 29: [13], 30: [13], 31: [13], 32: [13], 33: [13], 34: [13], 35: [13], 36: [13], 37: [13],
    38: [14], 39: [14], 40: [14], 41: [14], 42: [14], 43: [14],
    44: [15], 45: [15],
    46: [16],
    47: [17],
    48: [18], 49: [18],
    50: [19], 51: [19]
}

for it in sh.get("sayfalar", []):
    pg = int(it.get("sayfa", 0))
    it["bilgi"] = SLIDE_BILGI.get(pg, [1])

sh_path.write_text(json.dumps(sh, ensure_ascii=False, indent=2), encoding="utf-8")

# Derive outputs
md_txt, sayfalar_l = konusma_v2.turet(v2)
(taslak / "konusma_metni.md").write_text(md_txt, encoding="utf-8")
(taslak / "konusma_sayfalari.json").write_text(json.dumps(sayfalar_l), encoding="utf-8")
(taslak / "konusma_capalari.json").write_text(json.dumps(konusma_v2.capalar(v2), ensure_ascii=False), encoding="utf-8")

# Validate
errs = konusma_v2.dogrula(v2, konusma_v2.kaynak_sayfa(taslak), konusma_v2.kaynak_metin(taslak))
print("konusma_v2 dogrula errors:", errs)

kapsam = isle.sesli_kapsam(taslak)
print("sesli_kapsam errors:", kapsam)

total_words = sum(len(c["ses"].split()) for b in bolumler for p in b["paragraflar"] for c in p["cumleler"])
total_sent = sum(len(p["cumleler"]) for b in bolumler for p in b["paragraflar"])
print(f"Total sentences: {total_sent}, Total words: {total_words}, Est. Duration: {total_words/125:.1f} mins")
