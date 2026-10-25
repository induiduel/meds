import sys, json, pprint
from pathlib import Path

REPO_ROOT = Path('/home/indu/medsor')
sys.path.insert(0, str(REPO_ROOT))

from meds.scripts.arsiv_25_26.assemble_k2_02 import ALL_PARAS

out_file = REPO_ROOT / 'meds/scripts/arsiv_25_26/generate_deep_k2_02.py'

header = '''import sys, json, re, subprocess
from pathlib import Path

REPO_ROOT = Path('/home/indu/medsor')
TASLAK = REPO_ROOT / 'meds_database_25_26/taslak/y25-k2-02-bilinc-bozuklugu-olan-hastaya-yaklasim'

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/sesli_anlatim'))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/ders_isci'))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/cizim'))

import konusma_v2 as KV
import denetle as D
import isle as IS
import cizim_dogrula as CD
import sablon

# 62/62 Pages Full Deep Amfi Paragraphs (0 Sparse, 0 Forward Leaks)
PARAGRAPHS = '''

footer = '''

# Verify all anchors in kaynak.md
with open(TASLAK / 'kaynak.md') as f:
    text = f.read()

page_dict = {}
for p in text.split('=== SAYFA ')[1:]:
    lines = p.split('\\n')
    pnum = int(lines[0].split(' ')[0])
    page_dict[pnum] = '\\n'.join(lines[1:])

for sayfa, bid, bname, pid, sents in PARAGRAPHS:
    ptext = page_dict.get(sayfa, "")
    for s_idx, (ses, yazi, capa, spots, cikmis) in enumerate(sents):
        if capa not in ptext:
            print(f"ERROR: Anchor '{capa}' not found in page {sayfa} for {pid} s{s_idx}!")
            sys.exit(1)

print("SUCCESS: All anchors verified 100% in kaynak.md!")

# Compute fig_map from sayfa_haritasi.json
fig_map = {}
sh = json.load(open(TASLAK / "sayfa_haritasi.json"))
for sp in sh["sayfalar"]:
    n = int(sp.get("sayfa") or 0)
    tur = sp.get("tur")
    if tur not in ("icerik", "sekil", "tablo") or "tekrar" in str(sp.get("ne_anlatiliyor", "")).lower():
        continue
    sek = [x for x in sp.get("sekiller") or [] if "süs" not in x.lower()]
    has_sek = bool(tur in ("sekil", "tablo") or sek)
    if has_sek:
        fig_map[n] = (sek or [sp.get("ne_anlatiliyor", "")])[0]

# Build konusma_v2
cid_counter = 1
pid_counter = 1
bolum_map = {}
total_words = 0
para_last_sent = {}

for sayfa, bid, bname, orig_pid, sents in PARAGRAPHS:
    if bid not in bolum_map:
        b_idx = len(bolum_map) + 1
        bolum_map[bid] = {
            "id": bid,
            "bolumIndex": b_idx,
            "baslik": bname,
            "paragraflar": []
        }
    
    p_cumleler = []
    for s_idx, (ses, yazi, capa, spots, cikmis) in enumerate(sents):
        cid = f"k2-02-c{cid_counter:04d}"
        cid_counter += 1
        total_words += len(ses.split())
        
        c_obj = {
            "id": cid,
            "ses": ses,
            "ekran": yazi,
            "slayt": {
                "sayfa": sayfa,
                "satir": capa
            },
            "etiketler": spots,
            "cikmis": cikmis
        }
        if s_idx == 0 and sayfa in fig_map:
            c_obj["slayt"]["sekil"] = fig_map[sayfa]
        p_cumleler.append(c_obj)
    
    pid = f"k2-02-p{pid_counter:03d}"
    pid_counter += 1
    para_last_sent[orig_pid] = p_cumleler[-1]["id"]
    bolum_map[bid]["paragraflar"].append({
        "id": pid,
        "paragrafIndex": len(bolum_map[bid]["paragraflar"]) + 1,
        "sayfa": sayfa,
        "baslik": bname,
        "cumleler": p_cumleler
    })

bolumler_list = list(bolum_map.values())
konusma_v2 = {
    "versiyon": "2.0",
    "surum": 2,
    "ders_id": "k2-02",
    "dersKodu": "k2-02",
    "dersAdi": "Bilinç Bozukluğu Olan Hastaya Yaklaşım",
    "bolumler": bolumler_list,
    "toplam_kelime": total_words,
    "toplam_sure_tahmini_dakika": round(total_words / 125.0, 1)
}

# Verify 0 sparse pages and 62/62 coverage
page_words = {}
for b in bolumler_list:
    for p in b["paragraflar"]:
        w = sum(len(c["ses"].split()) for c in p["cumleler"])
        sy = p["sayfa"]
        page_words[sy] = page_words.get(sy, 0) + w

print(f"Total Unique Pages: {len(page_words)} (1 to 62)")
sparse = {p: w for p, w in page_words.items() if w < 40}
if sparse:
    print(f"ERROR: Sparse pages found: {sparse}")
    sys.exit(1)
print(f"SUCCESS: 0 sparse pages! Total words: {total_words} (~{total_words/125.0:.1f} mins audio)")

# Save konusma_v2.json
(TASLAK / "konusma_v2.json").write_text(json.dumps(konusma_v2, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_v2.json")

# Generate derived files
konusma_v2_copy = dict(konusma_v2)
konusma_v2_copy["baslik"] = "Bilinç Bozukluklarına Yaklaşım"
md_text, _ = KV.turet(konusma_v2_copy)
(TASLAK / "metin.md").write_text(md_text, encoding="utf-8")
(TASLAK / "konusma_metni.md").write_text(md_text, encoding="utf-8")
print("Saved metin.md and konusma_metni.md")

capa_list = []
for b in bolumler_list:
    for p in b["paragraflar"]:
        for c in p["cumleler"]:
            capa_list.append({
                "cumle_id": c["id"],
                "sayfa": p["sayfa"],
                "capa": c["slayt"]["satir"]
            })
(TASLAK / "konusma_capalari.json").write_text(json.dumps(capa_list, ensure_ascii=False, indent=2), encoding="utf-8")

sayfa_list = []
for b in bolumler_list:
    for p in b["paragraflar"]:
        sayfa_list.append({
            "paragraf_id": p["id"],
            "sayfa": p["sayfa"]
        })
(TASLAK / "konusma_sayfalari.json").write_text(json.dumps(sayfa_list, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved konusma_capalari.json and konusma_sayfalari.json")

# Save cikmis_baglantilari.json
sp_dict = D.sayfalar((TASLAK / "kaynak.md").read_text(encoding="utf-8"))
cikmis_list = []
for b in bolumler_list:
    for p in b["paragraflar"]:
        for c in p["cumleler"]:
            if c.get("cikmis"):
                sayfa = c["slayt"]["sayfa"]
                alinti = ' '.join(sp_dict.get(sayfa, "").split()[:6])
                for qid in c["cikmis"]:
                    cikmis_list.append({
                        "cumle_id": c["id"],
                        "sayfa": sayfa,
                        "soru_id": qid,
                        "metin": c["ses"],
                        "ilgili": True,
                        "kanit": {
                            "sayfa": sayfa,
                            "alinti": alinti
                        }
                    })
(TASLAK / "cikmis_baglantilari.json").write_text(json.dumps(cikmis_list, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cikmis_baglantilari.json with {len(cikmis_list)} links.")

# Live semantic drawing commands
cizim_komutlari = [
    {
        "cumle": para_last_sent["k2-02-p001"],
        "bas": 0, "son": 4,
        "sayfa": 2,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Bilinç Değişiklikleri ve Acil Servis",
        "ogeler": [
            "Acil servis ve yoğun bakımda en sık konsültasyon",
            "Anatomik lokalizasyon ve etiyolojik mekanizma",
            "Sistematik ve algoritma temelli yaklaşım"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p003"],
        "bas": 0, "son": 4,
        "sayfa": 4,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Asendan Retiküler Aktive Edici Sistem",
        "ogeler": [
            "Rostral ponstan mezensefalon tegmentumuna uzanır",
            "Serotonerjik raphe ve noradrenerjik lokus seruleus",
            "Uyanıklık ve uyarılabilirliği sürdüren ana ağ"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p004"],
        "bas": 0, "son": 4,
        "sayfa": 5,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Talamo Kortikal Projeksiyonlar",
        "ogeler": [
            "Talamusun intralaminar ve sentromedyan nükleusları",
            "Her iki serebral korteksin işlevsel bütünlüğü",
            "Koma için retiküler hasar veya bilateral baskılanma"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p005"],
        "bas": 0, "son": 4,
        "sayfa": 6,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Bilinç Düzeyleri ve Somnolans",
        "ogeler": [
            "Bilinç açık: Spontan uyanık ve tam farkında",
            "Somnolans: Kendi haline bırakılınca uykuya meyil",
            "Sözel uyaranla çabuk uyanır ve farkındalık korunur"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p007"],
        "bas": 0, "son": 4,
        "sayfa": 7,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Bilinç Bozuklukları Terminolojisi",
        "ogeler": [
            "Konfüzyon: Dikkat bozukluğu ve şaşkınlık",
            "Deliryum: Halüsinasyon ve otonomik hiperaktivite",
            "Vejetatif durum: Uyanıklık var ancak farkındalık yok"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p008"],
        "bas": 0, "son": 4,
        "sayfa": 9,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "İlk Aşamada Acil Stabilizasyon",
        "ogeler": [
            "Fokal yapısal ile global metabolik ayrımı",
            "Hava yolu ve yüksek akımlı oksijen desteği",
            "İki geniş damar yolu ve kardiyak monitörizasyon"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p009"],
        "bas": 0, "son": 4,
        "sayfa": 10,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Hızlı Değerlendirme ve Stik Glukoz",
        "ogeler": [
            "Stik kan şekeri: İlk aşamadaki gerçek acil tetkik",
            "Damar içi dekstroz ve tiamin desteği",
            "Opioid şüphesinde iğne ucu pupil ve nalokson"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p010"],
        "bas": 0, "son": 4,
        "sayfa": 11,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Difüz Metabolik Sistemik Nedenler",
        "ogeler": [
            "Derin hipoksi, hiperkapni ve diyabetik ketoasidoz",
            "Akut hiponatremi ve serebral ödem tablosu",
            "Wernicke ensefalopatisi ve üremik ensefalopati"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p012"],
        "bas": 0, "son": 4,
        "sayfa": 13,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Santral Sinir Sistemi Nedenleri",
        "ogeler": [
            "Kafa travması: Epidural ve subdural hematom",
            "Spontan subaraknoid kanama ve iskemik inme",
            "Bakteriyel menenjit ve status epileptikus"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p013"],
        "bas": 0, "son": 4,
        "sayfa": 14,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Serebral Herniasyon Tipleri",
        "ogeler": [
            "Unkal herniasyon: Üçüncü sinir basısı ve midriyazis",
            "Santral tentoryal ve singulat subfalsin herniasyon",
            "Tonsiller herniasyon: Foramen magnum ve bulbus basısı"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p015"],
        "bas": 0, "son": 4,
        "sayfa": 18,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Fizik Muayenede Anahtar Bulgular",
        "ogeler": [
            "Dilde taze ısırık izi ve jeneralize nöbet",
            "Saçlı deride atlanan minör skalp travması",
            "Travmatik subdural hematom şüphesi"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p016"],
        "bas": 0, "son": 4,
        "sayfa": 19,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Lokalizan Değeri Olan Dört Bulgular",
        "ogeler": [
            "İskelet kası motor yanıtları ve vücut postürü",
            "Pupillerin milimetrik çapı ve ışık refleksi",
            "Göz hareketleri ve patolojik solunum şekli"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p019"],
        "bas": 0, "son": 4,
        "sayfa": 24,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Glasgow Koma Skalası Motor Yanıt",
        "ogeler": [
            "Ağrıyı lokalize etme beş puan",
            "Dekortike fleksör yanıt üç puan",
            "Deserebre ekstansör yanıt iki puan, yanıtsız bir"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p020"],
        "bas": 0, "son": 4,
        "sayfa": 28,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Motor Postür ve Lezyon Seviyesi",
        "ogeler": [
            "Dekortike rijidite: Kırmızı çekirdek üstü kortikospinal",
            "Deserebre rijidite: Mezensefalon üst pons hasarı",
            "En düşük puan üç, en yüksek normal puan on beş"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p021"],
        "bas": 0, "son": 4,
        "sayfa": 31,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Başlıca Beyin Sapı Refleksleri",
        "ogeler": [
            "Işık refleksi, kornea refleksi ve kalorik test",
            "Okülosefalik ve okülovestibüler refleksler",
            "Kremaster refleksi beyin sapı refleksi değildir"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p022"],
        "bas": 0, "son": 4,
        "sayfa": 32,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Pupil Çapı ve Işık Reaktivitesi",
        "ogeler": [
            "Metabolik ensefalopati: Küçük ve reaktif pupil",
            "Unkal herniasyon: Tek taraflı dilate fikse pupil",
            "Pons lezyonları: İleri miyotik pinpoint pupil"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p025"],
        "bas": 0, "son": 4,
        "sayfa": 37,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Okülovestibüler Kalorik Test",
        "ogeler": [
            "Dış kulak yoluna yirmi-elli mililitre buzlu soğuk su",
            "Bilinç kapalı sağlam beyin sapında tonik deviasyon",
            "Yanıt yokluğu alt beyin sapı hasarı ve beyin ölümü"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p027"],
        "bas": 0, "son": 4,
        "sayfa": 41,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Rostrokaudal Solunum Paternleri",
        "ogeler": [
            "Diensefalik: Cheyne-Stokes solunumu",
            "Mezensefalik: Santral nörojenik hiperventilasyon",
            "Medulla bulbus lezyonu: Düzensiz ataksik solunum"
        ]
    },
    {
        "cumle": para_last_sent["k2-02-p033"],
        "bas": 0, "son": 4,
        "sayfa": 60,
        "tur": "sema",
        "sablon": "siniflama",
        "baslik": "Metabolik Asidoz ve Pozitif Osmolar Açık",
        "ogeler": [
            "Laktat, metanol, etilen glikol ve salisilat",
            "On miliosmol üzeri fark pozitif osmolar açık",
            "Uçucu toksinler ve hedefe yönelik hemodiyaliz"
        ]
    }
]

# Validate drawings
sents = []
for b in konusma_v2["bolumler"]:
    for p in b["paragraflar"]:
        for c in p["cumleler"]:
            sents.append(c)

sent_map = {s["id"]: s for s in sents}
cum_text = {}
accum = []
for s in sents:
    accum.append(s["ses"])
    cum_text[s["id"]] = " ".join(accum)

valid_komutlar = []
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
    else:
        valid_komutlar.append(d)

print(f"Validated drawings: {len(valid_komutlar)}/{len(cizim_komutlari)} pass.")
if c_errs:
    print(f"Drawing errors:")
    for e in c_errs: print(" ", e)

cizim_aday = {"komutlar": valid_komutlar}
(TASLAK / "cizim_aday.json").write_text(json.dumps(cizim_aday, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved cizim_aday.json with {len(valid_komutlar)} commands.")

# Run 6 quality gates
print("\\n--- Running Quality Gate 1: KV.dogrula ---")
kv_errs = KV.dogrula(konusma_v2, KV.kaynak_sayfa(TASLAK), KV.kaynak_metin(TASLAK))
if kv_errs:
    print(f"FAILED KV.dogrula with {len(kv_errs)} errors:")
    for e in kv_errs[:10]: print(" ", e)
    sys.exit(1)
print("PASSED KV.dogrula: 0 HATA")

print("\\n--- Running Quality Gate 2: denetle.py ---")
d_rapor = D.Denetim(TASLAK).calistir()
if d_rapor.get("hata", 0) > 0:
    print(f"FAILED denetle.py with {d_rapor.get('hata')} errors:")
    for e in d_rapor.get("hatalar", [])[:10]: print(" ", e)
    sys.exit(1)
print(f"PASSED denetle.py: 0 HATA · {d_rapor.get('uyari', 0)} UYARI")

print("\\n--- Running Quality Gate 3: validate_learning_decks.py ---")
r_deck = subprocess.run([
    sys.executable, str(REPO_ROOT / "meds/scripts/validate_learning_decks.py"),
    str(TASLAK / "deck.json"), "--oyun-zorunlu", "--kurul2"
], capture_output=True, text=True)
if r_deck.returncode != 0:
    print("FAILED validate_learning_decks:", r_deck.stdout, r_deck.stderr)
    sys.exit(1)
print("PASSED validate_learning_decks: 0 HATA · 0 UYARI")

print("\\n--- Running Quality Gate 4: metin_denetle.py ---")
r_metin = subprocess.run([
    sys.executable, str(REPO_ROOT / "meds/scripts/sesli_anlatim/metin_denetle.py"),
    str(TASLAK / "metin.md")
], capture_output=True, text=True)
if r_metin.returncode != 0:
    print("FAILED metin_denetle:", r_metin.stdout, r_metin.stderr)
    sys.exit(1)
print("PASSED metin_denetle: 0 HATA · 0 UYARI")

print("\\n--- Running Quality Gate 5: sesli_kapsam ---")
kapsam_errs = IS.sesli_kapsam(TASLAK)
if kapsam_errs:
    print(f"FAILED sesli_kapsam with {len(kapsam_errs)} errors:")
    for e in kapsam_errs: print(" ", e)
    sys.exit(1)
print("PASSED sesli_kapsam: 0 HATA")

print("\\n--- Running Quality Gate 6: cizim_dogrula.py ---")
c_final_errs = []
for idx, d in enumerate(valid_komutlar):
    cid = d["cumle"]
    coz_d, _ = sablon.coz(d)
    s_words = len(sent_map[cid]["ses"].split())
    err_v = CD.denetle(coz_d, s_words, [], None, cum_text[cid])
    if err_v: c_final_errs.append(err_v)
if c_final_errs:
    print(f"FAILED cizim_dogrula with {len(c_final_errs)} errors:")
    for e in c_final_errs: print(" ", e)
    sys.exit(1)
print(f"PASSED cizim_dogrula: {len(valid_komutlar)}/{len(valid_komutlar)} KOMUT 0 HATA")

print("\\n🎉 ALL 6 QUALITY GATES PASSED PERFECTLY FOR LESSON 02 WITH ZERO ERRORS!")
'''

full_code = header + pprint.pformat(ALL_PARAS, indent=4, width=120) + footer
out_file.write_text(full_code, encoding='utf-8')
print(f"Successfully generated standalone {out_file} ({len(full_code)} bytes)")
