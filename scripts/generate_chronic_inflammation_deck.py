#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_chronic_inflammation_deck.py
Generates the deep (%500 detail) 22-slide learning deck for:
"Kronik Enflamasyon, Granülomlar ve Doku Onarımı" (Tıbbi Patoloji - Prof. Dr. Hikmet Keleş)
Incorporating 22 slides, 44 3D flashcards, 5 comparison tables, and 30+ past exam questions.
"""

import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')
META_PATH = os.path.join('src', 'data', 'learning_decks_meta.json')
QUEUE_PATH = os.path.join('src', 'data', 'learning_batch_queue.json')
QUESTIONS_PATH = os.path.join('src', 'data', 'pastQuestions.json')

def load_questions():
    if not os.path.exists(QUESTIONS_PATH):
        return []
    with open(QUESTIONS_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        return json.load(f)

ALL_QUESTIONS = load_questions()

def find_matched_questions(keywords, max_count=2):
    matched = []
    seen_ids = set()
    for q in ALL_QUESTIONS:
        if q.get('discipline') != 'Tıbbi Patoloji':
            continue
        text = (str(q.get('stem', '')) + ' ' + str(q.get('explanation', ''))).lower()
        if any(kw in text for kw in keywords):
            qid = q.get('id')
            if qid not in seen_ids and q.get('stem') and q.get('options'):
                seen_ids.add(qid)
                opts = []
                for o in q.get('options', []):
                    opts.append({
                        'key': o.get('key', ''),
                        'text': o.get('text', ''),
                        'isCorrect': o.get('key') == q.get('correctAnswer')
                    })
                matched.append({
                    'id': qid,
                    'examYear': q.get('examYear', 'Kurul 1 Çıkmış'),
                    'question': q.get('stem'),
                    'options': opts,
                    'correctAnswer': q.get('correctAnswer', 'A'),
                    'explanation': q.get('explanation') or 'Bu soru Kurul 1 Patoloji müfredatında kronik enflamasyon ve granülom patolojisi ile doğrudan ilişkilidir.'
                })
                if len(matched) >= max_count:
                    break
    return matched

SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Kronik Enflamasyonun Tanımı ve Biyolojik Çerçevesi",
        "subtitle": "Uzamış yangısal yanıt, eşzamanlı aktif doku yıkımı ve onarım girişimleri",
        "badge": "Kronik Enflamasyon",
        "badgeColor": "indigo",
        "keywords": ["kronik enflamasyon", "mononükleer", "yıkım", "onarım"],
        "lead": "Kronik enflamasyon; haftalar, aylar hatta yıllar süren, aktif iltihabın, doku yıkımının ve onarım girişimlerinin bir arada eşzamanlı olarak yürüdüğü uzamış bir yangı sürecidir.",
        "spotPearls": [
            "Akut enflamasyonun aksine kronik enflamasyonda; AKTİF İLTİHAP, DOKU YIKIMI VE ONARIM (Fibrozis/Anjiyogenez) AYNI ANDA bir arada bulunur.",
            "Kronik enflamasyonun temel hücresel yürütücüleri nötrofiller değil; MONONÜKLEER HÜCRELERDİR (Makrofajlar, Lenfositler ve Plazma hücreleri)."
        ],
        "keyBullets": [
            {"title": "Zaman Spektrumu", "desc": "Akut yanıtın saatler-günler içinde bitmesine karşılık, kronik enflamasyon etken yok edilemediğinde aylarca veya ömür boyu seyreder."},
            {"title": "Eşzamanlı Yıkım ve Onarım", "desc": "Sürekli salınan enzimler ve serbest oksijen radikalleri parankimi eritirken; fibroblastlar ve endotel hücreleri skarla boşluğu doldurmaya çalışır."},
            {"title": "Sessiz ve Sinsi Başlangıç", "desc": "Bazen çözülemeyen akut yangının devamı olarak ortaya çıkarken, çoğu zaman (otoimmünite, ateroskleroz) sessizce doğrudan kronik olarak başlar."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-1",
                "question": "Kronik enflamasyonu akut enflamasyondan ayıran en temel biyolojik karakteristik nedir?",
                "answer": "Kronik enflamasyonda aktif iltihap, parankimal doku yıkımı ve onarım girişimlerinin (anjiyogenez ve fibrozis) aynı anda eşzamanlı olarak birlikte sürmesidir.",
                "hint": "Bir yandan yakılırken diğer yandan tamir edilmeye çalışılır."
            },
            {
                "id": "fc-ci-2",
                "question": "Kronik enflamasyonun hakim hücresel infiltratını hangi hücre grubu oluşturur?",
                "answer": "Mononükleer hücreler! Başlıca Makrofajlar, T ve B Lenfositleri ile Plazma hücreleri (nötrofiller istisnalar hariç kaybolmuştur).",
                "hint": "Tek yuvarlak çekirdekli mononükleer hücreler."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Akut ve Kronik Enflamasyonun Karşılaştırmalı Matrisi",
        "subtitle": "Zamanlama, hücresel kompozisyon, vasküler yanıt ve sonlanım paternleri",
        "badge": "Karşılaştırma",
        "badgeColor": "red",
        "keywords": ["akut vs kronik", "nötrofil", "eksüda", "fibrozis"],
        "lead": "Akut ve kronik enflamasyon; konağın savunma stratejisinin iki zıt zaman dilimi ve hücresel mekanizmasıdır.",
        "spotPearls": [
            "Akut enflamasyonda temel hücre NÖTROFİLDİR, vasküler sızıntı ve ödem belirgindir; tam rezolüsyonla iyileşebilir.",
            "Kronik enflamasyonda temel hücre MAKROFAJ ve LENFOSİTTİR; vasküler eksüdasyon geri plandadır, doku yıkımı ve FİBROZİS (Skar) baskındır."
        ],
        "keyBullets": [
            {"title": "Hücresel Hakimiyet", "desc": "Akut: Nötrofiller (ilk 24-48 saat). Kronik: Makrofajlar, lenfositler, plazma hücreleri, fibroblastlar."},
            {"title": "Vasküler ve Sıvı Yanıtı", "desc": "Akut: Vazodilatasyon, yüksek geçirgenlik ve sıvı eksüdasyonu (ödem). Kronik: Yeni damar oluşumu (anjiyogenez) ve kollajen birikimi."},
            {"title": "Klinik Belirtiler", "desc": "Akut: Rubor, calor, dolor, tumor, functio laesa (belirgin). Kronik: Genellikle sinsi, düşük dereceli ateş, kilo kaybı ve halsizlik."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-3",
                "question": "Akut enflamasyon ile kronik enflamasyonun hakim hücre tipleri sırasıyla hangileridir?",
                "answer": "Akut enflamasyonda NÖTROFİLLER; kronik enflamasyonda ise MAKROFAJLAR ve LENFOSİTLERDİR.",
                "hint": "Akutta polimorflar, kronikte mononükleerler."
            },
            {
                "id": "fc-ci-4",
                "question": "Doku fibrozisi ve skarlaşma akut enflamasyonun mu yoksa kronik enflamasyonun mu tipik sonucudur?",
                "answer": "Kronik enflamasyonun! Uzamış doku hasarında makrofajlardan salınan TGF-beta ve sitokinler fibroblastları uyararak masif kollajen birikimine (fibrozise) yol açar.",
                "hint": "Kronik yangının bedeli fibrozis ve fonksiyon kaybıdır."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Kronik Enflamasyonun 3 Temel Etyolojik Nedeni",
        "subtitle": "Kalıcı enfeksiyonlar, aşırı duyarlılık/otoimmünite ve toksik maruziyet",
        "badge": "Etyopatogenez",
        "badgeColor": "amber",
        "keywords": ["tüberküloz", "otoimmünite", "silikozis", "ateroskleroz"],
        "lead": "Kronik enflamasyon üç ana patolojik durumda tetiklenir ve konağın zedeleyici etkeni temizleyememesi sonucu kronikleşir.",
        "spotPearls": [
            "1) DİRENÇLİ MİKROORGANİZMALAR (Tüberküloz basili, Treponema pallidum, mantarlar): Hücre içinde saklanarak Tip IV gecikmiş aşırı duyarlılık uyarır.",
            "2) İMMÜN ARACILI HASTALIKLAR (Otoimmünite ve Alerji): SLE, Romatoid Artrit, İnflamatuvar Bağırsak Hastalığı.",
            "3) UZAMIŞ TOKSİK MARUZİYET: Ekzojen (Silikozis, asbestozis) veya Endojen (Aterosklerozda toksik lipidler)."
        ],
        "keyBullets": [
            {"title": "Kalıcı Mikrobiyal İnvazyon", "desc": "Mikobakteriler fagozom-lizozom füzyonunu engelleyerek makrofaj içinde sağ kalır; konak ancak granülomla etrafını sarabilir."},
            {"title": "Otoimmün Reaksiyonlar", "desc": "Konağın kendi antijenlerine karşı toleransın kırılmasıdır. Antijen sürekli mevcut olduğundan iltihap asla kendiliğinden sönmez."},
            {"title": "Metabolik ve Partiküler Toksisite", "desc": "Solunan silika kristalleri sindirilemez, lizozomları patlatır. Benzer şekilde arter duvarında biriken kolesterol kristalleri kronik vasküliti besler."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-5",
                "question": "Endojen (vücut içi) bir toksik maddenin tetiklediği ve günümüz dünyasında en sık görülen kronik enflamasyon hastalığı nedir?",
                "answer": "ATEROSKLEROZ! Arter duvarında biriken okside LDL ve kolesterol kristalleri damar endoteli ve makrofajlar tarafından yabancı toksin gibi algılanarak kronik iltihap başlatır.",
                "hint": "Damar sertliği aslında kronik bir enflamatuvar hastalıktır."
            },
            {
                "id": "fc-ci-6",
                "question": "Otoimmün hastalıklarda (örneğin Romatoid Artrit) enflamasyonun kronikleşmesinin ve durdurulamamasının temel nedeni nedir?",
                "answer": "Çünkü hedef antijen 'öz doku antijenidir'; vücuttan atılamaz veya tüketilemez. Antijen sürekli mevcut olduğu için immün sistem sürekli uyarılır.",
                "hint": "Etken vücudun kendi parçası olduğu için temizlenemez."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Kronik Enflamasyonun 3 Temel Morfolojik Özelliği",
        "subtitle": "Mononükleer infiltrat, parankimal doku destrüksiyonu ve onarım/anjiyogenez",
        "badge": "Histopatoloji",
        "badgeColor": "violet",
        "keywords": ["mononükleer infiltrasyon", "doku yıkımı", "anjiyogenez", "fibrozis"],
        "lead": "Işık mikroskobunda bir doku kesitinde kronik enflamasyon tanısı koyduran üç temel histopatolojik bileşen bulunur.",
        "spotPearls": [
            "1) MONONÜKLEER HÜCRE İNFİLTRASYONU: Makrofajlar, lenfositler ve plazma hücrelerinin dokuyu istilası.",
            "2) DOKU YIKIMI (Destrüksiyon): Enflamatuvar hücre ürünleriyle sağlam parankimin nekroze olması.",
            "3) ONARIM GİRİŞİMLERİ: Yeni damarlanma (Anjiyogenez) ve hasarlı dokunun yerini alan Fibrozis (kollajenleşme)."
        ],
        "keyBullets": [
            {"title": "Mononükleer Hücreler", "desc": "H&E boyasında koyu mavi yuvarlak çekirdekli lenfositler, saat kadranı nükleuslu plazma hücreleri ve geniş pembe sitoplazmalı makrofajlar izlenir."},
            {"title": "Kalıcı Parankim Kaybı", "desc": "Kronik peptik ülserde mide mukoza ve kas tabakası tamamen erir; akciğer tüberkülozunda kavitasyonlar açılır."},
            {"title": "Anjiyogenez ve Fibrozis Birlikteliği", "desc": "Endotelyal tomurcuklanma ile küçük kırılgan kılcallar oluşur; aktive fibroblastlar zengin Tip I ve Tip III kollajen sentezleyerek dokuyu sertleştirir."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-7",
                "question": "Histopatolojik incelemede 'kronik enflamasyon' tanısı koymak için aranan 3 klasik mikroskopik bulgu nedir?",
                "answer": "1) Mononükleer lökosit infiltrasyonu (makrofaj, lenfosit, plazma hücresi), 2) Doku yıkımı / destrüksiyonu, 3) Onarım girişimleri (anjiyogenez ve bağ dokusu birikimi / fibrozis).",
                "hint": "Hücre infiltratı + Yıkım + Tamir dokusu."
            },
            {
                "id": "fc-ci-8",
                "question": "Kronik bir ülser tabanında mikroskopta görülen bol kapillerli, fibroblastik genç bağ dokusuna ne ad verilir?",
                "answer": "Granülasyon Dokusu (Granulation tissue). Yeni damarlar ve prolifere fibroblastlardan oluşur; granülomatöz iltihap ile karıştırılmamalıdır!",
                "hint": "Granülom başka, granülasyon dokusu başka!"
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Makrofajların Merkezi Rolü ve Mononükleer Fagositik Sistem",
        "subtitle": "Kupffer, Alveoler makrofaj, Mikroglia, Sinüs histiyositi ve Osteoklast ailesi",
        "badge": "Mononükleer Sistem",
        "badgeColor": "indigo",
        "keywords": ["makrofaj", "monosit", "mononükleer fagositik sistem", "kupffer", "mikroglia"],
        "lead": "Makrofajlar; kemik iliğinden köken alan monositlerin dokulara göç edip farklılaşmasıyla oluşan, kronik yangının baş aktörü ve orkestra şefidir.",
        "spotPearls": [
            "Kandaki Monosit dokuya geçtiğinde MAKROFAJA (Histiyosit) dönüşür ve ömrü aylarca veya yıllarca sürebilir.",
            "Dokularda yerleşik makrofajlar: Karaciğerde KUPFFER HÜCRESİ, Akciğerde ALVEOLER MAKROFAJ, Beyinde MİKROGLİA, Dalak/Lenf nodunda SİNÜS HİSTİYOSİTİ, Kemikte OSTEOKLAST."
        ],
        "keyBullets": [
            {"title": "Kemik İliği ve Dolaşım Aşaması", "desc": "Monoblastlar olgun monosite dönüşür, kanda 1 gün dolaşır, enflamatuvar kemokinlerle (MCP-1) damar dışına ekstravaze olur."},
            {"title": "Doku İkameti", "desc": "Mononükleer Fagositik Sistem (Eski adıyla Retiküloendotelyal Sistem - RES) vücudun tüm organlarında filtre görevi görür."},
            {"title": "Kronik İltihaptaki Akümülasyon", "desc": "Makrofajların odakta toplanması 3 yolla olur: 1) Kandan sürekli monosit rekrutmanı, 2) Dokudaki makrofajların lokal proliferasyonu, 3) Göçün engellenip dokuda hapsolması."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-9",
                "question": "Karaciğer ve santral sinir sisteminde yerleşik olarak bulunan Mononükleer Fagositik Sistem hücreleri sırasıyla hangileridir?",
                "answer": "Karaciğerde: KUPFFER HÜCRELERİ; Santral Sinir Sisteminde: MİKROGLİA HÜCRELERİ.",
                "hint": "Kupffer ve Mikroglia doku makrofajlarıdır."
            },
            {
                "id": "fc-ci-10",
                "question": "Nötrofillerin ömrü 1-2 gün iken, doku makrofajlarının ömrü ne kadardır?",
                "answer": "Aylar hatta yıllar boyunca dokuda canlı kalabilir ve fonksiyon görmeye devam edebilirler. Bu uzun ömür, kronik iltihabın sürekliliğini sağlayan ana unsurdur.",
                "hint": "Nötrofil intihar komandosu, makrofaj kıdemli askerdir."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Klasik Makrofaj Aktivasyonu (M1 Yolağı): Mikrobisidal Savaş",
        "subtitle": "IFN-γ, TLR ligandları, NO, ROS, lizozomal enzimler ve Th1/Th17 uyarısı",
        "badge": "M1 Yolağı",
        "badgeColor": "red",
        "keywords": ["m1 makrofaj", "ifn-gama", "nitrik oksit", "ros", "mikrobisidal"],
        "lead": "Klasik yolak (M1); mikropları yok etmek ve immün savunmayı alevlendirmek üzere aktive olan saldırgan 'savaşçı' makrofaj fenotipidir.",
        "spotPearls": [
            "M1 AKTİVASYONUNUN EN GÜÇLÜ UYARICISI: Th1 lenfositlerinden salınan İNTERFERON-GAMA (IFN-γ) ve bakteriyel endotoksindir (LPS / TLR ligandları).",
            "M1 makrofajlar iNOS ile NİTRİK OKSİT (NO) ve NADPH oksidaz ile REAKTİF OKSİJEN RADİKALLERİ (ROS) üreterek intraselüler patojenleri öldürür."
        ],
        "keyBullets": [
            {"title": "Uyaran Sinyalleri", "desc": "Mikrobiyal Toll-Like Reseptör (TLR) ligandları ve aktive T hücrelerinden gelen IFN-γ."},
            {"title": "Silah Cephaneliği", "desc": "Yüksek miktarda ROS, NO ve asit hidrolazlar. Yan etki olarak çevre sağlam konak dokusunda da ağır nekroza yol açarlar."},
            {"title": "Pro-enflamatuvar Sitokin Üretimi", "desc": "IL-1, IL-12, IL-23 ve TNF salgılarlar. IL-12 Th1 hücrelerini, IL-23 ise Th17 hücrelerini uyararak yangıyı katlar."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-11",
                "question": "Bir doku makrofajını 'Klasik M1 Fenotipine' yönlendiren en primer T lenfosit sitokini hangisidir?",
                "answer": "İNTERFERON-GAMA (IFN-γ)! Esas olarak Th1 hücreleri ve Natural Killer (NK) hücreleri tarafından üretilir.",
                "hint": "IFN-gama M1'in ana anahtarıdır."
            },
            {
                "id": "fc-ci-12",
                "question": "M1 makrofajların fagositoz ettikleri mikropları öldürmek için sentezledikleri temel iki serbest radikal nedir?",
                "answer": "1) Reaktif Oksijen Radikalleri (ROS - Süperoksit vb.), 2) Nitrik Oksit (NO - indüklenebilir nitrik oksit sentaz / iNOS aracılığıyla).",
                "hint": "ROS ve NO birleşip peroksinitrit gibi ölümcül gazlar üretir."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Alternatif Makrofaj Aktivasyonu (M2 Yolağı): Onarım ve Fibrozis",
        "subtitle": "IL-4, IL-13, TGF-β, anjiyogenez, kollajen sentezi ve anti-enflamatuvar fren",
        "badge": "M2 Yolağı",
        "badgeColor": "sky",
        "keywords": ["m2 makrofaj", "il-4", "il-13", "tgf-beta", "onarım", "fibrozis"],
        "lead": "Alternatif yolak (M2); yangıyı yatıştırmak, doku artıklarını temizlemek ve yara iyileşmesini/fibrozisi yönetmek üzere çalışan 'tamirci' makrofaj fenotipidir.",
        "spotPearls": [
            "M2 AKTİVASYONUNUN ANA UYARICILARI: Th2 lenfositlerinden ve eozinofillerden salınan İNTERLÖKİN-4 (IL-4) ve İNTERLÖKİN-13'tür (IL-13).",
            "M2 makrofajlar mikrobisidal değildir; TRANSFORMİNG GROWTH FACTOR-BETA (TGF-β) salgılayarak fibroblastları uyarır ve FİBROZİSİ (kollajen birikimini) başlatır."
        ],
        "keyBullets": [
            {"title": "Anti-enflamatuvar Görev", "desc": "IL-10 ve IL-1 reseptör antagonisti (IL-1RA) salgılayarak aşırı yangıyı frenler ve akut atağı sonlandırır."},
            {"title": "Doku Onarımı ve Anjiyogenez", "desc": "VEGF, PDGF ve FGF büyüme faktörleriyle yeni kapillerlerin büyümesini ve granülasyon dokusu gelişimini yönetir."},
            {"title": "Kollajenaz ve Arginaz Aktivitesi", "desc": "Arginaz enzimini kullanarak L-arginini prolin ve poliaminlere dönüştürür; bu metabolitler doğrudan kollajen sentezinde yapıtaşı olarak kullanılır."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-13",
                "question": "Makrofajları alternatif M2 onarım fenotipine yönlendiren temel sitokin ikilisi hangisidir?",
                "answer": "İNTERLÖKİN-4 (IL-4) ve İNTERLÖKİN-13 (IL-13)! Th2 hücreleri, mast hücreleri ve eozinofiller tarafından salgılanırlar.",
                "hint": "Th2 sitokinleri IL-4 ve IL-13."
            },
            {
                "id": "fc-ci-14",
                "question": "M2 makrofajların doku fibrozisini ve yara onarımını tetiklemek için salgıladığı en güçlü profibrotik büyüme faktörü nedir?",
                "answer": "TGF-BETA (Transforming Growth Factor-Beta). Fibroblast proliferasyonunu ve kollajen sentezini uyarır, matriks yıkımını engeller.",
                "hint": "Fibrozisin en büyük patronu TGF-beta'dır."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "M1 ve M2 Makrofaj Dengesi ve Kronik Doku Hasarı Dinamikleri",
        "subtitle": "Kritik dengenin bozulması: Otoimmün destrüksiyon vs patolojik organ fibrozisi",
        "badge": "M1/M2 Dengesi",
        "badgeColor": "amber",
        "keywords": ["m1 m2 dengesi", "fibrozis", "organ iflası", "siroz"],
        "lead": "M1 ve M2 makrofajlar arasındaki hassas denge, kronik enflamasyonun doku yıkımıyla mı yoksa organ iflasına götüren fibrozisle mi seyredeceğini tayin eder.",
        "spotPearls": [
            "M1 aşırılığı: Kronik aktif doku destrüksiyonu, kavitasyonlar ve otoimmün eklem harabiyeti (Romatoid Artrit).",
            "M2 aşırılığı: Kontrolsüz aşırı kollajen depolanması, İdiyopatik Pulmoner Fibrozis, Karaciğer Sirozu ve Sistemik Skleroz."
        ],
        "keyBullets": [
            {"title": "Zaman Sıralı Geçiş", "desc": "Fizyolojik yanıtta önce M1'ler mikrobu öldürür; ardından M2'ler sahaya girerek ortalığı temizler ve dokuyu onarır."},
            {"title": "Kronik Yangıda İki Yolun da Kilitlenmesi", "desc": "Etken temizlenemediğinde M1'ler dokuyu parçalamaya devam ederken, M2'ler de sürekli bağ dokusu yığarak organ mimarisini bozar."},
            {"title": "Hedefe Yönelik Tedaviler", "desc": "Modern immünolojide M1/M2 polarizasyonunu kontrol eden sitokin blokörleri fibrozis ve otoimmünite tedavisinde devrim yaratmaktadır."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-15",
                "question": "Karaciğer sirozunda ve idiyopatik pulmoner fibroziste kontrolsüz bağ dokusu (kollajen) birikimini hangi makrofaj alt tipi yönetir?",
                "answer": "M2 (Alternatif aktive) Makrofajlar! Sürekli TGF-beta salgılayarak fibroblastları miyofibroblasta dönüştürür ve masif skar dokusu ürettirirler.",
                "hint": "Tamirci hücre kontrolden çıkarsa her yer skar olur."
            },
            {
                "id": "fc-ci-16",
                "question": "M1 makrofajlar ile M2 makrofajlar L-Arginin aminoasidini hangi enzimlerle ve ne amaçla kullanır?",
                "answer": "M1 makrofajlar 'iNOS' enzimiyle argininden mikrobisidal NİTRİK OKSİT (NO) üretir. M2 makrofajlar ise 'Arginaz' enzimiyle argininden kollajen sentezi için PROLİN üretir.",
                "hint": "M1 arginini silaha, M2 arginini tamir harcına çevirir!"
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "CD4+ T Lenfosit Alt Tipleri: Th1, Th2 ve Th17 Hücreleri",
        "subtitle": "Kazanılmış bağışıklığın antijenik uzmanlaşması ve sitokin imzaları",
        "badge": "T Lenfositler",
        "badgeColor": "indigo",
        "keywords": ["th1", "th2", "th17", "cd4", "lenfosit"],
        "lead": "Kronik enflamasyonda aktive olan CD4+ yardımcı T lenfositleri, salgıladıkları karakteristik sitokin profillerine göre üç temel alt gruba ayrılır.",
        "spotPearls": [
            "Th1 HÜCRELERİ: IFN-γ üretir; M1 makrofajları aktive eder; hücre içi mikroplara (TBC) ve otoimmüniteye karşı savaşır.",
            "Th2 HÜCRELERİ: IL-4, IL-5, IL-13 üretir; M2 makrofajları ve eozinofilleri uyarır; alerji ve parazitlere yanıt verir.",
            "Th17 HÜCRELERİ: IL-17 üretir; nötrofil ve monositleri sahaya çeken kemokinleri tetikler; ekstraselüler bakteri ve mantarlara yanıttır."
        ],
        "keyBullets": [
            {"title": "Th1 Yanıtı ve Granülom", "desc": "Mikobakteriyel antijenlerle uyarılır. Makrofaj aktivasyonunun ve granülomatöz iltihabın ana yürütücüsüdür."},
            {"title": "Th2 Yanıtı ve Alerji", "desc": "Helmint enfeksiyonları ve bronşiyal astımda başroldedir. Eozinofil rekrutmanı ve IgE antikor sınıf değişimini sağlar."},
            {"title": "Th17 Yanıtı ve Nötrofil Desteği", "desc": "Kronik seyirli bazı hastalıklarda (Sedef/Psöriasis, İnflamatuvar Bağırsak Hastalığı) nötrofil göçünün devamlılığını sağlayarak doku yıkımını besler."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-17",
                "question": "Th1, Th2 ve Th17 lenfosit alt tiplerinin imza sitokinleri nelerdir?",
                "answer": "Th1 imza sitokini: İNTERFERON-GAMA (IFN-γ). Th2 imza sitokinleri: IL-4, IL-5, IL-13. Th17 imza sitokini: IL-17.",
                "hint": "Th1 = IFN-gama; Th2 = IL-4/5/13; Th17 = IL-17."
            },
            {
                "id": "fc-ci-18",
                "question": "Sedef hastalığı (Psöriasis) ve Romatoid Artrit gibi kronik hastalıklarda yoğun nötrofil akışını tetikleyen T hücresi hangisidir?",
                "answer": "Th17 hücreleridir! Salgıladıkları IL-17 diğer hücrelerden kemokin salgılatarak ortama sürekli taze nötrofil göçü sağlar.",
                "hint": "IL-17 nötrofil çağırıcıdır."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "Lenfosit - Makrofaj Etkileşimi: Kısır Döngü Mekanizması",
        "subtitle": "Antijen sunumu, IL-12 ve IFN-γ aksı ile yangının otonom alevlenmesi",
        "badge": "İmmün Döngü",
        "badgeColor": "red",
        "keywords": ["lenfosit makrofaj döngüsü", "il-12", "ifn-gama", "antijen sunumu"],
        "lead": "Kronik enflamasyonun aylarca kendi kendini besleyerek devam etmesinin altında T lenfositler ile makrofajlar arasındaki iki yönlü pozitif geri bildirim yatar.",
        "spotPearls": [
            "Makrofaj T hücresine antijeni sunar ve İNTERLÖKİN-12 (IL-12) salgılar.",
            "IL-12 ile aktive olan T hücresi İNTERFERON-GAMA (IFN-γ) salgılar; IFN-γ ise makrofajı daha da hiddetlendirir (Kendi kendini besleyen döngü).",
            "Bu iki yönlü sinyalleşme kırılamadığında doku hasarı kronikleşir ve granülomlar oluşur."
        ],
        "keyBullets": [
            {"title": "1. Adım: Antijen Sunumu", "desc": "Makrofaj mikrobu fagositoz eder, parçalar ve MHC Sınıf II molekülü üzerinde T Hücre Reseptörüne (TCR) sunar."},
            {"title": "2. Adım: Makrofajdan IL-12 Deşarjı", "desc": "Makrofaj IL-12 salgılayarak naif CD4+ T hücrelerinin Th1 fenotipine farklılaşmasını emreder."},
            {"title": "3. Adım: T Hücresinden IFN-γ Yanıtı", "desc": "Th1 hücresi IFN-γ dökerek makrofajı M1 fenotipinde süper-aktive eder. Makrofaj daha çok TNF ve IL-1 üretir."},
            {"title": "Tersiyer Lenfoid Organlar", "desc": "Uzamış lenfosit-makrofaj göçü romatoid eklemde veya Hashimoto tiroiditinde lenf nodu benzeri germinal merkezler (tersiyer lenfoid yapılar) oluşturur."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-19",
                "question": "Lenfosit-makrofaj pozitif geri bildirim döngüsünde makrofajın T hücresine, T hücresinin de makrofaja gönderdiği iki ana sitokin sırasıyla hangileridir?",
                "answer": "Makrofaj -> T hücresine: İNTERLÖKİN-12 (IL-12). T hücresi -> Makrofaja: İNTERFERON-GAMA (IFN-γ).",
                "hint": "Makrofaj IL-12 atar, T hücresi IFN-gama ile yanıt verir."
            },
            {
                "id": "fc-ci-20",
                "question": "Romatoid Artritli bir eklemin sinoviyasında lenf nodunu taklit eden germinal merkezli lenfoid agregatların birikmesine ne ad verilir?",
                "answer": "Tersiyer Lenfoid Yapılar (Tersiyer Lenfoid Organogenez / Ektopik Lenfoid Foliküller). Uzamış kronik enflamasyonun lokal dokuda lenf nodu kurmasıdır.",
                "hint": "Ektopik lenfoid folikül oluşumu."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "Kronik Enflamasyonun Diğer Hücreleri: Plazma Hücreleri ve Eozinofiller",
        "subtitle": "Russel cisimcikleri, IgE bağımlı parankimal infiltrasyon ve Major Basic Protein",
        "badge": "Hücresel Kadro",
        "badgeColor": "violet",
        "keywords": ["plazma hücresi", "russel cisimciği", "eozinofil", "major basic protein"],
        "lead": "Kronik yangı odağında makrofaj ve T hücrelerine; antikor fabrikası plazma hücreleri ile parazit/alerji uzmanı eozinofiller eşlik eder.",
        "spotPearls": [
            "PLAZMA HÜCRELERİ: Antijenik uyarının devamında B hücrelerinden gelişir; arabatekeri/saat kadranı çekirdeği ve yoğun immünoglobulin yüklü RUSSEL CİSİMCİKLERİ içerir.",
            "EOZİNOFİLLER: Parazit enfeksiyonlarında ve IgE aracılı alerjilerde (Astım) başroldedir; granüllerinde parazit duvarını eriten MAJOR BASİC PROTEİN (MBP) taşır."
        ],
        "keyBullets": [
            {"title": "Plazma Hücresi Morfolojisi", "desc": "Eksantrik yerleşimli nükleus, nükleus kenarında kaba kromatin blokları (araba tekeri) ve bol bazofilik sitoplazma ile belirgin perinükleer solukluk (Golgi zonu)."},
            {"title": "Russel Cisimcikleri", "desc": "Endoplazmik retikulum lümeninde aşırı miktarda sentezlenip biriken immünoglobulinlerin oluşturduğu parlak eozinofilik küresel inklüzyonlardır."},
            {"title": "Eozinofil Eotaksin Aksı", "desc": "Eotaksin kemokini ile dokuya çağrılır. Granüllerindeki MBP parazitleri öldürürken bronş epitelini dökerek astım krizine neden olur."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-21",
                "question": "Histopatolojide plazma hücresi sitoplazmasında izlenen, immünoglobulin birikimiyle dolu parlak pembe yuvarlak kitlelere ne ad verilir?",
                "answer": "RUSSEL CİSİMCİKLERİ (Russell bodies). Eğer çekirdek içinde birikirse Dutcher cisimciği adını alır.",
                "hint": "Plazma hücresinin antikor deposu = Russel cisimciği."
            },
            {
                "id": "fc-ci-22",
                "question": "Eozinofillerin granüllerinde bulunan ve hem parazitleri öldüren hem de alerjide doku hasarı yapan en önemli sitotoksik protein hangisidir?",
                "answer": "MAJOR BASİC PROTEİN (MBP). Eozinofil katyonik protein (ECP) ve eozinofil peroksidaz ile birlikte çalışır.",
                "hint": "Major Temel Protein."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Granülomatöz Enflamasyon Tanımı ve Oluşum Biyolojisi",
        "subtitle": "Elimine edilemeyen etkenler, Tip IV aşırı duyarlılık ve hücresel duvar örme stratejisi",
        "badge": "Granülom Biyolojisi",
        "badgeColor": "red",
        "keywords": ["granülomatöz enflamasyon", "tip iv aşırı duyarlılık", "epiteloid histiyosit"],
        "lead": "Granülomatöz enflamasyon; konağın kolayca sindiremediği veya fagositozla öldüremediği etkenleri sınırlamak için oluşturduğu özelleşmiş bir kronik yangı paternidir.",
        "spotPearls": [
            "GRANÜLOMATÖZ İNFLAMASYON BİR TİP IV (Gecikmiş Tip) AŞIRI DUYARLILIK REAKSİYONUDUR.",
            "Granülomun temel yapıtaşı modifiye olmuş aktive makrofajlar olan 'EPİTELOİD HİSTİYOSİTLER'dir (Epitel hücresine benzeyen makrofajlar)."
        ],
        "keyBullets": [
            {"title": "Savunma Stratejisi: Duvar Örmek", "desc": "Etken öldürülemiyorsa çevresi epiteloid hücrelerle sımsıkı örülür, dışına lenfosit ve fibroblast barikatı kurularak sistemik yayılım durdurulur."},
            {"title": "Gelişim Süreci", "desc": "T lenfositler dirençli antijeni tanır -> Sürekli IFN-γ salgılar -> Makrofajlar devleşir, lizozomları genişler ve epiteloid hücreye döner."},
            {"title": "Çift Uçlu Kılıç", "desc": "Granülom mikrobu hapseder ama merkezinde kazeöz nekroz açarak akciğer dokusunu kavitasyonla tahrip eder."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-23",
                "question": "Granülomatöz enflamasyon Gell-Coombs sınıflamasına göre hangi tip aşırı duyarlılık reaksiyonudur?",
                "answer": "TİP IV (Hücresel / Gecikmiş Tip Aşırı Duyarlılık Reaksiyonu - Delayed Type Hypersensitivity). Antikorlar değil, T hücreleri ve makrofajlar yürütür.",
                "hint": "Hücresel bağışıklık = Tip IV."
            },
            {
                "id": "fc-ci-24",
                "question": "Bir dokuda 'Granülom' varlığından söz edebilmek için mikroskopta MUTLAKA bulunması gereken temel hücre tipi nedir?",
                "answer": "EPİTELOİD HİSTİYOSİTLER (Aktive makrofaj agregatları). Dev hücreler veya kazeöz nekroz olmasa bile epiteloid histiyosit topluluğu granülom tanısı için şarttır!",
                "hint": "Granülomun vazgeçilmez omurgası epiteloid histiyosittir."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Granülomun Morfolojik Yapısı: Epiteloid Histiyosit ve Dev Hücreler",
        "subtitle": "Langhans dev hücresi (at nalı nükleus) vs Yabancı cisim dev hücresi",
        "badge": "Granülom Mimarisi",
        "badgeColor": "amber",
        "keywords": ["langhans", "yabancı cisim dev hücresi", "epiteloid", "terlik çekirdek"],
        "lead": "Klasik bir granülom mikroskopta merkezden perifere doğru organize katmanlar halinde eşsiz bir mimari sergiler.",
        "spotPearls": [
            "EPİTELOİD HİSTİYOSİT: Geniş soluk pembe sitoplazmalı, sınırları birbirine kaynaşmış, oval/terlik şeklinde veziküler çekirdekli makrofajlardır.",
            "LANGHANS TİPİ DEV HÜCRE: Makrofajların füzyonuyla oluşur; 20-50 çekirdeği hücrenin periferinde 'AT NALI' veya U şeklinde dizilmiştir (Tüberkülozda tipik).",
            "YABANCI CİSİM DEV HÜCRESİ: Çekirdekler sitoplazma içine düzensiz ve dağınık olarak serpilmiştir."
        ],
        "keyBullets": [
            {"title": "Hücresel Füzyon Mekanizması", "desc": "IFN-γ uyarısıyla makrofaj zarları birbiriyle kaynaşarak tek bir dev sitoplazma içinde onlarca çekirdek barındıran dev hücreler üretir."},
            {"title": "Granülomun Tabakaları", "desc": "1) Merkez: Nekroz (varsa), 2) İç halka: Epiteloid histiyositler ve Dev hücreler, 3) Dış halka: T lenfositleri, 4) En dış sınır: Fibroblastlar ve kollajen kuşak."},
            {"title": "Epiteloid Terimi Nereden Gelir?", "desc": "Hücre sınırları kaynaşıp epitel tabakası gibi yanaşık durduğu ve pembe sitoplazması yassı epitele benzediği için bu ad verilmiştir."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-25",
                "question": "Langhans tipi dev hücre ile Yabancı Cisim tipi dev hücre arasındaki nükleer dizilim farkı nedir?",
                "answer": "Langhans dev hücresinde çekirdekler hücrenin çevresinde düzenli bir AT NALI (horseshoe) veya yarım çember şeklinde dizilir. Yabancı cisim dev hücresinde ise çekirdekler sitoplazmada dağınık ve düzensiz yerleşir.",
                "hint": "At nalı şeklinde nükleus = Langhans."
            },
            {
                "id": "fc-ci-26",
                "question": "Işık mikroskobunda epiteloid histiyositlerin çekirdek şekli patolojide neye benzetilir?",
                "answer": "Tabanı düz, ucu yuvarlak 'TERLİK' (slipper-shaped) veya 'ayak izi' şekline benzetilir.",
                "hint": "Terlik benzeri oval çekirdek."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Kazeöz (Kazeifiye) Granülomlar vs Non-Kazeöz Granülomlar",
        "subtitle": "Merkezde aselüler nekrotik enkaz varlığına göre ayırıcı tanı",
        "badge": "Granülom Tipleri",
        "badgeColor": "red",
        "keywords": ["kazeöz granülom", "non-kazeöz granülom", "tüberküloz", "sarkoidoz"],
        "lead": "Granülomlar mikroskopik olarak merkezlerinde kazeöz nekroz bulunup bulunmamasına göre iki büyük diagnostik gruba ayrılır.",
        "spotPearls": [
            "KAZEİFİYE (KAZEÖZ) GRANÜLOM: Merkezinde şekilsiz, aselüler, pembe amorf nükleer enkaz (kazeöz nekroz) barındırır. EN TİPİK ÖRNEĞİ TÜBERKÜLOZDUR.",
            "NON-KAZEİFİYE GRANÜLOM: Merkezinde nekroz YOKTUR; baştan başa canlı epiteloid histiyositlerden oluşur. EN TİPİK ÖRNEKLERİ SARKOİDOZ VE CROHN HASTALIĞIDIR."
        ],
        "keyBullets": [
            {"title": "Kazeöz Nekrozun Gelişimi", "desc": "Tüberküloz basilinin mikolik asit ve kord faktörü ile salınan TNF ve serbest radikaller merkezdeki hücreleri öldürür."},
            {"title": "Bulaşıcılık ve Kavitasyon", "desc": "Kazeöz granülom bronşa açıldığında nekrotik materyal öksürükle atılır; geride oksijenden zengin kaviteler kalır ve basil hızla ürer."},
            {"title": "Non-Kazeöz Paternin Önemi", "desc": "Biyopside kazeöz nekroz olmaması tüberkülozu dışlatmaz; ancak çok sayıda non-kazeöz granülom varlığı Sarkoidoz lehinedir."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-27",
                "question": "Lenf nodu biyopsisinde merkezinde kazeöz nekroz İÇERMEYEN (Non-kazeöz), çok sayıda iyi sınırlı granülom saptanan bir hastada ilk akla gelecek sistemik hastalık nedir?",
                "answer": "SARKOİDOZ! Akciğer ve hiler lenf nodlarını tutan, non-kazeifiye granülomlarla seyreden idiyopatik sistemik hastalıktır.",
                "hint": "Nekrozsuz çıplak granülom = Sarkoidoz."
            },
            {
                "id": "fc-ci-28",
                "question": "Gastrointestinal sistem biyopsisinde 'Non-kazeifiye Granülom' görülmesi Crohn Hastalığı ile Ülseratif Kolit arasında hangisini kesin olarak destekler?",
                "answer": "CROHN HASTALIĞINI destekler! Ülseratif kolitte granülom görülmez; non-kazeöz granülom Crohn hastalığının patognomonik ayrım kriteridir.",
                "hint": "Granülom varsa Crohn, yoksa Ülseratif Kolit."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Yabancı Cisim Granülomları ve Polarize Işık Mikroskopisi",
        "subtitle": "İmmünolojik olmayan reaksiyonlar, sütür, talk, asbest ve çift kırıcılık",
        "badge": "Yabancı Cisim",
        "badgeColor": "amber",
        "keywords": ["yabancı cisim granülomu", "sütür", "polarize ışık", "çift kırıcılık"],
        "lead": "Yabancı cisim granülomları; T hücresi aracılı immün yanıt olmaksızın, fagositoz edilemeyecek büyüklükteki inert maddelerin etrafında gelişir.",
        "spotPearls": [
            "İmmün granülomlardan farkı: T LENFOSİT ARACILI SPESİFİK İMMÜN YANIT YOKTUR.",
            "Polarize ışık mikroskobunda cerrahi sütür iplikleri, talk pudrası veya silika kristalleri PARLAK ÇİFT KIRICILIK (Birefringence) verir ve dev hücrelerin içinde gösterilebilir."
        ],
        "keyBullets": [
            {"title": "Etyolojik Maddeler", "desc": "Cerrahi operasyon dikiş iplikleri (sütür granülomu), cerrahi eldiven talkı, damar içi madde bağımlılarında enjekte edilen partiküller veya asbest lifleri."},
            {"title": "Histopatolojik Dizilim", "desc": "Yabancı cisim dev hücreleri ve epiteloid histiyositler yabancı materyalin yüzeyine doğrudan yapışır; çevre lenfosit halkası immün granülomlara göre çok daha zayıftır."},
            {"title": "Klinik Sorunlar", "desc": "Operasyon sonrası aylar sonra yara yerinde kitle (tümör taklidi) veya batında yapışıklıklara (ileus) neden olabilir."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-29",
                "question": "Yabancı cisim granülomu ile İmmün granülom (enfeksiyöz/otoimmün) arasındaki en temel immünolojik fark nedir?",
                "answer": "Yabancı cisim granülomunda T hücresi aracılı antijene spesifik immün yanıt ve aşırı duyarlılık YOKTUR; reaksiyon fagositoz edilemeyen inert maddeye karşı salt makrofaj yanıtıdır.",
                "hint": "T hücresi ve mikrop yok, sadece yabancı madde var."
            },
            {
                "id": "fc-ci-30",
                "question": "Patolog, şüpheli bir granülomun merkezinde yabancı cisim (örneğin sütür veya talk) olup olmadığını kesinleştirmek için hangi mikroskopi yöntemini kullanır?",
                "answer": "POLARİZE IŞIK MİKROSKOBİSİ. Yabancı kristal ve sentetik lifler polarize ışık altında parlayarak 'çift kırıcılık' (birefringence) sergiler.",
                "hint": "Polarize ışıkta parlayan kristaller."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Granülomatöz Enflamasyonla Seyreden Önemli Hastalıklar",
        "subtitle": "TBC, Lepra, Sifiliz, Kedi Tırmığı, Sarkoidoz ve Crohn ayırıcı tanı matrisi",
        "badge": "Hastalık Matrisi",
        "badgeColor": "indigo",
        "keywords": ["lepra", "sifiliz", "gom", "kedi tırmığı", "bartonella"],
        "lead": "Granülomatöz inflamasyon klinikte sınırlı sayıda özgül hastalık tarafından oluşturulur ve her birinin karakteristik bir histopatolojik imzası vardır.",
        "spotPearls": [
            "TÜBERKÜLOZ: Aselüler kazeöz nekrozlu tüberkül granülomu.",
            "KEDİ TIRMIĞI HASTALIĞI (Bartonella henselae): Merkezinde nötrofillerin bulunduğu YILDIZSI (STELLAT) NEKROTİK GRANÜLOM.",
            "SİFİLİZ (Tersiyer evre): GOM (Gumma) lezyonu; ortada koagülasyon nekrozu, plazma hücre zenginliği ve endarteritis obliterans.",
            "LEPRA (Cüzzam): Mycobacterium leprae; sinir kılıflarını tutan asidorezistan basilli granülomlar."
        ],
        "keyBullets": [
            {"title": "Bartonella Henselae (Kedi Tırmığı)", "desc": "Aksiller veya boyun lenf nodunda ağrılı büyüme. Granülomun ortasında nötrofil mikroapseleri içeren yıldızsı nekroz patognomoniktir."},
            {"title": "Tersiyer Sifiliz ve Gom", "desc": "Karaciğer, kemik veya deride lastik kıvamında nekrotik kitlelerdir. Damar endotel proliferasyonu (endarterit) ve yoğun plazma hücreleri eşlik eder."},
            {"title": "Lepramatöz vs Tüberküloid Lepra", "desc": "Tüberküloid leprada güçlü hücresel yanıt ve tipik granülomlar varken; lepramatöz leprada anerji vardır, köpüksü makrofajlar (Virchow hücreleri) basille doludur."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-31",
                "question": "Genç bir hastanın koltuk altı lenf nodu biyopsisinde merkezinde nötrofiller içeren 'Yıldızsı (Stellat) Nekrotizan Granülom' saptandığında en olası tanı nedir?",
                "answer": "KEDİ TIRMIĞI HASTALIĞI (Cat-scratch disease / Bartonella henselae enfeksiyonu).",
                "hint": "Yıldızsı / stellat süpüratif granülom = Kedi tırmığı."
            },
            {
                "id": "fc-ci-32",
                "question": "Sifilizin tersiyer evresinde görülen granülomatöz lezyona ne ad verilir ve mikroskopisinde hangi lökosit dikkat çeker?",
                "answer": "GOM (Gumma). Mikroskopisinde yoğun PLAZMA HÜCRESİ infiltrasyonu ve küçük damarlarda 'Endarteritis Obliterans' (oblitere edici endarterit) karakteristiktir.",
                "hint": "Gom lezyonu ve plazma hücreleri = Sifiliz."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Tüberküloz Granülomu Patolojisi ve Ghon Kompleksi",
        "subtitle": "Primer enfeksiyon, kazeöz tüberkül, kalsifikasyon ve Ranke kompleksi",
        "badge": "Tüberküloz",
        "badgeColor": "red",
        "keywords": ["ghon kompleksi", "ranke", "kazeöz nekroz", "tüberküloz", "langhans"],
        "lead": "Mycobacterium tuberculosis; granülomatöz yanıtın dünyadaki en yaygın prototipidir ve akciğerde anatomik lezyon zinciri oluşturur.",
        "spotPearls": [
            "GHON ODAĞI: Akciğer subplevral parankiminde (orta lob altı veya alt lob üstü) gelişen kazeöz nekrotik primer odaktır.",
            "GHON KOMPLEKSİ: Ghon odağı + Drene olan hiler lenf nodundaki kazeöz granülomatöz lenfadenitin toplamıdır.",
            "RANKE KOMPLEKSİ: Ghon kompleksinin zamanla kalsifiye ve fibrotik olarak iyileşmiş radyolojik izidir."
        ],
        "keyBullets": [
            {"title": "Mikroskopik Tüberkül Mimarisi", "desc": "Ortada pembe aselüler kazeöz nekroz, etrafında epiteloid histiyositler ve Langhans dev hücreleri, en dışta CD4+ T lenfositleri."},
            {"title": "Özel Boyama: Erlich-Ziehl-Neelsen (EZN)", "desc": "Basil hücre duvarındaki mikolik asit nedeniyle aside dirençlidir (ARB); EZN boyamasında mavi zemin üzerinde parlak kırmızı çomaklar olarak parlar."},
            {"title": "Sekonder (Reaktivasyon) Tüberkülozu", "desc": "Bağışıklık düştüğünde apikal kavitasyonlar, masif doku nekrozu ve hemoptizi (kan tükürme) ile reaktive olur."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-33",
                "question": "Patolojide 'Ghon Kompleksi' hangi iki lezyonun birlikteliğini tanımlar?",
                "answer": "1) Akciğer parankimindeki kazeifiye primer granülom (Ghon odağı), 2) Drenaj bölgesindeki hiler lenf nodu kazeöz tutulumu.",
                "hint": "Akciğer odağı + Hiler lenf nodu = Ghon kompleksi."
            },
            {
                "id": "fc-ci-34",
                "question": "Tüberküloz basilini granülom içinde mikroskopik olarak göstermek için kullanılan altın standart histokimyasal boya hangisidir?",
                "answer": "Ehrlich-Ziehl-Neelsen (EZN) boyası (Aside Dirençli Basil / ARB boyaması). Kırmızı çomaklar şeklinde boyanır.",
                "hint": "ARB boyası = EZN."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Sarkoidoz Patolojisi: 'Çıplak' Non-Kazeöz Granülomlar",
        "subtitle": "Bilateral hiler LAP, Schaumann cisimcikleri, Asteroid cisimcikleri ve Kveim testi",
        "badge": "Sarkoidoz",
        "badgeColor": "violet",
        "keywords": ["sarkoidoz", "schaumann", "asteroid", "non-kazeöz", "kveim"],
        "lead": "Sarkoidoz; bilinmeyen bir antijene karşı gelişen, akciğer ve lenf nodlarını tutan, kazeöz nekroz İÇERMEYEN granülomlarla karakterize sistemik hastalıktır.",
        "spotPearls": [
            "SARKOİDOZ GRANÜLOMLARI 'ÇIPLAK GRANÜLOM' (Naked Granuloma) OLARAK ADLANDIRILIR; çünkü etraflarında kalın bir lenfosit/fibroblast manşonu bulunmaz ve nekroz içermez.",
            "Dev hücrelerin sitoplazmasında iki karakteristik inklüzyon görülebilir: SCHAUMANN CİSİMCİKLERİ (kalsiyum ve protein laminasyonları) ve ASTEROİD CİSİMCİKLERİ (yıldızsı inklüzyonlar)."
        ],
        "keyBullets": [
            {"title": "Bilateral Hiler Lenfadenopati (BHL)", "desc": "Akciğer grafisinde her iki hilusta simetrik patates benzeri dev lenf nodu büyümeleri sarkoidozun en tipik radyolojisidir."},
            {"title": "Non-Kazeöz Granülomlar", "desc": "Granülomlar tekdüze, sıkıca paketlenmiş epiteloid histiyositlerden oluşur. Nekroz kesinlikle izlenmez."},
            {"title": "Kalsiyum Metabolizması Bozukluğu", "desc": "Granülomdaki epiteloid histiyositler 1-alfa hidroksilaz eksprese ederek kontrolsüz D vitamini üretir; hastalarda HİPERKALSEMİ ve hiperkalsiüri gelişir."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-35",
                "question": "Sarkoidozlu bir hastanın dev hücreleri içinde izlenen konsantrik kalsiyum ve demir katmanlarından oluşan inklüzyona ne ad verilir?",
                "answer": "SCHAUMANN CİSİMCİĞİ. Yıldızsı sitoplazmik inklüzyona ise Asteroid Cisimciği denir.",
                "hint": "Schaumann = Kalsiyum katmanı; Asteroid = Yıldızsı inklüzyon."
            },
            {
                "id": "fc-ci-36",
                "question": "Sarkoidoz hastalarında serumda kalsiyum yüksekliği (hiperkalsemi) görülmesinin biyokimyasal mekanizması nedir?",
                "answer": "Granülomdaki aktive epiteloid histiyositlerin otonom olarak '1-alfa hidroksilaz' enzimi sentezlemesi ve kontrolsüz biçimde D vitaminini aktif forma (1,25-(OH)2 D3) dönüştürmesidir.",
                "hint": "Granülomlar kontrolsüz D vitamini üretir."
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "Kronik Enflamasyonun Kaçınılmaz Sonu: Doku Fibrozisi",
        "subtitle": "Miyofibroblast aktivasyonu, ekstrasellüler matriks yığılması ve organ sklerozu",
        "badge": "Fibrogenez",
        "badgeColor": "amber",
        "keywords": ["fibrozis", "tgf-beta", "miyofibroblast", "ekstrasellüler matriks", "kolajen"],
        "lead": "Kronik enflamasyon dokuda durdurulamadığında; parenkimal hücrelerin yerini kollajenden zengin yoğun fibröz bağ dokusu alır ve organ fonksiyonel olarak iflas eder.",
        "spotPearls": [
            "FİBROGENEZİN MASTER DÜZENLEYİCİSİ TRANSFORMİNG GROWTH FACTOR-BETA'DIR (TGF-β).",
            "TGF-β; fibroblastları MİYOFİBROBLASTLARA dönüştürür, Tip I ve Tip III kollajen sentezini patlatır ve metalloproteinazları baskılayarak kollajen yıkımını kilitler."
        ],
        "keyBullets": [
            {"title": "Parankim Hücre Kaybı", "desc": "Karaciğerde siroz, böbrekte kronik interstisyel nefrit, akciğerde bal peteği akciğeri (pulmoner fibrozis) kronik iltihabın nihai fibrotik sonucudur."},
            {"title": "Miyofibroblastların Rolü", "desc": "Hem alfa-düz kas aktini (alfa-SMA) ile yara kontraksiyonu yaparlar hem de masif ekstraselüler matriks proteini salgılarlar."},
            {"title": "Kalıcı Fonksiyon Kaybı", "desc": "Skar dokusu yapısal bütünlüğü korur ancak hiçbir parankimal fonksiyonu (filtrasyon, gaz değişimi, metabolizma) yerine getiremez."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-37",
                "question": "Patolojide doku fibrozisini başlatan, fibroblast proliferasyonunu artıran ve kollajen yıkımını engelleyen en güçlü sitokin hangisidir?",
                "answer": "TGF-BETA (Transforming Growth Factor-Beta)! M2 makrofajlar ve trombositler tarafından salgılanır.",
                "hint": "Fibrozisin ana büyüme faktörü."
            },
            {
                "id": "fc-ci-38",
                "question": "Fibrozis gelişen bir dokuda ekstraselüler matriks sentezleyen ve kasılma yeteneğiyle skarı büzüştüren temel efektör hücre nedir?",
                "answer": "MİYOFİBROBLASTLAR (Myofibroblasts). Sitoplazmalarında düz kas aktini taşırlar.",
                "hint": "Fibroblast + Düz kas hücresi = Miyofibroblast."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Doku Onarımına Giriş: Rejenerasyon vs Skarlaşma",
        "subtitle": "Kök hücreler, ekstrasellüler iskelet intaktlığı ve granülasyon dokusu mimarisi",
        "badge": "Onarım Prensipleri",
        "badgeColor": "sky",
        "keywords": ["rejenerasyon", "skarlaşma", "granülasyon dokusu", "anjiyogenez", "labile"],
        "lead": "Doku zedelenmesinden sonra vücut iki yoldan biriyle onarım yapar: Dokunun birebir kopyasıyla yenilenmesi (Rejenerasyon) veya bağ dokusu yaması konulması (Skarlaşma).",
        "spotPearls": [
            "REJENERASYON: Bölünme yeteneği olan hücrelerde (labile/stabil) ve BAZAL MEMBRAN SAĞLAMSA gelişir; geride hiçbir hasar kalmaz.",
            "SKARLAŞMA: Kalıcı (bölünmeyen) dokularda (kalp kası, nöron) veya bazal membran/iskelet parçalanmışsa gelişir; yerini fibröz bağ dokusu alır.",
            "GRANÜLASYON DOKUSU onarımın pembe, granüler, yumuşak erken evresidir (Yeni damarlar + Genç fibroblastlar + Ödem)."
        ],
        "keyBullets": [
            {"title": "Hücre Çoğalma Kapasitesi Sınıflaması", "desc": "1) Labile (sürekli bölünen: kemik iliği, GIS epiteli), 2) Stabil (uyaranla bölünen: hepatosit, tübül), 3) Kalıcı/Permanent (asla bölünmeyen: kardiyomiyosit, nöron)."},
            {"title": "Matriks İskeletinin Önemi", "desc": "Karaciğer toksin hasarında bazal membran sağlamsa tam rejenerasyon olur; cerrahi keside veya absede iskelet çöktüğü için skar kalır."},
            {"title": "Granülasyon Dokusu Bileşenleri", "desc": "H&E boyasında yüzeye dik uzanan endotel tomurcukları (anjiyogenez), gevşek interstisyel ödem ve araya serpişmiş fibroblastlar izlenir."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-39",
                "question": "Kalp kası enfarktüsü sonrasında miyokard dokusu neden rejenerasyonla değil daima fibröz skar ile onarılır?",
                "answer": "Çünkü kardiyomiyositler 'Kalıcı (Permanent)' hücrelerdir; mitoz bölünme yetenekleri yoktur. Ölen kas liflerinin yerini ancak fibroblastik bağ dokusu (skar) doldurabilir.",
                "hint": "Kalp kası bölünemez, tek çare skardır."
            },
            {
                "id": "fc-ci-40",
                "question": "Yara tabanında oluşan genç 'Granülasyon Dokusu' mikroskobik olarak hangi 3 temel yapıdan oluşur?",
                "answer": "1) Yeni oluşan proliferatif kılcal damarlar (Anjiyogenez), 2) Aktif prolifere olan fibroblastlar, 3) Gevşek, ödemli ekstraselüler matriks ve az sayıda lökosit.",
                "hint": "Damar tomurcuğu + Fibroblast + Ödem."
            }
        ]
    },
    {
        "slideNumber": 21,
        "title": "Yara İyileşmesi Kalıpları: Primer vs Sekonder İyileşme",
        "subtitle": "Cerrahi insizyon vs geniş doku kaybı ve skar komplikasyonları (Keloid)",
        "badge": "Yara İyileşmesi",
        "badgeColor": "red",
        "keywords": ["primer iyileşme", "sekonder iyileşme", "keloid", "hipertrofik skar", "kontraksiyon"],
        "lead": "Kutanöz yara iyileşmesi; yaranın cerrahi temiz dikişle mi kapatıldığına yoksa açık bırakılan geniş doku kaybı mı olduğuna göre iki farklı klinikle yürür.",
        "spotPearls": [
            "PRİMER İYİLEŞME (İlk niyetle): Temiz cerrahi kesiler; yara dudakları birbirine yaklaştırılmıştır; minimal granülasyon dokusu ve incecik çizgi skar bırakır.",
            "SEKONDER İYİLEŞME (İkinci niyetle): Geniş enfekte doku kayıpları, yanıklar ve apseler; devasa granülasyon dokusu, MİYOFİBROBLASTİK KONTRAKSİYON ve geniş çirkin skar bırakır.",
            "KELOİD: Yaranın orijinal sınırlarını aşarak çevre sağlam deriye taşan, Tip I ve Tip III kollajen yüklü anormal tümöral skar büyümesidir."
        ],
        "keyBullets": [
            {"title": "Yara Kontraksiyonu", "desc": "Sekonder iyileşmede yara tabanındaki miyofibroblastlar kasılarak yara alanını %70-80 oranında büzüştürür ve küçültür."},
            {"title": "Yara Direnci Zamanlaması", "desc": "1. haftada dikişler alındığında yara gerilme direnci normal cildin %10'udur; 3. ayda maksimum %70-80'e ulaşır ve asla %100 olmaz."},
            {"title": "Hipertrofik Skar vs Keloid Ayrımı", "desc": "Hipertrofik skar yara sınırları içinde kalır ve zamanla gerileyebilir. Keloid ise yara sınırlarını aşar, gerilemez ve cerrahi eksizyonla tekrarlar."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-41",
                "question": "Keloid ile Hipertrofik Skar arasındaki en kritik patolojik ve klinik fark nedir?",
                "answer": "Hipertrofik skar yaranın orijinal sınırları içinde kalır ve zamanla küçülebilir. KELOİD ise orijinal yara sınırlarını taşarak çevre sağlam deriye doğru invaziv tümör gibi yayılır, gerilemez ve afrikoid ırkta daha sıktır.",
                "hint": "Sınırı aşıyorsa Keloid, sınırda kalıyorsa Hipertrofik skar."
            },
            {
                "id": "fc-ci-42",
                "question": "Geniş bir cilt yanığında yara açıklığını haftalar içinde büzüştürerek küçülten temel hücre hangisidir?",
                "answer": "MİYOFİBROBLASTLAR. Sitoplazmalarındaki aktin-miyozin kasılma sistemiyle yara kenarlarını merkeze doğru çekerler (Yara Kontraksiyonu).",
                "hint": "Yarayı büzüştüren miyofibroblasttır."
            }
        ]
    },
    {
        "slideNumber": 22,
        "title": "Kronik Enflamasyon ve Non-Klasik Hastalıklar Entegrasyonu",
        "subtitle": "Karsinogenez, Alzheimer, Metabolik Sendrom ve Kurul 1 Büyük Sentezi",
        "badge": "Sentez ve Vizyon",
        "badgeColor": "indigo",
        "keywords": ["non-klasik enflamasyon", "kanser", "alzheimer", "ateroskleroz"],
        "lead": "Modern tıpta kronik enflamasyon sadece enfeksiyon ve otoimmüniteyle sınırlı değildir; aterosklerozdan kansere ve nörodejenerasyona kadar çağımızın tüm kronik hastalıklarının ortak paydasıdır.",
        "spotPearls": [
            "KRONİK ENFLAMASYON VE KANSER BAĞLANTISI: Sürekli hücre proliferasyonu, ROS kaynaklı DNA mutasyonları ve büyüme faktörleri karsinogenezi tetikler (Barrett özofagusu -> Adenokarsinom; Ülseratif Kolit -> Kolon kanseri).",
            "Metabolik sendrom ve Tip 2 Diyabette yağ dokusu makrofajlarından salınan TNF ve IL-6 periferik insülin direncini kalıcı hale getirir.",
            "Alzheimer hastalığında beyinde biriken amiloid-beta plakları mikrogliayı uyararak kronik nöro-enflamasyon ve sinaptik ölüm üretir."
        ],
        "keyBullets": [
            {"title": "Onkojenik Yangı Aksı", "desc": "H. pylori gastriti mide kanserine ve MALT lenfomaya; Hepatit B/C enfeksiyonu hepatosellüler karsinoma zemin hazırlar."},
            {"title": "Aterosklerozda Düşük Dereceli Yangı", "desc": "Plak içi M1 makrofajlar köpük hücrelerine dönüşür; salınan metalloproteinazlar fibröz başlığı eriterek plak rüptürü ve MI yapar."},
            {"title": "Kurul 1 Entegrasyonu", "desc": "Hücre Hasarı -> Apoptoz/Nekroz -> Akut Yangı -> Kronik Yangı -> Granülomatöz Reaksiyon -> Fibrozis zinciri patolojinin ana omurgasıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-ci-43",
                "question": "Kronik enflamasyonun kanser (malignite) gelişimini tetiklemesindeki temel mekanizma nedir?",
                "answer": "Sürekli hücre yenilenmesi (mitoz) sırasında DNA replikasyon hatalarının artması, yangı hücrelerinden salınan serbest oksijen radikallerinin (ROS) DNA'yı mutasyona uğratması ve büyüme faktörlerinin apoptozu engellemesidir.",
                "hint": "Sürekli bölünme + Serbest radikal DNA hasarı = Malignite."
            },
            {
                "id": "fc-ci-44",
                "question": "Kronik H. pylori gastritinin zemin hazırladığı iki temel malign tümör nedir?",
                "answer": "1) Mide Adenokarsinomu, 2) Mide MALT Lenfoması (Mukozayla ilişkili lenfoid doku lenfoması).",
                "hint": "Hem karsinom hem de B hücreli lenfoma yapabilir."
            }
        ]
    }
]

COMPARISON_TABLES = {
    2: {
        "title": "Akut Enflamasyon ile Kronik Enflamasyonun Karşılaştırmalı Özellikleri",
        "headers": ["Özellik", "Akut Enflamasyon", "Kronik Enflamasyon"],
        "rows": [
            ["Başlangıç Hızı", "Hızlı (dakikalar veya saatler içinde)", "Yavaş ve sinsi (günler, haftalar içinde)"],
            ["Hücresel İnfiltrat", "Başlıca NÖTROFİLLER", "MAKROFAJLAR, LENFOSİTLER, Plazma hücreleri"],
            ["Doku Hasarı ve Fibrozis", "Hafif ve kendini sınırlar", "Şiddetli, ilerleyici ve kalıcı FİBROZİS (Skar)"],
            ["Lokal ve Sistemik Belirtiler", "Belirgin (Kızarıklık, sıcaklık, şişlik, ağrı, yüksek ateş)", "Daha silik, subfebril ateş, yorgunluk, kilo kaybı"],
            ["Vasküler Olaylar", "Vazodilatasyon ve yüksek geçirgenlik (ödem/eksüda)", "Yeni damar oluşumu (Anjiyogenez)"],
            ["Sonlanım", "Tam iyileşme (rezolüsyon), apse veya kronikleşme", "Doku destrüksiyonu, skarlaşma ve organ yetmezliği"]
        ]
    },
    7: {
        "title": "Klasik (M1) vs Alternatif (M2) Makrofaj Aktivasyonu Matrisi",
        "headers": ["Kriter", "Klasik Makrofaj (M1 Fenotipi)", "Alternatif Makrofaj (M2 Fenotipi)"],
        "rows": [
            ["Tetikleyici Sitokinler", "IFN-γ (Th1 hücrelerinden), Mikrobiyal TLR ligandları (LPS)", "IL-4 ve IL-13 (Th2 hücrelerinden ve eozinofillerden)"],
            ["Temel Biyolojik Görevi", "Mikropları öldürmek, fagositoz, aktif yangıyı alevlendirmek", "Doku onarımı, yangıyı yatıştırmak, fibrozisi başlatmak"],
            ["Salgıladığı Toksik Mediyatörler", "Yüksek oranda ROS, NO (iNOS ile) ve lizozomal enzimler", "Yoktur (Mikrobisidal aktivitesi düşüktür)"],
            ["Salgıladığı Büyüme Faktörleri", "Minimal; pro-enflamatuvar IL-1, IL-12, IL-23, TNF salgılar", "Yüksek TGF-β, VEGF, PDGF, FGF ve IL-10"],
            ["L-Arginin Metabolizması", "iNOS ile NİTRİK OKSİT (NO) üretir", "Arginaz ile kollajen sentezi için PROLİN üretir"],
            ["Patolojideki Yansımaları", "Kronik doku nekrozu, kavitasyon, otoimmün harabiyet", "Organ sirozu, akciğer fibrozisi, keloid ve skar oluşumu"]
        ]
    },
    14: {
        "title": "Kazeifiye (Kazeöz) ve Non-kazeifiye Granülomların Karşılaştırılması",
        "headers": ["Özellik", "Kazeifiye Granülom", "Non-kazeifiye Granülom"],
        "rows": [
            ["Merkezi Nekroz", "VARDIR (aselüler, peynirimsi pembe amorf enkaz)", "YOKTUR (merkezde nekroz bulunmaz)"],
            ["Hücresel Bütünlük", "Merkezdeki hücreler tamamen ölmüş ve silinmiştir", "Tüm granülom alanı canlı epiteloid histiyositlerle doludur"],
            ["En Tipik Etyolojik Neden", "Mycobacterium tuberculosis (Tüberküloz), Mantarlar", "Sarkoidoz, Crohn Hastalığı, Berilyozis"],
            ["Kavitasyon Riski", "Yüksektir; nekrotik materyal bronşa dökülüp kavite açar", "Kavitasyon görülmez; fibrotik kitleye dönüşür"],
            ["Dev Hücre Tipi", "Langhans dev hücreleri sıktır (At nalı çekirdek)", "Langhans ve yabancı cisim dev hücreleri (Schaumann/Asteroid)"],
            ["Mikroorganizma Varlığı", "Aside Dirençli Basil (ARB/EZN) ile gösterilebilir", "Mikrop saptanamaz (İmmünolojik / non-enfeksiyöz)"]
        ]
    },
    16: {
        "title": "Granülomatöz Enflamasyon Yapan Hastalıklar ve Histopatolojik Özellikleri",
        "headers": ["Hastalık", "Etyolojik Etken", "Doku Reaksiyonu ve Karakteristik Histopatoloji"],
        "rows": [
            ["Tüberküloz", "Mycobacterium tuberculosis", "Merkezde kazeöz nekrozlu tüberkül granülomu, Langhans dev hücreleri, EZN(+)"],
            ["Sarkoidoz", "Bilinmeyen otoantijen / genetik", "Nekrozsuz çıplak granülomlar, Schaumann ve Asteroid cisimcikleri, BHL"],
            ["Kedi Tırmığı Hastalığı", "Bartonella henselae", "Merkezinde nötrofil mikroapseleri içeren yıldızsı (stellat) nekrotizan granülom"],
            ["Sifiliz (Gom)", "Treponema pallidum", "Tersiyer evrede lastiksi nekrotik gomlar, yoğun plazma hücreleri, endarterit"],
            ["Lepra (Cüzzam)", "Mycobacterium leprae", "Periferik sinirleri tutan granülomlar; Tüberküloidde granülom(+), Lepramatözde köpüksü histiyosit"],
            ["Crohn Hastalığı", "Bağırsak mikrobiyotası / immünite", "Bağırsak duvarında tüm katları tutan transmural non-kazeifiye granülomlar"],
            ["Yabancı Cisim Reaksiyonu", "Sütür, talk, asbest, silika", "Yabancı cisim dev hücreleri, polarize ışıkta parlayan çift kırıcı kristaller"]
        ]
    },
    21: {
        "title": "Primer (İlk Niyetle) ve Sekonder (İkinci Niyetle) Yara İyileşmesi",
        "headers": ["Kriter", "Primer İyileşme (Primary Intention)", "Sekonder İyileşme (Secondary Intention)"],
        "rows": [
            ["Yara Tipi ve Açıklığı", "Temiz cerrahi kesi; yara kenarları dikişle birleştirilmiş", "Büyük doku kaybı, enfekte yara, yanık, derin ülser"],
            ["Granülasyon Dokusu Miktarı", "Minimal miktarda granülasyon dokusu gerekir", "Çok geniş, devasa granülasyon dokusu tabanı oluşur"],
            ["Yara Kontraksiyonu", "Yoktur veya ihmal edilebilir düzeydedir", "Miyofibroblastlar aracılığıyla belirgin (%70-80 büzüşme)"],
            ["Skar Görünümü ve Seviyesi", "İnce, lineer, estetik açıdan kabul edilebilir çizgi skar", "Geniş, kabarık, çekintili ve şekilsiz büyük skar dokusu"],
            ["Enfeksiyon Riski", "Düşüktür (steril cerrahi ortam)", "Yüksektir (uzamış açık yara yüzeyi)"],
            ["İyileşme Süresi", "Hızlı (günler içinde epitelize olur)", "Çok yavaş (haftalar veya aylar sürer)"]
        ]
    }
}

def build_deck():
    slides = []
    total_matched_questions = 0

    for s_raw in SLIDES_DATA:
        s_num = s_raw["slideNumber"]
        title = s_raw["title"]
        subtitle = s_raw["subtitle"]
        badge = s_raw["badge"]
        badge_color = s_raw["badgeColor"]
        keywords = s_raw["keywords"]
        lead = s_raw["lead"]
        spot_pearls = s_raw["spotPearls"]
        key_bullets = s_raw["keyBullets"]
        flashcards = s_raw["flashcards"]

        matched_qs = find_matched_questions(keywords, max_count=2)
        total_matched_questions += len(matched_qs)

        narrative_lines = []
        narrative_lines.append(f"### {title}")
        narrative_lines.append(f"#### {subtitle}")
        narrative_lines.append("")
        narrative_lines.append(lead)
        narrative_lines.append("")
        narrative_lines.append("💡 **Klinik ve Sınav Odaklı Spot İpuçları:**")
        for p in spot_pearls:
            narrative_lines.append(f"• {p}")
        narrative_lines.append("")
        narrative_lines.append("#### Detaylı Müfredat Maddeleri ve Tıbbi Patoloji Sentezi")
        for b in key_bullets:
            narrative_lines.append(f"• **{b['title']}:** {b['desc']}")

        synthesis_narrative = "\n".join(narrative_lines).strip()

        core_content = {
            "keyBullets": key_bullets
        }

        if s_num in COMPARISON_TABLES:
            core_content["table"] = COMPARISON_TABLES[s_num]

        slide_obj = {
            "slideNumber": s_num,
            "title": title,
            "subtitle": subtitle,
            "badge": badge,
            "badgeColor": badge_color,
            "synthesisNarrative": synthesis_narrative,
            "flashcards": flashcards,
            "coreContent": core_content,
            "spotPearls": spot_pearls,
            "relatedQuestions": matched_qs,
            "aiPromptSuggestions": [
                f"{title} konusundaki en kritik TUS ve Kurul soruları nelerdir?",
                f"Robbins patolojiye göre {title} mekanizmasını açıkla.",
                f"Bu slayttaki granülomatöz bulgular klinikte hangi hastalıklarla prezente olur?"
            ]
        }
        slides.append(slide_obj)

    deck_obj = {
        "id": "learn-kronik-enflamasyon",
        "title": "Kronik Enflamasyon, Granülomlar ve Doku Onarımı Patolojisi",
        "shortTitle": "Kronik Enflamasyon & Granülom",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 - Hücre Hasarı, İltihap ve Neoplazi (TIP 301)",
        "instructor": "Prof. Dr. Hikmet Keleş (Tıbbi Patoloji AD)",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_matched_questions,
        "totalFlashcardsCount": len(slides) * 2,
        "themeColor": "indigo",
        "overview": (
            "Dönem 3 Kurul 1 Patoloji müfredatının yangı ve immünopatoloji bloğu; Prof. Dr. Hikmet Keleş'in "
            "resmi amfi ders notları (Ders 8) ve Robbins Temel Patoloji ilkeleri doğrultusunda %500 derinlikte "
            "yapılandırılmıştır. Kronik enflamasyonun 3 temel nedeni ve 3 morfolojik özelliği, mononükleer "
            "fagositik sistem, Klasik M1 vs Alternatif M2 makrofaj aktivasyon kaskatları, Th1/Th2/Th17 lenfosit "
            "sitokin imzaları, makrofaj-lenfosit kısır döngüsü, Russel cisimcikleri, Granülomatöz enflamasyon "
            "(Tip IV aşırı duyarlılık), Epiteloid histiyositler, Langhans dev hücreleri, kazeifiye vs non-kazeifiye "
            "ayrımı, granülomatöz hastalıklar matrisi (TBC, Ghon kompleksi, Sarkoidoz, Kedi Tırmığı, Sifiliz), "
            "TGF-beta aracılı doku fibrozisi, granülasyon dokusu ve yara iyileşmesi (Primer vs Sekonder, Keloid) "
            "22 kapsamlı interaktif slayt, 44 3D akıl kartı ve 5 karşılaştırma tablosu ile eksiksiz sunulmaktadır."
        ),
        "highYieldPearls": [
            "Kronik enflamasyonda AKTİF İLTİHAP, DOKU YIKIMI ve ONARIM GİRİŞİMLERİ (fibrozis/anjiyogenez) eşzamanlı olarak birlikte yürür.",
            "M1 makrofajlar IFN-γ ile aktive olup mikrop öldürür (NO/ROS); M2 makrofajlar IL-4/IL-13 ile aktive olup TGF-β ile FİBROZİS ve onarım yapar.",
            "GRANÜLOMATÖZ İNFLAMASYON BİR TİP IV (Gecikmiş Tip) AŞIRI DUYARLILIK REAKSİYONUDUR; temel hücre 'Epiteloid Histiyosit'tir.",
            "At nalı şeklinde nükleer dizilim = LANGHANS DEV HÜCRESİ (Tüberküloz); Dağınık nükleer dizilim = Yabancı cisim dev hücresi.",
            "Tüberkülozda kazeöz nekrozlu granülom görülürken; SARKOİDOZ ve CROHN hastalığında KAZEOZ NEKROZ İÇERMEYEN granülomlar görülür.",
            "Yaranın orijinal sınırlarını aşarak çevre deriye taşan kollajenöz büyüme KELOİD olarak adlandırılır."
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for Kronik Enflamasyon ve Granülomlar...")
    deck = build_deck()
    print(f"Generated deck with {len(deck['slides'])} slides and {deck['totalFlashcardsCount']} flashcards.")

    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    found_idx = -1
    for i, d in enumerate(decks):
        if d.get('id') == deck['id']:
            found_idx = i
            break

    if found_idx >= 0:
        decks[found_idx] = deck
        print(f"Updated existing deck at index {found_idx} (ID: {deck['id']})")
    else:
        decks.append(deck)
        print(f"Appended new deck (ID: {deck['id']})")

    with open(DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    if os.path.exists(META_PATH):
        with open(META_PATH, 'r', encoding='utf-8') as f:
            meta_list = json.load(f)
        
        meta_entry = {
            "id": deck["id"],
            "title": deck["title"],
            "shortTitle": deck["shortTitle"],
            "discipline": deck["discipline"],
            "committee": deck["committee"],
            "instructor": deck["instructor"],
            "totalSlides": deck["totalSlides"],
            "matchedQuestionsCount": deck["matchedQuestionsCount"],
            "totalFlashcardsCount": deck["totalFlashcardsCount"],
            "themeColor": deck["themeColor"],
            "overview": deck["overview"]
        }

        m_idx = -1
        for i, m in enumerate(meta_list):
            if m.get('id') == deck['id']:
                m_idx = i
                break
        if m_idx >= 0:
            meta_list[m_idx] = meta_entry
        else:
            meta_list.append(meta_entry)

        with open(META_PATH, 'w', encoding='utf-8') as f:
            json.dump(meta_list, f, ensure_ascii=False, indent=2)
        print("Updated learning_decks_meta.json successfully.")

    # Update queue file
    if os.path.exists(QUEUE_PATH):
        with open(QUEUE_PATH, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        for item in queue:
            if item.get('id') == deck['id']:
                item['status'] = 'completed'
                item['slidesCount'] = len(deck['slides'])
                item['detailLevel'] = '500%'
            elif item.get('id') == 'learn-hucresel-adaptasyon-ve-hu':
                item['status'] = 'next_in_queue'
        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Updated learning_batch_queue.json: Kronik Enflamasyon marked as completed, Hücresel Adaptasyon next!")

    print("Success! Chronic inflammation deck generation completed.")

if __name__ == '__main__':
    main()
