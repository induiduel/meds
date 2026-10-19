/**
 * Dönem 3 Kurul 1 — Tıbbi Biyoloji ve Genetik (TBG) Sınav Kalıbı & Hızlı Check Up Verisi.
 * Kaynak: Dr. Öğr. Üyesi Serap Arslan'ın 6 Kurul 1 ders slaytı (g01..g06), çıkmış genetik soruları ve örnek sorular.
 *
 * Üç temel sınav kalıbı:
 *  1) "sendrom": "... bulguyla gelen hasta hangi sendromu düşündürür?" (Klinik / Dismorfolojik / USG / Biyokimyasal / Sitogenetik bulgu → Sendrom)
 *  2) "ilac":    "Kanser (meme, over, mesane, böbrek, prostat, endometriyum) türlerinde belirli ilaç tedavileri"
 *  3) "belirtec":"Spesifik kanser belirteçleri, prognostik genler ve prenatal tarama belirteçleri"
 */

export type GenetikKalip = 'sendrom' | 'ilac' | 'belirtec';

export const KALIP_META: Record<GenetikKalip, { kisa: string; baslik: string; aciklama: string }> = {
  sendrom: {
    kisa: 'Bulgu → Sendrom',
    baslik: '“… bulguyla gelen hasta hangi sendromu düşündürür?”',
    aciklama:
      'Klinik dismorfoloji, prenatal USG (kistik higroma, NT, kalp defekti), hormon/enzim profili veya sitogenetik delesyon/UPD bulgusundan doğrudan sendrom tanısına giden kalıp.',
  },
  ilac: {
    kisa: 'Kanser → Hedef İlaç',
    baslik: 'Kanser türlerinde (meme, over, mesane, böbrek, prostat, endometriyum) belirli ilaç tedavileri',
    aciklama:
      'Tümördeki somatik veya germline mutasyona (BRCA1/2, HRR, FGFR2/3, VHL, TSC1/2, HER2, dMMR/MSI-H, NTRK, CDK12) göre seçilen hedefe yönelik ilaçlar, kombinasyonlar ve direnç mekanizmaları.',
  },
  belirtec: {
    kisa: 'Spesifik Belirteçler',
    baslik: 'Spesifik kanser belirteçleri, prognostik genler ve prenatal tarama belirteçleri',
    aciklama:
      'Serum tümör belirteçleri (AFP, β-hCG, LDH, PSA), doku gen panelleri (Decipher, Oncotype DX, Prolaris), iyi/kötü prognoz genleri (FGFR3, TP53, POLE) ve prenatal ikili/üçlü/dörtlü test biyokimyasal belirteçleri.',
  },
};

export const DERS_AD: Record<string, string> = {
  g01: 'Dismorfolojide Genetik Terminoloji',
  g02: 'Kromozomal Hastalıklar ve Genetik Danışma',
  g03: 'Doğumsal Kadın-Erkek Gelişim Anomalileri',
  g04: 'Ürogenital Sistem Tümörlerinde Genetik Belirteçler',
  g05: 'Prenatal Tanı ve Uygulama Alanları',
  g06: 'Preimplantasyon Genetik Tanı',
};

export interface GenetikTablo {
  id: string;
  baslik: string;
  kalip: GenetikKalip;
  sutun: string[];
  satir: string[][];
  k: string[];
}

export interface GenetikSpot {
  id: string;
  kalip: GenetikKalip;
  m: string;
  k: string;
}

export interface GenetikSoruCevap {
  id: string;
  kalip: GenetikKalip;
  s: string;
  c: string;
  k: string;
}

export type SecenekHarf = 'A' | 'B' | 'C' | 'D' | 'E';

export interface GenetikSoru {
  id: string;
  tur: 'cikmis' | 'ornek';
  yil?: string;
  kalip: GenetikKalip;
  ders: string;
  soru: string;
  secenekler: Record<SecenekHarf, string>;
  dogru: SecenekHarf;
  aciklama: string;
  sikAciklamalari: Record<SecenekHarf, string>;
  k: string;
}

export interface GenetikBolum {
  id: string;
  ad: string;
  kisa: string;
  kalip: GenetikKalip;
  tablolar: GenetikTablo[];
  spotlar: GenetikSpot[];
  soruCevaplar: GenetikSoruCevap[];
  sorular: GenetikSoru[];
}

export function kaynakGrupla(kodlar: string[]): { kod: string; ad: string; slaytlar: string[] }[] {
  const m = new Map<string, string[]>();
  for (const k of kodlar) {
    const [kod, s] = k.split(':');
    const liste = m.get(kod) || [];
    if (s && !liste.includes(s)) liste.push(s);
    m.set(kod, liste);
  }
  return Array.from(m.entries()).map(([kod, slaytlar]) => ({ kod, ad: DERS_AD[kod] || kod, slaytlar }));
}

export const katla = (s: string) =>
  s
    .toLocaleLowerCase('tr-TR')
    .replace(/ı/g, 'i')
    .replace(/ğ/g, 'g')
    .replace(/ü/g, 'u')
    .replace(/ş/g, 's')
    .replace(/ö/g, 'o')
    .replace(/ç/g, 'c')
    .replace(/[âîû]/g, (c) => ({ â: 'a', î: 'i', û: 'u' }[c] || c));

export const GENETIK_BOLUMLER: GenetikBolum[] = [
  /* ============================================================================
   * BÖLÜM 1 — KALIP 1A: DİSMORFOLOJİ, MİKRODELESYON & KROMOZOMAL SENDROMLAR
   * ============================================================================ */
  {
    id: 'sendrom-dismorfoloji-kromozom',
    ad: 'Dismorfoloji ve Kromozomal Sendromlar',
    kisa: 'Potter sekansı, Williams, Frajil X, Cri du chat, Wolf-Hirschhorn, Prader-Willi, Angelman, Trizomi 21/18/13, Turner, Klinefelter',
    kalip: 'sendrom',
    tablolar: [
      {
        id: 'gt-anomali-mekanizma',
        baslik: 'Konjenital Anomali Mekanizmaları, Majör/Minör Ayrımı ve Klinik Örnekler',
        kalip: 'sendrom',
        sutun: ['Kavram / Tablo', 'Temel Mekanizma ve Dönem', 'Tipik Klinik Bulgular / Örnekler', 'Ayırıcı Sınav Noktası'],
        satir: [
          [
            'Malformasyon',
            'Embriyonik organogenez döneminde (ilk 8 hafta) primer içsel programlama hatası',
            'Yarık dudak-damak, konjenital kalp defektleri (ASD, VSD), nöral tüp defektleri, polidaktili',
            'İzole malformasyonlar en sık konjenital anomali grubudur; genellikle multifaktöriyel kalıtılır',
          ],
          [
            'Deformasyon',
            'Fetal dönemde (organogenez sonrası) normal gelişen dokuya dışsal mekanik bası',
            'Oligohidramniyoza bağlı kraniyofasiyal basıklık ve talipes ekinovarus; prematürede yatışa bağlı plagiosefali/skafosefali',
            'Doku intrinsik olarak normaldir; mekanik bası kalkarsa postnatal düzelme potansiyeli yüksektir (Çıkmış Soru)',
          ],
          [
            'Disrupsiyon',
            'Normal gelişmekte olan yapının vasküler iskemi, enfeksiyon veya amniyotik bant ile yıkımı',
            'Amniyotik bant sekansına bağlı asimetrik parmak/ekstremite amputasyonu, kokain/varfarin teratojenitesi',
            'Kalıtsal değildir; tekrarlama riski çok düşüktür, doku yıkımı kalıcıdır',
          ],
          [
            'Displazi',
            'Enzim veya yapısal protein defekti nedeniyle dokuda anormal hücresel organizasyon',
            'Akondroplazi (FGFR3), osteogenezis imperfekta, mukopolisakkaridozlar, ektodermal displazi',
            'Tek bir doku tipini (ör. kemik/kıkırdak) tutar; doku büyüdükçe klinik bulgular yaşla belirginleşir',
          ],
          [
            'Potter Sekansı (Oligohidramniyos sekansı)',
            'Primer bilateral renal agenezi veya üretral obstrüksiyon → ağır oligohidramniyos → fetal bası',
            'Yassılmış yüz (Potter yüzü), geniş burun kökü, düşük kulak, talipes ekinovarus, pulmoner hipoplazi',
            'Tek bir primer malformasyonun (renal agenezi) zincirleme ikincil deformasyonlara yol açtığı sekans örneğidir',
          ],
          [
            'VACTERL Assosiasyonu',
            'Ortak etiyolojisi bilinmeyen, rastlantıdan sık birliktelik gösteren sporadik anomaliler',
            'Vertebra anomalisi, Anal atrezi, Kardiyak defekt, Trakeoözofageal fistül, Renal anomali, Limb (radial) defekti',
            'Sendromdan farkı ortak tek bir etiyolojinin bulunmamasıdır; zekâ normaldir, tiroid tutulumu bileşeni değildir',
          ],
          [
            'Minör vs. Majör Anomali',
            'Minör: tıbbi/kozmetik sorun yaratmayan (%<4 varyasyon); Majör: cerrahi/tıbbi müdahale gerektiren defekt',
            'Minör: beyaz perçem, iris heterokromisi, telekantus, hipertelorizm, simian çizgisi, epikantus, tek ön kesici diş (spesifik)',
            'Yarık damak/dudak majör anomalidir (Çıkmış Soru); ≥3 minör anomali varlığında majör anomali/sendrom aranır',
          ],
        ],
        k: ['g01:10-42', 'g01:64-68'],
      },
      {
        id: 'gt-dismorfik-mikrodelesyon',
        baslik: '“… Bulguyla Gelen Hasta Hangi Sendromu Düşündürür?” — Dismorfik, Mikrodelesyon ve İmprinting Sendromları',
        kalip: 'sendrom',
        sutun: ['Sendrom', 'Genetik Lokus / Mekanizma', 'Soruda Verilen Anahtar Klinik Bulgular', 'Ayırıcı Tanı ve Yönetim İpucu'],
        satir: [
          [
            'Cornelia de Lange Sendromu',
            'NIPBL, SMC1A, SMC3 (kohezin kompleksi genleri)',
            'Orta hatta birleşen kalın kaşlar (sinofriz), uzun kıvrık kirpikler, dar-ince aşağı dönük üst dudak, mikromeli, büyüme ve mental gerilik',
            'Sinofriz + mikromeli + ince üst dudak üçlüsü sorulduğunda ilk akla gelecek klasik dismorfik sendromdur',
          ],
          [
            'Seckel Sendromu',
            'Otozomal resesif (ATR vb. DNA hasar yanıt genleri)',
            'Belirgin gaga burun (beaked nose / kuş başı görünümü), ağır mikrosefali, intrauterin başlayan primordial cücelik, mental retardasyon',
            'Gaga burun + ağır mikrosefali + cücelik kombinasyonu tipiktir',
          ],
          [
            'Williams Sendromu',
            '7q11.23 mikrodelesyonu (ELN — elastin geni kaybı), otozomal dominant',
            'Elfin-like yüz (perimsi yüz, yıldızsı iris), supravalvüler aort stenozu (SVAS), infantil hiperkalsemi, büyüme geriliği, IQ 50-60 (dışadönük kişilik)',
            'Elastin (ELN) haployetmezliği SVAS yapar; tanı FISH veya mikroarray ile konur',
          ],
          [
            'Frajil X Sendromu',
            'Xq27.3 FMR1 geni 5’UTR (CGG)n üçlü tekrarı (>200 tam mutasyon → promotör metilasyonu)',
            'Uzun-ince yüz, belirgin çene, büyük kepçe kulaklar, puberte sonrası makroorşidizm, çift eklemli (hipermobil) parmaklar, %60 otizm/ADHD',
            'Kalıtsal mental retardasyonun en sık tek gen nedenidir; 50-200 tekrar premutasyon, >200 tekrar tam mutasyondur',
          ],
          [
            'Cri du Chat (Kedi Ağlaması) Sendromu',
            '5p terminal delesyonu (5p15.2-5p15.3), %85 de novo (%10-15 ebeveyn translokasyonu)',
            'Larinks hipoplazisine bağlı kedi miyavlaması şeklinde tiz ağlama, mikrosefali, yuvarlak (ay) yüz, hipertelorizm, epikantus, aşağı çekik palpebral fissür, ağır MR',
            '5. kromozom kısa kol (5p-) delesyonudur (Çıkmış Soru); karakteristik ağlama bebek büyüdükçe azalır/kaybolur',
          ],
          [
            'Wolf-Hirschhorn Sendromu',
            '4p16.3 mikrodelesyonu (4p- sendromu)',
            'Belirgin glabella ve geniş burun kökü (“Yunan savaşçı miğferi” yüzü), balık ağzı, mikrosefali, hipertelorizm, korpus kallozum agenezisi, renal hipoplazi, ağır MR ve nöbet',
            'Genellikle submikroskopik delesyondur; standart karyotipte gözden kaçabilir, FISH ile tanı konur',
          ],
          [
            'Prader-Willi Sendromu (PWS)',
            '15q11-q13 paternal delesyon (%70) veya maternal uniparental dizomi (mat UPD 15, %25-30)',
            'Yenidoğanda ağır hipotoni ve beslenme güçlüğü; çocuklukta durdurulamayan hiperfaji, santral obezite, küçük el ve ayaklar, hipogonadizm, hafif-orta MR',
            'Trizomi 15 kurtuluşu (trisomy rescue) sonrası fetüste her iki 15. kromozom anneden kalırsa (maternal UPD 15) PWS gelişir (Çıkmış Soru)',
          ],
          [
            'Angelman Sendromu (AS)',
            '15q11-q13 maternal delesyon (UBE3A kaybı) veya paternal uniparental dizomi (pat UPD 15)',
            'Ağır mental retardasyon, konuşamama (afazi), geniş tabanlı ataksik yürüyüş, uygunsuz gülme atakları, dirençli konvülziyonlar, mikrosefali',
            'Aynı 15q11-q13 bölgesinin anne kopyası kaybedilirse veya her iki 15 babadan gelirse (paternal UPD 15) gelişir',
          ],
          [
            'DiGeorge / Velokardiyofasiyal Sendrom',
            '22q11.2 mikrodelesyonu (en sık mikrodelesyon)',
            'Konotrunkal kalp anomalileri (Fallot, trunkus arteriozus), timus hipoplazisi (T hücre yetmezliği), paratiroid hipoplazisi (hipokalsemi), yarık damak',
            'Aynı bölgenin mikroduplikasyonu (22q11.2 dup) Cat-Eye (Kedi Gözü) sendromuna yol açar',
          ],
          [
            'Smith-Magenis / CMT1A / HNPP',
            '17p11.2 del (Smith-Magenis); 17p12 dup (CMT1A); 17p12 del (HNPP)',
            'Smith-Magenis: brakisefali, uyku bozukluğu, kendine zarar verme. CMT1A: periferik motor-duyusal nöropati. HNPP: basıya duyarlı nöropati',
            'Eşit olmayan (unequal) krossing-over ile 17p12 duplikasyonu CMT1A, delesyonu HNPP yapar',
          ],
        ],
        k: ['g01:50-85', 'g02:18', 'g02:67-68', 'g02:79-85', 'g05:92'],
      },
      {
        id: 'gt-trizomi-gonozom',
        baslik: 'Otozomal Trizomiler ve Gonozomal Sendromlarda Ayırıcı Klinik Bulgular',
        kalip: 'sendrom',
        sutun: ['Sendrom ve Karyotip', 'Temel Oluşum Mekanizması', 'Tipik Klinik ve USG Bulguları', 'Kritik Sınav ve Danışma Spotu'],
        satir: [
          [
            'Down Sendromu (Trizomi 21)',
            '%95 serbest trizomi (%90 maternal Mayoz I ayrılmama), %4 Robertsonian translokasyon [en sık rob(14;21)], %1-2 mozaik',
            'Hipotoni, brakisefali, yukarı çekik palpebral fissür, epikantus, Brushfield lekeleri, simian çizgisi, endokardiyal yastık defekti (AVSD, %33), duodenal atrezi',
            'rob(21;21) veya i(21q) taşıyıcısında canlı doğumda Down riski %100’dür; translokasyon anne kaynaklıysa risk (%15) babadan (%4-5) yüksektir',
          ],
          [
            'Edwards Sendromu (Trizomi 18)',
            'Maternal mayotik ayrılmama (ileri anne yaşı ilişkili); gebeliklerin %95’i spontan abortusla sonlanır',
            'Yenidoğanda hipertonisite, belirgin oksiput, mikrognati, kısa sternum, yumruk el (clenched hand: 2. parmak 3. üzerine, 5. parmak 4. üzerine biner), fırlak topuk (rocker-bottom feet)',
            'Down sendromunun aksine hipotoni değil hipertonisite görülür; canlı doğan bebeklerin %80’i kızdır, ilk ayda çoğu kaybedilir',
          ],
          [
            'Patau Sendromu (Trizomi 13)',
            '%75 serbest trizomi, %20 Robertsonian translokasyon [özellikle rob(13;14)]',
            'Klasik triad: Mikroftalmi/anoftalmi + Yarık dudak-damak + Postaksiyel polidaktili; ayrıca holoprozensefali ve oksipital saçlı deride defekt (cutis aplasia congenita)',
            'Orta hat ön beyin anomalisi (holoprozensefali) ve klasik triad sorulduğunda Trizomi 13 seçilir; %90’ı ilk ayda kaybedilir',
          ],
          [
            'Triploidi (69,XXX / 69,XXY / 69,XYY)',
            'En sık dispermi (oositin iki spermle döllenmesi, baba kaynaklı ekstra set); 1. trimester kromozomal düşüklerin %20’si',
            'Ağır asimetrik İUGR, büyük kistik plasenta (parsiyel mol hidatidiform), sindaktili (3-4. parmaklar), hidrosefali',
            'Ekstra takım babadan gelirse (diandri) plasenta büyük ve kistik (parsiyel mol); anneden gelirse (digini) plasenta küçük ve fetüs ağır büyüme geriliklidir',
          ],
          [
            'Turner Sendromu (45,X ve varyantları)',
            '%50-60 klasik 45,X (%75-80 paternal X/Y kaybı), %20 izokromozom i(Xq), %30 mozaik (45,X/46,XX veya 45,X/46,XY)',
            'Prenatal USG: kistik higroma, geniş ASD/VSD, aort koarktasyonu, biküspit aort. Postnatal: kısa boy, yele boyun, el-ayak sırtında lenfödem, kalkan göğüs, kubitus valgus, çizgi (streak) gonad, primer amenore',
            'Zekâ düzeyi tipik olarak normaldir (Çıkmış Soru); del(Xp) kısa boy ve somatik malformasyon, del(Xq) ise yalnız gonadal disfonksiyon yapar; tedavide GH + östrojen verilir',
          ],
          [
            'Klinefelter Sendromu (47,XXY)',
            'Canlı erkek doğumlarda en sık gonozomal varyant (1/500); %50 maternal, %50 paternal ayrılmama',
            'Uzun boy (östaki/alt ekstremite uzun), küçük ve sert testisler (seminifer tübül hiyalinizasyonu), azoospermi/infertilite, jinekomasti (%30), düşük testosteron, yüksek FSH/LH',
            'USG’de artmış ense saydamlığı (NT) beklenen sendromlardan değildir (Çıkmış Soru); ekstra X sayısı arttıkça (48,XXXY, 49,XXXXY) mental retardasyon ağırlaşır',
          ],
        ],
        k: ['g02:10', 'g02:42-78', 'g03:39-44', 'g05:30'],
      },
    ],
    spotlar: [
      { id: 'gs-101', kalip: 'sendrom', m: 'Oligohidramniyoza bağlı kraniyofasiyal basıklık ve talipes ekinovarus deformitesi, fetal dönemde normal gelişen dokunun mekanik basıya uğramasıyla oluşan klasik bir **deformasyon** (Potter sekansı) örneğidir.', k: 'g01:28' },
      { id: 'gs-102', kalip: 'sendrom', m: 'Dismorfolojik muayenede **yarık damak ve yarık dudak** majör konjenital anomalidir; beyaz perçem, iris heterokromisi, telekantus, hipertelorizm, epikantus ve simian çizgisi ise **minör** anomalilerdir.', k: 'g01:18' },
      { id: 'gs-103', kalip: 'sendrom', m: 'Bir yenidoğanda birinci derece akrabalarında bulunmayan **en az 3 minör anomali** saptandığında çocuk “dismorfik” kabul edilir ve eşlik eden majör anomali (SSS, KVS, GİS) araştırılır.', k: 'g01:20' },
      { id: 'gs-104', kalip: 'sendrom', m: 'Orta hatta birleşen kalın kaşlar (**sinofriz**), dar-ince aşağı dönük üst dudak, mikromeli ve büyüme-zihinsel gerilik bulguları **Cornelia de Lange sendromunu** düşündürür.', k: 'g01:50' },
      { id: 'gs-105', kalip: 'sendrom', m: 'Belirgin **gaga burun (beaked nose)**, ağır mikrosefali ve intrauterin başlayan cücelik ile gelen hastada **Seckel sendromu** düşünülür.', k: 'g01:56' },
      { id: 'gs-106', kalip: 'sendrom', m: 'Perimsi yüz (**Elfin-like face**), **supravalvüler aort stenozu**, infantil hiperkalsemi ve hafif-orta mental retardasyon ile gelen hastada **7q11.23 ELN (elastin) mikrodelesyonuna** bağlı **Williams sendromu** düşünülür.', k: 'g01:79' },
      { id: 'gs-107', kalip: 'sendrom', m: 'Uzun-ince yüz, büyük kulaklar, puberte sonrası **makroorşidizm**, hipermobil parmaklar ve otizm bulgularıyla gelen erkek hastada **FMR1 geni 5’UTR (CGG)n üçlü tekrar artışına (>200 tam mutasyon, promotör metilasyonu)** bağlı **Frajil X sendromu** düşünülür.', k: 'g01:82' },
      { id: 'gs-108', kalip: 'sendrom', m: '**Beşinci kromozomun kısa kolunda terminal delesyon (5p15.2-5p15.3)**, larinks anomalisine bağlı kedi miyavlaması ağlaması, mikrosefali ve yuvarlak yüz ile karakterize **Cri du chat sendromuna** yol açar.', k: 'g02:67' },
      { id: 'gs-109', kalip: 'sendrom', m: 'Belirgin glabella (“Yunan savaşçı miğferi” yüzü), balık ağzı, korpus kallozum agenezisi, renal hipoplazi ve ağır mental gerilik ile gelen hastada **4p16.3 mikrodelesyonuna** bağlı **Wolf-Hirschhorn sendromu** düşünülür.', k: 'g02:68' },
      { id: 'gs-110', kalip: 'sendrom', m: 'Yenidoğanda **hipertonisite**, belirgin oksiput, kısa sternum, üst üste binmiş parmaklarla **yumruk el (clenched hand)** ve **fırlak topuk (rocker-bottom feet)** bulguları **Edwards sendromunu (Trizomi 18)** düşündürür.', k: 'g02:53' },
      { id: 'gs-111', kalip: 'sendrom', m: '**Mikroftalmi/anoftalmi + yarık dudak-damak + postaksiyel polidaktili** triadı, **holoprozensefali** ve oksipital deri defekti (cutis aplasia) ile gelen yenidoğanda **Patau sendromu (Trizomi 13)** düşünülür.', k: 'g02:60' },
      { id: 'gs-112', kalip: 'sendrom', m: 'Fetal ultrasonografide **kistik higroma, geniş ASD ve VSD** saptanan fetüste ve zekâ düzeyi tipik olarak **normal** olan kısa boylu, primer amenoreli kız hastada **Turner sendromu (45,X)** düşünülür.', k: 'g02:75' },
      { id: 'gs-113', kalip: 'sendrom', m: '15q11-q13 bölgesinde **paternal delesyon veya maternal UPD 15** varsa hipotoni, hiperfaji ve obezite ile seyreden **Prader-Willi sendromu**; **maternal delesyon veya paternal UPD 15** varsa ağır MR, ataksi ve gülme ataklarıyla seyreden **Angelman sendromu** gelişir.', k: 'g02:83' },
    ],
    soruCevaplar: [
      {
        id: 'gqa-101',
        kalip: 'sendrom',
        s: 'Oligohidramniyoza bağlı kraniyofasiyal basıklık ve talipes ekinovarus ile doğan bebekte hangi anomali mekanizması ve hangi sekans düşünülür?',
        c: 'Fetal dönemde mekanik basıya bağlı gelişen Deformasyon mekanizması ve Potter sekansı (primer neden: bilateral renal agenezi).',
        k: 'g01:28',
      },
      {
        id: 'gqa-102',
        kalip: 'sendrom',
        s: '5. kromozomun kısa kolunda (5p15.2-5p15.3) delesyon ve kedi miyavlaması şeklinde tiz ağlama ile gelen bebekte tanı nedir?',
        c: 'Cri du chat (Kedi ağlaması) sendromu (%85 de novo 5p delesyonu).',
        k: 'g02:67',
      },
      {
        id: 'gqa-103',
        kalip: 'sendrom',
        s: 'Elfin-like yüz, supravalvüler aort stenozu ve infantil hiperkalsemi bulgularıyla gelen çocukta hangi sendrom ve hangi gen delesyonu düşünülür?',
        c: 'Williams sendromu — 7q11.23 bölgesinde ELN (elastin) genini içeren mikrodelesyon.',
        k: 'g01:79',
      },
      {
        id: 'gqa-104',
        kalip: 'sendrom',
        s: 'Diğer kromozomal sendromların aksine zekâ düzeyi tipik olarak normal olan, prenatal USG’de kistik higroma ve kalp defekti (ASD/VSD, aort koarktasyonu) ile gelen sendrom hangisidir?',
        c: 'Turner sendromu (45,X). Sözel zekâ normaldir; kısa boy için büyüme hormonu (GH), sekonder cinsiyet karakterleri için östrojen verilir.',
        k: 'g02:75',
      },
      {
        id: 'gqa-105',
        kalip: 'sendrom',
        s: 'Trizomi 15 kurtuluşu (trisomy rescue) sonucunda her iki 15. kromozomu da anneden kalıtılan (maternal UPD 15) bir çocukta hangi imprinting sendromu gelişir?',
        c: 'Prader-Willi sendromu (yenidoğanda ağır hipotoni, çocuklukta hiperfaji, obezite, küçük el-ayak ve hipogonadizm).',
        k: 'g02:83',
      },
    ],
    sorular: [
      {
        id: 'gq-cikmis-101',
        tur: 'cikmis',
        yil: '2025-2026',
        kalip: 'sendrom',
        ders: 'g02',
        soru: 'Beşinci kromozomun kısa kolunda delesyon (5p delesyonu) sonucu ortaya çıkan sendrom aşağıdakilerden hangisidir?',
        secenekler: {
          A: 'Wolf-Hirschhorn sendromu',
          B: 'Prader-Willi sendromu',
          C: 'Cri du chat sendromu (kedi miyavlaması sendromu)',
          D: 'Angelman sendromu',
          E: 'DiGeorge sendromu',
        },
        dogru: 'C',
        aciklama: 'Beşinci kromozomun kısa kolunun terminal delesyonu (5p15.2-5p15.3) larinks hipoplazisine bağlı kedi miyavlaması şeklinde ağlama, mikrosefali, yuvarlak yüz ve ağır mental gerilik ile seyreden Cri du chat sendromuna neden olur.',
        sikAciklamalari: {
          A: 'Wolf-Hirschhorn sendromu 4. kromozomun kısa kolundaki mikrodelesyon (4p16.3) sonucu oluşur ve belirgin glabella (miğfer yüzü) ile karakterizedir.',
          B: 'Prader-Willi sendromu 15q11-q13 bölgesinin paternal delesyonu veya maternal uniparental dizomisi sonucu gelişir.',
          C: 'Cri du chat sendromu 5p (5p15.2-5p15.3) terminal delesyonu sonucu ortaya çıkar; olguların %85’i de novo delesyondur.',
          D: 'Angelman sendromu 15q11-q13 bölgesinin maternal delesyonu (UBE3A kaybı) veya paternal uniparental dizomisi sonucu oluşur.',
          E: 'DiGeorge sendromu 22q11.2 mikrodelesyonu sonucu gelişir ve konotrunkal kalp anomalileri, timus ve paratiroid hipoplazisi ile seyreder.',
        },
        k: 'g02:67',
      },
      {
        id: 'gq-cikmis-102',
        tur: 'cikmis',
        yil: '2025-2026',
        kalip: 'sendrom',
        ders: 'g01',
        soru: 'Aşağıdaki konjenital anomali örneklerinden hangisi bir deformasyon örneğidir?',
        secenekler: {
          A: 'Amniyotik bant sekansına bağlı parmak amputasyonu',
          B: 'Akondroplazide görülen rizomelik ekstremite kısalığı',
          C: 'Oligohidramniyoza bağlı kraniyofasiyal basıklık ve talipes deformitesi',
          D: 'Organogenez hatasına bağlı ventriküler septal defekt',
          E: 'Nöral tüp kapanma kusuruna bağlı meningomyelosel',
        },
        dogru: 'C',
        aciklama: 'Deformasyon, fetal dönemde genetik ve yapısal olarak normal gelişmiş bir dokunun rahim içi mekanik basıya (örneğin oligohidramniyos, çoğul gebelik veya uterin anomali) maruz kalarak şekil değiştirmesidir. Oligohidramniyoza bağlı kraniyofasiyal basıklık ve talipes (Potter sekansı) klasik deformasyon örneğidir.',
        sikAciklamalari: {
          A: 'Amniyotik bantlara bağlı parmak amputasyonu, normal gelişen dokunun dışsal bir etkenle yıkıma uğradığı disrupsiyon mekanizmasıdır.',
          B: 'Akondroplazi, FGFR3 mutasyonu nedeniyle kıkırdak dokusunun hücresel organizasyonunun bozulduğu iskelet displazisi örneğidir.',
          C: 'Oligohidramniyoza bağlı kraniyofasiyal basıklık ve talipes ekinovarus, intrauterin mekanik sıkışmaya bağlı gelişen bir deformasyondur.',
          D: 'Ventriküler septal defekt (VSD), embriyonik organogenez dönemindeki birincil gelişim hatası olduğundan malformasyondur.',
          E: 'Meningomyelosel, nöral tüpün embriyonik dönemde kapanamaması sonucu gelişen primer bir malformasyondur.',
        },
        k: 'g01:28',
      },
      {
        id: 'gq-cikmis-103',
        tur: 'cikmis',
        yil: '2024-2025',
        kalip: 'sendrom',
        ders: 'g02',
        soru: 'Aşağıdaki genetik sendromlardan hangisinde zekâ düzeyi tipik olarak normaldir ve belirgin zihinsel yetersizlik (mental retardasyon) birincil klinik tabloyu oluşturmaz?',
        secenekler: {
          A: 'Down sendromu (Trizomi 21)',
          B: 'Edwards sendromu (Trizomi 18)',
          C: 'Turner sendromu (45,X)',
          D: 'Cri du chat sendromu (5p delesyonu)',
          E: 'Frajil X sendromu',
        },
        dogru: 'C',
        aciklama: 'Turner sendromunda (45,X) hastaların sözel zekâ düzeyi tipik olarak normal veya normalin üzerindedir; yalnızca görsel-uzamsal algı ve matematik alanında hafif destek gerekebilir. Kısa boy ve çizgi gonad (primer amenore) ana bulgulardır.',
        sikAciklamalari: {
          A: 'Down sendromunda (Trizomi 21) hafif-orta derecede mental retardasyon (ortalama IQ 25-50) her zaman klinik tabloya eşlik eder.',
          B: 'Edwards sendromunda (Trizomi 18) ağır psikomotor ve zihinsel gerilik ile çoklu organ anomalileri mevcuttur.',
          C: 'Turner sendromunda (45,X) zekâ düzeyi tipik olarak normaldir; belirgin mental retardasyon yalnız küçük halka X kromozomu (XIST eksikliği) varsa görülür.',
          D: 'Cri du chat sendromunda (5p-) mikrosefali ve ağır mental retardasyon (IQ genellikle <20) temel bulgular arasındadır.',
          E: 'Frajil X sendromu kalıtsal mental retardasyonun en sık tek gen nedenidir ve erkeklerde orta-ağır zihinsel gerilik yapar.',
        },
        k: 'g02:75',
      },
      {
        id: 'gq-cikmis-104',
        tur: 'cikmis',
        yil: '2023-2024',
        kalip: 'sendrom',
        ders: 'g01',
        soru: 'Aşağıdakilerden hangisi minör anomaliler arasında yer almaz?',
        secenekler: {
          A: 'Yarık damak/dudak',
          B: 'Beyaz perçem',
          C: 'İris heterokromisi',
          D: 'Telekantus',
          E: 'Hipertelorizm',
        },
        dogru: 'A',
        aciklama: 'Yarık damak ve/veya yarık dudak, beslenme, konuşma ve estetik açıdan cerrahi ve tıbbi müdahale gerektiren majör bir konjenital malformasyondur. Diğer şıklardaki bulgular tıbbi sorun yaratmayan ancak sendrom tanısında ipucu veren minör anomalilerdir.',
        sikAciklamalari: {
          A: 'Yarık damak/dudak fonksiyonel bozukluk yapan ve cerrahi onarım gerektiren majör bir anomalidir.',
          B: 'Beyaz perçem (poliozis), Waardenburg sendromu gibi tablolarda ipucu olabilen ancak tek başına tıbbi sorun yaratmayan minör bir anomalidir.',
          C: 'İris heterokromisi, göz fonksiyonunu bozmayan pigmentasyon farklılığı olup minör anomali grubundadır.',
          D: 'Telekantus (iç kantuslar arası mesafenin artması, pupiller mesafe normal), dismorfolojik değerlendirmede kullanılan minör bir bulgudur.',
          E: 'Hipertelorizm (her iki orbita ve pupilla arası mesafenin artması), kraniofasiyal sendromlara eşlik edebilen minör bir anomalidir.',
        },
        k: 'g01:18',
      },
      {
        id: 'gq-ornek-105',
        tur: 'ornek',
        kalip: 'sendrom',
        ders: 'g01',
        soru: 'Mental retardasyon, kısa boy, tipik yüz görünümü (Elfin-like face), supravalvüler aortik stenoz ve infantil hiperkalsemi bulguları olan bir çocukta en olası tanı ve sorumlu genetik değişiklik aşağıdakilerden hangisidir?',
        secenekler: {
          A: 'Williams sendromu – 7q11.23 ELN delesyonu',
          B: 'Wolf-Hirschhorn sendromu – 4p16.3 delesyonu',
          C: 'Cornelia de Lange sendromu – 5p13 NIPBL mutasyonu',
          D: 'DiGeorge sendromu – 22q11.2 delesyonu',
          E: 'Smith-Magenis sendromu – 17p11.2 delesyonu',
        },
        dogru: 'A',
        aciklama: 'Williams sendromu 7q11.23 bölgesindeki ELN (elastin) genini içeren mikrodelesyon sonucu gelişir. Elastin yetersizliği supravalvüler aort stenozuna yol açarken, Elfin-like yüz ve infantil hiperkalsemi tanı koydurucu bulgulardır.',
        sikAciklamalari: {
          A: 'Williams sendromu 7q11.23 ELN mikrodelesyonu ile oluşur; Elfin yüzü, supravalvüler aort stenozu ve infantil hiperkalsemi klasik bulgularıdır.',
          B: 'Wolf-Hirschhorn sendromu 4p16.3 delesyonu ile oluşur; belirgin glabella (miğfer yüzü), balık ağzı ve nöbetlerle seyreder.',
          C: 'Cornelia de Lange sendromu sinofriz (birleşik kaşlar), ince üst dudak ve mikromeli ile karakterizedir.',
          D: 'DiGeorge sendromu 22q11.2 delesyonu sonucu gelişir; timus aplazisi, hipoparatiroidi (hipokalsemi) ve konotrunkal kalp anomalisi yapar.',
          E: 'Smith-Magenis sendromu 17p11.2 mikrodelesyonu sonucu gelişir; brakisefali ve davranış/uyku bozukluklarıyla seyreder.',
        },
        k: 'g01:79',
      },
      {
        id: 'gq-ornek-106',
        tur: 'ornek',
        kalip: 'sendrom',
        ders: 'g02',
        soru: 'Yenidoğan döneminde tipik hipertonisite, belirgin oksiput, kısa sternum, üst üste binmiş parmaklarla karakterize yumruk el (clenched hand) ve fırlak topuk (rocker-bottom ayak) bulguları saptanan bir bebekte en olası tanı aşağıdakilerden hangisidir?',
        secenekler: {
          A: 'Down sendromu (Trizomi 21)',
          B: 'Edwards sendromu (Trizomi 18)',
          C: 'Patau sendromu (Trizomi 13)',
          D: 'Turner sendromu (45,X)',
          E: 'Wolf-Hirschhorn sendromu (4p-)',
        },
        dogru: 'B',
        aciklama: 'Yenidoğanda hipertonisite, belirgin oksiput, kısa sternum, yumruk el (2. parmağın 3., 5. parmağın 4. parmak üzerine binmesi) ve fırlak topuk (rocker-bottom feet) Edwards sendromunun (Trizomi 18) klasik klinik tablosudur.',
        sikAciklamalari: {
          A: 'Down sendromunda hipertonisite değil belirgin hipotoni, brakisefali, simian çizgisi ve endokardiyal yastık defekti görülür.',
          B: 'Edwards sendromu (Trizomi 18) hipertonisite, yumruk el (clenched hand), rocker-bottom ayak ve kısa sternum ile karakterizedir.',
          C: 'Patau sendromunda (Trizomi 13) mikroftalmi, yarık dudak-damak, postaksiyel polidaktili ve holoprozensefali ön plandadır.',
          D: 'Turner sendromunda (45,X) yele boyun, el-ayak sırtında konjenital lenfödem ve aort koarktasyonu görülür.',
          E: 'Wolf-Hirschhorn sendromunda (4p16.3 del) belirgin glabella, hipertelorizm, balık ağzı ve ağır hipotoni/nöbet görülür.',
        },
        k: 'g02:53',
      },
    ],
  },

  /* ============================================================================
   * BÖLÜM 2 — KALIP 1B: CİNSİYET GELİŞİM BOZUKLUKLARI (CGB / DSD) & AMBİGUS GENİTALYA
   * ============================================================================ */
  {
    id: 'sendrom-cinsiyet-gelisim',
    ad: 'Cinsiyet Gelişim Anomalileri (CGB / DSD) ve Sendromları',
    kisa: '21-OH KAH, Testiküler feminizasyon (CAIS), 5α-redüktaz 2 eksikliği, Swyer, Miks gonadal disgenezi, SRY/SOX9/WNT4/FOXL2/WT1/DAX1',
    kalip: 'sendrom',
    tablolar: [
      {
        id: 'gt-gonad-genler',
        baslik: 'Gonadal Farklılaşma Genleri (Testis vs. Over) ve Mutasyonlarında Gelişen Sendromlar',
        kalip: 'sendrom',
        sutun: ['Gen ve Kromozom', 'Normal Görevi (Yolak)', 'Mutasyon / Dozaj Değişikliği', 'Gelişen Klinik Sendrom ve Bulgular'],
        satir: [
          [
            'SRY (Yp11.3)',
            'Bipotansiyel gonadda SOX9 ekspresyonunu başlatarak testis gelişimini tetikler',
            'Delesyon veya fonksiyon kaybı (46,XY’de %10-15); Xp’ye translokasyon (46,XX’te %80-90)',
            'Kaybı → 46,XY Swyer sendromu (saf gonadal disgenezi); Xp translokasyonu → 46,XX erkek CGB',
          ],
          [
            'SOX9 (17q24)',
            'Otozomal testis belirleyici gen; Sertoli hücresi farklılaşması, AMH sentezi ve kıkırdak gelişimi',
            'Heterozigot fonksiyon kaybı (haployetmezlik) veya duplikasyon',
            'Kaybı → Kampomelik displazi (ağır iskelet displazisi) + olguların %75’inde 46,XY CGB; duplikasyonu → SRY negatif 46,XX erkek',
          ],
          [
            'WT1 (11p13)',
            'Bipotansiyel gonad ve böbrek (ürogenital katlantı) gelişimi için zorunlu transkripsiyon faktörü',
            'Heterozigot mutasyonlar (46,XY CGB olgularının %3-4’ü)',
            'Wilms tümörü + Fokal segmental glomerüloskleroz (FSGS) + 46,XY CGB (Denys-Drash / Frasier spektrumu)',
          ],
          [
            'SF-1 / NR5A1 (9q33)',
            'Hipotalamo-hipofizer-gonadal aks, adrenal bez gelişimi ve steroidogenez regülasyonu',
            'Heterozigot/homozigot fonksiyon kaybı mutasyonları',
            '46,XY CGB (gonadal disgenezi ± primer adrenal yetmezlik); SRY ve SOX9 ile birlikte testis yolağında çalışır',
          ],
          [
            'DAX1 / NR0B1 (Xp21.2)',
            'Adrenal ve gonadal gelişimde rol alır; normal kopyada testis gelişimini engellemez',
            'Duplikasyon (doza bağımlı anti-testis etki) vs. İnaktive edici mutasyon (LOF)',
            'Duplikasyonu → SOX9’u baskılayarak 46,XY CGB (cinsiyet tersine dönmesi); LOF mutasyonu → X’e bağlı konjenital adrenal hipoplazi (AHC) + hipogonadotropik hipogonadizm',
          ],
          [
            'WNT4 (1p36) ve RSPO1 (1p34)',
            'Over gelişim yolağı: β-katenini stabilize ederek SOX9’u baskılar, oosit sağkalımını korur',
            'WNT4 homozigot LOF mutasyonu vs. WNT4 heterozigot mutasyonu',
            'WNT4 homozigot kaybı → SERKAL sendromu (46,XX cinsiyet tersine dönmesi + böbrek/adrenal/akciğer agenezisi); heterozigot kaybı → 46,XX’te Müllerian aplazi ve hiperandrojenizm',
          ],
          [
            'FOXL2 (3q22)',
            'Pregranüloza hücrelerinde SOX9 transkripsiyonunu baskılayarak over kimliğini korur',
            'Heterozigot fonksiyon kaybı mutasyonu (otozomal dominant)',
            'BPES sendromu (Blefarofimozis, Pitozis, Epikantus inversus) + erken over yetmezliği (POF)',
          ],
          [
            'DHCR7 (11q13) ve MKKS (20p12)',
            'DHCR7: kolesterol biyosentezi (7-dehidrokolesterol redüktaz)',
            'Otozomal resesif enzim/şaperon mutasyonu',
            'DHCR7 mutasyonu → Smith-Lemli-Opitz sendromu (kolesterol ve testosteron sentez eksikliği → 46,XY CGB, 2-3. ayak parmak sindaktilisi); MKKS → McKusick-Kaufman sendromu (46,XX vajinal atrezi/hidrometrokolpos, polidaktili, KKH)',
          ],
        ],
        k: ['g03:11-32'],
      },
      {
        id: 'gt-cgb-ayirici',
        baslik: 'Kuşkulu Genitalya (Ambigus Genitalya) ve CGB Sendromlarında Ayırıcı Tanı Tablosu',
        kalip: 'sendrom',
        sutun: ['Sendrom ve Karyotip', 'Genetik / Enzimatik Defekt', 'İç ve Dış Genitalya + Klinik Bulgular', 'Laboratuvar ve Tedavi / Sınav İpucu'],
        satir: [
          [
            'Konjenital Adrenal Hiperplazi — 21-Hidroksilaz Eksikliği (46,XX CGB)',
            '6p21.3 CYP21A2 mutasyonu (OR); KAH olgularının %90-95’i',
            'Overler, uterus ve tüpler normal; dış genitalyada klitoromegali ve labioskrotal füzyon (ambigus genitalya); gonadlar ele gelmez; %75 tuz kaybı krizi',
            'Yenidoğanda ambigus genitalyanın EN SIK nedenidir; serum 17-OHP çok yüksektir; gebeliğin 6-8. haftasında anneye deksametazon verilerek kız fetüste virilizasyon önlenir (Çıkmış Soru)',
          ],
          [
            '11β-Hidroksilaz vs. 3β-HSD / POR Eksikliği',
            'CYP11B1 (11β-OH), HSD3B2 (3β-HSD), POR (P450 oksiredüktaz)',
            '11β-OH eksikliği yalnız 46,XX CGB (virilizasyon + hipertansiyon) yapar; 3β-HSD ve POR eksikliği ise HEM 46,XX HEM 46,XY CGB yapar',
            '11β-hidroksilaz eksikliği 46,XY DSD etiyolojisinde yer almaz; 3β-HSD hem 46,XX hem 46,XY DSD yapar (Çıkmış Soru)',
          ],
          [
            'Komplet Androjen Duyarsızlık Sendromu — Testiküler Feminizasyon (46,XY CGB)',
            'Xq11-12 AR (Androjen Reseptörü) geninde X’e bağlı resesif inaktive edici mutasyon',
            'Doğumda dış genitalya tamamen normal dişi; pubertede normal dişi meme gelişimi var, primer amenore, aksiller/pubik kıllanma yok, kısa kör vajen; uterus/tüp (AMH var) ve Wolff yapıları (AR direnci) YOK',
            'Testisler inguinal kanalda/labiumda palpabl olabilir (gonadoblastom/disgerminom riski nedeniyle puberte sonrası gonadoktomi); parsiyel formu (PAIS) Reifenstein sendromudur (Çıkmış Soru)',
          ],
          [
            '5α-Redüktaz 2 Eksikliği (46,XY CGB)',
            '2p23 SRD5A2 geni mutasyonu (OR; Türkiye’de en sık p.L55Q)',
            'Doğumda ambigus genitalya / perineoskrotal hipospadias ve kör vajinal poş nedeniyle genellikle kız yetiştirilir; uterus yok, Wolff yapıları var; pubertede ses kalınlaşması, kas kitlesi artışı ve fallus büyümesiyle erkek yönünde virilizasyon',
            'Testosteron normal/yüksek, DHT düşüktür (T/DHT oranı artmış); pubertede virilizasyonu sağlayan artan testosteron düzeyidir',
          ],
          [
            'Swyer Sendromu — 46,XY Saf Gonadal Disgenezi',
            'SRY (%10-15), SOX9, SF1 veya DHH mutasyonu',
            'Bilateral çizgi (streak) gonad; Sertoli ve Leydig hücresi olmadığı için AMH ve testosteron üretilemez → uterus ve fallop tüpleri VARDIR, dış genitalya tamamen normal dişidir',
            'Yenidoğan döneminde ambigus genitalya YAPMAZ (Çıkmış Soru); pubertede boyu uzun, meme gelişimi olmayan primer amenoreli kız olarak başvurur; gonadoblastom riski çok yüksektir',
          ],
          [
            'Miks Gonadal Disgenezi (45,X/46,XY Mozaikliği)',
            '45,X/46,XY mozaik karyotip',
            'En karakteristik özelliği ASİMETRİK gonad gelişimidir: bir tarafta disgenetik testis, karşı tarafta çizgi (streak) gonad ve Müllerian yapılar; yenidoğanda ambigus genitalya',
            '46,XX/46,XY kimerizminden (iki ayrı zigotun birleşmesi) farklı olarak tek zigottaki mitotik Y kaybıyla oluşur; disgenetik gonadlarda tümör riski yüksektir',
          ],
        ],
        k: ['g03:34-75', 'g05:78'],
      },
    ],
    spotlar: [
      { id: 'gs-201', kalip: 'sendrom', m: 'Yenidoğan bir bebekte kuşkulu dış genitalyanın (**ambigus genitalya**) ve **46,XX CGB**’nin en sık nedeni **21-hidroksilaz (CYP21A2) eksikliğine bağlı Konjenital Adrenal Hiperplazidir (%90-95)**; tanı **serum 17-hidroksiprogesteron (17-OHP)** yüksekliğiyle konur.', k: 'g03:60' },
      { id: 'gs-202', kalip: 'sendrom', m: 'Konjenital adrenal hiperplazi riski taşıyan gebelikte 46,XX kız fetusun dış genital virilizasyonunu engellemek için gebeliğin 6-8. haftasında anneye plasentayı geçen **deksametazon** başlanır; CVS ile 46,XX hasta fetüs doğrulanırsa doğuma kadar sürdürülür.', k: 'g03:67' },
      { id: 'gs-203', kalip: 'sendrom', m: '**3β-hidroksisteroid dehidrogenaz (3β-HSD)** ve **P450 oksiredüktaz (POR)** eksiklikleri hem 46,XX hem 46,XY CGB yapabilirken; **11β-hidroksilaz** ve **21-hidroksilaz** eksiklikleri yalnızca **46,XX CGB** yapar (46,XY DSD etiyolojisinde yer almaz).', k: 'g03:62' },
      { id: 'gs-204', kalip: 'sendrom', m: '**46,XY** karyotip, **X’e bağlı resesif AR mutasyonu**, doğumda tamamen dişi dış genitalya, pubertede **normal dişi meme gelişimi**, **primer amenore**, aksiller/pubik kıllanma yokluğu ve **uterus/tüp ile Wolff yapılarının bulunmaması** **Testiküler feminizasyon (Komplet AIS)** sendromunu düşündürür.', k: 'g03:56' },
      { id: 'gs-205', kalip: 'sendrom', m: 'Doğumda kuşkulu/dişi dış genitalya nedeniyle kız yetiştirilen **46,XY** bir çocukta **pubertede artan testosteronla ses kalınlaşması, kas kitlesi artışı ve fallus büyümesi (virilizasyon)** gelişmesi, **otozomal resesif 5α-redüktaz 2 eksikliğini (SRD5A2, en sık p.L55Q)** düşündürür.', k: 'g03:53' },
      { id: 'gs-206', kalip: 'sendrom', m: '**Swyer sendromunda (46,XY saf gonadal disgenezi)** çizgi gonadlar hem AMH hem testosteron üretemediği için uterus vardır ve dış genitalya tamamen normal dişidir; bu nedenle **yenidoğan ambigus genitalya ayırıcı tanısında yer almaz**.', k: 'g03:48' },
      { id: 'gs-207', kalip: 'sendrom', m: '**45,X/46,XY** mozaik karyotip, kuşkulu genitalya ve bir tarafta disgenetik testis, karşı tarafta streak gonad (**asimetrik gonadal gelişim**) varlığı **Miks gonadal disgeneziyi** düşündürür.', k: 'g03:49' },
      { id: 'gs-208', kalip: 'sendrom', m: 'Embriyonik dönemde bipotansiyel gonadın **testis** yönünde farklılaşmasını **SRY, SOX9 ve SF1 (NR5A1)**; **over (yumurtalık)** yönünde farklılaşmasını ise **WNT4, RSPO1, FOXL2 ve DAX1** genleri yönetir.', k: 'g03:12' },
      { id: 'gs-209', kalip: 'sendrom', m: '**SOX9** heterozigot kaybı **Kampomelik displazi + 46,XY CGB**; **WT1** mutasyonu **Wilms tümörü + FSGS + 46,XY CGB**; **WNT4** homozigot kaybı **SERKAL sendromu**; **FOXL2** mutasyonu ise **BPES sendromu** yapar.', k: 'g03:25' },
    ],
    soruCevaplar: [
      {
        id: 'gqa-201',
        kalip: 'sendrom',
        s: 'Kuşkulu genitalya (ambigus genitalya) ile doğan, gonadları ele gelmeyen, pelvik USG’de uterusu bulunan ve serum 17-hidroksiprogesteron düzeyi yüksek saptanan 46,XX bebekte tanı nedir?',
        c: '21-hidroksilaz (CYP21A2) eksikliğine bağlı Konjenital Adrenal Hiperplazi (yenidoğanda ambigus genitalyanın en sık nedeni).',
        k: 'g03:60',
      },
      {
        id: 'gqa-202',
        kalip: 'sendrom',
        s: '16 yaşında primer amenore ile başvuran, meme gelişimi normal dişi görünümde olan ancak aksiller/pubik kıllanması bulunmayan, kör vajeni olan, uterusu izlenmeyen 46,XY hastada tanı nedir?',
        c: 'Komplet Androjen Duyarsızlık Sendromu (Testiküler feminizasyon — Xq11-12 AR gen mutasyonu). Sertoli hücreleri AMH salgıladığı için uterus gelişmemiş, AR direnci nedeniyle Wolff yapıları da oluşmamıştır.',
        k: 'g03:56',
      },
      {
        id: 'gqa-203',
        kalip: 'sendrom',
        s: 'Doğumda ambigus genitalya nedeniyle kız yetiştirilen 46,XY bireyde pubertede ses kalınlaşması ve fallus büyümesi gelişiyorsa, testosteron normal iken DHT düşükse tanı ve en sık mutasyon nedir?',
        c: '5α-redüktaz 2 enzim eksikliği (Otozomal resesif, SRD5A2 geninde en sık p.L55Q mutasyonu).',
        k: 'g03:53',
      },
      {
        id: 'gqa-204',
        kalip: 'sendrom',
        s: 'Hangi 46,XY cinsiyet gelişim bozukluğunda AMH üretilemediği için uterus ve fallop tüpleri mevcuttur ve hasta yenidoğanda ambigus genitalya göstermeyip pubertede primer amenore ile başvurur?',
        c: 'Swyer sendromu (46,XY saf gonadal disgenezi).',
        k: 'g03:48',
      },
    ],
    sorular: [
      {
        id: 'gq-cikmis-201',
        tur: 'cikmis',
        yil: '2024-2025',
        kalip: 'sendrom',
        ders: 'g03',
        soru: '46,XX cinsiyet gelişim bozukluğu (CGB) bulunan bir hastada serum 17-hidroksiprogesteron düzeyi yüksek saptanıyor. En olası tanı aşağıdakilerden hangisidir?',
        secenekler: {
          A: '5α-redüktaz 2 enzim eksikliği',
          B: 'Komplet androjen duyarsızlık sendromu',
          C: 'Konjenital adrenal hiperplazi (21-hidroksilaz eksikliği)',
          D: 'Swyer sendromu (46,XY saf gonadal disgenezi)',
          E: 'Turner sendromu (45,X)',
        },
        dogru: 'C',
        aciklama: '46,XX CGB ve yenidoğan ambigus genitalya olgularının %90-95’inden 21-hidroksilaz (CYP21A2) eksikliğine bağlı konjenital adrenal hiperplazi sorumludur. Enzim bloğu öncesinde biriken 17-hidroksiprogesteron (17-OHP) tanı koydurucudur ve adrenal androjen artışına yol açarak dişi fetüsü virilize eder.',
        sikAciklamalari: {
          A: '5α-redüktaz 2 eksikliği 46,XY CGB nedenidir; testosteronun DHT’ye dönüşümü bozulur, 17-OHP düzeyi normaldir.',
          B: 'Komplet androjen duyarsızlık sendromu (Testiküler feminizasyon) 46,XY bireylerde X’e bağlı AR mutasyonu ile gelişir.',
          C: '21-hidroksilaz eksikliğine bağlı KAH, 46,XX bireylerde yüksek 17-OHP ve adrenal androjen fazlalığı ile kuşkulu genitalya yapan en sık nedendir.',
          D: 'Swyer sendromu 46,XY saf gonadal disgenezidir; adrenal steroidogenez normaldir ve 17-OHP yükselmez.',
          E: 'Turner sendromu 45,X gonozomal monozomisidir; çizgi gonad ve kısa boy yapar, ambigus genitalya ve 17-OHP yüksekliği beklenmez.',
        },
        k: 'g03:60',
      },
      {
        id: 'gq-cikmis-202',
        tur: 'cikmis',
        yil: '2023-2024',
        kalip: 'sendrom',
        ders: 'g03',
        soru: 'Testiküler feminizasyon sendromu (androjen duyarsızlığı sendromu) ile ilgili aşağıdakilerden hangisi yanlıştır?',
        secenekler: {
          A: 'Hastaların karyotipi 46,XY’dir.',
          B: 'X’e bağlı resesif kalıtılır ve androjen reseptör (AR) geninde mutasyon vardır.',
          C: 'Uterus ve fallop tüpleri bulunmaz, vajina kısa ve kör sonlanır.',
          D: 'Pubertede primer amenore ile başvururlar ve aksiller/pubik kıllanma yoktur.',
          E: 'Normal erkek meme yapısı vardır.',
        },
        dogru: 'E',
        aciklama: 'Testiküler feminizasyon (Komplet AIS) hastalarında testislerden salgılanan testosteron periferde aromataz enzimiyle östrojene dönüştürülür; androjen reseptörleri çalışmadığı için östrojen etkisi baskın kalır ve pubertede normal dişi meme gelişimi (telarş) görülür.',
        sikAciklamalari: {
          A: 'Komplet androjen duyarsızlık sendromu bir 46,XY cinsiyet gelişim bozukluğudur.',
          B: 'Hastalık Xq11-12 bölgesindeki androjen reseptör (AR) geninin inaktive edici mutasyonlarıyla X’e bağlı resesif kalıtılır.',
          C: 'Testislerdeki Sertoli hücreleri normal AMH salgıladığı için Müller kanalı yapıları (uterus ve üst vajen) geriler; alt vajen kısa ve kör sonlanır.',
          D: 'Uterus olmadığı için primer amenore görülür; androjen reseptör direnci nedeniyle pubik ve aksiller kıllanma gelişmez.',
          E: 'Hastalarda erkek tipi meme değil, testosteronun periferik aromatizasyonuyla oluşan östrojene bağlı normal dişi meme gelişimi vardır.',
        },
        k: 'g03:56',
      },
      {
        id: 'gq-cikmis-203',
        tur: 'cikmis',
        yil: '2021-2022',
        kalip: 'sendrom',
        ders: 'g03',
        soru: 'Yenidoğan döneminde aşağıdaki hastalıklardan hangisi ambigus genitalya ayırıcı tanısında yer almaz?',
        secenekler: {
          A: '21-hidroksilaz eksikliğine bağlı konjenital adrenal hiperplazi',
          B: '5α-redüktaz 2 enzim eksikliği',
          C: 'Swyer sendromu',
          D: 'Miks gonadal disgenezi (45,X/46,XY)',
          E: 'Parsiyel androjen duyarsızlık sendromu (Reifenstein sendromu)',
        },
        dogru: 'C',
        aciklama: 'Swyer sendromunda (46,XY saf gonadal disgenezi) gonadlar fibröz çizgi (streak) halindedir; ne AMH ne de testosteron üretilebilir. Androjen etkisi hiç olmadığı için dış genitalya tamamen normal dişi görünümündedir ve yenidoğanda ambigus genitalya oluşturmaz.',
        sikAciklamalari: {
          A: '21-hidroksilaz eksikliği 46,XX fetüste intrauterin virilizasyon yaparak yenidoğanda en sık ambigus genitalya tablosuna yol açar.',
          B: '5α-redüktaz 2 eksikliğinde DHT sentezlenemediği için 46,XY yenidoğanda perineoskrotal hipospadias ve kuşkulu genitalya görülür.',
          C: 'Swyer sendromunda (46,XY saf gonadal disgenezi) testosteron hiç üretilmediğinden dış genitalya tam dişidir; hasta pubertede primer amenore ile tanı alır.',
          D: 'Miks gonadal disgenezide (45,X/46,XY) tek taraflı disgenetik testis kısmi virilizasyon yaparak asimetrik ambigus genitalyaya neden olur.',
          E: 'Parsiyel androjen duyarsızlık sendromunda (PAIS) kısmi reseptör yanıtı nedeniyle yenidoğanda ambigus genitalya saptanır.',
        },
        k: 'g03:48',
      },
      {
        id: 'gq-cikmis-204',
        tur: 'cikmis',
        yil: '2022-2023',
        kalip: 'sendrom',
        ders: 'g03',
        soru: 'Aşağıdaki enzim defektlerinden hangisi hem 46,XY hem de 46,XX cinsiyet farklılaşma bozukluğu (DSD) etiyolojisinde yer alır?',
        secenekler: {
          A: '21-hidroksilaz enzim eksikliği',
          B: '11β-hidroksilaz enzim eksikliği',
          C: '5α-redüktaz 2 enzim eksikliği',
          D: '3β-hidroksisteroid dehidrogenaz enzim eksikliği',
          E: 'Aromataz enzim eksikliği',
        },
        dogru: 'D',
        aciklama: '3β-hidroksisteroid dehidrogenaz (3β-HSD) hem adrenal bezde hem de gonadda steroidogenezin erken basamağında görev yapar. Eksikliğinde 46,XY fetüste yeterli testosteron yapılamadığı için eksik virilizasyon, 46,XX fetüste ise biriken zayıf androjen olan DHEA nedeniyle hafif virilizasyon (ambigus genitalya) gelişir.',
        sikAciklamalari: {
          A: '21-hidroksilaz eksikliği yalnızca adrenal kortizol/aldosteron yolunu bozup androjenleri artırır; yalnız 46,XX DSD yapar.',
          B: '11β-hidroksilaz eksikliği adrenal androjen fazlalığı ve hipertansiyon yapar; yalnızca 46,XX DSD etiyolojisinde yer alır.',
          C: '5α-redüktaz 2 eksikliği dış genitalyada testosteronun DHT’ye dönüşümünü bozar; yalnızca 46,XY DSD nedenidir.',
          D: '3β-hidroksisteroid dehidrogenaz (ve POR) eksikliği hem 46,XY hem de 46,XX DSD etiyolojisinde yer alan ortak enzim defektidir.',
          E: 'Plasental aromataz eksikliği androjenlerin östrojene dönüşümünü bozarak yalnızca 46,XX fetüste virilizasyona yol açar.',
        },
        k: 'g03:62',
      },
      {
        id: 'gq-cikmis-205',
        tur: 'cikmis',
        yil: '2023-2024',
        kalip: 'sendrom',
        ders: 'g03',
        soru: 'Konjenital adrenal hiperplazi (KAH) riski taşıyan bir gebelikte fetal virilizasyonu engellemek amacıyla kullanılan steroid aşağıdakilerden hangisidir?',
        secenekler: {
          A: 'Hidrokortizon',
          B: 'Prednizolon',
          C: 'Fludrokortizon',
          D: 'Metilprednizolon',
          E: 'Deksametazon',
        },
        dogru: 'E',
        aciklama: 'Deksametazon plasental 11β-HSD2 enzimi tarafından inaktive edilmeden plasentayı geçerek fetal hipofizer ACTH salgısını baskılar. Gebeliğin 6-8. haftasında anneye başlanarak 46,XX KAH’lı kız fetüste dış genital virilizasyonu önler.',
        sikAciklamalari: {
          A: 'Hidrokortizon plasentada 11β-HSD2 ile yıkıldığı için fetüse geçemez; postnatal idame tedavisinde kullanılır.',
          B: 'Prednizolon plasentada büyük oranda inaktive edildiği için fetal adrenal aksı baskılamada etkisizdir.',
          C: 'Fludrokortizon tuz kaybettiren KAH’ta postnatal mineralokortikoid replasmanı için kullanılır.',
          D: 'Metilprednizolon maternal antiinflamatuvar tedavide kullanılır, fetal ACTH baskılamasında standart ajan değildir.',
          E: 'Deksametazon plasentadan aktif olarak fetüse geçer ve 6-8. haftada başlandığında fetal adrenal androjen üretimini baskılar.',
        },
        k: 'g03:67',
      },
      {
        id: 'gq-ornek-206',
        tur: 'ornek',
        kalip: 'sendrom',
        ders: 'g03',
        soru: 'Doğumda kuşkulu genitalya ve perineoskrotal hipospadias nedeniyle kız olarak yetiştirilen 46,XY karyotipli bir çocukta, pubertede ses kalınlaşması, kas kitlesinde artış, fallus büyümesi ve testislerin skrotuma inmesi gözleniyor. Laboratuvarda testosteron düzeyi normal, dihidrotestosteron (DHT) düzeyi düşük saptanan bu hastada en olası tanı ve kalıtım şekli hangisidir?',
        secenekler: {
          A: 'Komplet androjen duyarsızlık sendromu — X’e bağlı resesif',
          B: '5-alfa redüktaz 2 enzim eksikliği — Otozomal resesif',
          C: 'Swyer sendromu — Y’ye bağlı kalıtım',
          D: '21-hidroksilaz eksikliği — Otozomal resesif',
          E: 'Miks gonadal disgenezi — Otozomal dominant',
        },
        dogru: 'B',
        aciklama: 'Otozomal resesif kalıtılan 5α-redüktaz 2 (SRD5A2) eksikliğinde intrauterin dönemde DHT yapılamadığı için dış genitalya virilize olamaz; ancak pubertede yükselen testosteron doğrudan androjen reseptörlerini uyararak ses kalınlaşması, kas kitlesi artışı ve fallus büyümesi yapar.',
        sikAciklamalari: {
          A: 'Komplet AIS X’e bağlı resesif kalıtılır; reseptör direnci nedeniyle pubertede virilizasyon değil meme gelişimi görülür.',
          B: '5α-redüktaz 2 eksikliği otozomal resesif kalıtılır (en sık p.L55Q); T normal, DHT düşüktür ve pubertede virilizasyon gelişir.',
          C: 'Swyer sendromunda çizgi gonad vardır, testosteron üretilemez ve pubertede virilizasyon gelişmez.',
          D: '21-hidroksilaz eksikliği 46,XX bireylerde kuşkulu genitalya yapar; 46,XY bireylerde dış genitalya doğumda zaten normal erkektir.',
          E: 'Miks gonadal disgenezi 45,X/46,XY mozaikliği ile oluşur ve asimetrik gonad gelişimiyle karakterizedir.',
        },
        k: 'g03:53',
      },
    ],
  },

  /* ============================================================================
   * BÖLÜM 3 — KALIP 1C: KALITSAL KANSER SENDROMLARI (ÜROGENİTAL, MEME, OVER)
   * ============================================================================ */
  {
    id: 'sendrom-kanser-yatkinlik',
    ad: 'Kalıtsal Kanser Sendromları (Böbrek, Meme, Over, Endometriyum)',
    kisa: 'VHL, Birt-Hogg-Dubé, HLRCC, HPRC, BAP1, Tüberoz Skleroz, HBOC (BRCA1/2), Lynch, Peutz-Jeghers, Li-Fraumeni, Cowden, CDH1',
    kalip: 'sendrom',
    tablolar: [
      {
        id: 'gt-rcc-sendrom',
        baslik: 'Herediter Renal Hücreli Karsinom (RCC) Sendromları (%3; NCCN Tanı Yaşı ≤46 Yaş)',
        kalip: 'sendrom',
        sutun: ['Sendrom (hepsi OD)', 'Kromozom ve Gen (Protein)', 'Böbrek Tümörü Histolojisi ve Riski', 'Eşlik Eden Ekstrarenal Bulgular (Sorudaki İpucu)'],
        satir: [
          [
            'Von Hippel-Lindau Sendromu (VHLS)',
            '3p25.5 — VHL tümör süpresör geni',
            'Bilateral/multifokal Berrak Hücreli (Clear Cell) RCC (yaşam boyu %70 risk; en sık ölüm nedeni)',
            'Serebellar ve retinal hemanjioblastom, feokromositoma (%7), pankreas kistleri ve nöroendokrin tümör, iç kulak endolenfatik kese tümörü (ELST)',
          ],
          [
            'Birt-Hogg-Dubé Sendromu (BHDS)',
            '17p11.2 — FLCN geni (Folikülin proteini)',
            'Kromofob RCC, onkositom ve hibrit onkositik/kromofob böbrek tümörleri (%15-30)',
            'Yüz/boyunda kıl folikülü hamartomları (fibrofolikülom), bazal akciğer kistleri ve tekrarlayan spontan pnömotoraks öyküsü',
          ],
          [
            'Herediter Leiomyomatozis ve RCC (HLRCC)',
            '1q43 — FH geni (Fumarat hidrataz — Krebs döngüsü enzimi)',
            'Agresif seyirli, erken metastaz yapan Tip 2 Papiller RCC (%15-20)',
            'Çoklu kutanöz (deri) piloleiomyomlar ve kadınlarda erken yaşta semptomatik uterin leiomyomlar (myomlar)',
          ],
          [
            'Herediter Papiller Renal Karsinom (HPRC)',
            '7q31 — MET proto-onkogeni (ekzon 16-19 tirozin kinaz aktive edici mutasyon)',
            'Bilateral ve multifokal Tip 1 Papiller RCC (yüksek penetranlı)',
            'Genellikle böbreğe sınırlıdır; belirgin ekstrarenal bulgu beklenmez',
          ],
          [
            'BAP1 Tümör Yatkınlık Sendromu (BAP1-TPDS)',
            '3p21 — BAP1 tümör süpresör geni (deubikuitinaz)',
            'Agresif seyirli, yüksek dereceli Berrak Hücreli RCC (%10)',
            'Uveal (göz içi) melanom, malign mezotelyoma, kutanöz melanom ve bazal hücreli karsinom (BCC)',
          ],
          [
            'Tüberoz Skleroz Kompleksi (TSC)',
            '9q34 TSC1 (Hamartin) ve 16p13.3 TSC2 (Tüberin)',
            'Bilateral multifokal renal anjiyomiyolipom (%70-80), renal kistler ve %1-3 RCC',
            'Beyin kortikal tüberleri/SEGA (dirençli epilepsi), kalp rabdomiyomu, fasiyal anjiyofibrom, akciğer lenfanjiyoleyomiyomatozisi; mTOR yolağı aşırı aktiftir',
          ],
        ],
        k: ['g04:8-21'],
      },
      {
        id: 'gt-meme-over-endometriyum-sendrom',
        baslik: 'Meme, Over, Endometriyum ve Prostat Kanseri Kalıtsal Sendromları',
        kalip: 'sendrom',
        sutun: ['Sendrom ve Kalıtım', 'Sorumlu Genler ve Lokus', 'Kanser Riskleri ve Histolojik Tip', 'Ayırıcı Klinik Özellik ve Sınav İpucu'],
        satir: [
          [
            'Kalıtsal Meme-Over Kanseri (HBOC, OD)',
            'BRCA1 (17q21) ve BRCA2 (13q12.3) — homolog rekombinasyon DNA çift zincir kırık tamiri',
            'Meme ca (%50-80), Over ca (BRCA1 %40, BRCA2 %18; yüksek dereceli seröz — prekürsörü fallop tüpü), Prostat ve Pankreas ca',
            '<60 yaş triple-negatif (ER-, PR-, HER2-) meme kanserinde mutlaka BRCA1/2 bakılır; erkek meme kanserinde (%10 kalıtsal) BRCA2 ön plandadır',
          ],
          [
            'Lynch Sendromu (HNPCC, OD)',
            'MLH1, MSH2, MSH6, PMS2 ve EPCAM (DNA yanlış eşleşme tamiri — MMR genleri)',
            'Kolorektal ca, Endometriyal ca (70 yaşa kadar %39), Over ca (%10; endometrioid/berrak hücreli, erken evre), Ürotelyal ve Prostat ca',
            'Endometriyal ca riski EN YÜKSEK gen MSH6 (%26-71), EN DÜŞÜK gen PMS2 (%15); tümörde mikrosatellit instabilitesi (MSI-H) saptanır',
          ],
          [
            'Peutz-Jeghers Sendromu (PJS, OD)',
            '19p13.3 — STK11 (LKB1) tümör süpresör geni',
            'Meme ca (%55), Over ca (%21 — özellikle seks kord tümörü / SCTAT), Servikste Adenoma Malignum (%10), GİS/pankreas ca',
            'Gastrointestinal hamartomatöz polipozis + %95 mukokutanöz melanin pigmentasyonu (dudak, bukkal mukoza) + servikste adenoma malignum',
          ],
          [
            'Li-Fraumeni Sendromu (LFS, OD)',
            '17p13.1 — TP53 (“genomun koruyucusu”)',
            'Kadınlarda yaşam boyu ~%100 kanser riski; çok erken yaşta meme ca, yumuşak doku/osteosarkom, beyin tümörü, adrenokortikal karsinom, lösemi',
            'p53; G1/S kontrol noktası, DNA tamiri ve apoptozu yönetir; mutasyonunda kemoterapi/radyoterapiye direnç ve ikincil tümör riski artar',
          ],
          [
            'PTEN Hamartom Tümör (Cowden) Sendromu (OD)',
            '10q23.3 — PTEN fosfataz geni (PI3K/AKT/mTOR baskılayıcısı)',
            'Kadınlarda yaşam boyu %85 meme kanseri riski, endometriyal karsinom (%28), foliküler tiroid karsinomu ve RCC',
            'Makrosefali, mukokutanöz trikolemmomlar, oral papillomlar ve tiroid/meme/endometriyum hamartomları ile seyreder',
          ],
          [
            'Herediter Diffüz Mide ve Lobüler Meme Ca (OD)',
            '16q22.1 — CDH1 geni (E-kadherin hücre adezyon proteini)',
            'Taşlı yüzük hücreli diffüz mide kanseri (%70) ve kadınlarda %60 İnvaziv Lobüler Meme Karsinomu',
            'İnvaziv duktal değil, spesifik olarak hücre kohezyon kaybıyla giden İnvaziv Lobüler Meme Kanseri ile ilişkilidir',
          ],
        ],
        k: ['g04:37-43', 'g04:51-71'],
      },
    ],
    spotlar: [
      { id: 'gs-301', kalip: 'sendrom', m: 'NCCN kılavuzuna göre **≤46 yaşında** renal hücreli karsinom (RCC) tanısı alan her hasta, tüm RCC’lerin **%3**’ünü oluşturan herediter RCC sendromları açısından genetik danışmaya yönlendirilmelidir.', k: 'g04:8' },
      { id: 'gs-302', kalip: 'sendrom', m: 'Serebellar/retinal **hemanjioblastom**, pankreas kistleri/NET, feokromositoma (%7) ve **%70 berrak hücreli RCC** ile gelen hastada **3p25.5 VHL** mutasyonuna bağlı **Von Hippel-Lindau sendromu** düşünülür.', k: 'g04:12' },
      { id: 'gs-303', kalip: 'sendrom', m: '**Kıl folikülü hamartomları (fibrofolikülom)**, bazal akciğer kistleri / **spontan pnömotoraks** ve **kromofob/onkositom** böbrek tümörü üçlüsüyle gelen hastada **17p11 FLCN (folikülin)** mutasyonuna bağlı **Birt-Hogg-Dubé sendromu** düşünülür.', k: 'g04:10' },
      { id: 'gs-304', kalip: 'sendrom', m: 'Deri ve uterusta çoklu **leiomyomlar** ile agresif **Tip 2 papiller RCC** birlikteliği **1q43 FH (fumarat hidrataz)** mutasyonuna bağlı **HLRCC**’yi; bilateral multifokal **Tip 1 papiller RCC** ise **7q31 MET** mutasyonuna bağlı **HPRC**’yi düşündürür.', k: 'g04:15' },
      { id: 'gs-305', kalip: 'sendrom', m: '**Uveal melanom, malign mezotelyoma**, kutanöz melanom, bazal hücreli karsinom ve agresif berrak hücreli RCC birlikteliği **3p21 BAP1 tümör yatkınlık sendromunu** düşündürür.', k: 'g04:16' },
      { id: 'gs-306', kalip: 'sendrom', m: 'Çoklu organ hamartomları, dirençli epilepsi ve **bilateral multifokal renal anjiyomiyolipom** ile gelen hastada **9q34 TSC1 (hamartin)** veya **16p13 TSC2 (tüberin)** mutasyonuna bağlı **Tüberoz Skleroz Kompleksi** düşünülür.', k: 'g04:19' },
      { id: 'gs-307', kalip: 'sendrom', m: 'GİS hamartomatöz polipozis, **%95 mukokutanöz pigmentasyon**, overyan seks kord tümörü, %55 meme ca ve servikste **%10 adenoma malignum** ile gelen hastada **STK11** mutasyonuna bağlı **Peutz-Jeghers sendromu** düşünülür.', k: 'g04:63' },
      { id: 'gs-308', kalip: 'sendrom', m: 'Kadınlarda yaşam boyu **%85 meme kanseri** riski oluşturan sendrom **PTEN (Cowden) sendromu**, **~%100 genel kanser** riski oluşturan sendrom **Li-Fraumeni (TP53)**, **%60 invaziv lobüler meme ca** yapan gen ise **CDH1**’dir.', k: 'g04:68' },
      { id: 'gs-309', kalip: 'sendrom', m: '**Lynch sendromunda** 70 yaşına kadar endometriyal kanser riski **%39** olup, endometriyal kanser açısından **en yüksek risk MSH6 (%26-71)**, **en düşük risk ise PMS2 (%15)** gen mutasyonundadır.', k: 'g04:51' },
    ],
    soruCevaplar: [
      {
        id: 'gqa-301',
        kalip: 'sendrom',
        s: 'Kıl folikülü hamartomları, akciğer kistleri / spontan pnömotoraks ve kromofob/onkositom tipi böbrek tümörü ile başvuran hastada hangi sendrom ve hangi gen düşünülür?',
        c: 'Birt-Hogg-Dubé sendromu (BHDS) — 17p11 bölgesindeki FLCN (folikülin) tümör süpresör geni.',
        k: 'g04:10',
      },
      {
        id: 'gqa-302',
        kalip: 'sendrom',
        s: 'Serebellar ve retinal hemanjioblastom, feokromositoma, pankreas kistleri ve %70 yaşam boyu berrak hücreli RCC riski taşıyan sendrom ve hedefe yönelik ilacı nedir?',
        c: 'Von Hippel-Lindau sendromu (3p25.5 VHL geni); ilişkili RCC tedavisinde HIF-2α inhibitörü Belzutifan kullanılır.',
        k: 'g04:12',
      },
      {
        id: 'gqa-303',
        kalip: 'sendrom',
        s: 'Gastrointestinal hamartomatöz polipler, %95 mukokutanöz pigmentasyon, overyan seks kord tümörü ve servikste %10 adenoma malignum gelişimiyle karakterize sendrom ve sorumlu gen nedir?',
        c: 'Peutz-Jeghers sendromu — STK11 (19p13.3) tümör süpresör geni.',
        k: 'g04:63',
      },
      {
        id: 'gqa-304',
        kalip: 'sendrom',
        s: 'Kalıtsal over kanserlerinde BRCA1/BRCA2 (HBOC) ilişkili tümörler ile Lynch sendromu ilişkili tümörlerin histopatolojik ve prekürsör farkı nedir?',
        c: 'BRCA1/2 pozitif olgularda yüksek dereceli seröz karsinom görülür ve prekürsör lezyonu fallop tüpüdür; Lynch sendromunda ise endometrioid veya berrak hücreli over karsinomu görülür ve tanı anında genellikle erken evrededir (Evre I/II).',
        k: 'g04:62',
      },
    ],
    sorular: [
      {
        id: 'gq-ornek-301',
        tur: 'ornek',
        kalip: 'sendrom',
        ders: 'g04',
        soru: 'Kıl folikülü hamartomları (benign deri tümörleri), akciğer kistleri ve spontan pnömotoraks öyküsü ile çeşitli böbrek tümörleri (kromofob, onkositom) üçlüsüyle karakterize olan, 17p11’deki FLCN (folikülin) gen mutasyonu sonucu gelişen otozomal dominant sendrom hangisidir?',
        secenekler: {
          A: 'Von Hippel-Lindau sendromu (VHLS)',
          B: 'Birt-Hogg-Dubé sendromu (BHDS)',
          C: 'Herediter leiomyomatozis ve renal hücreli kanser (HLRCC)',
          D: 'Herediter papiller renal karsinom (HPRC)',
          E: 'Tüberoz skleroz kompleksi (TSC)',
        },
        dogru: 'B',
        aciklama: '17p11’deki FLCN (folikülin) gen mutasyonu sonucu gelişen Birt-Hogg-Dubé sendromu; fibrofolikülomlar (kıl folikülü hamartomu), bazal akciğer kistleri / spontan pnömotoraks ve kromofob/onkositom böbrek tümörleri üçlüsü ile tanı alır.',
        sikAciklamalari: {
          A: 'Von Hippel-Lindau sendromu 3p25.5 VHL mutasyonu ile oluşur; hemanjioblastom, feokromositoma ve berrak hücreli RCC yapar.',
          B: 'Birt-Hogg-Dubé sendromu 17p11 FLCN mutasyonu ile oluşur; deri fibrofolikülomları, spontan pnömotoraks ve kromofob/onkositom böbrek tümörü yapar.',
          C: 'HLRCC 1q43 fumarat hidrataz (FH) mutasyonu ile oluşur; deri/uterus leiomyomları ve agresif Tip 2 papiller RCC ile seyreder.',
          D: 'HPRC 7q31 MET proto-onkogen mutasyonu ile oluşur ve bilateral multifokal Tip 1 papiller RCC yapar.',
          E: 'Tüberoz skleroz kompleksi TSC1/TSC2 mutasyonu ile oluşur; kortikal tüber, anjiyofibrom ve bilateral renal anjiyomiyolipom yapar.',
        },
        k: 'g04:10',
      },
      {
        id: 'gq-ornek-302',
        tur: 'ornek',
        kalip: 'sendrom',
        ders: 'g04',
        soru: 'Otozomal dominant kalıtılan, STK11 gen mutasyonu sonucu gastrointestinal hamartomatöz polipozis, mukokutanöz lezyonlar (%95), overyan seks kord tümörü ve %10 yaşam boyu riskle servikste “adenoma malignum” gelişimine yol açan sendrom hangisidir?',
        secenekler: {
          A: 'Peutz-Jeghers sendromu',
          B: 'Cowden sendromu (PTEN hamartom tümör sendromu)',
          C: 'Li-Fraumeni sendromu',
          D: 'Lynch sendromu',
          E: 'BAP1 tümör yatkınlık sendromu',
        },
        dogru: 'A',
        aciklama: 'STK11 (19p13.3) mutasyonu ile gelişen Peutz-Jeghers sendromu; GİS hamartomatöz polipleri, %95 mukokutanöz pigmentasyon, %55 meme kanseri, %21 over tümörü (seks kord tümörü) ve %10 servikal adenoma malignum riski ile karakterizedir.',
        sikAciklamalari: {
          A: 'Peutz-Jeghers sendromu STK11 mutasyonu sonucu gelişir ve mukokutanöz pigmentasyon, GİS hamartomları ile serviks adenoma malignumuna yol açar.',
          B: 'Cowden sendromu PTEN mutasyonu sonucu gelişir; makrosefali, trikolemmomlar ve %85 meme kanseri riski taşır.',
          C: 'Li-Fraumeni sendromu TP53 mutasyonu sonucu gelişir; sarkom, beyin tümörü, meme ca ve adrenokortikal karsinom ile ~%100 kanser riski taşır.',
          D: 'Lynch sendromu MMR gen (MLH1, MSH2, MSH6, PMS2) mutasyonları sonucu gelişir; kolorektal ve endometriyal kanserle seyreder.',
          E: 'BAP1 tümör yatkınlık sendromu uveal melanom, malign mezotelyoma ve berrak hücreli RCC ile seyreder.',
        },
        k: 'g04:63',
      },
      {
        id: 'gq-ornek-303',
        tur: 'ornek',
        kalip: 'sendrom',
        ders: 'g04',
        soru: 'Kalıtsal over kanserlerinde BRCA1/BRCA2 (HBOC) pozitif olgular ile Lynch sendromu ilişkili olguların karşılaştırılmasıyla ilgili aşağıdakilerden hangisi doğrudur?',
        secenekler: {
          A: 'Lynch sendromunda over kanserlerinin tamamı fallop tüpü kökenli yüksek dereceli seröz karsinomdur.',
          B: 'BRCA2 mutasyonu taşıyıcılarında over kanseri riski meme kanseri riskinden daha yüksektir.',
          C: 'BRCA1/2 pozitif olgularda yüksek dereceli seröz karsinom ve fallop tüpü prekürsörü görülür.',
          D: 'BRCA1/2 ilişkili over kanserleri her zaman Evre I’de yakalanır ve berrak hücreli histolojidedir.',
          E: 'Lynch sendromunda over kanseri gelişme riski (%85), endometriyal kanser riskinden (%10) çok daha yüksektir.',
        },
        dogru: 'C',
        aciklama: 'BRCA1/BRCA2 pozitif kalıtsal meme-over kanseri (HBOC) olgularında gelişen over tümörleri tipik olarak yüksek dereceli seröz adenokarsinomdur ve prekürsör lezyonu fallop tüpü fimbrial ucundaki seröz tubal intraepitelyal karsinomdur (STIC).',
        sikAciklamalari: {
          A: 'Fallop tüpü kökenli yüksek dereceli seröz karsinom Lynch sendromunun değil, BRCA1/2 (HBOC) olgularının özelliğidir.',
          B: 'BRCA1 ve BRCA2 taşıyıcılarının her ikisinde de meme kanseri riski (%50-80), over kanseri riskinden (%18-40) belirgin olarak daha yüksektir.',
          C: 'BRCA1/2 pozitif olgularda yüksek dereceli seröz histoloji ve fallop tüpü prekürsörü görülür; bu nedenle profilaktik salpingo-ooferektomi önerilir.',
          D: 'Erken evre (Evre I/II) ve endometrioid/berrak hücreli non-seröz histoloji BRCA1/2’nin değil, Lynch sendromu ilişkili over kanserlerinin özelliğidir.',
          E: 'Lynch sendromunda 70 yaşına kadar endometriyal kanser riski %39 iken over kanseri riski yaklaşık %10’dur.',
        },
        k: 'g04:62',
      },
    ],
  },

  /* ============================================================================
   * BÖLÜM 4 — KALIP 2: KANSER TÜRLERİNDE BELİRLİ İLAÇ TEDAVİLERİ
   * ============================================================================ */
  {
    id: 'kanser-ilac-tedavileri',
    ad: 'Kanser Türlerinde Belirli İlaç Tedavileri (Meme, Over, Mesane, Prostat, Böbrek, Endometriyum)',
    kisa: 'PARP inh. (Olaparib, Rucaparib), Erdafitinib (FGFR2/3), Belzutifan (VHL), mTOR inh. (TSC), Trastuzumab (HER2), Lenvatinib, Kabozantinib, Aksitinib, PD-1/PD-L1',
    kalip: 'ilac',
    tablolar: [
      {
        id: 'gt-kanser-hedef-ilac',
        baslik: 'Meme, Over, Prostat ve Mesane Kanserlerinde Genetik Hedefler ve Spesifik İlaç Tedavileri',
        kalip: 'ilac',
        sutun: ['Kanser Türü', 'Genetik / Moleküler Biyobelirteç', 'Spesifik Hedefe Yönelik İlaç(lar)', 'Etki Mekanizması ve Klinik / Sınav Notu'],
        satir: [
          [
            'Meme ve Over Kanseri',
            'BRCA1, BRCA2, ATM veya PTEN mutasyonu (Homolog rekombinasyon tamir [HRR] defekti)',
            'PARP İnhibitörleri (Olaparib, Rucaparib)',
            'PARP enzimi tek zincir kırık tamirini yapar; BRCA mutant hücrede PARP inhibisyonu çift zincir kırıklarının birikmesiyle “Sentetik Letalite” üzerinden tümör hücresini öldürür (Çıkmış Soru)',
          ],
          [
            'Prostat Kanseri (mCRPC)',
            'HRR gen mutasyonu (en sık BRCA2 ve ATM; ayrıca BRCA1, PALB2, CHEK2)',
            'Olaparib ve Rucaparib (PARP inhibitörleri — Mayıs 2020 FDA onaylı)',
            'Somatik veya germline HRR mutasyonu pozitif metastatik kastrasyona dirençli prostat kanserinde sağkalımı uzatır',
          ],
          [
            'Prostat Kanseri (CDK12 Mutant Alt Grup)',
            'CDK12 biallelik inaktivasyonu',
            'PD-1 İnhibitörleri (Nivolumab, Pembrolizumab)',
            'KRİTİK İSTİSNA: CDK12 mutasyonu olan prostat kanseri hormonal tedaviye, taksanlara ve PARP inhibitörlerine DİRENÇLİDİR; yüksek neoantijen yükü nedeniyle anti-PD-1 immünoterapiye yanıt verebilir',
          ],
          [
            'Mesane Kanseri (İleri Evre / Metastatik Ürotelyal Ca)',
            'FGFR2 veya FGFR3 gen mutasyonu / füzyonu',
            'Erdafitinib (Pan-FGFR tirozin kinaz inhibitörü)',
            'Platin bazlı kemoterapi sonrası progrese olan veya Evre IVA/IVB metastatik FGFR2/FGFR3 mutant mesane kanserinin spesifik hedef ilacıdır',
          ],
          [
            'Mesane Kanseri (İmmünoterapi)',
            'PD-L1 ekspresyonu / platin uygunsuz veya dirençli ileri ürotelyal karsinom',
            'Avelumab, Pembrolizumab, Atezolizumab, Nivolumab',
            'PD-1 / PD-L1 immün kontrol noktası inhibitörleri ileri evre mesane kanserinde idame ve kurtarma tedavisinde kullanılır',
          ],
        ],
        k: ['g04:30-31', 'g04:44', 'g04:69'],
      },
      {
        id: 'gt-rcc-endometriyum-ilac',
        baslik: 'Böbrek (RCC / VHL / TSC) ve Endometriyum Kanserlerinde Hedefe Yönelik İlaç Tedavileri',
        kalip: 'ilac',
        sutun: ['Kanser / Sendrom', 'Moleküler Hedef / Alt Grup', 'Hedefe Yönelik İlaç veya Kombinasyon', 'Moleküler Mekanizma ve Sınav Vurgusu'],
        satir: [
          [
            'Von Hippel-Lindau (VHL) İlişkili RCC',
            '3p25.5 VHL mutasyonu → HIF-2α birikimi',
            'Belzutifan (Ağustos 2021 FDA onaylı)',
            'HIF-2α inhibitörüdür; acil cerrahi gerektirmeyen VHL ilişkili RCC, SSS hemanjioblastomu ve pankreas NET tedavisinde onaylı spesifik ilaçtır',
          ],
          [
            'Tüberoz Skleroz Kompleksi (TSC)',
            'TSC1 (Hamartin) veya TSC2 (Tüberin) kaybı → mTOR aktivasyonu',
            'mTOR İnhibitörleri (Sirolimus, Everolimus) + Dirençli epilepside Ketojenik Diyet',
            'Hamartin-tüberin kompleksi normalde mTOR’u baskılar; mutasyonunda aşırı çalışan mTOR yolağı renal anjiyomiyolipom ve SEGA’da mTOR inhibitörleriyle hedeflenir',
          ],
          [
            'İleri Evre Berrak Hücreli RCC (1. Basamak TKI + İmmünoterapi)',
            'VEGFR / MET / AXL / FGFR tirozin kinazlar + PD-1 / PD-L1 / CTLA-4',
            '1) Aksitinib + Pembrolizumab (veya Avelumab)\n2) Kabozantinib + Nivolumab\n3) Lenvatinib + Pembrolizumab\n4) İpilimumab + Nivolumab',
            'Aksitinib: selektif VEGFR 1-3 TKI; Kabozantinib: VEGFR + MET + AXL TKI; Lenvatinib: VEGFR + FGFR + PDGFRα + KIT + RET çok hedefli TKI; İpilimumab: anti-CTLA-4',
          ],
          [
            'Endometriyum Kanseri — HER2 Pozitif Seröz Ca',
            'HER2 (ERBB2) amplifikasyonu / aşırı ekspresyonu (Evre III/IV uterin seröz ca ve karsinosarkom)',
            'Karboplatin + Paklitaksel + Trastuzumab',
            'İleri evre veya rekürren HER2-pozitif uterin seröz karsinomda kemoterapiye anti-HER2 antikor Trastuzumab eklenmesi sağkalımı belirgin artırır',
          ],
          [
            'Endometriyum Kanseri — dMMR / MSI-H vs. pMMR',
            'dMMR / MSI-H / TMB-H (Yüksek mutasyon yükü) vs. pMMR (MMR sağlam)',
            'dMMR/MSI-H: Pembrolizumab, Dostarlimab-gxly, Avelumab, Nivolumab\npMMR: Lenvatinib + Pembrolizumab',
            'MMR eksikliği varsa tek başına anti-PD-1/PD-L1 etkilidir; MMR sağlamsa (pMMR) immünoterapiye çok hedefli TKI Lenvatinib eklenir',
          ],
          [
            'Endometriyum Kanseri — NTRK Füzyonu ve Hormonoterapi',
            'NTRK1/2/3 gen füzyonu pozitif tümörler; düşük dereceli ER/PR+ tümörler',
            'NTRK+: Larotrektinib veya Entrektinib\nHormonal: Megestrol asetat / Tamoksifen, Everolimus + Letrozol',
            'Dikkat: Meme kanseri tedavisinde kullanılan selektif östrojen reseptör modülatörü Tamoksifen, endometriyum üzerinde agonist etkiyle endometriyal kanser riskini artırır',
          ],
        ],
        k: ['g04:20-25', 'g04:56-58'],
      },
    ],
    spotlar: [
      { id: 'gs-401', kalip: 'ilac', m: '**BRCA1, BRCA2, ATM veya PTEN** mutasyonu taşıyan **meme, over ve prostat** kanserlerinde **PARP inhibitörleri (Olaparib, Rucaparib)** DNA tek zincir kırık tamirini bloke ederek **sentetik letalite** mekanizmasıyla tümör hücresini öldürür.', k: 'g04:69' },
      { id: 'gs-402', kalip: 'ilac', m: '**Mesane kanserinde** Evre IVA/IVB veya kemoterapi sonrası progrese hastalarda **FGFR2 veya FGFR3 mutasyonu** saptandığında spesifik hedefe yönelik ilaç olarak pan-FGFR inhibitörü **Erdafitinib** kullanılır.', k: 'g04:31' },
      { id: 'gs-403', kalip: 'ilac', m: 'İleri evre **mesane kanserinde** kullanılan PD-1 / PD-L1 immün kontrol noktası inhibitörleri **Avelumab, Pembrolizumab, Atezolizumab ve Nivolumab**’dır.', k: 'g04:31' },
      { id: 'gs-404', kalip: 'ilac', m: '**Prostat kanserinde** HRR mutasyonlarında (BRCA1/2, ATM) **Olaparib ve Rucaparib** etkiliyken; **CDK12 mutasyonu** olan prostat kanserleri PARP inhibitörlerine ve hormon tedavisine **dirençlidir** (bu hastalarda **PD-1 inhibitörleri** denenir).', k: 'g04:44' },
      { id: 'gs-405', kalip: 'ilac', m: '**Von Hippel-Lindau (VHL) sendromu** ile ilişkili renal hücreli karsinom (RCC) olgularının tedavisinde Ağustos 2021 FDA onayı alan spesifik ilaç **Belzutifan**’dır.', k: 'g04:21' },
      { id: 'gs-406', kalip: 'ilac', m: '**Tüberoz Skleroz Kompleksinde (TSC1/TSC2)** hamartin-tüberin kaybına bağlı aşırı aktifleşen mTOR yolağını baskılamak için **mTOR inhibitörleri (Sirolimus, Everolimus)** kullanılır.', k: 'g04:20' },
      { id: 'gs-407', kalip: 'ilac', m: 'İleri evre **berrak hücreli RCC** birinci basamak tedavisinde **Aksitinib** (VEGFR TKI) + **Pembrolizumab/Avelumab**; **Kabozantinib** (VEGFR/MET/AXL TKI) + **Nivolumab**; **Lenvatinib** (çok hedefli TKI) + **Pembrolizumab** ve **İpilimumab + Nivolumab** kombinasyonları kullanılır.', k: 'g04:22' },
      { id: 'gs-408', kalip: 'ilac', m: '**Endometriyum kanserinde** **HER2-pozitif** uterin seröz karsinomda kemoterapiye **Trastuzumab** eklenir; **NTRK füzyonu** pozitif tümörlerde **Larotrektinib / Entrektinib**; **dMMR/MSI-H** tümörlerde **Pembrolizumab / Dostarlimab**; **pMMR** tümörlerde ise **Lenvatinib + Pembrolizumab** kullanılır.', k: 'g04:57' },
    ],
    soruCevaplar: [
      {
        id: 'gqa-401',
        kalip: 'ilac',
        s: 'Meme, over ve prostat kanserlerinde BRCA1/BRCA2 mutasyonu varlığında hangi hedefe yönelik ilaç grubu kullanılır ve hücre ölüm mekanizması nedir?',
        c: 'PARP inhibitörleri (Olaparib, Rucaparib) kullanılır; homolog rekombinasyon bozukken tek zincir tamirini de durdurarak Sentetik Letalite ile tümör hücresini apoptoza götürür.',
        k: 'g04:69',
      },
      {
        id: 'gqa-402',
        kalip: 'ilac',
        s: 'İleri evre veya kemoterapi sonrası progrese mesane kanserinde FGFR2 veya FGFR3 mutasyonu saptandığında hangi spesifik hedefe yönelik ilaç verilir?',
        c: 'Erdafitinib (pan-FGFR tirozin kinaz inhibitörü).',
        k: 'g04:31',
      },
      {
        id: 'gqa-403',
        kalip: 'ilac',
        s: 'Prostat kanserinde hangi gen mutasyonu PARP inhibitörlerine, hormonal tedaviye ve taksanlara zayıf yanıt (direnç) ile ilişkili olup anti-PD-1 immünoterapiye adaydır?',
        c: 'CDK12 mutasyonu.',
        k: 'g04:44',
      },
      {
        id: 'gqa-404',
        kalip: 'ilac',
        s: 'VHL sendromu ilişkili böbrek tümörlerinde (RCC) ve Tüberoz Skleroz Kompleksinde (TSC) kullanılan hedefe yönelik ilaçlar sırasıyla hangileridir?',
        c: 'VHL ilişkili RCC’de Belzutifan; Tüberoz Skleroz Kompleksinde mTOR inhibitörleri (Sirolimus / Everolimus).',
        k: 'g04:20-21',
      },
      {
        id: 'gqa-405',
        kalip: 'ilac',
        s: 'Endometriyum kanserinde HER2+ seröz karsinomda, NTRK füzyonunda ve pMMR (MMR sağlam) rekürren hastalıkta kullanılan hedef tedaviler nelerdir?',
        c: 'HER2+ seröz ca: Trastuzumab (+ Karboplatin/Paklitaksel); NTRK füzyonu: Larotrektinib veya Entrektinib; pMMR rekürren ca: Lenvatinib + Pembrolizumab.',
        k: 'g04:56-58',
      },
    ],
    sorular: [
      {
        id: 'gq-cikmis-401',
        tur: 'cikmis',
        yil: '2023-2024',
        kalip: 'ilac',
        ders: 'g04',
        soru: 'Meme-over kanseri olgularında özellikle BRCA mutasyonu bulunan hastalarda sıklıkla kullanılan hedefe yönelik (akıllı) ilaç grubu aşağıdakilerden hangisidir?',
        secenekler: {
          A: 'mTOR inhibitörleri',
          B: 'PARP inhibitörleri',
          C: 'BCR-ABL tirozin kinaz inhibitörleri',
          D: 'Anti-CD20 monoklonal antikorları',
          E: 'HIF-2α inhibitörleri',
        },
        dogru: 'B',
        aciklama: 'BRCA1 ve BRCA2 genleri çift zincir DNA kırıklarının homolog rekombinasyonla tamirinden sorumludur. Bu genlerde mutasyon taşıyan meme, over ve prostat kanseri hastalarında tek zincir DNA tamir enzimi olan PARP’ı bloke eden PARP inhibitörleri (Olaparib, Rucaparib) sentetik letalite oluşturarak tümör hücrelerini seçici olarak öldürür.',
        sikAciklamalari: {
          A: 'mTOR inhibitörleri (Sirolimus, Everolimus) TSC1/TSC2 mutasyonlu Tüberoz Skleroz Kompleksinde ve hormon reseptörü pozitif dirençli tümörlerde kullanılır.',
          B: 'PARP inhibitörleri (Olaparib, Rucaparib) BRCA1/2 ve ATM/PTEN mutant meme, over ve prostat kanserlerinde sentetik letalite sağlayan temel hedef ilaç grubudur.',
          C: 'BCR-ABL tirozin kinaz inhibitörleri (İmatinib vb.) t(9;22) Philadelphia kromozomu pozitif kronik miyeloid lösemide kullanılır.',
          D: 'Anti-CD20 monoklonal antikorları (Rituksimab) B hücreli lenfoma ve otoimmün hastalıkların tedavisinde kullanılır.',
          E: 'HIF-2α inhibitörü (Belzutifan) 3p25.5 VHL mutasyonu bulunan Von Hippel-Lindau sendromu ilişkili RCC olgularında kullanılır.',
        },
        k: 'g04:69',
      },
      {
        id: 'gq-ornek-402',
        tur: 'ornek',
        kalip: 'ilac',
        ders: 'g04',
        soru: 'Prostat kanserinde PARP inhibitörlerine ve hormonal tedaviye zayıf yanıtla ilişkili olan gen mutasyonu hangisidir?',
        secenekler: {
          A: 'BRCA2 mutasyonu',
          B: 'ATM mutasyonu',
          C: 'BRCA1 mutasyonu',
          D: 'CDK12 mutasyonu',
          E: 'PALB2 mutasyonu',
        },
        dogru: 'D',
        aciklama: 'Prostat kanserinde BRCA1, BRCA2, ATM ve PALB2 gibi klasik HRR gen mutasyonları PARP inhibitörlerine (Olaparib, Rucaparib) duyarlılık sağlarken; CDK12 mutasyonu bulunan prostat kanserleri hormonal tedaviye, taksanlara ve PARP inhibitörlerine zayıf yanıt verir (bu olgularda PD-1 inhibitörleri nivolumab/pembrolizumab tercih edilir).',
        sikAciklamalari: {
          A: 'BRCA2 mutasyonu prostat kanserinde en sık saptanan HRR defektidir ve PARP inhibitörlerine yüksek duyarlılık sağlar.',
          B: 'ATM mutasyonu DNA hasar yanıtında görev alır ve prostat kanserinde PARP inhibitörü endikasyonları arasındadır.',
          C: 'BRCA1 mutasyonu homolog rekombinasyon eksikliği yaparak PARP inhibitörlerine duyarlılık oluşturur.',
          D: 'CDK12 mutasyonu agresif seyir, hormonal tedaviye ve PARP inhibitörlerine direnç ile ilişkilidir; anti-PD-1 immünoterapiye yanıt verebilir.',
          E: 'PALB2, BRCA2 ile birlikte çalışan bir HRR genidir ve mutasyonunda PARP inhibitörlerine yanıt beklenir.',
        },
        k: 'g04:44',
      },
      {
        id: 'gq-ornek-403',
        tur: 'ornek',
        kalip: 'ilac',
        ders: 'g04',
        soru: 'Yirmi altı yaşında bir hastada serebellar ve retinal hemanjioblastom, pankreas kistleri ve bilateral berrak hücreli renal hücreli karsinom saptanıyor. Hastada 3p25.5 bölgesinde yer alan tümör süpresör gende germline mutasyon tespit ediliyor. Bu sendromla ilgili aşağıdakilerden hangisi yanlıştır?',
        secenekler: {
          A: 'Otozomal dominant kalıtılan Von Hippel-Lindau sendromudur.',
          B: 'Taşıyıcılarda yaşam boyu berrak hücreli RCC gelişme riski yaklaşık %70’tir.',
          C: 'İlişkili RCC olgularının tedavisinde spesifik olarak erdafitinib onay almıştır.',
          D: 'Olguların yaklaşık %7’sinde feokromositoma gelişir.',
          E: 'İlişkili RCC tedavisinde Ağustos 2021’de belzutifan FDA onayı almıştır.',
        },
        dogru: 'C',
        aciklama: 'Tarif edilen tablo 3p25.5 VHL mutasyonuna bağlı Von Hippel-Lindau sendromudur. VHL ilişkili RCC tedavisinde onay alan spesifik ilaç Belzutifan’dır. Erdafitinib ise FGFR2/FGFR3 mutasyonu pozitif ileri evre mesane kanserinde kullanılan ilaçtır.',
        sikAciklamalari: {
          A: '3p25.5 VHL mutasyonu otozomal dominant kalıtılan Von Hippel-Lindau sendromuna yol açar.',
          B: 'VHL sendromunda berrak hücreli RCC yaşam boyu %70 oranında gelişir ve en önemli mortalite nedenidir.',
          C: 'Erdafitinib VHL ilişkili böbrek kanserinde değil, FGFR2/FGFR3 mutant ileri evre mesane kanserinde onaylıdır.',
          D: 'VHL sendromlu hastaların yaklaşık %7’sinde adrenal medullada feokromositoma görülür.',
          E: 'VHL ilişkili RCC, SSS hemanjioblastomu ve pankreas NET tedavisinde HIF-2α inhibitörü Belzutifan FDA onayı almıştır.',
        },
        k: 'g04:12,21',
      },
      {
        id: 'gq-ornek-404',
        tur: 'ornek',
        kalip: 'ilac',
        ders: 'g04',
        soru: 'Rekürren veya metastatik endometriyal karsinomda moleküler biyobelirteç sonuçlarına göre seçilen hedefe yönelik tedavilerle ilgili aşağıdaki eşleştirmelerden hangisi yanlıştır?',
        secenekler: {
          A: 'HER2-pozitif uterin seröz karsinom — Karboplatin/Paklitaksel + Trastuzumab',
          B: 'dMMR / MSI-H tümörler — Pembrolizumab veya Dostarlimab',
          C: 'pMMR (MMR sağlam) rekürren tümörler — Lenvatinib + Pembrolizumab',
          D: 'NTRK gen füzyonu pozitif tümörler — Larotrektinib veya Entrektinib',
          E: 'POLE mutasyonu pozitif erken evre tümörler — Belzutifan monoterapisi',
        },
        dogru: 'E',
        aciklama: 'POLE mutasyonu pozitif endometriyal karsinomlar en iyi prognozlu moleküler alt gruptur ve Belzutifan (VHL ilişkili RCC ilacı) ile tedavi edilmez. Diğer dört şıktaki biyobelirteç-ilaç eşleştirmeleri endometriyum kanseri tedavisinin doğrudan slayt bilgisidir.',
        sikAciklamalari: {
          A: 'Evre III/IV veya rekürren HER2-pozitif uterin seröz karsinom ve karsinosarkomda kemoterapiye Trastuzumab eklenir.',
          B: 'Yanlış eşleşme tamiri eksikliği (dMMR / MSI-H) veya TMB-H olan endometriyal kanserlerde Pembrolizumab ve Dostarlimab kullanılır.',
          C: 'MMR sistemi sağlam (pMMR) olan rekürren endometriyal karsinomda çok hedefli TKI Lenvatinib ile Pembrolizumab kombine edilir.',
          D: 'NTRK gen füzyonu taşıyan metastatik endometriyal karsinomlarda TRK inhibitörleri Larotrektinib veya Entrektinib kullanılır.',
          E: 'Belzutifan VHL ilişkili RCC ilacıdır; POLE mutant endometriyal karsinom ise en iyi prognozlu grup olup Belzutifan endikasyonu yoktur.',
        },
        k: 'g04:56-58',
      },
      {
        id: 'gq-ornek-405',
        tur: 'ornek',
        kalip: 'ilac',
        ders: 'g04',
        soru: 'İleri evre berrak hücreli renal hücreli karsinom (ccRCC) birinci basamak tedavisinde kullanılan ilaçlar ve moleküler hedefleri ile ilgili aşağıdaki eşleştirmelerden hangisi yanlıştır?',
        secenekler: {
          A: 'Aksitinib — VEGFR 1, 2 ve 3 selektif tirozin kinaz inhibitörü',
          B: 'Kabozantinib — VEGFR, MET ve AXL tirozin kinaz inhibitörü',
          C: 'İpilimumab — CTLA-4’e bağlanarak CD80/CD86 etkileşimini bloke eden antikor',
          D: 'Lenvatinib — Yalnızca östrojen reseptörünü bloke eden modülatör',
          E: 'Nivolumab / Pembrolizumab — PD-1 immün kontrol noktası inhibitörleri',
        },
        dogru: 'D',
        aciklama: 'Lenvatinib bir östrojen reseptör modülatörü değil; VEGFR 1-3, FGFR 1-4, PDGFR-α, c-KIT ve RET reseptörlerini eşzamanlı inhibe eden çok hedefli bir tirozin kinaz inhibitörüdür ve hem ccRCC hem de endometriyum kanserinde Pembrolizumab ile kombine kullanılır.',
        sikAciklamalari: {
          A: 'Aksitinib, VEGFR 1-3’ü selektif inhibe eder ve ccRCC 1. basamakta Pembrolizumab veya Avelumab ile kombine edilir.',
          B: 'Kabozantinib; VEGFR yanı sıra MET ve AXL kinazları inhibe eder ve Nivolumab ile kombine kullanılır.',
          C: 'İpilimumab, T hücrelerindeki CTLA-4’ü bloke eden monoklonal antikordur ve Nivolumab ile kombine edilir.',
          D: 'Lenvatinib östrojen reseptör modülatörü değildir; VEGFR, FGFR, PDGFR-α, KIT ve RET’i hedefleyen çoklu tirozin kinaz inhibitörüdür.',
          E: 'Nivolumab ve Pembrolizumab anti-PD-1 antikorları olup ccRCC kombinasyonlarının temel immünoterapi bileşenleridir.',
        },
        k: 'g04:22-25',
      },
    ],
  },

  /* ============================================================================
   * BÖLÜM 5 — KALIP 3: SPESİFİK KANSER VE PRENATAL TANI BELİRTEÇLERİ
   * ============================================================================ */
  {
    id: 'kanser-prenatal-belirtecler',
    ad: 'Spesifik Kanser Belirteçleri ve Prenatal Tanı Belirteçleri',
    kisa: 'Testis (AFP, β-hCG, LDH), Mesane (FGFR3 iyi prognoz vs TP53/pRB/Ki67 kötü prognoz), Prostat panelleri, Endometriyum 4 grup (POLE vs p53), İkili/Üçlü/Dörtlü test',
    kalip: 'belirtec',
    tablolar: [
      {
        id: 'gt-kanser-belirtecler',
        baslik: 'Ürogenital ve Jinekolojik Kanserlerde Spesifik Serum, Doku ve Prognoz Belirteçleri',
        kalip: 'belirtec',
        sutun: ['Kanser Türü', 'Serum / Doku Belirteçleri', 'İyi Prognoz / Yüzeysel Belirteçler', 'Kötü Prognoz / Agresiflik / Nüks Belirteçleri'],
        satir: [
          [
            'Testis Germ Hücreli Tümörleri (TGCT)',
            'Serum üçlüsü: AFP + β-hCG + LDH (tanı, evreleme, prognoz ve tedavi takibinde birlikte kullanılır — Çıkmış Soru)',
            'Beş yıllık sağkalım >%95; seminom ve non-seminom olarak ikiye ayrılır',
            'Somatik genler: BCL10 (1p22.3), spermatositik seminomda FGFR3 (4p16.3), KIT (4q12), STK11 (19p13.3); inmemiş testis riski artırır (erkek kardeşte 8-10x, babada 4x)',
          ],
          [
            'Mesane Kanseri (Ürotelyal Karsinom)',
            'TSG kayıpları: PTEN (%50 LOH), TSC1 (%34 LOH), SFRP1 (%25 metilasyon), CDKN2A (%14)',
            'FGFR3 mutasyonu (yüzeysel papiller tümörlerde %82 — düşük derece, İYİ PROGNOZ) ve RAS mutasyonu',
            'Kötü prognoz / invazivlik: TP53 mutasyonu, pRB yolağı kaybı, yüksek Ki67 indeksi, c-MYC aşırı ekspresyonu\nErken nüks: ERBB2, RAS, PIK3CA\nApoptoz inhibisyonu: MDM2 aşırı ekspresyonu (%6)',
          ],
          [
            'Böbrek Tümörleri (RCC)',
            'En sık histoloji: Berrak hücreli (%75-85), Papiller (%10-15), Kromofob (%5); en sık uzak metastaz: Akciğer',
            'Evre I’de 5 yıllık sağkalım >%90',
            '5 yıllık sağkalımı belirleyen prognostik faktörler: Tümör evresi, derecesi (grade), lokal yayılımı, bölgesel lenf nodu metastazı ve tanı anında uzak metastazdır. AİLE ÖYKÜSÜ prognostik belirteç DEĞİLDİR (Çıkmış Soru)',
          ],
          [
            'Prostat Kanseri',
            'Serum: PSA\nDoku gen ekspresyon panelleri: Decipher (1.4M RNA), Oncotype DX (12 gen + 5 kontrol RT-PCR), Prolaris (31 hücre siklusu geni + 15 kontrol RT-PCR)',
            'Düşük Gleason skoru ve düşük Prolaris/Oncotype DX risk skoru (aktif izlem adayı)',
            'Kalıtsal spesifik gen: HOXB13 (OD); en sık HRR mutasyonları: BRCA2 ve ATM; en agresif / PARP ve hormon dirençli belirteç: CDK12 mutasyonu',
          ],
          [
            'Endometriyum Kanseri (4 Moleküler Grup)',
            'MMR İHK (MLH1, MSH2, MSH6, PMS2), MSI testi, p53 İHK ve POLE ekzonükleaz sekanslama',
            '1) POLE mutasyonlu grup: EN İYİ PROGNOZ\n2) MSI-H / dMMR grup: Orta prognoz\n3) Kopya sayısı düşük (normal p53): Orta prognoz',
            '4) Kopya sayısı yüksek (anormal / mutant p53) grup: EN AGRESİF / EN KÖTÜ PROGNOZ (seröz karsinom benzeri davranış)',
          ],
        ],
        k: ['g04:5', 'g04:28-48', 'g04:52-55'],
      },
      {
        id: 'gt-prenatal-pgt-belirtecler',
        baslik: 'Prenatal Tarama Belirteçleri (İkili, Üçlü, Dörtlü Test, USG) ve İnvaziv / PGT Kriterleri',
        kalip: 'belirtec',
        sutun: ['Test / Yöntem ve Haftası', 'Ölçülen Biyokimyasal / Hücresel Belirteçler', 'Down Sendromu (+21) ve Edwards (+18) Profili', 'Kritik Sınav ve Tuzak Noktası'],
        satir: [
          [
            'İlk Trimester İkili Tarama Testi (11 hf 0 gün – 13 hf 6 gün)',
            'Fetal ense saydamlığı (NT) + Maternal serum serbest β-hCG + PAPP-A (sinsityotrofoblast kökenli)',
            'Trizomi 21: NT artar, serbest β-hCG ARTAR, PAPP-A AZALIR (%80-90 saptama)\nTrizomi 18 ve 13: NT artar, serbest β-hCG AZALIR, PAPP-A AZALIR',
            'NT >3 mm artmış kabul edilir; Trizomi 21/18/13, Turner (45,X), Noonan, diyafram hernisi ve omfaloselde NT artar; KLINEFELTER (47,XXY) sendromunda NT artışı beklenmez (Çıkmış Soru)',
          ],
          [
            'İkinci Trimester Üçlü ve Dörtlü Tarama Testi (16–18. haftalar, en geniş 15–20. hf)',
            'Üçlü test: AFP + hCG + unkonjuge estriol (uE3)\nDörtlü test: Üçlü test + Dimerik İnhibin-A',
            'Trizomi 21 (Down): AFP azalır, uE3 azalır, hCG ARTAR, İnhibin-A ARTAR (Çıkmış Soru)\nTrizomi 18 (Edwards): AFP, uE3 ve hCG ÜÇÜ DE AZALIR',
            'Açık nöral tüp defektlerinde (anensefali, açık spina bifida) ve karın ön duvarı defektlerinde (omfalosel, gastroşizis) maternal serum ve amniyon sıvısı AFP düzeyi YÜKSELİR',
          ],
          [
            'Fetal USG: Kistik Higroma + Kalp Defekti',
            'Boyun lenfatik kese obstrüksiyonu (kistik higroma) + geniş ASD / VSD / aort koarktasyonu',
            'Kromozom anomalisi yoksa %95 kendiliğinden geriler; hidrops fetalis gelişirse mortalite %100’e yaklaşır',
            'En sık eşlik eden kromozom anomalisi TURNER SENDROMU (45,X) ve ardından Trizomi 21 / Trizomi 18’dir (Çıkmış Soru)',
          ],
          [
            'İnvaziv Prenatal Tanı (CVS, Amniyosentez, Kordosentez)',
            'CVS: 10-12. hf (sitotrofoblast — direkt analiz)\nAmniyosentez: 15-18. hf (~20 ml sıvı)\nKordosentez: ≥18-20. hf (fetal kan, 48-72 saatte sonuç)',
            'CVS kayıp riski %0.5-2; Amniyosentez %0.5-1; Kordosentez %2-3; Fetoskopi (15-18. hf) %20 abortus',
            'CVS <10. haftada yapılırsa ekstremite kısalması defekti yapar; Kordosentez 18. haftadan önce uygulanmaz (Çıkmış Soru); uzun süreli CVS’de XX/XY çıkarsa maternal kontaminasyon için amniyosentez yapılır',
          ],
          [
            'Preimplantasyon Genetik Tanı (PGT)',
            'Polar cisimcik (yalnız maternal), Blastomer (3. gün, 6-8 hücre), Trofektoderm (5. gün blastosist — iç hücre kitlesi korunur)',
            'Tek gen: WGA + STR (PGH) veya SNP (Karyomapping)\nAnöploidi (24 kromozom): aCGH veya NGS (FISH yalnız sınırlı kromozom bakar)',
            'Yabancı sperm DNA kontaminasyonunu önlemek için ICSI zorunludur; RFLP PGT’de kullanılmaz (Çıkmış Soru); tek hücre PCR hatası Alel Düşmesi (ADO); HLA uyumlu kardeş PGT en sık Beta-talasemi majörde yapılır',
          ],
        ],
        k: ['g05:20-92', 'g06:10-90'],
      },
    ],
    spotlar: [
      { id: 'gs-501', kalip: 'belirtec', m: '**AFP, β-hCG ve LDH** serum tümör belirteçleri **testis germ hücreli tümörlerinin (TGCT)** tanı, evreleme, prognoz ve tedavi takibinde birlikte kullanılır.', k: 'g04:48' },
      { id: 'gs-502', kalip: 'belirtec', m: '**Mesane kanserinde** düşük dereceli yüzeysel papiller tümörlerde **%82 saptanan FGFR3 mutasyonu İYİ PROGNOZ** belirteci iken; **TP53 mutasyonu, pRB kaybı, yüksek Ki67 ve c-MYC** artışı **KÖTÜ PROGNOZ / invazivlik** belirtecidir.', k: 'g04:29-32' },
      { id: 'gs-503', kalip: 'belirtec', m: '**Mesane kanserinde** **ERBB2 (HER2), RAS ve PIK3CA** mutasyonları **erken nüks** belirteci; **MDM2 aşırı ekspresyonu (%6)** ise p53 yıkımını artırarak **apoptoz inhibisyonu** belirtecidir.', k: 'g04:30-32' },
      { id: 'gs-504', kalip: 'belirtec', m: '**Böbrek tümörlerinde (RCC)** 5 yıllık sağkalımı belirleyen prognostik faktörler **tümör evresi, derecesi, lokal yayılımı, lenf nodu tutulumu ve uzak metastazdır**; **aile öyküsü** prognostik belirteç değildir.', k: 'g04:5' },
      { id: 'gs-505', kalip: 'belirtec', m: '**Prostat kanserinde** kalıtsal yatkınlıkla doğrudan ilişkili homeobox gen **HOXB13**; en sık HRR mutasyonları **BRCA2 ve ATM**; doku bazlı prognostik gen panelleri ise **Decipher, Oncotype DX ve Prolaris**’tir.', k: 'g04:34-43' },
      { id: 'gs-506', kalip: 'belirtec', m: '**Endometriyal karsinomun** 4 moleküler alt grubu içinde **en iyi prognozlu olan POLE mutasyonlu grup**, **en agresif / en kötü prognozlu olan ise kopya sayısı yüksek (anormal/mutant p53) gruptur** (MSI-H grup orta prognozludur).', k: 'g04:53' },
      { id: 'gs-507', kalip: 'belirtec', m: 'Maternal serumda **β-hCG ve İnhibin-A artışı** ile **AFP, uE3 ve PAPP-A azalması Down sendromunu (Trizomi 21)**; tüm biyokimyasal belirteçlerin (**AFP, uE3, β-hCG, PAPP-A**) birlikte azalması ise **Edwards sendromunu (Trizomi 18)** düşündürür.', k: 'g05:25-29' },
      { id: 'gs-508', kalip: 'belirtec', m: '11–14. haftalarda yapılan ikili testte **artmış ense saydamlığı (NT >3 mm)** Trizomi 21, 18, 13, Turner (45,X), Noonan sendromu, diyafram hernisi ve omfaloselde görülür; **Klinefelter sendromunda (47,XXY)** öncelikle beklenmez.', k: 'g05:29' },
      { id: 'gs-509', kalip: 'belirtec', m: '**Koryon villus örneklemesinde (CVS, 10–12. hf)** doğrudan kromozom analizi aktif bölünen **sitotrofoblast** hücrelerinden yapılır; **kordosentez** ise 18–20. haftadan önce uygulanmaz.', k: 'g05:56-65' },
      { id: 'gs-510', kalip: 'belirtec', m: '**Preimplantasyon genetik tanıda (PGT)** baba kaynaklı anomalileri gösteremeyen yöntem **polar cisimcik biyopsisidir**; tek hücre PCR’da heterozigot alelin çoğalamaması hatasına **alel düşmesi (ADO)** denir ve PGT’de **RFLP** kullanılmaz.', k: 'g06:24-52' },
    ],
    soruCevaplar: [
      {
        id: 'gqa-501',
        kalip: 'belirtec',
        s: 'AFP, β-hCG ve LDH tümör belirteçleri hangi ürogenital kanserde tanı, prognoz ve tedavi takibinde birlikte kullanılır?',
        c: 'Testis germ hücreli tümörlerinde (TGCT).',
        k: 'g04:48',
      },
      {
        id: 'gqa-502',
        kalip: 'belirtec',
        s: 'Mesane kanserinde düşük dereceli yüzeysel papiller tümörlerde (%82) saptanan iyi prognoz belirteci ile invaziv tümörlerde saptanan kötü prognoz belirteçleri nelerdir?',
        c: 'İyi prognoz: FGFR3 mutasyonu (%82). Kötü prognoz: TP53 mutasyonu, pRB kaybı, yüksek Ki67 proliferasyon indeksi ve c-MYC aşırı ekspresyonu (erken nüks: ERBB2, RAS, PIK3CA).',
        k: 'g04:29-32',
      },
      {
        id: 'gqa-503',
        kalip: 'belirtec',
        s: 'Endometriyal karsinomun 4 moleküler alt grubundan en iyi prognozlu olanı ve en agresif seyirli olanı hangileridir?',
        c: 'En iyi prognozlu: POLE mutasyonlu grup; En agresif / kötü prognozlu: Kopya sayısı yüksek (anormal/mutant p53) grup.',
        k: 'g04:53',
      },
      {
        id: 'gqa-504',
        kalip: 'belirtec',
        s: 'Maternal serum üçlü tarama testinde β-hCG artışı, AFP ve unkonjuge estriol (uE3) azalması hangi sendromu düşündürür?',
        c: 'Down sendromu (Trizomi 21). Üçünün birden azalması ise Edwards sendromunu (Trizomi 18) düşündürür.',
        k: 'g05:25',
      },
      {
        id: 'gqa-505',
        kalip: 'belirtec',
        s: 'Fetal ultrasonografide kistik higroma, geniş ASD ve VSD saptanan bir fetüste en olası kromozomal tanı nedir?',
        c: 'Turner sendromu (45,X).',
        k: 'g05:30',
      },
    ],
    sorular: [
      {
        id: 'gq-cikmis-501',
        tur: 'cikmis',
        yil: '2025-2026',
        kalip: 'belirtec',
        ders: 'g04',
        soru: 'AFP, β-hCG ve LDH tümör belirteçleri aşağıdaki kanserlerden hangisinde birlikte kullanılır?',
        secenekler: {
          A: 'Renal hücreli karsinom',
          B: 'Testis germ hücreli tümörleri',
          C: 'Mesane ürotelyal karsinomu',
          D: 'Prostat adenokarsinomu',
          E: 'Endometriyal karsinom',
        },
        dogru: 'B',
        aciklama: 'Alfa-fetoprotein (AFP), beta-insan koryonik gonadotropini (β-hCG) ve laktat dehidrojenaz (LDH) üçlüsü testis germ hücreli tümörlerinin (TGCT) tanı, evreleme, risk sınıflaması ve tedavi yanıtı takibinde birlikte kullanılan spesifik serum tümör belirteçleridir.',
        sikAciklamalari: {
          A: 'Renal hücreli karsinomda tanı ve takipte AFP/β-hCG/LDH üçlüsü kullanılmaz; VHL, MET, FLCN, FH ve BAP1 gibi genetik belirteçler önemlidir.',
          B: 'Testis germ hücreli tümörlerinde serum AFP, β-hCG ve LDH belirteçleri tanı, prognoz ve nüks takibinde standart olarak birlikte kullanılır.',
          C: 'Mesane karsinomunda doku düzeyinde FGFR3, TP53, pRB ve ERBB2 belirteçleri kullanılır; serum AFP/β-hCG bakılmaz.',
          D: 'Prostat adenokarsinomunda temel serum belirteci PSA olup doku düzeyinde Decipher, Oncotype DX ve Prolaris panelleri kullanılır.',
          E: 'Endometriyal karsinomda POLE, MMR/MSI ve p53 moleküler sınıflaması kullanılır.',
        },
        k: 'g04:48',
      },
      {
        id: 'gq-cikmis-502',
        tur: 'cikmis',
        yil: '2024-2025',
        kalip: 'belirtec',
        ders: 'g04',
        soru: 'Böbrek tümörlerinde prognostik belirteç olmayan aşağıdakilerden hangisidir?',
        secenekler: {
          A: 'Tümör evresi',
          B: 'Tümör derecesi (grade)',
          C: 'Tümörün lokal yayılımı',
          D: 'Bölgesel lenf nodu metastazı',
          E: 'Aile öyküsü',
        },
        dogru: 'E',
        aciklama: 'Renal hücreli karsinomda (RCC) 5 yıllık sağkalım oranlarını belirleyen beş temel prognostik faktör; tümörün evresi, histolojik derecesi (grade), lokal yayılımı, bölgesel nodal metastaz varlığı ve tanı anında uzak metastaz bulunmasıdır. Aile öyküsü herediter yatkınlık taraması için ipucu verir ancak prognostik belirteç değildir.',
        sikAciklamalari: {
          A: 'Tümör evresi (TNM) RCC’de en güçlü sağkalım belirtecidir; Evre I’de >%90 olan sağkalım Evre IV’te belirgin düşer.',
          B: 'Tümörün nükleer/histolojik derecesi (Fuhrman/ISUP grade) doğrudan prognozu ve metastaz potansiyelini belirler.',
          C: 'Perinefrik yağ dokusu, renal ven veya Gerota fasyasına lokal yayılım kötü prognostik göstergedir.',
          D: 'Bölgesel lenf nodu metastazı varlığı sağkalımı belirgin azaltan temel prognostik faktörlerden biridir.',
          E: 'Aile öyküsü genetik danışma endikasyonudur; RCC’de sağkalımı belirleyen prognostik faktörler arasında yer almaz.',
        },
        k: 'g04:5',
      },
      {
        id: 'gq-cikmis-503',
        tur: 'cikmis',
        yil: '2023-2024',
        kalip: 'belirtec',
        ders: 'g05',
        soru: 'Maternal serumda β-hCG artışı, AFP ve uE3 azalması aşağıdakilerden hangisini düşündürür?',
        secenekler: {
          A: 'Edwards sendromu (Trizomi 18)',
          B: 'Açık nöral tüp defekti',
          C: 'Turner sendromu (45,X)',
          D: 'Down sendromu (Trizomi 21)',
          E: 'Klinefelter sendromu (47,XXY)',
        },
        dogru: 'D',
        aciklama: 'İkinci trimester üçlü tarama testinde maternal serumda AFP ve unkonjuge estriol (uE3) düzeylerinin azalması, β-hCG (ve dörtlü testte dimerik inhibin-A) düzeyinin ise artması Down sendromunun (Trizomi 21) klasik biyokimyasal profilidir.',
        sikAciklamalari: {
          A: 'Edwards sendromunda (Trizomi 18) β-hCG artmaz; AFP, uE3 ve β-hCG düzeylerinin üçü birden azalır.',
          B: 'Açık nöral tüp defektlerinde (anensefali, açık spina bifida) maternal serum AFP düzeyi azalmaz, aksine belirgin olarak yükselir.',
          C: 'Turner sendromu tanısal olarak birinci/ikinci trimester USG’de kistik higroma, lenfödem ve kalp anomalileriyle saptanır.',
          D: 'Down sendromunda (Trizomi 21) AFP ve uE3 azalırken β-hCG (ve inhibin-A) artar.',
          E: 'Klinefelter sendromu (47,XXY) maternal serum üçlü tarama testinde karakteristik bir biyokimyasal patern oluşturmaz.',
        },
        k: 'g05:25',
      },
      {
        id: 'gq-cikmis-504',
        tur: 'cikmis',
        yil: '2025-2026',
        kalip: 'sendrom',
        ders: 'g05',
        soru: 'Fetal ultrasonografide kistik higroma, geniş bir atriyal septal defekt (ASD) ve ventriküler septal defekt (VSD) saptanan bir gebede en olası tanı hangisidir?',
        secenekler: {
          A: 'Turner sendromu (45,X)',
          B: 'Klinefelter sendromu (47,XXY)',
          C: 'Cri du chat sendromu (5p-)',
          D: 'Prader-Willi sendromu',
          E: 'Angelman sendromu',
        },
        dogru: 'A',
        aciklama: 'Prenatal ultrasonografide boyun bölgesinde lenfatik kese obstrüksiyonuna bağlı kistik higroma ve eşlik eden konjenital kalp anomalileri (geniş ASD, VSD, aort koarktasyonu) saptandığında en sık eşlik eden kromozomal hastalık 45,X Turner sendromudur.',
        sikAciklamalari: {
          A: 'Turner sendromu (45,X), fetal USG’de kistik higroma ve kardiyak septal/aortik defektlerle en sık prezente olan kromozom anomalisidir.',
          B: 'Klinefelter sendromunda (47,XXY) prenatal USG’de kistik higroma veya artmış ense saydamlığı beklenmez.',
          C: 'Cri du chat sendromu (5p-) postnatal kedi miyavlaması ağlaması ve mikrosefali ile tanınır; kistik higromanın tipik nedeni değildir.',
          D: 'Prader-Willi sendromu 15q11-13 imprinting bozukluğudur; yenidoğanda hipotoni ve çocuklukta obezite ile seyreder.',
          E: 'Angelman sendromu 15q11-13 maternal kaybıyla oluşur; postnatal ağır MR, ataksi ve konvülziyonlarla tanınır.',
        },
        k: 'g05:30',
      },
      {
        id: 'gq-cikmis-505',
        tur: 'cikmis',
        yil: '2024-2025',
        kalip: 'sendrom',
        ders: 'g05',
        soru: 'Ultrasonografide artmış ense saydamlığı (nukal translusens, NT) saptanan bir fetüste aşağıdaki kromozomal hastalıklardan hangisi öncelikle düşünülmez?',
        secenekler: {
          A: 'Down sendromu (Trizomi 21)',
          B: 'Edwards sendromu (Trizomi 18)',
          C: 'Patau sendromu (Trizomi 13)',
          D: 'Turner sendromu (45,X)',
          E: 'Klinefelter sendromu (47,XXY)',
        },
        dogru: 'E',
        aciklama: 'Gebeliğin 11-14. haftalarında ölçülen fetal ense saydamlığı (NT >3 mm) Trizomi 21, Trizomi 18, Trizomi 13 ve Monozomi X (Turner sendromu) ile doğrudan ilişkilidir. Klinefelter sendromunda (47,XXY) ise artmış NT beklenen bir bulgu değildir.',
        sikAciklamalari: {
          A: 'Trizomi 21 (Down sendromu), birinci trimesterde artmış ense saydamlığının en sık saptanan otozomal trizomi nedenidir.',
          B: 'Trizomi 18 (Edwards sendromu) belirgin NT artışı ve erken fetal yapısal anomalilerle seyreder.',
          C: 'Trizomi 13 (Patau sendromu) artmış NT, holoprozensefali ve kalp defektleri ile ilişkilidir.',
          D: 'Turner sendromu (45,X) lenfatik drenaj bozukluğu nedeniyle en yüksek NT ve kistik higroma değerlerine yol açan sendromdur.',
          E: 'Klinefelter sendromunda (47,XXY) intrauterin lenfatik obstrüksiyon veya kalp defekti beklenmediğinden NT artışı öncelikle düşünülmez.',
        },
        k: 'g05:29',
      },
      {
        id: 'gq-ornek-506',
        tur: 'ornek',
        kalip: 'belirtec',
        ders: 'g04',
        soru: 'Mesane kanserinde düşük dereceli ve invaziv olmayan yüzeysel papiller tümörlerde yaklaşık %82 oranında saptanan ve iyi prognozla ilişkili olan genetik belirteç aşağıdakilerden hangisidir?',
        secenekler: {
          A: 'TP53 inaktive edici mutasyonu',
          B: 'FGFR3 aktive edici mutasyonu',
          C: 'pRB tümör süpresör yolağı kaybı',
          D: 'MDM2 aşırı ekspresyonu',
          E: 'Yüksek Ki67 proliferasyon indeksi',
        },
        dogru: 'B',
        aciklama: 'Mesane tümörlerinde FGFR3 reseptör tirozin kinaz mutasyonu yüzeysel papiller (invaziv olmayan) tümörlerin yaklaşık %82’sinde bulunur ve düşük derece / iyi prognoz belirtecidir. Buna karşılık TP53, pRB kaybı, c-MYC ve yüksek Ki67 kötü prognoz ve kas invazyonu ile ilişkilidir.',
        sikAciklamalari: {
          A: 'TP53 mutasyonu mesane kanserinde yüksek dereceli, kas invaziv ve kötü prognozlu tümörlerin karakteristik belirtecidir.',
          B: 'FGFR3 mutasyonu yüzeysel papiller mesane tümörlerinde %82 oranında saptanır ve düşük derece / iyi prognoz göstergesidir.',
          C: 'pRB (retinoblastom) yolağı bozukluğu hücre siklusu kontrolünü ortadan kaldırarak invaziv ve agresif mesane kanserine yol açar.',
          D: 'MDM2 aşırı ekspresyonu (%6) p53’ü baskılayarak apoptoz inhibisyonuna ve tümör progresyonuna neden olur.',
          E: 'Yüksek Ki67 proliferasyon indeksi hızlı hücre bölünmesini ve kötü prognozu gösterir.',
        },
        k: 'g04:29-32',
      },
      {
        id: 'gq-ornek-507',
        tur: 'ornek',
        kalip: 'belirtec',
        ders: 'g04',
        soru: 'Endometriyal karsinomların moleküler sınıflandırmasında yer alan 4 alt gruptan “en iyi prognozlu” olan ile “en agresif seyirli” olan aşağıdakilerin hangisinde sırasıyla doğru verilmiştir?',
        secenekler: {
          A: 'MSI-H (dMMR) grup — POLE mutasyonlu grup',
          B: 'POLE mutasyonlu grup — Kopya sayısı yüksek (anormal p53) grup',
          C: 'Kopya sayısı yüksek (anormal p53) grup — Kopya sayısı düşük (normal p53) grup',
          D: 'Kopya sayısı düşük (normal p53) grup — MSI-H (dMMR) grup',
          E: 'POLE mutasyonlu grup — MSI-H (dMMR) grup',
        },
        dogru: 'B',
        aciklama: 'Endometriyal karsinomun 4 moleküler alt grubu içinde POLE ultramutant grup mükemmel sağkalım ile en iyi prognozlu gruptur; kopya sayısı yüksek (anormal/mutant p53) grup ise seröz karsinom benzeri davranış gösteren en agresif ve en kötü prognozlu gruptur.',
        sikAciklamalari: {
          A: 'MSI-H (dMMR) grup orta prognozludur; POLE mutasyonlu grup ise en kötü değil en iyi prognozlu gruptur.',
          B: 'POLE mutasyonlu grup en iyi prognozlu, kopya sayısı yüksek (anormal p53) grup ise en agresif seyirli alt gruptur.',
          C: 'Kopya sayısı yüksek (anormal p53) grup en iyi değil en kötü prognozlu gruptur.',
          D: 'Hem kopya sayısı düşük (normal p53) hem de MSI-H grup orta prognozlu sınıfta yer alır.',
          E: 'MSI-H grup orta prognozludur; en agresif seyirli olan grup kopya sayısı yüksek (anormal p53) gruptur.',
        },
        k: 'g04:53',
      },
    ],
  },
];

import { EK_SORU_CEVAPLAR, EK_SORULAR, EK_SPOTLAR } from './genetikCheckupEkVeri';

for (const b of GENETIK_BOLUMLER) {
  if (EK_SPOTLAR[b.id]) b.spotlar.push(...EK_SPOTLAR[b.id]);
  if (EK_SORU_CEVAPLAR[b.id]) b.soruCevaplar.push(...EK_SORU_CEVAPLAR[b.id]);
  if (EK_SORULAR[b.id]) b.sorular.push(...EK_SORULAR[b.id]);
}

export type GenetikBolumId = string;

export interface GenetikZenginTablo extends GenetikTablo {
  bolum: string;
  aciklama: string;
  sutunlar: string[];
  satirlar: string[][];
}

export interface GenetikZenginSpot extends GenetikSpot {
  bolum: string;
  cumle: string;
  etiket: string;
  cikmisYil?: string;
}

export interface GenetikZenginSoruCevap extends GenetikSoruCevap {
  bolum: string;
  soru: string;
  cevap: string;
  odak: string;
  ipucu?: string;
}

export interface GenetikZenginSoru extends GenetikSoru {
  bolum: string;
  kok: string;
  kalipEtiketi: string;
  spotCikarim: string;
}

export const GENETIK_TABLOLAR: GenetikZenginTablo[] = GENETIK_BOLUMLER.flatMap((b) =>
  b.tablolar.map((tb) => ({
    ...tb,
    bolum: b.id,
    aciklama: `${b.kisa} · ${KALIP_META[tb.kalip].kisa} (Slayt: ${tb.k.join(', ')})`,
    sutunlar: tb.sutun,
    satirlar: tb.satir,
  })),
);

export const GENETIK_SPOTLAR: GenetikZenginSpot[] = GENETIK_BOLUMLER.flatMap((b) =>
  b.spotlar.map((sp) => ({
    ...sp,
    bolum: b.id,
    cumle: sp.m,
    etiket: `${KALIP_META[sp.kalip].kisa} · ${sp.k}`,
  })),
);

export const GENETIK_SORU_CEVAPLAR: GenetikZenginSoruCevap[] = GENETIK_BOLUMLER.flatMap((b) =>
  b.soruCevaplar.map((sc) => ({
    ...sc,
    bolum: b.id,
    soru: sc.s,
    cevap: sc.c,
    odak: `${KALIP_META[sc.kalip].kisa} · ${sc.k}`,
  })),
);

export const GENETIK_SORULAR: GenetikZenginSoru[] = GENETIK_BOLUMLER.flatMap((b) =>
  b.sorular.map((q) => ({
    ...q,
    bolum: b.id,
    kok: q.soru,
    kalipEtiketi: `${KALIP_META[q.kalip].kisa} · ${DERS_AD[q.ders] || q.ders}`,
    spotCikarim: q.sikAciklamalari[q.dogru] || q.aciklama,
  })),
);

export const GENETIK_TOPLAM = {
  bolum: GENETIK_BOLUMLER.length,
  tablo: GENETIK_TABLOLAR.length,
  satir: GENETIK_TABLOLAR.reduce((x, t) => x + t.satir.length, 0),
  spot: GENETIK_SPOTLAR.length,
  soruCevap: GENETIK_SORU_CEVAPLAR.length,
  soru: GENETIK_SORULAR.length,
  cikmis: GENETIK_SORULAR.filter((q) => q.tur === 'cikmis').length,
  ornek: GENETIK_SORULAR.filter((q) => q.tur === 'ornek').length,
};


