#!/usr/bin/env python3
"""Yönetici bildirimi (panel › bildirimler): Oracle /api/universal-report — ders işçisinin kullandığı yol.
Cihazdan ssh ile Oracle loopback'ine gider; parola sunucunun .env'inden okunur (cihazda saklanmaz).
  from bildir import bildir; bildir("Başlık", "ayrıntı", hedef="otomasyon-hat")
  python3 bildir.py "Başlık" "ayrıntı"
"""
import json, shlex, subprocess, sys


def bildir(baslik: str, ayrinti: str, hedef: str = "otomasyon-hat") -> bool:
    govde = shlex.quote(json.dumps({"targetType": "pipeline", "targetId": hedef, "reason": baslik[:200],
                                    "details": ayrinti[:4000], "reportedBy": "Otomasyon hattı"}, ensure_ascii=False))
    uzak = ("cd /home/ubuntu/medsor/meds && PW=$(grep -m1 '^MEDSORU_API_PASSWORD=' .env | cut -d= -f2- | tr -d '\"') && "
            "curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -H \"X-API-Password: $PW\" "
            f"--data {govde} http://127.0.0.1:3000/api/universal-report")
    try:
        r = subprocess.run(["ssh", "-o", "ConnectTimeout=15", "medsor-oracle", uzak], capture_output=True, text=True, timeout=60)
        ok = r.stdout.strip()[-3:] in ("200", "201")
        if not ok:
            print(f"bildirim yanıtı: {r.stdout[-200:]!r} {r.stderr[-300:]!r}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        ok = False
    if not ok:
        print("bildirim gönderilemedi", file=sys.stderr)
    return ok


if __name__ == "__main__":
    sys.exit(0 if bildir(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "") else 1)
