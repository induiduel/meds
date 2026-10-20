#!/usr/bin/env bash
# deploy/oracle/servis_isci.sh — Yönetim › Sistem servis denetiminin Oracle HOST işçisi.
#
# Konteyner (meds-app) host systemctl/docker çalıştıramaz; panel isteği dosyaya yazar, bu betik uygular:
#   istek : /home/ubuntu/medsor/meds/data/servis_kontrol/istekler/<id>.json  {id, service, action}
#   sonuç : .../servis_kontrol/sonuclar/<id>.json                           {ok, message, status, at}
#   durum : .../servis_kontrol/durum.json  (beyaz listedeki her birim: durum + son 200 satır günlük)
# Beyaz liste BURADA YENİDEN doğrulanır (sunucu tarafı: src/services/serviceControlRoutes.ts ORACLE_SERVICES;
# ikisi birlikte güncellenir). Liste dışı birim/eylem reddedilir. meds-app/meds-pg/meds-server/meds-tunnel
# asla durdurulmaz (yalnız yeniden başlatma; meds-app 3 sn gecikmeli, yanıt dönsün diye).
#
# Kullanım:  servis_isci.sh isle   → bekleyen istekleri uygula + durum dök (path birimi çağırır)
#            servis_isci.sh durum  → yalnız durum dök (zamanlayıcı dakikada bir çağırır; zararsız)
#
# Kurulum (Oracle):
#   sudo cp deploy/oracle/systemd/meds-servis-isci.{path,service} deploy/oracle/systemd/meds-servis-durum.{service,timer} /etc/systemd/system/
#   sudo systemctl daemon-reload
#   sudo systemctl enable --now meds-servis-isci.path meds-servis-durum.timer
# Sınama: sudo bash deploy/oracle/servis_isci.sh durum && jq '.at' data/servis_kontrol/durum.json
set -euo pipefail
export CUDA_VISIBLE_DEVICES=""
ROOT="${MEDS_SERVIS_KOK:-/home/ubuntu/medsor/meds/data/servis_kontrol}"
MODE="${1:-durum}"
mkdir -p "$ROOT/istekler" "$ROOT/sonuclar"
exec 9>"$ROOT/.kilit"
flock -w 120 9

ROOT="$ROOT" MODE="$MODE" exec python3 - <<'PY'
import json, os, re, subprocess, time, datetime, glob

ROOT = os.environ["ROOT"]; MODE = os.environ["MODE"]
RS = ["restart", "stop", "start"]
# kimlik -> (tür, izinli eylemler)
WL = {
    "meds-app": ("container", ["restart"]),
    "meds-pg": ("container", ["restart"]),
    "meds-server": ("container", ["restart"]),
    "meds-tunnel": ("container", ["restart"]),
    "meds-embed": ("container", RS),
    "meds-ema": ("container", RS),
    "meds-ders-isci": ("container", RS),
    "meds-ders-yayin.timer": ("unit", RS),
    "meds-cumle-zaman.timer": ("unit", RS),
    "meds-arama-paketi.timer": ("unit", RS),
    "meds-pg-yedek.timer": ("unit", RS),
}
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def sh(args, timeout=90):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + ("\n" + p.stderr if p.stderr else "")).strip()
    except Exception as e:
        return 1, str(e)

def clip(text, n=200):
    return "\n".join(l[:500] for l in text.splitlines()[-n:])

def status(sid, with_log=True):
    kind, _ = WL[sid]
    if kind == "container":
        c, out = sh(["docker", "inspect", "-f", "{{.State.Status}}|{{.State.StartedAt}}|{{.State.Health}}", sid], 20)
        if c != 0:
            st = {"active": "unknown", "sub": "bulunamadı", "loaded": False}
        else:
            s, since, health = (out.split("|") + ["", ""])[:3]
            st = {"active": "active" if s == "running" else "inactive", "sub": s, "since": since, "enabled": "", "loaded": True}
            m = re.search(r"\{(\w+)", health or "")
            if m: st["sub"] = f"{s} ({m.group(1)})"
        if with_log:
            st["log"] = clip(sh(["docker", "logs", "--tail", "200", "--timestamps", sid], 30)[1])
    else:
        c, out = sh(["systemctl", "show", sid, "--no-pager", "-p", "ActiveState,SubState,UnitFileState,ActiveEnterTimestamp,LoadState"], 20)
        m = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
        st = {"active": m.get("ActiveState", "unknown"), "sub": m.get("SubState", ""), "enabled": m.get("UnitFileState", ""),
              "since": m.get("ActiveEnterTimestamp", ""), "loaded": m.get("LoadState") != "not-found"}
        if with_log:
            svc = sid[:-6] + ".service" if sid.endswith(".timer") else sid
            st["log"] = clip(sh(["journalctl", "-u", sid, "-u", svc, "-n", "200", "--no-pager", "-o", "short-iso"], 30)[1])
    return st

def dump():
    data = {"at": NOW(), "services": {sid: status(sid) for sid in WL}}
    tmp = os.path.join(ROOT, ".durum.tmp")
    with open(tmp, "w") as f: json.dump(data, f, ensure_ascii=False)
    os.chmod(tmp, 0o644); os.replace(tmp, os.path.join(ROOT, "durum.json"))

def write_result(rid, obj):
    path = os.path.join(ROOT, "sonuclar", f"{rid}.json")
    with open(path + ".tmp", "w") as f: json.dump({**obj, "at": NOW()}, f, ensure_ascii=False)
    os.replace(path + ".tmp", path)

def handle(path):
    name = os.path.basename(path)
    rid = name[:-5]
    try:
        if not re.fullmatch(r"\d+-[0-9a-f]{8}\.json", name) or os.path.getsize(path) > 2048:
            return  # tanınmayan dosya: sonuç yazılmaz, yalnız silinir
        req = json.load(open(path))
        sid, act = str(req.get("service", "")), str(req.get("action", ""))
        if sid not in WL or act not in WL[sid][1]:
            write_result(rid, {"ok": False, "message": f"Reddedildi: {sid} / {act} beyaz listede değil."}); return
        if time.time() - os.path.getmtime(path) > 600:
            write_result(rid, {"ok": False, "message": "İstek 10 dakikadan eski; uygulanmadı."}); return
        kind = WL[sid][0]
        if kind == "container" and sid == "meds-app":
            # Kendini yeniden başlatma: önce sonucu yaz, panel yanıtını alsın; sonra arka planda.
            write_result(rid, {"ok": True, "message": "meds-app 3 sn sonra yeniden başlıyor (~30 sn).", "status": status(sid, False)})
            subprocess.Popen(["/bin/sh", "-c", "sleep 3; docker restart -t 15 meds-app"], start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        args = ["docker", act, sid] if kind == "container" else ["systemctl", act, sid]
        if kind == "container" and act in ("restart", "stop"): args[2:2] = ["-t", "20"]
        c, out = sh(args, 120)
        st = status(sid, False)
        msg = {"restart": "yeniden başlatıldı", "stop": "durduruldu", "start": "başlatıldı"}[act]
        write_result(rid, {"ok": c == 0, "message": f"{sid} {msg}." if c == 0 else f"{sid}: {out[-400:]}", "status": st})
    except Exception as e:
        write_result(rid, {"ok": False, "message": f"İşçi hatası: {e}"})
    finally:
        try: os.remove(path)
        except FileNotFoundError: pass

if MODE == "isle":
    for p in sorted(glob.glob(os.path.join(ROOT, "istekler", "*.json")))[:20]:
        handle(p)
# Eski sonuçları temizle (en yeni 50 kalır)
res = sorted(glob.glob(os.path.join(ROOT, "sonuclar", "*.json")), key=os.path.getmtime)
for p in res[:-50]:
    try: os.remove(p)
    except OSError: pass
dump()
PY
