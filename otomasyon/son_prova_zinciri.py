#!/usr/bin/env python3
"""Son Prova zinciri — Kurul 2+ (gece; kurul sınavından SON_PROVA_GUN gün önce açılır). Kurul 1 Son Provası elle kuruldu
(scripts/son_prova/README.md); bu zincir aynı adımları insan müdahalesiz yürütür:

  plan    scripts/son_prova/plan_kurul.py → meds_temp/son_prova_k<N>/plan.json + havuz/ (ders bilgi deposundan, PDF okunmaz)
  yazar   Claude, TALIMAT.md + YENI_SORU.md, yazar grubu başına → parca/<part>/aNN.json; kapı dogrula.py <dosya> 0 HATA
  denetçi Claude (bağımsız oturum), DENETIM.md + YENI_DENETIM.md → kapı dogrula.py --part <part> PART 0 HATA
  derle   derle.py <part> → cikti/<part>/;  özet PDF  node scripts/son_prova/pdf_kirp.mjs → data/son_prova/pdf/<part>.pdf
  sorular soru_dagit.py → src/data/son_prova/k<N>/ (gece içerik dağıtımı yayınlar)
  ses     yeni_ses.py (EMA, CPU, korumalı kapsam) → data/<k<N><slug>>_cozucu/ses/sNN/
  canlı   metin/hizalama/vurgu + özet PDF + ses Oracle'a (rsync, dağıtım kilidi) → POST /api/sesli-anlatim/ders-ekle (yalnizEma)

Betikler çalışma klasörüne kopyalanır (KOK = kendi klasörleri); talimatlardaki `meds_temp/son_prova/` yolu o klasöre çevrilir.
Bir part ders kümesi ve özetleri değişmedikçe yeniden yazılmaz (iz.txt). Kapı geçmeyen part yayına girmez, bildirim gider.
  son_prova_zinciri.py [--kurul N] [--part KEY] [--zorla] [--kuru] [--prova]
--prova: yalnız plan + ilk partın yazar/denetçi/derle adımları; src/data, data/ ve Oracle'a dokunmaz.
"""
import argparse, datetime as dt, hashlib, json, shutil, subprocess, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[1]; KOK = MEDS.parent
SP = MEDS / "scripts/son_prova"
IZIN = "Read,Write,Edit,Glob,Grep,Bash(python3 *)"
SON_PROVA_GUN = 9  # sınavdan kaç gün önce (dahil) üretim başlar
BUTCE_SAAT = float(__import__("os").environ.get("MEDS_SON_PROVA_SAAT", "5"))  # gece başına; kalan partlar ertesi gece (gece birimi 10 sa)
KOPYA = ["dogrula.py", "derle.py", "soru_dagit.py", "deneme_degistir.py", "TALIMAT.md", "DENETIM.md", "YENI_SORU.md", "YENI_DENETIM.md"]
EMA_PY = Path.home() / ".local/share/meds-ema/venv/bin/python"
ORACLE = "/home/ubuntu/medsor/meds"


def kos(kom, kuru=False, **k):
    print("   $", " ".join(map(str, kom))[:220], flush=True)
    return 0 if kuru else subprocess.run(kom, **k).returncode


def claude(istem, W, kuru):
    if kuru:
        print("   [kuru] claude:", istem[:160]); return
    with open(W / "log" / "claude.log", "a") as log:
        try:
            subprocess.run(["claude", "-p", istem, "--model", "claude-opus-5-5", "--allowedTools", IZIN, "--add-dir", str(KOK)],
                           cwd=W, stdout=log, stderr=subprocess.STDOUT, timeout=4 * 3600)
        except subprocess.TimeoutExpired:
            print("   claude zaman aşımı")


def kapili(istem, kapi, W, kuru, tur=3):
    claude(istem, W, kuru)
    for _ in range(tur):
        if kos(kapi, kuru, cwd=W) == 0:
            return 0
        claude(f"Bu kapı HATA verdi: `{' '.join(map(str, kapi))}`. Çalıştır, hataların hepsini düzelt (yalnız bu partın dosyaları), "
               f"0 HATA olduğunu doğrulayıp bitir.", W, kuru)
    return kos(kapi, kuru, cwd=W)


def hazirla(N):
    W = KOK / f"meds_temp/son_prova_k{N}"
    for d in ("parca", "cikti", "havuz", "log"):
        (W / d).mkdir(parents=True, exist_ok=True)
    rel = f"meds_temp/son_prova_k{N}/"
    for f in KOPYA:
        t = (SP / f).read_text(encoding="utf-8")
        if f.endswith(".md"):
            t = t.replace("meds_temp/son_prova/", rel)
        (W / f).write_text(t, encoding="utf-8")
    return W


def part_izi(p):
    return hashlib.sha256(json.dumps([[d["kod"], d["sayfa"], d["cikmis"], d["havuz"], d["hedef_kelime"]] for d in p["dersler"]]
                                     + [p["key"]]).encode()).hexdigest()[:16]


def part_yaz(p, W, kuru):
    """yazar grupları → aşama dosyaları; sonra bağımsız denetçi; PART 0 HATA döner 0."""
    P = W / "parca" / p["key"]; P.mkdir(parents=True, exist_ok=True)
    kod_asama = {d["kod"]: i for i, d in enumerate(p["dersler"], 1)}  # bir ders = bir aşama
    for g in p["yazar_gruplari"]:
        nolar = [kod_asama[k] for k in g]
        if all((P / f"a{n:02d}.json").exists() for n in nolar):
            continue
        hedefler = ", ".join(f"{k} ≈ {next(d['hedef_kelime'] for d in p['dersler'] if d['kod'] == k)} kelime" for k in g)
        dosyalar = " ".join(str(P / f"a{n:02d}.json") for n in nolar)
        istem = (f"{W}/TALIMAT.md ve {W}/YENI_SORU.md talimatlarını uygula. Part: {p['key']} ({p['brans_ad']}, Kurul {p['key'][1]}). "
                 f"Plan girdisi: {W}/plan.json içindeki bu part. Bu görevde yalnız şu dersleri yaz, her ders bir aşama: {', '.join(g)} "
                 f"(aşama numaraları {nolar}; hedef: {hedefler}). Çıktı: {dosyalar}. Her aşama dosyasına yeni_sorular (2) de ekle. "
                 f"Bitince her dosya için `python3 {W}/dogrula.py <dosya>` 0 HATA olmalı.")
        kapi = ["python3", str(W / "dogrula.py"), *[str(P / f"a{n:02d}.json") for n in nolar]]
        if kapili(istem, kapi, W, kuru):
            return 1
    istem = (f"{W}/DENETIM.md ve {W}/YENI_DENETIM.md talimatlarını uygula (bağımsız denetçisin; yazar sen değilsin). "
             f"Part: {p['key']}, dosyalar {P}/a*.json. Kaynaklar {W}/plan.json'da. Bitince `python3 {W}/dogrula.py --part {p['key']}` "
             f"PART 0 HATA olmalı.")
    return kapili(istem, ["python3", str(W / "dogrula.py"), "--part", p["key"]], W, kuru)


def canliya(p, N, W, kuru):
    key = p["key"]; C = W / "cikti" / key
    hedef = MEDS / "data/sesli_anlatim"
    for alt, kaynak in (("metin", C / f"{key}.md"), ("hizalama", C / "hizalama.json"), ("vurgu", C / "vurgu.json")):
        (hedef / alt).mkdir(parents=True, exist_ok=True)
        if not kuru:
            shutil.copy(kaynak, hedef / alt / (f"{key}.md" if alt == "metin" else f"{key}.json"))
    rs = ["rsync", "-az", "--mkpath", "--rsync-path=flock /tmp/meds-deploy.lock sudo rsync"]
    no = key.split("-")[1]
    gonder = [(hedef / "metin" / f"{key}.md", f"{ORACLE}/data/sesli_anlatim/metin/"),
              (hedef / "hizalama" / f"{key}.json", f"{ORACLE}/data/sesli_anlatim/hizalama/"),
              (hedef / "vurgu" / f"{key}.json", f"{ORACLE}/data/sesli_anlatim/vurgu/")]
    gonder += [(f, f"{ORACLE}/data/son_prova/pdf/") for f in sorted((MEDS / "data/son_prova/pdf").glob(f"{key}.*"))]
    ses = MEDS / f"data/{p['brans']}_cozucu/ses/s{no}"
    if ses.exists():
        gonder.append((f"{ses}/", f"{ORACLE}/data/{p['brans']}_cozucu/ses/s{no}/"))
    for kaynak, uzak in gonder:
        if kos(rs + [str(kaynak), f"medsor-oracle:{uzak}"], kuru, timeout=900):
            return f"{key}: Oracle'a gönderilemedi ({kaynak})"
    govde = json.dumps({"key": key, "metin": (hedef / "metin" / f"{key}.md").read_text(encoding="utf-8") if not kuru else "",
                        "baslik": f"{p['kisa']} · Son Prova{' ' + str(p['no']) if key[-1].isdigit() else ''}", "yalnizEma": True})
    uzak = (f"cd {ORACLE} && PW=$(grep -m1 '^MEDSORU_API_PASSWORD=' .env | cut -d= -f2- | tr -d '\"') && "
            "PS=$(grep -m1 '^MEDS_PANEL_SECRET=' .env | cut -d= -f2- | tr -d '\"') && "
            "curl -s -X POST -H 'Content-Type: application/json' -H \"X-API-Password: $PW\" -H \"x-panel-secret: $PS\" "
            "--data-binary @- http://127.0.0.1:3000/api/sesli-anlatim/ders-ekle")
    if kuru:
        return f"{key}: [kuru] ders-ekle"
    r = subprocess.run(["ssh", "medsor-oracle", uzak], input=govde, capture_output=True, text=True, timeout=120)
    return f"{key}: canlı derse → {r.stdout.strip()[:160]}" if '"success":true' in r.stdout else f"{key}: ders-ekle HATA {r.stdout[:200]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kurul", type=int); ap.add_argument("--part"); ap.add_argument("--zorla", action="store_true")
    ap.add_argument("--kuru", action="store_true"); ap.add_argument("--prova", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, str(MEDS / "scripts/takvim")); sys.path.insert(0, str(MEDS / "otomasyon"))
    from aktif_kurul import durum
    du = durum(dt.date.today().isoformat())
    N = a.kurul or du["aktif"]
    if N < 2 and not a.kuru:
        print("Son Prova zinciri Kurul 2+ içindir (Kurul 1 elle kuruldu)."); return 0
    gun = du.get("sinava_gun") if N == du["aktif"] else None
    if not (a.zorla or a.prova or a.kuru) and not (gun is not None and 0 < gun <= SON_PROVA_GUN):
        print(f"Kurul {N}: sınava {gun} gün — Son Prova penceresi değil ({SON_PROVA_GUN} gün kala açılır)"); return 0
    W = hazirla(N)
    if kos(["python3", str(SP / "plan_kurul.py"), "--kurul", str(N), "--kok", str(W)]):
        print("Son Prova planı kurulamadı"); return 1
    plan = json.loads((W / "plan.json").read_text())
    from bildir import bildir
    notlar = []
    if plan.get("sinav_tahmini"):
        notlar.append(f"Sınav dağılımı ders saatinden TAHMİN; fakülte duyurusu src/data/son_prova/k{N}/sinav.json ({{slug: soru}}) olarak yazılmalı.")
    if plan.get("eksik_depo"):
        notlar.append(f"Bilgi deposu olmayan dersler (Son Prova'ya girmedi): {', '.join(plan['eksik_depo'][:20])}")
    partlar = [p for p in plan["partlar"] if not a.part or p["key"] == a.part][: 1 if a.prova else None]
    hata, biten, sonuc = 0, [], []
    basla = dt.datetime.now()
    for p in partlar:
        P = W / "parca" / p["key"]; iz = part_izi(p)
        if (dt.datetime.now() - basla).total_seconds() > BUTCE_SAAT * 3600 and not a.part:
            sonuc.append(f"süre bütçesi ({BUTCE_SAAT:g} sa) doldu: kalan partlar sonraki gece"); break
        if not a.zorla and (P / "iz.txt").exists() and (P / "iz.txt").read_text() == iz and (W / "cikti" / p["key"] / "asamalar.json").exists():
            biten.append(p); continue
        if (P / "iz.txt").exists() and (P / "iz.txt").read_text() != iz:  # ders kümesi değişti: eskiyi sakla, baştan yaz
            eski = W / "_eski" / f"{p['key']}-{dt.datetime.now():%Y%m%d%H%M}"; eski.parent.mkdir(exist_ok=True)
            shutil.move(str(P), str(eski)); P.mkdir(parents=True)
        print(f"▶ {p['key']}: {len(p['dersler'])} ders · hedef {p['hedef_kelime']} kelime", flush=True)
        if part_yaz(p, W, a.kuru):
            hata += 1; sonuc.append(f"{p['key']}: kapı geçmedi (yayına girmedi)"); continue
        if kos(["python3", str(W / "derle.py"), p["key"]], a.kuru, cwd=W):
            hata += 1; sonuc.append(f"{p['key']}: derle HATA"); continue
        if not a.prova and kos(["node", str(SP / "pdf_kirp.mjs"), str(W / "cikti" / p["key"] / "kirp.json")], a.kuru, cwd=MEDS):
            hata += 1; sonuc.append(f"{p['key']}: özet PDF HATA"); continue
        if not a.kuru:
            (P / "iz.txt").write_text(iz)
        biten.append(p)
    if a.prova or a.kuru:
        print(f"PROVA/KURU bitti: {len(biten)} part · {hata} HATA (src/data, data/ ve Oracle'a dokunulmadı)"); return 1 if hata else 0
    if biten and len(biten) == len([p for p in plan["partlar"] if not a.part or p["key"] == a.part]):
        if kos(["python3", str(W / "soru_dagit.py")], cwd=W):
            hata += 1; sonuc.append("soru_dagit HATA (sorular yayına girmedi)")
        else:
            s = subprocess.run(["systemd-run", "--user", "--scope", "-q", "-p", "CPUQuota=300%", "-p", "MemoryMax=2200M", "--nice=10",
                                "env", "CUDA_VISIBLE_DEVICES=", "EMA_IS_PARCACIGI=3", f"SON_PROVA_KOK={W}", str(EMA_PY),
                                str(SP / "yeni_ses.py"), *[p["key"] for p in biten]])
            if s.returncode:
                hata += 1; sonuc.append("yeni soru sesleri (EMA) HATA")
            for p in biten:
                isaret = W / "cikti" / p["key"] / "canli.txt"
                if isaret.exists() and isaret.read_text() == part_izi(p):
                    continue
                r = canliya(p, N, W, False); sonuc.append(r)
                if "HATA" not in r and "gönderilemedi" not in r:
                    isaret.write_text(part_izi(p))
                else:
                    hata += 1
    elif biten:
        sonuc.append("tüm partlar hazır değil: sorular ve canlı yayın bekletildi (yarım Son Prova yayınlanmaz)")
    rapor = "\n".join(notlar + sonuc) or "değişiklik yok"
    print(rapor)
    if hata or notlar or sonuc:
        bildir(f"Kurul {N} Son Prova: {len(biten)}/{len(plan['partlar'])} part hazır, {hata} HATA", rapor, hedef="son-prova")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
