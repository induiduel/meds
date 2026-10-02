#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_infection_isolation_deck.py
Generates the comprehensive %500 detail 20-slide learning deck for:
"Hastane Enfeksiyonları ve İzolasyon Önlemleri" (Enfeksiyon Hastalıkları & Klinik Mikrobiyoloji - Dr. Rüveyda Korkmazer & Dr. Merve Kaçar)
Incorporating 20 slides, 40 3D flashcards, 5 comparison tables, and matched Kurul 1 exam questions (d3-k1-enf-003, d3-k1-enf-004, d3-k1-enf-006, d3-k1-enf-009, d3-k1-enf-010, d3-k1-enf-011, d3-k1-enf-012, d3-k1-enf-013, d3-k1-enf-014).
"""

import json
import os
import sys

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

def find_matched_questions(target_ids=None, keywords=None, max_count=2):
    matched = []
    seen_ids = set()

    if target_ids:
        for tid in target_ids:
            for q in ALL_QUESTIONS:
                if q.get('id') == tid and tid not in seen_ids:
                    seen_ids.add(tid)
                    opts = []
                    for o in q.get('options', []):
                        opts.append({
                            'key': o.get('key', ''),
                            'text': o.get('text', ''),
                            'isCorrect': o.get('key') == q.get('correctAnswer')
                        })
                    matched.append({
                        'id': tid,
                        'examYear': q.get('examYear', 'Kurul 1 Çıkmış'),
                        'question': q.get('stem'),
                        'options': opts,
                        'correctAnswer': q.get('correctAnswer', 'A'),
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Enfeksiyon Hastalıkları müfredatında izolasyon önlemleri ile doğrudan ilişkilidir.'
                    })
                    break

    if len(matched) < max_count and keywords:
        for q in ALL_QUESTIONS:
            text = (str(q.get('stem', '')) + ' ' + str(q.get('explanation', ''))).lower()
            if any(kw.lower() in text for kw in keywords):
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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Enfeksiyon Hastalıkları müfredatında izolasyon önlemleri ile doğrudan ilişkilidir.'
                    })
                    if len(matched) >= max_count:
                        break

    return matched

SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Enfeksiyon Hastalıklarına Giriş ve Temel İlkeler",
        "subtitle": "Enfeksiyon vs Enfeksiyon Hastalığı ayrımı, asemptomatik kolonizasyon ve üçlü belirteç",
        "badge": "Giriş & Temel Kavramlar",
        "badgeColor": "sky",
        "target_ids": [],
        "keywords": ["enfeksiyon", "enfeksiyon hastalığı", "asemptomatik", "mikroorganizma"],
        "lead": "Enfeksiyon; bir mikroorganizmanın duyarlı konağa girmesi, yerleşmesi ve/veya çoğalmasıdır; ancak her enfeksiyon klinik belirti vererek bir enfeksiyon hastalığına dönüşmek zorunda değildir.",
        "spotPearls": [
            "ENFEKSİYON VS HASTALIK: Enfeksiyon mikrobiyal kolonizasyon ve çoğalmayı ifade ederken; doku hasarı, semptom ve fizik muayene bulguları geliştiğinde 'Enfeksiyon Hastalığı' adını alır.",
            "ASEMPTOMATİK SEYİR: Pek çok enfeksiyon subklinik (belirtisiz) seyreder; bu bireyler asemptomatik taşıyıcı olarak etkeni topluma yayabilirler.",
            "ENFEKSİYONUN 3 BELİRLEYİCİSİ: 1) Mikroorganizmanın virülansı, 2) Vücuda giren mikroorganizma miktarı (enfeksiyon dozu / inokülum), 3) Konağın duyarlılığı ve immün durumu."
        ],
        "keyBullets": [
            {"title": "Doku İnvazyonu Eşiği", "desc": "Bakteri epitel yüzeyinde sınırlı kaldığında sadece kolonizasyon iken, bazal membranı aşıp dokuya girdiğinde enfeksiyon başlar."},
            {"title": "Genel Klinik Belirtiler", "desc": "Ateş, üşüme-titreme, taşikardi, halsizlik, lökositoz ve akut faz reaktifi (CRP, prokalsitonin) artışı sistemik yanıtın göstergeleridir."},
            {"title": "Taşıyıcılık Riski", "desc": "Asemptomatik taşıyıcılar (örneğin Salmonella Typhi safra kesesi taşıyıcılığı) salgınların sinsi kaynaklarıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-1",
                "question": "Enfeksiyon ile Enfeksiyon Hastalığı arasındaki temel kavramsal fark nedir?",
                "answer": "Enfeksiyon mikroorganizmanın konakta çoğalmasıdır (asemptomatik olabilir); Enfeksiyon Hastalığı ise doku hasarı ve klinik belirti-bulguların ortaya çıkması durumudur.",
                "hint": "Enfeksiyon = çoğalma; Hastalık = klinik belirti/hasar."
            },
            {
                "id": "fc-iz-2",
                "question": "Bir mikrobiyal temasın klinik enfeksiyon hastalığına dönüşüp dönüşmeyeceğini belirleyen 3 temel faktör nedir?",
                "answer": "1) Mikroorganizmanın virülansı, 2) Vücuda giren mikrop miktarı (enfeksiyon dozu), 3) Konağın immün duyarlılığı.",
                "hint": "Virülans, doz ve konak bağışıklığı."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Patojenite ve Virülans Kavramlarının Kesin Ayrımı",
        "subtitle": "Kalitatif hastalık yapma yeteneği (Patojenite) vs Kantitatif hastalık şiddeti (Virülans)",
        "badge": "Patojenite & Virülans",
        "badgeColor": "indigo",
        "target_ids": ["d3-k1-enf-003"],
        "keywords": ["virülans", "patojenite", "hastalık oluşturma yeteneği", "virülans derecesi"],
        "lead": "Tıbbi mikrobiyoloji ve enfeksiyon disiplininde sınavların en vazgeçilmez soru kalıbı patojenite (nitelik) ile virülans (nicelik/derece) arasındaki kesin tanımsal ayrımdır.",
        "spotPearls": [
            "PATOJENİTE: Bir mikroorganizmanın konakta hastalık oluşturabilme YETENEĞİ veya KAPASİTESİDİR (kalitatif/niteliksel bir özelliktir: patojen ya da non-patojen).",
            "VİRÜLANS (SINAV SPOTU): Bir mikroorganizmanın patojenitesinin DERECESİNİ, yani oluşturduğu hastalığın ŞİDDET VEYA AĞIRLIĞINI ifade eder (Kurul 1 Çıkmış Soru!).",
            "AYNI TÜRÜN FARKLI SUŞLARI: Aynı bakteri türünün farklı suşları farklı virülans genlerine sahip olabilir (örneğin kommensal E. coli ile enterohemorajik E. coli O157:H7).",
            "VİRÜLANS FAKTÖRLERİ: Kapsül (fagositozdan kaçış), Adezinler ve pili (tutunma), Biyofilm (antibiyotikten korunma), Ekzotoksinler ve Endotoksin (LPS)."
        ],
        "keyBullets": [
            {"title": "Letal Doz (LD50)", "desc": "Virülans deneysel olarak deney hayvanlarının %50'sini öldüren mikroorganizma sayısı (LD50) ile ölçülür; LD50 ne kadar düşükse virülans o kadar yüksektir."},
            {"title": "Kapsülün Rolü", "desc": "Pnömokoklarda kapsüllü suşlar ölümcül menenjit yaparken kapsülsüz suşlar fagositozla anında yok edilir."},
            {"title": "Biyofilm Direnci", "desc": "Kateter ve protez yüzeylerinde biyofilm oluşturan bakteriler antibiyotik konsantrasyonlarına 1000 kat daha dirençli hale gelir."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-3",
                "question": "Enfeksiyon etkeninin duyarlı bir konakta 'hastalık oluşturma yeteneğinin derecesine veya oluşturduğu hastalığın şiddetine' ne ad verilir?",
                "answer": "Virülans adı verilir (Kurul 1 Çıkmış Soru).",
                "hint": "Virülans."
            },
            {
                "id": "fc-iz-4",
                "question": "Patojenite ile virülans arasındaki felsefi ve tanımsal fark nedir?",
                "answer": "Patojenite mikroorganizmanın hastalık yapabilme potansiyelidir (var/yok, kalitatif); Virülans ise bu potansiyelin derecesi ve hastalığın ağırlığıdır (kantitatif).",
                "hint": "Patojenite = Yetenek; Virülans = Derece/Şiddet."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Mikroorganizma Sınıflandırması: Prionlardan Parazitlere Biyolojik Spektrum",
        "subtitle": "Aselüler ajanlar, Prionların nükleik asitsiz yapısı, direnç profili ve spongiform ensefalopatiler",
        "badge": "Mikrobiyal Spektrum",
        "badgeColor": "purple",
        "target_ids": [],
        "keywords": ["prion", "aselüler", "nükleik asit", "creutzfeldt jakob", "otoklav direnci"],
        "lead": "Enfeksiyon etkenleri aselüler partiküllerden çok hücreli ökaryotlara kadar geniş bir yelpazeyi kapsar; bu spektrumun en sıradışı üyesi nükleik asit içermeyen enfeksiyöz proteinler olan Prionlardır.",
        "spotPearls": [
            "PRİONLARIN TEMEL ÖZELLİKLERİ: NÜKLEİK ASİT (DNA veya RNA) İÇERMEZLER; tamamen anormal katlanmış hidrofobik protein yapısındadırlar (PrPSc).",
            "MİKROSKOBİK BOYUT: En küçük virüslerden dahi EN AZ 100 KAT DAHA KÜÇÜKTÜRLER.",
            "İN AKTİVASYONA AŞIRI DİRENÇ: Standart otoklavlama, UV ışınları, formol ve bilinen kimyasal dezenfektanlara olağanüstü dirençlidirler; cerrahi alet sterilizasyonunda özel kostik soda ve yüksek basınçlı buhar protokolleri gerektirirler.",
            "KLİNİK TABLOLAR: Yıllarca süren uzun inkübasyon periyodu sonrası santral sinir sisteminde süngersi (spongiform) vakuolizasyon ve fatal nörodejenerasyon yaparlar: Creutzfeldt-Jakob Hastalığı (CJD), Kuru, Ölümcül Ailevi Uykusuzluk (FFI) ve Deli Dana (BSE)."
        ],
        "keyBullets": [
            {"title": "Replikasyon Mekanizması", "desc": "Hücresel normal PrPC proteinlerini temas yoluyla anormal beta-tabakalı PrPSc formuna dönüştürerek çoğalırlar."},
            {"title": "İmmün Yanıt Yokluğu", "desc": "Konağın kendi proteininin izoformu olduklarından vücutta enflamatuar yanıt veya antikor oluşmaz."},
            {"title": "İyatrojenik Bulaş", "desc": "Kontamine beyin cerrahisi aletleri, kornea nakli veya kadavra kaynaklı büyüme hormonu kullanımıyla insandan insana geçebilir."}
        ],
        "table": {
            "title": "Enfeksiyon Etkenlerinin Biyolojik Spektrumu ve Ayırt Edici Özellikleri",
            "headers": ["Grup", "Hücresel Yapı", "Genetik Materyal", "Hücre Duvarı / Zarf", "Önemli Klinik Örnekler"],
            "rows": [
                ["Prionlar", "Aselüler (Protein partikülü)", "YOK (Ne DNA ne RNA)", "Yok (Saf anormal protein)", "Creutzfeldt-Jakob, Kuru, Deli Dana"],
                ["Virüsler", "Aselüler (Nükleokapsid)", "DNA VEYA RNA (Biri)", "Kapsid var, bazısında lipid zarf", "İnfluenza, HIV, Hepatit B/C, Kuduz"],
                ["Bakteriler", "Prokaryot tek hücreli", "DNA VE RNA (İkisi de var)", "Peptidoglikan duvar (Mikoplazma hariç)", "S. aureus, E. coli, M. tuberculosis"],
                ["Mantarlar", "Ökaryot (Maya / Küf)", "DNA ve RNA", "Kitin ve beta-glukan duvar", "Candida albicans, Aspergillus fumigatus"],
                ["Protozoonlar", "Ökaryot tek hücreli", "DNA ve RNA", "Hücre duvarı yok, esnek membran", "Plasmodium (Sıtma), Entamoeba, Giardia"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-iz-5",
                "question": "Prionların yapısında hangi genetik materyal bulunur ve fiziksel/kimyasal dezenfeksiyona dirençleri nasıldır?",
                "answer": "Hiçbir nükleik asit (DNA veya RNA) İÇERMEZLER, saf proteindirler; standart fiziksel ve kimyasal inaktivasyon yöntemlerine aşırı derecede dirençlidirler.",
                "hint": "Nükleik asit içermez, aşırı dirençlidir."
            },
            {
                "id": "fc-iz-6",
                "question": "İnsanlarda prionların yol açtığı süngersi ensefalopati hastalıklarına 3 örnek veriniz.",
                "answer": "1) Creutzfeldt-Jakob Hastalığı (CJD), 2) Kuru, 3) Ölümcül Ailevi Uykusuzluk (Fatal Familial Insomnia - FFI).",
                "hint": "Creutzfeldt-Jakob, Kuru, FFI."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Atipik Bakteriyel Ajanlar: Mikoplazma, Klamidya ve Riketsiyalar",
        "subtitle": "Hücre duvarsız bakteriler, enerji parazitleri, zorunlu hücre içi yaşam ve eskar oluşumu",
        "badge": "Atipik Bakteriler",
        "badgeColor": "teal",
        "target_ids": [],
        "keywords": ["mikoplazma", "klamidya", "riketsiya", "hücre duvarı yok", "tache noire"],
        "lead": "Klasik bakterilerin dışında kalan atipik prokaryotlar hücresel yapıları, enerji metabolizmaları ve antibiyotik duyarlılıklarıyla klinik tıpta özel bir yere sahiptir.",
        "spotPearls": [
            "MİKOPLAZMALAR (HÜCRE DUVARI YOKTUR): Peptidoglikan hücre duvarları kesinlikle bulunmaz; bu nedenle Gram boyası ile BOYANMAZLAR ve hücre duvarını hedef alan BETA-LAKTAM (penisilin, sefalosporin) ANTİBİYOTİKLERE DOĞAL DİRENÇLİDİRLER! Hücre zarlarında kolesterol içerirler, yapay besiyerinde üreyebilirler (Mycoplasma pneumoniae).",
            "KLAMİDYALAR (ENERJİ PARAZİTİ): Kendi ATP'sini sentezleyemez; konağın ATP'sine muhtaç ZORUNLU HÜCRE İÇİ bakterilerdir. Peptidoglikan tabakaları yoktur (Chlamydia trachomatis, C. pneumoniae).",
            "RİKETSİYALAR (ARTROPOD VEKTÖRLERİ): Zorunlu hücre içi pleomorfik mikroorganizmalardır; kene, bit ve pirelerle bulaşırlar.",
            "TACHE NOIRE (KARA ESKAR): Rickettsia conorii'nin neden olduğu Akdeniz Benekli Ateşi'nde kenenin ısırdığı yerde karakteristik siyah nekrotik eskar (tache noire) görülür."
        ],
        "keyBullets": [
            {"title": "Beta-Laktam Duyarsızlığı", "desc": "Atipik pnömoni şüphesinde amoksisilin verilmesi etkisizdir; hücre duvarı olmayan mikoplazmaya karşı makrolid veya kinolon seçilmelidir."},
            {"title": "Chlamydia Yaşam Döngüsü", "desc": "Hücre dışında enfeksiyöz 'Elementer Cisimcik' (EB), hücre içinde ise çoğalan 'Retiküler Cisimcik' (RB) formunda bulunur."},
            {"title": "Epidemik Tifüs Vektörü", "desc": "Rickettsia prowazekii insan vücut biti (Pediculus humanus corporis) aracılığıyla savaş ve göç koşullarında ölümcül salgınlar yapar."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-7",
                "question": "Mikoplazmaların hücre yapısındaki en belirgin eksiklik nedir ve bu durum hangi antibiyotik grubuna doğal direnç kazandırır?",
                "answer": "Hücre duvarları (peptidoglikan tabakası) yoktur; bu nedenle hücre duvarı sentezini bozan beta-laktam antibiyotiklere doğal olarak dirençlidirler.",
                "hint": "Hücre duvarı yok, beta-laktamlara dirençli."
            },
            {
                "id": "fc-iz-8",
                "question": "ATP sentezleyemediği için 'enerji paraziti' olarak adlandırılan ve zorunlu hücre içi yaşayan bakteri cinsi hangisidir?",
                "answer": "Chlamydia (Klamidya) cinsidir.",
                "hint": "Chlamydia."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Normal İnsan Mikrobiyotası (Florası) ve Vücudun Steril Bölgeleri",
        "subtitle": "Kommensal flora alanları, kesinlikle flora bulunmayan steril anatomik boşluklar",
        "badge": "Mikrobiyota vs Steril Alan",
        "badgeColor": "amber",
        "target_ids": ["d3-k1-enf-006"],
        "keywords": ["normal flora", "steril bölgeler", "üreter steril", "bos steril", "mikrobiyota"],
        "lead": "İnsan vücudunun dış çevreyle temas eden yüzeyleri trilyonlarca faydalı mikrop barındırırken; iç organlar, dolaşım ve kapalı boşluklar mutlak bir steriliteye sahiptir.",
        "spotPearls": [
            "STERİL BÖLGELER (KESİNLİKLE FLORA BULUNMAZ!): 1) Merkezi Sinir Sistemi ve Beyin Omurilik Sıvısı (BOS), 2) Alt Solunum Yolları (trakea, bronşlar, akciğer parankimi), 3) Dolaşım Sistemi (kan ve lenf), 4) Üst Ürogenital Sistem (Böbrekler, ÜRETER, mesane), 5) Vücut Boşlukları (plevra, periton, perikard, sinovya) (Kurul 1 Çıkmış Soru!).",
            "FLORA BULUNAN BÖLGELER: Deri, ağız boşluğu, burun, boğaz, göz konjonktivası, üst solunum yolları, sindirim kanalı (özellikle kolon), dış genital organlar, dış kulak yolu.",
            "DERİ VE KOLON PROTO TİPLERİ: Deride Staphylococcus epidermidis ve Propionibacterium acnes; kolonda ise Bacteroides fragilis ve Enterobacteriaceae üyeleri dominanttır.",
            "STERİL BÖLGEDE TEK BİR BAKTERİ: İdrarda, kanda veya BOS'ta tek bir bakterinin saptanması kolonizasyon değil doğrudan patolojik bir enfeksiyon kanıtıdır."
        ],
        "keyBullets": [
            {"title": "Mukoza Koruma Bariyeri", "desc": "Flora bakterileri yer işgal ederek ve bakteriyosin üreterek patojen mikropların tutunmasını (kolonizasyon direnci) engeller."},
            {"title": "Üreter ve Mesane Sterilitesi", "desc": "İdrarın tek yönlü akımı, üreterovezikal bileşke valv mekanizması ve ürotelyal mukus üst üriner sistemi steril tutar."},
            {"title": "Alt Solunum Mukosiliyer Yürüyen Merdiveni", "desc": "Mukosiliyer klirens ve alveoler makrofajlar trakea altındaki bronş ağacını bakterilerden arındırır."}
        ],
        "table": {
            "title": "İnsan Vücudunda Normal Mikrobiyota Bulunan ve Kesinlikle Steril Olan Bölgeler Matrisi",
            "headers": ["Anatomik Bölge", "Flora Durumu", "Dominant Mikroorganizmalar", "Klinik / Sınav Önemi"],
            "rows": [
                ["Deri", "Zengin Flora Var", "Staphylococcus epidermidis, Corynebacterium, P. acnes", "Kateter giriş yerinde enfeksiyon kaynağı"],
                ["Ağız ve Farenks", "Zengin Flora Var", "Viridans streptokoklar, anaeroplar", "Diş çekimi sonrası infektif endokardit riski"],
                ["Kalın Bağırsak (Kolon)", "Çok Yoğun Flora Var", "Bacteroides fragilis, E. coli, Enterokoklar", "Vücudun en yoğun mikrobiyal biyokütlesi"],
                ["Merkezi Sinir Sistemi (BOS)", "MUTLAK STERİL", "HİÇBİR MİKROORGANİZMA BULUNMAZ", "Tek bir bakteri üremesi Menenjit tanısıdır"],
                ["Alt Solunum (Bronş / Alveol)", "MUTLAK STERİL", "HİÇBİR FLORA BULUNMAZ", "Mukosiliyer klirens ve makrofajlarla korunur"],
                ["Üst Üriner Sistem (Böbrek, Üreter)", "MUTLAK STERİL", "HİÇBİR FLORA BULUNMAZ", "Üreterde bakteri bulunması Piyelonefrit göstergesidir"],
                ["Dolaşım Sistemi (Kan)", "MUTLAK STERİL", "HİÇBİR MİKROORGANİZMA BULUNMAZ", "Kanda bakteri bulunması Bakteriyemi / Sepsistir"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-iz-9",
                "question": "Aşağıdaki vücut bölgelerinden hangilerinde normal mikrobiyal flora KESİNLİKLE bulunmaz (sterildir)? (BOS, Üreter, Konjonktiva, Kolon)",
                "answer": "BOS ve Üreter kesinlikle steril bölgelerdir, normal flora içermezler; konjonktiva ve kolonda ise zengin flora bulunur (Kurul 1 Çıkmış Soru).",
                "hint": "BOS ve Üreter sterildir."
            },
            {
                "id": "fc-iz-10",
                "question": "Deride en sık bulunan normal kommensal flora bakterisi hangisidir?",
                "answer": "Staphylococcus epidermidis (koagülaz negatif stafilokok).",
                "hint": "Staphylococcus epidermidis."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Kolonizasyon, Disbiyoz ve Fırsatçı (Opportunistik) Enfeksiyonlar",
        "subtitle": "Taşıyıcılık vs invazyon, geniş spektrumlu antibiyotikler, disbiyoz ve C. difficile koliti",
        "badge": "Fırsatçı Enfeksiyonlar",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["kolonizasyon", "disbiyoz", "fırsatçı enfeksiyon", "c difficile", "candida"],
        "lead": "Kolonizasyon bir mikroorganizmanın konakta yerleşip çoğalması ancak doku invazyonu yapmamasıdır; konak savunması bozulduğunda bu kommensaller ölümcül fırsatçı enfeksiyonlara dönüşür.",
        "spotPearls": [
            "KOLONİZASYON ÖRNEĞİ: Sağlıklı bireyin burun mukozasında Staphylococcus aureus bulunması kolonizasyondur; aynı bakteri cerrahi yaraya girip apse yaptığında enfeksiyon adını alır.",
            "FIRSATÇI PATOJEN TANIMI: Normal koşullarda hastalık yapma potansiyeli sınırlı olan; ancak konak immünitesi baskılandığında, floranın anatomik yeri değiştiğinde veya antibiyotikle mikrobiyota bozulduğunda hastalık yapan mikroorganizmalardır.",
            "DİSBİYOZ VE C. DIFFICILE: Geniş spektrumlu antibiyotik kullanımı koruyucu bağırsak florasını yok eder; fırsatçı Clostridioides difficile aşırı çoğalarak Psödomembranöz Kolite yol açar.",
            "YER DEĞİŞTİRME MEKANİZMASI: Kolonun normal üyesi olan E. coli'nin üretraya ve mesaneye geçmesi üriner sistem enfeksiyonunun bir numaralı nedenidir."
        ],
        "keyBullets": [
            {"title": "Pneumocystis jirovecii", "desc": "Hücresel immün yetmezliği (CD4 <200 olan HIV hastaları) fırsat bilerek ölümcül interstisyel pnömoni yapar."},
            {"title": "Kandida İnvazyonu", "desc": "Geniş spektrumlu antibiyotik veya santral venöz kateter kullanımı Candida mayalarının kan dolaşımına geçip kandidemiye yol açmasına neden olur."},
            {"title": "Anatomik Bariyer Kırılması", "desc": "Yanık, cerrahi kesi veya endotrakeal tüp vücudun birincil mekanik kalkanını yıkarak florayı fırsatçı patojene dönüştürür."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-11",
                "question": "Bir mikroorganizmanın doku hasarı ve klinik hastalık oluşturmaksızın vücut yüzeyinde yerleşip çoğalmasına ne ad verilir?",
                "answer": "Kolonizasyon adı verilir.",
                "hint": "Kolonizasyon."
            },
            {
                "id": "fc-iz-12",
                "question": "Geniş spektrumlu antibiyotik kullanımı sonucu bağırsak mikrobiyotasının bozulmasıyla (disbiyoz) ölümcül psödomembranöz kolit tablosuna yol açan klasik fırsatçı patojen hangisidir?",
                "answer": "Clostridioides difficile.",
                "hint": "Clostridioides difficile."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Hastane Enfeksiyonları (Sağlık Hizmetiyle İlişkili Enfeksiyonlar - SHİE)",
        "subtitle": "48-72 saat kuralı, nozokomiyal enfeksiyonlar, dirençli bakteriler ve invaziv cihaz ilişkisi",
        "badge": "Hastane Enfeksiyonları (SHİE)",
        "badgeColor": "red",
        "target_ids": [],
        "keywords": ["hastane enfeksiyonu", "nozokomiyal", "shie", "48 saat kuralı", "kateter ilişkili"],
        "lead": "Sağlık hizmetiyle ilişkili enfeksiyonlar (SHİE / Nozokomiyal enfeksiyonlar); hastaneye yatış anında kuluçka evresinde olmayan, yatıştan belirli bir süre sonra gelişen ve mortaliteyi katlayan tablolardır.",
        "spotPearls": [
            "48-72 SAAT KURALI: Hastaneye yattığı sırada enfeksiyon bulgusu ve inkübasyon dönemi olmayan bir hastada, YATIŞTAN 48-72 SAAT SONRA ortaya çıkan enfeksiyonlar nozokomiyal kabul edilir.",
            "TABURCULUK SONRASI SÜRE: Taburculuktan sonraki ilk 10-30 gün içinde (implant veya protez cerrahisi yapılmışsa 1 yıl içinde) gelişen enfeksiyonlar da hastane enfeksiyonu sayılır.",
            "DÖRT BÜYÜK HASTANE ENFEKSİYONU: 1) Ventilatör İlişkili Pnömoni (VİP), 2) Santral Venöz Kateter İlişkili Kan Dolaşımı Enfeksiyonu (KİKDE), 3) Üriner Kateter İlişkili Enfeksiyon (Kİ-ÜSE), 4) Cerrahi Alan Enfeksiyonu (CAE).",
            "ÇOĞUL DİRENÇLİ PATOJENLER (ESKAPE): Enterococcus faecium (VRE), Staphylococcus aureus (MRSA), Klebsiella pneumoniae, Acinetobacter baumannii, Pseudomonas aeruginosa, Enterobacter spp."
        ],
        "keyBullets": [
            {"title": "Maliyet ve Mortalite", "desc": "Hastane enfeksiyonları yoğun bakım kalış süresini 3 kat uzatır ve sepsis mortalitesini %40'ların üzerine çıkarır."},
            {"title": "Cihaz İhtiyacını Günlük Sorgulama", "desc": "Kateter veya ventilatör ihtiyacı kalmayan hastada cihazın çekilmesi enfeksiyon riskini yarı yarıya azaltır."},
            {"title": "Direnç Genlerinin Aktarımı", "desc": "Hastane ortamındaki yüksek antibiyotik baskısı plazmitler aracılığıyla bakteriler arası direnç gen transferini körükler."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-13",
                "question": "Bir enfeksiyonun 'Hastane Enfeksiyonu' (Sağlık Hizmetiyle İlişkili Enfeksiyon) kabul edilebilmesi için yatıştan en az kaç saat sonra ortaya çıkması gerekir?",
                "answer": "Hastaneye yatıştan en az 48-72 saat sonra ortaya çıkması gerekir.",
                "hint": "48-72 saat kuralı."
            },
            {
                "id": "fc-iz-14",
                "question": "Hastanelerde ve yoğun bakımlarda en sık görülen 4 majör invaziv cihaz/işlem ilişkili enfeksiyon tipi hangileridir?",
                "answer": "1) Ventilatör İlişkili Pnömoni (VİP), 2) Santral Kateter İlişkili Kan Dolaşımı Enfeksiyonu (KİKDE), 3) Kateter İlişkili Üriner Sistem Enfeksiyonu (Kİ-ÜSE), 4) Cerrahi Alan Enfeksiyonu (CAE).",
                "hint": "VİP, KİKDE, Kİ-ÜSE, CAE."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "Enfeksiyon Zinciri ve İzolasyonun Koruyucu Rolü",
        "subtitle": "Kaynak, çıkış kapısı, bulaş yolu, giriş kapısı, duyarlı konak ve zinciri kırma stratejisi",
        "badge": "Enfeksiyon Zinciri",
        "badgeColor": "cyan",
        "target_ids": [],
        "keywords": ["enfeksiyon zinciri", "kaynak", "bulaş yolu", "çıkış kapısı", "duyarlı konak"],
        "lead": "Bir enfeksiyonun yayılabilmesi için altı halkadan oluşan biyolojik bir zincirin kesintisiz tamamlanması gerekir; izolasyon önlemlerinin yegane hedefi bu zinciri en zayıf halkasından kırmaktır.",
        "spotPearls": [
            "ZİNCİRİN HALKALARI: Kaynak (Rezervuar) → Çıkış Kapısı → Bulaş (Taşınma) Yolu → Giriş Kapısı → Duyarlı Konak.",
            "CANLI KAYNAKLAR: Hasta birey, sağlık personeli, hasta yakını, ziyaretçiler ve asemptomatik kolonize taşıyıcılar.",
            "CANSIZ KAYNAKLAR (FOMİTLER): Tıbbi cihazlar (stetoskop, tansiyon aleti), lavabolar, su şebekesi, klima santralleri, hasta yatağı ve komodin yüzeyleri.",
            "İZOLASYONUN VURDUĞU HALKA: İzolasyon tedbirleri enfeksiyon zincirini özellikle 'TAŞINMA YOLU' (bulaş yolu) ve 'GİRİŞ/ÇIKIŞ KAPILARI' düzeyinde bloke ederek duyarlı kişiyi korur."
        ],
        "keyBullets": [
            {"title": "Duyarlı Konak Faktörleri", "desc": "Diyabet, nötropeni, steroid kullanımı, kemoterapi ve yanık hastanın enfeksiyon zincirindeki duyarlılığını dramatik artırır."},
            {"title": "Çıkış Kapısı Yönetimi", "desc": "Öksüren hastaya cerrahi maske takılması çıkış kapısını kapatmanın en pratik örneğidir."},
            {"title": "El Hijyeninin Pozisyonu", "desc": "Sağlık personelinin elleri zincirdeki en kritik 'Taşınma Yolu' halkasıdır; el yıkamak zinciri anında parçalar."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-15",
                "question": "Enfeksiyon zincirini oluşturan ardışık basamaklar nelerdir?",
                "answer": "Kaynak (Rezervuar) → Çıkış Kapısı → Bulaş (Taşınma) Yolu → Giriş Kapısı → Duyarlı Konak.",
                "hint": "Kaynak -> Çıkış -> Bulaş -> Giriş -> Duyarlı Kişi."
            },
            {
                "id": "fc-iz-16",
                "question": "Hastanede uygulanan izolasyon önlemleri enfeksiyon zincirinin öncelikle hangi halkasını kırmayı hedefler?",
                "answer": "Bulaş (Taşınma) Yolu halkasını kırmayı hedefler.",
                "hint": "Bulaş (Taşınma) Yolu."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Bulaş (Taşınma) Şekilleri: Temas, Damlacık ve Solunum (Aerosol) Dinamikleri",
        "subtitle": "Knight ve ark. (1980) partikül boyut analizi, asılı kalma süreleri ve fiziksel ivme",
        "badge": "Bulaş Dinamikleri",
        "badgeColor": "blue",
        "target_ids": ["d3-k1-enf-005", "d3-k1-enf-007"],
        "keywords": ["damlacık boyutu", "aerosol", "knight partikül", "havada asılı kalma"],
        "lead": "Solunum yoluyla atılan patojenlerin davranışı damlacık kütlesi ve aerodinamik kuvvetler (F=m.a) tarafından belirlenir; partikülün boyutu bulaşın damlacık mı yoksa aerosol mü olacağını tayin eder.",
        "spotPearls": [
            "BÜYÜK DAMLACIKLAR (>100 µm): Kütlesi büyüktür; yerçekimi etkisiyle havada süzülemez ve 10 SANİYE İÇİNDE 1 metre mesafe içinde hızla yere düşer (Damlacık bulaşı).",
            "KÜÇÜK DAMLACIKLAR / AEROSOL (<10 µm): Sıvı buharlaşarak 'damlacık çekirdeği' (droplet nuclei) haline gelir; saatlerce havada asılı kalır ve hava akımlarıyla uzak mesafelere taşınır (Solunum/havayolu bulaşı).",
            "KNIGHT VE ARK. (1980) PARTİKÜL DÜŞME SÜRELERİ: 100 µm → 10 saniye; 20 µm → 4 dakika; 10 µm → 17 dakika; 1-3 µm partiküller ise UZUN SÜRE (saatlerce) HAVADA ASILI KALIR!",
            "EN FAZLA PARTİKÜL SAÇAN EYLEM: HAPŞIRMA (milyonlarca damlacık saçar; öksürme ve konuşmadan çok daha fazladır - Kurul 1 Çıkmış Soru!).",
            "ÇEVRESEL DAYANIKLILIK: M. tuberculosis ve mantar sporları kuruluğa ve çevreye çok dayanıklıyken; zarflı virüsler UV ve kuruluğa çok duyarlıdır."
        ],
        "keyBullets": [
            {"title": "Damlacık İvmesi", "desc": "Öksürme saatte 80 km, hapşırma ise saatte 160 km hızla damlacık püskürterek mukozalara çarpar."},
            {"title": "İndirek Temas Fomitleri", "desc": "Hastanın salgılarıyla kirlenmiş stetoskop veya yatak kenarlıkları indirek temas bulaşının ana kaynağıdır."},
            {"title": "Aerosol Üreten İşlemler", "desc": "Entübasyon, bronkoskopi, aspirasyon ve nebülizatör kullanımı damlacıkları parçalayarak yapay aerosol oluşturur."}
        ],
        "table": {
            "title": "Partikül Boyutuna Göre Solunum Sekresyonlarının Havadaki Davranışı (Knight vd. 1980)",
            "headers": ["Partikül Çapı", "Fiziksel Durum", "Havada Kalma / Düşme Süresi", "İzolasyon Tipi & Korunma"],
            "rows": [
                ["> 100 µm", "Ağır kaba damlacık", "10 saniyede 1 metre içinde yere düşer", "Damlacık İzolasyonu (Cerrahi maske)"],
                ["20 µm", "Orta boy damlacık", "Yaklaşık 4 dakikada çöker", "Damlacık İzolasyonu"],
                ["10 µm", "Geçiş boyutu damlacık", "Yaklaşık 17 dakikada çöker", "Damlacık / Solunum"],
                ["1 - 3 µm", "Aerosol / Damlacık çekirdeği", "SAATLERCE HAVADA ASILI KALIR", "Solunum İzolasyonu (Negatif basınç, N95)"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-iz-17",
                "question": "Knight ve ark. (1980) verilerine göre 1-3 µm boyutundaki küçük aerosol partiküllerinin havadaki davranışı nasıldır?",
                "answer": "Yerçekimiyle hemen düşmezler; hava akımlarıyla saatlerce havada asılı kalırlar.",
                "hint": "Saatlerce havada asılı kalır."
            },
            {
                "id": "fc-iz-18",
                "question": "Konuşma, nefes alma, öksürme ve hapşırma eylemleri arasında en fazla sayıda solunum partikülü saçılımına yol açan eylem hangisidir?",
                "answer": "Hapşırmadır (milyonlarca partikül saçar - Kurul 1 Çıkmış Soru).",
                "hint": "Hapşırma."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "İzolasyon Önlemlerinin 2 Kademeli Mimarisi",
        "subtitle": "1. Kademe: Standart (Evrensel) Önlemler; 2. Kademe: Bulaş Yoluna Yönelik Önlemler",
        "badge": "İzolasyon Mimarisi",
        "badgeColor": "teal",
        "target_ids": ["d3-k1-enf-009"],
        "keywords": ["izolasyon mimarisi", "standart önlemler", "bulaş yoluna yönelik", "evrensel önlemler"],
        "lead": "Modern enfeksiyon kontrol sisteminde izolasyon iki aşamalı bir güvenlik piramididir; ilk basamak tüm hastaları kapsarken, ikinci basamak spesifik bulaş yollarına kilitlenir.",
        "spotPearls": [
            "1. KADEME - STANDART (EVRENSEL) ÖNLEMLER: Tanısına veya enfeksiyon durumuna bakılmaksızın HASTANEDEKİ TÜM HASTALARA istisnasız uygulanır (Yalnızca HIV pozitiflere uygulanır iddiası KESİNLİKLE YANLIŞTIR! - Kurul 1 Çıkmış Soru!).",
            "2. KADEME - BULAŞ YOLUNA YÖNELİK ÖNLEMLER: Standart önlemlerin tek başına yetersiz kaldığı, bilinen veya şüphelenilen spesifik patojen varlığında standart önlemlere EK OLARAK uygulanır.",
            "ÜÇ BULAŞ YOLU İZOLASYONU: 1) Temas İzolasyonu, 2) Damlacık İzolasyonu, 3) Solunum (Hava Yolu) İzolasyonu.",
            "KOMBİNASYON ZORUNLULUĞU: Bulaş yoluna yönelik önlemler standart önlemlerin yerine geçmez; daima standart önlemlerle BİRLİKTE yürütülür."
        ],
        "keyBullets": [
            {"title": "Evrensel Kan Kabulü", "desc": "Standart önlemlere göre her hastanın kanı ve vücut sıvısı potansiyel olarak Hepatit B, C ve HIV taşıyor kabul edilir."},
            {"title": "Gereksiz İzolasyon Maliyeti", "desc": "Endikasyonu olmayan hastaya solunum izolasyonu uygulamak negatif basınçlı oda israfına yol açar."},
            {"title": "Dinamik Kaldırma", "desc": "Etken eradike edildiğinde veya arka arkaya negatif kontrol kültürleri alındığında bulaş önlemleri sonlandırılır."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-19",
                "question": "Standart (evrensel) izolasyon önlemleri hastanede hangi hasta grubuna uygulanır?",
                "answer": "Tanısına veya enfeksiyon taşıyıp taşımadığına bakılmaksızın hastaneye başvuran TÜM HASTALARA istisnasız uygulanır.",
                "hint": "Tüm hastalara uygulanır."
            },
            {
                "id": "fc-iz-20",
                "question": "Bulaş yoluna yönelik izolasyon önlemleri hangi 3 kategoriye ayrılır?",
                "answer": "1) Temas İzolasyonu, 2) Damlacık İzolasyonu, 3) Solunum (Hava Yolu) İzolasyonu.",
                "hint": "Temas, Damlacık, Solunum."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "Standart Önlemler ve El Hijyeni İlkeleri",
        "subtitle": "Enfeksiyon kontrolünün temeli, el yıkama endikasyonları, su-sabun vs alkol antiseptiği",
        "badge": "Standart: El Hijyeni",
        "badgeColor": "emerald",
        "target_ids": ["d3-k1-enf-013"],
        "keywords": ["el hijyeni", "su ve sabun", "alkol bazlı el antiseptiği", "eldiven kullanımı"],
        "lead": "Nozokomiyal enfeksiyonların yayılmasını önlemede dünyada kanıtlanmış en etkili, en ucuz ve en kritik yöntem doğru ve zamanında uygulanan el hijyenidir.",
        "spotPearls": [
            "EN ETKİLİ ÖNLEM: El hijyeni hastane enfeksiyonlarının önlenmesinde tek başına en etkili yöntemdir.",
            "SU VE SABUN ŞARTI (GÖZLE GÖRÜLÜR KİRLENME): Ellerde gözle görülür kan, vücut sıvısı kirlenmesi varsa veya sporlu bakterilerle (Clostridioides difficile) temas edilmişse MUTLAKA SU VE SABUNLA YIKANMALIDIR (alkol sporları öldürmez!).",
            "ALKOL BAZLI EL ANTİSEPTİĞİ: Gözle görülür kirlenme yoksa rutin hasta temasları öncesi ve sonrasında tercih edilen hızlı ve etkili yöntemdir.",
            "ELDİVEN EL YIKAMANIN YERİNE GEÇMEZ: Eldiven kullanımı el hijyeninin alternatifi DEĞİLDİR; eldiven çıkarıldıktan sonra eller MUTLAKA yıkanmalı veya ovalanmalıdır!",
            "ELDİVEN DEĞİŞTİRME KURALI: Aynı hastada kirli bölgeden temiz bölgeye geçerken eldiven çıkarılır, el hijyeni sağlanır, yeni eldiven giyilir; hastadan hastaya geçerken de kesinlikle değiştirilir."
        ],
        "keyBullets": [
            {"title": "DSÖ'nün 5 El Hijyeni Endikasyonu", "desc": "1) Hastaya dokunmadan önce, 2) Temiz/aseptik işlemden önce, 3) Vücut sıvısı bulaş riskinden sonra, 4) Hastaya dokunduktan sonra, 5) Hasta çevresine dokunduktan sonra."},
            {"title": "Yıkama Süresi", "desc": "Su ve sabunla en az 40-60 saniye, alkol bazlı antiseptikle en az 20-30 saniye tüm el yüzeyleri ovulmalıdır."},
            {"title": "Yapay Tırnak Yasağı", "desc": "Yapay tırnaklar ve ojeli çatlaklar gram negatif basiller ve mayalar için rezervuardır; sağlık personelinde yasaktır."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-21",
                "question": "Hangi iki durumda alkol bazlı el antiseptiği yerine ellerin MUTLAKA su ve sabunla yıkanması zorunludur?",
                "answer": "1) Ellerde gözle görülür kirlenme veya kan/vücut sıvısı bulaşı olduğunda, 2) Sporlu bakteri (Clostridioides difficile) ile temas durumunda.",
                "hint": "Gözle görülür kirlenme ve C. difficile teması."
            },
            {
                "id": "fc-iz-22",
                "question": "Eldiven kullanımı ile el hijyeni arasındaki ilişkiye dair temel kural nedir?",
                "answer": "Eldiven el hijyeninin alternatifi değildir; eldiven giymeden önce ve eldiven çıkarıldıktan hemen sonra el hijyeni uygulanması şarttır.",
                "hint": "Eldiven el yıkamanın alternatifi değildir."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Güvenli Enjeksiyon ve Kesici-Delici Alet Yaralanmalarından Korunma",
        "subtitle": "Asla kılıfına takmama (No Recapping) kuralı, sarı atık kutuları ve sıçrama önlemleri",
        "badge": "Standart: Güvenli Enjeksiyon",
        "badgeColor": "amber",
        "target_ids": ["d3-k1-enf-013"],
        "keywords": ["güvenli enjeksiyon", "recapping", "iğne kapağı", "delinmeye dirençli kutu"],
        "lead": "Sağlık çalışanlarının kan yoluyla bulaşan patojenlere (HBV, HCV, HIV) maruz kalmasının bir numaralı nedeni enjeksiyon iğnelerinin kapağını iki elle kapatmaya çalışmaktır.",
        "spotPearls": [
            "ASLA KILIFINA GEÇİRMEYİN (NO RECAPPING!): Kullanılmış enjektör iğneleri kesinlikle kılıfına tekrar geçirilmemelidir (recapping yapılmamalıdır), iki elle tutulmamalı, eğilip bükülmemelidir! (Kurul 1 Çıkmış Soru!).",
            "DELİNMEYE DAYANIKLI SARI KUTULAR: İğneler kullanıldıktan hemen sonra ayrıştırılmadan delinmeye ve sızdırmaya dirençli özel sarı tıbbi atık kutularına atılmalıdır.",
            "SIÇRAMA RİSKİNE KARŞI TAM KORUMA: Kan ve vücut sıvılarının sıçrama ihtimali olan işlemlerde (entübasyon, aspirasyon, doğum, pansuman) yalnızca önlük ve eldiven yetmez; MASKE, YÜZ VE GÖZ KORUYUCU (SİPERLİK) da ZORUNLUDUR! (Kurul 1 Çıkmış Soru!).",
            "TEK DOZLUK FLAKON KURALI: Enjektörler asla birden fazla hastada veya flakonda ortak kullanılmamalıdır."
        ],
        "keyBullets": [
            {"title": "Kutu Doldurma Limiti", "desc": "Kesici-delici alet kutuları 3/4 oranında dolduğunda kapatılmalı ve kilitlenerek tıbbi atığa gönderilmelidir."},
            {"title": "İğne Batması Sonrası Eylem", "desc": "Batan bölge sıkılmadan hemen su ve sabunla yıkanmalı, antiseptik dökülmeli ve 2 saat içinde Enfeksiyon Komitesine bildirilerek profilaksi değerlendirilmelidir."},
            {"title": "Hepatit B Aşılaması", "desc": "Tüm sağlık personeli göreve başlarken HBV aşısı ile bağışıklanmalı ve Anti-HBs titresi belgelenmelidir."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-23",
                "question": "Enjeksiyon sonrası iğne batması yaralanmalarını önlemede 'altın kural' nedir?",
                "answer": "Kullanılmış iğneler kesinlikle kılıfına tekrar geçirilmemeli (recapping yapılmamalı), bükülmemeli ve doğrudan delinmeye dirençli sarı kutuya atılmalıdır.",
                "hint": "Recapping yapılmaz, kılıfına takılmaz."
            },
            {
                "id": "fc-iz-24",
                "question": "Kan ve vücut sıvılarının sıçrama ihtimali olan cerrahi veya girişimsel bir işlemde standart önlemler kapsamında hangi kişisel koruyucu donanımlar eksiksiz giyilmelidir?",
                "answer": "Önlük, eldiven, tıbbi maske ve yüz/göz koruyucu (gözlük veya siperlik) birlikte giyilmelidir.",
                "hint": "Önlük + Eldiven + Maske + Gözlük/Siperlik."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Temas İzolasyonu (Kırmızı Yıldız) ve Çoğul Dirençli Mikroorganizmalar",
        "subtitle": "Kırmızı Yıldız sembolü, MRSA, VRE, Acinetobacter, CRE ve hastaya özel ekipman",
        "badge": "Temas İzolasyonu",
        "badgeColor": "red",
        "target_ids": ["d3-k1-enf-010", "d3-k1-enf-011", "d3-k1-enf-014"],
        "keywords": ["temas izolasyonu", "kırmızı yıldız", "mrsa", "vre", "karbapenem dirençli"],
        "lead": "Temas izolasyonu; hastanelerde antibiyotik direncinin yayılmasını durduran en kritik bariyerdir ve kapıya asılan Kırmızı Yıldız sembolü ile tanımlanır.",
        "spotPearls": [
            "ENFEKSİYON KONTROL SEMBOLÜ: Hastanelerde temas izolasyonunu simgeleyen işaret KIRMIZI YILDIZ'dır (veya Kırmızı El) (Kurul 1 Çıkmış Soru!).",
            "MAJÖR ENDİKASYONLAR: Çoğul dirençli bakteriler (MRSA, VRE, Acinetobacter baumannii, Pseudomonas aeruginosa, Karbapenem Dirençli Klebsiella - CRE/KPC - Kurul 1 Çıkmış Soru!), C. difficile psödomembranöz koliti, rota/norovirüs enfeksiyonları, uyuz (skabiyez) ve bit.",
            "ODAYA GİRİŞ VE ÇIKIŞ PROTOKOLÜ: Odaya girerken ÖNLÜK VE ELDİVEN GİYİLİR; kişisel koruyucu ekipmanlar HASTA ODASINDAN AYRILMADAN ÇIKARILIR ve odadan çıktıktan sonra el hijyeni uygulanır!",
            "ODA YÖNETİMİ: Tercihen TEK KİŞİLİK ODA; tek kişilik oda yoksa aynı mikroorganizma ile enfekte/kolonize hastalar aynı odaya yerleştirilir (KOHORTLAMA).",
            "N95 MASKE YANILGISI: Temas izolasyonunda N95 partikül maskesi takılması GEREKMEZ (N95 solunum izolasyonuna aittir! - Kurul 1 Çıkmış Soru!).",
            "CİHAZ PAYLAŞIMI YASAĞI: Stetoskop, tansiyon aleti ve derece hastaya özel tahsis edilir; diğer hastalarla ortak kullanılamaz."
        ],
        "keyBullets": [
            {"title": "C. difficile İçin Çamaşır Suyu", "desc": "C. difficile sporları alkole dirençlidir; oda yüzeyleri klor bazlı solüsyonlarla (çamaşır suyu) dezenfekte edilmelidir."},
            {"title": "Hasta Ziyaretçi Kısıtlaması", "desc": "Temas izolasyonundaki hastanın ziyaretçileri eğitilmeli ve odaya girerken koruyucu önlük giymeleri sağlanmalıdır."},
            {"title": "Transport Kuralları", "desc": "Hasta tetkik için odadan çıkarılacaksa enfekte bölgesi temiz çarşafla örtülmeli ve gidilen birim önceden uyarılmalıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-25",
                "question": "Hastanelerde temas izolasyonunu simgeleyen enfeksiyon kontrol sembolü nedir ve odada N95 maske takılması gerekir mi?",
                "answer": "KIRMIZI YILDIZ'dır; temas izolasyonunda N95 maske takılmasına GEREK YOKTUR (önlük ve eldiven giyilir).",
                "hint": "Kırmızı Yıldız, N95 gerekmez."
            },
            {
                "id": "fc-iz-26",
                "question": "Karbapenem dirençli Klebsiella pneumoniae (CRE) veya VRE ile kolonize bir hastada standart önlemlere ek olarak hangi izolasyon tipi uygulanmalıdır?",
                "answer": "Temas İzolasyonu uygulanmalıdır (Kurul 1 Çıkmış Soru).",
                "hint": "Temas İzolasyonu."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Damlacık İzolasyonu (Mavi Çiçek) ve 1 Metre Güvenlik Kuralı",
        "subtitle": "Mavi Papatya/Çiçek sembolü, Meningokok, İnfluenza, Boğmaca ve cerrahi maske zorunluluğu",
        "badge": "Damlacık İzolasyonu",
        "badgeColor": "blue",
        "target_ids": ["d3-k1-enf-004", "d3-k1-enf-012"],
        "keywords": ["damlacık izolasyonu", "mavi çiçek", "meningokok", "cerrahi maske", "1 metre kuralı"],
        "lead": "Damlacık izolasyonu; konuşma, öksürme veya hapşırma sırasında çevreye saçılan büyük solunum damlacıklarının (>100 µm) ağız, burun ve göz mukozasına sıçramasını önler.",
        "spotPearls": [
            "ENFEKSİYON KONTROL SEMBOLÜ: Damlacık izolasyonunu simgeleyen işaret MAVİ ÇİÇEK (veya Mavi Papatya)'dir.",
            "MAJÖR ENDİKASYONLAR: Neisseria meningitidis (Meningokoksemi ve menenjit - DİKKAT: solunum değil damlacıktır! - Kurul 1 Çıkmış Soru!), Bordetella pertussis (Boğmaca), İnfluenza (Grip), Kabakulak, Rubella (Kızamıkçık), Parvovirüs B19, Mycoplasma pneumoniae.",
            "1 METRE MESAFE VE CERRAHİ MASKE: Hastaya 1 METREDEN YAKIN MESAFEDE çalışırken CERRAHİ / TIBBİ MASKE takılması zorunludur (N95 maske şart değildir).",
            "ODA DÜZENİ: Tek kişilik oda; mümkün değilse kohortlama veya farklı tanılı hastalar arasında EN AZ 1 METRE (tercihen 2 metre) fiziksel mesafe bırakılması şarttır.",
            "HASTANIN TRANSPORTU: Damlacık izolasyonundaki hasta oda dışına çıkmak zorunda kalırsa ağız ve burnunu kapatan CERRAHİ MASKE takmalıdır."
        ],
        "keyBullets": [
            {"title": "Meningokok Kemoprofilaksisi", "desc": "Meningokok damlacığına maruz kalan yakın temaslı sağlık personeline 24 saat içinde rifampisin veya siprofloksasin profilaksisi verilir."},
            {"title": "Havalandırma İhtiyacı", "desc": "Damlacıklar havada asılı kalmayıp hızla çöktüğü için negatif basınçlı özel havalandırma sistemine İHTİYAÇ YOKTUR."},
            {"title": "Göz Koruması", "desc": "Aspirasyon veya entübasyon gibi damlacık sıçratacak işlemlerde maskeye ek olarak koruyucu gözlük veya yüz siperliği takılmalıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-27",
                "question": "Hastanelerde damlacık izolasyonunu simgeleyen işaret nedir ve hastaya kaç metreden yakın mesafede cerrahi maske takılmalıdır?",
                "answer": "MAVİ ÇİÇEK (veya Mavi Papatya)'dir; hastaya 1 metreden yakın mesafede cerrahi maske takılması zorunludur.",
                "hint": "Mavi Çiçek ve 1 metre mesafede cerrahi maske."
            },
            {
                "id": "fc-iz-28",
                "question": "Neisseria meningitidis (meningokok menenjiti) tanısı alan bir hastada solunum izolasyonu mu yoksa damlacık izolasyonu mu uygulanmalıdır?",
                "answer": "Damlacık İzolasyonu uygulanmalıdır (aerosol/solunum değil büyük damlacıkla bulaşır - Kurul 1 Çıkmış Soru).",
                "hint": "Damlacık İzolasyonu."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Solunum (Hava Yolu) İzolasyonu (Sarı Yaprak) ve Negatif Basınç",
        "subtitle": "Sarı Yaprak sembolü, Tüberküloz, Kızamık, Suçiçeği, N95 maske ve saatte 6-12 hava değişimi",
        "badge": "Solunum İzolasyonu",
        "badgeColor": "amber",
        "target_ids": ["d3-k1-enf-004", "d3-k1-enf-010", "d3-k1-enf-012"],
        "keywords": ["solunum izolasyonu", "sarı yaprak", "tüberküloz", "n95 maske", "negatif basınç"],
        "lead": "Solunum (hava yolu) izolasyonu; havada saatlerce asılı kalan mikroskobik damlacık çekirdekleriyle (<10 µm) bulaşan tüberküloz, kızamık gibi son derece bulaşıcı patojenlere karşı en üst düzey mühendislik kontrolüdür.",
        "spotPearls": [
            "ENFEKSİYON KONTROL SEMBOLÜ: Solunum (hava yolu) izolasyonunu simgeleyen işaret SARI YAPRAK'tır.",
            "MAJÖR ENDİKASYONLAR: Mycobacterium tuberculosis (Akciğer ve larinks tüberkülozu), Kızamık (Rubeola), Suçiçeği (Varicella zoster), Yaygın Zona (dissemine herpes zoster), SARS, ve aerosol oluşturan işlemler sırasında COVID-19 (Kurul 1 Çıkmış Soru!).",
            "NEGATİF BASINÇLI ÖZEL ODA ŞARTI: Oda havasının koridora sızmasını önlemek için koridordan odaya doğru hava akışı sağlayan NEGATİF BASINÇLI ODA şarttır; hava SAATTE 6-12 KEZ DEĞİŞTİRİLMELİ ve dışarıya atılmadan önce HEPA filtreden geçirilmelidir!",
            "N95 / FFP2 MASKE ZORUNLULUĞU: Odaya giren tüm sağlık personeli yüksek filtrasyonlu partikül maskesi (N95, FFP2 veya FFP3) takmak ZORUNDADIR! (Cerrahi maske personeli korumaz!).",
            "HASTANIN MASKESİ: Hasta odaya kapatıldığında maske takmaz; ancak oda dışına transport gerektiğinde CERRAHİ MASKE takar (valfsiz maske)."
        ],
        "keyBullets": [
            {"title": "Oda Kapısının Kapalı Kalması", "desc": "Negatif basınç gradiyentinin korunması için oda kapısı ve pencereler sürekli kapalı tutulmalıdır."},
            {"title": "N95 Maske Uyumu (Fit Test)", "desc": "N95 maske takıldığında kenarlardan hava kaçırmadığından emin olmak için kullanıcı sızdırmazlık testi (seal check) yapmalıdır."},
            {"title": "Bağışık Personel Görevlendirmesi", "desc": "Kızamık ve suçiçeği hastalarının bakımında aşılanmış veya hastalığı geçirmiş bağışık personelin çalışması tercih edilir."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-29",
                "question": "Hastanelerde solunum (hava yolu) izolasyonunu simgeleyen işaret nedir ve oda havasının özellikleri nasıl olmalıdır?",
                "answer": "SARI YAPRAK'tır; oda koridora göre NEGATİF BASINÇLI olmalı ve saatte 6-12 kez hava değişimi (HEPA filtreli) sağlanmalıdır.",
                "hint": "Sarı Yaprak, negatif basınç, saatte 6-12 hava değişimi."
            },
            {
                "id": "fc-iz-30",
                "question": "Aktif akciğer tüberkülozu veya kızamık hastasının odasına girerken sağlık personeli hangi tip maske takmak zorundadır?",
                "answer": "N95 (veya FFP2 / FFP3) yüksek filtrasyonlu partikül maskesi takmak zorundadır (cerrahi maske yetersizdir - Kurul 1 Çıkmış Soru).",
                "hint": "N95 / FFP2 maske."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Üç İzolasyon Tipinin ve Hastane Sembollerinin Karşılaştırma Matrisi",
        "subtitle": "Kırmızı Yıldız vs Mavi Çiçek vs Sarı Yaprak; endikasyon, KKE ve oda gereksinimleri",
        "badge": "İzolasyon Karşılaştırma",
        "badgeColor": "purple",
        "target_ids": ["d3-k1-enf-011", "d3-k1-enf-012"],
        "keywords": ["izolasyon sembolleri", "kırmızı yıldız", "mavi çiçek", "sarı yaprak", "karşılaştırma tablosu"],
        "lead": "Klinik pratikte ve Kurul sınavlarında hangi hastalığa hangi sembolün ve hangi kişisel koruyucu ekipmanın atanacağı hayati bir karar matrisidir.",
        "spotPearls": [
            "SEMBOL ÖZETİ: Temas = KIRMIZI YILDIZ; Damlacık = MAVİ ÇİÇEK; Solunum = SARI YAPRAK.",
            "MASKE AYRIMI: Temas'ta maske şart değil; Damlacık'ta 1 metre yakında CERRAHİ MASKE; Solunum'da odaya girerken N95 / FFP2 MASKE zorunludur.",
            "ODA AYRIMI: Temas ve Damlacık'ta standart tek kişilik oda veya kohortlama yeterli iken; Solunum İzolasyonunda NEGATİF BASINÇLI ÖZEL ODA zorunludur.",
            "AYIRICI TANI TUZAĞI: Meningokok damlacıktır (Mavi Çiçek); Tüberküloz solunumdur (Sarı Yaprak); MRSA/VRE temastır (Kırmızı Yıldız)!"
        ],
        "keyBullets": [
            {"title": "Çoklu İzolasyon", "desc": "Bir hastada hem MRSA hem tüberküloz varsa kapıya hem Kırmızı Yıldız hem Sarı Yaprak asılır."},
            {"title": "Görsel Uyarı Panoları", "desc": "Semboller hasta odasının kapısına göz hizasında asılmalı ve odaya giren herkesin görmesi sağlanmalıdır."},
            {"title": "Hasta Yakını Eğitimi", "desc": "Hasta yakınlarına sembolün anlamı anlatılmalı ve koruyucu ekipman giymeden odaya girmeleri engellenmelidir."}
        ],
        "table": {
            "title": "Hastanelerde Bulaş Yoluna Yönelik İzolasyon Önlemleri Karşılaştırma Matrisi",
            "headers": ["İzolasyon Tipi", "Sembol", "Bulaş Partikülü", "Prototip Hastalıklar", "Oda Tipi", "Sağlık Personeli KKE", "Hasta Transportu"],
            "rows": [
                ["Temas İzolasyonu", "Kırmızı Yıldız (veya El)", "Direk / İndirek temas, fomitler", "MRSA, VRE, Acinetobacter, CRE, C. difficile, Uyuz", "Tek kişilik veya kohort", "Önlük + Eldiven (N95 gerekmez)", "Enfekte alan örtülür"],
                ["Damlacık İzolasyonu", "Mavi Çiçek (Papatya)", "> 100 µm kaba damlacıklar", "Meningokok, Boğmaca, İnfluenza, Kabakulak, Parvovirüs", "Tek kişilik oda (hastalar arası ≥1m)", "1 m yakında Cerrahi Maske", "Hastaya cerrahi maske"],
                ["Solunum (Hava Yolu)", "Sarı Yaprak", "< 10 µm damlacık çekirdeği (aerosol)", "Akciğer Tüberkülozu, Kızamık, Suçiçeği, Dissemine Zona", "NEGATİF BASINÇLI ODA (saatte 6-12 hava değişimi)", "N95 / FFP2 Maske (Zorunlu)", "Hastaya cerrahi maske"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-iz-31",
                "question": "Hastanelerde Temas, Damlacık ve Solunum izolasyonlarını simgeleyen renkli işaretler sırasıyla nelerdir?",
                "answer": "Temas = Kırmızı Yıldız; Damlacık = Mavi Çiçek (Papatya); Solunum = Sarı Yaprak.",
                "hint": "Kırmızı Yıldız, Mavi Çiçek, Sarı Yaprak."
            },
            {
                "id": "fc-iz-32",
                "question": "Damlacık izolasyonundaki bir hastanın bakımında cerrahi maske yeterli midir, yoksa N95 maske zorunlu mudur?",
                "answer": "Cerrahi maske 1 metreden yakın temasta tamamen yeterlidir; N95 maske damlacık için değil, solunum (hava yolu) izolasyonu için zorunludur.",
                "hint": "Cerrahi maske yeterlidir; N95 solunum içindir."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Kişisel Koruyucu Ekipman (KKE) Giyme ve Çıkarma Protokolü",
        "subtitle": "Temizden kirliye giyme, en kirliden en temize çıkarma sıralaması ve el hijyeni entegrasyonu",
        "badge": "KKE Protokolü",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["kke giyme sırası", "kke çıkarma sırası", "önlük eldiven maske", "kontaminasyon"],
        "lead": "Kişisel koruyucu ekipmanların giyilmesi kadar çıkarılması da enfeksiyon kontrolünün en kritik anıdır; çıkarma esnasında yapılacak tek bir hata personelin kendisini kontamine etmesine yol açar.",
        "spotPearls": [
            "GİYME SIRASI (AŞAĞIDAN YUKARIYA / TEMİZDEN KİRLİYE): 1) ÖNLÜK → 2) MASKE (Cerrahi veya N95) → 3) GÖZLÜK VEYA SİPERLİK → 4) ELDİVEN (eldiven manşeti önlüğün kolunu kapatmalıdır).",
            "ÇIKARMA SIRASI (EN KİRLİDEN EN TEMİZE): 1) ELDİVEN (en kontamine yüzey!) → 2) GÖZLÜK VEYA SİPERLİK → 3) ÖNLÜK (içten dışa rulo yapılarak) → 4) MASKE (iplerinden tutularak, ön yüzüne asla dokunulmadan!) → 5) EL HİJYENİ.",
            "N95 ÇIKARMA YERİ: N95 maske hasta odasında DEĞİL; odanın kapısı kapatıldıktan sonra KORİDORDA / ANTE-ROOM'DA çıkarılmalıdır!",
            "ASLA DOKUNULMAYACAK YÜZEY: Maskenin ve siperliğin ön dış yüzeyi yoğun mikrop yüklüdür; çıkarırken kesinlikle ön yüze dokunulmaz, arkadaki lastik ve iplerden tutulur."
        ],
        "keyBullets": [
            {"title": "Eldiven Çıkarma Tekniği", "desc": "Glove-in-glove (eldiven içinde eldiven) tekniği ile dış yüzey içe katlanarak soyulur ve tıbbi atığa atılır."},
            {"title": "Önlük Çıkarma Tekniği", "desc": "Boyun ve bel bağları çözüldükten sonra omuzlardan öne doğru çekilip iç kısmı dışa gelecek şekilde rulo yapılır."},
            {"title": "Her Basamakta El Hijyeni", "desc": "Şüpheli bir temas olduğunda çıkarma adımları arasında dahi el antiseptiği kullanılabilir."}
        ],
        "table": {
            "title": "Kişisel Koruyucu Ekipman (KKE) Standart Giyme ve Çıkarma Sıralaması",
            "headers": ["Adım No", "Giyme Sırası (Odaya Girerken)", "Çıkarma Sırası (Odadan Çıkarken)"],
            "rows": [
                ["1. Adım", "Önlük (Beden tam sarılır, arkadan bağlanır)", "Eldiven (En kirli parçadır, ilk çıkarılır)"],
                ["2. Adım", "Maske (Burun teli sıkıştırılır, tam oturma sağlanır)", "Gözlük / Yüz Siperliği (Dışına dokunmadan arkadan)"],
                ["3. Adım", "Gözlük veya Yüz Siperliği (Gözler korunur)", "Önlük (İç yüzü dışa çevrilerek rulo yapılır)"],
                ["4. Adım", "Eldiven (Önlük manşetlerinin üzerine geçirilir)", "Maske (Oda dışında iplerinden tutularak çıkarılır)"],
                ["Son İşlem", "Odaya güvenli giriş", "MUTLAKA EL HİJYENİ (Su-sabun veya alkol antiseptiği)"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-iz-33",
                "question": "Kişisel koruyucu ekipmanların (KKE) standart giyme sırası nasıldır?",
                "answer": "1) Önlük → 2) Maske → 3) Gözlük/Siperlik → 4) Eldiven.",
                "hint": "Önlük -> Maske -> Gözlük -> Eldiven."
            },
            {
                "id": "fc-iz-34",
                "question": "Kişisel koruyucu ekipmanların (KKE) standart çıkarma sırası nasıldır ve maskenin ön yüzeyine dokunulur mu?",
                "answer": "1) Eldiven → 2) Gözlük/Siperlik → 3) Önlük → 4) Maske → 5) El Hijyeni; maskenin ön yüzeyine kesinlikle dokunulmaz, iplerinden tutularak çıkarılır.",
                "hint": "Eldiven -> Gözlük -> Önlük -> Maske -> El Hijyeni."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Çoğul İlaç Dirençli Bakteriler (MDRO) ve Antibiyotik Yönetimi",
        "subtitle": "ESBL, MRSA, VRE, CRE/KPC, kolistin direnci ve akılcı antibiyotik kullanımı",
        "badge": "Antibiyotik Direnci & MDRO",
        "badgeColor": "red",
        "target_ids": [],
        "keywords": ["mdro", "çoğul direnç", "mrsa", "vre", "antibiyotik yönetimi", "esbl"],
        "lead": "Antibiyotiklerin bilinçsiz ve aşırı kullanımı hastaneleri çoğul ilaç dirençli bakterilerin (MDRO) üreme merkezine çevirmiştir; enfeksiyon kontrolü akılcı antibiyotik yönetimiyle (Antimicrobial Stewardship) ayrılmaz bir bütündür.",
        "spotPearls": [
            "KRİTİK MDRO TÜRLERİ: 1) MRSA (Metisiline Dirençli S. aureus - mecA geni / PBP2a değişimi), 2) VRE (Vankomisine Dirençli Enterokok - vanA/vanB), 3) ESBL (Genişlemiş Spektrumlu Beta-Laktamaz üreten E. coli/Klebsiella), 4) CRE / KPC (Karbapenem Dirençli Enterobacteriaceae).",
            "SON ÇARE ANTİBİYOTİKLERİN TÜKENİŞİ: Karbapenemlere ve Kolistine direnç gelişmesi durumunda tedavi seçeneği kalmayan 'pan-rezistan' suşlar ortaya çıkar.",
            "ANTİBİYOTİK YÖNETİMİ (STEWARDSHIP) İLKELERİ: 1) Kültür almadan ampirik antibiyotik başlama, 2) Kültür-antibiyogram sonucu çıkınca spektrumu daralt (De-eskalasyon), 3) Tedavi süresini gereksiz uzatma, 4) Kolonizasyonu tedavi etme!",
            "TEMAS İZOLASYONU ZORUNLULUĞU: Bir serviste tek bir CRE veya VRE saptandığında derhal temas izolasyonu uygulanmazsa tüm servis haftalar içinde enfekte olur."
        ],
        "keyBullets": [
            {"title": "MecA Geni ve PBP2a", "desc": "MRSA'da penisilin bağlayan protein (PBP) yapısı değiştiğinden tüm standart beta-laktamlar (sefalosporinler dahil) etkisiz kalır; glikopeptid (vankomisin) gerekir."},
            {"title": "Kolonizasyon Tedavi Edilmez", "desc": "Asemptomatik bakteriüri veya trakeal aspiratta üreyen kolonize bakteriye antibiyotik vermek sadece dirençli suş seçer."},
            {"title": "El Yıkama ile Direnç Kırılması", "desc": "Dirençli bakterilerin hastadan hastaya taşınmasının %90'ı sağlık personelinin kontamine elleriyle gerçekleşir."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-35",
                "question": "MRSA'da metisilin direncinin moleküler mekanizması nedir ve hangi hedef protein değişir?",
                "answer": "mecA geni aracılığıyla beta-laktam antibiyotiklerin bağlanamadığı PBP2a (penisilin bağlayan protein 2a) sentezlenmesidir.",
                "hint": "mecA geni ve PBP2a."
            },
            {
                "id": "fc-iz-36",
                "question": "Akılcı antibiyotik yönetiminde (Antimicrobial Stewardship) kültür ve antibiyogram sonuçları çıktıktan sonra geniş spektrumlu tedavinin dar spektrumlu spesifik ajana çevrilmesine ne ad verilir?",
                "answer": "De-eskalasyon (spektrum daraltma) adı verilir.",
                "hint": "De-eskalasyon."
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "Koruyucu Ortam (Ters İzolasyon) ve Nötropenik Hasta Yönetimi",
        "subtitle": "Pozitif basınçlı odalar, mutlak nötrofil <500/mm³, allojeneik KİT ve çevresel mantar korunması",
        "badge": "Ters İzolasyon",
        "badgeColor": "cyan",
        "target_ids": [],
        "keywords": ["ters izolasyon", "koruyucu ortam", "pozitif basınç", "nötropeni", "aspergillus"],
        "lead": "Klasik izolasyon toplumu ve personeli hastadan korurken; Koruyucu Ortam (Ters İzolasyon) ağır immünsüprese savunmasız hastayı hastane ortamındaki mikroplardan korumak için tasarlanmıştır.",
        "spotPearls": [
            "KORUYUCU ORTAM TANIMI: Ağır immün yetmezlikli bireyleri (özellikle allojeneik hematopoetik kök hücre nakli alıcıları ve mutlak nötrofil sayısı <500/mm³ olan derin nötropenik hastalar) çevresel fırsatçı patojenlerden korumak için oluşturulan ortamdır.",
            "POZİTİF BASINÇLI ODA: Solunum izolasyonunun tam tersine, ODADAN KORİDORA DOĞRU hava akışı sağlayan POZİTİF BASINÇLI ODA kullanılır; odaya giren hava %99.97 verimlilikte HEPA filtrelerden geçirilir.",
            "ASPERGİLLUS KORUNMASI: Havadaki mantar sporlarının (özellikle Aspergillus küf sporları) hastanın solunum yollarına ulaşmasını engellemek ana hedeftir.",
            "YASAKLAR: Odaya canlı/taze çiçek, saksı bitkisi sokulması ve çiğ meyve-sebze tüketimi kesinlikle yasaktır (Pseudomonas ve mantar kaynağı!)."
        ],
        "keyBullets": [
            {"title": "Basınç Yönü Zıtlığı", "desc": "Solunum izolasyonu: Negatif basınç (mikrop dışarı kaçmasın); Ters izolasyon: Pozitif basınç (mikrop içeri girmesin)."},
            {"title": "Sağlık Personeli Girişi", "desc": "Odaya giren personel ellerini titizlikle yıkamalı, maske ve temiz önlük giymelidir; enfeksiyon semptomu olan personel giremez."},
            {"title": "Düşük Mikrobiyal Diyet", "desc": "Nötropenik hastalara pastörize, iyi pişmiş gıdalar verilir; kabuklu soyulmamış meyveler yasaklanır."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-37",
                "question": "Solunum (hava yolu) izolasyon odası ile Koruyucu Ortam (ters izolasyon) odası arasındaki hava basıncı yönü farkı nedir?",
                "answer": "Solunum izolasyonu NEGATİF BASINÇLIDIR (hava koridordan odaya akar); Koruyucu ortam ise POZİTİF BASINÇLIDIR (hava odadan koridora akar).",
                "hint": "Solunum = Negatif basınç; Koruyucu ortam = Pozitif basınç."
            },
            {
                "id": "fc-iz-38",
                "question": "Derin nötropenik (kemik iliği nakilli) bir hastanın koruyucu ortam odasına canlı saksı çiçeği sokulmasının yasak olmasının temel mikrobiyolojik nedeni nedir?",
                "answer": "Toprak ve bitkilerde ölümcül invaziv aspergillozise yol açan Aspergillus küf sporları ve Pseudomonas bakterilerinin bulunmasıdır.",
                "hint": "Aspergillus mantar sporları ve Pseudomonas."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Büyük Sentez: İzolasyon Karar Ağacı ve Kurul 1 Altın İpuçları",
        "subtitle": "Dr. Rüveyda Korkmazer & Dr. Merve Kaçar amfi dersleri çekirdek sentezi ve çıkmış soru analizleri",
        "badge": "Büyük Sentez",
        "badgeColor": "sky",
        "target_ids": ["d3-k1-enf-009", "d3-k1-enf-011", "d3-k1-enf-014"],
        "keywords": ["büyük sentez", "altın spotlar", "izolasyon karar ağacı", "kurul 1 çıkmış"],
        "lead": "İzolasyon önlemleri sağlık çalışanını, hastayı ve toplumu koruyan tıbbi savunma duvarıdır; doğru endikasyon, doğru sembol ve tavizsiz el hijyeni ile hayat kurtarır.",
        "spotPearls": [
            "TÜM HASTALARA: Standart önlemler (El hijyeni, eldiven, kan/sıvı sıçramasında önlük/maske/gözlük, recapping yapmama, sarı kutu).",
            "KIRMIZI YILDIZ (TEMAS): MRSA, VRE, Acinetobacter, CRE, C. difficile, uyuz → Önlük + Eldiven giyilir, odada çıkarılır, hastaya özel stetoskop, N95 GEREKMEZ!",
            "MAVİ ÇİÇEK (DAMLACIK): Meningokok, Boğmaca, İnfluenza, Kabakulak, Parvovirüs → 1 metre mesafede CERRAHİ MASKE, tek kişilik oda veya ≥1m aralık.",
            "SARI YAPRAK (SOLUNUM): Tüberküloz, Kızamık, Suçiçeği → NEGATİF BASINÇLI ODA (saatte 6-12 hava değişimi), odaya girerken N95 / FFP2 MASKE ZORUNLU!",
            "STERİL BÖLGELER: BOS, Üreter, Böbrek, Alt solunum ve Kan kesinlikle sterildir; flora İÇERMEZ!",
            "VİRÜLANS DERECEDİR: Patojenite hastalık yapabilme kapasitesi, Virülans ise hastalığın şiddet ve ağırlık derecesidir."
        ],
        "keyBullets": [
            {"title": "Meningokok Sınav Tuzağı", "desc": "Meningokok solunum değil DAMLACIKTIR (Mavi Çiçek); N95 değil cerrahi maske takılır."},
            {"title": "C. Difficile ve Alkol Tuzağı", "desc": "C. difficile hastasına temas sonrası alkol bazlı jel yetersizdir; mutlaka SU VE SABUNLA yıkanmalıdır."},
            {"title": "Güvenli İğne Kuralı", "desc": "Kullanılmış iğne ucu asla kapağına sokulmaz, tek elle bile olsa recapping yapılmaz."}
        ],
        "flashcards": [
            {
                "id": "fc-iz-39",
                "question": "Hastanede aktif akciğer tüberkülozu olan bir hastaya refakat edecek stajyer doktor hangi sembolün asılı olduğu odaya girmeli ve hangi maskeyi takmalıdır?",
                "answer": "SARI YAPRAK sembolü bulunan negatif basınçlı odaya girmeli ve N95 (veya FFP2) partikül maskesi takmalıdır.",
                "hint": "Sarı Yaprak ve N95 maske."
            },
            {
                "id": "fc-iz-40",
                "question": "Kurul 1 sınavında 'Standart izolasyon önlemleri yalnızca HIV veya hepatit taşıyan hastalara uygulanır' ifadesi doğru mudur?",
                "answer": "KESİNLİKLE YANLIŞTIR; standart önlemler tanısına ve enfeksiyon durumuna bakılmaksızın hastanedeki TÜM HASTALARA uygulanır.",
                "hint": "Yanlıştır; tüm hastalara uygulanır."
            }
        ]
    }
]

def build_synthesis_narrative(slide_data):
    lines = []
    lines.append(f"### {slide_data['title']}")
    lines.append(f"#### {slide_data['subtitle']}")
    lines.append("")
    lines.append(f"• **Temel Enfeksiyon Kontrolü ve Mikrobiyolojik Çerçeve:** {slide_data['lead']}")
    lines.append("")
    
    for kb in slide_data.get('keyBullets', []):
        lines.append(f"• **{kb['title']}:** {kb['desc']}")
        lines.append("")

    lines.append("💡 **Enfeksiyon Hastalıkları Sentezi ve Fakülte Sınav İncileri (Dr. Rüveyda Korkmazer & Dr. Merve Kaçar):**")
    for sp in slide_data.get('spotPearls', []):
        lines.append(f"• {sp}")
    
    return "\n".join(lines)

def build_deck():
    slides = []
    total_cards = 0
    total_questions = 0

    for s_raw in SLIDES_DATA:
        narrative = build_synthesis_narrative(s_raw)
        
        core_content = {
            "keyBullets": s_raw.get('keyBullets', [])
        }
        if "table" in s_raw:
            core_content["table"] = s_raw["table"]

        target_ids = s_raw.get('target_ids', [])
        keywords = s_raw.get('keywords', [])
        matched_qs = find_matched_questions(target_ids=target_ids, keywords=keywords, max_count=2)
        total_questions += len(matched_qs)

        title_clean = s_raw['title']
        ai_prompts = [
            f"Dr. Rüveyda Korkmazer ve Dr. Merve Kaçar'ın amfi derslerinde '{title_clean}' konusunda vurguladığı en kritik sınav tuzakları nelerdir?",
            f"Klinik hastane uygulamasında '{title_clean}' ilkeleri doğrultusunda bir enfeksiyon kontrol hemşiresi veya hekimi nasıl karar almalıdır?",
            f"Dönem 3 Kurul 1 Enfeksiyon sınavında '{title_clean}' konusundan gelebilecek vaka kurgulu sorular nelerdir?"
        ]

        flashcards = []
        for fc in s_raw.get('flashcards', []):
            q_val = fc.get('question') or fc.get('front', '')
            a_val = fc.get('answer') or fc.get('back', '')
            flashcards.append({
                "id": fc.get('id', ''),
                "category": fc.get('category', 'Akıl Kartı'),
                "front": q_val,
                "back": a_val,
                "question": q_val,
                "answer": a_val,
                "hint": fc.get('hint', '')
            })
        total_cards += len(flashcards)

        slide_obj = {
            "slideNumber": s_raw['slideNumber'],
            "title": s_raw['title'],
            "subtitle": s_raw['subtitle'],
            "badge": s_raw['badge'],
            "badgeColor": s_raw['badgeColor'],
            "synthesisNarrative": narrative,
            "flashcards": flashcards,
            "coreContent": core_content,
            "spotPearls": s_raw.get('spotPearls', []),
            "relatedQuestions": matched_qs,
            "aiPromptSuggestions": ai_prompts
        }
        slides.append(slide_obj)

    deck_obj = {
        "id": "learn-enfeksiyon-izolasyon",
        "title": "Hastane Enfeksiyonları ve İzolasyon Önlemleri",
        "shortTitle": "İzolasyon Yöntemleri & Enfeksiyon Kontrolü",
        "discipline": "Enfeksiyon Hastalıkları",
        "committee": "Dönem 3 Kurul 1",
        "instructor": "Dr. Rüveyda Korkmazer & Dr. Merve Kaçar",
        "sourceFile": "3)İzolasyon yöntemleri.txt & 4)Enfeksiyon Hastalıklarında Temel Kavramlar ve Genel Özellikler.txt",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_questions,
        "totalFlashcardsCount": total_cards,
        "themeColor": "red",
        "overview": "Dönem 3 Kurul 1 Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji müfredatında yer alan İzolasyon Yöntemleri ve Enfeksiyon Hastalıklarında Temel Kavramlar derslerinin %500 derinlikte kapsamlı interaktif öğrenim sunumu. Patojenite vs virülans, mikrobiyal spektrum (prionlar, atipik bakteriler), normal mikrobiyota ve steril vücut bölgeleri, hastane enfeksiyonları (SHİE), 48 saat kuralı, enfeksiyon zinciri, bulaş yolları aerodinamiği, standart (evrensel) önlemler, el hijyeni, güvenli enjeksiyon, temas izolasyonu (Kırmızı Yıldız), damlacık izolasyonu (Mavi Çiçek), solunum izolasyonu (Sarı Yaprak), negatif basınçlı odalar, KKE giyme ve çıkarma sırası, çoğul ilaç dirençli bakteriler (MDRO) ve koruyucu ortamı (ters izolasyon), 40 adet 3D akıl kartını, 5 adet karşılaştırma tablosunu ve Kurul 1 çıkmış sınav sorularını içerir.",
        "keyExamPearls": [
            "Patojenite hastalık yapabilme kapasitesidir; Virülans ise hastalığın şiddet ve ağırlık derecesidir.",
            "Prionlar nükleik asit (DNA/RNA) içermez; fiziksel ve kimyasal inaktivasyona aşırı dirençlidir.",
            "Mikoplazmaların hücre duvarı yoktur; Gram boyanmazlar ve beta-laktam antibiyotiklere doğal dirençlidirler.",
            "BOS, alt solunum yolları, dolaşım sistemi ve üst ürogenital sistem (üreter, böbrek) KESİNLİKLE STERİLDİR, flora bulunmaz.",
            "Hastane enfeksiyonu (SHİE): Yatışta inkübasyon döneminde olmayan, yatıştan 48-72 saat sonra ortaya çıkan enfeksiyonlardır.",
            "Standart (evrensel) önlemler tanısına bakılmaksızın hastanedeki TÜM HASTALARA uygulanır; sadece HIV'e değil!",
            "Kullanılmış enjektör iğneleri kesinlikle kılıfına takılmaz (recapping yapılmaz); delinmeye dayanıklı sarı kutuya atılır.",
            "Temas izolasyonu simgesi KIRMIZI YILDIZ'dır (MRSA, VRE, CRE, Acinetobacter, C. difficile); önlük ve eldiven giyilir, N95 GEREKMEZ!",
            "Damlacık izolasyonu simgesi MAVİ ÇİÇEK'tir (Meningokok, Boğmaca, İnfluenza); 1 metre mesafede CERRAHİ MASKE takılır.",
            "Solunum (hava yolu) izolasyonu simgesi SARI YAPRAK'tır (Tüberküloz, Kızamık, Suçiçeği); NEGATİF BASINÇLI ODA ve N95 MASKE zorunludur!",
            "KKE Giyme Sırası: Önlük -> Maske -> Gözlük/Siperlik -> Eldiven. Çıkarma Sırası: Eldiven -> Gözlük -> Önlük -> Maske -> El Hijyeni.",
            "Koruyucu ortam (ters izolasyon) nötropenik hastalar için POZİTİF BASINÇLI ve HEPA filtreli odalardır; taze çiçek yasaktır."
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for Hastane Enfeksiyonları ve İzolasyon Önlemleri...")
    deck = build_deck()
    print(f"Generated deck with {len(deck['slides'])} slides and {deck['totalFlashcardsCount']} flashcards.")

    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    # We also update or replace learn-izolasyon-yontemleri and learn-enfeksiyon-hastaliklari
    target_ids = ['learn-enfeksiyon-izolasyon', 'learn-izolasyon-yontemleri', 'learn-enfeksiyon-hastaliklari']
    
    # Check if learn-enfeksiyon-izolasyon exists
    found_idx = -1
    for i, d in enumerate(decks):
        if d.get('id') == 'learn-enfeksiyon-izolasyon':
            found_idx = i
            break

    if found_idx >= 0:
        decks[found_idx] = deck
        print(f"Updated existing deck at index {found_idx} (ID: {deck['id']})")
    else:
        decks.append(deck)
        print(f"Appended new deck (ID: {deck['id']})")

    # Also update learn-izolasyon-yontemleri (index 13) and learn-enfeksiyon-hastaliklari (index 7) with the same comprehensive content
    for i, d in enumerate(decks):
        if d.get('id') in ['learn-izolasyon-yontemleri', 'learn-enfeksiyon-hastaliklari']:
            alt_deck = dict(deck)
            alt_deck['id'] = d.get('id')
            alt_deck['title'] = d.get('title')
            decks[i] = alt_deck
            print(f"Synchronized linked deck at index {i} (ID: {d.get('id')}) with full %500 content!")

    with open(DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    if os.path.exists(META_PATH):
        with open(META_PATH, 'r', encoding='utf-8') as f:
            meta_list = json.load(f)
        
        for tid in target_ids:
            meta_entry = {
                "id": tid,
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
                if m.get('id') == tid:
                    m_idx = i
                    break
            if m_idx >= 0:
                meta_list[m_idx] = meta_entry
            else:
                meta_list.append(meta_entry)

        with open(META_PATH, 'w', encoding='utf-8') as f:
            json.dump(meta_list, f, ensure_ascii=False, indent=2)
        print("Updated learning_decks_meta.json successfully.")

    if os.path.exists(QUEUE_PATH):
        with open(QUEUE_PATH, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        for item in queue:
            if item.get('id') == 'learn-enfeksiyon-izolasyon':
                item['status'] = 'completed'
                item['slidesCount'] = len(deck['slides'])
                item['detailLevel'] = '500%'
        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Updated learning_batch_queue.json: ALL KURUL 1 DECKS ARE NOW COMPLETED!")

    print("Success! Infection and isolation deck generation completed.")

if __name__ == '__main__':
    main()
