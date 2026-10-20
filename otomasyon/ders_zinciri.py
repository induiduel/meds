#!/usr/bin/env python3
"""Ders zinciri (Kurul 2+): yayımlanmış her ders paketi için spot/önem → soru çözücü → denetim → birleştirme →
sesli asistan → EMA ses → Oracle. Ders listesi src/data/dersler/k<N>.json (ders kayıt defteri); ders işçisinin
yayımladığı paket yayin_kaydi.json'dan bulunur (ders_id = <defter id>-<slug>).

Her adım kapı ile biter (0 HATA değilse ders o adımda kalır, sonraki gece yeniden dener; sessiz geçiş yok).
Durum: meds_temp/hat/dersler/<ders id>.json → {kaynak_sha, adimlar: {adim: {zaman, kod, not}}}. Kaynak (kaynak.md)
değişirse zincir baştan çalışır. LLM adımları yalnız Claude (claude -p) ile — kullanıcı kararı 2026-10-20.

Branş klasörü kurul öneklidir: meds_temp/spot_cozucu/k<N><brans>/ (ör. k2noroloji) — Kurul 1 klasörleri ezilmez.
Kodlar defterden (2n03): kurullar ve branşlar arası tekil.

  ders_zinciri.py --durum [--kurul 2]                 hangi ders hangi adımda
  ders_zinciri.py --kurul 2 [--ders k2-07] [--adim hazirla] [--kuru]
"""
import argparse, datetime as dt, hashlib, json, os, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
SC = MEDS / "scripts/spot_cozucu"
W0 = KOK / "meds_temp/spot_cozucu"
DURUM = KOK / "meds_temp/hat/dersler"
sys.path.insert(0, str(SC))
import aday_hazirla as AH  # noqa: E402  gizli_silinen, aday, grupla, ornek_hedefi, norm

BRANS_SLUG = {b["ad"]: b["slug"] for b in json.loads((MEDS / "src/data/dersler/branslar.json").read_text())["branslar"]}  # tek kaynak
ADIMLAR = ["hazirla", "onem", "cozucu", "denetim", "birlestir", "asistan", "ses", "oracle"]
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
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rsync", "-az", f"medsor-oracle:/home/ubuntu/medsor/{pk['kaynak_md']}", str(p)], timeout=120)
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
        return subprocess.run(kom, cwd=W, stdout=log, stderr=subprocess.STDOUT).returncode


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
    L = []
    for q in Q:
        m = (q.get("checkSolve") or {}).get("mufredat") or {}
        if m.get("kurul") == d["kurul"] and m.get("ders") == d["brans"] and AH.norm(m.get("konu")) in hedef_konu:
            c = AH.aday(q, gizli, silinen)
            if c: L.append(c)
    cik = AH.grupla(L) if L else []
    (W / "cikmis" / f"{kod}.json").write_text(json.dumps(cik, ensure_ascii=False, indent=1))
    (W / "girdi" / f"{kod}.json").write_text(json.dumps(
        {**liste[-1], "brans": W.name, "cikmis_tekil": len(cik), "ornek_hedef": AH.ornek_hedefi(len(cik), sayfa)},
        ensure_ascii=False, indent=1))
    print(f"   {kod}: {sayfa} sayfa · çıkmış aday {len(L)} → tekil {len(cik)}")
    # Önem haritası: sayfa başına sınava konu olma puanı (çıkmış benzerliği × sıklık × yakınlık) → tüm üreticilere girdi
    return calistir([str(MEDS / ".venv-ocr/bin/python"), str(MEDS / "scripts/onem/onem_haritasi.py"),
                     str(W / "pdf_metin" / f"{kod}.md"), str(W / "cikmis" / f"{kod}.json"), "--kod", kod,
                     "--yaz", str(W / "onem_haritasi" / f"{kod}.json")])


def a_onem(d, pk, W, kuru):
    k = d["kod"]
    return kapili_claude(
        f"{SC}/TALIMAT_ONEM.md talimatını uygula. Çalışma klasörü: {W} (branş klasörü {W.name}, Kurul {d['kurul']} "
        f"{d['brans']}). Yalnız ders kodu {k}: girdi/{k}.json, cikmis/{k}.json, pdf_metin/{k}.md → onem/{k}.json. "
        f"onem_haritasi/{k}.json her sayfanın çıkmış sorularla örtüşme puanını (0–100) ve bağlı çıkmışları verir: madde "
        f"puanlarını ve sırasını buna dayandır; puanı yüksek sayfaların bilgisi mutlaka madde olsun. "
        f"Kurul 2 kuralları: {MEDS}/docs/KURUL2_YAPILMAYACAK_HATALAR.md, TURKCE_USLUP_STANDARDI.md, SIK_ACIKLAMA_STANDARDI.md.",
        f"python3 {SC}/onem_dogrula.py {W}/onem/{k}.json", W, kuru)


def a_cozucu(d, pk, W, kuru):
    k = d["kod"]
    return kapili_claude(
        f"{SC}/TALIMAT_COZUCU.md talimatını uygula. Çalışma klasörü: {W}. Yalnız ders kodu {k}: onem/{k}.json + "
        f"cikmis/{k}.json + pdf_metin/{k}.md → cozucu/{k}.json. Şık açıklamaları {MEDS}/docs/SIK_ACIKLAMA_STANDARDI.md'ye uyar.",
        f"python3 {SC}/cozucu_dogrula.py {W}/cozucu/{k}.json", W, kuru)


def a_denetim(d, pk, W, kuru):
    """Bağımsız denetçi (yazar ≠ denetçi): DENETIM.md; düzeltmeden sonra iki kapı yeniden."""
    k = d["kod"]
    claude(f"Sen bağımsız denetçisin (yazar değil). {SC}/DENETIM.md talimatını uygula. Çalışma klasörü: {W}. Yalnız ders "
           f"kodu {k}: onem/{k}.json ve cozucu/{k}.json'u pdf_metin/{k}.md'ye karşı denetle, hataları düzelt, "
           f"denetim/{k}.md raporu yaz.", W, kuru)
    return (calistir(f"python3 {SC}/onem_dogrula.py {W}/onem/{k}.json", kuru=kuru)
            or calistir(f"python3 {SC}/cozucu_dogrula.py {W}/cozucu/{k}.json", kuru=kuru))


def a_birlestir(d, pk, W, kuru):
    return calistir(f"python3 {SC}/birlestir.py {W.name} --taslak", kuru=kuru)


def a_asistan(d, pk, W, kuru):
    k = d["kod"]
    if calistir(f"python3 {SC}/asistan_plan.py {W.name} {k}", kuru=kuru):
        return 1
    r = kapili_claude(f"{SC}/TALIMAT_ASISTAN.md talimatını uygula. Çalışma klasörü: {W}/asistan. Yalnız ders kodu {k}. "
                      f"Anlatım bir tıp doktorunun öğrenciye Türkçe anlatımı üslubunda; ekranda madde madde.",
                      f"python3 {SC}/asistan_dogrula.py {W}/asistan/cikti/{k}.json", W, kuru)
    return r or calistir(f"python3 {SC}/asistan_birlestir.py {W.name}", kuru=kuru)


def a_ses(d, pk, W, kuru):
    """EMA: çözücü + asistan + Öğren adımları. Ses işçileri flock'lu ve makine korumalı (CPU; GPU yalnız izinli kapsamda)."""
    k = d["kod"]
    r = calistir(f"bash {SC}/ses_kuyruk.sh {W.name} --ses ema {k}", kuru=kuru)
    r = r or calistir(f"bash {SC}/asistan_ses_kuyruk.sh {W.name} {k}", kuru=kuru)
    deste = pk.get("deste_id")
    if deste:
        # Öğren adım sesleri: EMA venv, makine korumalı kapsam, bitince Oracle'a rsync (--oracle)
        r = r or calistir(f"systemd-run --user --scope -q -p CPUQuota=300% -p MemoryMax=2200M --nice=10 "
                          f"env CUDA_VISIBLE_DEVICES= {Path.home()}/.local/share/meds-ema/venv/bin/python "
                          f"{MEDS}/scripts/ogren_ses/ogren_ses_uret.py {deste} --oracle", cwd=MEDS, kuru=kuru)
    return r or calistir(f"python3 {SC}/birlestir.py {W.name} --taslak", kuru=kuru)


def a_oracle(d, pk, W, kuru):
    """Ses dosyaları (git dışı) Oracle'a; içerik JSON'ları kod dağıtımıyla gider (esitle_dagit aşaması)."""
    hedef, r = "/home/ubuntu/medsor/meds/data", 0
    for alt in (f"{W.name}_cozucu", f"{W.name}_asistan"):
        if (MEDS / "data" / alt).exists() or kuru:
            r = r or calistir(f"rsync -az --rsync-path='sudo rsync' {MEDS}/data/{alt}/ medsor-oracle:{hedef}/{alt}/", kuru=kuru)
    return r


IS = {"hazirla": a_hazirla, "onem": a_onem, "cozucu": a_cozucu, "denetim": a_denetim, "birlestir": a_birlestir,
      "asistan": a_asistan, "ses": a_ses, "oracle": a_oracle}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kurul", type=int); ap.add_argument("--ders"); ap.add_argument("--adim", choices=ADIMLAR)
    ap.add_argument("--durum", action="store_true"); ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--en-cok", type=int, default=3, help="bir çalıştırmada en çok kaç ders (gece süresi)")
    a = ap.parse_args()
    if not a.kurul:
        sys.path.insert(0, str(MEDS / "scripts/takvim")); from aktif_kurul import durum
        a.kurul = durum(dt.date.today().isoformat())["aktif"]
    if a.kurul < 2:
        print("Kurul 1 eski hattında (elle); zincir Kurul 2+ için."); return 0
    defter = json.loads((MEDS / f"src/data/dersler/k{a.kurul}.json").read_text())["dersler"]
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
        kp = kaynak_getir(pk)
        sha = hashlib.sha256(kp.read_bytes()).hexdigest()[:16] if kp.exists() else ""
        if s.get("kaynak_sha") != sha:
            s = {"kaynak_sha": sha, "adimlar": {}}  # kaynak değişti → zincir baştan
        bekleyen = [x for x in ADIMLAR if (s["adimlar"].get(x) or {}).get("kod") != 0]
        if a.adim:
            bekleyen = [a.adim]
        if not bekleyen:
            continue
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
                print(f"  ✗ {x} kod={kod} — ders bu adımda kaldı"); hata += 1; break
            if x == "oracle" and not a.kuru:  # zincir bitti → içerik seti sürümleri (göç 0001), yerel + Oracle
                sys.path.insert(0, str(MEDS / "scripts/db")); from icerik_kaydi import kaydet
                for tur, alt in (("onem", "onem"), ("cozucu", "cozucu"), ("asistan", "asistan")):
                    kaydet(d["id"], tur, s.get("kaynak_sha"), f"src/data/{W.name}_{alt}/{d['kod']}.json", d["kurul"], oracle=True)
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
