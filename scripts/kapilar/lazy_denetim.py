#!/usr/bin/env python3
"""H588 kapısı: src altında `React.lazy(` / çıplak `lazy(` yalnız src/utils/guvenliLazy.tsx içinde geçer.

Neden: `vite:preloadError` dinleyicisi preventDefault() çağırınca Vite başarısız parça içe aktarımını `undefined` ile
çözer; çıplak React.lazy boş modülle çöker (`e._result.default`, React #306). Tüm tembel bileşenler `guvenliLazy`
kullanmalı. 0 bulgu = çıkış 0, bulgu = çıkış 1.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kok as _kok  # noqa: E402

SRC = Path(_kok.MEDS) / "src"
IZINLI = SRC / "utils" / "guvenliLazy.tsx"
DESEN = re.compile(r"React\.lazy\s*\(|(?<![.\w])lazy\s*\(\s*(?:\(\)|[A-Za-z_])")
YORUM = re.compile(r"^\s*(//|\*|/\*)")


def main() -> int:
    bulgular = []
    for yol in sorted(SRC.rglob("*.ts*")):
        if yol.suffix not in (".ts", ".tsx") or yol == IZINLI:
            continue
        for no, satir in enumerate(yol.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if YORUM.match(satir):
                continue
            if DESEN.search(satir):
                bulgular.append(f"{yol.relative_to(_kok.MEDS)}:{no}: {satir.strip()[:140]}")
    for b in bulgular:
        print("HATA", b)
    print(f"lazy_denetim: {len(bulgular)} HATA (React.lazy yerine utils/guvenliLazy kullanın)")
    return 1 if bulgular else 0


if __name__ == "__main__":
    sys.exit(main())
