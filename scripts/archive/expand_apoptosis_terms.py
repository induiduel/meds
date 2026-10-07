#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/expand_apoptosis_terms.py
Enriches medical_encyclopedia.json and medical_glossary.json with granular entries:
1. Bax Proteini (Bcl-2 Associated X Protein)
2. Bak Proteini (Bcl-2 Antagonist/Killer)
3. İntrensek Apoptoz Yolağı (Mitokondriyal Yol)
4. Ekstrensek Apoptoz Yolağı (Ölüm Reseptörü Yolağı)
5. Kaspaz-8 (Ekstrensek Başlatıcı Kaspaz)
6. Kaspaz-9 (İntrensek Başlatıcı Kaspaz)
7. Kaspaz-3 (Majör Yürütücü / Efektör Kaspaz)
8. Apaptozom Kompleksi (Sitokrom c + Apaf-1)
9. c-FLIP Proteini (Kaspaz-8 İnhibitörü)
10. Smac / DIABLO (IAP İnhibitörü)
11. Perforin ve Granzim B Yolu (CTL Sitotoksisitesi)
12. Nekroptoz (Programlı Nekroz / RIPK1-RIPK3-MLKL)
13. Pyroptoz (Kaspaz-1 / İnflamazom Bağımlı Hücre Ölümü)
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ENCYCLOPEDIA_PATH = os.path.join('src', 'data', 'medical_encyclopedia.json')
GLOSSARY_PATH = os.path.join('src', 'data', 'medical_glossary.json')

with open(ENCYCLOPEDIA_PATH, 'r', encoding='utf-8') as f:
    encyclopedia = json.load(f)

# Update or insert detailed terms
detailed_terms = [
    {
        "id": "bax-proteini",
        "term": "Bax Proteini (Bcl-2 Associated X Protein)",
        "latinName": "Bax proteinum",
        "aliases": ["Bax", "Bcl-2-associated X", "Pro-apoptotik Bax"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Biyoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Hücre Hasarı ve Apoptoz / Robbins 11. Baskı)",
        "definition": "Pro-apoptotik Bcl-2 ailesi üyesi çoklu alanlı (BH1, BH2, BH3) ana efektör proteindir. Normal sağlıklı hücrede inaktif bir monomer olarak sitoplazmada veya mitokondri dış zarına gevşek bağlı halde bekler. DNA hasarı (p53 uyarımı), büyüme faktörü yoksunluğu veya hücresel stres durumunda aktive olan BH3-only proteinleri (Bid, Bim, Puma) tarafından aktive edilir.",
        "description": "Normalde sitozolde inaktif monomer olarak bulunan, p53 ve BH3-only sensörler ile uyarıldığında mitokondri dış zarına (MOM) göç edip oligomerleşerek sitokrom c salınım delikleri açan majör pro-apoptotik efektör protein.",
        "morphologyOrMechanism": "Aktivasyon Mekanizması: DNA hasarı ➔ p53 indüksiyonu ➔ Puma/Noxa artışı ➔ Sitozolik Bax'ın konformasyonel değişimi ➔ Mitokondri dış zarına insersiyon ➔ Oligomerizasyon (Bak ile veya homo-oligomer) ➔ Mitokondriyal Dış Zar Geçirgenleşmesi (MOMP) ➔ Sitokrom c ve Smac/DIABLO salınımı. İnhibisyon: Anti-apoptotik Bcl-2 ve Bcl-xL proteinleri Bax ile heterodimer oluşturarak oligomerizasyonu doğrudan bloke eder.",
        "differentialDiagnosis": "Bak proteini (normalde de mitokondri zarına gömülüdür, Bax ise sitozolden göç eder), Bcl-2 (anti-apoptotik antagonisti), Bim/Puma (aktivatör sensörler).",
        "examSpotPearls": "🔴 **Önemli (Spot Kural):** Bax normalde sitozolde serbest monomerdir; p53 tarafından indüklenen Puma/Noxa ile aktive olup mitokondri zarına gider. Anti-apoptotik Bcl-2 tarafından tutularak nötralize edilir.",
        "clinicalPearl": "Foliküler lenfomada t(14;18) translokasyonu sonucu aşırı üretilen Bcl-2, Bax proteinini sürekli heterodimer halinde tutarak apoptozu engeller ve neoplastik hücrelerin ölümsüzleşmesine yol açar.",
        "pitfallsAndWarnings": "Bax tek başına bir sensör değildir; doğrudan zar kanalını açan 'efektör' proteindir. Sensör olanlar BH3-only proteinleridir (Bad, Bim, Bid, Puma, Noxa).",
        "relatedItems": ["bak-proteini", "bcl-2-proteini", "intrensek-apoptoz-yolagi", "apaptozom"],
        "badgeColor": "rose",
        "aiAuditScore": 100
    },
    {
        "id": "bak-proteini",
        "term": "Bak Proteini (Bcl-2 Antagonist/Killer)",
        "latinName": "Bak proteinum",
        "aliases": ["Bak", "Bcl-2 homologous antagonist/killer"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Tıbbi Biyoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Hücre Hasarı ve Apoptoz / Robbins 11. Baskı)",
        "definition": "Pro-apoptotik Bcl-2 ailesi üyesi çoklu alanlı (BH1-BH3) efektör proteindir. Bax'tan en temel farkı, normal dinlenme halindeki hücrede de doğrudan mitokondri dış zarına (MOM) transmembran uzantısıyla entegre şekilde yerleşik bulunmasıdır.",
        "description": "Mitokondri dış zarına kalıcı olarak bağlı duran, normalde anti-apoptotik Mcl-1 ve Bcl-xL tarafından tutularak susturulan, ölüm sinyaliyle serbest kalıp oligomerleşerek zar gözeneği açan pro-apoptotik efektör protein.",
        "morphologyOrMechanism": "Aktivasyon Mekanizması: Normalde Mcl-1 ve Bcl-xL proteinleri Bak'a bağlanarak onu inaktif konformasyonda tutar. Hücre stres sinyali aldığında BH3-only proteinleri (özellikle Noxa ve Puma) Mcl-1 ve Bcl-xL'yi bağlayarak Bak'ı serbest bırakır. Serbest kalan Bak molekülleri kendi aralarında ve Bax ile oligomerize olarak mitokondri dış zarında porlar açar ve Sitokrom c çıkışını sağlar.",
        "differentialDiagnosis": "Bax proteini (sitozolik monomer iken Bak mitokondri zarına gömülüdür), Mcl-1 (Bak'ı zarda tutan primer anti-apoptotik protein).",
        "examSpotPearls": "🔴 **Önemli Ayrım:** Bax sitoplazmadan mitokondriye göç ederken; Bak zaten mitokondri dış zarında hazır bekler. Bak'ın primer susturucusu Mcl-1 ve Bcl-xL'dir.",
        "clinicalPearl": "Kemoterapiye dirençli tümörlerde hem Bax hem Bak gen delesyonu veya mutasyonu varsa mitokondriyal geçirgenlik açılamaz ve intrensek apoptoz tamamen felç olur.",
        "pitfallsAndWarnings": "Bax ve Bak çift nakavt (Bax-/- Bak-/-) hücreler intrensek apoptotik uyaranların hiçbirine yanıt veremez.",
        "relatedItems": ["bax-proteini", "bcl-2-proteini", "intrensek-apoptoz-yolagi"],
        "badgeColor": "rose",
        "aiAuditScore": 100
    },
    {
        "id": "intrensek-apoptoz-yolagi",
        "term": "İntrensek Apoptoz Yolağı (Mitokondriyal Yol)",
        "latinName": "Via apoptotica intrinseca / mitochondrialis",
        "aliases": ["Mitokondriyal Apoptoz Yolu", "İntrinsik Yol", "Bcl-2 Regüleli Apoptoz"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Apoptoz Mekanizmaları / Robbins 11. Baskı)",
        "definition": "Hücre içi kaynaklı stresler (DNA hasarı, p53 indüksiyonu, radyasyon, kemoterapi, büyüme faktörü yoksunluğu, ER stresi) sonucu tetiklenen majör programlı hücre ölümü yolağıdır. Temel olay mitokondri dış zar geçirgenliğinin (MOMP) artması ve zarlar arası aralıktaki pro-apoptotik proteinlerin sitozole boşalmasıdır.",
        "description": "DNA hasarı ve hücresel stresle tetiklenen, mitokondriden Sitokrom c salınımı, Apaf-1 ile apaptozom oluşumu ve başlatıcı Kaspaz-9 aktivasyonu ile yürütülen majör hücre içi apoptoz yolağı.",
        "morphologyOrMechanism": "Kaskad Sırası:\n1. Hasar Algılama: BH3-only sensörleri (Bim, Bid, Puma, Noxa) aktive olur.\n2. Frenlerin Kaldırılması: Sensörler anti-apoptotik Bcl-2, Bcl-xL ve Mcl-1'i inhibe eder.\n3. Efektör Aktivasyonu: Bax ve Bak oligomerize olarak mitokondri dış zarında por açar.\n4. Molekül Salınımı: Sitokrom c ve Smac/DIABLO sitozole sızar.\n5. Apaptozom Kurulumu: Sitokrom c sitoplazmada Apaf-1 ve dATP ile birleşerek 7 kollu tekerlek yapısında Apaptozom oluşturur.\n6. Kaspaz Kaskadı: Apaptozom Prokaspaz-9'u keserek başlatıcı Kaspaz-9'u aktive eder; Kaspaz-9 da efektör Kaspaz-3 ve Kaspaz-7'yi kesip hücreyi parçalar.",
        "differentialDiagnosis": "Ekstrensek Yol (Ölüm reseptörü / Fas / Kaspaz-8 bağımlıdır, mitokondri gerekmeyebilir).",
        "examSpotPearls": "🔴 **Önemli:** İntrensek yolun anahtar başlatıcı kaspazı ==Kaspaz-9==dur. 🔵 **Çıkmış Soru:** \"Mitokondriden sitozole çıkarak Apaf-1 ile birleşip apaptozomu kuran molekül hangisidir?\" → ==Sitokrom c==.",
        "clinicalPearl": "Bcl-2 aşırı ekspresyonu mitokondri zarını stabilize ederek Sitokrom c çıkışını bloke eder ve B-hücreli lenfomaların gelişmesine yol açar.",
        "pitfallsAndWarnings": "İntrensek yolda Fas veya TNF reseptörü rol oynamaz; tetikleyiciler tamamen hücre içi stres ve p53 sinyalleridir.",
        "relatedItems": ["bax-proteini", "bak-proteini", "kaspaz-9", "kaspaz-3", "apaptozom", "bcl-2-proteini"],
        "badgeColor": "teal",
        "aiAuditScore": 100
    },
    {
        "id": "ekstrensek-apoptoz-yolagi",
        "term": "Ekstrensek Apoptoz Yolağı (Ölüm Reseptörü Yolağı)",
        "latinName": "Via apoptotica extrinseca / receptoris mortis",
        "aliases": ["Ölüm Reseptörü Yolu", "Fas/FasL Yolağı", "Ekstrinsik Apoptoz"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / İmmünoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Apoptoz Mekanizmaları / Robbins 11. Baskı)",
        "definition": "Hücre zarında bulunan TNF reseptör süperailesi üyeleri olan 'Ölüm Reseptörleri'nin (Fas/CD95, TNFR1, TRAIL reseptörleri DR4/DR5) hücre dışından ligantlarıyla uyarılmasıyla başlayan programlı hücre ölümü yolağıdır. Sitotoksik T lenfositleri (CTL) ve NK hücreleri tarafından virüsle enfekte veya tümöral hücrelerin öldürülmesinde primer kullanılır.",
        "description": "Fas (CD95) veya TNFR1 ölüm reseptörlerinin ligantlarıyla trimerizasyonu, sitoplazmik FADD adaptörü ile DISC kompleksi kurulması ve başlatıcı Kaspaz-8 aktivasyonu ile yürütülen dış kaynaklı apoptoz yolağı.",
        "morphologyOrMechanism": "Kaskad Sırası:\n1. Ligant Bağlanması: CTL üzerindeki FasL (Fas Ligand), hedef hücredeki Fas (CD95) reseptörüne bağlanır.\n2. Trimerizasyon ve DD Kümeleşmesi: Reseptörler trimerize olur; sitoplazmik Ölüm Alanları (Death Domain - DD) bir araya gelir.\n3. DISC Kurulumu: FADD (Fas-Associated Death Domain) adaptör proteini DD bölgelerine tutunur ve Prokaspaz-8'i toplar (DISC kompleksi).\n4. Başlatıcı Aktivasyon: Prokaspaz-8 oto-proteolitik kesimle aktif ==Kaspaz-8==e dönüşür.\n5. İnfaz ve Çapraz Köprü: Kaspaz-8 doğrudan efektör Kaspaz-3'ü aktive eder; ayrıca Bid proteinini keserek tBid oluşturur ve intrensek mitokondriyal yolu da tetikleyerek ölüm sinyalini amplifiye eder.\n6. İnhibitör: FLIP proteini Kaspaz-8'e bağlanıp DISC aktivasyonunu engeller.",
        "differentialDiagnosis": "İntrensek Yol (Mitokondriyal / Kaspaz-9 bağımlı), Perforin-Granzim Yolu (Kaspaz-8 gerektirmeden Granzim B direkt Kaspaz-3'ü keser).",
        "examSpotPearls": "🔴 **Önemli:** Ekstrensek yolun başlatıcı enzimi ==Kaspaz-8==dir (ve Kaspaz-10). 🔵 **Çıkmış Soru:** \"Ekstrensek yol ile intrensek yol arasındaki köprüyü kuran, Kaspaz-8 tarafından kesilip mitokondriye giden BH3-only proteini hangisidir?\" → ==Bid (tBid)==.",
        "clinicalPearl": "Otoimmün Lenfoproliferatif Sendromda (ALPS) Fas veya FasL gen mutasyonu vardır; oto-reaktif T lenfositler apoptoza uğratılamaz ve lenfadenopati, splenomegali ile otoimmün sitopeniler gelişir.",
        "pitfallsAndWarnings": "FLIP proteini Kaspaz-8 benzeri bir yapıya sahiptir ancak katalitik aktivitesi yoktur; bu nedenle Kaspaz-8'i yarışmalı olarak bloke eden bir apoptoz frenidir.",
        "relatedItems": ["kaspaz-8", "kaspaz-3", "intrensek-apoptoz-yolagi", "flip-proteini"],
        "badgeColor": "rose",
        "aiAuditScore": 100
    },
    {
        "id": "kaspaz-8",
        "term": "Kaspaz-8 (Ekstrensek Başlatıcı Kaspaz)",
        "latinName": "Caspasum-8",
        "aliases": ["İnisiyatör Kaspaz-8", "FLICE", "Caspase-8"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Apoptoz / Robbins 11. Baskı)",
        "definition": "Ekstrensek (ölüm reseptörü) apoptoz yolağının kilit başlatıcı sisteinil aspartat-spesifik proteaz enzimidir. FADD adaptör proteini ile DISC kompleksinde bir araya gelerek prokaspaz formundan dimerizasyon ve oto-proteolizle aktif hale geçer.",
        "description": "Ölüm reseptörü uyarısıyla DISC kompleksinde aktifleşen, efektör Kaspaz-3'ü doğrudan kesen ve Bid'i tBid'e çevirerek intrensek yolu tetikleyen majör ekstrensek başlatıcı kaspaz.",
        "morphologyOrMechanism": "Aktivasyon: Fas/FADD etkileşimi ➔ Prokaspaz-8 DED (Death Effector Domain) aracılığıyla bağlanır ➔ DISC oluşumu ➔ İki prokaspaz molekülünün dimerizasyonu ➔ Karşılıklı proteolitik kesim ➔ Aktif Kaspaz-8 heterodimeri salınır. Hedefler: Kaspaz-3/7 (efektör infaz) ve Bid (tBid aktivasyonu).",
        "differentialDiagnosis": "Kaspaz-9 (intrensek başlatıcı), Kaspaz-3 (efektör/yürütücü), Kaspaz-1 (piroptoz/inflamazom kaspazı - apoptotik değildir!).",
        "examSpotPearls": "🔴 **Önemli:** Ekstrensek yolun primer başlatıcı kaspazıdır. Bid proteinini keserek iki apoptoz yolu arasında çapraz köprü kurar. c-FLIP tarafından bloke edilir.",
        "clinicalPearl": "Kaspaz-8 inhibe edildiğinde veya bloke olduğunda hücre ölümü durmaz; alternatif yol olan Nekroptoz (RIPK1/RIPK3/MLKL) devreye girer.",
        "relatedItems": ["ekstrensek-apoptoz-yolagi", "kaspaz-3", "flip-proteini", "nekroptoz"],
        "badgeColor": "rose",
        "aiAuditScore": 100
    },
    {
        "id": "kaspaz-9",
        "term": "Kaspaz-9 (İntrensek Başlatıcı Kaspaz)",
        "latinName": "Caspasum-9",
        "aliases": ["İnisiyatör Kaspaz-9", "Caspase-9"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Apoptoz / Robbins 11. Baskı)",
        "definition": "İntrensek (mitokondriyal) apoptoz yolağının anahtar başlatıcı proteazıdır. Mitokondriden sitozole çıkan Sitokrom c'nin Apaf-1 ve dATP ile birleşerek oluşturduğu Apaptozom kompleksinin CARD (Caspase Recruitment Domain) bölgesine tutunarak aktifleşir.",
        "description": "Mitokondriyal Sitokrom c ve Apaf-1'in kurduğu Apaptozom kompleksi üzerinde aktifleşerek efektör Kaspaz-3 ve Kaspaz-7'yi kesip infazı başlatan intrensek başlatıcı enzim.",
        "morphologyOrMechanism": "Prokaspaz-9 sitozolde inaktif monomerdir. Apaptozom çarkına CARD etkileşimiyle bağlandığında konformasyonel olarak dimerize olur ve tam proteolitik aktivite kazanır. Aktif Kaspaz-9 doğrudan yürütücü Kaspaz-3 zimojenini keserek aktif Kaspaz-3 tetrameri oluşturur.",
        "differentialDiagnosis": "Kaspaz-8 (ekstrensek yol başlatıcısı), Kaspaz-3 (efektör kaspaz).",
        "examSpotPearls": "🔴 **Önemli:** İntrensek (mitokondriyal) yolun başlatıcı enzimidir; Apaptozom kompleksi olmadan aktifleşemez.",
        "clinicalPearl": "IAP (İnhibitör of Apoptosis) proteinleri aktif Kaspaz-9'u tutarak bloke eder; mitokondriden çıkan Smac/DIABLO ise IAP'leri nötralize ederek Kaspaz-9'u serbest bırakır.",
        "relatedItems": ["intrensek-apoptoz-yolagi", "apaptozom", "kaspaz-3", "smac-diablo"],
        "badgeColor": "teal",
        "aiAuditScore": 100
    },
    {
        "id": "kaspaz-3",
        "term": "Kaspaz-3 (Majör Yürütücü / Efektör Kaspaz)",
        "latinName": "Caspasum-3",
        "aliases": ["Efektör Kaspaz-3", "İnfaz Kaspazı", "CPP32", "Caspase-3"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Apoptoz / Robbins 11. Baskı)",
        "definition": "Hem intrensek (Kaspaz-9 aracılı) hem ekstrensek (Kaspaz-8 aracılı) hem de Granzim B yollarının birleştiği nihai infazcı/yürütücü (executioner) sistein proteazdır. Başlatıcı kaspazlar tarafından kritik aspartat kalıntısından kesilerek aktif heterodimer formuna geçer.",
        "description": "Tüm apoptoz yollarının ortak infaz enzimidir; hücre iskeletini (aktin, lamin) parçalar ve ICAD'i keserek CAD endonükleazını serbest bırakıp DNA merdiven parçalanmasını (DNA laddering) gerçekleştirir.",
        "morphologyOrMechanism": "Hücresel İnfaz Hedefleri:\n1. ICAD (İnhibitor of Caspase-Activated DNase): Kaspaz-3 ICAD'i yıkar; serbest kalan aktif CAD nükleusa girip internükleozomal DNA'yı 180-200 baz çiftlik fragmanlara böler.\n2. Nükleer Laminler: Nükleer zar iskeletini yıkarak nükleer büzüşme ve piknoz yapar.\n3. Hücre İskeleti Proteinleri: Aktin, fodrin, tubulin parçalanarak hücre küçülür ve apoptotik cisimcikler tomurcuklanır.\n4. Flippaz/Skramblaz: Membran asimetrisini bozar; fosfatidilserin iç yapraktan dış yaprağa döner ('Eat me' sinyali).",
        "differentialDiagnosis": "Kaspaz-8 ve 9 (başlatıcıdır, infaz yapmazlar), Kaspaz-3/6/7 (efektör kaspazlar grubu).",
        "examSpotPearls": "🔴 **Önemli:** Apoptozda hücresel morfolojiyi ve DNA merdivenlenmesini oluşturan nihai infazcı ==Kaspaz-3==tür. 🔵 **Çıkmış Soru:** \"Apoptozun hem intrensek hem ekstrensek yolunda ortak olarak aktive edilen majör efektör kaspaz hangisidir?\" → ==Kaspaz-3==.",
        "clinicalPearl": "Doku kesitlerinde apoptozun immunohistokimyasal gösterilmesinde 'Aktif Kaspaz-3 (Cleaved Caspase-3)' boyaması altın standarttır.",
        "relatedItems": ["intrensek-apoptoz-yolagi", "ekstrensek-apoptoz-yolagi", "kaspaz-8", "kaspaz-9"],
        "badgeColor": "rose",
        "aiAuditScore": 100
    },
    {
        "id": "apaptozom",
        "term": "Apaptozom Kompleksi (Sitokrom c - Apaf-1 Tekerleği)",
        "latinName": "Apoptosomus",
        "aliases": ["Apoptosome", "Ölüm Tekerleği", "Apaf-1 / Sitokrom c Kompleksi"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Biyokimya",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Apoptoz / Robbins 11. Baskı)",
        "definition": "İntrensek apoptoz yolağında mitokondriden salınan Sitokrom c, sitoplazmik Apaf-1 (Apoptotic Protease Activating Factor-1) ve dATP moleküllerinin birleşmesiyle sitozolde kurulan 7 kollu simetrik tekerlek benzeri makromoleküler aktivasyon platformudur.",
        "description": "Sitokrom c, Apaf-1 ve dATP'nin oluşturduğu 7'li tekerlek kompleksi; CARD bölgeleriyle Prokaspaz-9'u toplayıp aktif Kaspaz-9 dimerlerine dönüştürür.",
        "morphologyOrMechanism": "Sitokrom c Apaf-1'e bağlanır ➔ dATP hidrolizi ile Apaf-1 konformasyonu açılır ➔ 7 adet Apaf-1/Sitokrom c birimi heptamerik çark oluşturur ➔ Merkezdeki CARD bölgelerine Prokaspaz-9 bağlanır ➔ Prokaspaz-9 aktifleşir.",
        "differentialDiagnosis": "DISC kompleksi (ekstrensek yolda zarda kurulur; Apaptozom ise intrensek yolda sitozolde kurulur).",
        "examSpotPearls": "🔴 **Önemli:** Apaptozom bileşenleri: ==Sitokrom c + Apaf-1 + dATP + Prokaspaz-9==dur.",
        "relatedItems": ["intrensek-apoptoz-yolagi", "kaspaz-9"],
        "badgeColor": "teal",
        "aiAuditScore": 100
    },
    {
        "id": "flip-proteini",
        "term": "c-FLIP Proteini (Kaspaz-8 İnhibitörü)",
        "latinName": "Protein c-FLIP",
        "aliases": ["FLIP", "Caspase-8 inhibitörü", "FLICE-inhibitory protein"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / İmmünoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Apoptoz / Robbins 11. Baskı)",
        "definition": "Ekstrensek apoptoz yolağında hücreleri aşırı ölüm reseptörü sinyaline karşı koruyan endojen inhibitör proteindir. Yapısal olarak Prokaspaz-8'e benzer ve FADD'ye bağlanabilir; ancak katalitik aktif sistein bölgesine sahip olmadığı için proteaz aktivitesi gösteremez.",
        "description": "DISC kompleksine bağlanarak Prokaspaz-8'in yerini alan ve Kaspaz-8 aktivasyonunu yarışmalı olarak bloke eden anti-apoptotik düzenleyici protein.",
        "morphologyOrMechanism": "Ölüm reseptörü uyarıldığında c-FLIP FADD'nin DED bölgesine Prokaspaz-8'den önce bağlanır. Böylece Prokaspaz-8 DISC'e tutunamaz, dimerize olamaz ve ekstrensek apoptoz durur.",
        "differentialDiagnosis": "IAP proteinleri (Kaspaz-9 ve Kaspaz-3'ü inhibe eder; c-FLIP ise Kaspaz-8'i inhibe eder).",
        "examSpotPearls": "🔴 **Önemli:** Bazı virüsler (özellikle Herpesvirüsler) v-FLIP üreterek konağın sitotoksik T lenfositleri tarafından apoptoza uğratılmasını engeller.",
        "relatedItems": ["ekstrensek-apoptoz-yolagi", "kaspaz-8"],
        "badgeColor": "amber",
        "aiAuditScore": 100
    },
    {
        "id": "smac-diablo",
        "term": "Smac / DIABLO Proteini (IAP İnhibitörü)",
        "latinName": "Smac / DIABLO",
        "aliases": ["Smac", "DIABLO", "IAP antagonisti"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / Moleküler Biyoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Apoptoz / Robbins 11. Baskı)",
        "definition": "Mitokondri zarlar arası boşlukta yerleşik pro-apoptotik proteindir. Bax/Bak kanalları açıldığında Sitokrom c ile eş zamanlı olarak sitoplazmaya sızar. Görevi sitoplazmada kaspazları baskılayan IAP (İnhibitor of Apoptosis) proteinlerini (XIAP, survivin vb.) bağlayarak nötralize etmektir.",
        "description": "Mitokondriden sitozole salınarak IAP proteinlerini bağlayan, böylece Kaspaz-9 ve Kaspaz-3'ün frenini kaldırarak apoptozun önünü açan mitokondriyal faktör.",
        "morphologyOrMechanism": "Mitokondri zarı geçirgenleşir ➔ Smac/DIABLO sitozole çıkar ➔ XIAP ve Survivin'in BIR domenine bağlanır ➔ IAP'ler Kaspaz-9/3'ü tutamaz ➔ Kaspaz kaskadı tam güçle çalışır.",
        "differentialDiagnosis": "Sitokrom c (apaptozom kurar), Smac/DIABLO (IAP'leri nötralize eder).",
        "examSpotPearls": "🔴 **Önemli:** Smac/DIABLO doğrudan kaspaz aktive etmez; kaspazların inhibitörü olan IAP'leri inhibe ederek dolaylı aktivasyon sağlar (inhibitörün inhibitörü).",
        "relatedItems": ["intrensek-apoptoz-yolagi", "kaspaz-9", "kaspaz-3"],
        "badgeColor": "teal",
        "aiAuditScore": 100
    },
    {
        "id": "perforin-ve-granzim-yolu",
        "term": "Perforin ve Granzim B Yolu (CTL Apoptozu)",
        "latinName": "Via perforini et granzymi B",
        "aliases": ["Granzim Yolağı", "CTL Sitotoksik Apoptozu", "Granül Ekzositoz Yolu"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / İmmünoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Hücre Ölümü / Robbins 11. Baskı)",
        "definition": "Sitotoksik CD8+ T lenfositleri (CTL) ve Doğal Öldürücü (NK) hücrelerin virüsle enfekte veya tümöral hedef hücreleri öldürmede kullandığı reseptörden bağımsız direkt granül ekzositoz yolağıdır.",
        "description": "Perforin hedef zarda delik açar, Granzim B içeri girerek başlatıcı kaspazlara ihtiyaç duymadan doğrudan efektör Kaspaz-3'ü keserek hedef hücreyi apoptoza sokar.",
        "morphologyOrMechanism": "CTL hedef hücreye sinaps yapar ➔ Granüller ekzositozla salınır ➔ ==Perforin== hedef hücre zarında polimerize olup gözenek açar ➔ ==Granzim B== sitoplazmaya girer ➔ Doğrudan Prokaspaz-3'ü keserek Kaspaz-3'ü aktive eder; ayrıca Bid'i keserek mitokondriyal yolu da tetikler.",
        "differentialDiagnosis": "Fas/FasL yolu (ölüm reseptörü gerektirir), Perforin-Granzim yolu (reseptörsüz doğrudan delip proteaz enjekte eder).",
        "examSpotPearls": "🔴 **Önemli:** Granzim B, Kaspaz-8 veya Kaspaz-9 gibi başlatıcı kaspazları beklemeden ==doğrudan Kaspaz-3'ü aktive edebilir==.",
        "relatedItems": ["kaspaz-3", "ekstrensek-apoptoz-yolagi"],
        "badgeColor": "purple",
        "aiAuditScore": 100
    },
    {
        "id": "nekroptoz",
        "term": "Nekroptoz (Programlı Nekroz)",
        "latinName": "Necroptosis",
        "aliases": ["Programlanmış Nekroz", "RIPK1-RIPK3 Bağımlı Hücre Ölümü", "Kaspaz-Bağımsız Hücre Ölümü"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Yeni Hücre Ölümü Formları / Robbins 11. Baskı)",
        "definition": "Mekanik olarak programlı (genetik sinyal kaskadına bağlı) ancak morfolojik olarak nekroza benzeyen (hücre şişmesi, plazma zarı parçalanması, organel lizisi ve yoğun enflamasyon) kaspaz-bağımsız hibrit bir hücre ölümü biçimidir.",
        "description": "TNFR1 uyarısıyla Kaspaz-8 bloke olduğunda devreye giren, RIPK1 ve RIPK3 kinazlarının MLKL'yi fosforilleyip plazma zarını patlatmasıyla oluşan enflamatuar programlı hücre ölümü.",
        "morphologyOrMechanism": "Tetiklenme: TNF-TNFR1 bağlanması ➔ Kaspaz-8 inhibe ise (örn. viral enfeksiyonlarda) apoptoz gerçekleşemez ➔ RIPK1 ve RIPK3 kinazları bir araya gelerek 'Nekrozom' kompleksini kurar ➔ RIPK3 ==MLKL (Mixed Lineage Kinase Domain-Like)== proteinini fosforiller ➔ Fosforile MLKL plazma zarına göç edip zarı deler ➔ Hücre lizisi ve DAMP salınımı ile şiddetli yangı başlar.",
        "differentialDiagnosis": "Apoptoz (kaspaz bağımlı, membran sağlam, enflamasyon yok), Nekroz (tamamen pasif patolojik hasar), Nekroptoz (programlı genetik kaskat ama membran patlar ve yangı olur).",
        "examSpotPearls": "🔴 **Önemli:** Nekroptoz ==kaspaz-bağımsızdır==; RIPK1, RIPK3 ve MLKL proteinleri tarafından yürütülür. Apoptozun aksine plazma zarı yırtılır ve şiddetli enflamasyona yol açar.",
        "clinicalPearl": "Akut pankreatit, miyokardiyal iskemi-reperfüzyon hasarı ve viral enfeksiyonlarda doku nekrozunun temel mekanizması nekroptozdur.",
        "relatedItems": ["apoptoz", "kaspaz-8", "pyroptoz"],
        "badgeColor": "amber",
        "aiAuditScore": 100
    },
    {
        "id": "pyroptoz",
        "term": "Pyroptoz (İnflamazom / Kaspaz-1 Bağımlı Hücre Ölümü)",
        "latinName": "Pyroptosis",
        "aliases": ["Ateşli Hücre Ölümü", "Kaspaz-1 / Gasdermin D Hücre Ölümü"],
        "category": "patoloji",
        "kurul": "Kurul 1",
        "discipline": "Tıbbi Patoloji / İmmünoloji",
        "instructorAndSource": "Prof. Dr. Hikmet Keleş (Hücre Ölümü Tipleri / Robbins 11. Baskı)",
        "definition": "Hücre içi patojenlerle (Salmonella, Shigella, Legionella) enfekte makrofaj veya dendritik hücrelerde inflamazom kompleksi aktivasyonu sonucu gelişen, ateş ve yoğun enflamasyonla karakterize programlı hücre ölümü formudur ('Pyro' = ateş).",
        "description": "İnflamazom uyarısıyla aktifleşen Kaspaz-1'in IL-1β ve IL-18 salgılatıp Gasdermin D proteinini keserek hücre zarında porlar açmasıyla gelişen yangısal hücre ölümü.",
        "morphologyOrMechanism": "PAMP/DAMP ➔ NLRP3 İnflamazom aktivasyonu ➔ ==Kaspaz-1 (veya Kaspaz-4/5/11)== aktivasyonu ➔ 1) Pro-IL-1β ve pro-IL-18 kesilip aktif salınır (ateş ve yangı), 2) ==Gasdermin D== kesilir ve N-terminal parçası plazma zarında porlar açar ➔ Hücre şişip patlar.",
        "differentialDiagnosis": "Apoptoz (Kaspaz-3 bağımlı, sessiz ölüm), Pyroptoz (Kaspaz-1 bağımlı, Gasdermin D porlu, IL-1 salınımlı ateşli ölüm).",
        "examSpotPearls": "🔴 **Önemli:** Pyroptozun ana enzimi ==Kaspaz-1==, zarı patlatan por proteini ise ==Gasdermin D==dir.",
        "clinicalPearl": "Sepsis ve septik şok patogenezinde aşırı sitokin fırtınası ve lökosit kaybında pyroptoz başroldedir.",
        "relatedItems": ["nekroptoz", "apoptoz"],
        "badgeColor": "rose",
        "aiAuditScore": 100
    }
]

enc_map = {e['id']: i for i, e in enumerate(encyclopedia)}
added_count = 0
updated_count = 0

for item in detailed_terms:
    iid = item['id']
    if iid in enc_map:
        encyclopedia[enc_map[iid]].update(item)
        updated_count += 1
    else:
        encyclopedia.append(item)
        enc_map[iid] = len(encyclopedia) - 1
        added_count += 1

with open(ENCYCLOPEDIA_PATH, 'w', encoding='utf-8') as f:
    json.dump(encyclopedia, f, ensure_ascii=False, indent=2)

print(f"✓ Encyclopedia updated: Total {len(encyclopedia)} entries (Added: {added_count}, Updated: {updated_count})")

# Update glossary as well
with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
    glossary = json.load(f)

for item in detailed_terms:
    term_key = item['term'].lower()
    clean_key = item['term'].split('(')[0].strip().lower()
    
    entry_val = {
        "term": item['term'],
        "category": item.get('category', 'patoloji'),
        "description": item.get('description') or item.get('definition', ''),
        "clinicalPearl": item.get('clinicalPearl') or item.get('examSpotPearls', ''),
        "discipline": item.get('discipline', ''),
        "committee": item.get('kurul', '')
    }
    glossary[term_key] = entry_val
    if clean_key and clean_key != term_key:
        glossary[clean_key] = entry_val

with open(GLOSSARY_PATH, 'w', encoding='utf-8') as f:
    json.dump(glossary, f, ensure_ascii=False, indent=2)

print(f"✓ Glossary synchronized: Total {len(glossary)} active key terms!")
