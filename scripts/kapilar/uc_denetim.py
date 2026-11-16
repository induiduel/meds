#!/usr/bin/env python3
"""H596 kapısı: aynı HTTP yöntemi + yol sunucuda iki kez tanımlanamaz (`app.post('/api/x', …)` mükerrerliği).

Neden: Express ilk eşleşen tanımı çalıştırır; ikincisi sessizce ölü kalır. `server.ts`'te `/api/automation/run-full-local-sync`
iki kez tanımlıydı: ilki `requireAdmin`'li, ikincisi YETKİSİZ ve süreç başlatıyordu. İlki bir gün kaldırılsa/yeniden adlandırılsa
yetkisiz kopya canlanırdı. Ayrıca gövde ayrıştırıcılara (express.json/urlencoded) kimlik kademesiz 10 MB üstü genel tavan
konmasını da yakalar (aynı hata kaydı: kimliksiz 100 MB gövde).

  python3 scripts/kapilar/uc_denetim.py          # 0 bulgu = çıkış 0
  python3 scripts/kapilar/kos.py uc
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kok as _kok  # noqa: E402

MEDS = Path(_kok.MEDS)
UC = re.compile(r"""^\s*(?:app|router)\.(get|post|put|patch|delete)\(\s*(['"`])(/[^'"`$]*)\2""")
GENEL_TAVAN = re.compile(r"""^\s*app\.use\(\s*express\.(json|urlencoded)\([^)]*limit:\s*['"](\d+)\s*(kb|mb|gb)['"]""", re.I)
CARPAN = {"kb": 1 / 1024, "mb": 1, "gb": 1024}


def main() -> int:
    dosyalar = [MEDS / "server.ts", *sorted((MEDS / "src" / "services").rglob("*.ts")), *sorted((MEDS / "src").glob("server*.ts"))]
    gorulen: dict[tuple[str, str], list[str]] = defaultdict(list)
    bulgular: list[str] = []
    for yol in dosyalar:
        if not yol.is_file():
            continue
        for no, satir in enumerate(yol.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = UC.match(satir)
            if m:
                gorulen[(m.group(1).upper(), m.group(3))].append(f"{yol.relative_to(MEDS)}:{no}")
            t = GENEL_TAVAN.match(satir)
            if t and int(t.group(2)) * CARPAN[t.group(3).lower()] > 10:
                bulgular.append(f"{yol.relative_to(MEDS)}:{no}: genel express.{t.group(1)} tavanı {t.group(2)}{t.group(3)} "
                                f"(kimlik kademesiz >10 MB yasak; server.ts govdeKademesi kullan)")
    for (yontem, uc), yerler in sorted(gorulen.items()):
        if len(yerler) > 1:
            bulgular.append(f"{yontem} {uc} {len(yerler)} kez tanımlı: {', '.join(yerler)} (yalnız ilki çalışır)")
    for b in bulgular:
        print("HATA", b)
    print(f"uc_denetim: {len(bulgular)} HATA · {len(gorulen)} uç tarandı")
    return 1 if bulgular else 0


if __name__ == "__main__":
    sys.exit(main())
