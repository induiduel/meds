"""
Deck 61: Abortus - Section 10 (Slides 91-100)
Konu: Tekrarlayan Gebelik Kaybı (Rekürren Abortus - RPL), Etiyoloji, Önerilen Testler ve Büyük Final Checkpoint
Müfredat: TIP 310 · Abortus · Dr. Öğr. Üyesi Hilal Ezgi Türkmen · Dönem 3 Kurul 1
"""

from typing import List, Dict, Any
from .deck61_helper import (
    make_slide,
    make_quiz,
    make_cloze,
    make_table,
    make_slider,
    make_chain,
    make_recall,
    make_spot_the_lie,
    make_swipe,
    make_venn,
    make_branching
)

def get_sec10_slides() -> List[Dict[str, Any]]:
    slides = [
        # Slide 91
        make_slide(
            slide_num=91,
            title="Tekrarlayan Gebelik Kaybı (Rekürren Abortus): Dernek Tanımları",
            subtitle="ASRM, ESHRE ve RCOG Tanım ve Kriter Farklılıkları",
            clinical_focus="Farklı uluslararası derneklerin rekürren abortus tanımları ve sınırları sınavların en klasik sorularındandır.",
            narrative="""Tekrarlayan gebelik kaybı (TGK / RPL), çiftlerin ardışık gebelik kayıpları yaşaması durumudur. Uluslararası obstetrik dernekleri bu sendromu farklı kriterlerle tanımlamaktadır ve ders notunda bu tanımlar açıkça ayrılmıştır.

- **ASRM (2012, 2013) Tanımı:** Amerikan Üreme Tıbbı Derneği (ASRM), **2 veya daha fazla klinik gebelik kaybını** tekrarlayan gebelik kaybı olarak kabul eder. Biyokimyasal gebelikler bu tanıma dahil edilmez.
- **ESHRE (2019) Tanımı:** Avrupa İnsan Üremesi ve Embriyolojisi Derneği (ESHRE), **viabilite sınırına (24. gebelik haftasına) ulaşmadan önceki gebelik kayıplarını** esas alır. ESHRE tanımında ektopik gebelik, gestasyonel trofoblastik neoplazi (GTN) ve implantasyon başarısızlığı hariç tutulur.
- **RCOG (2011) Tanımı:** İngiltere Kraliyet Kadın Doğum Derneği (RCOG) ise **ardışık 3 veya daha fazla gebelik kaybını** şart koşar.

> [!IMPORTANT]
> ASRM 2 veya daha fazla klinik kayıp ararken, RCOG ardışık 3 veya daha fazla kayıp şartı koşar; ESHRE ise 24 hafta viabilite sınırını vurgular (ektopik ve mol hariç).""",
            bullets=[
                "ASRM: 2 veya daha fazla klinik gebelik kaybı",
                "ESHRE: Viabilite sınırından (24. hf) önce; ektopik, GTN ve implantasyon başarısızlığı hariç",
                "RCOG: Ardışık 3 veya daha fazla gebelik kaybı"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre Tekrarlayan Gebelik Kaybı (Rekürren Abortus) tanımları ile ilgili aşağıdaki dernek eşleştirmelerinden hangisi YANLIŞTIR?",
                    options=[
                        {"key": "A", "text": "ASRM (2012, 2013): 2 veya daha fazla klinik gebelik kaybı", "isCorrect": False, "explanation": "Doğrudur. Ders notundaki ASRM resmi tanımıdır."},
                        {"key": "B", "text": "RCOG (2011): Ardışık 3 veya daha fazla gebelik kaybı", "isCorrect": False, "explanation": "Doğrudur. Ders notundaki RCOG resmi tanımıdır."},
                        {"key": "C", "text": "ESHRE (2019): Tek bir kimyasal gebelik kaybı yeterlidir", "isCorrect": True, "explanation": "Yanlış (Tuzak!). ESHRE viabilite sınırına (24 hf) kadar olan kayıpları alır; ektopik, GTN ve implantasyon başarısızlığı hariçtir."},
                        {"key": "D", "text": "ESHRE (2019): Viabilite sınırına (24 hafta) ulaşmadan önce gebelik kaybı; ektopik, GTN ve implantasyon başarısızlığı hariç", "isCorrect": False, "explanation": "Doğrudur. Ders notundaki ESHRE tanımıdır."}
                    ],
                    correct_key="C"
                ),
                make_cloze(
                    sentence="Ders notuna göre RCOG 2011 kılavuzunda tekrarlayan gebelik kaybı ardışık üç veya daha fazla gebelik kaybı olarak tanımlanmıştır.",
                    masked_term="ardışık üç",
                    hint="İngiliz kılavuzunda birbirini peşi sıra izleme zorunluluğu olan sayı"
                ),
                make_table(
                    title="Uluslararası Kılavuzların Tekrarlayan Gebelik Kaybı (TGK) Tanımları",
                    headers=["Kılavuz / Dernek", "Resmi Tanım Kriteri", "Dışlama Kriterleri"],
                    rows=[
                        [
                            {"text": "ASRM (2012, 2013)", "isMasked": False},
                            {"text": "2 veya daha fazla klinik gebelik kaybı", "isMasked": True, "hint": "Gözlemsel USG ve histopatoloji ile belgelenen sayı"},
                            {"text": "Biyokimyasal gebelikler tanıya dahil edilmez", "isMasked": False}
                        ],
                        [
                            {"text": "ESHRE (2019)", "isMasked": False},
                            {"text": "Viabilite sınırı (24 hf) öncesi gebelik kaybı", "isMasked": True, "hint": "Fetal yaşayabilme eşiğine kadar olan sonlanmalar"},
                            {"text": "Ektopik, GTN ve implantasyon başarısızlığı hariç", "isMasked": False}
                        ],
                        [
                            {"text": "RCOG (2011)", "isMasked": False},
                            {"text": "Ardışık 3 veya daha fazla gebelik kaybı", "isMasked": True, "hint": "Aralıksız birbirini izleyen asgari sayı"},
                            {"text": "Arada canlı doğum olmaması şartı", "isMasked": False}
                        ]
                    ]
                ),
                make_recall(
                    question="ASRM ile RCOG arasındaki tekrarlayan gebelik kaybı tanım farkı nedir?",
                    answer="ASRM 2 veya daha fazla klinik gebelik kaybını yeterli görürken, RCOG ardışık en az 3 gebelik kaybı şartı aramaktadır."
                )
            ]
        ),

        # Slide 92
        make_slide(
            slide_num=92,
            title="Tekrarlayan Gebelik Kaybında Kabul Edilen Temel Etiyolojiler",
            subtitle="Kanıta Dayalı 5 Majör Neden ve Patofizyolojik Mekanizmaları",
            clinical_focus="Ders notunda RPL için bilimsel olarak kesin 'kabul edilen etiyolojiler' açıkça listelenmiştir.",
            narrative="""Tekrarlayan gebelik kayıplarında etiyolojik faktörler kanıt düzeyine göre sınıflandırılır. Ders notunda tekrarlayan gebelik kaybı için bilimsel olarak 'kabul edilen etiyolojiler' 5 ana başlıkta toplanmıştır.

- **Parental Kromozomal Anormallikler:** Anne veya babadaki dengeli translokasyonlar (en sık resiprokal veya Robertsonian) mayozda dengesiz gamet oluşumuna ve tekrarlayan fetal trizomi/monozomilere yol açar (%3-5).
- **Tedavi Edilmemiş Hipotiroidizm:** Tiroid hormon yetersizliği trofoblast farklılaşmasını ve erken plasentasyonu bozar.
- **Kontrolsüz Diabetes Mellitus:** Yüksek maternal HbA1c ve hiperglisemi organogenez döneminde embriyotoksik ve teratojenik etki yapar.
- **Uterin Anatomik Anormallikler:** Özellikle uterin septum (en yüksek düşük riski) ve geniş intrauterin sineşiler (Asherman sendromu) yetersiz kanlanma nedeniyle kayba neden olur.
- **Antifosfolipid Antikor Sendromu (APS):** Edinsel otoimmün trombofili olup uteroplasental damarlarda tromboz ve trofoblast hasarı oluşturur.

> [!IMPORTANT]
> Ders notunda kabul edilen 5 temel neden: Parental kromozom anomalileri, tedavi edilmemiş hipotiroidizm, kontrolsüz DM, uterin anatomik anomaliler ve Antifosfolipid Antikor Sendromudur (APS).""",
            bullets=[
                "Parental kromozomal anormallikler (dengeli resiprokal/Robertsonian translokasyonlar)",
                "Tedavi edilmemiş hipotiroidizm ve kontrolsüz diabetes mellitus",
                "Uterin anatomik anormallikler (özellikle uterin septum)",
                "Antifosfolipid antikor sendromu (APS)"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre Tekrarlayan Gebelik Kaybı (RPL) için bilimsel olarak 'kabul edilen etiyolojiler' arasında aşağıdakilerden hangisi yer ALMAZ?",
                    options=[
                        {"key": "A", "text": "Parental kromozomal anormallikler", "isCorrect": False, "explanation": "Kabul edilen temel etiyolojidir (resiprokal/Robertsonian translokasyon)."},
                        {"key": "B", "text": "Tedavi edilmemiş hipotiroidizm ve kontrolsüz diabetes mellitus", "isCorrect": False, "explanation": "Kabul edilen endokrin etiyolojilerdir."},
                        {"key": "C", "text": "Antifosfolipid antikor sendromu (APS)", "isCorrect": False, "explanation": "Kabul edilen en önemli edinsel otoimmün trombofilik nedendir."},
                        {"key": "D", "text": "Basit asemptomatik vajinal kandidiyazis enfeksiyonu", "isCorrect": True, "explanation": "Doğru (Tuzak!). Basit Candida enfeksiyonu TGK için kabul edilen bir etiyoloji değildir."}
                    ],
                    correct_key="D"
                ),
                make_cloze(
                    sentence="Ders notuna göre tekrarlayan gebelik kaybında kabul edilen edinsel otoimmün etiyoloji antifosfolipid antikor sendromu olarak tanımlanmaktadır.",
                    masked_term="antifosfolipid antikor sendromu",
                    hint="Lupus reaktifi ve kardiyolipin immünglobulinleriyle seyreden edinsel tablo"
                ),
                make_spot_the_lie(
                    topic="Tekrarlayan gebelik kaybında kabul edilen etiyolojik faktörler",
                    items=[
                        {"text": "Parental dengeli translokasyonlar tekrarlayan kayıplarda kabul edilen genetik nedendir.", "isLie": False, "explanation": "Kanıtlanmış temel etiyolojidir."},
                        {"text": "Tedavi edilmemiş hipotiroidizm ve kontrolsüz diyabet kabul edilen metabolik nedenlerdir.", "isLie": False, "explanation": "Ders notunda açıkça belirtilmiştir."},
                        {"text": "Uterin septum gibi anatomik malformasyonlar ve APS kabul edilen etiyolojiler arasındadır.", "isLie": False, "explanation": "Kanıta dayalı temel nedenlerdir."},
                        {"text": "Hafif fiziksel yorgunluk ve normal günlük yürüyüşler kabul edilen TGK etiyolojisidir.", "isLie": True, "explanation": "Tuzak! Günlük normal fiziksel aktivite veya yorgunluk abortus nedeni değildir."}
                    ]
                ),
                make_recall(
                    question="Ders notuna göre tekrarlayan gebelik kaybında kesin olarak 'kabul edilen' 5 etiyolojiyi sayınız.",
                    answer="1) Parental kromozomal anormallikler, 2) Tedavi edilmemiş hipotiroidizm, 3) Kontrolsüz diabetes mellitus, 4) Belirli uterin anatomik anormallikler (septum vb.), 5) Antifosfolipid antikor sendromu (APS)."
                )
            ]
        ),

        # Slide 93
        make_slide(
            slide_num=93,
            title="Diğer Olası Etiyolojiler ve Açıklanamayan TGK Olguları",
            subtitle="Trombofililer, İmmünoloji, Çevresel Faktörler ve %33'ten Fazla İdiopatik Grup",
            clinical_focus="Kapsamlı tetkiklere rağmen TGK olgularının üçte birinden fazlasında etiyoloji saptanamaz.",
            narrative="""Tekrarlayan gebelik kayıplarında kesin kabul edilen 5 majör nedenin yanı sıra, araştırmaların devam ettiği diğer olası etiyolojiler de bulunmaktadır. Ancak ders notunun en can alıcı vurgularından biri açıklanamayan vakalardır.

- **Diğer Olası Etiyolojiler:** Ders notunda endokrin bozukluklar (luteal faz yetmezliği, hiperprolaktinemi, PKOS), kalıtsal ve/veya edinilmiş trombofililer, immünolojik anormallikler ve çevresel nedenler belirtilmiştir.
- **Açıklanamayan TGK Oranı:** Ders notunda net bir dille vurgulanmıştır: **'Bu nedenler için değerlendirme yapıldıktan sonra tüm vakaların %33'ünden fazlası açıklanamayan TGK olarak kalır.'**
- **Klinik ve Psikolojik Yönetim:** Nedeni bulunamayan bu hasta grubunda ampirik ağır tedavilerden kaçınılmalı, yakın ultrasonik takip, destekleyici bakım ve güven verici yaklaşım ('tender loving care') uygulanmalıdır; zira bu çiftlerin bir sonraki gebelikte canlı doğum şansı %60-70 civarındadır.

> [!NOTE]
> Tekrarlayan gebelik kaybı olan çiftlerin kapsamlı incelemesine rağmen %33'ünden fazlasında hiçbir patoloji saptanamaz (Açıklanamayan TGK).""",
            bullets=[
                "Diğer olası etiyolojiler: Endokrin bozukluklar, kalıtsal trombofililer, immünolojik ve çevresel nedenler",
                "Tüm değerlendirmeler sonrasında vakaların %33'ünden fazlası açıklanamayan (idiopatik) kalır",
                "Açıklanamayan olgularda yakın izlem ve destekle sonraki gebelikte başarı şansı %60-70'tir"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre tüm etiyolojik değerlendirmeler tamamlandıktan sonra tekrarlayan gebelik kaybı vakalarının yüzde kaçından fazlası 'açıklanamayan TGK' olarak kalır?",
                    options=[
                        {"key": "A", "text": "Yalnızca %5'inden fazlası", "isCorrect": False, "explanation": "Çok düşüktür."},
                        {"key": "B", "text": "%33'ünden fazlası", "isCorrect": True, "explanation": "Doğru. Ders notu Bölüm 10'da 'tüm vakaların %33'ünden fazlası açıklanamayan TGK olarak kalır' ifadesi birebir yer almaktadır."},
                        {"key": "C", "text": "Tam olarak %99'u", "isCorrect": False, "explanation": "Aşırı abartılıdır."},
                        {"key": "D", "text": "Yalnızca %1-2'si", "isCorrect": False, "explanation": "Sepsis oranı ile karıştırılmamalıdır."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Ders notuna göre tüm etiyolojik faktörler incelendikten sonra tekrarlayan düşük vakalarının yüzde otuz üçünden fazlası açıklanamayan TGK olarak kalmaktadır.",
                    masked_term="yüzde otuz üçünden",
                    hint="Ders notunda belirtilen idiopatik tekrarlayan düşük oranı eşiği"
                ),
                make_table(
                    title="Tekrarlayan Gebelik Kayıplarında Etiyolojik Sınıflandırma ve Açıklanamayan Grup",
                    headers=["Etiyoloji Kategorisi", "Ders Notundaki Karşılığı", "Görülme ve Kanıt Durumu"],
                    rows=[
                        [
                            {"text": "Kesin Kabul Edilen Nedenler", "isMasked": False},
                            {"text": "Parental kromozom, hipotiroidi, DM, uterin, APS", "isMasked": True, "hint": "Ders notunda kanıtlanmış 5 majör faktör"},
                            {"text": "Spesifik tedavi ve düzeltme gerektirir", "isMasked": False}
                        ],
                        [
                            {"text": "Diğer Olası Faktörler", "isMasked": False},
                            {"text": "Endokrin, kalıtsal trombofililer, immünolojik, çevresel", "isMasked": True, "hint": "Araştırılan diğer ikincil nedenler"},
                            {"text": "Tartışmalı ve bireysel değerlendirilen faktörler", "isMasked": False}
                        ],
                        [
                            {"text": "Açıklanamayan (İdiopatik) TGK", "isMasked": False},
                            {"text": "Vakaların %33'ünden fazlası", "isMasked": True, "hint": "Ders notundaki resmi meçhul vaka oranı"},
                            {"text": "Destekleyici bakım ve yakın takip uygulanır", "isMasked": False}
                        ]
                    ]
                ),
                make_recall(
                    question="Tekrarlayan gebelik kaybı değerlendirmesi tamamlanan çiftlerde 'açıklanamayan TGK' oranı nedir ve bu çiftlerin canlı doğum prognozu nasıldır?",
                    answer="Ders notuna göre vakaların %33'ünden fazlası açıklanamayan grupta kalır. Buna rağmen bu çiftlerin sonraki gebelikte destekleyici takiple canlı doğum yapma şansı yaklaşık %60-70 gibi oldukça yüksektir."
                )
            ]
        ),

        # Slide 94
        make_slide(
            slide_num=94,
            title="Genetik Değerlendirme: Maternal ve Paternal Karyotip Analizi",
            subtitle="Dengeli Translokasyonlar, İnversiyonlar ve Genetik Danışmanlık",
            clinical_focus="Tekrarlayan kayıplarda ebeveyn karyotipi dengeli translokasyon taşıyıcılığını saptar.",
            narrative="""Tekrarlayan gebelik kayıplarında ders notundaki önerilen testler tablosunun ilk satırı **Genetik: Karyotip, maternal/paternal** analizidir.

- **Klinik Endikasyon:** Tekrarlayan gebelik kaybı yaşayan çiftlerin %3-5'inde ebeveynlerden birinde dengeli yapısal kromozom anomalisi (resiprokal translokasyon veya Robertsonian translokasyon) bulunur.
- **Taşıyıcı Ebeveyn Kliniği:** Ebeveyn fenotipik olarak tamamen sağlıklıdır çünkü genetik materyal kaybı yoktur (dengelidir).
- **Mayozda Dengesizlik:** Mayotik bölünme sırasında kromozomlar ayrılırken delesyonlu veya duplikasyonlu dengesiz gametler oluşur. Döllenme sonucu oluşan fetüs letal trizomi veya monozomi taşıyarak tekrarlayan düşüklere yol açar.
- **Klinik Yönetim:** Ebeveynlerde translokasyon saptandığında genetik danışmanlık verilir; preimplantasyon genetik tanı (PGT) veya prenatal invaziv tanı seçenekleri sunulur.

> [!IMPORTANT]
> Genetik incelemede sadece anneye değil, **her iki ebeveyne birden (maternal ve paternal)** periferik kandan karyotip analizi yapılmalıdır.""",
            bullets=[
                "Ders notunda genetik kategorisinde önerilen test: Karyotip (maternal ve paternal)",
                "Çiftlerin %3-5'inde dengeli translokasyon veya kromozomal inversiyon saptanır",
                "Ebeveyn fenotipik olarak normaldir ancak dengesiz gametler letal anöploidi ve düşüğe yol açar"
            ],
            elements=[
                make_quiz(
                    question="Ders notunda tekrarlayan gebelik kayıplarında önerilen testler tablosunda 'Genetik' kategorisinde yapılması önerilen temel inceleme aşağıdakilerden hangisidir?",
                    options=[
                        {"key": "A", "text": "Karyotip, maternal/paternal", "isCorrect": True, "explanation": "Doğru. Ders notu Tablo 'Genetik: Karyotip, maternal/paternal' olarak açıkça belirtilmiştir."},
                        {"key": "B", "text": "Yalnızca amniyosentez ve fetal kordosentez", "isCorrect": False, "explanation": "Gebelik sırasında yapılan invaziv testlerdir, TGK ön değerlendirme testi değildir."},
                        {"key": "C", "text": "Anne sütünde kromozom taraması", "isCorrect": False, "explanation": "Tıbbi gerçek dışıdır."},
                        {"key": "D", "text": "Yalnızca babada Y delesyon testi", "isCorrect": False, "explanation": "Y delesyonu azoospermi testidir, TGK ilk basamak genetik testi değildir."}
                    ],
                    correct_key="A"
                ),
                make_cloze(
                    sentence="Ders notundaki tekrarlayan düşük test tablosuna göre genetik kategoride hem anneye hem babaya karyotip analizi yapılması önerilmektedir.",
                    masked_term="karyotip analizi",
                    hint="Periferik lenfosit kültüründen kromozom haritalama testi"
                ),
                make_chain(
                    title="Ebeveyn Dengeli Translokasyonundan Abortusa Giden Genetik Süreç",
                    steps=[
                        "1. Ebeveyn Taşıyıcılığı: Anne veya babanın dengeli resiprokal translokasyon taşıması",
                        "2. Mayozda Eşleşme: Gametogenezde translokasyon kromozomlarının tetravalent oluşturması",
                        "3. Segregasyon Hatası: Gametlere eksik veya fazla kromozomal parça aktarılması",
                        "4. Dengesiz Zigot: Fertilizasyonla embriyoda letal parsiyel trizomi/monozomi oluşması",
                        "5. Erken Gelişimsel Duraklama: Genetik anöploidi sonucu embriyonun kaybedilmesi (abortus)"
                    ]
                ),
                make_recall(
                    question="Tekrarlayan gebelik kaybı yaşayan bir çiftte genetik incelemenin sadece anneye değil her iki eşe de yapılmasının gerekçesi nedir?",
                    answer="Çünkü dengeli translokasyon veya inversiyon gibi yapısal kromozom anomalileri anne kaynaklı olabileceği gibi baba kaynaklı da olabilir; her iki ebeveyn de fenotipik olarak sağlıklıdır."
                )
            ]
        ),

        # Slide 95
        make_slide(
            slide_num=95,
            title="Anatomik Değerlendirme: Uterin Boşluğun İncelenmesi",
            subtitle="HSG, Sonohisterogram, Histeroskopi ve İleri Görüntülemede MR",
            clinical_focus="Ders notunda anatomik incelemede HSG, sonohisterogram ve histeroskopinin yeri tanımlanmıştır.",
            narrative="""Tekrarlayan gebelik kaybı olan kadınlarda uterin kavite anomalileri implantasyon yetersizliğine veya plasental perfüzyon bozukluğuna yol açabilir. Ders notundaki anatomik testler net bir protokole bağlanmıştır.

- **Önerilen Temel Testler:** Ders notunda açıkça belirtilmiştir: **'Anatomik: HSG veya sonohisterogram veya histeroskopi'**.
  - **Histerosalpingografi (HSG):** Kavite içi dolum defektlerini ve fallop tüplerinin açıklığını gösterir.
  - **Sonohisterografi (SIS / Salin İnfüzyon Sonografi):** Uterus içine steril salin verilerek yapılan transvajinal ultrasondur; endometrial polip, submüköz miyom ve septumu mükemmel ayırır.
  - **Histeroskopi:** Kaviteyi doğrudan optik kamera ile görüntüleyen altın standart tanı ve anında tedavi (rezeksiyon) yöntemidir.
- **Diğer İleri Testler:** Ders notunda belirtildiği gibi şüpheli veya karmaşık Müllerian anomalilerde (örneğin bikornus ile septum ayırıcı tanısında) **'Belirtildiği gibi MR'** (Manyetik Rezonans Görüntüleme) kullanılır.

> [!NOTE]
> Anatomik değerlendirmede HSG, sonohisterogram veya histeroskopi önerilir; ayırıcı tanıda gerektiğinde pelvik MR kullanılır.""",
            bullets=[
                "Önerilen testler: Histerosalpingografi (HSG), sonohisterogram veya histeroskopi",
                "Diğer ileri inceleme: Belirtildiği gibi Manyetik Rezonans Görüntüleme (MR)",
                "Uterin septum cerrahi olarak histeroskopik metroplasti ile en başarılı düzeltilen anomalidir"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre tekrarlayan gebelik kaybında anatomik faktörlerin değerlendirilmesinde önerilen testler ve gerektiğinde başvurulan ileri görüntüleme yöntemi hangi seçenekte doğru verilmiştir?",
                    options=[
                        {"key": "A", "text": "Yalnızca direkt karın grafisi ve sintigrafi", "isCorrect": False, "explanation": "Uterin kaviteyi göstermez ve radyasyon içerir."},
                        {"key": "B", "text": "HSG veya sonohisterogram veya histeroskopi; belirtildiği gibi MR", "isCorrect": True, "explanation": "Doğru. Ders notu Tablo 'Anatomik: HSG veya sonohisterogram veya histeroskopi / Diğer testler: Belirtildiği gibi MR' ifadesinin birebir karşılığıdır."},
                        {"key": "C", "text": "Yalnızca pozitron emisyon tomografisi (PET-BT)", "isCorrect": False, "explanation": "Onkolojik yöntemdir, kaviter anatomi değerlendirmesinde yeri yoktur."},
                        {"key": "D", "text": "Yalnızca tanısal laparoskopi", "isCorrect": False, "explanation": "İntrauterin kavite içini doğrudan göstermez."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Ders notunda tekrarlayan düşüklerde anatomik değerlendirme için HSG veya sonohisterogram veya histeroskopi önerilirken diğer testler arasında gerektiğinde MR yer almaktadır.",
                    masked_term="histeroskopi",
                    hint="Uterin kaviteyi optik kamera sistemiyle doğrudan gözleme yöntemi"
                ),
                make_slider(
                    left_title="Uterin Septum",
                    right_title="Uterus Bikornis",
                    left_points=[
                        "Kavitede avasküler fibröz bant uzanır",
                        "Dış fundal kontur tamamen düz ve normaldir",
                        "Tedavisi histeroskopi ile septoplastidir (kesilme)"
                    ],
                    right_points=[
                        "İki ayrı uterin boynuz mevcuttur",
                        "Dış fundal konturda >1 cm derin çentik izlenir",
                        "Histeroskopi ile rezeke edilemez, cerrahi nadirdir"
                    ]
                ),
                make_recall(
                    question="Ders notuna göre tekrarlayan gebelik kayıplarında anatomik değerlendirme için önerilen testler ve endike olduğunda başvurulan diğer görüntüleme yöntemi nedir?",
                    answer="Önerilen testler: HSG veya sonohisterogram veya histeroskopidir. Gerektiğinde başvurulan diğer ileri test ise Manyetik Rezonans Görüntülemedir (MR)."
                )
            ]
        ),

        # Slide 96
        make_slide(
            slide_num=96,
            title="İmmünolojik Değerlendirme: Antifosfolipid Antikor Sendromu (APS)",
            subtitle="Lupus Antikoagülan, Antikardiyolipin Antikorları ve Kriterler",
            clinical_focus="Antifosfolipid antikor sendromu tekrarlayan kayıplarda en sık saptanan edinsel otoimmün trombofilidir.",
            narrative="""Antifosfolipid Antikor Sendromu (APS), tekrarlayan gebelik kaybında kabul edilen en önemli otoimmün ve edinsel trombofilik nedendir. Ders notundaki test tablosunda immünolojik başlık altında yer alır.

- **Önerilen İmmünolojik Testler:** Ders notunda net olarak tanımlanmıştır: **'İmmünolojik: Lupus antikoagülan, antikardiyolipin antikor'**.
- **Laboratuvar Doğrulama Kuralı:** Antifosfolipid antikorlarının (Lupus antikoagülan, antikardiyolipin IgG/IgM ve anti-beta2 glikoprotein-I) pozitifliği, geçici enfeksiyöz pozitiflikleri dışlamak için **en az 12 hafta arayla yapılan iki ayrı ölçümde** gösterilmelidir.
- **Patolojik Mekanizma:** Antikorlar plasental sinsityotrofoblast yüzeyindeki fosfolipidlere ve adneksin V koruyucu kalkanına bağlanır; desidual vaskülit, trofoblastik apopitoz ve spiral arter trombozuna yol açarak gebelik kaybını tetikler.
- **Klinik Tedavi:** APS tanısı alan TGK olgularında standart tedavi düşük doz aspirin (75-100 mg/gün) ile profilaktik düşük molekül ağırlıklı heparin (LMWH) kombinasyonudur.

> [!IMPORTANT]
> İmmünolojik değerlendirmede bakılan temel testler: **Lupus antikoagülan** ve **antikardiyolipin antikorlardır**.""",
            bullets=[
                "Ders notunda immünolojik panel: Lupus antikoagülan ve antikardiyolipin antikor",
                "Tekrarlayan kayıplarda kabul edilen en temel otoimmün edinsel trombofili tablosudur",
                "Spesifik tedavisi düşük doz aspirin ve düşük molekül ağırlıklı heparindir (LMWH)"
            ],
            elements=[
                make_quiz(
                    question="Ders notunda tekrarlayan gebelik kayıplarında önerilen testler tablosunda 'İmmünolojik' kategori altında bakılması önerilen testler hangi seçenekte doğru verilmiştir?",
                    options=[
                        {"key": "A", "text": "Romatoid faktör ve anti-CCP", "isCorrect": False, "explanation": "Romatoid artrit testleridir, TGK immünolojik panelinde yer almaz."},
                        {"key": "B", "text": "Anti-HBs ve Anti-HCV", "isCorrect": False, "explanation": "Viral hepatit serolojisidir."},
                        {"key": "C", "text": "Lupus antikoagülan, antikardiyolipin antikor", "isCorrect": True, "explanation": "Doğru. Ders notu Tablo 'İmmünolojik: Lupus antikoagülan, antikardiyolipin antikor' olarak belirtilmiştir."},
                        {"key": "D", "text": "Anti-nükleer antikor (ANA) ve kompleman C3/C4", "isCorrect": False, "explanation": "Rutin ilk basamak immünolojik test tablosunda adı geçmez."}
                    ],
                    correct_key="C"
                ),
                make_cloze(
                    sentence="Ders notuna göre tekrarlayan gebelik kaybında immünolojik testler arasında lupus antikoagülan ve antikardiyolipin antikor yer alır.",
                    masked_term="lupus antikoagülan",
                    hint="Fosfolipid bağımlı pıhtılaşma testlerini in vitro uzatan patolojik immünoglobülin faktörü"
                ),
                make_chain(
                    title="Antifosfolipid Antikor Sendromunda Gebelik Kaybı Mekanizması",
                    steps=[
                        "1. Otoantikor Varlığı: Dolaşımda Lupus antikoagülan ve antikardiyolipin antikorlarının bulunması",
                        "2. Trofoblasta Bağlanma: Antikorların sinsityotrofoblast membranındaki fosfolipid komplekslerine yapışması",
                        "3. Trombofil ve Hasar: Trofoblastik invazyonun bozulması ve adneksin V kalkanının dağılması",
                        "4. Uteroplasental Tromboz: Spiral arterlerde mikroangiopati ve mikrotrombüslerin oluşması",
                        "5. Plasental İskemi ve Kayıp: Trofoblastik nekroz sonucu gebeliğin kaybedilmesi"
                    ]
                ),
                make_recall(
                    question="Ders notuna göre tekrarlayan gebelik kaybı değerlendirmesinde immünolojik grupta bakılması önerilen iki temel test nedir?",
                    answer="Lupus antikoagülan ve antikardiyolipin antikorlarıdır (Antifosfolipid Antikor Sendromu paneli)."
                )
            ]
        ),

        # Slide 97
        make_slide(
            slide_num=97,
            title="Kalıtsal Trombofililer ve Koagülasyon Paneli",
            subtitle="Faktör V Leiden, Protrombin Gen Mutasyonu, Protein C, S ve Antitrombin III",
            clinical_focus="Ders notundaki geniş trombofili panelinde yer alan 8 temel biyobelirteç.",
            narrative="""Trombofililer gebelik sırasında fizyolojik olarak artan hiperkoagülabiliteyi daha da şiddetlendirerek plasental yatakta mikrovasküler trombozlara yol açabilir. Ders notundaki test tablosunda trombofili paneli son derece kapsamlı bir şekilde sıralanmıştır.

- **Ders Notundaki Resmi Trombofili Testleri:** Tabloda açıkça listelenen parametreler şunlardır:
  - **Faktör V Leiden mutasyonu** (en sık kalıtsal trombofili, APC direnci nedeni)
  - **Protrombin gen mutasyonu (G20210A)**
  - **Aktive protein C rezistansı (APCR)**
  - **Homosistein düzeyi**
  - **MTHFR (Metilentetrahidrofolat redüktaz) gen mutasyonu**
  - **Protein C aktivitesi**
  - **Protein S aktivitesi**
  - **Antitrombin III aktivitesi**
- **Klinik Tartışma:** Kalıtsal trombofililerin özellikle 2. ve 3. trimester geç fetal kayıplarındaki rolü ilk trimester erken kayıplarına göre çok daha güçlü kabul edilir.

> [!NOTE]
> Ders notundaki trombofili paneli: Faktör V Leiden, Protrombin mutasyonu, APCR, Homosistein, MTHFR, Protein C, Protein S ve Antitrombin III'ü içerir.""",
            bullets=[
                "Ders notundaki resmi trombofililer: Faktör V Leiden, protrombin gen mutasyonu, aktive protein C rezistansı",
                "Biyokimyasal kofaktörler ve inhibitörler: Homosistein, MTHFR, protein C, protein S, antitrombin III",
                "Özellikle plasental damar yatağında tromboz riskini artıran genetik ve biyokimyasal panellerdir"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre tekrarlayan gebelik kaybında 'Trombofililer' kategorisinde önerilen testler arasında aşağıdakilerden hangisi yer ALMAZ?",
                    options=[
                        {"key": "A", "text": "Faktör V Leiden ve protrombin gen mutasyonu", "isCorrect": False, "explanation": "Ders notundaki temel trombofili testleridir."},
                        {"key": "B", "text": "Protein C, protein S ve antitrombin III", "isCorrect": False, "explanation": "Ders notundaki doğal antikoagülan testleridir."},
                        {"key": "C", "text": "Homosistein, MTHFR ve aktive protein C rezistansı", "isCorrect": False, "explanation": "Ders notundaki trombofili panelinde yer almaktadır."},
                        {"key": "D", "text": "Faktör VIII eksikliği ve hemofili A gen analizi", "isCorrect": True, "explanation": "Doğru (Tuzak!). Hemofili kanama diyatezidir, trombofili (pıhtılaşma eğilimi) testi değildir ve listede yoktur."}
                    ],
                    correct_key="D"
                ),
                make_cloze(
                    sentence="Ders notunda trombofililer panelinde yer alan Faktör V Leiden mutasyonu aktive protein C rezistansı tablosuna yol açan en sık kalıtsal nedendir.",
                    masked_term="Faktör V Leiden",
                    hint="Kalıtsal venöz trombozda en sık rastlanan mutasyon"
                ),
                make_table(
                    title="Ders Notunda Yer Alan Trombofili Paneli ve Biyolojik İşlevleri",
                    headers=["Trombofili Parametresi", "Test Tipi / Sınıfı", "Ders Notu Belirtimi"],
                    rows=[
                        [
                            {"text": "Faktör V Leiden ve Protrombin", "isMasked": False},
                            {"text": "Kalıtsal genetik mutasyon analizleri", "isMasked": True, "hint": "DNA dizi varyasyon testleri"},
                            {"text": "Önerilen trombofili testlerindedir", "isMasked": False}
                        ],
                        [
                            {"text": "Protein C, Protein S, Antitrombin III", "isMasked": False},
                            {"text": "Doğal plazma antikoagülan aktivite testleri", "isMasked": True, "hint": "Fizyolojik pıhtılaşma frenleyicileri"},
                            {"text": "Önerilen trombofili testlerindedir", "isMasked": False}
                        ],
                        [
                            {"text": "Homosistein ve MTHFR", "isMasked": False},
                            {"text": "Metiyonin metabolizması belirteçleri", "isMasked": True, "hint": "Metilasyon döngüsü enzimleri"},
                            {"text": "Önerilen trombofili testlerindedir", "isMasked": False}
                        ]
                    ]
                ),
                make_recall(
                    question="Ders notunun 'Trombofililer' kategorisinde listelediği 8 testi sayınız.",
                    answer="1) Faktör V Leiden, 2) Protrombin gen mutasyonu, 3) Aktive protein C rezistansı, 4) Homosistein, 5) MTHFR, 6) Protein C, 7) Protein S, 8) Antitrombin III."
                )
            ]
        ),

        # Slide 98
        make_slide(
            slide_num=98,
            title="Endokrin, Enfeksiyöz ve Çevresel Değerlendirme Paneli",
            subtitle="TSH, Açlık Glukozu, HbA1c, Prolaktin, Gonore/Klamidya Kültürleri ve Anamnez",
            clinical_focus="Ders notundaki endokrin, enfeksiyöz ve çevresel önerilen testler tablosu.",
            narrative="""Tekrarlayan gebelik kaybı değerlendirmesinde sistemik endokrinopatiler, enfeksiyonlar ve çevresel maruziyetler de incelenmelidir. Ders notu bu başlıklar altında net testler belirtmiştir.

- **Endokrin Panel:** Ders notundaki resmi testler şunlardır: **'Endokrin: TSH, açlık glukozu, HbA1c, prolaktin'**.
  - **TSH:** Hipotiroidizm veya subklinik hipotiroidi tespiti için zorunludur (gebelikte TSH <2.5 mIU/L hedeflenir).
  - **Açlık Glukozu ve HbA1c:** Kontrolsüz diyabet ve insülin direncinin belirlenmesi için istenir.
  - **Prolaktin:** Hiperprolaktinemi luteal faz yetmezliği ve ovulatuar disfonksiyona neden olabilir.
- **Enfeksiyöz Panel:** Ders notunda önerilen temel testler: **'Gonorrhea ve Chlamydia kültürleri'**dir. Diğer testler sütununda ise **'Endike ise Listeria ve TORCH'** yer alır.
- **Çevresel Kategori:** Önerilen tek yöntem **'Öykü'**dür (sigara, alkol, aşırı kafein, mesleki toksinler ve radyasyon sorgulaması).

> [!IMPORTANT]
> Ders notunda: Endokrinde TSH, açlık glukozu, HbA1c, prolaktin; Enfeksiyözde Gonorrhea ve Chlamydia kültürleri (endike ise Listeria ve TORCH); Çevreselde Öykü önerilir.""",
            bullets=[
                "Endokrin: TSH, açlık glukozu, HbA1c ve prolaktin",
                "Enfeksiyöz: Gonorrhea ve Chlamydia kültürleri; endike ise Listeria ve TORCH",
                "Çevresel: Ayrıntılı klinik anamnez ve öykü"
            ],
            elements=[
                make_quiz(
                    question="Ders notuna göre tekrarlayan gebelik kaybında 'Endokrin' ve 'Enfeksiyöz' kategorilerde önerilen testler hangi seçenekte doğru eşleştirilmiştir?",
                    options=[
                        {"key": "A", "text": "Endokrin: B-hCG ve AFP; Enfeksiyöz: Yalnızca influenza sürüntüsü", "isCorrect": False, "explanation": "Yanlış test gruplarıdır."},
                        {"key": "B", "text": "Endokrin: TSH, açlık glukozu, HbA1c, prolaktin; Enfeksiyöz: Gonorrhea ve Chlamydia kültürleri", "isCorrect": True, "explanation": "Doğru. Ders notundaki resmi test tablosunun birebir karşılığıdır."},
                        {"key": "C", "text": "Endokrin: Yalnızca büyüme hormonu; Enfeksiyöz: HIV viral yükü", "isCorrect": False, "explanation": "Rutin TGK panelinde yer almaz."},
                        {"key": "D", "text": "Endokrin: Gastrin ve VIP; Enfeksiyöz: Yalnızca tüberküloz kültürü", "isCorrect": False, "explanation": "Alakasız gastroenterolojik ve infektif testlerdir."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Ders notunda tekrarlayan düşüklerde enfeksiyöz panelde önerilen testler Gonorrhea ve Chlamydia kültürleri olup endike ise Listeria ve TORCH bakılır.",
                    masked_term="Chlamydia kültürleri",
                    hint="Servikal yaymada araştırılan cinsel yolla bulaşan obligat hücre içi bakteri testi"
                ),
                make_venn(
                    title="Ders Notu Test Tablosunda Rutin Önerilen ve Endike İse İstenen Testler",
                    label_a="Rutin Önerilen Testler",
                    label_b="Endike İse / Diğer Testler",
                    items=[
                        {"criterion": "Karyotip (maternal/paternal) ve TSH analizi", "correct": "A", "explanation": "Ders notunda ilk sütunda 'Önerilen testler' arasındadır."},
                        {"criterion": "Gonorrhea ve Chlamydia kültürleri", "correct": "A", "explanation": "Ders notunda enfeksiyöz başlığında doğrudan önerilen testtir."},
                        {"criterion": "Anatomik şüphede pelvik MR çekimi", "correct": "B", "explanation": "Ders notunda 'Diğer testler: Belirtildiği gibi MR' olarak geçer."},
                        {"criterion": "Listeria ve TORCH serolojisi", "correct": "B", "explanation": "Ders notunda 'Diğer testler: Endike ise Listeria ve TORCH' olarak geçer."},
                        {"criterion": "Tekrarlayan gebelik kaybı etiyolojisini aydınlatma amacı", "correct": "both", "explanation": "Tüm testler TGK nedenini ortaya koymak için kullanılır."},
                        {"criterion": "Sadece 40. gebelik haftasında doğum sancısı başladığında istenme", "correct": "neither", "explanation": "Testler konsepsiyon öncesi veya erken kayıp sonrası değerlendirmedir."}
                    ]
                ),
                make_recall(
                    question="Ders notuna göre tekrarlayan gebelik kaybında enfeksiyöz kategoride 'önerilen testler' ile 'diğer testler' nelerdir?",
                    answer="Önerilen testler: Gonorrhea ve Chlamydia kültürleridir. Diğer testler (endike ise istenenler): Listeria ve TORCH paneli olarak belirtilmiştir."
                )
            ]
        ),

        # Slide 99
        make_slide(
            slide_num=99,
            title="Ders Notundaki Tüm Testlerin Büyük Sentezi ve Algoritması",
            subtitle="Tekrarlayan Düşükte Kapsamlı Klinik Yaklaşım Haritası",
            clinical_focus="7 kategorideki tüm testlerin sistematik olarak değerlendirilmesi ve hasta yönetimi.",
            narrative="""Tekrarlayan gebelik kaybı yaşayan bir çift başvurduğunda ders notundaki 7 kategorik test paneli adım adım devreye sokulur. Bu sistematik analiz hem etiyolojiyi bulmayı hem de gereksiz tedavileri önlemeyi sağlar.

- **1. Genetik:** Maternal ve paternal periferik karyotip (dengeli translokasyonlar için).
- **2. Anatomik:** HSG, SIS veya histeroskopi (septum, sineşi, polip/miyom); karmaşık vakalarda MR.
- **3. İmmünolojik:** Lupus antikoagülan ve antikardiyolipin antikorları (APS tanısı için).
- **4. Trombofililer:** Faktör V Leiden, Protrombin, APCR, Homosistein, MTHFR, Protein C/S, Antitrombin III.
- **5. Endokrin:** TSH, açlık glukozu, HbA1c, prolaktin (tiroid ve diyabet kontrolü).
- **6. Enfeksiyöz:** Gonore ve Klamidya kültürleri (endike ise Listeria ve TORCH).
- **7. Çevresel:** Sigara, alkol, kafein ve toksin sorgulaması için ayrıntılı öykü.

> [!NOTE]
> Bu 7 basamaklı incelemenin sonucunda olguların %33'ünden fazlasında hiçbir sebep bulunamaz; bu çiftlere ampirik toksik ilaçlar yerine moral ve yakın takip verilir.""",
            bullets=[
                "7 temel kategori: Genetik, anatomik, immünolojik, trombofililer, endokrin, enfeksiyöz, çevresel",
                "Kapsamlı tetkik paneli spesifik ve kanıta dayalı tedaviyi yönlendirir",
                "Açıklanamayan vakalarda ampirik aşırı tedaviden kaçınılır, yakın takip sunulur"
            ],
            elements=[
                make_quiz(
                    question="Tekrarlayan gebelik kaybı yaşayan bir kadında yapılan tetkiklerde TSH 7.2 mIU/L (yüksek) ve HbA1c %9.4 (çok yüksek) saptanıyor; diğer tüm testler normaldir. Bu hastada ders notuna göre öncelikli klinik yaklaşım ne olmalıdır?",
                    options=[
                        {"key": "A", "text": "Hemen acil histeroskopik uterin septum rezeksiyonu yapılmalıdır", "isCorrect": False, "explanation": "Anatomi normaldir, gereksiz cerrahidir."},
                        {"key": "B", "text": "Öncelikle hipotiroidizm ve diabetes mellitus medikal olarak kontrol altına alınmalı, ötiroidi ve glisemik kontrol sağlandıktan sonra yeni gebeliğe izin verilmelidir", "isCorrect": True, "explanation": "Doğru. Kabul edilen iki majör metabolik neden tedavi edilmemiş hipotiroidi ve kontrolsüz diyabettir."},
                        {"key": "C", "text": "Hiçbir tedavi verilmeden hasta hemen tüp bebek programına yönlendirilmelidir", "isCorrect": False, "explanation": "Kontrolsüz diyabet ve hipotiroidide tüp bebek de başarısız olur."},
                        {"key": "D", "text": "Sadece yüksek doz kemoterapi başlanmalıdır", "isCorrect": False, "explanation": "Tıbbi hata ve malpraktistir."}
                    ],
                    correct_key="B"
                ),
                make_cloze(
                    sentence="Ders notunda tekrarlayan gebelik kaybında çevresel etiyolojilerin tespiti için önerilen yöntem öykü sorgulamasıdır.",
                    masked_term="öykü",
                    hint="Klinisyenin anamnez yoluyla yaşam tarzı ve maruziyetleri sorgulaması"
                ),
                make_swipe(
                    title="Tekrarlayan Gebelik Kaybı Test Kategorisi Eşleme Kartları",
                    left_category="Genetik ve İmmünolojik Panel",
                    right_category="Endokrin ve Enfeksiyöz Panel",
                    cards=[
                        {"text": "Maternal ve paternal periferik karyotip analizi", "category": "left", "explanation": "Genetik test kategorisinde yer alır."},
                        {"text": "Lupus antikoagülan ve antikardiyolipin antikorları", "category": "left", "explanation": "İmmünolojik test kategorisinde yer alır."},
                        {"text": "Serum TSH, açlık plazma glukozu ve HbA1c", "category": "right", "explanation": "Endokrin test kategorisinde yer alır."},
                        {"text": "Serum prolaktin düzeyi ölçümü", "category": "right", "explanation": "Endokrin test kategorisinde yer alır."},
                        {"text": "Gonorrhea ve Chlamydia servikal kültürleri", "category": "right", "explanation": "Enfeksiyöz test kategorisinde yer alır."},
                        {"text": "Endike ise Listeria ve TORCH serolojisi", "category": "right", "explanation": "Enfeksiyöz test kategorisinde yer alır."}
                    ]
                ),
                make_recall(
                    question="Ders notundaki tekrarlayan düşük değerlendirme tablosunda yer alan 7 ana kategoriyi sayınız.",
                    answer="1) Genetik, 2) Anatomik, 3) İmmünolojik, 4) Trombofililer, 5) Endokrin, 6) Enfeksiyöz, 7) Çevresel."
                )
            ]
        ),

        # Slide 100 (Final Checkpoint 10 & 20 Altın Kural)
        make_slide(
            slide_num=100,
            title="[TEKRAR SAYFASI - CHECKPOINT 10] Abortus Dersi 20 Altın Sınav Spotu ve Büyük Sentez",
            subtitle="Tüm Dersin Eksiksiz Özeti: Tanımlar, Genetik, Tipler, USG, Yönetim ve TGK",
            clinical_focus="Tıp fakültesi amfi ders notunun (TIP 310 · Dr. Öğr. Üyesi Hilal Ezgi Türkmen) 100 slaytlık tam sentezi.",
            narrative="""Tıp fakültesi Kurul 1 'TIP 310 · Abortus' dersinin 100 slaytlık öğrenim yolculuğunu ders notundaki tüm altın spot kurallarla tamamlıyoruz.

- **Tanım ve İnsidans:** Abortus <20 hafta, <500 gramdır. <12 hafta erken, 13-20 hafta geçtir. İnsidans %15-20 (klinik %10-12). %80 ilk trimesterdedir. Risk ilk 8 haftada en yüksektir.
- **Genetik Etiyoloji:** 1. trim %70, 2. trim %30 kromozomaldir. En sık normal karyotip; en sık anomali 45,X0; en sık trizomi trizomi 16'dır. Trizomi 1, 3, 19 HİÇ GÖRÜLMEZ.
- **Tipler:** İmminens (kanama +, serviks KAPALI, canlı embriyo, tedavi: progesteron/indometazin). İnsipiens (kanama fazla, şiddetli ağrı, serviks AÇIK, materyal atılmamış). İnkomplet (kısmi atılım, serviks AÇIK, kavitede bozulmuş doku). Komplet (tüm materyal atılmış, kavite boş, TEDAVİ GEREKMEZ). Missed (canlılık kaybı >1 hf, hCG düşüyor, CRL ≥7 mm FKA yok veya MSD ≥25 mm embriyo yok). Septik (%1-2 enfeksiyon/sepsis, 100 binde 0.58 ölüm, IV antibiyotik + rest varsa cerrahi).
- **İlk Trimester USG:** Kese TV-USG 4-5. hf, TA-USG 6. hf; günde 1 mm büyür; hCG >2000 mIU/ml kese mutlaka görülmeli. Yolk sac 5. hf, fetal pole 6. hf. CRL 7-14. hf: 6 hafta + CRL(mm) = 6 hafta + gün. SAT-USG farkı 1. trim 7 gün, 2. trim 10 gün önemsizdir.
- **Yönetim ve TGK:** Bekleme, medikal (Misoprostol - PGE1, Mifepriston - antiprogesteron), cerrahi (D&C, vakum aspirasyon). Rh(-) gebede Anti-D immün globulin zorunludur. TGK: ASRM ≥2 klinik, RCOG ardışık ≥3, ESHRE <24 hf (ektopik/GTN/implantasyon hariç). %33'ten fazlası AÇIKLANAMAYAN TGK'dır.

> [!IMPORTANT]
> Bu 20 altın kural Dr. Hilal Ezgi Türkmen'in ders notunun ve kadın doğum obstetrik komite sınavlarının eksiksiz omurgasını oluşturur!""",
            bullets=[
                "Tanım: <20 hafta, <500 gram; %80 ilk trimester; trizomi 1, 3, 19 hiç görülmez",
                "İmminens kapalı/canlı, insipiens açık/atılmamış, inkomplet açık/kısmi, komplet kapalı/boş/tedavisiz",
                "hCG >2000 ise kese görülmeli; CRL formülü: 6 hafta + CRL(mm) = 6 hafta + gün",
                "Medikal: Misoprostol (PGE1) + Mifepriston; Cerrahi: D&C ve vakum aspirasyon; Anti-D profilaksisi",
                "TGK: ASRM ≥2, RCOG ardışık ≥3; >%33 açıklanamayan idiopatik grup"
            ],
            elements=[
                make_quiz(
                    question="Tüm ders notunun büyük sentezi olarak: Abortus, erken gebelik kaybı ve tekrarlayan düşüklerle ilgili aşağıdaki klinik ifadelerden hangisi YANLIŞTIR (tuzaktır)?",
                    options=[
                        {"key": "A", "text": "Spontan düşük materyallerinde trizomi 1, 3 ve 19 kromozom anomalilerine kesinlikle rastlanmaz", "isCorrect": False, "explanation": "Doğrudur. Ders notunda 'Trizomi 1, 3 ve 19 abort materyallerinde hiç görülmez' kuralı yer alır."},
                        {"key": "B", "text": "Transvajinal ultrasonda hCG >2000 mIU/ml olduğu halde kavitede kese görülmüyorsa ektopik gebelik ekarte edilmelidir", "isCorrect": False, "explanation": "Doğrudur. Diskriminatif zon kuralıdır."},
                        {"key": "C", "text": "Komplet abortus tanısı kesinleşen ve kanaması duran bir hastada mutlaka acil keskin küretaj yapılmalıdır", "isCorrect": True, "explanation": "Yanlış (Tuzak!). Ders notunda komplet abortus için 'Tedavi gerekmez' açıkça yazılıdır, cerrahi yapılmaz."},
                        {"key": "D", "text": "Tekrarlayan gebelik kaybı değerlendirmesi tamamlandıktan sonra vakaların %33'ünden fazlası açıklanamayan grupta kalır", "isCorrect": False, "explanation": "Doğrudur. Ders notundaki resmi idiopatik orandır."}
                    ],
                    correct_key="C"
                ),
                make_cloze(
                    sentence="Ders notuna göre komplet abortusta tüm gebelik materyali atılmış olup ultrasonografide materyal gözlenmez ve tedavi gerekmez.",
                    masked_term="tedavi gerekmez",
                    hint="Komplet abortusun ders notundaki resmi klinik yönetim prensibi"
                ),
                make_table(
                    title="Büyük Final: Abortus Tipleri ve Ayırıcı Tanı Şah Mat Tablosu",
                    headers=["Abortus Tipi", "Servikal Açıklık", "Ultrason Bulgusu", "Ders Notu Tedavi Kuralı"],
                    rows=[
                        [
                            {"text": "Abortus İmminens", "isMasked": False},
                            {"text": "Kapalı (kanama +)", "isMasked": True, "hint": "Kanalın mekanik durumu"},
                            {"text": "Canlı intrauterin embriyo / FKA (+)", "isMasked": False},
                            {"text": "Medikal (progesteron, indometazin)", "isMasked": False}
                        ],
                        [
                            {"text": "Abortus İnsipiens", "isMasked": False},
                            {"text": "Açık (şiddetli ağrı)", "isMasked": True, "hint": "Genişlemiş servikal kanal"},
                            {"text": "Gebelik gözlenir, henüz atılmamış", "isMasked": False},
                            {"text": "Medikal / cerrahi terminasyon", "isMasked": False}
                        ],
                        [
                            {"text": "İnkomplet Abortus", "isMasked": False},
                            {"text": "Açık", "isMasked": False},
                            {"text": "Bozulmuş fetoplasental dokular", "isMasked": True, "hint": "Lümende kalan doku parçaları"},
                            {"text": "Uterus tahliyesi (vakum / D&C)", "isMasked": False}
                        ],
                        [
                            {"text": "Komplet Abortus", "isMasked": False},
                            {"text": "Kapalı olabilir", "isMasked": False},
                            {"text": "Kavite tamamen boş, materyal yok", "isMasked": True, "hint": "Endometrium lümeninde kalıntı izlenmemesi"},
                            {"text": "Tedavi gerekmez", "isMasked": False}
                        ]
                    ]
                ),
                make_branching(
                    scenario="Acil obstetrik polikliniğe başvuran 4 hastanın klinik senaryosu veriliyor. Hangi hastaya ders notu ilkelerine tam uyumlu doğru yönetim uygulanmıştır?",
                    options=[
                        {
                            "text": "6 haftalık vajinal kanaması olan, serviksi kapalı, USG'de FKA(+) canlı embriyo izlenen hastaya abortus imminens tanısıyla progesteron başlanıp istirahat önerilmesi ve Rh(-) ise Anti-D yapılması.",
                            "isCorrect": True,
                            "feedback": "Mükemmel klinik karar! Abortus imminens tanı ve tedavisinin ders notundaki tam karşılığıdır."
                        },
                        {
                            "text": "Komplet abortus geçirip ultrasonda kavitesi tamamen boş olan asemptomatik hastaya genel anestezi altında acil keskin küretaj uygulanması.",
                            "isCorrect": False,
                            "feedback": "Hatalı karar. Komplet abortusta tüm doku atılmıştır ve tedavi gerekmez."
                        },
                        {
                            "text": "Septik abortus tablosunda 39°C ateşi ve pürülan akıntısı olan hastaya hiçbir antibiyotik verilmeden sadece bekleme-takip önerilmesi.",
                            "isCorrect": False,
                            "feedback": "Ölümcül tıbbi hata! Septik abortusta acil IV antibiyotik ve cerrahi tahliye hayatidir."
                        }
                    ]
                ),
                make_recall(
                    question="Tüm 'Abortus' dersinin en kritik 3 altın kuralını tek bir cümlede özetleyiniz.",
                    answer="1) Abortus <20 hafta, <500 gramdır ve trizomi 1, 3, 19 abortuslarda hiç görülmez; 2) Komplet abortusta tedavi gerekmezken septik abortusta acil IV antibiyotik ve cerrahi şarttır; 3) TGK olgularının %33'ünden fazlası açıklanamayan grupta kalır ve Rh-negatif gebelerde Anti-D profilaksisi zorunludur."
                )
            ],
            is_checkpoint=True,
            checkpoint_number=10
        )
    ]
    return slides
