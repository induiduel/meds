# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec10():
    slides = []

    # Slide 91: Ayaktan Piyelonefrit Tedavisi: Başlangıç Seftriakson/Aminoglikozid
    s91_narrative = (
        "Akut piyelonefrit, böbrek parankimini tutan sistemik ve ciddi bir enfeksiyon olup ayaktan "
        "tedavi edilecek hafif-orta olgularda dahi güçlü bir parenteral başlangıç dozu gerektirir.\n\n"
        "- **Başlangıç Önerisi:** Ülkemizde yüksek direnç oranları nedeniyle ayaktan piyelonefritte "
        "başlangıç tedavisi olarak **2 gr seftriakson ya da aminoglikozid** önerilir.\n"
        "- **Kültür Takibi:** Bu başlangıç parenteral dozunun ardından mutlaka **kültür takibi yapılmalıdır**; "
        "üreyen etkenin antibiyogram sonucuna göre oral tedavi şekillendirilir.\n"
        "- **Doku Penetrasyonu:** Seftriakson ve aminoglikozidler böbrek parankiminde ve idrarda "
        "çok yüksek konsantrasyonlara ulaşarak bakteriyemi ve sepsis gelişimini hızla bloke eder.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Ayaktan piyelonefritte yüksek direnç nedeniyle başlangıç tedavisi: 2 gr seftriakson ya da aminoglikozid parenteral uygulaması ve kültür takibidir."
    )
    s91_bullets = [
        "Başlangıç tedavisi: 2 gr seftriakson ya da aminoglikozid parenteral verilir.",
        "Kültür takibi mutlaka yapılmalıdır.",
        "Ülkemizdeki yüksek direnç oranları tek doz güçlü parenteral başlangıcı zorunlu kılar."
    ]
    s91_elements = [
        make_cloze("Ayaktan piyelonefrit başlangıç tedavisinde yüksek direnç oranları nedeniyle 2 gr seftriakson ya da aminoglikozid önerilir.", "2 gr seftriakson ya da aminoglikozid", "Piyelonefritteki güçlü parenteral başlangıç seçeneği"),
        make_table("Ayaktan Piyelonefrit Başlangıç Protokolü", ["Ajan", "Uygulama Dozu ve Şekli", "Klinik Zorunluluk"], [
            {"cells": [{"text": "Seftriakson", "isMasked": False}, {"text": "2 gram parenteral (IV/IM)", "isMasked": True, "hint": "iki gramlık yüksek seftriakson dozu"}, {"text": "Geniş parankim penetrasyonu"}]},
            {"cells": [{"text": "Aminoglikozid", "isMasked": False}, {"text": "Parenteral tek doz", "isMasked": False}, {"text": "Hızlı bakterisidal klirens", "isMasked": True, "hint": "hızlı mikrop öldürücü etki"}]},
            {"cells": [{"text": "Kültür Takibi", "isMasked": False}, {"text": "Mutlaka yapılmalıdır", "isMasked": True, "hint": "antibiyogram kontrolü"}, {"text": "Duyarlılığa göre oral tedaviye geçiş"}]}
        ]),
        make_chain("Ayaktan Piyelonefrit Başlangıç Akışı", [
            "1. Teşhis: Ateş, yan ağrısı ve KVA hassasiyeti ile piyelonefrit tespiti.",
            "2. İdrar ve Kan Kültürü: Antibiyotik öncesi örneklerin alınması.",
            "3. Başlangıç Dozu: Poliklinikte/Acilde 2 gr seftriakson veya aminoglikozid yapılması.",
            "4. Kültür Takibi: Sonuç çıkana kadar yakın ayaktan izlem."
        ]),
        make_recall("Ayaktan akut piyelonefritte ülkemizdeki yüksek direnç nedeniyle başlangıç tedavisinde önerilen parenteral rejim nedir?", "2 gr seftriakson ya da aminoglikozid uygulanması ve kültür takibidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Ayaktan Piyelonefrit", [
            {"text": "Ayaktan piyelonefrit başlangıcında 2 gr seftriakson ya da aminoglikozid önerilir.", "isLie": False, "explanation": "Doğru. Ders notu protokolüdür."},
            {"text": "Tedavi verildikten sonra kültür takibi yapılmalıdır.", "isLie": False, "explanation": "Doğru. Sonuç izlenmelidir."},
            {"text": "Ayaktan piyelonefritli hastaya sadece papatya çayı içirilip hiçbir antibiyotik verilmemelidir.", "isLie": True, "explanation": "Tuzak! Piyelonefrit böbrek parankim enfeksiyonudur; 2 gr seftriakson ya da aminoglikozid ile tedavi şarttır."},
            {"text": "Ülkemizdeki yüksek direnç oranları bu parenteral başlangıcı gerektirir.", "isLie": False, "explanation": "Doğru. Gerekçesi yerel dirençtir."}
        ]),
        make_quiz("Ayaktan akut piyelonefrit başlangıç ampirik tedavisinde ülkemizdeki yüksek direnç oranları nedeniyle önerilen ilk seçenek aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "2 gr seftriakson ya da aminoglikozid + kültür takibi", "isCorrect": True, "explanation": "Ders notunda açıkça 'başlangıç tedavisi olarak 2 gr seftriakson ya da aminoglikozid önerilir; kültür takibi yapılmalıdır' denmektedir."},
            {"key": "B", "text": "Ampisilin oral tablet 3 gün", "isCorrect": False, "explanation": "Ampisilin %60+ dirençlidir, piyelonefritte yeri yoktur."},
            {"key": "C", "text": "Nitrofurantoin tek doz", "isCorrect": False, "explanation": "Nitrofurantoin parankime geçmez, piyelonefritte kullanılmaz."},
            {"key": "D", "text": "Sadece idrar söktürücü çaylar", "isCorrect": False, "explanation": "Tıbbi tedavi değildir."}
        ])
    ]
    slides.append(make_slide(91, "Ayaktan Piyelonefrit Tedavisi", "2 gr seftriakson ya da aminoglikozid başlangıcı ve kültür takibi protokolü", "Piyelonefrit Tedavisi", s91_narrative, s91_bullets, s91_elements))

    # Slide 92: Ayaktan Piyelonefritte Alternatifler ve Florokinolon Kısıtlaması
    s92_narrative = (
        "Ayaktan piyelonefrit tedavisinde parenteral başlangıç sonrası veya oral devam aşamasında "
        "kullanılabilecek alternatif rejimler belirli süre ve direnç kurallarına bağlıdır.\n\n"
        "- **Alternatif Rejimler ve Süreleri:** 7 gün süre ile **siprofloksasin**; 5 gün süre ile "
        "**levofloksasin**; 7-10 gün süreyle **TMP-SXT**; 7-10 gün süre ile **amoksisilin klavulanik asit**tir.\n"
        "- **Siprofloksasin Kuralı:** Siprofloksasin **yalnızca yerel direnç <%10, 3. kuşak sefalosporin/"
        "aminoglikozid kontrendikasyonu veya beta-laktam aşırı duyarlılığı varsa** önerilir.\n"
        "- **Kesin Kontrendikasyon:** Ürolojide izlenen hastalarda veya **son altı ayda florokinolon "
        "kullanmış hastalarda** sistemik ÜSE'nin ampirik tedavisinde siprofloksasin/diğer florokinolonların kullanılması önerilmez.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Siprofloksasin ancak yerel direnç <%10 veya beta-laktam kontrendikasyonu varsa kullanılır; son 6 ayda florokinolon kullananlarda ve ürolojide izlenenlerde florokinolon ÖNERİLMEZ!"
    )
    s92_bullets = [
        "Alternatifler: Siprofloksasin 7 gün, levofloksasin 5 gün, TMP-SXT 7-10 gün, ko-amoksilav 7-10 gün.",
        "Siprofloksasin şartı: Yerel direnç <%10 veya beta-laktam kontrendikasyonu/alerjisi.",
        "Ürolojide izlenen veya son 6 ayda florokinolon kullananlarda florokinolon önerilmez."
    ]
    s92_elements = [
        make_cloze("Piyelonefritte siprofloksasin ancak yerel direnç <%10 veya beta-laktam kontrendikasyonu varsa kullanılır; son 6 ayda florokinolon alanlarda önerilmez.", "yerel direnç <%10", "Siprofloksasinin ampirik piyelonefritte kullanılabileceği katı direnç eşiği"),
        make_table("Ayaktan Piyelonefrit Alternatif İlaç Süreleri", ["Antibiyotik", "Tedavi Süresi", "Kullanım Şartı / Kısıtlama"], [
            {"cells": [{"text": "Siprofloksasin", "isMasked": False}, {"text": "7 gün", "isMasked": True, "hint": "yedi günlük süre"}, {"text": "Direnç <%10 veya beta-laktam alerjisi"}]},
            {"cells": [{"text": "Levofloksasin", "isMasked": False}, {"text": "5 gün", "isMasked": True, "hint": "beş günlük kür"}, {"text": "Kinolon kısıtlamalarına tabidir"}]},
            {"cells": [{"text": "TMP-SXT", "isMasked": False}, {"text": "7-10 gün", "isMasked": False}, {"text": "Kültürde duyarlıysa", "isMasked": True, "hint": "antibiyogram duyarlılık şartı"}]},
            {"cells": [{"text": "Amoksisilin-klavulanat", "isMasked": False}, {"text": "7-10 gün", "isMasked": False}, {"text": "Kültür takibi ile", "isMasked": True, "hint": "antibiyogram takibi"}]}
        ]),
        make_chain("Piyelonefritte Kinolon Karar Zinciri", [
            "1. Hasta Değerlendirmesi: Son 6 ayda kinolon kullanımı veya üroloji takibi var mı?",
            "2. Direnç Kontrolü: Bölgesel kinolon direnci <%10 mu?",
            "3. Beta-Laktam Alerjisi: Seftriakson/aminoglikozid verilemiyor mu?",
            "4. Karar: Bu şartlar sağlanıyorsa siprofloksasin 7 gün veya levo 5 gün başlama."
        ]),
        make_recall("Piyelonefritte siprofloksasinin kullanılabileceği yerel direnç eşiği nedir ve hangi iki hasta grubunda florokinolon önerilmez?", "Yerel direnç <%10 olmalıdır; ürolojide izlenen hastalarda ve son altı ayda florokinolon kullananlarda önerilmez."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Alternatifler ve Kinolon Kısıtı", [
            {"text": "Piyelonefritte alternatif olarak 7 gün siprofloksasin veya 5 gün levofloksasin kullanılabilir.", "isLie": False, "explanation": "Doğru. Ders notu süreleridir."},
            {"text": "Siprofloksasin yalnızca yerel direnç <%10 ise veya beta-laktam alerjisinde önerilir.", "isLie": False, "explanation": "Doğru. Kullanım kuralıdır."},
            {"text": "Son altı ayda florokinolon kullanmış bir hastaya yeni atakta hemen tekrar siprofloksasin verilmelidir.", "isLie": True, "explanation": "Tuzak! Son 6 ayda florokinolon kullananlarda sistemik ÜSE ampirik tedavisinde florokinolon önerilmez."},
            {"text": "TMP-SXT piyelonefritte 7-10 gün süreyle verilebilir.", "isLie": False, "explanation": "Doğru. Alternatif süresidir."}
        ]),
        make_quiz("Akut piyelonefrit tedavisinde siprofloksasin kullanımı ile ilgili aşağıdaki kurallardan hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Yalnızca yerel direnç <%10 veya beta-laktam kontrendikasyonu varsa önerilir; son 6 ayda kinolon kullananlarda önerilmez", "isCorrect": True, "explanation": "Ders notundaki iki temel kinolon uyarısıdır."},
            {"key": "B", "text": "Yerel direnç %90 olduğunda bile ilk tercihtir", "isCorrect": False, "explanation": "Direnç <%10 olmalıdır."},
            {"key": "C", "text": "Son 6 ayda kinolon kullananlarda zorunlu ilk seçenektir", "isCorrect": False, "explanation": "Tam tersine bu grupta önerilmez."},
            {"key": "D", "text": "Gebelikte en güvenli tek ilaçtır", "isCorrect": False, "explanation": "Gebelikte kinolonlar önerilmez."}
        ])
    ]
    slides.append(make_slide(92, "Piyelonefritte Alternatifler ve Kinolon Kısıtlaması", "Siprofloksasin 7 gün, levofloksasin 5 gün ve kinolon kısıtlama kuralları", "Piyelonefrit Tedavisi", s92_narrative, s92_bullets, s92_elements))

    # Slide 93: Yatarak Piyelonefrit Tedavisi: Parenteral Rejimler
    s93_narrative = (
        "Hastaneye yatış kriterlerini karşılayan akut piyelonefrit olgularında tedavi, intravenöz "
        "yoldan geniş spektrumlu bakterisidal ajanlarla derhal başlatılmalıdır.\n\n"
        "- **Parenteral Sefalosporinler:** Parenteral geniş spektrumlu sefalosporinler (**seftriakson, "
        "sefotaksim, sefepim**) birinci basamak seçenekler arasındadır.\n"
        "- **Beta-Laktam/İnhibitör:** Geniş spektrumlu beta-laktam/beta-laktamaz inhibitör kombinasyonları "
        "(**ampisilin-sulbaktam, piperasilin-tazobaktam**) ağır olgularda tercih edilir.\n"
        "- **Aminoglikozid ve Karbapenem:** Direnç riski veya sepsise eğilimli hastalarda **aminoglikozid "
        "veya karbapenem** rejimleri devreye sokulur.\n\n"
        "> [!IMPORTANT]\n"
        "> Yatarak piyelonefrit rejimleri: Parenteral sefalosporinler (seftriakson, sefotaksim, sefepim), inhibitörlü beta-laktamlar (SAM, PIP-TAZ), aminoglikozid veya karbapenemdir."
    )
    s93_bullets = [
        "Parenteral sefalosporinler: Seftriakson, sefotaksim, sefepim.",
        "Beta-laktam/inhibitör: Ampisilin-sulbaktam, piperasilin-tazobaktam.",
        "Direnç ve sepsiste aminoglikozid veya karbapenem seçenekleri.",
        "Parenteral uygulama ile parankimal ilaç düzeyi hızla garantiye alınır."
    ]
    s93_elements = [
        make_cloze("Yatarak piyelonefrit tedavisinde parenteral geniş spektrumlu sefalosporinler (seftriakson, sefotaksim, sefepim) ve piperasilin-tazobaktam kullanılır.", "seftriakson, sefotaksim, sefepim", "Yatarak tedavide kullanılan parenteral 3. ve 4. kuşak sefalosporinler"),
        make_table("Yatarak Piyelonefrit Parenteral İlaç Grupları", ["İlaç Grubu", "Spesifik Ajanlar", "Klinik Endikasyon Düzeyi"], [
            {"cells": [{"text": "Parenteral Sefalosporinler", "isMasked": False}, {"text": "Seftriakson, sefotaksim, sefepim", "isMasked": True, "hint": "üçüncü ve dördüncü kuşaklar"}, {"text": "Yatarak tedavide standart parenteral hat"}]},
            {"cells": [{"text": "Beta-Laktam/İnhibitörler", "isMasked": False}, {"text": "Ampisilin-sulbaktam, piperasilin-tazobaktam", "isMasked": False}, {"text": "Geniş spektrumlu parankimal tedavi", "isMasked": True, "hint": "ağır enfeksiyon kombine ajanları"}]},
            {"cells": [{"text": "İleri Rejimler", "isMasked": False}, {"text": "Aminoglikozid veya karbapenem", "isMasked": True, "hint": "dirençli basillere yönelik ilaçlar"}, {"text": "Direnç riski veya sepsiste kullanım"}]}
        ]),
        make_chain("Yatarak Tedavi Başlama Akışı", [
            "1. Servise Yatış: Oral alım bozukluğu veya toksisite ile yatış.",
            "2. Damar Yolu Açılması: İntravenöz hidrasyon ve parenteral hat.",
            "3. İlaç Seçimi: Seftriakson/sefepim veya PIP-TAZ başlanması.",
            "4. Klinik İzlem: Ateş, lökositoz ve semptom gerilemesinin takibi."
        ]),
        make_recall("Yatarak piyelonefrit tedavisinde önerilen parenteral ilaç grupları ve spesifik ajanlar nelerdir?", "Parenteral sefalosporinler (seftriakson, sefotaksim, sefepim), beta-laktam/inhibitörler (ampisilin-sulbaktam, piperasilin-tazobaktam), aminoglikozid veya karbapenemdir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Yatarak Tedavi Rejimleri", [
            {"text": "Seftriakson, sefotaksim ve sefepim yatarak tedavide kullanılabilir.", "isLie": False, "explanation": "Doğru. Ders notu sefalosporinleridir."},
            {"text": "Piperasilin-tazobaktam yatarak piyelonefrit seçeneklerindendir.", "isLie": False, "explanation": "Doğru. Geniş spektrumludur."},
            {"text": "Yatarak tedavi edilen piyelonefritli hastaya yalnızca ev yapımı sirke koklatılarak taburcu edilir.", "isLie": True, "explanation": "Tuzak! Yatarak piyelonefritte parenteral sefalosporin, PIP-TAZ veya karbapenem verilir."},
            {"text": "Ağır veya dirençli olgularda karbapenem veya aminoglikozid seçilebilir.", "isLie": False, "explanation": "Doğru. Ders notu seçeneğidir."}
        ]),
        make_quiz("Yatarak piyelonefrit tedavisinde kullanılan parenteral ajanlar arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Parenteral sefalosporinler (seftriakson, sefotaksim, sefepim), SAM, piperasilin-tazobaktam, aminoglikozid veya karbapenem", "isCorrect": True, "explanation": "Ders notundaki eksiksiz yatarak piyelonefrit ilaç listesidir."},
            {"key": "B", "text": "Yalnızca oral nistatin damla", "isCorrect": False, "explanation": "Ağız mantarı içindir, piyelonefritte yeri yoktur."},
            {"key": "C", "text": "Sadece aspirin tableti", "isCorrect": False, "explanation": "Ateş düşürücüdür, antibiyotik değildir."},
            {"key": "D", "text": "Lokal sürülen kortizonlu kremler", "isCorrect": False, "explanation": "Üriner sistemle ilgisizdir."}
        ])
    ]
    slides.append(make_slide(93, "Yatarak Piyelonefrit Tedavisi: Parenteral Seçenekler", "Parenteral sefalosporinler, PIP-TAZ, SAM, aminoglikozid ve karbapenem", "Piyelonefrit Tedavisi", s93_narrative, s93_bullets, s93_elements))

    # Slide 94: Oral Tedaviye Geçiş (48. Saat), Tedavi Süresi ve 72. Saat Ateşi
    s94_narrative = (
        "Yatarak parenteral tedavi alan piyelonefrit hastalarında de-eskalasyon zamanlaması ve "
        "tedaviye yanıtsızlık kriterleri çok net zaman kurallarıyla belirlenmiştir.\n\n"
        "- **Oral Tedaviye Geçiş:** Hasta parenteral tedavi alırken **ateşsiz 48. saatinden sonra "
        "oral tedaviye geçilir**.\n"
        "- **Toplam Tedavi Süresi:** Akut piyelonefritte toplam tedavi süresi klinik duruma göre "
        "**7-14 gündür**.\n"
        "- **72. Saat Ateş Uyarısı:** **Tedavinin 72. saatinden sonra devam eden ateş veya idrar kültüründe "
        "üreme durumunda komplikasyonlar açısından (renal apse, obstrüksiyon, perinefritik apse) tetkik** yapılmalıdır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Ateşsiz 48. saatten sonra oral tedaviye geçilir; toplam süre 7-14 gündür; tedavinin 72. saatinden sonra devam eden ateşte KOMPLİKASYONLAR açısından tetkik yapılmalıdır!"
    )
    s94_bullets = [
        "Ateşsiz 48. saatinden sonra oral tedaviye geçilir.",
        "Tedavi süresi klinik duruma göre 7-14 gündür.",
        "Tedavinin 72. saatinden sonra devam eden ateşte komplikasyonlar açısından tetkik yapılmalıdır."
    ]
    s94_elements = [
        make_cloze("Yatarak piyelonefritte ateşsiz 48. saatinden sonra oral tedaviye geçilir ve süre 7-14 gündür; 72. saatinden sonra devam eden ateşte komplikasyon araştırılır.", "72. saatinden sonra", "Komplikasyon araştırması gerektiren inatçı ateş zaman sınırı"),
        make_table("Piyelonefrit Zamanlama Kuralları", ["Klinik Eşik", "Zaman Kriteri", "Klinik Eylem"], [
            {"cells": [{"text": "Oral Tedaviye Geçiş", "isMasked": False}, {"text": "Ateşsiz 48. saatten sonra", "isMasked": True, "hint": "ateşin düşmesinden iki gün sonra"}, {"text": "Parenteralin kesilip orale dönülmesi"}]},
            {"cells": [{"text": "Toplam Tedavi Süresi", "isMasked": False}, {"text": "7-14 gün", "isMasked": False}, {"text": "Klinik duruma göre tam tamamlama", "isMasked": True, "hint": "bir ila iki haftalık süre"}]},
            {"cells": [{"text": "Komplikasyon Şüphesi", "isMasked": False}, {"text": "72. saatten sonra devam eden ateş", "isMasked": True, "hint": "üç gün süren inatçı ateş"}, {"text": "BT / USG ile apse ve obstrüksiyon tetkiki"}]}
        ]),
        make_chain("Piyelonefrit Klinik Zaman Akışı", [
            "1. Parenteral Başlangıç: Damardan antibiyotik tedavisi.",
            "2. 48. Saat Kuralı: Hastanın ateşsiz 48 saati tamamlamasıyla orale geçiş.",
            "3. 72. Saat Kontrolü: Ateş düşmemişse komplikasyon (apse vb.) tetkiki.",
            "4. Kür: Toplam 7-14 günde tedavinin sonlandırılması."
        ]),
        make_recall("Yatarak piyelonefritte oral tedaviye ne zaman geçilir, toplam süre nedir ve 72. saatte ateş sürerse ne yapılır?", "Ateşsiz 48. saatinden sonra oral tedaviye geçilir; toplam süre 7-14 gündür; 72. saatten sonra devam eden ateşte komplikasyonlar açısından tetkik yapılır."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Oral Geçiş ve 72 Saat", [
            {"text": "Ateşsiz 48. saatinden sonra oral tedaviye geçilir.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Tedavi süresi klinik duruma göre 7-14 gündür.", "isLie": False, "explanation": "Doğru. Standart süredir."},
            {"text": "Tedavinin 72. saatinden sonra ateş devam ederse bu normal kabul edilip hasta taburcu edilir.", "isLie": True, "explanation": "Tuzak! 72. saatten sonra devam eden ateşte apse veya komplikasyonlar açısından derhal tetkik yapılmalıdır."},
            {"text": "72. saatte idrarda üreme sürmesi de komplikasyon işaretidir.", "isLie": False, "explanation": "Doğru. Tedavi başarısızlığıdır."}
        ]),
        make_quiz("Akut piyelonefrit tedavisinde oral tedaviye geçiş zamanı, toplam süre ve 72. saat kuralı aşağıdakilerden hangisinde doğru verilmiştir?", [
            {"key": "A", "text": "Ateşsiz 48. saatten sonra oral tedaviye geçilir; toplam süre 7-14 gündür; 72. saatte ateş sürerse komplikasyon araştırılır", "isCorrect": True, "explanation": "Ders notunda harfiyen yer alan üç temel zamanlama kuralıdır."},
            {"key": "B", "text": "Ateş düşer düşmez ilk 1. dakikada tedavi tamamen kesilir", "isCorrect": False, "explanation": "En az 7-14 gün sürdürülmelidir."},
            {"key": "C", "text": "Tedavi süresi her zaman 6 aydır; ateş 1 yıl sürse bile tetkik yapılmaz", "isCorrect": False, "explanation": "Tıbbi kurallara aykırıdır."},
            {"key": "D", "text": "Oral tedaviye asla geçilemez, hasta ömür boyu hastanede damardan tedavi alır", "isCorrect": False, "explanation": "Ateşsiz 48 saatten sonra orale geçilir."}
        ])
    ]
    slides.append(make_slide(94, "Oral Tedaviye Geçiş (48. Saat) ve 72. Saat Ateşi", "Ateşsiz 48 saatte oral geçiş, 7-14 gün süre ve 72. saatte komplikasyon tetkiki", "Piyelonefrit Tedavisi", s94_narrative, s94_bullets, s94_elements))

    # Slide 95: Ürosepsis Tedavisi: Karbapenemler ve Gram Pozitif Kombinasyonu
    s95_narrative = (
        "Ürosepsis ve septik şok, üriner obstrüksiyon veya bakteriyemi zemininde hızla kardiyovasküler "
        "kollapsa yol açabilen en acil enfeksiyon tablosudur.\n\n"
        "- **Karbapenem Başlangıcı:** Sepsis/septik şok ve/veya üriner obstrüksiyon durumunda: dirençli "
        "Gram negatif etken şüphesiyle **imipenem, meropenem (antipseudomonal etkinlik)** başlanır.\n"
        "- **Gram Pozitif Şüphesi:** Dirençli Gram pozitif etken şüphesi (**MRSA, dirençli enterokok**) "
        "varsa rejime derhal **+ vankomisin, daptomisin veya teikoplanin** eklenir.\n"
        "- **Erken Müdahale:** Septik şokta ilk bir saat içinde başlanan uygun geniş spektrumlu "
        "parenteral tedavi sağkalımın en temel belirleyicisidir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Ürosepsis tedavisi: İmipenem veya meropenem başlanır; dirençli Gram pozitif (MRSA, dirençli enterokok) şüphesinde + vankomisin, daptomisin, teikoplanin eklenir."
    )
    s95_bullets = [
        "Sepsis/septik şok durumunda: İmipenem, meropenem (antipseudomonal etkinlik).",
        "Dirençli Gram pozitif şüphesinde: + Vankomisin, daptomisin, teikoplanin eklenir.",
        "Geniş spektrumlu bakterisidal kombinasyon hayat kurtarıcıdır."
    ]
    s95_elements = [
        make_cloze("Ürosepsis ve septik şok tedavisinde antipseudomonal etkili imipenem veya meropenem başlanır; Gram pozitif şüphesinde vankomisin, daptomisin veya teikoplanin eklenir.", "imipenem veya meropenem", "Ürosepsiste antipseudomonal etkili ilk basamak karbapenemler"),
        make_table("Ürosepsis Tedavi Protokolü", ["Hedef Patojen Şüphesi", "Seçilecek Antibiyotik", "Spektrum / Rol"], [
            {"cells": [{"text": "Dirençli Gram Negatif / Pseudomonas", "isMasked": False}, {"text": "İmipenem veya meropenem", "isMasked": True, "hint": "antipseudomonal karbapenem"}, {"text": "Antipseudomonal güçlü bakterisidal hat"}]},
            {"cells": [{"text": "Dirençli Gram Pozitif (MRSA, enterokok)", "isMasked": False}, {"text": "+ Vankomisin, daptomisin, teikoplanin", "isMasked": True, "hint": "glikopeptid veya lipopeptid ekleme"}, {"text": "MRSA ve dirençli enterokok kapsama"}]}
        ]),
        make_chain("Ürosepsis Acil Yönetim Zinciri", [
            "1. Tanı: SOFA artışı ve septik şok tablosunun tespiti.",
            "2. Karbapenem Başlangıcı: İmipenem veya meropenem infüzyonu.",
            "3. Gram Pozitif Değerlendirmesi: Kateter/MRSA riski varsa vankomisin eklenmesi.",
            "4. Obstrüksiyon Açılması: Üriner obstrüksiyon varsa derhal dekompresyon."
        ]),
        make_recall("Ürosepsis ve septik şokta ilk tercih edilen karbapenemler nelerdir ve MRSA şüphesinde ne eklenir?", "İmipenem veya meropenem başlanır; dirençli Gram pozitif (MRSA, enterokok) şüphesinde + vankomisin, daptomisin veya teikoplanin eklenir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Ürosepsis Tedavisi", [
            {"text": "Ürosepsiste imipenem ve meropenem antipseudomonal etkinlikle başlanır.", "isLie": False, "explanation": "Doğru. Ders notu protokolüdür."},
            {"text": "MRSA şüphesinde vankomisin, daptomisin veya teikoplanin eklenir.", "isLie": False, "explanation": "Doğru. Gram pozitif kombinasyonudur."},
            {"text": "Ürosepsisli hastaya sadece ağızdan C vitamini hapı verilip evine gönderilmelidir.", "isLie": True, "explanation": "Tuzak! Ürosepsis yoğun bakım takibi ve acil parenteral karbapenem ± vankomisin gerektirir."},
            {"text": "Septik şokta hemodinamik resüsitasyon ve acil antibiyotik esastır.", "isLie": False, "explanation": "Doğru. Hayat kurtarıcıdır."}
        ]),
        make_quiz("Üriner sistem enfeksiyonu nedeniyle gelişen sepsis/septik şok tablosunda ders notunda önerilen temel tedavi protokolü aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "İmipenem veya meropenem; dirençli Gram pozitif şüphesinde + vankomisin, daptomisin, teikoplanin", "isCorrect": True, "explanation": "Ders notunda harfiyen 'Ürosepsis tedavisi: imipenem, meropenem (antipseudomonal etkinlik); dirençli gram pozitif etken şüphesi varsa + vankomisin, daptomisin, teikoplanin eklenir' denmektedir."},
            {"key": "B", "text": "Ampisilin tek doz oral", "isCorrect": False, "explanation": "Sepsiste asla oral veya ampisilin verilmez."},
            {"key": "C", "text": "Sadece idrar torbasının boşaltılması ve ilaçsız izlem", "isCorrect": False, "explanation": "Antibiyotik verilmelidir."},
            {"key": "D", "text": "Yalnızca lokal pomad sürülmesi", "isCorrect": False, "explanation": "Sistemik yoğun tedavi şarttır."}
        ])
    ]
    slides.append(make_slide(95, "Ürosepsis Tedavisi: Karbapenemler ve Kombinasyon", "İmipenem/meropenem antipseudomonal protokolü ve Gram pozitif vankomisin eklenmesi", "Ürosepsis Tedavisi", s95_narrative, s95_bullets, s95_elements))

    # Slide 96: Kİ-ÜSE Tedavisi ve Karbapenem Dirençli Etkenler
    s96_narrative = (
        "Kateterle ilişkili üriner enfeksiyonlarda çoklu ilaç direnci sıktır; özellikle hastane "
        "kaynaklı suşlarda karbapenem direnci ortaya çıktığında son çare antibiyotikler devreye girer.\n\n"
        "- **Karbapenem Direnci Riski:** Kİ-ÜSE tedavisinde karbapenem dirençli etken (KPC, NDM, "
        "OXA-48 vb.) riski varsa ampirik ve hedefe yönelik rejimler genişletilir.\n"
        "- **Kullanılan Ajanlar:** **Aminoglikozid, kolistin, intravenöz (iv) fosfomisin, aminoglikozid-karbapenem "
        "kombinasyonu, ikili karbapenem kombinasyonu** kullanılır.\n"
        "- **Kateter Yönetimi:** Tedavinin vazgeçilmez bir parçası olarak enfeksiyon odağı olan eski "
        "kateter derhal çekilmeli veya yenisiyle değiştirilmelidir; aksi halde biyofilm eradike edilemez.\n\n"
        "> [!IMPORTANT]\n"
        "> Kİ-ÜSE tedavisinde karbapenem dirençli etken riski varsa: Aminoglikozid, kolistin, iv fosfomisin, aminoglikozid-karbapenem veya ikili karbapenem kombinasyonları uygulanır."
    )
    s96_bullets = [
        "Karbapenem dirençli etken riski varsa son seçenek ajanlar kullanılır.",
        "Seçenekler: Aminoglikozid, kolistin, iv fosfomisin.",
        "Kombinasyonlar: Aminoglikozid-karbapenem kombinasyonu veya ikili karbapenem kombinasyonu."
    ]
    s96_elements = [
        make_cloze("Kİ-ÜSE tedavisinde karbapenem dirençli etken riski varsa aminoglikozid, kolistin, iv fosfomisin ve ikili karbapenem kombinasyonu kullanılır.", "aminoglikozid, kolistin, iv fosfomisin", "Karbapenem direncinde kullanılan üç kritik parenteral antibiyotik"),
        make_table("Karbapenem Dirençli Kİ-ÜSE Tedavi Seçenekleri", ["Uygulama Tipi", "Antibiyotik / Rejim", "Klinik Özellik"], [
            {"cells": [{"text": "Monoterapi Seçenekleri", "isMasked": False}, {"text": "Aminoglikozid, kolistin, iv fosfomisin", "isMasked": True, "hint": "son çare antibiyotikler"}, {"text": "Dirençli Gram negatif klirensi"}]},
            {"cells": [{"text": "Kombinasyon Rejimleri", "isMasked": False}, {"text": "Aminoglikozid-karbapenem veya ikili karbapenem", "isMasked": True, "hint": "sinerjistik çift ajan tedavisi"}, {"text": "Karbapenemaz üreten suşlarda sinerji"}]}
        ]),
        make_chain("Kİ-ÜSE Direnç Yönetimi", [
            "1. Kateterin Çekilmesi/Değişimi: Biyofilmin fiziksel olarak uzaklaştırılması.",
            "2. Direnç Taraması: Karbapenem direnç riski varlığının saptanması.",
            "3. İlaç Seçimi: Kolistin, iv fosfomisin veya aminoglikozid kombinasyonu.",
            "4. Tedavi Takibi: Klinik iyileşme ve mikrobiyolojik klirensin izlenmesi."
        ]),
        make_recall("Kİ-ÜSE tedavisinde karbapenem dirençli etken riski varsa ders notunda belirtilen tedavi seçenekleri nelerdir?", "Aminoglikozid, kolistin, iv fosfomisin, aminoglikozid-karbapenem kombinasyonu ve ikili karbapenem kombinasyonudur."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Karbapenem Dirençli Kİ-ÜSE", [
            {"text": "Karbapenem dirençli etken riskinde kolistin ve iv fosfomisin kullanılabilir.", "isLie": False, "explanation": "Doğru. Ders notu seçenekleridir."},
            {"text": "İkili karbapenem kombinasyonu dirençli olgularda bir seçenektir.", "isLie": False, "explanation": "Doğru. Ders notunda yer alır."},
            {"text": "Karbapenem dirençli bakteriler sadece şekerli su içirilerek 5 dakikada yok edilir.", "isLie": True, "explanation": "Tuzak! Karbapenem dirençli etkenler kolistin, iv fosfomisin gibi son çare ajanlar gerektirir."},
            {"text": "Aminoglikozid-karbapenem kombinasyonu sinerji amacıyla uygulanabilir.", "isLie": False, "explanation": "Doğru. Ders notu protokolüdür."}
        ]),
        make_quiz("Kateterle ilişkili üriner sistem enfeksiyonunda (Kİ-ÜSE) karbapenem dirençli etken riski varlığında ders notunda önerilen rejimler arasında aşağıdakilerden hangisi YER ALIR?", [
            {"key": "A", "text": "Aminoglikozid, kolistin, iv fosfomisin, aminoglikozid-karbapenem kombinasyonu, ikili karbapenem kombinasyonu", "isCorrect": True, "explanation": "Ders notunda 'Kİ-ÜSE tedavisi: karbapenem dirençli etken riski varsa: aminoglikozid, kolistin, iv fosfomisin, aminoglikozid-karbapenem kombinasyonu, ikili karbapenem kombinasyonu' olarak listelenmiştir."},
            {"key": "B", "text": "Yalnızca oral amoksisilin", "isCorrect": False, "explanation": "Karbapenem direncinde amoksisilin tamamen etkisizdir."},
            {"key": "C", "text": "Sadece vitamin C", "isCorrect": False, "explanation": "Dirençli bakterileri öldürmez."},
            {"key": "D", "text": "Kateteri çekmeden sadece beklemek", "isCorrect": False, "explanation": "Aktif tedavi gerektirir."}
        ])
    ]
    slides.append(make_slide(96, "Kİ-ÜSE Tedavisi ve Karbapenem Direnci", "Kolistin, iv fosfomisin, aminoglikozid ve ikili karbapenem kombinasyonları", "Kİ-ÜSE Tedavisi", s96_narrative, s96_bullets, s96_elements))

    # Slide 97: Asemptomatik Bakteriüri Tedavi Endikasyonları: Gebeler ve Ürolojik İşlemler
    s97_narrative = (
        "Asemptomatik bakteriüri genel popülasyonda benign olup tedavi gerektirmezken, kanıta dayalı "
        "tıpta kesin tedavi endikasyonu bulunan iki kritik durum mevcuttur.\n\n"
        "- **Kesin İki Endikasyon:** Asemptomatik bakteriürinin kesin tedavi endikasyonları: **1) Gebeler, "
        "2) Mukozal hasarın olacağı ürolojik prosedür uygulanacak hastalar**dır.\n"
        "- **Ürolojik İşlem Zamanlaması:** Mukozal kanama riski taşıyan ürolojik prosedürde **işlemden "
        "24 saat önce etkene yönelik antimikrobiyal ajan başlanmalı, işlem sonrası kesilmelidir**.\n"
        "- **Göreceli Endikasyon:** Renal transplantasyonun erken döneminde (<1 ay) olan hastalar "
        "göreceli endikasyondur; ancak **posttransplant birinci aydan sonra ABU tedavisinin graft fonksiyonu, "
        "rejeksiyon ve mortalite üzerine katkısı yoktur**.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] ABU kesin tedavi endikasyonları: Gebeler ve mukozal hasarlı ürolojik prosedürlerdir (işlemden 24 saat önce başlanır, işlem sonrası kesilir); posttransplant 1. aydan sonra ABU tedavisinin faydası yoktur!"
    )
    s97_bullets = [
        "Kesin tedavi endikasyonları: Gebeler ve mukozal hasarlı ürolojik prosedürler.",
        "Ürolojik prosedürde işlemden 24 saat önce başlanır, işlem sonrası kesilir.",
        "Renal transplantasyonun ilk 1 ayında göreceli endikedir; 1. aydan sonra tedavi faydasızdır."
    ]
    s97_elements = [
        make_cloze("Mukozal hasarlı ürolojik prosedür uygulanacak hastalarda ABU tedavisi işlemden 24 saat önce başlanmalı, işlem sonrası kesilmelidir.", "işlemden 24 saat önce", "Ürolojik işlem öncesi antibiyotik başlama zamanı"),
        make_table("ABU Tedavi Endikasyonları ve Zamanlaması", ["Klinik Endikasyon", "Tedavi Durumu", "Uygulama Kuralı / Süresi"], [
            {"cells": [{"text": "Gebeler", "isMasked": False}, {"text": "KESİN TEDAVİ ENDİKASYONU", "isMasked": True, "hint": "mutlak tedavi şartı"}, {"text": "Piyelonefrit ve erken doğumu önleme"}]},
            {"cells": [{"text": "Ürolojik Prosedür (Mukozal Hasarlı)", "isMasked": False}, {"text": "KESİN TEDAVİ ENDİKASYONU", "isMasked": False}, {"text": "İşlemden 24 saat önce başla, sonra kes", "isMasked": True, "hint": "yirmi dört saat önce kuralı"}]},
            {"cells": [{"text": "Posttransplant Erken (<1 ay)", "isMasked": False}, {"text": "Göreceli tedavi endikasyonu", "isMasked": True, "hint": "koşullu endikasyon"}, {"text": "Erken dönemde graft koruma"}]},
            {"cells": [{"text": "Posttransplant >1 Ay Sonrası", "isMasked": False}, {"text": "TEDAVİ EDİLMEZ (katkısı yoktur)", "isMasked": False}, {"text": "Graft, rejeksiyon ve sağkalıma etkisi yok", "isMasked": True, "hint": "faydasız tedavi"}]}
        ]),
        make_chain("ABU Tedavi Karar Şeması", [
            "1. ABU Tespiti: Semptomsuz hastada ≥10⁵ CFU/mL üreme.",
            "2. Gebe mi?: Gebe ise derhal etkene yönelik tedavi başlama.",
            "3. Mukozal Ürolojik İşlem mi?: İşlemden 24 saat önce antibiyotik başlama.",
            "4. Transplant Kontrolü: 1. aydan sonra ise tedavi vermeme."
        ]),
        make_recall("Asemptomatik bakteriürinin kesin tedavi edildiği iki klinik durum ve ürolojik işlemdeki zamanlama kuralı nedir?", "Gebeler ve mukozal hasarlı ürolojik prosedür uygulanacak hastalardır; işlemden 24 saat önce başlanmalı, işlem sonrası kesilmelidir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: ABU Endikasyonları", [
            {"text": "Gebelerde asemptomatik bakteriüri kesin tedavi endikasyonudur.", "isLie": False, "explanation": "Doğru. Ders notu kuralıdır."},
            {"text": "Mukozal hasarlı ürolojik prosedürde işlemden 24 saat önce antibiyotik başlanmalıdır.", "isLie": False, "explanation": "Doğru. Zamanlama kuralıdır."},
            {"text": "Posttransplant 5. yılda olan semptomsuz her hastaya ömür boyu zorunlu antibiyotik verilir.", "isLie": True, "explanation": "Tuzak! Posttransplant birinci aydan sonra ABU tedavisinin graft ve mortaliteye katkısı yoktur, tedavi edilmez."},
            {"text": "Ürolojik işlem sonrası antibiyotik kesilmelidir.", "isLie": False, "explanation": "Doğru. Profilaktik yaklaşımdır."}
        ]),
        make_quiz("Asemptomatik bakteriürinin (ABU) kesin tedavi edilmesi gereken durumlar ve ürolojik işlem zamanlaması aşağıdakilerden hangisinde DOĞRU verilmiştir?", [
            {"key": "A", "text": "Gebeler ve mukozal hasarlı ürolojik işlem planlananlar (işlemden 24 saat önce başlanmalı, işlem sonrası kesilmelidir)", "isCorrect": True, "explanation": "Ders notundaki iki kesin endikasyon ve işlemden 24 saat önce başlama kuralıdır."},
            {"key": "B", "text": "Huzurevinde kalan tüm sağlıklı yaşlılar", "isCorrect": False, "explanation": "Yaşlıda ABU tedavi edilmez."},
            {"key": "C", "text": "Posttransplant 1. yılı doldurmuş semptomsuz hastalar", "isCorrect": False, "explanation": "1. aydan sonra tedavinin katkısı yoktur."},
            {"key": "D", "text": "Sadece genç erkek sporcular", "isCorrect": False, "explanation": "ABU endikasyonu değildir."}
        ])
    ]
    slides.append(make_slide(97, "ABU Tedavi Endikasyonları: Gebelik ve Ürolojik İşlemler", "Gebelerde ve ürolojik işlem planlananlarda (işlemden 24 saat önce) ABU tedavisi", "Asemptomatik Bakteriüri Tedavisi", s97_narrative, s97_bullets, s97_elements))

    # Slide 98: Tekrarlayan ÜSE Tedavisi ve Postkoital Profilaksi
    s98_narrative = (
        "Tekrarlayan üriner enfeksiyonların yönetiminde cerrahi düzeltmeler ve hastanın klinik "
        "öyküsüne göre bireyselleştirilmiş profilaksi protokolleri uygulanır.\n\n"
        "- **Anatomi Düzeltmesi:** Altta yatan vezikoüreteral reflü, taş veya üretra darlığı gibi "
        "**ürolojik anomali varsa cerrahi** tedavi planlanmalıdır.\n"
        "- **Postkoital Profilaksi:** Reenfeksiyonlar cinsel ilişki (koitus) ile ilişkili ise koitus "
        "sonrasında **tek doz TMP-SXT ya da 100 mg nitrofurantoin** uygulaması atağı son derece etkili biçimde önler.\n"
        "- **Uzun Süreli Profilaksi:** Reenfeksiyon herhangi bir predispozan faktör ile ilişkilendirilemez "
        "ve semptomlar şiddetli olursa düşük doz uzun süreli (6 ay) profilaksi uygulanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Reenfeksiyonlar koitus ilişkili ise postkoital profilaksi: Tek doz TMP-SXT ya da 100 mg nitrofurantoin verilir."
    )
    s98_bullets = [
        "Altta yatan ürolojik anomali varsa cerrahi tedavi uygulanır.",
        "Koitus ilişkili reenfeksiyonlarda postkoital profilaksi: Tek doz TMP-SXT ya da 100 mg nitrofurantoin.",
        "Predispozan faktör saptanamayan şiddetli vakalarda uzun süreli profilaksi verilir."
    ]
    s98_elements = [
        make_cloze("Tekrarlayan ÜSE'de reenfeksiyonlar koitus ilişkili ise postkoital profilaksi olarak tek doz TMP-SXT ya da 100 mg nitrofurantoin uygulanır.", "tek doz TMP-SXT ya da 100 mg nitrofurantoin", "Postkoital profilaksinin standart iki ilaç seçeneği"),
        make_table("Tekrarlayan ÜSE Tedavi Seçenekleri", ["Klinik Durum", "Tedavi Stratejisi", "İlaç ve Doz"], [
            {"cells": [{"text": "Ürolojik Anomali", "isMasked": False}, {"text": "Cerrahi düzeltme", "isMasked": True, "hint": "yapısal tamir ameliyatı"}, {"text": "Anatominin restore edilmesi"}]},
            {"cells": [{"text": "Koitus İlişkili Reenfeksiyon", "isMasked": False}, {"text": "Postkoital profilaksi", "isMasked": False}, {"text": "Tek doz TMP-SXT ya da 100 mg nitrofurantoin", "isMasked": True, "hint": "ilişki sonrası tek doz ilaç"}]},
            {"cells": [{"text": "Açıklanamayan Şiddetli Nüks", "isMasked": False}, {"text": "Uzun süreli profilaksi", "isMasked": True, "hint": "uzun dönem koruma"}, {"text": "Gece yatarken düşük doz antibiyotik"}]}
        ]),
        make_chain("Postkoital Profilaksi Mantığı", [
            "1. Anamnez: Nükslerin cinsel ilişkiden 24-48 saat sonra geliştiğinin saptanması.",
            "2. Postkoital Reçete: İlişki sonrasında tek doz ilaç alınması talimatı.",
            "3. İlaç Seçimi: Tek doz TMP-SXT veya 100 mg nitrofurantoin.",
            "4. Koruma: Mekanik itilen bakterilerin mesanede çoğalamadan yok edilmesi."
        ]),
        make_recall("Koitus ilişkili reenfeksiyonlarda postkoital profilaksi için önerilen ilaçlar ve dozları nelerdir?", "Tek doz TMP-SXT ya da 100 mg nitrofurantoindir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Postkoital Profilaksi", [
            {"text": "Koitus ilişkili reenfeksiyonlarda postkoital profilaksi uygulanabilir.", "isLie": False, "explanation": "Doğru. Ders notu yaklaşımıdır."},
            {"text": "Postkoital profilakside tek doz TMP-SXT ya da 100 mg nitrofurantoin verilir.", "isLie": False, "explanation": "Doğru. İki standart seçenektir."},
            {"text": "Altta yatan ürolojik anomali varsa cerrahi düzeltme yapılır.", "isLie": False, "explanation": "Doğru. Yapısal sorun cerrahidir."},
            {"text": "Postkoital profilakside her cinsel ilişkiden sonra hastaya 50 kutu kemoterapi ilacı verilir.", "isLie": True, "explanation": "Tuzak! Postkoital profilaksi yalnızca tek doz TMP-SXT veya 100 mg nitrofurantoindir."}
        ]),
        make_quiz("Tekrarlayan üriner sistem enfeksiyonlarında reenfeksiyonlar koitus (cinsel ilişki) ile ilişkili olduğunda önerilen postkoital profilaksi rejimi aşağıdakilerden hangisidir?", [
            {"key": "A", "text": "Tek doz TMP-SXT ya da 100 mg nitrofurantoin", "isCorrect": True, "explanation": "Ders notunda harfiyen 'Reenfeksiyonlar koitus ilişkili ise postkoital profilaksi: tek doz TMP-SXT ya da 100 mg nitrofurantoin' denmektedir."},
            {"key": "B", "text": "14 gün boyunca damardan meropenem", "isCorrect": False, "explanation": "Postkoital profilaksi değildir."},
            {"key": "C", "text": "Sadece her gün 1 bardak süt içmek", "isCorrect": False, "explanation": "Tıbbi profilaksi değildir."},
            {"key": "D", "text": "Günde 4 kez aminoglikozid", "isCorrect": False, "explanation": "Profilaksi rejimi değildir."}
        ])
    ]
    slides.append(make_slide(98, "Tekrarlayan ÜSE Tedavisi ve Postkoital Profilaksi", "Ürolojik anomali cerrahisi ve tek doz TMP-SXT / 100 mg nitrofurantoin profilaksisi", "Tekrarlayan ÜSE Tedavisi", s98_narrative, s98_bullets, s98_elements))

    # Slide 99: Kandidüri Tedavisi: Asemptomatik, Sistit ve Piyelonefrit Rejimleri
    s99_narrative = (
        "Üriner sistemde Candida türlerinin saptanması (kandidüri), asemptomatik kolonizasyondan "
        "renal parankimal mantar enfeksiyonlarına kadar uzanan özgül antifungal rejimler gerektirir.\n\n"
        "- **Asemptomatik Kandidüri Endikasyonları:** Yalnızca **nötropenik hastalar, düşük doğum "
        "ağırlıklı infantlar veya ürolojik girişim uygulanacak hastalar**da tedavi edilir.\n"
        "- **Semptomatik Sistit:** Azol duyarlı suşlarda **oral flukonazol 1x200 mg**; azol dirençli "
        "Candida glabrata ve Candida krusei'de sistemik **amfoterisin B ya da amfoterisin B ile irrigasyon** uygulanır.\n"
        "- **Klinik Piyelonefrit:** Obstrüksiyon değerlendirilmeli; azol duyarlılarda **flukonazol "
        "200-400 mg**, azol dirençli C. glabrata ve C. krusei için sistemik **amfoterisin B deoksikolat 14 gün süreyle** verilir.\n\n"
        "> [!IMPORTANT]\n"
        "> [SINAV SPOTU] Kandidüri tedavisi: Sistitte flukonazol 1x200 mg; dirençli C. glabrata/krusei'de sistemik amfoterisin B (piyelonefritte 14 gün) verilir; asemptomatikte nötropenik/ürolojik girişimde tedavi edilir."
    )
    s99_bullets = [
        "Asemptomatik kandidüri: Nötropenik, düşük doğum ağırlıklı infant, ürolojik girişimde tedavi edilir.",
        "Semptomatik sistit: Azol duyarlıya oral flukonazol 1x200 mg; dirençlide amfoterisin B.",
        "Piyelonefrit: Flukonazol 200-400 mg; C. glabrata ve C. krusei'de sistemik amfoterisin B 14 gün."
    ]
    s99_elements = [
        make_cloze("Kandidüri tedavisinde azol dirençli Candida glabrata ve Candida krusei piyelonefritinde sistemik amfoterisin B deoksikolat 14 gün süreyle kullanılır.", "14 gün süreyle", "Amfoterisin B ile piyelonefrit tedavi süresi"),
        make_table("Kandidüri Tedavi Şeması", ["Klinik Tablo", "Candida Türü / Duyarlılık", "Önerilen Antifungal Rejim"], [
            {"cells": [{"text": "Asemptomatik Kandidüri", "isMasked": False}, {"text": "Nötropenik / Ürolojik girişim", "isMasked": True, "hint": "özel endikasyon grupları"}, {"text": "Antifungal tedavi endikedir"}]},
            {"cells": [{"text": "Semptomatik Sistit", "isMasked": False}, {"text": "Azol duyarlı Candida spp.", "isMasked": False}, {"text": "Oral flukonazol 1x200 mg", "isMasked": True, "hint": "sistit flukonazol dozu"}]},
            {"cells": [{"text": "Dirençli Sistit / Piyelonefrit", "isMasked": False}, {"text": "C. glabrata ve C. krusei", "isMasked": True, "hint": "azol dirençli türler"}, {"text": "Sistemik amfoterisin B (piyelonefritte 14 gün)"}]}
        ]),
        make_chain("Kandidüri Karar Algoritması", [
            "1. Kandidüri Tespiti: İdrarda Candida üremesi saptanması.",
            "2. Semptom ve Risk Taraması: Semptom var mı, nötropenik mi, girişim var mı?",
            "3. Tür Tayini: C. albicans mı yoksa dirençli C. glabrata/krusei mi?",
            "4. İlaç Seçimi: Duyarlıya flukonazol (200 mg), dirençliye amfoterisin B (14 gün)."
        ]),
        make_recall("Kandidüri tedavisinde sistitte azol duyarlı suşlara ve azol dirençli C. glabrata/krusei'ye hangi tedaviler verilir?", "Azol duyarlı suşlarda oral flukonazol 1x200 mg; azol dirençli C. glabrata ve C. krusei'de sistemik amfoterisin B (piyelonefritte 14 gün) verilir."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Kandidüri Tedavisi", [
            {"text": "Azol duyarlı Candida sistitinde oral flukonazol 1x200 mg verilir.", "isLie": False, "explanation": "Doğru. Ders notu dozudur."},
            {"text": "C. glabrata ve C. krusei azol dirençli olduğunda amfoterisin B kullanılır.", "isLie": False, "explanation": "Doğru. Dirençli tür protokolüdür."},
            {"text": "Asemptomatik kandidürili her hasta hiçbir risk faktörü olmasa bile derhal ameliyat edilmelidir.", "isLie": True, "explanation": "Tuzak! Asemptomatik kandidüri sadece nötropenik, düşük doğum ağırlıklı infant veya ürolojik girişim planlananlarda tedavi edilir."},
            {"text": "Piyelonefritte amfoterisin B deoksikolat 14 gün süreyle kullanılır.", "isLie": False, "explanation": "Doğru. Tedavi süresidir."}
        ]),
        make_quiz("Kandidüri tedavisi ile ilgili ders notunda belirtilen kurallar değerlendirildiğinde aşağıdakilerden hangisi DOĞRUDUR?", [
            {"key": "A", "text": "Sistitte azol duyarlıya oral flukonazol 1x200 mg; azol dirençli C. glabrata/krusei'de sistemik amfoterisin B verilir", "isCorrect": True, "explanation": "Ders notundaki eksiksiz kandidüri protokolüdür."},
            {"key": "B", "text": "Candida glabrata her zaman flukonazole en duyarlı türdür", "isCorrect": False, "explanation": "C. glabrata azole dirençlidir."},
            {"key": "C", "text": "Asemptomatik kandidüri tüm insanlarda zorunlu tedavi endikasyonudur", "isCorrect": False, "explanation": "Yalnızca nötropenik, prematüre veya ürolojik girişimde tedavi edilir."},
            {"key": "D", "text": "Mantar enfeksiyonunda penisilin en etkili ilaçtır", "isCorrect": False, "explanation": "Mantar antibakteriyellerle tedavi edilmez."},
        ])
    ]
    slides.append(make_slide(99, "Kandidüri Tedavisi: Flukonazol ve Amfoterisin B", "Sistitte flukonazol 200 mg ve azol dirençli C. glabrata/krusei'de amfoterisin B (14 gün)", "Kandidüri Tedavisi", s99_narrative, s99_bullets, s99_elements))

    # Slide 100: [TEKRAR SAYFASI - CHECKPOINT 10] Tedavi Protokolleri ve Final Konsolidasyon
    s100_narrative = (
        "Bu son tekrar sayfasında 10. Bölümde işlenen piyelonefrit, ürosepsis, ABU tedavi endikasyonları, "
        "postkoital profilaksi ve kandidüri tedavi rejimlerini pekiştiriyoruz.\n\n"
        "- **Piyelonefrit ve Sepsis:** Ayaktan piyelonefritte **2 gr seftriakson/aminoglikozid + kültür**; "
        "yatarakta parenteral sefalosporin/PIP-TAZ/karbapenem (ateşsiz 48. saatte oral, toplam 7-14 gün, 72. saatte tetkik); "
        "ürosepsiste **imipenem/meropenem ± vankomisin**.\n"
        "- **ABU ve Profilaksi:** ABU yalnız **gebeler ve ürolojik prosedürde (24 saat önce)** tedavi edilir; "
        "koitus ilişkili nükste postkoital **tek doz TMP-SXT ya da 100 mg nitrofurantoin**.\n"
        "- **Kandidüri:** Sistitte **flukonazol 1x200 mg**; azol dirençli C. glabrata ve C. krusei'de "
        "**sistemik amfoterisin B (piyelonefritte 14 gün)** uygulanır.\n\n"
        "> [!IMPORTANT]\n"
        "> [TEKRAR SAYFASI - CHECKPOINT 10] Ayaktan piyelonefritte 2 gr seftriakson/aminoglikozid; sepsiste imipenem/meropenem ± vankomisin; ABU gebeler ve ürolojik işlemde (24 saat önce); postkoital tek doz TMP-SXT/nitrofurantoin; kandidüride flukonazol 200 mg vs amfoterisin B (14 gün)."
    )
    s100_bullets = [
        "Piyelonefrit: 2 gr seftriakson ya da aminoglikozid; yatarakta parenteral 7-14 gün (48. saat oral, 72. saat tetkik).",
        "Ürosepsis: İmipenem/meropenem ± vankomisin, daptomisin, teikoplanin.",
        "ABU: Gebeler ve ürolojik prosedür (işlemden 24 saat önce başla, sonra kes).",
        "Postkoital profilaksi: Tek doz TMP-SXT ya da 100 mg nitrofurantoin.",
        "Kandidüri: Flukonazol 1x200 mg; azol dirençlide amfoterisin B (piyelonefrit 14 gün)."
    ]
    s100_elements = [
        make_cloze("Ürosepsis tedavisinde imipenem veya meropenem başlanırken ayaktan piyelonefritte 2 gr seftriakson ya da aminoglikozid önerilir.", "2 gr seftriakson ya da aminoglikozid", "Ayaktan piyelonefritin başlangıç parenteral seçeneği"),
        make_table("10. Bölüm ve Deste Final Özet Tablosu", ["Klinik Tablo", "Temel İlaç / Protokol", "Kritik Kural / Süre"], [
            {"cells": [{"text": "Ayaktan Piyelonefrit", "isMasked": False}, {"text": "2 gr seftriakson ya da aminoglikozid", "isMasked": True, "hint": "başlangıç parenteral dozu"}, {"text": "Kültür takibi ile oral geçiş"}]},
            {"cells": [{"text": "Ürosepsis ve Şok", "isMasked": False}, {"text": "İmipenem/meropenem ± vankomisin", "isMasked": False}, {"text": "Antipseudomonal + MRSA kapsamı", "isMasked": True, "hint": "geniş sepsis kombinasyonu"}]},
            {"cells": [{"text": "ABU Tedavi Endikasyonu", "isMasked": False}, {"text": "Gebeler ve ürolojik prosedür", "isMasked": True, "hint": "iki kesin endikasyon"}, {"text": "İşlemden 24 saat önce başlanır"}]},
            {"cells": [{"text": "Postkoital Profilaksi", "isMasked": False}, {"text": "Tek doz TMP-SXT / 100 mg nitrofurantoin", "isMasked": False}, {"text": "Koitus ilişkili reenfeksiyonda", "isMasked": True, "hint": "ilişki sonrası tek doz"}]},
            {"cells": [{"text": "Kandidüri", "isMasked": False}, {"text": "Flukonazol 200 mg vs Amfoterisin B", "isMasked": True, "hint": "mantar tedavi ikilisi"}, {"text": "C. glabrata/krusei'de amfo B (14 gün)"}]}
        ]),
        make_chain("Final Sentez Zinciri", [
            "1. Ayaktan Piyelonefrit: 2 gr seftriakson/aminoglikozid başlanması.",
            "2. Yatarak/Sepsis: İmipenem/meropenem ± vankomisin (72. saatte komplikasyon kontrolü).",
            "3. ABU Kararı: Gebelerde ve ürolojik işlemde 24 saat önce profilaksi.",
            "4. Kandidüri ve Profilaksi: Flukonazol/Amfo B ve postkoital tek doz TMP-SXT."
        ]),
        make_recall("Checkpoint 10: Ayaktan piyelonefrit başlangıcı, ürosepsis rejimi, ABU kesin endikasyonları ve kandidüri amfoterisin B süresi nedir?", "Ayaktan piyelonefrit: 2 gr seftriakson/aminoglikozid; ürosepsis: imipenem/meropenem ± vankomisin; ABU: gebeler ve ürolojik işlem (24 saat önce); kandidüri amfoterisin B süresi piyelonefritte 14 gündür."),
        make_spot_lie("Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Checkpoint 10 Konsolidasyonu", [
            {"text": "Ayaktan piyelonefrit başlangıcında 2 gr seftriakson ya da aminoglikozid önerilir.", "isLie": False, "explanation": "Doğru. 10. bölüm temel kuralıdır."},
            {"text": "Ürosepsis tedavisinde imipenem veya meropenem ± vankomisin verilir.", "isLie": False, "explanation": "Doğru. Sepsis protokolüdür."},
            {"text": "Asemptomatik bakteriüri hiçbir zaman gebelerde tedavi edilmez, gebelere antibiyotik vermek yasaktır.", "isLie": True, "explanation": "Tuzak! Gebeler asemptomatik bakteriürinin kesin tedavi endikasyonudur."},
            {"text": "Kandidüri tedavisinde azol dirençli türlerde amfoterisin B (14 gün) kullanılır.", "isLie": False, "explanation": "Doğru. Tedavi süresidir."}
        ]),
        make_quiz("10. Bölümün tamamı (Piyelonefrit, Ürosepsis ve Kandidüri Tedavisi) değerlendirildiğinde aşağıdaki ifadelerden hangisi YANLIŞTIR?", [
            {"key": "A", "text": "Posttransplant 1. aydan sonra asemptomatik bakteriüri tedavisi graft fonksiyonunu ve sağkalımı katlar", "isCorrect": True, "explanation": "Yanlış! Ders notunda açıkça 'Posttransplant birinci aydan sonra asemptomatik bakteriüri tedavisinin graft fonksiyonu, rejeksiyon ve mortalite üzerine katkısı yoktur' denmektedir."},
            {"key": "B", "text": "Ayaktan piyelonefrit başlangıç tedavisinde 2 gr seftriakson ya da aminoglikozid önerilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "C", "text": "Ürosepsis tedavisinde imipenem/meropenem; Gram pozitif şüphesinde + vankomisin verilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."},
            {"key": "D", "text": "Reenfeksiyonlar koitus ilişkili ise postkoital tek doz TMP-SXT ya da 100 mg nitrofurantoin verilir", "isCorrect": False, "explanation": "Doğru bir bilgidir."}
        ])
    ]
    slides.append(make_slide(100, "[TEKRAR SAYFASI - CHECKPOINT 10] Tedavi Protokolleri ve Final Konsolidasyon", "10. Bölümün ve destenin kapsamlı final pekiştirmesi: piyelonefrit, ürosepsis, ABU ve kandidüri", "Bölüm Tekrarı", s100_narrative, s100_bullets, s100_elements))

    return slides
