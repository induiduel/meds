# -*- coding: utf-8 -*-
"""
Microbiology & Infectious Diseases Concepts Database
"""

MICROBIOLOGY_CONCEPTS = [
    # 1. Gram Pozitif Koklar
    ("Staphylococcus aureus & Toksinleri", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "staphylococcus aureus", "s aureus", "katalaz pozitif", "koagulaz pozitif", "altin sarisi koloni",
        "mannitol tuzlu agar fermentasyon", "protein a fc bolgesi baglanma", "tsst 1 toksik sok sendromu superantijen",
        "eksfolyatif toksin haslanmis deri sendromu ritter", "enterotoksin besin zehirlenmesi mayonez krema",
        "alfa toksin por olusumu", "pantone valentin lokosidin pvl nekrotizan pnomoni"
    ]),
    ("MRSA (Metisiline Dirençli S. aureus)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "mrsa", "metisilin direncli", "meca geni", "pbp2a penisilin baglayan protein", "oksasilin direnci",
        "vankomisin teikoplanin", "daptomisin", "linezolid", "seftarolin"
    ]),
    ("Staphylococcus epidermidis (Biyofilm & Protez)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "staphylococcus epidermidis", "koagulaz negatif stafilokok kns", "novobiyosine duyarli", "biyofilm slime faktor",
        "protez kapak endokarditi", "kateter enfeksiyonlari", "santral venoz kateter", "ortopedik protez"
    ]),
    ("Staphylococcus saprophyticus (Genç Kadında İYE)", ["Tıbbi Mikrobiyoloji", "Üroloji", "Enfeksiyon Hastalıkları"], [
        "staphylococcus saprophyticus", "novobiyosine direncli", "genc kadin sistit", "balayi sistiti", "ikinci sik iye etkeni"
    ]),
    ("Streptococcus pneumoniae (Pnömokok)", ["Tıbbi Mikrobiyoloji", "Göğüs Hastalıkları", "Enfeksiyon Hastalıkları"], [
        "streptococcus pneumoniae", "pnomokok", "alfa hemolitik", "optokine duyarli", "safra tuzlarinda erir",
        "lanzet kokus diplokok", "polisakkarit kapsul quellung sisme reaksiyonu", "pnomolizin", "iga proteaz",
        "toplum kokenli pnomoni pasli balgam", "eriskinde menenjit otitis media sinuzit"
    ]),
    ("Streptococcus pyogenes (A Grubu Beta-Hemolitik / GAS)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları", "Pediatri"], [
        "streptococcus pyogenes", "a grubu beta hemolitik streptokok agbhs gas", "basitrasine duyarli", "pyr pozitif",
        "m proteini fagositoz engeli otoantikor", "streptolizin o aso", "streptokinaz", "eritrojenik spe toksini kizil",
        "akut romatizmal ates ara jones kriterleri", "akut poststreptokoksik glomerulonefrit apsgn", "erisipel yılancık selulit nekrotizan fasiit"
    ]),
    ("Streptococcus agalactiae (B Grubu Streptokok / GBS)", ["Tıbbi Mikrobiyoloji", "Pediatri", "Kadın Hastalıkları ve Doğum"], [
        "streptococcus agalactiae", "b grubu streptokok gbs", "basitrasine direncli", "camp testi pozitif oku ucu hemoliz",
        "hipurat hidrolizi pozitif", "yenidogan menenjiti ve sepsisi en sik etken", "dogum kanali kolonizasyonu intrapartum profilaksi penisilin ampisilin"
    ]),
    ("Streptococcus viridans Grubu & S. bovis (gallolyticus)", ["Tıbbi Mikrobiyoloji", "Kardiyoloji", "Gastroenteroloji"], [
        "streptococcus viridans", "optokine direncli", "safrada erimez", "dekstran biyofilm uretimi", "dis cekimi sonrasi dogal kapak subakut endokarditi",
        "streptococcus gallolyticus", "streptococcus bovis", "kolon kanseri birlikteligi kolonoskopi sart"
    ]),
    ("Enterococcus faecalis & faecium (VRE)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "enterococcus faecalis", "enterococcus faecium", "yuzde 6 5 nacl de urer", "safra eskulin pozitif",
        "nobiotiklere dogal direnc sefalosporin direnci", "ureter manipulasynu nozokomiyal iye endokardit",
        "vre vankomisin direncli enterokok vana vanb geni", "linezolid daptomisin"
    ]),

    # 2. Gram Pozitif Basiller
    ("Bacillus anthracis (Şarbon)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "bacillus anthracis", "sarbon", "sporlu buyuk gram pozitif basil", "poliglutamik asit protein kapsul",
        "hareketsiz medusa basi koloni", "letal faktor odem faktor koruyucu antijen", "deri sarbonu agrisiz siyah eskar nekrotik kabuk",
        "akciger sarbonu yun egrisi mediastinal genisleme hemorajik mediastinit"
    ]),
    ("Bacillus cereus (Kızarmış Pilav Zehirlenmesi)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "bacillus cereus", "kizarmis pilav", "tekrar isitilan pirinc", "emetik toksin sereulid kisa kulucka bulanti kusma",
        "diyareik toksin uzun kulucka sulu ishal"
    ]),
    ("Clostridium tetani (Tetanoz)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları", "Nöroloji"], [
        "clostridium tetani", "tetanoz", "anaerop sporlu basil baget baget davul tokmagi spor", "tetanospazmin retrograd aksonal transport",
        "renshaw hucreleri gaba glisin salinimi blokaji", "spastik paralizi opistotonus risus sardonicus kilitli cene trismus", "tetanoz immunglobulin asi"
    ]),
    ("Clostridium botulinum (Botulizm)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları", "Nöroloji"], [
        "clostridium botulinum", "botulizm", "konserve zehirlenmesi balla bebek botulizmi", "botulinum toksini snare synaptobrevin yikimi",
        "asetilkolin salinimi engeli", "inen simetrik gevsek flask felc", "pitozis diplopi midriyazis disfaji disartri", "solunum yetmezligi"
    ]),
    ("Clostridium perfringens (Gazlı Gangren)", ["Tıbbi Mikrobiyoloji", "Genel Cerrahi", "Enfeksiyon Hastalıkları"], [
        "clostridium perfringens", "alfa toksin lesitinaz fosfolipaz c", "cift zonlu hemoliz nagler reaksiyonu",
        "gazli gangren miyonnekroz krepitasyon bilye gibi dokuda hava", "agir agri toksik tablo acil debritman hiperbarik oksijen"
    ]),
    ("Clostridioides difficile (Psödomembranöz Kolit)", ["Tıbbi Mikrobiyoloji", "Gastroenteroloji", "Enfeksiyon Hastalıkları"], [
        "clostridioides difficile", "c difficile", "antibiyotik iliskili psodomembranoz kolit", "toksin a enterotoksin", "toksin b sitotoksin aktin polimerizasyonu",
        "volkanik krizis sari beyaz psodomembranlar kolonoskopi", "oral vankomisin fidaksomisin fekal mikrobiyota transplantasyonu"
    ]),
    ("Listeria monocytogenes (Soğukta Üreme & Meningoensefalit)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları", "Pediatri"], [
        "listeria monocytogenes", "pastorize edilmemis sut urunleri cig peynir salam", "4 derecede buzdolabinda urer sogukta zenginlestirme",
        "takla atma hareketi tumbling motility", "aktin kuyruklari roket hareketi hucreden hucreye gecis", "yenidogan sepsisi granülomatozis infantiseptika",
        "yaslilarda gebelerde ve hucresel bagisiklik baskilanmis menenjit", "ampisilin ilk tercih sefalosporinler dogal direnc"
    ]),
    ("Corynebacterium diphtheriae (Krup / Difteri)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları", "Pediatri"], [
        "corynebacterium diphtheriae", "difteri", "loeffler besiyeri tellurit tinisdale agar siyah koloni", "metakromatik cisimcikler babes ernst cisimcigi albert neisser boyasi",
        "difteri toksini bofaj lizojenik ef 2 adp ribozilasyonu protein sentez inhibisyonu", "bogazda gri beyaz kaldirilamayan kanayan psodomembran",
        "boga boynu bull neck lenfadenopati", "miyokardit ve aritmi toksik felcler", "antitoksin at serumu ve eritromisin penisilin"
    ]),
    ("Actinomyces israelii & Nocardia asteroides", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "actinomyces israelii", "anaerop dallanan basil", "kavite olusturan fistulize cene boyun lezyonu lumpy jaw",
        "sari kükürt sulfur granulleri", "penisilin tedavisi",
        "nocardia asteroides", "aerop dallanan basil asido rezistan kismi zihl neelsen", "toprak solunumu beyin absesi ve akciger kavitasyonu", "tmp smx tedavisi"
    ]),

    # 3. Gram Negatif Koklar ve Kokobasiller
    ("Neisseria meningitidis (Meningokok)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "neisseria meningitidis", "meningokok", "gram negatif diplokok kahve cekirdegi", "thayer martin besiyeri cikolatali agar",
        "kapsul polisakkarit a b c y w135", "lipooligosakkarit los endotoksin agir vaskuler hasar", "peteşiyal purpurik dokuntu",
        "waterhouse friderichsen bilateral adrenal kanama sok", "kompleman c5 c9 terminal eksikligi tekrarlayan enfeksiyon", "seftriakson rifampisin profilaksi"
    ]),
    ("Neisseria gonorrhoeae (Gonokok / Bel Soğukluğu)", ["Tıbbi Mikrobiyoloji", "Üroloji", "Kadın Hastalıkları ve Doğum"], [
        "neisseria gonorrhoeae", "gonokok", "kapsulsuzdur", "antijenik varyasyon pilus opa proteinleri",
        "erkekte purulan uretra akintisi yanma", "kadinda servisit pelvik inflamatuar hastalik pid tuba ovarien abse ektopik gebelik infertilite",
        "dissemine gonokoksik enfeksiyon dge septik artrit diz eklemi pustuler dokuntu", "yenidogan oftalmia neonatorum profilaksi seftriakson azitromisin"
    ]),
    ("Moraxella catarrhalis", ["Tıbbi Mikrobiyoloji", "Göğüs Hastalıkları", "KBB"], [
        "moraxella catarrhalis", "oksidaz pozitif gram negatif diplokok", "koah akut alevlenme", "otitis media cocukta", "beta laktamaz pozitiftir ampisiline direncli"
    ]),
    ("Haemophilus influenzae Tip b (Hib)", ["Tıbbi Mikrobiyoloji", "Pediatri", "KBB"], [
        "haemophilus influenzae", "hib", "pleomorfik gram negatif kokobasil", "x faktoru hemin ve v faktoru nad gerektirir",
        "cikolatali agar stafilokok cevresinde uydu kolonizasyon satelitizm", "poliribozilribitol fosfat prp kapsul",
        "akut epiglottit basparmak belirtisi drooling", "menenjit krup sellulit otit", "konjuge hib asisi rifampisin profilaksisi"
    ]),
    ("Bordetella pertussis (Boğmaca)", ["Tıbbi Mikrobiyoloji", "Pediatri"], [
        "bordetella pertussis", "bogmaca", "regan lowe bordet gengou besiyeri civa damlasi koloni",
        "bogmaca toksini gi protein adp ribozilasyonu camp artisi", "adenilat siklaz toksini akt trakeal sitotoksin siliyer felc",
        "paroksismal oksuruk nobetleri ciftleme sesli ic cekme whoop", "belirgin lenfositoz lokositoz", "makrolid azitromisin klaritromisin"
    ]),
    ("Brucella melitensis & abortus (Bruselloz / Malta Humması)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "brucella melitensis", "brucella abortus", "bruselloz", "malta hummasi", "pastorize edilmemis taze koyun keci peyniri sutu",
        "ondulan ates dalgali ates gece terlemesi kus yemi kokusu", "sakroiliit spondilodiskit epididimoorsit hepatosplenomegali",
        "kemik iligi kulturu altin standart wright serolojisi roze bengal", "doksisiklin ve rifampisin veya streptomisin 6 hafta"
    ]),
    ("Francisella tularensis (Tularemi / Tavşan Ateşi)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları"], [
        "francisella tularensis", "tularemi", "tavsan kemirgen temasi kene sinek isirigi su kaynaklari", "cok dusuk enfektif doz 10 bakteri laboratuvar biyoguvenlik 3",
        "ulseroglanduler form agrisiz ulser ve dev bolgesel lenfadenopati", "okuloglanduler tifoidal orofaringeal", "streptomisin gentamisin doksisiklin"
    ]),

    # 4. Enterik Gram Negatif Basiller
    ("Escherichia coli (ETEC, EPEC, EHEC, UPEC)", ["Tıbbi Mikrobiyoloji", "Gastroenteroloji", "Nefroloji"], [
        "escherichia coli", "e coli", "laktoz fermentasyonu pembe koloni macconkey agarda", "indol pozitif",
        "upec p fimbria pyelonefrit sistit en sik etken",
        "etec turist diyaresi isi labil lt camp ve isi stabil st cgmp toksin sulu ishal",
        "ehec o157 h7 shiga benzeri toksin verotoksin sorbitol negatif macconkey",
        "hus hemolitik uremik sendrom mikroanjiyopatik anemi trombositopeni bobrek yetmezligi antibiyotik verilmez toksini artirir",
        "epec bebeklerde sulu ishal attaching and effacing"
    ]),
    ("Klebsiella pneumoniae & oxytoca", ["Tıbbi Mikrobiyoloji", "Göğüs Hastalıkları", "Enfeksiyon Hastalıkları"], [
        "klebsiella pneumoniae", "belirgin mukoid kapsullu koloni cekince uzar", "alkoliklerde diyabetiklerde agir lober pnomoni",
        "frenk uzumu jolesi kusburnu marmelati balgam red currant jelly", "kaviter abse olusumu ust lob tutulumu",
        "kpc karbapenemaz ureten direncli suslar"
    ]),
    ("Salmonella Typhi & Enteritidis", ["Tıbbi Mikrobiyoloji", "Gastroenteroloji", "Enfeksiyon Hastalıkları"], [
        "salmonella typhi", "salmonella enteritidis", "h2s hidrojen sulfur pozitif siyah merkezli koloni ssa hektoen", "hareketlidir kamcili",
        "tifo enterik ates basamakli ates rozeol goguste pembe lekeler bradikardi faget belirtisi",
        "safra kesesi tasiyiciligi kronik portorluk", "peyer plaklari nekrozu barsak perforasyonu kanama",
        "orak hucreli anemide osteomiyelit ilk akla gelen salmonella"
    ]),
    ("Shigella dysenteriae & flexneri (Basilli Dizanteri)", ["Tıbbi Mikrobiyoloji", "Gastroenteroloji"], [
        "shigella dysenteriae", "shigella sonnei", "shigella flexneri", "h2s negatiftir hareketsizdir", "cok dusuk enfektif doz 100 bakteri",
        "shiga toksini 60s ribozomal rna yikimi", "mukuslu kanli gayta tenesmus karin krampi basilli dizanteri", "hus gelisim riski"
    ]),
    ("Pseudomonas aeruginosa (Mavi-Yeşil İrin & Ekzotoksin A)", ["Tıbbi Mikrobiyoloji", "Göğüs Hastalıkları", "Enfeksiyon Hastalıkları"], [
        "pseudomonas aeruginosa", "oksidaz pozitif non fermenter laktoz negatif", "piyosiyanin mavi yesil pigment piyoverdin uzum tatli meyve kokusu",
        "ekzotoksin a difteri toksini ile ayni mekanizma ef 2 adp ribozilasyonu", "kistik fibrozis hastalarinda kronik bronsektazi mukoid sus",
        "yanik enfeksiyonlari notropenik ates dis kulak yolu malign otitis eksterna yuzucu kulagi", "ektima gangrenozum nekrotik büllü vaskulit lezyonlari", "jakuzi folikuliti"
    ]),
    ("Helicobacter pylori & Gastrit/Ülser", ["Tıbbi Mikrobiyoloji", "Gastroenteroloji"], [
        "helicobacter pylori", "h pylori", "mikroaeroffilik kivrık spiral gram negatif", "ureaz pozitifligi cok guclu mide asidini amonyakla notralize eder",
        "caga ve vaca sitotoksinleri virulans", "duodenal ulser gastrik ulser kronik b tipi gastrit antrum", "malt lenfoma ve mide adenokarsinomu riski dunya saglik orgutu grup 1 karsinojen",
        "ure nefes testi gaita antijen testi endoskopik biyopsi"
    ]),
    ("Campylobacter jejuni & Guillain-Barré İlişkisi", ["Tıbbi Mikrobiyoloji", "Gastroenteroloji", "Nöroloji"], [
        "campylobacter jejuni", "kivrık marti kanadi gorunumu mikroaerofilik 42 derecede urer campy bap agar", "cig tavuk urunleri tuketimi",
        "kanli sulu ishal kolit", "guillain barre sendromu molekuler benzerlik antikor capi gangliozid miyelin yikimi", "reaktif artrit"
    ]),
    ("Vibrio cholerae (Kolera & Pirinç Suyu İshal)", ["Tıbbi Mikrobiyoloji", "Gastroenteroloji"], [
        "vibrio cholerae", "virgul seklinde hareketli polar kamcili tcbs agarda sari koloni sukroz fermentasyonu", "alkali ortam sever mide asidine cok duyarlidir yuksek inokulum gerekir",
        "kolera toksini kolerajen gs alfa protein kilitlenmesi intraselluler camp patlamasi klor ve su sekresyonu",
        "pirinc yikanti suyu seklinde masif ishal pirinc suyu gayta", "agir hipovolemik sok olum acil sivi replasmani rehidrasyon"
    ]),
    ("Legionella pneumophila (Lejyoner Hastalığı)", ["Tıbbi Mikrobiyoloji", "Göğüs Hastalıkları"], [
        "legionella pneumophila", "bcye agarda demir ve l sistein gereksinimi", "klima su depolari nebulizatorler insandan insana bulasmaz",
        "atipik pnomoni kuru oksuruk mental konfuzyon bas agrisi", "hiponatremi uygunsuz adh artisi", "karaciger enzim yuksekligi idrarda legionella serogrup 1 antijeni"
    ]),

    # 5. Spiroketler ve Atipikler
    ("Treponema pallidum (Sifiliz / Frengi)", ["Tıbbi Mikrobiyoloji", "Dermatoloji", "Enfeksiyon Hastalıkları"], [
        "treponema pallidum", "sifiliz", "frengi", "karanlik saha mikroskopisi hareketli tirbuson spiroket",
        "primer sifiliz agrisiz sert tabanli sankr bolgesel agrisiz lap",
        "sekonder sifiliz avuc ici ve ayak tabaninda makulopapuler dokuntu condyloma lata mukoz plaklar yaygin lap",
        "tersiyer sifiliz gommuler aort anevrizmasi norosifiliz tabes dorsalis argyll robertson pupillasi",
        "tarama vdrl rpr dogrulama fta abs tpha tppa", "jarisch herxheimer reaksiyonu penisilin sonrasi ani titresim ates"
    ]),
    ("Borrelia burgdorferi (Lyme Hastalığı)", ["Tıbbi Mikrobiyoloji", "Enfeksiyon Hastalıkları", "Nöroloji"], [
        "borrelia burgdorferi", "lyme hastaligi", "ixodes kene isirigi",
        "evre 1 eritema kronikum migrans hedef tahtasi bullseye dokuntu",
        "evre 2 bilateral fasilal paralizi bell palsi kardit av bloklar artralji",
        "evre 3 kronik buyuk eklem monoartriti diz ensefalopati", "doksisiklin erken amoksisilin gebelede seftriakson gec donem"
    ]),
    ("Mycoplasma pneumoniae (Soğuk Aglütinin & Atipik Pnömoni)", ["Tıbbi Mikrobiyoloji", "Göğüs Hastalıkları"], [
        "mycoplasma pneumoniae", "hucre duvari yoktur peptidoglikan yok penisilin ve sefalosporinler tamamen etkisizdir",
        "sterol iceren hucre zari eaton agarda sahanda yumurta fried egg koloni", "okullarda kislalarda genclerde atipik pnomoni yuruyen pnomoni",
        "soguk aglutinin igm titresinde artis otoimmun hemolitik anemi", "eritema multiforme stevens johnson"
    ]),
    ("Chlamydia trachomatis (Trahom, Üretrit, LGV)", ["Tıbbi Mikrobiyoloji", "Göz Hastalıkları", "Üroloji"], [
        "chlamydia trachomatis", "zorunlu hucre ici bakteri atp uretemez elementer cisimcik enfektif retikuler cisimcik replikatif",
        "serotip a b c trahom korluk dunya genelinde en sik onlenebilir korluk",
        "serotip d k cinsel yolla bulasan nongonokoksik uretrit mukopurulan servisit pid fitz hugh curtis keman teli perisplenik yapisiklik",
        "serotip l1 l3 lenfogranuloma venereum lgv oluk belirtisi groove sign bufo fistulizasyon", "doksisiklin azitromisin"
    ])
]
