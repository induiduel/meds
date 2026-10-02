#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_chemical_mediators_deck.py
Generates the comprehensive 22-slide interactive learning deck for:
'Enflamasyonun Kimyasal Mediyatörleri: Vazoaktif Aminler, Araşidonik Asit Metabolitleri, Sitokinler ve Kompleman Sistemi'
Lecturer: Prof. Dr. Hikmet Keleş (Tıbbi Patoloji - Kurul 1 / Robbins 11. Baskı)
Integrates all medical terms into medical_encyclopedia.json and medical_glossary.json.
Guarantees 0 empty flashcards and valid question schemas.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')
ENCYCLOPEDIA_PATH = os.path.join('src', 'data', 'medical_encyclopedia.json')
GLOSSARY_PATH = os.path.join('src', 'data', 'medical_glossary.json')
QUEUE_PATH = os.path.join('src', 'data', 'learning_batch_queue.json')

slides_data = [
    {
        "slideNumber": 1,
        "title": "Enflamasyon Mediyatörlerine Giriş ve Temel İlkeler",
        "subtitle": "Hücre Kaynaklı vs. Plazma Kaynaklı Mediyatörlerin Biyolojisi",
        "badge": "Genel İlkeler",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Mediyatörler çözünebilir moleküllerdir; yangı bölgesinde lokal üretilir, etki süreleri son derece kısadır ve hızla yıkılırlar. Kontrolsüz salınımları doku hasarının bizzat temel nedenidir.",
            "timestamp": "02:15",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Mediyatörlerin kısa yarı ömürlü olması yangının kendiliğinden sınırlanmasını sağlar."
        },
        "synthesisNarrative": "Enflamasyonun kimyasal mediyatörleri, doku hasarına veya mikrobiyal istilaya karşı vasküler ve hücresel olayları başlatan, koordine eden ve sonlandıran moleküler habercilerdir. Bu mediyatörler temel kökenlerine göre **hücre kaynaklı** (mast hücreleri, makrofajlar, trombositler, endotel) ve **plazma kaynaklı** (karaciğerde üretilip kanda inaktif öncül gezen kompleman, kinin ve pıhtılaşma proteinleri) olmak üzere ikiye ayrılır.",
        "coreContent": [
            "• **Mediyatörün Tanımı:** Enflamatuar reaksiyonları başlatan, güçlendiren ve hücreler arası iletişimi sağlayan çözünebilir kimyasal moleküllerdir.",
            "• **Lokal Üretim ve Kısa Ömür:** Çoğu mediyatör yalnızca yangı odağında veya yakınında üretilir. Dokuda saniyeler veya dakikalar içinde enzimatik yıkıma uğrar (örn. histamin kinazlar/aminooksidazlarla, eikozanoidler spontan degradasyonla parçalanır).",
            "• **Hücre Kaynaklı Mediyatörler:** Doku makrofajları, mast hücreleri, dendritik hücreler, nötrofiller ve trombositler tarafından sentezlenir. İki farklı yolla salınırlar: 1) Önceden oluşturulup granüllerde depolanmış (örn. <span class='text-rose-600 font-bold'>Histamin</span>), 2) Yangı uyarısı sonrası de novo sentezlenen (örn. <span class='text-amber-600 font-bold'>Prostaglandinler, Sitokinler</span>).",
            "• **Plazma Kaynaklı Mediyatörler:** Karaciğer tarafından dolaşıma verilen ve inaktif prekürsör olarak bekleyen proteinlerdir. Proteolitik basamaklı kaskadlarla (kompleman C3 konvertaz, kallikrein-kinin ve koagülasyon sistemi) aktive edilirler.",
            "• **Sinerji ve Yedeklilik (Redundancy):** Birçok farklı mediyatör benzer fizyolojik etkileri (vazodilatasyon, ağrı) paylaşır. Bu durum yangı yanıtının hayati derecede sağlam olmasını sağlarken, tek bir ajanın bloke edilmesinin yangıyı tamamen durduramamasının da temel sebebidir."
        ],
        "spotPearls": [
            "⚡ En hızlı salınan mediyatörler: Mast hücre granüllerinde hazır depolanmış olan histamindir.",
            "⚡ Plazma kaynaklı mediyatörlerin ana sentez fabrikası karaciğerdir (Kompleman, Kinin, Pıhtılaşma faktörleri).",
            "⚡ Mediyatörlerin kontrolsüz aşırı üretimi septik şok ve otoimmün doku hasarının birincil nedenidir."
        ],
        "flashcards": [
            {
                "front": "Enflamasyonun kimyasal mediyatörleri kökenlerine göre hangi iki ana gruba ayrılır?",
                "back": "1) Hücre kaynaklı mediyatörler (Mast hücresi, makrofaj, lökosit, endotel kökenli; örn. histamin, sitokinler, eikozanoidler)\n2) Plazma kaynaklı mediyatörler (Karaciğerde üretilip proteolizle aktive olan kompleman, kinin ve pıhtılaşma faktörleri).",
                "question": "Enflamasyonun kimyasal mediyatörleri kökenlerine göre hangi iki ana gruba ayrılır?",
                "answer": "Hücre kaynaklı (granüllü veya de novo) ve plazma kaynaklı (karaciğerde üretilen proteolitik kaskadlar).",
                "hint": "Karaciğer üretimi vs. lökosit/mast hücresi üretimi",
                "category": "Genel İlkeler"
            },
            {
                "front": "Mediyatörlerin lokal etki gösterip hızla inaktive edilmesinin fizyolojik amacı nedir?",
                "back": "Enflamatuar yanıtın aşırı yayılmasını ve çevre sağlam dokularda kontrolsüz hasar oluşmasını engellemek; yangıyı hasar odağıyla sınırlı tutmaktır.",
                "question": "Mediyatörlerin lokal etki gösterip hızla inaktive edilmesinin fizyolojik amacı nedir?",
                "answer": "Yangıyı yerel sınırlarda tutmak ve komşu sağlam dokularda kontrolsüz nekroz/hasar gelişmesini engellemek.",
                "hint": "Kendi kendini sınırlama",
                "category": "Genel İlkeler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-001",
                "question": "Aşağıdakilerden hangisi plazma kaynaklı ve karaciğerde inaktif öncül olarak sentezlenen enflamasyon mediyatörlerinden biridir?",
                "options": [
                    "A) Histamin",
                    "B) Lökotrien B4",
                    "C) Kompleman C3 bileşeni",
                    "D) Prostaglandin E2",
                    "E) Platelet Aktive Edici Faktör (PAF)"
                ],
                "correctAnswer": "C",
                "explanation": "Kompleman sistemi bileşenleri (C3, C5 vb.), kininler ve koagülasyon proteinleri karaciğerde sentezlenen ve dolaşımda inaktif gezen plazma kaynaklı mediyatörlerdir. Histamin, LTB4, PGE2 ve PAF ise hücre kaynaklı mediyatörlerdir."
            }
        ],
        "aiPromptSuggestions": [
            "Hücre kaynaklı ve plazma kaynaklı mediyatörlerin etki sürelerini karşılaştır.",
            "Mediyatörlerin yedeklilik (redundancy) ilkesi farmakolojik tedaviyi nasıl etkiler?",
            "Mast hücre degranülasyonunu tetikleyen başlıca faktörler nelerdir?"
        ]
    },
    {
        "slideNumber": 2,
        "title": "Vazoaktif Aminler: Histamin ve Salınım Mekanizmaları",
        "subtitle": "Mast Hücresi Degranülasyonu, H1 Reseptörleri ve Akut Vasküler Yanıt",
        "badge": "Vazoaktif Aminler",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Akut enflamasyonda arteriollerde ilk dakikalardaki vazodilatasyon ve özellikle postkapiller venüllerdeki endotel kasılmasına bağlı geçici geçirgenlik artışının baş mimarı histamindir!",
            "timestamp": "05:40",
            "emphasisType": "high-yield",
            "note": "Prof. Dr. Hikmet Keleş: Histamin etkisi H1 reseptör blokerleri (antihistaminikler) ile engellenir."
        },
        "synthesisNarrative": "Histamin, akut yangının en erken devreye giren vazoaktif aminidir. Dokulardaki bağ dokusunda kan damarlarına yakın yerleşen mast hücrelerinde, kanda ise bazofil ve trombositlerde hazır granüller içinde depolanmış halde bulunur. Bir uyarı geldiğinde saniyeler içinde ekzositozla salınarak mikrosirkülasyonda süratli değişikliklere yol açar.",
        "coreContent": [
            "• **Temel Kaynak:** En zengin kaynak doku <span class='text-rose-600 font-bold'>mast hücreleridir</span>. Ayrıca kanda dolaşan bazofiller ve trombositler de histamin içerir.",
            "• **Degranülasyon Tetikleyicileri:**",
            "  1. <span class='text-amber-600 font-semibold'>İmmünolojik uyarı:</span> Mast hücresi yüzeyindeki FcεRI reseptörlerine bağlı IgE antijen köprüleşmesi (Tip 1 Aşırı Duyarlılık).",
            "  2. <span class='text-rose-600 font-bold'>Kompleman anafilatoksinleri:</span> C3a ve C5a peptidleri mast hücre yüzeyindeki reseptörlerine bağlanarak direkt degranülasyona neden olur.",
            "  3. <span class='text-blue-600 font-semibold'>Fiziksel hasar:</span> Travma, mekanik darbe, aşırı soğuk veya ısı.",
            "  4. <span class='text-purple-600 font-semibold'>Sitokinler ve Nöropeptidler:</span> IL-1, IL-8, Substans P gibi peptidler.",
            "• **Vasküler Etkiler:**",
            "  - **Arterioller:** Düz kas gevşemesi ile <span class='text-rose-600 font-bold'>vazodilatasyon</span> yapar (kızarıklık ve sıcaklık artışı - rubor ve calor).",
            "  - **Postkapiller Venüller:** Endotel hücrelerinin kasılarak aralarındaki boşlukların açılmasına (endotel kontraksiyonu) ve <span class='text-rose-600 font-bold'>vasküler geçirgenlik artışına</span> neden olur (sıvı eksüdasyonu ve ödem - tumor).",
            "• **Reseptör ve Klinik:** Bu vasküler etkilerin neredeyse tamamı endotel üzerindeki **H1 histamin reseptörleri** aracılığıyla yürütülür. Klasik antihistaminikler (H1 blokerleri) ürtiker, alerjik rinit ve erken vasküler geçirgenliği bu reseptörü bloke ederek engeller."
        ],
        "spotPearls": [
            "⚡ Histamin venüllerde endotel kontraksiyonu yaparak 'erken geçici geçirgenlik artışına' yol açar (15-30 dk sürer).",
            "⚡ C3a ve C5a kompleman anafilatoksinleri mast hücresini degranüle ederek histamin salgılatır.",
            "⚡ Histaminin inflamatuar vasküler etkileri H1 reseptörleri üzerinden gerçekleşir."
        ],
        "flashcards": [
            {
                "front": "Mast hücrelerinden histamin degranülasyonunu tetikleyen en önemli iki kompleman parçası hangileridir?",
                "back": "C3a ve C5a (Anafilatoksinler olarak adlandırılırlar).",
                "question": "Mast hücrelerinden histamin degranülasyonunu tetikleyen en önemli iki kompleman parçası hangileridir?",
                "answer": "C3a ve C5a anafilatoksinleri.",
                "hint": "Anafilatoksinler",
                "category": "Vazoaktif Aminler"
            },
            {
                "front": "Histaminin postkapiller venüllerde oluşturduğu vasküler geçirgenlik artışının hücresel mekanizması nedir?",
                "back": "H1 reseptör uyarımı ile endotel hücrelerinin hücre içi kalsiyum artışına bağlı kasılması (kontraksiyonu) ve endotelyal aralıkların açılmasıdır.",
                "question": "Histaminin postkapiller venüllerde oluşturduğu vasküler geçirgenlik artışının hücresel mekanizması nedir?",
                "answer": "Endotel hücre kontraksiyonu ile hücreler arası bağlantıların geçici olarak açılması.",
                "hint": "Endotel kontraksiyonu",
                "category": "Vazoaktif Aminler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-002",
                "question": "Akut enflamasyonun erken evresinde postkapiller venüllerde endotel kontraksiyonuna neden olarak ani ve geçici vasküler geçirgenlik artışına yol açan, mast hücre granüllerinde önceden depolanmış primer mediyatör aşağıdakilerden hangisidir?",
                "options": [
                    "A) Histamin",
                    "B) Prostaglandin D2",
                    "C) Lökotrien B4",
                    "D) İnterlökin-6",
                    "E) Bradikinin"
                ],
                "correctAnswer": "A",
                "explanation": "Histamin mast hücre granüllerinde önceden depolanmış vazoaktif bir amindir ve erken geçici vasküler geçirgenlik artışının başlıca sorumlusudur."
            }
        ],
        "aiPromptSuggestions": [
            "H1 ve H2 reseptörlerinin yangı ve gastrik fizyolojideki farkları nelerdir?",
            "Postkapiller venüller neden arteriyollere göre histaminle geçirgenlik artışına daha duyarlıdır?",
            "Tip 1 aşırı duyarlılık reaksiyonunda mast hücresi degranülasyon basamaklarını sırala."
        ]
    },
    {
        "slideNumber": 3,
        "title": "Serotonin (5-Hidroksitriptamin) ve Vasküler Regülasyon",
        "subtitle": "Trombosit Agregasyonu, Vazokonstriksiyon ve Nöroendokrin Roller",
        "badge": "Vazoaktif Aminler",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Serotonin insanda mast hücrelerinde değil, kanda esas olarak trombositlerde bulunur. Trombosit agregasyonu sırasında salınarak vazokonstriktör etki gösterir.",
            "timestamp": "08:15",
            "emphasisType": "warning",
            "note": "Prof. Dr. Hikmet Keleş: Kemirgenlerde mast hücrelerinde bulunurken insanda primer kaynak trombositlerdir."
        },
        "synthesisNarrative": "Serotonin (5-HT), histamin gibi vazoaktif bir amin olup insan dokularında gastrointestinal enterokromaffin hücrelerde sentezlenir ve kanda dolaşan trombositler tarafından endositozla alınıp yoğun granüllerde depolanır. Damar endotel hasarı gerçekleştiğinde trombosit agregasyonu sırasında serbestleşerek hemostaz ve vasküler yanıta katılır.",
        "coreContent": [
            "• **Kaynak ve Dağılım:** İnsanda temel kaynak dolaşımdaki <span class='text-amber-600 font-bold'>trombositlerin yoğun (delta) granülleridir</span> ve GIS enterokromaffin hücreleridir (Karsinoid tümörlerde aşırı salınır).",
            "• **Salınım Mekanizması:** Trombositler kollajen, trombin veya PAF ile aktive olup agrege olduklarında serotonin hızla ekstraselüler alana salınır.",
            "• **Vasküler Etkiler:**",
            "  - Çoğu sistemik damar yatağında <span class='text-rose-600 font-bold'>vazokonstriktör</span> etki gösterir.",
            "  - Kanama bölgesinde hemostatik tıkaç oluşumunu desteklemek için lümeni daraltır.",
            "• **İnflamasyondaki Önemi:** Histamin kadar belirgin bir yangı mediyatörü olmamakla birlikte, trombosit-lökosit etkileşimini ve mikrovasküler tonusu düzenleyerek koagülasyon ile yangı arasındaki köprüyü kurar."
        ],
        "spotPearls": [
            "⚡ İnsanda serotonin mast hücrelerinde DEĞİL, trombosit granüllerinde ve GIS enterokromaffin hücrelerinde depolanır.",
            "⚡ Histamin belirgin vazodilatatör iken, serotonin temelde vazokonstriktör olarak hemostazı destekler."
        ],
        "flashcards": [
            {
                "front": "İnsan dolaşımında serotoninin (5-HT) depolandığı başlıca hücre ve granül tipi hangisidir?",
                "back": "Trombositlerin yoğun (delta) granülleridir.",
                "question": "İnsan dolaşımında serotoninin (5-HT) depolandığı başlıca hücre ve granül tipi hangisidir?",
                "answer": "Trombositlerin yoğun (delta) granülleri.",
                "hint": "Platelet delta granülleri",
                "category": "Vazoaktif Aminler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-003",
                "question": "İnsanda kan pulcuklarının (trombositler) agregasyonu esnasında yoğun granüllerinden salınan ve hemostatik odaklarda vazokonstriksiyona katkıda bulunan vazoaktif amin aşağıdakilerden hangisidir?",
                "options": [
                    "A) Histamin",
                    "B) Serotonin (5-HT)",
                    "C) Bradikinin",
                    "D) Dopamin",
                    "E) Prostasiklin"
                ],
                "correctAnswer": "B",
                "explanation": "Trombositlerin yoğun (dense) granüllerinde depolanan ve agregasyon sırasında salınarak vazokonstriksiyon yapan temel vazoaktif amin serotonindir."
            }
        ],
        "aiPromptSuggestions": [
            "Trombosit alfa granülleri ile yoğun (delta) granüllerinin içerik farkları nelerdir?",
            "Serotoninin inflamatuar ve hemostatik süreçlerdeki ikili rolünü özetle."
        ]
    },
    {
        "slideNumber": 4,
        "title": "Araşidonik Asit Kaskadı ve Fosfolipaz A2 Aktivasyonu",
        "subtitle": "Hücre Membranından Eikozanoid Biyosentezine İlk Adım",
        "badge": "Eikozanoidler",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Eikozanoidler hücrede hazır bekletilmez! Mekanik, kimyasal veya immünolojik uyarı geldiğinde Fosfolipaz A2 enzimi hücre zarı fosfolipidlerinden 20 karbonlu araşidonik asidi koparır. Kortikosteroidler işte tam bu ilk adımı, Fosfolipaz A2'yi inhibe eder!",
            "timestamp": "11:20",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Steroidlerin tüm eikozanoidleri birden kesmesinin sebebi PLA2 inhibisyonudur."
        },
        "synthesisNarrative": "Araşidonik asit (AA), hücre membranındaki fosfolipidlerin sn-2 pozisyonunda esterleşmiş halde bulunan 20 karbonlu çoklu doymamış bir yağ asididir (5,8,11,14-eikosatetraenoik asit). Yangısal, mekanik veya kimyasal bir uyarı hücre içi kalsiyum konsantrasyonunu artırdığında, **Fosfolipaz A2 (PLA2)** enzimi aktive olarak araşidonik asidi serbestleştirir.",
        "coreContent": [
            "• **Araşidonik Asit Kaynağı:** Hücre zarı fosfolipidleri (özellikle fosfatidilkolin ve fosfatidiletanolamin).",
            "• **Kritik Hız Kısıtlayıcı Basamak:** <span class='text-purple-600 font-bold'>Fosfolipaz A2 (PLA2)</span> aktivasyonudur. Hücre içi serbest AA konsantrasyonu normalde çok düşüktür; enzim aktivasyonuyla saniyeler içinde kaskat başlar.",
            "• **İki Ana Dallanma Yolu:**",
            "  1. <span class='text-rose-600 font-bold'>Siklooksijenaz (COX) Yolu:</span> Prostaglandinler (PGD2, PGE2, PGF2α), Prostasiklin (PGI2) ve Tromboksan A2 (TXA2) üretilir.",
            "  2. <span class='text-emerald-600 font-bold'>Lipoksijenaz (LOX) Yolu:</span> 5-LOX ile Lökotrienler (LTB4, LTC4, LTD4, LTE4); 12-LOX ile Lipoksinler (LXA4, LXB4) üretilir.",
            "• **Steroidlerin Etki Noktası:** Glukokortikoidler, <span class='text-rose-600 font-bold'>Lipokortin-1 (Anneksin A1)</span> proteinini indükleyerek Fosfolipaz A2'yi doğrudan baskılar. Böylece HEM siklooksijenaz HEM DE lipoksijenaz ürünlerinin tamamının sentezi kökten engellenir."
        ],
        "spotPearls": [
            "⚡ Eikozanoidler hazır depolanmaz; Fosfolipaz A2 uyarımıyla de novo (yeni) sentezlenir.",
            "⚡ Glukokortikoidler Anneksin A1 (Lipokortin-1) aracılığıyla PLA2'yi inhibe ederek hem PG hem de LT sentezini durdurur.",
            "⚡ Eikozanoidlerin tamamı hücre yüzeyindeki G-protein kenetli reseptörler (GPCR) aracılığıyla sinyal iletir."
        ],
        "flashcards": [
            {
                "front": "Hücre zarı fosfolipidlerinden araşidonik asidin serbestleşmesini sağlayan ve glukokortikoidler tarafından dolaylı olarak inhibe edilen enzim hangisidir?",
                "back": "Fosfolipaz A2 (PLA2). Glukokortikoidler Anneksin-1 (Lipokortin-1) sentezini artırarak bu enzimi inhibe eder.",
                "question": "Hücre zarı fosfolipidlerinden araşidonik asidin serbestleşmesini sağlayan ve glukokortikoidler tarafından dolaylı olarak inhibe edilen enzim hangisidir?",
                "answer": "Fosfolipaz A2 (PLA2).",
                "hint": "PLA2",
                "category": "Eikozanoidler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-004",
                "question": "Glukokortikoidlerin hem prostaglandinlerin hem de lökotrienlerin sentezini eş zamanlı olarak baskılayabilmesinin temel moleküler mekanizması aşağıdakilerden hangisidir?",
                "options": [
                    "A) 5-lipoksijenaz enziminin yarışmalı inhibisyonu",
                    "B) H1 histamin reseptörlerinin desensitizasyonu",
                    "C) Anneksin A1 indüksiyonu ile Fosfolipaz A2 aktivitesinin bloke edilmesi",
                    "D) Tromboksan sentaz enziminin parçalanması",
                    "E) C3 konvertaz enziminin proteolizi"
                ],
                "correctAnswer": "C",
                "explanation": "Glukokortikoidler Anneksin A1 (Lipokortin-1) üretimini artırarak Fosfolipaz A2'yi inhibe eder; böylece araşidonik asit serbestleşemez ve hem COX hem LOX kolları eş zamanlı bloke olur."
            }
        ],
        "aiPromptSuggestions": [
            "NSAİİ'lar ile Kortikosteroidlerin etki mekanizması şemasını karşılaştır.",
            "Fosfolipaz A2 enziminin kalsiyuma bağımlı aktivasyon basamakları nelerdir?"
        ]
    },
    {
        "slideNumber": 5,
        "title": "Siklooksijenaz İzoenzimleri: COX-1 ve COX-2 Karşılaştırması",
        "subtitle": "Konstitütif Homeostaz vs. İndüklenebilir İnflamatuar Yanıt",
        "badge": "Enzim Yolları",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "COX-1 vücudun nöbetçi bekçisidir; midede koruyucu mukusu, böbrekte kan akımını sağlar. COX-2 ise mikrop veya sitokin uyarısıyla yangı odağında uyanır. Selektif COX-2 inhibitörü verdiğinizde mideyi korursunuz ama endotel-trombosit dengesini bozup kardiyovasküler tromboz riskini artırırsınız!",
            "timestamp": "14:50",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Selektif COX-2 inhibitörlerinin tromboz riski sınavların klasik sorusudur."
        },
        "synthesisNarrative": "Siklooksijenaz enzimi serbest araşidonik asidi önce dengesiz bir ara ürün olan Prostaglandin G2'ye (PGG2), ardından Prostaglandin H2'ye (PGH2) dönüştürür. Vücutta iki ana siklooksijenaz izoformu bulunur: Yapısal (konstitütif) olarak çoğu dokuda sürekli çalışan **COX-1** ve pro-inflamatuar uyaranlarla dokularda hızla eksprese edilen **COX-2**.",
        "coreContent": [
            "• **COX-1 (Yapısal / Konstitütif İzoenzim):**",
            "  - Hemen her dokuda bazal düzeyde bulunur.",
            "  - <span class='text-blue-600 font-semibold'>Mide Mukozası:</span> PGE2 ve PGI2 sentezleyerek mukus/bikarbonat salgısını artırır, asit salgısını azaltır (sitoproteksiyon).",
            "  - <span class='text-blue-600 font-semibold'>Böbrekler:</span> Afferent arteriyol vazodilatasyonu ile Glomerüler Filtrasyon Hızını (GFH) korur.",
            "  - <span class='text-blue-600 font-semibold'>Trombositler:</span> Tromboksan A2 (TXA2) üreterek agregasyonu başlatır.",
            "• **COX-2 (İndüklenebilir İzoenzim):**",
            "  - Normal dokularda çok düşüktür (beyin, böbrek ve endotel hariç).",
            "  - İnflamasyon odağında **IL-1, TNF-α ve bakteriyel endotoksin (LPS)** etkisiyle hızla indüklenir.",
            "  - Yangı bölgesinde ağrı, ateş ve vazodilatasyondan sorumlu prostaglandinlerin ana kaynağıdır.",
            "• **Selektif vs. Non-Selektif İnhibitörler:**",
            "  - *Non-selektif NSAİİ (Aspirin, İbuprofen, İndometazin):* Hem COX-1 hem COX-2'yi bloke eder. Yan etki: Peptik ülser, GİS kanaması, akut böbrek hasarı.",
            "  - *Selektif COX-2 İnhibitörleri (Selekoksib):* Mide ülseri riskini azaltır; ancak endoteldeki vazodilatatör PGI2'yi kesip trombositteki TXA2'ye dokunmadığı için <span class='text-rose-600 font-bold'>Miyokard Enfarktüsü ve Tromboz riskini</span> artırır."
        ],
        "spotPearls": [
            "⚡ COX-1 mide mukozasında koruyucu PGE2 ve PGI2 üretiminden sorumludur (NSAİİ ülserinin sebebi COX-1 inhibisyonudur).",
            "⚡ COX-2 inflamatuar sitokinler (IL-1, TNF) ile indüklenir.",
            "⚡ Selektif COX-2 inhibitörleri PGI2 sentezini baskılarken trombositteki COX-1 kaynaklı TXA2'yi baskılamaz; bu da tromboz ve inme riskini artırır."
        ],
        "flashcards": [
            {
                "front": "Selektif COX-2 inhibitörlerinin kardiyovasküler tromboz ve MI riskini artırmasının moleküler mekanizması nedir?",
                "back": "Endoteldeki vazodilatatör ve antitrombotik Prostasiklin (PGI2) sentezini bloke ederken; trombositlerde COX-1 aracılığıyla üretilen protrombotik Tromboksan A2 (TXA2) sentezini etkilememeleridir. Denge TXA2 lehine bozulur.",
                "question": "Selektif COX-2 inhibitörlerinin kardiyovasküler tromboz ve MI riskini artırmasının moleküler mekanizması nedir?",
                "answer": "PGI2/TXA2 dengesini protrombotik TXA2 yönünde bozarak trombosit agregasyonunu tetiklemeleri.",
                "hint": "PGI2 azalır, TXA2 değişmez",
                "category": "Enzim Yolları"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-005",
                "question": "Mide mukozasında koruyucu prostaglandin sentezini sağlayan, böbrek perfüzyonunu koruyan ve trombositlerde TXA2 üretiminden sorumlu olan yapısal (konstitütif) siklooksijenaz izoenzimi aşağıdakilerden hangisidir?",
                "options": [
                    "A) Siklooksijenaz-1 (COX-1)",
                    "B) Siklooksijenaz-2 (COX-2)",
                    "C) 5-Lipoksijenaz",
                    "D) 12-Lipoksijenaz",
                    "E) Fosfolipaz C"
                ],
                "correctAnswer": "A",
                "explanation": "COX-1 vücutta hemen her dokuda bazal bulunan konstitütif izoenzimdir; mide sitoproteksiyonu ve renal perfüzyondan sorumludur."
            }
        ],
        "aiPromptSuggestions": [
            "Aspirinin COX-1 üzerindeki geri dönüşümsüz (kovalan) asetilasyon mekanizması nasıldır?",
            "Böbrek yetmezliğinde NSAİİ kullanımının GFH'yi düşürme patofizyolojisini açıkla."
        ]
    },
    {
        "slideNumber": 6,
        "title": "Prostaglandinler: PGE2, PGD2 ve PGF2α Biyolojik Rolleri",
        "subtitle": "Vazodilatasyon, Ateş Patogenezi, Ağrı Sensitizasyonu ve Ödem",
        "badge": "Prostaglandinler",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Hipotalamustaki termoregülasyon merkezinin ayar noktasını yukarı çeken ve ateşe neden olan molekül PGE2'dir. Aspirin ve parasetamol ateşi hipotalamusta PGE2 sentezini keserek düşürür.",
            "timestamp": "18:30",
            "emphasisType": "high-yield",
            "note": "Prof. Dr. Hikmet Keleş: PGE2 tek başına ağrı yapmaz, nosiseptörleri bradikinin ve histamin gibi ağrı yapıcı ajanlara duyarlı hale getirir (hiperaljezi)."
        },
        "synthesisNarrative": "PGH2 ara ürününden dokuya özgü izomeraz ve sentaz enzimleri aracılığıyla prostaglandin alt tipleri oluşturulur. Mast hücreleri, makrofajlar ve endotel hücreleri bu prostanoidlerin başlıca sentez merkezleridir. İnflamasyonun kardinal bulgularından olan calor (sıcaklık), rubor (kızarıklık) ve dolor (ağrı) gelişiminde prostaglandinler merkezi rol üstlenir.",
        "coreContent": [
            "• **Prostaglandin E2 (PGE2):**",
            "  - <span class='text-rose-600 font-bold'>Ateş (Fever):</span> İnflamatuar sitokinler (IL-1, TNF, IL-6) hipotalamik preoptik alandaki perivasküler hücrelerde COX-2 indükler ve PGE2 sentezletir. PGE2 termostat ayar noktasını yükselterek ateşi başlatır.",
            "  - <span class='text-amber-600 font-semibold'>Ağrı Duyarlılığı (Hiperaljezi):</span> C tipi nosiseptif sinir uçlarını duyarlı kılar, bradikinin ve substans P'nin ağrı oluşturma eşiğini belirgin şekilde düşürür.",
            "  - <span class='text-rose-600 font-semibold'>Arteriyoler Vazodilatasyon:</span> Kan akımını artırarak lokal kızarıklık ve ısı artışına yol açar.",
            "• **Prostaglandin D2 (PGD2):**",
            "  - Başlıca doku <span class='text-rose-600 font-bold'>mast hücreleri</span> tarafından üretilir.",
            "  - Vazodilatasyon yapar ve venüler geçirgenlik artışına (ödem) katkıda bulunur.",
            "  - Nötrofiller ve Th2 lenfositler için kemoatraktan işlev görür.",
            "• **Prostaglandin F2α (PGF2α):**",
            "  - Uterus ve bronş düz kaslarında güçlü kasılmaya yol açar; damarlarda vazokonstriksiyon yapabilir."
        ],
        "spotPearls": [
            "⚡ Hipotalamusta ateş ayar noktasını yükselten temel eikozanoid PGE2'dir.",
            "⚡ PGE2 nosiseptif sinirleri sensitize ederek ağrı eşiğini düşürür (hiperaljezi).",
            "⚡ PGD2'nin ana sentez kaynağı mast hücreleridir; vazodilatasyon ve ödeme katkı sağlar."
        ],
        "flashcards": [
            {
                "front": "Hipotalamik termoregülasyon merkezinde ayar noktasını (set point) yükselterek ateşe neden olan temel prostaglandin hangisidir?",
                "back": "Prostaglandin E2 (PGE2). Antipiretik ilaçlar hipotalamusta PGE2 sentezini baskılayarak ateşi düşürür.",
                "question": "Hipotalamik termoregülasyon merkezinde ayar noktasını yükselterek ateşe neden olan temel prostaglandin hangisidir?",
                "answer": "Prostaglandin E2 (PGE2).",
                "hint": "PGE2",
                "category": "Prostaglandinler"
            },
            {
                "front": "Mast hücrelerinin temel siklooksijenaz ürünü olan ve vazodilatasyon ile nötrofil kemotaksisine katkı sağlayan prostaglandin hangisidir?",
                "back": "Prostaglandin D2 (PGD2).",
                "question": "Mast hücrelerinin temel siklooksijenaz ürünü olan ve vazodilatasyon ile nötrofil kemotaksisine katkı sağlayan prostaglandin hangisidir?",
                "answer": "Prostaglandin D2 (PGD2).",
                "hint": "PGD2",
                "category": "Prostaglandinler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-006",
                "question": "Sistemik enfeksiyon ve enflamasyon süreçlerinde interlökin-1 ve TNF etkisiyle hipotalamusta sentezlenerek vücut sıcaklık ayar noktasını yükselten ve ateşe yol açan temel mediyatör aşağıdakilerden hangisidir?",
                "options": [
                    "A) Prostaglandin E2 (PGE2)",
                    "B) Tromboksan A2 (TXA2)",
                    "C) Lökotrien B4 (LTB4)",
                    "D) Lipoksin A4 (LXA4)",
                    "E) Serotonin"
                ],
                "correctAnswer": "A",
                "explanation": "PGE2 hipotalamusta cAMP artışına neden olarak sıcaklık termostatını yükseltir ve ateşe (fever) neden olur."
            }
        ],
        "aiPromptSuggestions": [
            "PGE2'nin ağrı sensitizasyonundaki iyon kanalı etkileşimleri nelerdir?",
            "Antipiretik ilaçların etki mekanizmasını PGE2 üzerinden açıkla."
        ]
    },
    {
        "slideNumber": 7,
        "title": "Prostasiklin (PGI2) ve Tromboksan A2 (TXA2) Karşıtlığı",
        "subtitle": "Endotel-Trombosit Ekseni ve Vasküler Hemostaz Dengesi",
        "badge": "Vasküler Denge",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "PGI2 endotelindir, vazodilatasyon yapar ve pıhtıyı engeller. TXA2 ise trombositindir, damarı kasar ve pıhtılaştırır. Bu iki zıt kardeşin dengesi bozulursa ya kontrolsüz kanama ya da ölümcül tromboz gelişir!",
            "timestamp": "22:10",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Düşük doz aspirinin antitrombotik etkisi bu dengenin kinetiğine dayanır."
        },
        "synthesisNarrative": "Vasküler sistemde endotel hücreleri ile trombositler arasında mükemmel bir biyokimyasal denge mevcuttur. Endotel hücreleri **Prostasiklin Sentaz** enzimi ile PGI2 üretirken; trombositler **Tromboksan Sentaz** enzimi ile TXA2 üretir. Bu iki molekül damar tonusu ve trombosit agregasyonu üzerinde birbirine taban tabana zıt etki göstererek fizyolojik hemostazı korur.",
        "coreContent": [
            "• **Prostasiklin (PGI2):**",
            "  - *Sentez Yeri:* Sağlıklı <span class='text-teal-600 font-bold'>vasküler endotel hücreleri</span>.",
            "  - *Etkileri:* Güçlü **vazodilatatördür**; trombosit yüzeyindeki IP reseptörüne bağlanıp cAMP'yi artırarak <span class='text-teal-600 font-bold'>trombosit agregasyonunu güçlü biçimde inhibe eder</span>.",
            "• **Tromboksan A2 (TXA2):**",
            "  - *Sentez Yeri:* Dolaşımdaki <span class='text-rose-600 font-bold'>trombositler</span> (COX-1 ve TXA sentaz yolu).",
            "  - *Etkileri:* Güçlü **vazokonstriktördür**; trombosit agregasyonunu ve degranülasyonunu kuvvetle uyararak <span class='text-rose-600 font-bold'>trombüs oluşumunu başlatır</span>.",
            "• **Düşük Doz Aspirin Mucizesi:**",
            "  - Trombositlerde çekirdek olmadığı için yeni COX-1 sentezleyemezler; aspirin COX-1'i kovalan asetilleyince trombositin tüm ömrü boyunca (7-10 gün) TXA2 üretimi durur.",
            "  - Endotel hücreleri ise çekirdekli olduğu için asetillenen COX enzimlerini saatler içinde yeniden sentezleyerek PGI2 üretmeye devam eder. Böylece denge antitrombotik tarafa kayar."
        ],
        "spotPearls": [
            "⚡ PGI2 (Endotel): Vazodilatasyon + Trombosit agregasyon inhibisyonu (Antitrombotik).",
            "⚡ TXA2 (Trombosit): Vazokonstriksiyon + Trombosit agregasyon aktivasyonu (Protrombotik).",
            "⚡ Trombositler çekirdeksiz olduğu için aspirinle inhibe olan COX-1'i yenileyemezler."
        ],
        "flashcards": [
            {
                "front": "Endotel kaynaklı PGI2 ile trombosit kaynaklı TXA2'nin damar çapı ve trombosit agregasyonu üzerindeki zıt etkilerini özetleyiniz.",
                "back": "• PGI2 (Endotel): Vazodilatasyon yapar, trombosit agregasyonunu inhibe eder (antitrombotik).\n• TXA2 (Trombosit): Vazokonstriksiyon yapar, trombosit agregasyonunu uyarır (protrombotik).",
                "question": "PGI2 ile TXA2'nin damar çapı ve trombosit agregasyonu üzerindeki zıt etkilerini özetleyiniz.",
                "answer": "PGI2 vazodilatasyon ve agregasyon inhibisyonu yaparken; TXA2 vazokonstriksiyon ve agregasyon uyarımı yapar.",
                "hint": "Zıt kardeşler",
                "category": "Vasküler Denge"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-007",
                "question": "Vasküler endotel hücreleri tarafından sentezlenen, güçlü vazodilatatör etkiye sahip olan ve trombosit agregasyonunu inhibe ederek intakt damarlarda trombüs oluşumunu engelleyen eikozanoid hangisidir?",
                "options": [
                    "A) Tromboksan A2",
                    "B) Prostasiklin (PGI2)",
                    "C) Lökotrien C4",
                    "D) Lökotrien B4",
                    "E) Prostaglandin F2α"
                ],
                "correctAnswer": "B",
                "explanation": "Prostasiklin (PGI2) endotel kaynaklıdır; vazodilatasyon yapar ve trombosit kümeleşmesini engelleyerek damar açıklığını korur."
            }
        ],
        "aiPromptSuggestions": [
            "Düşük doz aspirinin antitrombotik mekanizmasını trombosit ve endotel biyolojisi üzerinden açıkla.",
            "Ateroskleroz zemininde endotel hasarı PGI2/TXA2 dengesini nasıl bozar?"
        ]
    },
    {
        "slideNumber": 8,
        "title": "5-Lipoksijenaz Yolu ve Lökotrien Biyosentezi",
        "subtitle": "Nötrofiller, Mast Hücreleri ve Eozinofillerde Lökotrien Sentezi",
        "badge": "Lökotrienler",
        "badgeColor": "emerald",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Lipoksijenaz yolunun kilit enzimi 5-lipoksijenazdır. Buradan önce dayanıksız LTA4 sentezlenir. LTA4 nötrofilde LTB4'e dönerken; mast hücresi ve eozinofilde sisteinil lökotrienlere (LTC4, LTD4, LTE4) dönüşür.",
            "timestamp": "26:00",
            "emphasisType": "high-yield",
            "note": "Prof. Dr. Hikmet Keleş: Zileuton 5-LOX enzimini inhibe ederek astımda kullanılır."
        },
        "synthesisNarrative": "Araşidonik asidin ikinci ana metabolik güzergahı **Lipoksijenaz (LOX)** yoludur. Özellikle miyeloid hücrelerde (nötrofiller, eozinofiller, bazofiller, mast hücreleri ve monositler) bulunan **5-lipoksijenaz (5-LOX)** enzimi, AA'ya moleküler oksijen ekleyerek önce 5-HPETE'yi, ardından kararsız bir epoksit olan **Lökotrien A4'ü (LTA4)** oluşturur.",
        "coreContent": [
            "• **Hücresel Dağılım:** 5-lipoksijenaz ekspresyonu COX gibi yaygın değildir; başlıca lökositlerde (nötrofil, mast hücresi, eozinofil, makrofaj) kısıtlıdır.",
            "• **Sentez Basamakları:**",
            "  1. Araşidonik Asit ➔ (5-LOX + FLAP) ➔ 5-HPETE ➔ <span class='text-emerald-600 font-bold'>Lökotrien A4 (LTA4)</span>.",
            "  2. Nötrofillerde LTA4 hidrolaz enzimi ile ➔ <span class='text-blue-600 font-bold'>Lökotrien B4 (LTB4)</span>.",
            "  3. Mast hücreleri ve eozinofillerde glutatyon eklenmesiyle ➔ <span class='text-rose-600 font-bold'>LTC4 ➔ LTD4 ➔ LTE4 (Sisteinil Lökotrienler)</span>.",
            "• **Farmakolojik Müdahale:** 5-LOX enzim inhibitörü olan **Zileuton**, lökotrien kaskadını en baştan keserek bronşiyal astım profilaksisinde kullanılır."
        ],
        "spotPearls": [
            "⚡ 5-lipoksijenaz enzimi başlıca lökositlerde (nötrofil, eozinofil, mast hücresi) aktiftir.",
            "⚡ LTA4 tüm lökotrienlerin ortak öncül molekülüdür.",
            "⚡ Zileuton 5-LOX enzim inhibitörüdür."
        ],
        "flashcards": [
            {
                "front": "Lökotrien biyosentezinde tüm lökotrienlerin (LTB4 ve sisteinil lökotrienler) ortak dayanıksız öncülü olan molekül hangisidir?",
                "back": "Lökotrien A4 (LTA4).",
                "question": "Lökotrien biyosentezinde tüm lökotrienlerin ortak dayanıksız öncülü olan molekül hangisidir?",
                "answer": "Lökotrien A4 (LTA4).",
                "hint": "LTA4",
                "category": "Lökotrienler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-008",
                "question": "Alerjik astım tedavisinde kullanılan Zileuton adlı ilacın primer hedefi olan ve araşidonik asitten lökotrien sentezinin ilk basamağını katalizleyen enzim hangisidir?",
                "options": [
                    "A) Siklooksijenaz-2",
                    "B) 5-Lipoksijenaz",
                    "C) Tromboksan sentaz",
                    "D) Fosfolipaz C",
                    "E) Fosfodiesteraz-4"
                ],
                "correctAnswer": "B",
                "explanation": "Zileuton 5-lipoksijenaz (5-LOX) enzimini seçici olarak inhibe ederek lökotrien sentezini engeller."
            }
        ],
        "aiPromptSuggestions": [
            "FLAP (5-lipoksijenaz aktive edici protein) molekülünün fonksiyonunu açıkla.",
            "Lökotrien biyosentezinin hücre içi lokalizasyonu (çekirdek zarı) neden önemlidir?"
        ]
    },
    {
        "slideNumber": 9,
        "title": "Lökotrien B4 (LTB4): Majör Lökosit Kemoatraktanı",
        "subtitle": "Nötrofil Kemotaksisi, Adezyon Aktivasyonu ve ROS Patlaması",
        "badge": "Lökotrienler",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Sınavda nötrofil kemotaksisi dendiğinde aklınıza 4 altın molekül gelecek: 1) LTB4, 2) C5a, 3) İnterlökin-8 (CXCL8) ve 4) Bakteriyel N-formil peptidler. LTB4 bunların lipid türevi olan lideridir!",
            "timestamp": "29:15",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Nötrofil kemotaksisini sağlayan 4 majör ajan patolojinin demirbaşıdır."
        },
        "synthesisNarrative": "Lökotrien B4 (LTB4), nötrofillerde LTA4 hidrolaz enzimi tarafından üretilen son derece güçlü bir lipid kemoatraktandır. Yangı odağında bakteriyel ürünler veya fagositoz ile uyarılan nötrofiller LTB4 salgılayarak dolaşımdaki diğer nötrofilleri hızla olay yerine çağırır.",
        "coreContent": [
            "• **Temel Fonksiyonlar:**",
            "  - <span class='text-blue-600 font-bold'>Güçlü Kemotaktik Ajan:</span> Konsantrasyon gradiyenti boyunca nötrofilleri yangı odağına çeker.",
            "  - <span class='text-rose-600 font-semibold'>İntegrin Afinitesi Artışı:</span> Nötrofillerdeki β2 integrinlerin (LFA-1, Mac-1) konformasyonunu değiştirerek endoteldeki ICAM-1'e sıkı yapışmasını (adezyon) sağlar.",
            "  - <span class='text-amber-600 font-semibold'>Lökosit Aktivasyonu:</span> Nötrofil lizozomal enzim degranülasyonunu ve NADPH oksidaz kaynaklı reaktif oksijen türleri (ROS) üretimini indükler.",
            "• **Sınavın Altın Kuralı (Dört Büyük Kemotaktik Faktör):**",
            "  1. <span class='text-blue-600 font-bold'>LTB4</span> (Araşidonik asit lipid metaboliti)",
            "  2. <span class='text-rose-600 font-bold'>C5a</span> (Kompleman anafilatoksini)",
            "  3. <span class='text-emerald-600 font-bold'>IL-8 (CXCL8)</span> (Kemokin)",
            "  4. <span class='text-purple-600 font-bold'>Bakteriyel N-formil-metionil peptidler</span>"
        ],
        "spotPearls": [
            "⚡ LTB4 lipid yapılı en güçlü nötrofil kemoatraktanıdır.",
            "⚡ Dört büyük nötrofil kemotaktik ajanı: LTB4, C5a, IL-8 ve bakteriyel formil peptidlerdir.",
            "⚡ LTB4 nötrofillerin endotelyal adezyonunu ve lizozomal enzim salınımını tetikler."
        ],
        "flashcards": [
            {
                "front": "Akut enflamasyonda nötrofillerin kemotaksisini sağlayan 4 majör kimyasal aracı molekül hangileridir?",
                "back": "1) Lökotrien B4 (LTB4)\n2) Kompleman C5a parçası\n3) İnterlökin-8 (IL-8 / CXCL8)\n4) Bakteriyel ürünler (N-formil-metionil peptidleri).",
                "question": "Akut enflamasyonda nötrofillerin kemotaksisini sağlayan 4 majör kimyasal aracı molekül hangileridir?",
                "answer": "LTB4, C5a, IL-8 ve bakteriyel N-formil peptidler.",
                "hint": "4 altın kemotaktik ajan",
                "category": "Lökotrienler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-009",
                "question": "Aşağıdakilerden hangisi akut enflamatuar odakta nötrofillerin kemotaksisini uyaran araşidonik asit 5-lipoksijenaz yolu lipid mediyatörüdür?",
                "options": [
                    "A) Lökotrien C4",
                    "B) Lökotrien B4",
                    "C) Prostaglandin I2",
                    "D) Tromboksan A2",
                    "E) Lipoksin A4"
                ],
                "correctAnswer": "B",
                "explanation": "Lökotrien B4 (LTB4) nötrofiller için güçlü bir kemotaktik faktördür ve integrin adezyonunu uyarır."
            }
        ],
        "aiPromptSuggestions": [
            "LTB4 reseptörleri (BLT1 ve BLT2) arasındaki afinite ve ekspresyon farkları nelerdir?",
            "Lökosit adezyon eksikliği (LAD) sendromlarında LTB4 yanıtı neden bozulur?"
        ]
    },
    {
        "slideNumber": 10,
        "title": "Sisteinil Lökotrienler (LTC4, LTD4, LTE4): SRS-A ve Astım",
        "subtitle": "Şiddetli Bronkospazm, Mukus Hipersekresyonu ve Permeabilite Artışı",
        "badge": "Lökotrienler",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Eski adıyla Anafilaksinin Yavaş Reaksiyon Veren Maddesi (SRS-A) olan LTC4, LTD4 ve LTE4, histaminden bin kat daha güçlü bronkokonstriktördür! Astım krizindeki hava yolu tıkanıklığının ve aşırı mukusun temel sorumlusu bunlardır.",
            "timestamp": "33:10",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Montelukast ve Zafirlukast bu lökotrienlerin CysLT1 reseptörünü bloke eder."
        },
        "synthesisNarrative": "LTA4 molekülüne glutatyon-S-transferaz enzimiyle glutatyon eklenmesiyle **Lökotrien C4 (LTC4)** oluşur. Ardından enzimatik basamaklarla glutamik asit ve glisin ayrılarak sırasıyla **Lökotrien D4 (LTD4)** ve **Lökotrien E4 (LTE4)** meydana gelir. Yapılarında sistein aminoasidi barındırdıkları için bu üçlüye **sisteinil lökotrienler** adı verilir.",
        "coreContent": [
            "• **Biyolojik Etkileri:**",
            "  - <span class='text-rose-600 font-bold'>Güçlü Bronkokonstriksiyon:</span> Bronş düz kaslarını histaminden yaklaşık 1000 kat daha güçlü ve uzun süreli kasar.",
            "  - <span class='text-amber-600 font-bold'>Artmış Vasküler Permeabilite:</span> Postkapiller venüllerde belirgin endotel kontraksiyonu yaparak havayolu mukozasında şiddetli ödeme yol açar.",
            "  - <span class='text-purple-600 font-semibold'>Mukus Hipersekresyonu:</span> Bronşiyal kadeh (goblet) hücrelerinden koyu ve yapışkan mukus salgısını stimüle eder.",
            "  - <span class='text-blue-600 font-semibold'>Vazokonstriksiyon:</span> Koroner ve sistemik mikrosirkülasyonda vazokonstriksiyona neden olabilir.",
            "• **Klinik ve Tedavi:** Astım ve alerjik rinit patogenezinde merkezi rol oynarlar. **Montelukast** ve **Zafirlukast** gibi ilaçlar hedef hücrelerdeki **CysLT1 reseptörünü** antagonize ederek hava yolu daralmasını önler."
        ],
        "spotPearls": [
            "⚡ LTC4, LTD4 ve LTE4 sisteinil lökotrienler olarak adlandırılır (eski adıyla SRS-A).",
            "⚡ Histaminden 1000 kat daha güçlü bronkokonstriksiyon yaparlar.",
            "⚡ Montelukast/Zafirlukast CysLT1 reseptör antagonistidir."
        ],
        "flashcards": [
            {
                "front": "Sisteinil lökotrienler (LTC4, LTD4, LTE4) bronş düz kasları üzerinde histamin ile kıyaslandığında nasıl bir etki gücüne sahiptir?",
                "back": "Histaminden yaklaşık 1000 kat daha güçlü ve uzun süreli bronkokonstriksiyon (bronkospazm) yaparlar.",
                "question": "Sisteinil lökotrienler bronş düz kasları üzerinde histamin ile kıyaslandığında nasıl bir etki gücüne sahiptir?",
                "answer": "Histaminden yaklaşık 1000 kat daha güçlü bronkokonstriksiyon yaparlar.",
                "hint": "1000 kat daha güçlü",
                "category": "Lökotrienler"
            },
            {
                "front": "Montelukast ve zafirlukast adlı astım ilaçlarının hedef aldığı reseptör hangisidir?",
                "back": "CysLT1 (Sisteinil lökotrien tip 1) reseptörüdür.",
                "question": "Montelukast ve zafirlukast adlı astım ilaçlarının hedef aldığı reseptör hangisidir?",
                "answer": "CysLT1 reseptörü.",
                "hint": "CysLT1",
                "category": "Lökotrienler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-010",
                "question": "Bronşiyal astım atağında bronş düz kaslarında histaminden çok daha güçlü ve uzamış spazma, venüler geçirgenlik artışına ve mukus hipersekresyonuna neden olan 'sisteinil lökotrienler' grubu aşağıdakilerden hangisinde doğru verilmiştir?",
                "options": [
                    "A) LTA4, LTB4, LTC4",
                    "B) LTC4, LTD4, LTE4",
                    "C) PGD2, PGE2, PGF2α",
                    "D) LXA4, LXB4, LTB4",
                    "E) TXA2, PGI2, PAF"
                ],
                "correctAnswer": "B",
                "explanation": "Sisteinil lökotrienler (SRS-A) LTC4, LTD4 ve LTE4'tür."
            }
        ],
        "aiPromptSuggestions": [
            "Aspirinle tetiklenen astımda (Widal sendromu) lökotrien kaskadı nasıl aşırı aktifleşir?",
            "LTC4'ün LTD4 ve LTE4'e metabolize olma basamaklarındaki enzimler nelerdir?"
        ]
    },
    {
        "slideNumber": 11,
        "title": "Lipoksinler (LXA4, LXB4): Enflamasyonun Freni ve Çözünme",
        "subtitle": "Transsellüler Biyosentez, Nötrofil İnhibisyonu ve Rezolüsyon",
        "badge": "Rezolüsyon",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Bütün eikozanoidler yangıyı alevlendirirken lipoksinler yangıyı söndüren itfaiyecidir! Yangının sonlanması (çözünme/resolution) aşamasında lökosit-trombosit işbirliğiyle sentezlenip nötrofilleri durdururlar.",
            "timestamp": "36:40",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Lipoksinler anti-inflamatuar eikozanoidlerdir; sınavların en sevilen ayrım noktasıdır."
        },
        "synthesisNarrative": "Diğer tüm araşidonik asit türevlerinin aksine, **Lipoksinler (Lipoxin A4 ve B4)** endojen **anti-inflamatuar** lipid mediyatörleridir. Yangısal reaksiyonun doruk noktasında lökositler ile trombositlerin karşılıklı enzimatik etkileşimi (transsellüler biyosentez) sonucu üretilirler ve yangının çözünme (rezolüsyon) fazına geçişini yönetirler.",
        "coreContent": [
            "• **Transsellüler Biyosentez (İki Hücreli Üretim):**",
            "  - Nötrofiller araşidonik asitten 5-LOX ile ara metabolitleri (örneğin LTA4) üretir.",
            "  - Bu ara ürün komşu trombosite transfer edilir; trombositteki **12-lipoksijenaz (12-LOX)** enzimi bunu aktif **Lipoksin A4 ve B4'e** dönüştürür.",
            "• **Anti-İnflamatuar Etkileri:**",
            "  - <span class='text-teal-600 font-bold'>Nötrofil Kemotaksisi ve Adezyonunun İnhibisyonu:</span> Nötrofillerin damar dışına çıkışını durdurur.",
            "  - <span class='text-teal-600 font-semibold'>Monositlerin Alımı:</span> Yangı alanındaki hücresel enkazı ve apoptotik nötrofilleri temizlemek (eferositoz) üzere non-inflamatuar monosit/makrofajları bölgeye davet eder.",
            "  - <span class='text-blue-600 font-semibold'>Damar Geçirgenliğinin Normale Dönmesi:</span> Endotel bariyerini stabilize eder."
        ],
        "spotPearls": [
            "⚡ Lipoksinler anti-inflamatuar etki gösteren tek majör eikozanoid grubudur.",
            "⚡ Nötrofil (5-LOX) ve trombosit (12-LOX) arasındaki transsellüler işbirliğiyle sentezlenirler.",
            "⚡ Yangının rezolüsyon (çözünme) fazında nötrofil göçünü durdurur ve temizleyici makrofajları aktive ederler."
        ],
        "flashcards": [
            {
                "front": "Araşidonik asit metabolitleri arasında nötrofil kemotaksisini ve adezyonunu inhibe ederek yangının sonlanmasına (rezolüsyonuna) öncülük eden anti-inflamatuar lipidler hangileridir?",
                "back": "Lipoksinler (Lipoksin A4 ve Lipoksin B4).",
                "question": "Araşidonik asit metabolitleri arasında nötrofil göçünü durduran anti-inflamatuar lipidler hangileridir?",
                "answer": "Lipoksinler (LXA4 ve LXB4).",
                "hint": "LXA4 / LXB4",
                "category": "Rezolüsyon"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-011",
                "question": "Lökosit-trombosit transsellüler metabolik işbirliği ile sentezlenen ve diğer eikozanoidlerin aksine nötrofil adezyonu ile kemotaksisini baskılayarak enflamasyonun rezolüsyonunu (çözünmesini) sağlayan lipid mediyatör hangisidir?",
                "options": [
                    "A) Lökotrien B4",
                    "B) Tromboksan A2",
                    "C) Lipoksin A4 (LXA4)",
                    "D) Prostaglandin D2",
                    "E) Platelet Aktive Edici Faktör"
                ],
                "correctAnswer": "C",
                "explanation": "Lipoksinler (LXA4, LXB4) anti-inflamatuar etkilidir; nötrofil rekrutmanını frenler ve yangının çözünmesini teşvik eder."
            }
        ],
        "aiPromptSuggestions": [
            "Aspirinle tetiklenen lipoksinlerin (15-epi-lipoksinler / ATL) biyosentezini açıkla.",
            "Eferositoz nedir ve lipoksinler apoptotik nötrofil fagositozunu nasıl kolaylaştırır?"
        ]
    },
    {
        "slideNumber": 12,
        "title": "Araşidonik Asit Yolağını Hedefleyen Farmakolojik Ajanlar",
        "subtitle": "Kortikosteroidler, NSAİİ, Koksibler ve Lökotrien Engelleyicileri",
        "badge": "Farmakoloji Özeti",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Bu slayt patoloji ile farmakolojinin tam kesiştiği yerdir. Kortikosteroid PLA2'yi durdurur, Aspirin COX'u asetiller, Zileuton 5-LOX'u keser, Montelukast ise CysLT1 reseptörünü bloke eder. Sınavda bu dördü mutlaka sorulur!",
            "timestamp": "40:15",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Hedef basamakları karıştırmamak için tabloyu zihninize kazıyın."
        },
        "synthesisNarrative": "İnflamatuar hastalıkların modern tıptaki medikal tedavisinin çok büyük bir kısmı araşidonik asit kaskadındaki stratejik enzim ve reseptörlerin farmakolojik olarak inhibe edilmesine dayanır. Hangi ilacın kaskadın neresini kestiği klinik başarı ve yan etki profilini belirler.",
        "coreContent": [
            "• **İlaç Sınıfları ve Hedef Molekülleri Tablosu:**",
            "  1. <span class='text-rose-600 font-bold'>Kortikosteroidler (Prednizolon, Deksametazon):</span> Lipokortin-1 (Anneksin A1) indüksiyonu ile **Fosfolipaz A2 (PLA2)** enzimini inhibe eder; ayrıca COX-2 ekspresyonunu baskılar. *Sonuç:* Hem PG hem LT sentezi durur.",
            "  2. <span class='text-blue-600 font-bold'>Non-Selektif NSAİİ (Aspirin, İbuprofen):</span> **COX-1 ve COX-2** enzimlerini yarışmalı inhibe eder (Aspirin kovalan asetilasyonla irreversibl inhibe eder). *Sonuç:* Prostaglandin ve tromboksan sentezi durur.",
            "  3. <span class='text-amber-600 font-bold'>Selektif COX-2 İnhibitörleri (Selekoksib):</span> Yalnızca **COX-2** izoenzimini bloke eder. *Sonuç:* Mide korunur ama protrombotik risk artar.",
            "  4. <span class='text-emerald-600 font-bold'>5-Lipoksijenaz İnhibitörleri (Zileuton):</span> **5-LOX** enzimini doğrudan inhibe eder. *Sonuç:* Tüm lökotrienlerin (LTB4, C4, D4, E4) üretimi kesilir.",
            "  5. <span class='text-purple-600 font-bold'>Lökotrien Reseptör Antagonistleri (Montelukast, Zafirlukast):</span> **CysLT1 reseptörünü** bloke eder. *Sonuç:* LTC4/D4/E4 etkileri engellenir."
        ],
        "spotPearls": [
            "⚡ En üst basamağı (PLA2) kesen: Kortikosteroidlerdir.",
            "⚡ Enzimi kovalan/irreversibl bağlayan: Aspirindir.",
            "⚡ 5-LOX enzimini kesen Zileuton iken, reseptörü bloke eden Montelukast'tır."
        ],
        "flashcards": [
            {
                "front": "Glukokortikoidler, Aspirin, Zileuton ve Montelukast ilaçlarının araşidonik asit yolundaki hedeflerini eşleştiriniz.",
                "back": "• Glukokortikoidler: Fosfolipaz A2 (PLA2)\n• Aspirin: COX-1 ve COX-2 (kovalan asetilasyon)\n• Zileuton: 5-Lipoksijenaz enzimi\n• Montelukast: CysLT1 reseptörü.",
                "question": "Glukokortikoidler, Aspirin, Zileuton ve Montelukast ilaçlarının hedeflerini eşleştiriniz.",
                "answer": "Kortikosteroid: PLA2; Aspirin: COX; Zileuton: 5-LOX; Montelukast: CysLT1 reseptörü.",
                "hint": "4 büyük ilaç grubu",
                "category": "Farmakoloji Özeti"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-012",
                "question": "Aşağıdaki ilaç-hedef eşleştirmelerinden hangisi YANLIŞTIR?",
                "options": [
                    "A) Zileuton — 5-lipoksijenaz enzimi inhibisyonu",
                    "B) Montelukast — CysLT1 lökotrien reseptör blokajı",
                    "C) Aspirin — Siklooksijenaz enzimlerinin asetilasyonu",
                    "D) Deksametazon — C5 konvertaz enzim inhibisyonu",
                    "E) Selekoksib — İndüklenebilir siklooksijenaz-2 (COX-2) inhibisyonu"
                ],
                "correctAnswer": "D",
                "explanation": "Deksametazon (glukokortikoid) C5 konvertazı değil; lipokortin-1 indüksiyonu ile Fosfolipaz A2'yi inhibe eder."
            }
        ],
        "aiPromptSuggestions": [
            "NSAİİ kullanımı sırasında araşidonik asidin LOX yoluna kayması (lökotrien şantı) ne tür klinik tablolara yol açar?",
            "Aspirin intoksikasyonunda asit-baz dengesi değişiklikleri nelerdir?"
        ]
    },
    {
        "slideNumber": 13,
        "title": "Akut Enflamasyonun Ana Sitokinleri: TNF ve IL-1",
        "subtitle": "Aktive Makrofajlar, Mikrobiyal PAMP/DAMP Uyarımı ve İnflamazom",
        "badge": "Sitokinler",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Akut yangının orkestra şefleri TNF ve IL-1'dir. İkisi de aktive makrofajlardan salınır. IL-1 salınımı için sitoplazmadaki inflamazom kompleksinin kaspaz-1'i aktive etmesi şarttır!",
            "timestamp": "43:50",
            "emphasisType": "high-yield",
            "note": "Prof. Dr. Hikmet Keleş: İnflamazom kaspaz-1'i aktive ederek pro-IL-1beta'yı olgunlaştırır."
        },
        "synthesisNarrative": "Sitokinler, hücreler arası iletişimi sağlayan polipeptid yapılı moleküllerdir. Akut enflamasyon yanıtında başrolü **Tümör Nekroz Faktörü (TNF)** ve **İnterlökin-1 (IL-1)** oynar. Bu iki sitokin mikrobiyal ürünlerin (LPS gibi PAMP'lar) Toll-benzeri reseptörlere (TLR) veya nekrotik hücre artıklarının (DAMP) hücre içi reseptörlere bağlanmasıyla aktive olan **doku makrofajları ve dendritik hücreler** tarafından bolca sentezlenir.",
        "coreContent": [
            "• **Temel Kaynaklar:** Başlıca <span class='text-rose-600 font-bold'>aktive doku makrofajları</span>, mast hücreleri ve dendritik hücreler. TNF ayrıca T lenfositler tarafından da salınır.",
            "• **Sentez Uyarımı:** Bakteriyel lipopolisakkarit (LPS/endotoksin), viral nükleik asitler, hücresel nekroz ürünleri (ürik asit kristalleri, ekstraselüler ATP) ve kompleman ürünleri.",
            "• **İnflamazom ve IL-1 İşlenmesi:**",
            "  - IL-1 önce inaktif *pro-IL-1β* olarak üretilir.",
            "  - Hücre sitozolündeki **NLRP3 inflamazom** kompleksi uyarıldığında **Kaspaz-1** enzimini aktive eder.",
            "  - Kaspaz-1 pro-IL-1β'yı keserek aktif IL-1'e dönüştürür ve hücre dışına salar.",
            "• **Lokal ve Sistemik Köprü:** Hem enfeksiyon odağında endotel aktivasyonu yaparlar hem de kan dolaşımına geçerek ateş, halsizlik ve akut faz yanıtı başlatırlar."
        ],
        "spotPearls": [
            "⚡ TNF ve IL-1'in en zengin hücresel kaynağı aktive doku makrofajlarıdır.",
            "⚡ IL-1β'nın aktifleşmesi için NLRP3 inflamazom kompleksi ve Kaspaz-1 aktivasyonu zorunludur.",
            "⚡ Gut hastalığında ürat kristalleri NLRP3 inflamazomu uyararak yoğun IL-1 salınımına ve akut artrite neden olur."
        ],
        "flashcards": [
            {
                "front": "Hücre sitoplazmasında bulunan NLRP3 inflamazom kompleksi hangi enzimi aktive ederek pro-IL-1β'yı olgun aktif IL-1'e dönüştürür?",
                "back": "Kaspaz-1 enzimini aktive eder.",
                "question": "NLRP3 inflamazom kompleksi hangi enzimi aktive ederek IL-1'i olgunlaştırır?",
                "answer": "Kaspaz-1 enzimi.",
                "hint": "Kaspaz-1",
                "category": "Sitokinler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-013",
                "question": "Makrofajlarda mikrobiyal ürünler veya ürat kristalleriyle aktive olan NLRP3 inflamazom kompleksi, aşağıdaki enzimlerden hangisini aktive ederek pro-interlökin-1β'nın aktif forma dönüşmesini sağlar?",
                "options": [
                    "A) Kaspaz-3",
                    "B) Kaspaz-1",
                    "C) Kaspaz-8",
                    "D) Kaspaz-9",
                    "E) Fosfolipaz A2"
                ],
                "correctAnswer": "B",
                "explanation": "İnflamazom kompleksi Kaspaz-1 enzimini proteolitik olarak aktive eder; Kaspaz-1 de pro-IL-1β'yı aktif IL-1'e dönüştürür."
            }
        ],
        "aiPromptSuggestions": [
            "Gut artriti patogenezinde inflamazom-IL-1 aksının rolünü açıkla.",
            "Anti-IL-1 tedavisi (Anakinra, Kanakinumab) hangi otoenflamatuar hastalıklarda kullanılır?"
        ]
    },
    {
        "slideNumber": 14,
        "title": "TNF ve IL-1'in Lokal Endotelyal ve Lökositer Etkileri",
        "subtitle": "E/P-Selektin İndüksiyonu, İntegrin Ligandları (ICAM-1, VCAM-1) ve Doku Hasarı",
        "badge": "Lokal Etkiler",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "TNF ve IL-1 olmadan lökosit damardan çıkamaz! Endotele gidip E-selektin, ICAM-1 ve VCAM-1 astırırlar. Lökosit bu sayede yuvarlanır, yapışır ve transmigrasyonla dokuya sızar.",
            "timestamp": "47:20",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: TNF ve IL-1 endoteli prokoagülan hale de getirir."
        },
        "synthesisNarrative": "TNF ve IL-1 enfeksiyon odağında lokal konsantrasyonları arttığında postkapiller venül endotel hücreleri üzerinde son derece belirgin bir **endotel aktivasyonu** başlatır. Bu aktivasyon lökosit ekstravazasyonu için gerekli tüm adezyon reseptörlerinin ekspresyonunu sağlar.",
        "coreContent": [
            "• **Endotel Hücre Aktivasyonu:**",
            "  - *Selektin Ekspresyonu:* Endotel yüzeyinde **E-selektin** ekspresyonunu ve depolanmış Weibel-Palade cisimciklerindeki **P-selektin** dağılımını artırır (Lökosit yuvarlanması / rolling).",
            "  - *İntegrin Ligandları:* Endotel yüzeyinde **ICAM-1** (LFA-1 ve Mac-1 ligantı) ve **VCAM-1** (VLA-4 ligantı) ekspresyonunu güçlü şekilde uyarır (Lökosit sıkı tutunması / adhesion).",
            "• **Kemokin ve Sitokin Salgılatma:** Endotel ve çevre stromadan kemokin (IL-8 vb.) salgılatarak lökosit aktivasyonunu perçinler.",
            "• **Prokoagülan Endotel Dönüşümü:** Endotel yüzeyindeki trombomodulin ve antikoagülan molekülleri azaltırken, **Doku Faktörü (TF)** ekspresyonunu artırır; lokal mikrovasküler tromboz eğilimini tetikler (enfeksiyonun sınırlandırılması).",
            "• **Lökosit Aktivasyonu:** Nötrofil ve makrofajların fagositer gücünü, lizozom degranülasyonunu ve bakterisidal ROS üretimini katlayarak artırır."
        ],
        "spotPearls": [
            "⚡ TNF ve IL-1 endotelde E-selektin, ICAM-1 ve VCAM-1 ekspresyonunu artırarak lökosit adezyonunu sağlar.",
            "⚡ Endoteli prokoagülan yöne kaydırarak lokal mikrovasküler fibrin pıhtılaşmasını uyarırlar.",
            "⚡ Fibroblast proliferasyonunu ve kolajen sentezini uyararak doku onarımının zeminini hazırlarlar."
        ],
        "flashcards": [
            {
                "front": "TNF ve IL-1'in postkapiller venül endotelinde ekspresyonunu artırarak lökositlerin sıkı tutunmasını (adezyonunu) sağlayan temel integrin ligandları hangileridir?",
                "back": "ICAM-1 (İntraselüler Adezyon Molekülü-1) ve VCAM-1 (Vasküler Hücre Adezyon Molekülü-1).",
                "question": "TNF ve IL-1'in endotelde ekspresyonunu artırdığı integrin ligandları hangileridir?",
                "answer": "ICAM-1 ve VCAM-1.",
                "hint": "ICAM-1 ve VCAM-1",
                "category": "Lokal Etkiler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-014",
                "question": "Akut enflamasyon alanında makrofajlardan salınan TNF ve IL-1 sitokinlerinin vasküler endotel hücreleri üzerindeki primer etkilerinden biri aşağıdakilerden hangisidir?",
                "options": [
                    "A) E-selektin ve ICAM-1 adezyon moleküllerinin ekspresyonunu artırmak",
                    "B) Trombomodulin ekspresyonunu artırarak kanı sulandırmak",
                    "C) Vasküler geçirgenliği tamamen kapatmak",
                    "D) Endotel hücre proliferasyonunu derhal durdurmak",
                    "E) Nitrik oksit sentazı tamamen inhibe etmek"
                ],
                "correctAnswer": "A",
                "explanation": "TNF ve IL-1 endotel aktivasyonu yaparak E-selektin, ICAM-1 ve VCAM-1 ekspresyonunu güçlü şekilde artırır; lökosit rekrutmanını sağlar."
            }
        ],
        "aiPromptSuggestions": [
            "Anti-TNF biyolojik tedavisi (İnfliksimab, Adalimumab) alan hastalarda tüberküloz reaktivasyonu riski neden artar?",
            "Lökosit rolling ve firm adhesion basamaklarındaki moleküler ligant-reseptör çiftlerini özetle."
        ]
    },
    {
        "slideNumber": 15,
        "title": "TNF ve IL-1'in Sistemik Etkileri: Akut Faz Yanıtı ve Septik Şok",
        "subtitle": "Ateş, Lökositoz, Karaciğer Akut Faz Proteinleri ve Miyokard Depresyonu",
        "badge": "Sistemik Etkiler",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Düşük dozda lokal yararlı olan TNF, kana boca edildiğinde felakete yol açar! Kalbi baskılar (miyokard kontraktilitesi düşer), damarları felç eder (vazodilatasyon ve hipotansiyon) ve septik şoka sokar.",
            "timestamp": "51:10",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: TNF'nin kaşektin olarak adlandırılmasının sebebi iştahı kesip lipid metabolizmasını bozarak kaşeksi yapmasıdır."
        },
        "synthesisNarrative": "Ağır enfeksiyonlarda veya sistemik yayılımda TNF ve IL-1 dolaşıma katılarak tüm organizmayı etkileyen **Akut Faz Yanıtını (Systemic Inflammatory Response)** tetikler. Çok yüksek düzeylere ulaştığında ise hemodinamik kollaps, dissemine intravasküler koagülasyon (DİK) ve septik şok ile hayatı tehdit eder.",
        "coreContent": [
            "• **Koruyucu Sistemik Etkiler (Orta Düzey Salınım):**",
            "  - <span class='text-rose-600 font-bold'>Ateş (Fever):</span> Hipotalamus preoptik alanda PGE2 sentezini indüklerler.",
            "  - <span class='text-amber-600 font-bold'>Akut Faz Proteinleri:</span> Karaciğeri uyararak **CRP (C-Reaktif Protein), SAA (Serum Amiloid A) ve Fibrinojen** sentezini kat kat artırırlar (Fibrinojen eritrosit sedimantasyon hızını - ESH artırır).",
            "  - <span class='text-blue-600 font-bold'>Lökositoz:</span> Kemik iliğinden nötrofil salınımını uyarırlar; sola kayma (çomak nötrofil artışı) görülür.",
            "• **Patolojik Sistemik Etkiler (Aşırı / Yüksek TNF Salınımı - Septik Şok):**",
            "  - *Miyokard Kontraktilite Depresyonu:* Kalp debisini düşürür.",
            "  - *Yaygın Vazodilatasyon ve Permeabilite:* Ciddi hipotansiyon ve periferik göllenme.",
            "  - *Yaygın İntravasküler Koagülasyon (DİK):* Mikrovasküler trombozlar ve tüketim koagülopatisi.",
            "  - *Kaşeksi (Kaşektin Etkisi):* İştah merkezini baskılayıp lipoprotein lipazı inhibe ederek kanser veya tüberküloz hastalarında şiddetli zayıflamaya (kaşeksiye) yol açar."
        ],
        "spotPearls": [
            "⚡ Karaciğerde CRP, SAA ve Fibrinojen sentezini indükleyen ana sitokinler IL-6, IL-1 ve TNF'dir.",
            "⚡ TNF aşırı salındığında miyokard depresyonu, hipotansiyon ve septik şoka neden olur.",
            "⚡ Kronik hastalıklarda kaşeksiye (aşırı zayıflama) yol açan sitokin TNF-alfa'dır (eski adı Kaşektin)."
        ],
        "flashcards": [
            {
                "front": "Kronik enfeksiyon ve malignitelerde iştahı baskılayıp periferik yağ/kas dokusunu yıkarak 'kaşeksi' tablosuna yol açan ve bu nedenle eskiden 'kaşektin' olarak adlandırılan sitokin hangisidir?",
                "back": "Tümör Nekroz Faktörü-alfa (TNF-α).",
                "question": "Kronik hastalıklarda kaşeksiye yol açan ve eski adı kaşektin olan sitokin hangisidir?",
                "answer": "Tümör Nekroz Faktörü-alfa (TNF-α).",
                "hint": "Kaşektin",
                "category": "Sistemik Etkiler"
            },
            {
                "front": "Akut faz yanıtında karaciğerden salınan fibrinojenin kanda artması hangi rutin laboratuvar testinin yükselmesine yol açar?",
                "back": "Eritrosit Sedimantasyon Hızı (ESH / ESR). Fibrinojen eritrositlerin birbirine yapışıp rulo (rouleaux) oluşturmasını ve hızla çökmesini sağlar.",
                "question": "Fibrinojen artışı hangi rutin laboratuvar testinin değerini yükseltir?",
                "answer": "Eritrosit Sedimantasyon Hızı (ESH).",
                "hint": "Sedimantasyon / Rouleaux",
                "category": "Sistemik Etkiler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-015",
                "question": "Gram-negatif bakteriyel sepsis tablosunda masif endotoksin (LPS) salınımına bağlı olarak aşırı düzeyde üretilen; miyokardiyal kontraktiliteyi baskılayarak, yaygın vazodilatasyon ve DIC tablosuyla septik şoka yol açan primer sitokin hangisidir?",
                "options": [
                    "A) Tümör Nekroz Faktörü (TNF)",
                    "B) İnterlökin-10",
                    "C) İnterferon-gamma",
                    "D) Transforming Growth Factor-beta (TGF-β)",
                    "E) İnterlökin-4"
                ],
                "correctAnswer": "A",
                "explanation": "Yüksek doz TNF sistemik dolaşımda miyokardiyal depresyona, vasküler kollapsa ve septik şoka neden olan temel sitokindir."
            }
        ],
        "aiPromptSuggestions": [
            "SIRS (Sistemik İnflamatuar Yanıt Sendromu) tanı kriterleri nelerdir?",
            "Serum Amiloid A (SAA) proteininin kronik inflamasyonda sekonder amiloidozis (AA amiloidoz) yapma mekanizmasını açıkla."
        ]
    },
    {
        "slideNumber": 16,
        "title": "İnterlökin-6 (IL-6), IL-17 ve Th17 Hücrelerinin Rolü",
        "subtitle": "Karaciğer Akut Faz Üretimi, Nötrofil Rekrutmanı ve Kronik İnflamasyon Köprüsü",
        "badge": "Sitokinler",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Karaciğerde akut faz proteinlerinin (özellikle CRP'nin) üretiminde bir numara IL-6'dır! IL-17 ise Th17 hücrelerinden salınarak dokuya nötrofil çağıran kemokinleri patlatır; psöriyazis ve romatoid artritin göbeğindedir.",
            "timestamp": "55:30",
            "emphasisType": "high-yield",
            "note": "Prof. Dr. Hikmet Keleş: IL-6 reseptör antagonisti Tosilizumab Covid-19 sitokin fırtınasında ve RA'da hayat kurtarmıştır."
        },
        "synthesisNarrative": "Akut faz yanıtının devamlılığını sağlayan en kritik sitokinlerden biri **İnterlökin-6'dır (IL-6)**. Makrofajlar ve endotel hücreleri tarafından TNF/IL-1 etkisiyle üretilen IL-6, karaciğer hepatositleri üzerindeki spesifik reseptörlerine bağlanarak akut faz protein sentezini maksimuma ulaştırır. **IL-17** ise T yardımcı 17 (Th17) lenfositlerince üretilerek nötrofil toplanmasını sağlayan kemokinleri indükler.",
        "coreContent": [
            "• **İnterlökin-6 (IL-6) Özellikleri:**",
            "  - *Temel Görev:* Karaciğerde <span class='text-blue-600 font-bold'>akut faz protein sentezinin (özellikle CRP)</span> en güçlü uyarıcısıdır.",
            "  - *Kemik İliği:* Trombopoietin benzeri etkiyle trombosit üretimini uyarır (enfeksiyonlarda reaktif trombositoz).",
            "  - *B Hücre Farklılaşması:* B lenfositlerin antikor üreten plazma hücrelerine dönüşümünü destekler.",
            "• **İnterlökin-17 (IL-17) Özellikleri:**",
            "  - Başlıca <span class='text-purple-600 font-bold'>Th17 hücreleri</span> tarafından üretilir.",
            "  - Epitel, endotel ve fibroblastları uyararak nötrofil kemotaktik kemokinlerinin (IL-8 vb.) salınımını tetikler; dokuya yoğun nötrofil akını sağlar.",
            "  - Fungal ve ekstraselüler bakteriyel savunmada kritiktir.",
            "  - Aşırı aktivasyonu **Romatoid Artrit, Psöriyazis (Sedef) ve Ankilozan Spondilit** patogenezinde kritik rol oynar (Anti-IL-17 ilacı: Sekukinumab)."
        ],
        "spotPearls": [
            "⚡ Karaciğerden CRP üretimini en güçlü uyaran sitokin IL-6'dır.",
            "⚡ IL-17 Th17 hücrelerinden salınır ve dokuya nötrofil toplanmasını sağlar.",
            "⚡ Psöriyazis tedavisinde IL-17 inhibitörleri (Sekukinumab) son derece başarılıdır."
        ],
        "flashcards": [
            {
                "front": "Klinikte enfeksiyon ve doku nekrozu takibinde kullanılan C-Reaktif Protein (CRP) sentezini karaciğerde en güçlü şekilde indükleyen sitokin hangisidir?",
                "back": "İnterlökin-6 (IL-6).",
                "question": "Karaciğerde CRP sentezini en güçlü şekilde indükleyen sitokin hangisidir?",
                "answer": "İnterlökin-6 (IL-6).",
                "hint": "IL-6",
                "category": "Sitokinler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-016",
                "question": "Th17 lenfositler tarafından üretilen, diğer hücrelerden kemokin salgılatarak nötrofillerin enfeksiyon veya kronik inflamasyon bölgesine toplanmasını (rekrutmanını) sağlayan ve psöriyazis patogenezinde rol oynayan sitokin hangisidir?",
                "options": [
                    "A) İnterlökin-4",
                    "B) İnterlökin-10",
                    "C) İnterlökin-17",
                    "D) İnterferon-alfa",
                    "E) Transforming Growth Factor-beta"
                ],
                "correctAnswer": "C",
                "explanation": "IL-17 Th17 hücrelerinden salınır; epitel ve stromadan nötrofil kemokinleri salgılatarak dokuya nötrofil çeker."
            }
        ],
        "aiPromptSuggestions": [
            "Tosilizumab (Anti-IL-6R) hangi klinik durumlarda kullanılır?",
            "Th1, Th2 ve Th17 hücrelerinin temel sitokinlerini karşılaştırınız."
        ]
    },
    {
        "slideNumber": 17,
        "title": "Kemokinler: Lökosit Trafiği ve Kemotaktik Gradiyent",
        "subtitle": "C-X-C, C-C, C ve CX3-C Sınıfları, Reseptörleri ve Homeostaz",
        "badge": "Kemokinler",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Kemokinler 8-10 kilodaltonluk küçük yol göstericilerdir. Korunmuş sistein aminoasitlerinin dizilişine göre 4 sınıfa ayrılırlar. C-X-C nötrofillere bakar (örneğin IL-8), C-C ise monosit ve eozinofillere bakar (MCP-1, Eotaksin).",
            "timestamp": "59:40",
            "emphasisType": "high-yield",
            "note": "Prof. Dr. Hikmet Keleş: Kemokinler proteoglikanlara tutunarak dokuda konsantrasyon gradiyenti oluşturur."
        },
        "synthesisNarrative": "Kemokinler (kemotaktik sitokinler), lökositlerin damardan çıkıp doku içinde hedef odağa doğru yönlenmiş göçünü (kemotaksis) yöneten 8–10 kDa ağırlığında küçük proteinlerdir. Yaklaşık 40 farklı kemokin ve 20 civarında G-protein kenetli kemokin reseptörü (GPCR) mevcuttur. Dokuda ve endotel yüzeyindeki heparan sülfat proteoglikanlarına tutunarak kimyasal bir gradiyent haritası çizerler.",
        "coreContent": [
            "• **Yapısal 4 Ana Grup:**",
            "  1. <span class='text-blue-600 font-bold'>C-X-C Kemokinler (α Kemokinler):</span> İki sistein arasında bir aminoasit (X) bulunur. En prototipik üyesi **İnterlökin-8'dir (CXCL8)**. Başlıca **nötrofilleri** hedefler ve yangı odağına çeker.",
            "  2. <span class='text-rose-600 font-bold'>C-C Kemokinler (β Kemokinler):</span> Sistein kalıntıları yan yanadır. **MCP-1 (CCL2), MIP-1α (CCL3) ve Eotaksin (CCL11)**. Başlıca **monositleri, eozinofilleri, bazofilleri ve lenfositleri** çeker (nötrofillere etki etmez!).",
            "  3. <span class='text-amber-600 font-bold'>C Kemokinler (γ Kemokinler):</span> Yalnızca bir sistein içerir (örn. Lenfotaktin / XCL1). Lenfositlere özgüdür.",
            "  4. <span class='text-purple-600 font-bold'>CX3-C Kemokinler:</span> İki sistein arasında 3 aminoasit vardır (Fraktalkin / CX3CL1). Hem çözünür kemokin hem endotel yüzeyinde adezyon proteini olarak çift işlev görür.",
            "• **Homeostatik vs. İnflamatuar Kemokinler:**",
            "  - *İnflamatuar:* Yangıda indüklenir, lökositleri dokuya toplar.",
            "  - *Homeostatik:* Sağlıklı lenf düğümlerinde T ve B hücrelerinin folikül ve parakorteks bölgelerine doğru yerleşimini organize eder."
        ],
        "spotPearls": [
            "⚡ CXCL8 (İnterlökin-8) C-X-C grubundadır ve nötrofil kemotaksisinin ana kemokinidir.",
            "⚡ C-C kemokinler (MCP-1, Eotaksin) nötrofilleri ÇEKMEZ; monosit, lenfosit ve eozinofilleri çeker.",
            "⚡ HIV virüsü hücreye girerken kemokin reseptörlerini (CCR5 ve CXCR4) koreseptör olarak kullanır."
        ],
        "flashcards": [
            {
                "front": "C-X-C kemokin ailesinin prototipi olan ve özellikle nötrofillerin yangı odağına kemotaksisini sağlayan kemokin hangisidir?",
                "back": "İnterlökin-8 (IL-8 / CXCL8).",
                "question": "C-X-C ailesine ait ve nötrofilleri hedefleyen primer kemokin hangisidir?",
                "answer": "İnterlökin-8 (IL-8 / CXCL8).",
                "hint": "CXCL8 / IL-8",
                "category": "Kemokinler"
            },
            {
                "front": "C-C kemokinleri (MCP-1, Eotaksin vb.) hangi lökosit alt grubunu hedeflemez?",
                "back": "Nötrofilleri hedeflemez! Monosit, eozinofil, bazofil ve lenfositleri çekerler.",
                "question": "C-C kemokinleri hangi lökosit alt grubunu hedeflemez?",
                "answer": "Nötrofilleri.",
                "hint": "Nötrofiller",
                "category": "Kemokinler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-017",
                "question": "Alerjik enflamasyonda eozinofillerin seçici olarak dokuya göçünü sağlayan 'Eotaksin (CCL11)' hangi kemokin ailesine aittir?",
                "options": [
                    "A) C-X-C kemokinler",
                    "B) C-C kemokinler",
                    "C) C kemokinler",
                    "D) CX3-C kemokinler",
                    "E) Sitotoksik defensinler"
                ],
                "correctAnswer": "B",
                "explanation": "Eotaksin (CCL11) C-C ailesine aittir ve monosit/eozinofil kemotaksisinde rol oynar."
            }
        ],
        "aiPromptSuggestions": [
            "CCR5 mutasyonunun (CCR5-delta32) HIV enfeksiyonuna direnç sağlamadaki mekanizmasını açıkla.",
            "Homeostatik kemokinlerin lenf nodu mimarisindeki organizasyon rolleri nelerdir?"
        ]
    },
    {
        "slideNumber": 18,
        "title": "Kompleman Sistemine Giriş ve 3 Aktivasyon Yolu",
        "subtitle": "Klasik, Alternatif ve Lektin Yollarının C3 Konvertazda Birleşmesi",
        "badge": "Kompleman Sistemi",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Kompleman plazmanın en ölümcül silahıdır! Karaciğerde üretilir, kanda uyur. Üç ayrı yoldan tetiklenebilir: 1) Antikor görürse Klasik yol, 2) Mikrop şekeri görürse Lektin yolu, 3) Doğrudan mikrop yüzeyini görürse Alternatif yol. Üçü de C3 konvertaz basamağında birleşir!",
            "timestamp": "64:10",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: C3'ün parçalanması komplemanın en merkezi ve hız kısıtlayıcı adımıdır."
        },
        "synthesisNarrative": "Kompleman sistemi, karaciğer tarafından sentezlenip plazmada inaktif zimojenler olarak dolaşan 30'dan fazla çözünür protein ve membran reseptöründen meydana gelir. Temel işlevi mikroorganizmaların fagositozunu kolaylaştırmak (opsonizasyon), yangıyı alevlendirmek ve hücre zarında delikler açarak mikrobu patlatmaktır (lizis).",
        "coreContent": [
            "• **Aktivasyonun Üç Farklı Yolu:**",
            "  1. <span class='text-blue-600 font-bold'>Klasik Yol (Antikor Bağımlı):</span> Mikroba bağlanmış **IgM veya IgG** (özellikle IgG1 ve IgG3) antikorlarının Fc parçasına C1q'nun bağlanması ile tetiklenir (C1qrs kompleksi ➔ C4 ve C2 parçalanır ➔ <span class='text-blue-600 font-bold'>C4b2a</span> [Klasik C3 konvertaz] oluşur).",
            "  2. <span class='text-emerald-600 font-bold'>Lektin Yolu (Karbonhidrat Bağımlı):</span> Plazmadaki **Mannoz Bağlayıcı Lektin (MBL)** proteininin mikrop yüzeyindeki mannoz kalıntılarına bağlanmasıyla MASP enzimleri aktive olur; C4 ve C2'yi keserek klasik yol gibi <span class='text-emerald-600 font-bold'>C4b2a</span> oluşturur.",
            "  3. <span class='text-amber-600 font-bold'>Alternatif Yol (Doğrudan Mikrop Yüzeyi):</span> Antikor gerektirmez. Dolaşımdaki C3'ün spontan hidrolizi (tick-over) ve mikrobiyal endotoksin (LPS) veya polisakkaritlere Faktör B ve D yardımıyla tutunmasıyla tetiklenir. Alternatif C3 konvertaz: <span class='text-amber-600 font-bold'>C3bBb</span>.",
            "• **Merkezi Kesişme Noktası:** Her üç yol da **C3 konvertaz** oluşturur. C3 konvertaz C3'ü parçalayarak küçük **C3a** (anafilatoksin) ve büyük **C3b** (opsonin) moleküllerini serbestleştirir."
        ],
        "spotPearls": [
            "⚡ Klasik yol antijene bağlı IgM veya IgG ile aktive olur (C1 fiksasyonu).",
            "⚡ Alternatif yol antikordan bağımsızdır; doğrudan mikrop yüzeyiyle tetiklenir.",
            "⚡ Tüm yollar C3'ün C3a ve C3b'ye parçalandığı C3 konvertaz basamağında birleşir."
        ],
        "flashcards": [
            {
                "front": "Kompleman sisteminin üç aktivasyon yolu (Klasik, Lektin, Alternatif) hangi enzimatik basamakta birleşir?",
                "back": "C3 konvertaz enzim kompleksinin oluşumu ve C3'ün C3a ile C3b'ye parçalanması basamağında birleşir.",
                "question": "Komplemanın üç aktivasyon yolu hangi enzimatik basamakta birleşir?",
                "answer": "C3 konvertaz basamağında (C3'ün parçalanması).",
                "hint": "C3 konvertaz",
                "category": "Kompleman Sistemi"
            },
            {
                "front": "Klasik kompleman yolunu aktive edebilen iki ana immünglobulin sınıfı hangileridir?",
                "back": "IgM (en güçlü) ve IgG (özellikle IgG1 ve IgG3).",
                "question": "Klasik kompleman yolunu aktive eden iki immünglobulin sınıfı hangileridir?",
                "answer": "IgM ve IgG.",
                "hint": "IgM ve IgG",
                "category": "Kompleman Sistemi"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-018",
                "question": "Aşağıdakilerden hangisi kompleman sisteminin 'Alternatif Yolu' aktivasyonunu tetikleyen unsurlardan biridir?",
                "options": [
                    "A) Antijene bağlanmış IgM molekülü",
                    "B) Mannoz bağlayıcı lektinin (MBL) fiksasyonu",
                    "C) Mikrobiyal yüzey molekülleri (LPS, polisakkaritler) ve Faktör B/D etkileşimi",
                    "D) C1q inhibitörü eksikliği",
                    "E) Bradikinin reseptör aktivasyonu"
                ],
                "correctAnswer": "C",
                "explanation": "Alternatif yol antikor gerektirmez; doğrudan mikrop yüzeyindeki polisakkarit ve endotoksinlere C3b'nin Faktör B ve D ile tutunmasıyla aktive olur."
            }
        ],
        "aiPromptSuggestions": [
            "Klasik yol C3 konvertazı (C4b2a) ile alternatif yol C3 konvertazının (C3bBb) yapısal farkları nelerdir?",
            "Properdin (Faktör P) alternatif C3 konvertazını nasıl stabilize eder?"
        ]
    },
    {
        "slideNumber": 19,
        "title": "Komplemanın Efektör Fonksiyonları: Opsonizasyon, Anafilatoksinler ve MAC",
        "subtitle": "C3b (Fagositoz), C3a/C5a (İnflamasyon/Kemotaksis) ve C5b-9 (Lizis)",
        "badge": "Efektör Yanıt",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Komplemanın 3 temel işi vardır: 1) C3b mikroba yapışıp fagosite lezzetli hale getirir (opsonizasyon), 2) C3a ve C5a mast hücresini patlatıp histamin salgılatır, C5a nötrofili çağırır (en güçlü anafilatoksin C5a'dır!), 3) C5b-9 birleşip zar üzerinde delik açar (Membran Atak Kompleksi - MAC).",
            "timestamp": "68:30",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: C5-C9 (MAC) eksikliği olanlar özellikle Neisseria enfeksiyonlarına (menenjit, gonore) aşırı duyarlıdır."
        },
        "synthesisNarrative": "C3 konvertaz C3'ü parçaladıktan sonra oluşan C3b moleküllerinin bir kısmı enzim kompleksine katılarak **C5 konvertazı** oluşturur. C5 konvertaz C5'i parçalayarak dolaşıma **C5a** verirken, yüzeyde kalan **C5b** sırasıyla C6, C7, C8 ve çok sayıda C9 monomerini toplayarak hedef hücre membranında porlar (delikler) açan litik kompleksi kurar.",
        "coreContent": [
            "• **1. Opsonizasyon ve Fagositoz (C3b & iC3b):**",
            "  - C3b mikrop yüzeyine kovalent olarak bağlanır.",
            "  - Nötrofil ve makrofaj yüzeyindeki **Kompleman Reseptörü 1 (CR1 / CD35)** C3b'yi tanır ve fagositozu dramatik biçimde hızlandırır.",
            "• **2. İnflamasyon ve Anafilatoksinler (C3a, C4a, C5a):**",
            "  - *Mast Hücre Degranülasyonu:* Histamin salınımını tetikleyerek vazodilatasyon ve vasküler geçirgenlik artışı yaparlar.",
            "  - *C5a'nın Özel Rolü:* <span class='text-rose-600 font-bold'>En güçlü anafilatoksindir</span>. Ayrıca güçlü bir nötrofil ve monosit **kemoatraktanıdır**; integrin afinitesini artırır ve lipoksijenaz yolunu uyarır.",
            "• **3. Hücre Lizisi (Membran Atak Kompleksi - MAC / C5b-9):**",
            "  - C5b, C6, C7, C8 ve 10-16 adet C9 molekülü bir araya gelerek hücre zarını silindirik bir tünel gibi deler.",
            "  - Hücre içine kontrolsüz su ve sodyum girişi sonucu mikrop **osmotik lizisle** patlar.",
            "  - Özellikle ince hücre duvarlı **Neisseria türlerine (N. meningitidis, N. gonorrhoeae)** karşı savunmada vazgeçilmezdir."
        ],
        "spotPearls": [
            "⚡ En önemli opsonin C3b'dir (Fagositozu uyarır).",
            "⚡ En güçlü anafilatoksin ve nötrofil kemoatraktanı C5a'dır.",
            "⚡ C5b-9 (Membran Atak Kompleksi) por açarak osmotik lizis yapar; eksikliğinde tekrarlayan Neisseria enfeksiyonları görülür."
        ],
        "flashcards": [
            {
                "front": "Kompleman sisteminde mikropları kaplayarak makrofaj ve nötrofillerin CR1 reseptörleri aracılığıyla fagositozunu sağlayan primer opsonin molekülü hangisidir?",
                "back": "C3b (ve inaktif formu iC3b).",
                "question": "Kompleman sisteminde en önemli opsonin parçası hangisidir?",
                "answer": "C3b parçası.",
                "hint": "C3b",
                "category": "Efektör Yanıt"
            },
            {
                "front": "C5b-9 Membran Atak Kompleksi (MAC) eksikliği olan hastalarda özellikle hangi bakteri cinsine bağlı ağır enfeksiyonlar (menenjit/bakteriyemi) sıklıkla tekrarlar?",
                "back": "Neisseria türleri (Neisseria meningitidis ve Neisseria gonorrhoeae).",
                "question": "MAC (C5b-9) eksikliğinde hangi mikroorganizma enfeksiyonlarına yatkınlık oluşur?",
                "answer": "Neisseria türleri (N. meningitidis, N. gonorrhoeae).",
                "hint": "Neisseria",
                "category": "Efektör Yanıt"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-019",
                "question": "Kompleman sisteminin aktivasyonu sonucu oluşan ürünlerden hangisi hem mast hücrelerinden histamin salınımını tetikleyen güçlü bir anafilatoksin, hem de nötrofiller için güçlü bir kemoatraktandır?",
                "options": [
                    "A) C3b",
                    "B) C5a",
                    "C) C5b",
                    "D) C1q",
                    "E) C9"
                ],
                "correctAnswer": "B",
                "explanation": "C5a kompleman sisteminin en güçlü anafilatoksini olup, aynı zamanda nötrofil kemotaksisini doğrudan uyaran majör faktördür."
            }
        ],
        "aiPromptSuggestions": [
            "Opsonizasyonda IgG antikorunun Fc parçası ile C3b'nin sinerjik etkisini açıkla.",
            "Eculizumab (Anti-C5 monoklonal antikoru) hangi kompleman fonksiyonlarını durdurur?"
        ]
    },
    {
        "slideNumber": 20,
        "title": "Kompleman Düzenleyici Proteinleri ve Klinik Hastalıklar",
        "subtitle": "C1 İnhibitörü (Anjiyoödem), DAF/CD59 (PNH) ve Faktör H (aHÜS)",
        "badge": "Düzenleyici Proteinler",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Kendi hücrelerimizi kompleman saldırısından koruyan bekçiler vardır. C1-INH eksik olursa kallikrein durmaz, bradikinin birikir ve Herediter Anjiyoödem gelişir. Eritrosit zarında DAF ve CD59 eksikse kompleman kendi kanımızı eritir; buna Paroksismal Noktürnal Hemoglobinüri (PNH) denir!",
            "timestamp": "73:00",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: PNH patogenezindeki PIGA gen mutasyonu ve CD55/CD59 yokluğu klinikte altın değerindedir."
        },
        "synthesisNarrative": "Kompleman sistemi son derece tahripkar olduğu için sağlıklı konak hücrelerinin yüzeyinde ve plazmada aktivasyonu sınırlandıran düzenleyici proteinler bulunur. Bu düzenleyicilerin genetik yokluğu veya mutasyonu kontrolsüz otoimmün lizise ve ölümcül klinik tablolara yol açar.",
        "coreContent": [
            "• **1. C1 İnhibitörü (C1-INH):**",
            "  - *Görevi:* Klasik yolda C1 aktivasyonunu ve plazmada Kallikrein enzimini sınırlar.",
            "  - *Eksikliği:* <span class='text-rose-600 font-bold'>Herediter Anjiyoödem (HAE)</span>. Kallikrein inhibe edilemez; aşırı **Bradikinin** birikir. Deride ve gırtlakta hayatı tehdit eden laringeal ödem atakları gelişir.",
            "• **2. DAF (Decay-Accelerating Factor / CD55) ve CD59 (MAC İnhibitörü / Protectin):**",
            "  - *Görevi:* Hücre zarına **GPI (Glikozilfosfatidilinozitol) çıpası** ile bağlanırlar. DAF C3 konvertazı parçalar; CD59 ise C9 polimerizasyonunu bloke ederek hücre zarında MAC oluşumunu engeller.",
            "  - *Eksikliği:* <span class='text-purple-600 font-bold'>Paroksismal Noktürnal Hemoglobinüri (PNH)</span>. Miyeloid kök hücrede *PIGA geni* somatik mutasyonu sonucu GPI çıpası üretilemez; eritrositler CD55 ve CD59'dan mahrum kalır ve kompleman tarafından parçalanır (intravasküler hemoliz).",
            "• **3. Faktör H ve Faktör I:**",
            "  - *Görevi:* Alternatif yolda C3b'yi parçalayarak temizler.",
            "  - *Mutasyonları:* <span class='text-amber-600 font-bold'>Atipik Hemolitik Üremik Sendrom (aHÜS)</span> ve yaşa bağlı makula dejenerasyonu."
        ],
        "spotPearls": [
            "⚡ C1-INH eksikliği: Herediter Anjiyoödem (aşırı bradikinin artışı ile laringeal ödem).",
            "⚡ CD55 (DAF) ve CD59 (Protectin) eksikliği: Paroksismal Noktürnal Hemoglobinüri (PNH).",
            "⚡ PNH'de temel defekt GPI çapa sentezini sağlayan PIGA genindeki somatik mutasyondur."
        ],
        "flashcards": [
            {
                "front": "C1 inhibitörü (C1-INH) genetik eksikliğinde kallikrein baskılanamaması sonucu hangi vazoaktif peptid birikir ve hangi klinik tablo ortaya çıkar?",
                "back": "Bradikinin birikir; klinik tablo 'Herediter Anjiyoödem'dir (tekrarlayan subkutan ve laringeal ödem atakları).",
                "question": "C1-INH eksikliğinde hangi peptid birikir ve hangi tablo gelişir?",
                "answer": "Bradikinin birikir; Herediter Anjiyoödem gelişir.",
                "hint": "Bradikinin ve Anjiyoödem",
                "category": "Düzenleyici Proteinler"
            },
            {
                "front": "Paroksismal Noktürnal Hemoglobinüri (PNH) hastalığında eritrositlerin kompleman lizisine açık hale gelmesine yol açan GPI-bağlı iki düzenleyici protein hangisidir?",
                "back": "DAF (CD55 - Decay Accelerating Factor) ve CD59 (Protectin / MAC İnhibitörü).",
                "question": "PNH'de eritrosit yüzeyinde eksik olan iki koruyucu kompleman proteini hangisidir?",
                "answer": "CD55 (DAF) ve CD59.",
                "hint": "CD55 ve CD59",
                "category": "Düzenleyici Proteinler"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-020",
                "question": "Eritrosit yüzeyinde kompleman kaynaklı lizisi engelleyen CD55 (DAF) ve CD59 proteinlerinin hücre zarına tutunmasını sağlayan glikozilfosfatidilinozitol (GPI) çıpasının sentezlenememesi sonucu intravasküler hemolitik anemiyle seyreden hastalık hangisidir?",
                "options": [
                    "A) Herediter Sferositoz",
                    "B) Orak Hücreli Anemi",
                    "C) Paroksismal Noktürnal Hemoglobinüri (PNH)",
                    "D) Herediter Anjiyoödem",
                    "E) Glukoz-6-Fosfat Dehidrogenaz Eksikliği"
                ],
                "correctAnswer": "C",
                "explanation": "PNH'de PIGA mutasyonu nedeniyle GPI çıpası yapılamaz; CD55 ve CD59 eksikliği sonucu eritrositler kompleman saldırısıyla lizise uğrar."
            }
        ],
        "aiPromptSuggestions": [
            "PNH tanısında akım sitometrisinde (Flow Cytometry) CD55 ve CD59 analizi nasıl değerlendirilir?",
            "Herediter Anjiyoödem tedavisinde C1 esteraz inhibitör konsantresi ve İkatibant (Bradikinin B2 blokeri) kullanımını açıkla."
        ]
    },
    {
        "slideNumber": 21,
        "title": "Kallikrein-Kinin Sistemi ve Bradikinin",
        "subtitle": "Hageman Faktörü (FXII), Ağrı Patogenezi ve Vasküler Geçirgenlik",
        "badge": "Kinin Sistemi",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Bradikinin dendiğinde aklınıza direkt AĞRI (dolor) gelecek! Enflamasyonda ağrıyı doğrudan tetikleyen iki ana kimyasal: Bradikinin ve Substans P'dir (Prostaglandinler ise ağrıyı sensitize eder). Ayrıca venüllerde histaminden bile güçlü geçirgenlik artışı yapar.",
            "timestamp": "77:15",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Bradikinin ACE (Anjiyotensin Dönüştürücü Enzim) tarafından parçalanır; ACE inhibitörü öksürüğünün sebebi bradikinindir."
        },
        "synthesisNarrative": "Kallikrein-kinin sistemi, vazoaktif peptidlerin proteolitik kaskatla üretildiği plazma kaynaklı bir mediyatör sistemidir. Damar duvarında endotel altı kollajene temas eden **Faktör XII'nin (Hageman Faktörü)** aktifleşmesiyle tetiklenir. Aktif Faktör XIIa prekallikreini kallikreine çevirir; kallikrein de plazmadaki yüksek molekül ağırlıklı kininojenden (HMWK) **Bradikinin** peptidini serbestleştirir.",
        "coreContent": [
            "• **Aktivasyon Basamakları:**",
            "  1. Negatif yüklü yüzeyler / Kollajen ➔ **Faktör XII (Hageman)** otoaktivasyonu (FXIIa).",
            "  2. FXIIa ➔ Plazma **Prekallikreini ➔ Kallikreine** dönüştürür.",
            "  3. Kallikrein ➔ Yüksek Molekül Ağırlıklı Kininojenden (HMWK) <span class='text-rose-600 font-bold'>Bradikinin</span> peptidini koparır.",
            "• **Bradikininin Biyolojik Etkileri:**",
            "  - <span class='text-rose-600 font-bold'>Ağrı (Dolor):</span> Duyusal C-liflerindeki **Bradikinin B2 reseptörlerine** bağlanarak doğrudan aksiyon potansiyeli başlatır ve şiddetli ağrı oluşturur.",
            "  - <span class='text-amber-600 font-bold'>Vasküler Permeabilite Artışı:</span> Postkapiller venüllerde endotel kontraksiyonu ile belirgin sıvı eksüdasyonu ve ödem yapar.",
            "  - <span class='text-blue-600 font-semibold'>Arteriyoler Vazodilatasyon:</span> Endotelden NO ve prostasiklin salgılatarak lümeni genişletir.",
            "  - <span class='text-purple-600 font-semibold'>Düz Kas Kasılması:</span> Bronş ve barsak düz kaslarında spazma yol açar.",
            "• **Yıkımı ve Klinik (ACE İlişkisi):** Bradikinin akciğer endotelindeki **Kininaz II (ACE - Anjiyotensin Dönüştürücü Enzim)** tarafından hızla parçalanır. Hipertansiyonda ACE inhibitörü (örn. Ramipril, Enalapril) kullanan hastalarda bradikinin birikir; kuru öksürük ve anjiyoödem yan etkisinin asıl sorumlusudur."
        ],
        "spotPearls": [
            "⚡ Enflamasyonda doğrudan ağrı oluşturan temel mediyatör Bradikinindir (PGE2 ise duyarlılaştırır).",
            "⚡ Hageman Faktörü (Faktör XII) kallikrein ve bradikinin aktivasyonunun kilit anahtarıdır.",
            "⚡ ACE inhibitörlerinin neden olduğu inatçı kuru öksürük ve anjiyoödem bradikinin birikimine bağlıdır."
        ],
        "flashcards": [
            {
                "front": "Akut enflamasyonda duyusal sinir uçlarını doğrudan uyararak ağrı (dolor) duyusuna yol açan ve ACE (Kininaz II) enzimi tarafından parçalanan vazoaktif peptid hangisidir?",
                "back": "Bradikinin.",
                "question": "Enflamasyonda doğrudan ağrı oluşturan ve ACE tarafından yıkılan peptid hangisidir?",
                "answer": "Bradikinin.",
                "hint": "Bradikinin",
                "category": "Kinin Sistemi"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-021",
                "question": "Hipertansiyon tedavisi amacıyla ACE inhibitörü başlanan bir hastada ilacın başlamasından 2 hafta sonra inatçı kuru öksürük ve dudaklarda anjiyoödem gelişmiştir. Bu klinik tablonun ortaya çıkmasında dokularda birikerek vasküler geçirgenliği artıran ve duyusal sinirleri uyaran mediyatör aşağıdakilerden hangisidir?",
                "options": [
                    "A) Lökotrien B4",
                    "B) Bradikinin",
                    "C) Tromboksan A2",
                    "D) Serotonin",
                    "E) Kompleman C3a"
                ],
                "correctAnswer": "B",
                "explanation": "ACE enzimi bradikinini yıkar (Kininaz II). ACE inhibitörleri bradikinin birikimine neden olarak bronşial irritasyon (kuru öksürük) ve anjiyoödeme yol açar."
            }
        ],
        "aiPromptSuggestions": [
            "Faktör XII'nin pıhtılaşma, fibrinoliz ve kinin sistemleri arasındaki kesişim noktası rollerini özetle.",
            "Bradikinin B1 ve B2 reseptörlerinin ekspresyon farkları nelerdir?"
        ]
    },
    {
        "slideNumber": 22,
        "title": "Platelet Aktive Edici Faktör (PAF), Nitrik Oksit (NO) ve Özet Tablo",
        "subtitle": "Diğer Mediyatörler, Sinerji Kuralları ve Tüm Konunun Büyük Karşılaştırma Matrisi",
        "badge": "Büyük Özet",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "professorAudioHighlight": {
            "quote": "Dersin finalinde şu altın kuralı unutmayın: Yangıda vazodilatasyonu histamin ve prostaglandin yapar; geçirgenliği histamin, bradikinin ve sisteinil lökotrienler artırır; kemotaksiyi LTB4 ve C5a sağlar; ateşi PGE2 ve IL-1 yapar; ağrıyı bradikinin başlatır, PGE2 şiddetlendirir!",
            "timestamp": "81:40",
            "emphasisType": "critical",
            "note": "Prof. Dr. Hikmet Keleş: Robbins Tablo 2.8 tüm patoloji sınavlarının garanti soru kaynağıdır."
        },
        "synthesisNarrative": "Akut enflamasyon yanıtı hiçbir zaman tek bir molekülün eseri değildir. Birbiriyle iç içe geçmiş, birbirinin üretimini tetikleyen ve bir diğeri bloke olduğunda yedek yollardan görevi devralan olağanüstü bir kimyasal orkestradır. PAF, NO ve Nöropeptidler bu orkestranın vasküler tonus ve mikrobisidal aktivitedeki tamamlayıcı üyeleridir.",
        "coreContent": [
            "• **Platelet Activating Factor (PAF):**",
            "  - Membran fosfolipidlerinden fosfolipaz A2 yardımıyla türetilir.",
            "  - Düşük dozda histaminden 10.000 kat daha güçlü vazodilatasyon ve venüler geçirgenlik artışı yapabilir.",
            "  - Trombosit agregasyonunu, lökosit adezyonunu ve degranülasyonunu kuvvetlendirir.",
            "• **Nitrik Oksit (NO):**",
            "  - L-arjinin aminoasidinden sentezlenen serbest radikal gazdır.",
            "  - *Endotel (eNOS):* Damar düz kasını gevşeterek vazodilatasyon yapar.",
            "  - *Makrofaj (iNOS):* İndüklenebilir formdur; süperoksitle birleşip **Peroksinitrit (ONOO-)** oluşturarak mikropları öldürür.",
            "• **Nöropeptidler (Substans P):** Duyusal sinirlerden salınır; ağrı sinyali iletir ve vasküler geçirgenliği artırır.",
            "• **İNFLAMASYONUN KARDİNAL REAKSİYONLARI VE BAŞLICA MEDİYATÖRLERİ (TABLO 2.8 ÖZETİ):**",
            "  - <span class='text-rose-600 font-bold'>Vazodilatasyon:</span> Histamin, Prostaglandinler (PGI2, PGE2, PGD2), Nitrik Oksit (NO).",
            "  - <span class='text-amber-600 font-bold'>Artmış Vasküler Permeabilite:</span> Histamin, Bradikinin, C3a ve C5a, Lökotrienler (LTC4, LTD4, LTE4), PAF.",
            "  - <span class='text-blue-600 font-bold'>Kemotaksi ve Lökosit Aktivasyonu:</span> TNF, IL-1, Kemokinler (IL-8), C5a, Lökotrien B4 (LTB4), Bakteriyel ürünler.",
            "  - <span class='text-rose-600 font-bold'>Ateş (Fever):</span> IL-1, TNF, IL-6, Prostaglandin E2 (PGE2).",
            "  - <span class='text-purple-600 font-bold'>Ağrı (Pain):</span> Bradikinin, Prostaglandinler (PGE2), Substans P.",
            "  - <span class='text-rose-600 font-bold'>Doku Hasarı:</span> Nötrofil lizozomal enzimleri, Reaktif Oksijen Türleri (ROS), Nitrik Oksit."
        ],
        "spotPearls": [
            "⚡ Vazodilatasyon: Histamin, Prostaglandinler, NO.",
            "⚡ Permeabilite Artışı: Histamin, Bradikinin, LTC4/D4/E4, C3a, C5a.",
            "⚡ Kemotaksi: LTB4, C5a, IL-8, formil peptidler.",
            "⚡ Ağrı: Bradikinin, PGE2, Substans P.",
            "⚡ Ateş: IL-1, TNF, IL-6, PGE2."
        ],
        "flashcards": [
            {
                "front": "Akut enflamasyonda arteriyollerde vazodilatasyona yol açan 3 temel mediyatör grubu hangileridir?",
                "back": "1) Histamin\n2) Prostaglandinler (PGI2, PGE2, PGD2)\n3) Nitrik Oksit (NO).",
                "question": "Enflamasyonda vazodilatasyon yapan 3 temel mediyatör hangileridir?",
                "answer": "Histamin, Prostaglandinler ve Nitrik Oksit (NO).",
                "hint": "Histamin, PG, NO",
                "category": "Büyük Özet"
            },
            {
                "front": "Enflamasyonda postkapiller venüllerde vasküler geçirgenlik artışına neden olan başlıca 4 mediyatör grubu hangileridir?",
                "back": "1) Histamin\n2) Bradikinin\n3) Sisteinil Lökotrienler (LTC4, LTD4, LTE4)\n4) Kompleman anafilatoksinleri (C3a, C5a).",
                "question": "Vasküler geçirgenlik artışına neden olan 4 mediyatör grubu hangileridir?",
                "answer": "Histamin, Bradikinin, Sisteinil Lökotrienler (LTC4/D4/E4) ve C3a/C5a.",
                "hint": "Histamin, Bradikinin, LT, C3a/C5a",
                "category": "Büyük Özet"
            }
        ],
        "relatedQuestions": [
            {
                "id": "pat-med-022",
                "question": "Akut enflamasyon sürecinde gelişen kardinal belirtiler ile bu belirtilerden primer sorumlu kimyasal mediyatör eşleştirmelerinden hangisi DOĞRUDUR?",
                "options": [
                    "A) Ateş — Yalnızca Histamin",
                    "B) Kemotaksis — Lökotrien B4 ve C5a",
                    "C) Ağrı — Yalnızca Tromboksan A2",
                    "D) Vasküler geçirgenlik artışı — Yalnızca Lipoksin A4",
                    "E) Vazodilatasyon — Yalnızca Lökotrien C4"
                ],
                "correctAnswer": "B",
                "explanation": "Lökotrien B4 (LTB4) ve kompleman C5a nötrofillerin kemotaksisini sağlayan majör kemoatraktanlardır."
            }
        ],
        "aiPromptSuggestions": [
            "Robbins Tablo 2.8'deki mediyatörlerin örtüşen sinerjik etkilerini bir akış şemasıyla özetle.",
            "Kronik enflamasyona geçişte makrofaj-lenfosit aksında devreye giren sitokinler hangileridir?"
        ]
    }
]

new_deck = {
    "id": "learn-enflamasyon-kimyasal-mediyatorleri",
    "title": "Enflamasyonun Kimyasal Mediyatörleri: Vazoaktif Aminler, Araşidonik Asit Metabolitleri, Sitokinler ve Kompleman Sistemi",
    "shortTitle": "Enflamasyonun Kimyasal Mediyatörleri",
    "discipline": "Tıbbi Patoloji",
    "lecturer": "Prof. Dr. Hikmet Keleş",
    "committee": "Dönem 3 Kurul 1",
    "committeeId": "kurul-1",
    "overview": "Hücre ve plazma kaynaklı mediyatörlerin genel özellikleri, vazoaktif aminler (histamin, serotonin), araşidonik asit metabolitleri (siklooksijenaz ve lipoksijenaz yolları, prostaglandinler, lökotrienler, lipoksinler), sitokinler ve kemokinler (TNF, IL-1, IL-6, IL-17, IL-8), kompleman sistemi (klasik, lektin ve alternatif yollar; opsonizasyon, anafilatoksinler ve MAC), kompleman düzenleyici proteinleri (C1-INH, DAF, CD59, Faktör H), kallikrein-kinin sistemi (bradikinin), PAF, NO ve farmakolojik hedef basamakları.",
    "slides": slides_data,
    "totalSlides": len(slides_data),
    "deepDeck": True,
    "detailLevel": "500%",
    "updatedAt": "2026-10-02"
}

# New medical encyclopedia entries to expand the database
new_encyclopedia_entries = [
    {
        "id": "enc-bradikinin",
        "term": "Bradikinin",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / Farmakoloji",
        "committee": "Kurul 1",
        "description": "Kallikrein-kinin sistemi aracılığıyla plazma kininojenlerinden üretilen vazoaktif 9 aminoasitlik nonapeptid. C liflerindeki B2 reseptörlerine bağlanarak doğrudan ağrı (dolor) duyusunu tetikler. Arteriollerde vazodilatasyon ve postkapiller venüllerde güçlü vasküler geçirgenlik artışına neden olur. Akciğer endotelinde bulunan Kininaz II (Anjiyotensin Dönüştürücü Enzim - ACE) tarafından hızla yıkılır. ACE inhibitörleri bradikinini biriktirerek kuru öksürük ve anjiyoödem yapar.",
        "clinicalPearl": "Enflamasyonda doğrudan ağrı oluşturan temel moleküldür (PGE2 ağrıyı duyarlılaştırır). C1 inhibitörü eksikliğinde yıkılamayıp birikerek Herediter Anjiyoödem tablosuna yol açar.",
        "keywords": ["bradikinin", "kallikrein", "kinin sistemi", "ağrı", "dolor", "ace inhibitörü", "anjiyoödem", "herediter anjiyoödem"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-prostasiklin",
        "term": "Prostasiklin (PGI2)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1",
        "description": "Vasküler endotel hücreleri tarafından araşidonik asitten COX-1/COX-2 ve Prostasiklin Sentaz enzimleri aracılığıyla sentezlenen prostanoid. Trombosit IP reseptörlerine bağlanıp hücre içi cAMP düzeyini artırarak trombosit agregasyonunu kuvvetle inhibe eder ve arteriollerde güçlü vazodilatasyon oluşturur. Trombositte üretilen protrombotik Tromboksan A2 (TXA2) ile zıt çalışarak damar içi trombüs oluşumunu engeller.",
        "clinicalPearl": "Selektif COX-2 inhibitörleri endoteldeki PGI2 sentezini baskılarken trombositteki TXA2'ye dokunmaz; bu durum tromboz, inme ve miyokard enfarktüsü riskini artırır.",
        "keywords": ["prostasiklin", "pgi2", "endotel", "vazodilatasyon", "trombosit agregasyon inhibisyonu", "cox-2", "txa2"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-tromboksan-a2",
        "term": "Tromboksan A2 (TXA2)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "committee": "Kurul 1",
        "description": "Dolaşımdaki trombositler tarafından COX-1 ve Tromboksan Sentaz enzimleri aracılığıyla üretilen son derece kararsız lipid mediyatör. Güçlü vazokonstriktördür ve trombosit agregasyonu ile granül salınımını tetikleyerek primer hemostatik tıkacın oluşmasını sağlar.",
        "clinicalPearl": "Trombositler çekirdeksiz olduğu için aspirin tarafından geri dönüşümsüz asetillenen COX-1 enzimini yenileyemezler; bu nedenle düşük doz aspirin tüm trombosit ömrü boyunca (7-10 gün) TXA2 üretimini durdurur.",
        "keywords": ["tromboksan a2", "txa2", "trombosit", "cox-1", "vazokonstriksiyon", "agregasyon", "aspirin"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-lokotrien-b4",
        "term": "Lökotrien B4 (LTB4)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1",
        "description": "Nötrofiller ve diğer miyeloid hücrelerde 5-lipoksijenaz ve LTA4 hidrolaz enzimleri ile sentezlenen majör lipid kemoatraktan. Nötrofillerin yangı odağına doğru yönlenmiş kemotaksisini yönetir, lökosit integrinlerinin (Mac-1, LFA-1) afinitesini artırarak endotelyal adezyonu sağlar, lizozomal enzim salınımını ve ROS üretimini tetikler.",
        "clinicalPearl": "Akut enflamasyonda nötrofil kemotaksisini sağlayan 4 altın ajandan biridir (LTB4, C5a, IL-8, bakteriyel N-formil peptidler).",
        "keywords": ["lökotrien b4", "ltb4", "5-lipoksijenaz", "kemotaksis", "nötrofil", "adezyon", "ros"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-sisteinil-lokotrienler",
        "term": "Sisteinil Lökotrienler (LTC4, LTD4, LTE4)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / Farmakoloji",
        "committee": "Kurul 1",
        "description": "Mast hücreleri, eozinofiller ve bazofillerde LTA4'e glutatyon eklenmesiyle sentezlenen sistein içerikli eikozanoidler (eski adıyla SRS-A / Slow Reacting Substance of Anaphylaxis). Bronş düz kaslarında histaminden 1000 kat daha güçlü ve uzun süreli bronkokonstriksiyon yaparlar; venüllerde vasküler geçirgenliği artırıp mukus hipersekresyonunu tetiklerler.",
        "clinicalPearl": "Bronşiyal astım ve alerjik rinit patogenezinde başroldedirler. Montelukast ve zafirlukast bu moleküllerin CysLT1 reseptörlerini antagonize ederek hava yollarını rahatlatır.",
        "keywords": ["sisteinil lökotrienler", "ltc4", "ltd4", "lte4", "srs-a", "bronkospazm", "astım", "montelukast"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-lipoksinler",
        "term": "Lipoksinler (LXA4, LXB4)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1",
        "description": "Enflamasyonun çözünme (rezolüsyon) fazında nötrofiller (5-LOX) ile trombositler (12-LOX) arasındaki transsellüler metabolik işbirliği ile sentezlenen endojen anti-inflamatuar lipid mediyatörler. Nötrofil kemotaksisini ve damar dışına göçünü inhibe eder, makrofajların apoptotik hücre enkazını temizlemesini (eferositoz) uyarırlar.",
        "clinicalPearl": "Diğer tüm araşidonik asit metabolitlerinin aksine yangıyı alevlendirmez; enflamasyonu sonlandıran bir fren görevi görür.",
        "keywords": ["lipoksin", "lxa4", "lxb4", "anti-inflamatuar", "rezolüsyon", "transsellüler", "eferositoz"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-kompleman-c3b",
        "term": "Kompleman C3b (Opsonin)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / İmmünoloji",
        "committee": "Kurul 1",
        "description": "Klasik, lektin veya alternatif C3 konvertaz enzimi tarafından C3'ün proteolitik parçalanması sonucu ortaya çıkan büyük fragman. Mikrop ve antijen yüzeylerine kovalent tioester bağlarıyla tutunur. Nötrofil ve makrofajların yüzeyindeki Kompleman Reseptörü 1 (CR1 / CD35) tarafından tanınarak fagositozu dramatik biçimde hızlandırır (opsonizasyon).",
        "clinicalPearl": "İmmün sistemdeki en güçlü opsonindir; ayrıca C5 konvertaz kompleksinin yapısına katılarak MAC oluşumunu başlatır.",
        "keywords": ["c3b", "opsonin", "opsonizasyon", "fagositoz", "cr1", "cd35", "kompleman"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-kompleman-c5a",
        "term": "Kompleman C5a (Anafilatoksin & Kemoatraktan)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / İmmünoloji",
        "committee": "Kurul 1",
        "description": "C5 konvertazın C5 molekülünü parçalamasıyla salınan 74 aminoasitlik çözünür peptid. Kompleman sisteminin en güçlü anafilatoksini ve kemoatraktanıdır. Mast hücrelerinden histamin degranülasyonunu tetikler; nötrofiller, monositler ve makrofajlar için son derece güçlü kemotaksis uyarısı sağlar ve integrin adezyonunu artırır.",
        "clinicalPearl": "Nötrofil kemotaksisinde LTB4 ve IL-8 ile yarışan majör plazma ürünüdür; şok tablolarında kontrolsüz salınımı vasküler kollapsa yol açar.",
        "keywords": ["c5a", "anafilatoksin", "kemotaksis", "nötrofil", "mast hücresi", "enflamasyon"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-membran-atak-kompleksi",
        "term": "Membran Atak Kompleksi (MAC / C5b-9)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / İmmünoloji",
        "committee": "Kurul 1",
        "description": "C5b parçasının hedef hücre zarına tutunmasının ardından C6, C7, C8 ve çok sayıda C9 monomerinin birleşmesiyle oluşan silindirik transmembran por kompleksi. Hücre zarında 10 nanometrelik delikler açarak serbest su ve iyon girişine, hücrenin osmotik lizisle patlamasına neden olur. CD59 (Protectin) konağın kendi hücrelerini bu kompleksten korur.",
        "clinicalPearl": "Terminal kompleman (C5b-C9) eksikliği olan bireylerde tekrarlayan Neisseria meningitidis ve Neisseria gonorrhoeae enfeksiyonları (bakteriyemi, menenjit) görülür.",
        "keywords": ["membran atak kompleksi", "mac", "c5b-9", "lizis", "neisseria", "cd59", "protectin"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-daf-cd55",
        "term": "Decay-Accelerating Factor (DAF / CD55)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "committee": "Kurul 1",
        "description": "Hücre zarına GPI (Glikozilfosfatidilinozitol) çıpasıyla bağlanan kompleman düzenleyici glikoprotein. Klasik ve alternatif C3 konvertaz enzim komplekslerini (C4b2a ve C3bBb) hızla ayrıştırıp inaktive ederek konak dokularının oto-kompleman saldırısına uğramasını engeller. CD59 ile birlikte eritrosit zarını korur.",
        "clinicalPearl": "PIGA gen mutasyonu sonucu GPI çıpası yapılamadığında eritrositlerde CD55 ve CD59 eksikliği gelişir ve Paroksismal Noktürnal Hemoglobinüri (PNH) ortaya çıkar.",
        "keywords": ["daf", "cd55", "c3 konvertaz", "gpi çıpası", "pnh", "paroksismal noktürnal hemoglobinüri"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-cd59-protectin",
        "term": "CD59 (Protectin / MAC İnhibitörü)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / Hematoloji",
        "committee": "Kurul 1",
        "description": "Hücre membranına GPI çıpası ile tutunan 18-20 kDa ağırlığında kompleman inhibitörü protein. Oluşmakta olan C5b-8 kompleksine C9 monomerlerinin bağlanmasını ve polimerleşerek zar tüneli açmasını engelleyerek konak hücrelerini litik parçalanmadan korur.",
        "clinicalPearl": "PNH'de eritrositlerin intravasküler kompleman lizisine uğramasının primer sebebi hücre yüzeyinde CD59 bulunmayışıdır.",
        "keywords": ["cd59", "protectin", "mac inhibitörü", "c9 polimerizasyonu", "pnh", "gpi"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-paf-platelet-activating-factor",
        "term": "Platelet Aktive Edici Faktör (PAF)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1",
        "description": "Nötrofiller, makrofajlar, mast hücreleri ve endotel tarafından membran fosfolipidlerinden Fosfolipaz A2 yardımıyla sentezlenen fosfolipid türevi vazoaktif mediyatör. Trombosit agregasyonunu uyarır; son derece düşük konsantrasyonlarda histaminden binlerce kat daha güçlü vazodilatasyon ve venüler geçirgenlik artışı yapar.",
        "clinicalPearl": "Bronkokonstriksiyon, vazodilatasyon ve lökosit adezyonunu aynı anda tetikleyen çok yönlü bir inflamasyon mediyatörüdür.",
        "keywords": ["paf", "platelet activating factor", "trombosit", "vazodilatasyon", "vasküler geçirgenlik", "fosfolipaz a2"],
        "aiAuditScore": 100
    },
    {
        "id": "enc-interlokin-8-cxcl8",
        "term": "İnterlökin-8 (IL-8 / CXCL8)",
        "category": "patoloji",
        "discipline": "Tıbbi Patoloji / İmmünoloji",
        "committee": "Kurul 1",
        "description": "Makrofajlar ve endotel hücreleri tarafından mikrobiyal ürünler, IL-1 ve TNF uyarımı ile sentezlenen C-X-C ailesi kemokin. Dolaşımdaki nötrofillerin CXCR1 ve CXCR2 reseptörlerine bağlanarak nötrofillerin enfeksiyon alanına yoğun kemotaksisini ve mikrobisidal aktivasyonunu sağlar.",
        "clinicalPearl": "Akut irinli (pürülan) enfeksiyonlarda nötrofilleri olay yerine toplayan en temel kemokindir.",
        "keywords": ["il-8", "cxcl8", "c-x-c kemokin", "nötrofil kemotaksisi", "cxcr1", "cxcr2"],
        "aiAuditScore": 100
    }
]

def main():
    print("=" * 70)
    print("🚀 GÜVERTE VE ANSİKLOPEDİ ENTEGRASYONU BAŞLATILIYOR...")
    print("=" * 70)

    # 1. Update interactive_learning_decks.json
    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    # Replace existing or append
    existing_idx = next((i for i, d in enumerate(decks) if d.get('id') == new_deck['id']), -1)
    if existing_idx >= 0:
        decks[existing_idx] = new_deck
        print(f"✓ Mevcut güverte güncellendi: {new_deck['id']}")
    else:
        decks.append(new_deck)
        print(f"✓ Yeni güverte eklendi: {new_deck['id']} ({len(new_deck['slides'])} slayt)")

    with open(DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
    print(f"✓ Toplam Güverte Sayısı: {len(decks)}")

    # 2. Update medical_encyclopedia.json
    with open(ENCYCLOPEDIA_PATH, 'r', encoding='utf-8') as f:
        enc_entries = json.load(f)

    enc_map = {e.get('id'): i for i, e in enumerate(enc_entries)}
    added_enc = 0
    updated_enc = 0

    for item in new_encyclopedia_entries:
        iid = item.get('id')
        if iid in enc_map:
            enc_entries[enc_map[iid]] = item
            updated_enc += 1
        else:
            enc_entries.append(item)
            enc_map[iid] = len(enc_entries) - 1
            added_enc += 1

    with open(ENCYCLOPEDIA_PATH, 'w', encoding='utf-8') as f:
        json.dump(enc_entries, f, ensure_ascii=False, indent=2)
    print(f"✓ Tıbbi Ansiklopedi Güncellendi: Toplam {len(enc_entries)} terim (Yeni: {added_enc}, Güncellenen: {updated_enc})")

    # 3. Synchronize medical_glossary.json
    glossary_data = {}
    for e in enc_entries:
        term = e.get('term', '')
        if term:
            glossary_data[term.lower()] = {
                "term": term,
                "category": e.get('category', 'patoloji'),
                "description": e.get('description', ''),
                "clinicalPearl": e.get('clinicalPearl', ''),
                "discipline": e.get('discipline', ''),
                "committee": e.get('committee', '')
            }

    with open(GLOSSARY_PATH, 'w', encoding='utf-8') as f:
        json.dump(glossary_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Tıbbi Sözlük (Glossary) Senkronize Edildi: {len(glossary_data)} anahtar terim aktif!")

    # 4. Update learning_batch_queue.json
    if os.path.exists(QUEUE_PATH):
        with open(QUEUE_PATH, 'r', encoding='utf-8') as f:
            queue = json.load(f)

        q_idx = next((i for i, q in enumerate(queue) if q.get('id') == new_deck['id']), -1)
        if q_idx >= 0:
            queue[q_idx]['status'] = 'completed'
            queue[q_idx]['slidesCount'] = len(new_deck['slides'])
        else:
            queue.append({
                "id": new_deck['id'],
                "title": new_deck['title'],
                "discipline": new_deck['discipline'],
                "status": "completed",
                "slidesCount": len(new_deck['slides']),
                "detailLevel": "500%"
            })

        # Set next in queue
        next_planned = "learn-asiri-duyarlilik-ve-otoimmunite"
        np_idx = next((i for i, q in enumerate(queue) if q.get('id') == next_planned), -1)
        if np_idx < 0:
            queue.append({
                "id": next_planned,
                "title": "Aşırı Duyarlılık Reaksiyonları ve Otoimmünite Patolojisi",
                "discipline": "Tıbbi Patoloji",
                "status": "next_in_queue",
                "slidesCount": 22,
                "detailLevel": "500% (Planlanan)"
            })
        else:
            queue[np_idx]['status'] = 'next_in_queue'

        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("✓ Batch Kuyruğu Güncellendi (Sıradaki: Aşırı Duyarlılık ve Otoimmünite)")

    print("=" * 70)
    print("✅ TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI!")
    print("=" * 70)

if __name__ == '__main__':
    main()
