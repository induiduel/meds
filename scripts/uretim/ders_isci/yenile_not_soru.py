"""Revize taslağının YENİ ders notu + örnek sorularını yayına alır (deste, sözlük, bağlar dokunulmaz).

V2 destesi "hafif" yayınlandıktan sonra (2026-10-12, kullanıcı: "yenile") her dersin notu ve örnek soruları 2026-27
PDF'inden yeniden üretildi. Bunlar dersin sürümden bağımsız tek kaydıdır: yenisi V1'inkinin yerine geçer.
Örnek soru setleri sitede ders başına 85–350 soruya genişletilmiş olduğundan s16'nın "kazanım başına 3–10" kuralı
burada "en az 3, her zorluktan en az 1" olarak uygulanır; site dosyası doğrudan yazılır (s16 upsert'i daha çok sorulu
eski seti koruyacağı için kullanılmaz). Önceki hâller yayinla.py yedeğine alınır.

  python3 yenile_not_soru.py <is_id> [<is_id> …] [--deneme]
"""
from __future__ import annotations

import fcntl
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yayinla as Y  # noqa: E402
from yayinla import ROOT, PAKET, YEDEK, oku, s14, s16  # noqa: E402

ZORLUK = s16.ZORLUK


class NotSoru(Y.Yayin):
    def denetle(self, kaynak_id=None) -> bool:  # noqa: ARG002
        b, p = self.b, self.paket
        self.n = int(b.get("numara") or 0)
        self.ders_id = b.get("ders_id") or ""
        if p.get("id") != self.ders_id:
            self.hata.append(f"paket kimliği {p.get('id')} ≠ {self.ders_id}")
        if oku(self.d / "denetim.json", {}).get("hata"):
            self.hata.append("işçi denetimi HATA içeriyor")
        mevcut = dict(enumerate(s14.LESSONS, 1))
        ders, konu, hoca, tarih = (mevcut[self.n][:4] if self.n in mevcut
                                   else (p.get("ders"), p.get("konu"), p.get("ogretim_uyesi"), p.get("tarih") or ""))
        self.kayit = {"ders": ders, "konu": konu, "hoca": p.get("ogretim_uyesi") or hoca, "tarih": p.get("tarih") or tarih or ""}
        nt = self.d / "ders_notu.md"
        if not nt.exists():
            self.hata.append("ders_notu.md yok")
            return False
        md = nt.read_text(encoding="utf-8")
        self.sadakat = s14.fidelity(md, Y._BosDerlem(), [], (self.d / "kaynak.md").read_text(encoding="utf-8"))
        if self.sadakat < s14.SADAKAT_ESIK:
            self.hata.append(f"ders notu sadakati {self.sadakat} < {s14.SADAKAT_ESIK}")
        if len(re.findall(r"^##\s+", md, flags=re.M)) < 3:
            self.hata.append("ders notunda en az 3 bölüm olmalı")
        sor = oku(self.d / "ornek_sorular.json", {})
        cik = s16._cikmislar()
        tum = {q["question_id"] for q in cik} | {q["question_id"] for q in s16._site_cikmislar()}
        for f in sorted(s16.SORU_DIR.glob("*.jsonl")):
            for line in f.read_text(encoding="utf-8").splitlines():
                tum.add(json.loads(line)["question_id"])
        sorun = [x for x in s16._denetle({**p, "kazanimlar": p.get("kazanimlar") or []}, sor, [], tum)
                 if not re.match(r"^K\d+: (\d+) soru \(3-10 olmalı\)$", x) or int(re.match(r"^K\d+: (\d+)", x).group(1)) < 3]
        say = Counter(q.get("kazanim") for q in sor.get("sorular", []))
        for kn in range(1, len(p.get("kazanimlar") or []) + 1):
            z = Counter(q.get("zorluk") for q in sor.get("sorular", []) if q.get("kazanim") == kn)
            if say[kn] > 10 and any(z[x] < 1 for x in ZORLUK):
                sorun.append(f"K{kn}: kolay/orta/zor her biri en az 1 olmalı ({dict(z)})")
        hedef = (b.get("yenileme") or {}).get("soru_hedefi") or 0
        # Hedef = sitedeki eski setin sayısı. Kaynakta bilgi biterse ajan dolgu/tekrar soru yazmaz: eksik kalırsa not
        # düşülür (raporlanır); %60'ın altı ise üretim yarım kalmış sayılır.
        adet = len(sor.get("sorular", []))
        if hedef and adet < int(hedef * 0.6):
            sorun.append(f"soru sayısı {adet} < hedefin %60'ı ({hedef})")
        elif hedef and adet < hedef:
            self.not_.append(f"soru {adet}/{hedef} (kaynak bilgisi tükendi; dolgu yazılmadı)")
        self.hata += [f"örnek soru: {x}" for x in sorun[:15]]
        if not p.get("kazanimlar"):
            self.hata.append("ders paketinde kazanım yok")
        return not self.hata

    def yaz(self):
        p, n, did = self.paket, self.n, self.ders_id
        md = (self.d / "ders_notu.md").read_text(encoding="utf-8")
        # ders paketi (+ dizin)
        eski_paket = oku(PAKET / f"{did}.json", {})
        paket = {**eski_paket, **p, "gecen_yil_kaynagi": False, "ders_notu": md, "kaynak": "ders_isci_revize",
                 "is_id": self.d.name, "ogrenim_slaytlari": eski_paket.get("ogrenim_slaytlari") or p.get("ogrenim_slaytlari") or []}
        self._yaz(PAKET / f"{did}.json", paket)
        idx = [x for x in oku(PAKET / "index.json", []) if x.get("id") != did]
        idx.append({"sira": n, "id": did, "ders": self.kayit["ders"], "konu": self.kayit["konu"], "ogretim_uyesi": self.kayit["hoca"],
                    "tarih": self.kayit["tarih"], "gecen_yil": False, "kazanim": len(p.get("kazanimlar") or []),
                    "bilgi_paketi": len(p.get("bilgi_paketi") or []), "ozet_kelime": len(json.dumps(p.get("ders_ozeti") or {}).split()),
                    "not_karakter": len(md), "kaynak_kapsama": None, "dosya": f"{did}.json", "sorunlar": []})
        self._yaz(PAKET / "index.json", sorted(idx, key=lambda x: x["sira"]))
        # ders notu: çalışma dosyası + site özet kayıtları
        for e in s14.WORK.glob(f"{n:02d}_*.md"):
            self._yedekle(e)
            e.unlink()
        self._yaz_metin(s14.WORK / f"{n:02d}_{s14._slug(self.kayit['konu'])}.md", s14.textnorm.nfc(md).strip() + "\n")
        self._not_kayitlari(md)
        # örnek sorular: s16 çalışma kopyası + site dosyası (doğrudan, eski set yedekte)
        sor = oku(self.d / "ornek_sorular.json", {}).get("sorular", [])
        self._yaz(s16.YAZIM_DIR / f"{did}.json", {"sorular": sor})
        by_id = {q["question_id"]: q for q in s16._cikmislar()}
        for q in s16._site_cikmislar():
            by_id.setdefault(q["question_id"], q)
        kaz = []
        for ki, metin in enumerate(p["kazanimlar"], 1):
            qs = sorted((q for q in sor if q["kazanim"] == ki), key=lambda q: ZORLUK.index(q["zorluk"]))
            ilgili = [i for i in dict.fromkeys(c for q in qs for c in q.get("benzer_cikmis") or []) if i in by_id]
            kaz.append({"no": ki, "metin": metin, "sorular": qs, "ilgili_cikmis": [
                {"id": i, "soru": by_id[i]["stem"], "secenekler": by_id[i].get("options") or {}, "cevap": by_id[i].get("answer")}
                for i in ilgili]})
        site = {"id": did, "sira": n, "kurul": 1, "ders": self.kayit["ders"], "konu": self.kayit["konu"],
                "ogretim_uyesi": self.kayit["hoca"], "tarih": self.kayit["tarih"], "soru_sayisi": len(sor), "kazanimlar": kaz}
        self._yaz(s16.SITE_DIR / f"{did}.json", site)
        sidx = {x["id"]: x for x in oku(s16.SITE_DIR / "index.json", [])}
        sidx[did] = {k: site[k] for k in ("id", "sira", "ders", "konu", "ogretim_uyesi", "soru_sayisi")} | {"kazanim": len(kaz)}
        self._yaz(s16.SITE_DIR / "index.json", sorted(sidx.values(), key=lambda x: x["sira"]))


def main() -> int:
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    deneme = "--deneme" in sys.argv
    kilit = open(ROOT / "ders_isci" / ".yayin.lock", "w")
    fcntl.flock(kilit, fcntl.LOCK_EX)  # yayinla.py ile aynı kilit: kaynak dosyalara tek yazar
    yedek = YEDEK / ("notsoru_" + time.strftime("%Y%m%d_%H%M%S"))
    kod = 0
    for iid in ids:
        d = ROOT / "ders_isci" / "taslak" / iid
        y = NotSoru(d, deneme, yedek)
        ok = y.denetle()
        print(f"== {iid} · {y.ders_id} · sadakat {getattr(y, 'sadakat', '?')} · {'TAMAM' if ok else 'HATALI'}")
        for h in y.hata:
            print("  HATA", h)
        if not ok:
            kod = 1
            continue
        if deneme:
            continue
        y.yaz()
        ky = oku(d / "yayin.json", {}) or {}
        ky["not_soru"] = {"zaman": datetime.now().isoformat(timespec="seconds"), "sadakat": y.sadakat,
                          "soru": len(oku(d / "ornek_sorular.json", {}).get("sorular", [])), "yedek": str(yedek)}
        Y.yaz_json(d / "yayin.json", ky)
    return kod


if __name__ == "__main__":
    sys.exit(main())
