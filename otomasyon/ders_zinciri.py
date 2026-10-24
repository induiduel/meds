#!/usr/bin/env python3
"""Ders zinciri (Kurul 2+): yayımlanmış her ders paketi için spot/önem → soru çözücü → denetim → birleştirme →
sesli asistan → EMA ses → Oracle. Ders listesi src/data/dersler/k<N>.json (ders kayıt defteri); ders işçisinin
yayımladığı paket yayin_kaydi.json'dan bulunur (ders_id = <defter id>-<slug>).

Her adım kapı ile biter (0 HATA değilse ders o adımda kalır, sonraki gece yeniden dener; sessiz geçiş yok).
Durum: meds_temp/hat/dersler/<ders id>.json → {kaynak_sha, adimlar: {adim: {zaman, kod, not}}}. Kaynak (kaynak.md)
değişirse zincir baştan çalışır. LLM adımları Claude (claude -p) ile; önem/çözücü adımları otomasyon/llm/gorevler.json `mod`
alanına göre görev yoluyla (aktif) ya da Claude + gölge görev (golge) — R4, 2026-10-23.

Branş klasörü kurul öneklidir: meds_temp/spot_cozucu/k<N><brans>/ (ör. k2noroloji) — Kurul 1 klasörleri ezilmez.
Kodlar defterden (2n03): kurullar ve branşlar arası tekil.

  ders_zinciri.py --durum [--kurul 2]                 hangi ders hangi adımda
  ders_zinciri.py --kurul 2 [--ders k2-07] [--adim hazirla] [--kuru]
"""
import argparse, datetime as dt, hashlib, json, os, re, shutil, subprocess, sys
from collections import defaultdict
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
SC = MEDS / "scripts/spot_cozucu"
W0 = KOK / "meds_temp/spot_cozucu"
DURUM = KOK / "meds_temp/hat/dersler"
sys.path.insert(0, str(SC))
import aday_hazirla as AH  # noqa: E402  gizli_silinen, aday, grupla, ornek_hedefi, norm

BRANS_SLUG = {b["ad"]: b["slug"] for b in json.loads((MEDS / "src/data/dersler/branslar.json").read_text())["branslar"]}  # tek kaynak
ADIMLAR = ["hazirla", "onem", "cozucu", "denetim", "birlestir", "asistan", "ses", "oracle", "capa", "cizim"]
IZIN = "Read,Write,Edit,Glob,Grep,Bash(python3 *),Bash(curl -s http://127.0.0.1:3000/*)"


def brans_klasoru(d):
    return f"k{d['kurul']}{BRANS_SLUG.get(d['brans'], AH.norm(d['brans']).replace(' ', ''))}"


def yayinlar():
    """Yayımlanmış ders paketleri. Asıl kayıt Oracle'dadır (ders işçisi orada yayınlar): SSH ile salt-okunur çekilir;
    ulaşılamazsa cihaz kopyası (yayinla.py --esitle günceller). --esitle commit attığı için gece işinde çağrılmaz."""
    yerel = MEDS / "scripts/ders_isci/yayin_kaydi.json"
    try:
        r = subprocess.run(["ssh", "-o", "ConnectTimeout=15", "-o", "BatchMode=yes", "medsor-oracle",
                            "cat /home/ubuntu/medsor/ders_isci/yayin_kaydi.json"], capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout.strip().startswith("["):
            return json.loads(r.stdout)
        print("   uyarı: Oracle yayın kaydı okunamadı, cihaz kopyası kullanılıyor:", r.stderr.strip()[:160])
    except (subprocess.TimeoutExpired, ValueError) as e:
        print("   uyarı: Oracle yayın kaydı okunamadı:", e)
    return json.loads(yerel.read_text()) if yerel.exists() else []


def kaynak_getir(pk):
    """Paketin kaynak.md'si cihazda yoksa Oracle'dan (aynı göreli yol) çekilir."""
    p = KOK / pk["kaynak_md"]
    if not p.exists() or not (p.parent / "sayfalar.json").exists():
        # yayımlanan taslağın tamamı: kaynak.md + sayfalar.json + sayfa_goruntu/ (yazar Claude görselleri de okur)
        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rsync", "-az", f"medsor-oracle:/home/ubuntu/medsor/{Path(pk['kaynak_md']).parent}/", f"{p.parent}/"],
                       timeout=300)
    return p


def paket_bul(d, kayit):
    adaylar = [y for y in kayit if y.get("kurul") == d["kurul"] and str(y.get("ders_id", "")).startswith(d["id"] + "-")]
    return max(adaylar, key=lambda y: y.get("yayin_zamani") or "", default=None)


def durum_oku(d):
    p = DURUM / f"{d['id']}.json"
    return json.loads(p.read_text()) if p.exists() else {"adimlar": {}}


def durum_yaz(d, s):
    DURUM.mkdir(parents=True, exist_ok=True)
    (DURUM / f"{d['id']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1))


def calistir(komut, cwd=KOK, kuru=False):
    print("   $", komut if isinstance(komut, str) else " ".join(komut))
    if kuru:
        return 0
    r = subprocess.run(komut, shell=isinstance(komut, str), cwd=cwd, env={**os.environ, "CUDA_VISIBLE_DEVICES": ""})
    return r.returncode


def claude(istem, W, kuru):
    kom = ["claude", "-p", istem, "--model", "claude-opus-5-5", "--allowedTools", IZIN, "--add-dir", str(KOK)]
    print("   $ claude -p …", istem[:120])
    if kuru:
        return 0
    with open(W / "claude.log", "a") as log:
        log.write(f"\n=== {dt.datetime.now().isoformat(timespec='seconds')} ===\n{istem}\n")
        try:  # takılan oturum gecenin tamamını yemesin
            return subprocess.run(kom, cwd=W, stdout=log, stderr=subprocess.STDOUT, timeout=3 * 3600).returncode
        except subprocess.TimeoutExpired:
            log.write("\n!!! claude zaman aşımı (3 sa)\n"); return 124


def kapili_claude(istem, kapi, W, kuru, tur=3):
    """Claude yazar → kapı; HATA varsa aynı oturum dışı düzeltme turu (en çok `tur`)."""
    claude(istem, W, kuru)
    for i in range(tur):
        if calistir(kapi, kuru=kuru) == 0:
            return 0
        claude(f"Bu kapı HATA verdi: `{kapi}`. Komutu çalıştır, hataların hepsini düzelt (yalnız bu dersin dosyaları), "
               f"sonra kapıyı yeniden çalıştırıp 0 HATA olduğunu doğrula.", W, kuru)
    return calistir(kapi, kuru=kuru)


# ── adımlar ────────────────────────────────────────────────────────────────────────────────────────────────────────
def _konu_kati(k):
    """Konu adı yazım farkları ("Gebelik Terminolojisi/Kavramları" ↔ "Gebelik Terminolojisi ve Kavramları"): /, &, "ve",
    noktalama ve boşluk yok sayılır."""
    k = AH.norm(k or "")
    k = re.sub(r"\s*(/|&|\+|,|-|–)\s*", " ve ", k)
    return re.sub(r"[^0-9a-zçğıöşü ]+", " ", re.sub(r"\bve\b", " ", k)).split()


def konu_eslesen_cikmislar(Q, d, hedef_konu, gizli, silinen):
    """Dersin çıkmışları: önce müfredat konusu BİREBİR, tutmazsa yazım farkı yok sayılarak, o da tutmazsa ≥0,92 benzerlik.
    (2026-10-23 prova: birebir eşleme "/" ↔ "ve" farkı yüzünden dersi sessizce çıkmışsız bırakıyordu.)"""
    import difflib
    adaylar = []
    for q in Q:
        m = (q.get("checkSolve") or {}).get("mufredat") or {}
        if m.get("kurul") == d.get("cikmis_kurul", d["kurul"]) and m.get("ders") == d["brans"]:
            adaylar.append((q, m.get("konu")))
    hedef_kat = [_konu_kati(k) for k in hedef_konu]
    for yol, uyar in (("birebir", lambda k: AH.norm(k) in hedef_konu),
                      ("yazım farkı yok sayılarak", lambda k: _konu_kati(k) in hedef_kat),
                      ("benzerlik ≥0,92", lambda k: any(difflib.SequenceMatcher(None, " ".join(_konu_kati(k)), " ".join(h)).ratio()
                                                        >= 0.92 for h in hedef_kat))):
        L = [c for q, k in adaylar if k and uyar(k) for c in [AH.aday(q, gizli, silinen)] if c]
        if L:
            return L, yol
    return [], "yok"


def a_hazirla(d, pk, W, kuru):
    """pdf_metin + pdf_liste + cikmis (müfredat konusu = defter konusu, tekrar grupları) + girdi."""
    kod = d["kod"]
    kaynak = kaynak_getir(pk)
    if not kaynak.exists():
        print("   kaynak.md yok:", kaynak); return 2
    metin = kaynak.read_text()
    sayfa = len(re.findall(r"=== SAYFA \d+ ===", metin))
    if kuru:
        return 0
    for alt in ("pdf_metin", "cikmis", "girdi", "onem", "cozucu"):
        (W / alt).mkdir(parents=True, exist_ok=True)
    (W / "pdf_metin" / f"{kod}.md").write_text(metin)
    lp = W / "pdf_liste.json"
    liste = [x for x in (json.loads(lp.read_text()) if lp.exists() else []) if x["kod"] != kod]
    liste.append({"kod": kod, "no": int(d["id"].split("-")[1]), "ad": Path(pk.get("pdf") or "").name or d["konu"],
                  "sayfa": sayfa, "ders_id": d["id"], "konu": d["konu"], "ogretim_uyesi": d.get("ogretim_uyesi")})
    lp.write_text(json.dumps(sorted(liste, key=lambda x: x["no"]), ensure_ascii=False, indent=1))
    Q = json.load(open(MEDS / "data/pastQuestions.json"))
    gizli, silinen = AH.gizli_silinen()
    hedef_konu = {AH.norm(d["konu"])} | {AH.norm(k) for k in d.get("cikmis_konular") or []}
    L, yol = konu_eslesen_cikmislar(Q, d, hedef_konu, gizli, silinen)
    if L:
        print(f"   çıkmış konu eşlemesi: {yol}")
    cik = AH.grupla(L) if L else []
    (W / "cikmis" / f"{kod}.json").write_text(json.dumps(cik, ensure_ascii=False, indent=1))
    (W / "girdi" / f"{kod}.json").write_text(json.dumps(
        {**liste[-1], "brans": W.name, "cikmis_tekil": len(cik), "ornek_hedef": AH.ornek_hedefi(len(cik), sayfa)},
        ensure_ascii=False, indent=1))
    print(f"   {kod}: {sayfa} sayfa · çıkmış aday {len(L)} → tekil {len(cik)}")
    if not cik:  # yeni konu olabilir; ama müfredat eşlemesi kopuk da olabilir → görünür kalsın
        print(f"   UYARI {kod}: bu derse eşlenmiş çıkmış soru yok (konu: {d['konu']}) — önem yalnız PDF + örnek sorularla")
    # Önem haritası: sayfa başına sınava konu olma puanı (çıkmış benzerliği × sıklık × yakınlık) → tüm üreticilere girdi
    return calistir([str(MEDS / ".venv-ocr/bin/python"), str(MEDS / "scripts/onem/onem_haritasi.py"),
                     str(W / "pdf_metin" / f"{kod}.md"), str(W / "cikmis" / f"{kod}.json"), "--kod", kod,
                     "--yaz", str(W / "onem_haritasi" / f"{kod}.json"),
                     "--sayfalar", str(kaynak.parent / "sayfalar.json")])


def a_onem(d, pk, W, kuru):
    r = _a_onem(d, pk, W, kuru)
    if r == 0 and not kuru:
        n = karantina_onerileri(d, W)
        if n:
            print(f"   {n} çıkmış anahtar çelişkisi → karantina önerisi + bildirim")
    return r


def gorev_modu(gorev):
    """otomasyon/llm/gorevler.json → mod: aktif (görev yolu) | golge (Claude + yanında ücretsiz görev yolu, kıyas)."""
    try:
        g = next(x for x in json.loads((MEDS / "otomasyon/llm/gorevler.json").read_text())["gorevler"] if x["id"] == gorev)
        return g.get("mod", "golge")
    except Exception:  # noqa: BLE001
        return "kapali"


def spot_gorev(adim, W, kod, golge, kuru):
    """R4: önem/çözücü adımını görev yoluyla yürütür (otomasyon/llm/spot_zinciri.py). Gölgede yalnız ücretsiz katman,
    çıktı W/_golge/ aynasında (Claude dosyalarını ezmez) ve kıyas meds_temp/golge/<gün>.jsonl'a yazılır."""
    kom = [str(MEDS / ".venv-ocr/bin/python"), str(MEDS / "otomasyon/llm/spot_zinciri.py"), adim, str(W), kod]
    if golge:
        kom += ["--golge", "--katman", "A"]   # gölge = Claude dışı ajanlar (spot_zinciri --golge MEDS_AJAN_CLAUDE=0 koyar)
    r = calistir(kom, kuru=kuru)
    if golge and not kuru:
        try:
            alt = {"onem": "onem", "cozucu": "cozucu", "asistan": "asistan/cikti"}[adim]
            gs = W / "_golge" / alt / f"{kod}.json"
            cs = W / alt / f"{kod}.json"
            kayit = {"zaman": dt.datetime.now().isoformat(timespec="seconds"), "gorev": f"zincir_{adim}", "hedef": kod,
                     "kapi": r == 0, "kod": r}
            if r == 0 and gs.exists() and cs.exists() and adim == "onem":
                g, c_ = json.loads(gs.read_text()), json.loads(cs.read_text())
                kul = lambda o: {x for m in o["maddeler"] for x in m.get("cikmis") or []}  # noqa: E731
                ortak = (kul(g) | {x["id"] for x in g.get("elenen_cikmis") or []})
                kayit.update({"madde": [len(g["maddeler"]), len(c_["maddeler"])],
                              "cikmis_karar_uyumu": sum(1 for x in ortak if (x in kul(g)) == (x in kul(c_))) / max(len(ortak), 1)})
            (KOK / "meds_temp/golge").mkdir(parents=True, exist_ok=True)
            with open(KOK / f"meds_temp/golge/{dt.date.today().isoformat()}.jsonl", "a") as f:
                f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
        except Exception as e:  # noqa: BLE001
            print(f"   gölge kıyası yazılamadı: {e}")
    return r


def _a_onem(d, pk, W, kuru):
    k = d["kod"]
    mod = gorev_modu("onem_listesi")
    if mod == "aktif":
        return spot_gorev("onem", W, k, False, kuru)
    r = _a_onem_claude(d, pk, W, kuru)
    if r == 0 and mod == "golge":
        spot_gorev("onem", W, k, True, kuru)          # gölge sonucu zinciri ETKİLEMEZ
    return r


def _a_onem_claude(d, pk, W, kuru):
    k = d["kod"]
    return kapili_claude(
        f"{SC}/TALIMAT_ONEM.md talimatını uygula. Çalışma klasörü: {W} (branş klasörü {W.name}, Kurul {d['kurul']} "
        f"{d['brans']}). Yalnız ders kodu {k}: girdi/{k}.json, cikmis/{k}.json, pdf_metin/{k}.md → onem/{k}.json. "
        f"onem_haritasi/{k}.json her sayfanın çıkmış sorularla örtüşme puanını (0–100) ve bağlı çıkmışları verir: madde "
        f"puanlarını ve sırasını buna dayandır; puanı yüksek sayfaların bilgisi mutlaka madde olsun. "
        f"Ders klasöründeki sayfalar.json'da tablolar, hoca vurgusu ve görsel sayfa görüntüleri (sayfa_goruntu/) var: "
        f"{(KOK / pk['kaynak_md']).parent}/ — görsel ağırlıklı sayfaları Read ile görüntü olarak aç. "
        f"Kurul 2 kuralları: {MEDS}/docs/KURUL2_YAPILMAYACAK_HATALAR.md, TURKCE_USLUP_STANDARDI.md, SIK_ACIKLAMA_STANDARDI.md.",
        f"python3 {SC}/onem_dogrula.py {W}/onem/{k}.json", W, kuru)


def karantina_onerileri(d, W):
    """H10: yazar ajanın "anahtar_celiskili" diye elediği çıkmışlar (veritabanı anahtarı ders PDF'iyle çelişiyor).
    Otomatik DÜZELTİLMEZ ve sitede otomatik GİZLENMEZ: öneri dosyasına yazılır + yöneticiye bildirim; karar yöneticinin."""
    p = W / "onem" / f"{d['kod']}.json"
    if not p.exists():
        return 0
    el = [x for x in json.loads(p.read_text()).get("elenen_cikmis") or [] if x.get("neden") == "anahtar_celiskili"]
    if not el:
        return 0
    dosya = KOK / "meds_database_v2/ders_isci/cikmis_karantina_onerileri.jsonl"
    dosya.parent.mkdir(parents=True, exist_ok=True)
    eski = {json.loads(l)["id"] for l in dosya.read_text().splitlines() if l.strip()} if dosya.exists() else set()
    yeni = [x for x in el if x["id"] not in eski]
    with open(dosya, "a") as f:
        for x in yeni:
            f.write(json.dumps({"id": x["id"], "ders": d["id"], "kod": d["kod"], "not": x.get("not"),
                                "zaman": dt.datetime.now().isoformat(timespec="seconds")}, ensure_ascii=False) + "\n")
    if yeni:
        sys.path.insert(0, str(MEDS / "otomasyon")); from bildir import bildir
        bildir(f"Çıkmış anahtarı ders PDF'iyle çelişiyor ({len(yeni)} soru, {d['id']})",
               "\n".join(f"{x['id']}: {x.get('not', '')}" for x in yeni)
               + "\nSorular bu dersin çözücüsüne/önem listesine alınmadı. Sitede düzeltme/gizleme kararı yöneticinin "
                 f"(öneri listesi: {dosya.relative_to(KOK)}).", hedef="cikmis-anahtar")
    return len(yeni)


def a_cozucu(d, pk, W, kuru):
    k = d["kod"]
    mod = gorev_modu("cozucu_sorusu")
    if mod == "aktif":
        return spot_gorev("cozucu", W, k, False, kuru)
    r = _a_cozucu_claude(d, pk, W, kuru)
    if r == 0 and mod == "golge" and (W / "_golge" / "onem" / f"{k}.json").exists():
        spot_gorev("cozucu", W, k, True, kuru)
    return r


def _a_cozucu_claude(d, pk, W, kuru):
    k = d["kod"]
    return kapili_claude(
        f"{SC}/TALIMAT_COZUCU.md talimatını uygula. Çalışma klasörü: {W}. Yalnız ders kodu {k}: onem/{k}.json + "
        f"cikmis/{k}.json + pdf_metin/{k}.md → cozucu/{k}.json. Şık açıklamaları {MEDS}/docs/SIK_ACIKLAMA_STANDARDI.md'ye uyar.",
        f"python3 {SC}/cozucu_dogrula.py {W}/cozucu/{k}.json", W, kuru)


def onayli_yaz(W, kod, ekle):
    """Bağımsız denetimi geçmiş kodlar (birlestir.py / asistan_birlestir.py yalnız bunları yayına alır)."""
    p = W / "onayli.json"
    o = set(json.loads(p.read_text())) if p.exists() else set()
    (o.add if ekle else o.discard)(kod)
    p.write_text(json.dumps(sorted(o), ensure_ascii=False))


def a_denetim(d, pk, W, kuru):
    """Bağımsız denetçi (yazar ≠ denetçi): DENETIM.md; düzeltmeden sonra iki kapı yeniden. Önem/çözücü görev yoluyla
    üretildiyse (mod aktif) denetim de görev yoluyla: yazarın ailesi dışından denetçi (spot_zinciri.py denetim)."""
    k = d["kod"]
    if gorev_modu("onem_listesi") == "aktif":
        r = spot_gorev("denetim", W, k, False, kuru)
        if not kuru:
            onayli_yaz(W, k, r == 0)
        return r
    claude(f"Sen bağımsız denetçisin (yazar değil). {SC}/DENETIM.md talimatını uygula. Çalışma klasörü: {W}. Yalnız ders "
           f"kodu {k}: onem/{k}.json ve cozucu/{k}.json'u pdf_metin/{k}.md'ye karşı denetle, hataları düzelt, "
           f"denetim/{k}.md raporu yaz.", W, kuru)
    r = (calistir(f"python3 {SC}/onem_dogrula.py {W}/onem/{k}.json", kuru=kuru)
         or calistir(f"python3 {SC}/cozucu_dogrula.py {W}/cozucu/{k}.json", kuru=kuru))
    if not kuru and r == 0 and not (W / "denetim" / f"{k}.md").exists():
        print("   denetçi raporu yazılmadı (denetim/<kod>.md) — denetim yapılmış sayılmaz"); r = 8
    if not kuru:
        onayli_yaz(W, k, r == 0)
    return r


def _sayim(klasor):
    """Birleştirme çıktısı özeti: ders sayısı + toplam madde/soru (index.json ve ders dosyaları)."""
    if not klasor.exists():
        return (0, 0)
    dersler, ogeler = 0, 0
    for f in klasor.glob("*.json"):
        if f.name == "index.json":
            continue
        dersler += 1
        try:
            j = json.loads(f.read_text())
            ogeler += len(j.get("maddeler") or j.get("sorular") or j.get("bolumler") or [])
        except ValueError:
            pass
    return (dersler, ogeler)


def korumali(klasorler, is_):
    """H6: birleştirici dosya silmesin / içerik küçültmesin. Önce yedek; sonra ders sayısı ya da öğe sayısı %10'dan fazla
    düşerse yedeği geri koy ve hata ver (reddedilen ders eski hâliyle kalır)."""
    import tempfile
    yedek = Path(tempfile.mkdtemp(prefix="medsor-birlestir-"))
    once = {k: _sayim(k) for k in klasorler}
    for k in klasorler:
        if k.exists():
            shutil.copytree(k, yedek / k.name)
    r = is_()
    sorun = [f"{k.name}: {once[k]} → {_sayim(k)}" for k in klasorler
             if _sayim(k)[0] < once[k][0] or _sayim(k)[1] < 0.9 * once[k][1]]
    if sorun:
        for k in klasorler:
            if (yedek / k.name).exists():
                shutil.rmtree(k, ignore_errors=True); shutil.copytree(yedek / k.name, k)
        print("   HATA: birleştirme içerik sildi/küçülttü — geri alındı:", "; ".join(sorun)); r = 11
    shutil.rmtree(yedek, ignore_errors=True)
    return r


def kopya_tutarliligi(W_ad, kod):
    """H7: aynı soru (aynı kök) önem listesinde ve çözücüde farklı doğru cevapla duramaz (düzeltme tek kopyada kalmış).
    Döner: uyuşmazlık listesi (boşsa tutarlı)."""
    def n(t):
        return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", str(t or "").casefold())).strip()
    oy, cy = MEDS / "src/data" / f"{W_ad}_onem" / f"{kod}.json", MEDS / "src/data" / f"{W_ad}_cozucu"
    if not oy.exists():
        return []
    o = json.loads(oy.read_text())
    kaynak = {}  # kök → (doğru harf, doğru metin, nereden)
    for i, c in (o.get("cikmis") or {}).items():
        kaynak[n(c.get("kok"))] = (c.get("dogru"), n((c.get("secenekler") or {}).get(c.get("dogru"))), f"önem çıkmış {i}")
    for m in o.get("maddeler") or []:
        for q in m.get("ornek26") or []:
            kaynak.setdefault(n(q.get("kok")), (q.get("dogru"), n((q.get("secenekler") or {}).get(q.get("dogru"))), f"önem örnek {m.get('id')}"))
    sorun = []
    for f in sorted(cy.glob(f"{kod}*.json")):
        for q in json.loads(f.read_text()).get("sorular") or []:
            k = kaynak.get(n(q.get("soru")))
            if not k:
                continue
            dm = n((q.get("secenekler") or {}).get(q.get("dogru")))
            if k[1] and dm and k[1] != dm:  # harf karışık olabilir (şık sırası); doğru şık METNİ aynı olmalı
                sorun.append(f"{k[2]} ↔ çözücü no {q.get('no')}: doğru şık farklı ({k[0]} '{k[1][:40]}' / {q.get('dogru')} '{dm[:40]}')")
    return sorun


def a_birlestir(d, pk, W, kuru):
    if kuru:
        return calistir(f"python3 {SC}/birlestir.py {W.name} --taslak", kuru=True)
    hedef = [MEDS / "src/data" / f"{W.name}_onem", MEDS / "src/data" / f"{W.name}_cozucu"]
    r = korumali(hedef, lambda: calistir(f"python3 {SC}/birlestir.py {W.name} --taslak"))
    if r:
        return r
    # --taslak hatalı dersi atlayıp 0 döner: bu dersin çıktısı gerçekten yazıldı mı?
    if not (MEDS / "src/data" / f"{W.name}_onem" / f"{d['kod']}.json").exists():
        print(f"   birleştirme {d['kod']} önem çıktısını yazmadı"); return 9
    tut = kopya_tutarliligi(W.name, d["kod"])
    if tut:
        print("   HATA (H7) aynı soru ürünler arasında farklı:", *tut[:8], sep="\n     "); return 13
    # "Öğren'de bu bilgi": çözücü/asistan ↔ Öğren adımı eşlemesi (tüm branşlar, ~3 sn). Provada atlanır: bütün branşların
    # cozucu_ogren dosyalarını yeniden yazıyordu (2026-10-24, K1 dosyalarına istenmeyen dokunuş)
    if os.environ.get("MEDS_PROVA") == "1":
        return 0
    return calistir(f"python3 {SC}/ogren_esle.py", cwd=MEDS)


def a_asistan(d, pk, W, kuru):
    k = d["kod"]
    if calistir(f"python3 {SC}/asistan_plan.py {W.name} {k}", kuru=kuru):
        return 1
    if not kuru:
        hedef = [MEDS / "src/data" / f"{W.name}_asistan"]
        birlestir_asistan = lambda: calistir(f"python3 {SC}/asistan_birlestir.py {W.name}")  # noqa: E731
    else:
        hedef, birlestir_asistan = [], lambda: calistir(f"python3 {SC}/asistan_birlestir.py {W.name}", kuru=True)  # noqa: E731
    mod = gorev_modu("asistan_nokta")
    if mod == "aktif":
        r = spot_gorev("asistan", W, k, False, kuru)
    else:
        r = kapili_claude(f"{SC}/TALIMAT_ASISTAN.md talimatını uygula. Çalışma klasörü: {W}/asistan. Yalnız ders kodu {k}. "
                          f"Anlatım bir tıp doktorunun öğrenciye Türkçe anlatımı üslubunda; ekranda madde madde.",
                          f"python3 {SC}/asistan_dogrula.py {W}/asistan/cikti/{k}.json", W, kuru)
        if r == 0 and mod == "golge":
            spot_gorev("asistan", W, k, True, kuru)       # gölge: W/_golge/asistan/cikti, zinciri etkilemez
    return r or (korumali(hedef, birlestir_asistan) if hedef else birlestir_asistan())


def a_ses(d, pk, W, kuru):
    """EMA: çözücü + asistan + Öğren adımları. Ses işçileri flock'lu; DAİMA GPU (cozucu_ses_gpu.sh, koruyucu + ısı protokolü)."""
    k = d["kod"]
    r = calistir(f"bash {SC}/ses_kuyruk.sh {W.name} --ses ema {k}", kuru=kuru)
    r = r or calistir(f"bash {SC}/asistan_ses_kuyruk.sh {W.name} {k}", kuru=kuru)
    deste = pk.get("deste_id")
    if deste:
        # Öğren adım sesleri: EMA venv, makine korumalı kapsam, bitince Oracle'a rsync (--oracle)
        # EMA daima GPU (kullanıcı kararı 2026-10-24): koruyuculu GPU başlatıcısı (cozucu_ses_gpu.sh)
        r = r or calistir(f"bash {MEDS}/scripts/patoloji_cozucu/cozucu_ses_gpu.sh "
                          f"{MEDS}/scripts/ogren_ses/ogren_ses_uret.py {deste} --oracle", cwd=MEDS, kuru=kuru)
    return r or calistir(f"python3 {SC}/birlestir.py {W.name} --taslak", kuru=kuru)


def a_oracle(d, pk, W, kuru):
    """Ses dosyaları (git dışı) Oracle'a; içerik JSON'ları kod dağıtımıyla gider (esitle_dagit aşaması)."""
    hedef, r = "/home/ubuntu/medsor/meds/data", 0
    for alt in (f"{W.name}_cozucu", f"{W.name}_asistan"):
        if (MEDS / "data" / alt).exists() or kuru:
            r = r or calistir(f"rsync -az --rsync-path='sudo rsync' {MEDS}/data/{alt}/ medsor-oracle:{hedef}/{alt}/", kuru=kuru)
    if r or kuru:
        return r
    # H11: ses gerçekten canlıda mı (404 olursa tarayıcı sesine düşüyordu) — bu dersin rastgele 5 klibi
    import random
    url = {f"{W.name}_cozucu": "https://api.nofrostlife.com.tr/api/cozucu-ses/{b}/ema/{k}/{c}",
           f"{W.name}_asistan": "https://api.nofrostlife.com.tr/api/patoloji-asistan/ses/{k}/{c}"}
    for alt, kalip in url.items():
        klipler = sorted((MEDS / "data" / alt / "ses" / d["kod"]).glob("*.mp3"))
        for f in random.sample(klipler, min(5, len(klipler))):
            u = kalip.format(b=W.name, k=d["kod"], c=f.name)
            kod = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-m", "20", "-r", "0-99", u],
                                 capture_output=True, text=True).stdout
            if kod not in ("200", "206"):
                print(f"   HATA: canlıda ses yok ({kod}): {u}"); return 12
    return 0


def a_capa(d, pk, W, kuru):
    """Anlamsal slayt çapası (2026-10-21, Kurul 1'de elle yazıldı): sesli dersin her cümlesine slayttaki madde/resim kutusu.
    Oracle'daki metin + hizalama + v2 çapası alınır → capa_dok.py görüntü dökümü → Claude TALIMAT_CAPA.md → kapı
    capa_dogrula.py 0 HATA → data/sesli_anlatim/capa/<key>.json cihaz + Oracle (Oracle pdf_isaret zamanlayıcısı 30 dk'da işler)."""
    key, S = pk["ders_id"], MEDS / "data/sesli_anlatim"
    uz = "medsor-oracle:/home/ubuntu/medsor/meds/data/sesli_anlatim"
    for alt, ad in (("metin", f"{key}.md"), ("hizalama", f"{key}.json"), ("capa", f"{key}.json")):
        (S / alt).mkdir(parents=True, exist_ok=True)
        calistir(f"rsync -az {uz}/{alt}/{ad} {S}/{alt}/", kuru=kuru)
    if not kuru and not ((S / "metin" / f"{key}.md").exists() and (S / "hizalama" / f"{key}.json").exists()):
        print(f"   {key}: sesli ders metni/hizalaması henüz yok"); return 13
    C = W / "capa" / d["kod"]; C.mkdir(parents=True, exist_ok=True)
    py, api = MEDS / ".venv-ocr/bin/python", "MEDS_API=https://api.nofrostlife.com.tr"
    r = calistir(f"{api} {py} {MEDS}/scripts/sesli_anlatim/capa_dok.py {key} {C}/dok", cwd=MEDS, kuru=kuru)
    if r:
        return r
    if not kuru:
        sha = hashlib.sha1((S / "metin" / f"{key}.md").read_bytes()).hexdigest()
        bas = json.loads((S / "capa" / f"{key}.json").read_text()) if (S / "capa" / f"{key}.json").exists() else {"p": []}
        bas["mdSha1"] = sha
        if not (C / "capa.json").exists():
            (C / "capa.json").write_text(json.dumps(bas, ensure_ascii=False))
    kapi = f"{api} {py} {MEDS}/scripts/sesli_anlatim/capa_dogrula.py {key} {C}/capa.json"
    istem = (f"{MEDS}/scripts/sesli_anlatim/TALIMAT_CAPA.md talimatını uygula. Ders anahtarı {key}; çalışma klasörü {C} "
             f"(dok/ ve capa.json orada). Bitince şu kapıyı 0 HATA olana dek çalıştır: {kapi}")
    r = kapili_claude(istem, kapi, C, kuru)
    if r or kuru:
        return r
    shutil.copy(C / "capa.json", S / "capa" / f"{key}.json")
    return calistir(f"rsync -az --rsync-path='flock /tmp/meds-deploy.lock sudo rsync' {S}/capa/{key}.json {uz}/capa/", kuru=kuru)


def a_cizim(d, pk, W, kuru):
    """Canlı çizim (R6, ICERIK_MOTORU_V3.md §4; 2026-10-24): çapa dökümü + işaret → scripts/cizim/cizim_uret.py (sayfa
    partileri eşzamanlı Claude, kapı cizim_dogrula.py; geçmeyen komut atılır) → data/sesli_anlatim/cizim/<key>.json cihaz +
    Oracle. İşaret, çapa geldikten sonra Oracle'da hemen yeniden üretilir ki metinHash aynı sürümden olsun."""
    key, S = pk["ders_id"], MEDS / "data/sesli_anlatim"
    uz = "medsor-oracle:/home/ubuntu/medsor/meds/data/sesli_anlatim"
    C = W / "capa" / d["kod"]
    if not kuru and not ((C / "dok" / "cumleler.md").exists() and (C / "capa.json").exists()):
        print(f"   {key}: çapa dökümü yok (önce capa adımı)"); return 13
    r = calistir("ssh medsor-oracle 'sudo systemctl start meds-cumle-zaman.service'", kuru=kuru)
    (S / "isaret").mkdir(parents=True, exist_ok=True)
    r = r or calistir(f"rsync -az {uz}/isaret/{key}.json {S}/isaret/", kuru=kuru)
    py = MEDS / ".venv-ocr/bin/python"
    r = r or calistir(f"{py} {MEDS}/scripts/cizim/cizim_uret.py {key} --dok {C}/dok --capa {C}/capa.json "
                      f"--isaret {S}/isaret/{key}.json --is-dizini {W}/cizim/{d['kod']}", cwd=MEDS, kuru=kuru)
    if r:
        return r
    return calistir(f"rsync -az --rsync-path='flock /tmp/meds-deploy.lock sudo rsync' {S}/cizim/{key}.json {uz}/cizim/", kuru=kuru)


IS = {"hazirla": a_hazirla, "onem": a_onem, "cozucu": a_cozucu, "denetim": a_denetim, "birlestir": a_birlestir,
      "asistan": a_asistan, "ses": a_ses, "oracle": a_oracle, "capa": a_capa, "cizim": a_cizim}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kurul", type=int); ap.add_argument("--ders"); ap.add_argument("--adim", choices=ADIMLAR)
    ap.add_argument("--durum", action="store_true"); ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--en-cok", type=int, default=3, help="bir çalıştırmada en çok kaç ders (gece süresi)")
    a = ap.parse_args()
    if a.kurul:
        kurullar = [a.kurul]
    else:  # aktif kurul + önceki Kurul 2+ kurulları (önceki kurulun yarım dersleri terk edilmez)
        sys.path.insert(0, str(MEDS / "scripts/takvim")); from aktif_kurul import durum
        kurullar = list(range(2, durum(dt.date.today().isoformat())["aktif"] + 1))
    kurullar = [k for k in kurullar if k >= 2]
    if not kurullar:
        print("Kurul 1 eski hattında (elle); zincir Kurul 2+ için."); return 0
    defter = [d for k in sorted(kurullar, reverse=True)  # aktif kurul önce
              for d in json.loads((MEDS / f"src/data/dersler/k{k}.json").read_text())["dersler"]]
    kayit = yayinlar(); hata = 0; islenen = 0
    for d in defter:
        if a.ders and d["id"] != a.ders:
            continue
        pk = paket_bul(d, kayit); s = durum_oku(d)
        if a.durum:
            son = [x for x in ADIMLAR if (s["adimlar"].get(x) or {}).get("kod") == 0]
            print(f"{d['id']} {d['kod']:5} {d['konu'][:44]:44} paket:{'var' if pk else 'yok':3} "
                  f"tamam: {','.join(son) or '-'}")
            continue
        if not pk:
            continue
        if s.get("cekildi") and not a.ders:  # Hat panosundan yayından çekildi: kendiliğinden yeniden yayına alınmaz
            continue
        kp = kaynak_getir(pk)
        sha = hashlib.sha256(kp.read_bytes()).hexdigest()[:16] if kp.exists() else ""
        if not sha:
            print(f"  {d['id']}: kaynak.md alınamadı — sonraki gece (durum korunur)"); hata += 1; continue
        if s.get("kaynak_sha") and s.get("kaynak_sha") != sha:  # kaynak değişti: eski ara dosyalar kenara, onay düşer
            Wk = W0 / brans_klasoru(d); eski = Wk / "_eski" / f"{d['kod']}-{dt.datetime.now():%Y%m%d%H%M}"
            for alt in ("onem", "cozucu", "denetim", "asistan/cikti"):
                f = Wk / alt / (f"{d['kod']}.md" if alt == "denetim" else f"{d['kod']}.json")
                if f.exists():
                    eski.mkdir(parents=True, exist_ok=True); f.rename(eski / f"{alt.replace('/', '_')}_{f.name}")
            if Wk.exists():
                onayli_yaz(Wk, d["kod"], False)
        if s.get("kaynak_sha") != sha:
            s = {"kaynak_sha": sha, "adimlar": {}, "hata_sayisi": 0}  # kaynak değişti → zincir baştan
        bekleyen = [x for x in ADIMLAR if (s["adimlar"].get(x) or {}).get("kod") != 0]
        if a.adim:
            bekleyen = [a.adim]
        if not bekleyen:
            continue
        # geri çekilme: art arda hata veren ders 1, 2, 4 … gün (en çok 7) bekler; kota diğer dersleri tıkamaz
        n_hata = int(s.get("hata_sayisi") or 0)
        son_h = s.get("son_hata")
        if n_hata and son_h and not a.ders and not a.adim:
            bekle = min(7, 2 ** (n_hata - 1))
            if dt.datetime.now() - dt.datetime.fromisoformat(son_h) < dt.timedelta(days=bekle):
                print(f"  {d['id']}: {n_hata} kez hata, {bekle} gün bekliyor"); continue
        if islenen >= a.en_cok:
            break
        islenen += 1
        W = W0 / brans_klasoru(d); W.mkdir(parents=True, exist_ok=True)
        print(f"▶ {d['id']} {d['kod']} {d['konu']} → {W.name}")
        for x in bekleyen:
            print(f"  · {x}")
            kod = IS[x](d, pk, W, a.kuru)
            if not a.kuru:
                s["adimlar"][x] = {"zaman": dt.datetime.now().isoformat(timespec="seconds"), "kod": kod}
                durum_yaz(d, s)
            if kod:
                if not a.kuru:
                    s["hata_sayisi"] = int(s.get("hata_sayisi") or 0) + 1
                    s["son_hata"] = dt.datetime.now().isoformat(timespec="seconds"); durum_yaz(d, s)
                print(f"  ✗ {x} kod={kod} — ders bu adımda kaldı"); hata += 1; break
            if x == "oracle" and not a.kuru:  # zincir bitti → içerik seti sürümleri (göç 0001), yerel + Oracle
                sys.path.insert(0, str(MEDS / "scripts/db")); from icerik_kaydi import kaydet
                kayit_hata = 0
                for tur in ("onem", "cozucu", "asistan"):
                    yol = next(iter(sorted((MEDS / "src/data" / f"{W.name}_{tur}").glob(f"{d['kod']}*.json"))), None)
                    if yol:  # çözücü 40+ soruda <kod>-1.json setlerine bölünür
                        kayit_hata += kaydet(d["id"], tur, s.get("kaynak_sha"), str(yol.relative_to(MEDS)), d["kurul"], oracle=True)
                if kayit_hata:  # sürüm kaydı yazılamadı: oracle adımı yeniden denensin
                    s["adimlar"]["oracle"]["kod"] = 6; durum_yaz(d, s); hata += 1
                else:
                    s["hata_sayisi"] = 0; durum_yaz(d, s)
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
