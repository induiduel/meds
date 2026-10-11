#!/usr/bin/env python3
"""Ders işçisi çıktı denetleyicisi: python3 denetle.py <taslak_klasörü>  → çıkış kodu 0 = HATA yok.

Denetimler:
  - Her çıktı dosyası var ve şemaya uygun.
  - KANIT: her `kanit.alinti` `kaynak.md`'nin belirtilen sayfasında (±1 sayfa) kelimesi kelimesine geçiyor
    (Türkçe katlama + boşluk normalize). Geçmeyen kayıt HATA'dır (uydurma bilgi reddedilir).
  - deck.json: /app/scripts/validate_learning_decks.py 0 HATA.
  - ornek_sorular: kazanım başına 3–10 soru (kolay/orta/zor ≥1, fazlası çoğunlukla orta), A–E tam, doğru A–E,
    her şık ≥20 karakter gerekçeli açıklama, kanıtlı (yayın aracı s16 ile aynı kurallar).
Sonuç ayrıca <klasör>/denetim.json'a yazılır.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
_FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiucgiosuaiu")


def norm(s: str) -> str:
    s = str(s).replace("İ", "i").replace("I", "ı").lower().translate(_FOLD)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def sayfalar(kaynak: str) -> dict[int, str]:
    out, cur, buf = {}, None, []
    for line in kaynak.splitlines():
        m = re.match(r"^=== SAYFA (\d+) ===$", line.strip())
        if m:
            if cur is not None:
                out[cur] = norm("\n".join(buf))
            cur, buf = int(m.group(1)), []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = norm("\n".join(buf))
    return out


class Denetim:
    def __init__(self, d: Path):
        self.d = d
        self.hatalar: list[str] = []
        self.uyarilar: list[str] = []
        self.sayilar: dict[str, int] = {}
        self.referanslar: list[str] = []
        self.sp = sayfalar((d / "kaynak.md").read_text(encoding="utf-8")) if (d / "kaynak.md").exists() else {}

    def hata(self, m):
        self.hatalar.append(m)

    def json_oku(self, ad, gerekli=True):
        p = self.d / ad
        if not p.exists():
            (self.hata if gerekli else self.uyarilar.append)(f"{ad}: dosya yok")
            return None
        try:
            if ad.endswith(".jsonl"):
                return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            self.hata(f"{ad}: JSON okunamadı ({e})")
            return None

    REFERANS_RE = re.compile(r"robbins|guyton|katzung|goodman|harrison|williams|thompson|emery|mandell|murray|jawetz|"
                             r"campbell|who\b|cdc\b|sa[gğ]l[iı]k bakanl|statpearls|ncbi|bookshelf|kılavuz|kilavuz|guideline|"
                             r"nelson|sherris|lippincott|junqueira|moore|netter|ganong|harper|lehninger|kumar|uptodate", re.I)

    def kanit(self, k, yer: str, zorunlu=True) -> bool:
        if isinstance(k, dict) and k.get("referans") and not k.get("alinti"):
            # Referansla tamamlanan/düzeltilen bilgi: kabul, ama onay ekranında ayrıca listelenir
            if not self.REFERANS_RE.search(str(k["referans"])):
                self.hata(f"{yer}: referans tanınan bir standart kaynak değil → \"{str(k['referans'])[:60]}\"")
                return False
            self.sayilar["referans"] = self.sayilar.get("referans", 0) + 1
            self.referanslar.append(f"{yer}: {k['referans']}" + (f" ({k['neden']})" if k.get("neden") else ""))
            return True
        if not isinstance(k, dict) or not k.get("alinti"):
            if zorunlu:
                self.hata(f"{yer}: kanit/alinti yok")
            return False
        a = norm(k["alinti"])
        n = len(a.split())
        if n < 4:
            self.hata(f"{yer}: alıntı çok kısa ({n} kelime)")
            return False
        s = int(k.get("sayfa") or 0)
        for p in (s, s - 1, s + 1):
            if a and a in self.sp.get(p, ""):
                return True
        # Sayfa yanlış verilmişse ama alıntı başka sayfada birebir varsa: uyarı (bilgi doğru, künye yanlış)
        for p, t in self.sp.items():
            if a in t:
                self.uyarilar.append(f"{yer}: alıntı s.{s} değil s.{p}'de")
                return True
        self.hata(f"{yer}: alıntı kaynakta YOK → \"{k['alinti'][:70]}\"")
        return False

    def calistir(self):
        paket = self.json_oku("ders_paketi.json")
        if paket:
            for f in ("id", "kurul", "ders", "konu", "kazanimlar", "bilgi_paketi"):
                if not paket.get(f):
                    self.hata(f"ders_paketi: '{f}' boş")
            for b in paket.get("bilgi_paketi") or []:
                self.kanit(b.get("kanit"), f"bilgi_paketi #{b.get('no')}")
            self.sayilar["bilgi"] = len(paket.get("bilgi_paketi") or [])

        nt = self.d / "ders_notu.md"
        if not nt.exists():
            self.hata("ders_notu.md yok")
        else:
            t = nt.read_text(encoding="utf-8")
            if t.count("\n## ") < 3:
                self.hata("ders_notu.md: en az 3 '## ' bölümü olmalı")
            if "SPOT B" not in t.upper():
                self.uyarilar.append("ders_notu.md: SPOT BİLGİLER bölümü yok")

        if (self.d / "deck.json").exists():
            r = subprocess.run([sys.executable, str(APP / "scripts" / "validate_learning_decks.py"), str(self.d / "deck.json")],
                               capture_output=True, text=True)
            ozet = (r.stdout.strip().splitlines() or [""])[-1]
            if r.returncode != 0 or " 0 HATA" not in ozet:
                self.hata(f"deck.json doğrulayıcı: {ozet}")
                self.hatalar += [ln.strip() for ln in r.stdout.splitlines() if "HATA" in ln][:15]
            deck = self.json_oku("deck.json")
            if isinstance(deck, dict):
                self.sayilar["slayt"] = len(deck.get("slides") or [])
        else:
            self.hata("deck.json yok")

        os_ = self.json_oku("ornek_sorular.json")
        if os_:
            sorular = os_.get("sorular") or []
            per = {}
            for q in sorular:
                qid = q.get("id", "?")
                sec = q.get("secenekler") or {}
                if sorted(sec) != ["A", "B", "C", "D", "E"] or len({norm(v) for v in sec.values()}) != 5:
                    self.hata(f"soru {qid}: şıklar A–E tam ve tekrarsız olmalı")
                if q.get("dogru") not in "ABCDE" or not q.get("dogru"):
                    self.hata(f"soru {qid}: dogru A–E olmalı")
                if len(str(q.get("aciklama", ""))) < 20:
                    self.hata(f"soru {qid}: açıklama çok kısa")
                sa = q.get("sik_aciklamalari") or {}
                kisa = [h for h in "ABCDE" if len(str(sa.get(h, "")).strip()) < 20]
                if kisa:  # yayın (s16) kuralı: her şıkkın gerekçeli açıklaması; "Yanlış. Doğrudur." yetmez
                    self.hata(f"soru {qid}: şık açıklaması eksik/kısa (<20 karakter, gerekçe+sayfa yaz): {''.join(kisa)}")
                if q.get("zorluk") not in ("kolay", "orta", "zor"):
                    self.hata(f"soru {qid}: zorluk kolay|orta|zor olmalı")
                if not isinstance(q.get("kazanim"), int) or not isinstance(q.get("bilgi"), list):
                    self.hata(f"soru {qid}: kazanim tamsayı, bilgi liste olmalı")
                if len(str(q.get("soru", "")).strip()) < 15:
                    self.hata(f"soru {qid}: soru kökü kısa")
                self.kanit(q.get("kanit"), f"soru {qid}")
                per.setdefault(q.get("kazanim"), []).append(q.get("zorluk"))
            for k, zs in per.items():
                if not 3 <= len(zs) <= 10:
                    self.hata(f"kazanım {k}: {len(zs)} soru (3–10 olmalı)")
                elif any(z not in zs for z in ("kolay", "orta", "zor")):
                    self.hata(f"kazanım {k}: kolay/orta/zor her biri en az 1 olmalı")
                elif len(zs) > 3 and zs.count("orta") < max(zs.count("kolay"), zs.count("zor")):
                    self.hata(f"kazanım {k}: fazladan sorular çoğunlukla orta olmalı")
            self.sayilar["soru"] = len(sorular)

        sz = self.json_oku("sozluk.json")
        if sz:
            for i, t in enumerate(sz.get("yeni") or []):
                if not t.get("term") or not t.get("definition"):
                    self.hata(f"sözlük yeni #{i}: term/definition yok")
                self.kanit(t.get("kanit"), f"sözlük '{t.get('term')}'")
            for t in sz.get("zenginlestir") or []:
                self.kanit(t.get("kanit"), f"sözlük zenginleştir '{t.get('key')}'")
            self.sayilar["terim"] = len(sz.get("yeni") or []) + len(sz.get("zenginlestir") or [])

        hs = self.json_oku("hastaliklar.json")
        if isinstance(hs, list):
            for h in hs:
                kan = {(k.get("alan"), k.get("madde")): k for k in h.get("kanitlar") or []}
                for alan, v in h.items():
                    if isinstance(v, list) and alan not in ("kanitlar", "aliases"):
                        for i, _ in enumerate(v):
                            k = kan.get((alan, i))
                            if not k:
                                self.hata(f"hastalık '{h.get('name')}': {alan}[{i}] kanıtsız")
                            else:
                                self.kanit(k, f"hastalık '{h.get('name')}' {alan}[{i}]")
            self.sayilar["hastalik"] = len(hs)

        bh = self.json_oku("bilgi_havuzu.jsonl")
        if isinstance(bh, list):
            for i, b in enumerate(bh):
                if not b.get("varlik") or not b.get("bilgi"):
                    self.hata(f"bilgi_havuzu #{i}: varlik/bilgi yok")
                self.kanit(b.get("kanit"), f"bilgi_havuzu #{i} ({b.get('varlik')})")
            self.sayilar["havuz"] = len(bh)

        cb = self.json_oku("cikmis_baglantilari.json")
        if isinstance(cb, list):
            for c in cb:
                if c.get("ilgili"):
                    self.kanit(c.get("kanit"), f"çıkmış bağ {c.get('soru_id')}")
            self.sayilar["bag"] = sum(1 for c in cb if c.get("ilgili"))

        if not (self.d / "rapor.md").exists():
            self.uyarilar.append("rapor.md yok")

        sonuc = {"hata": len(self.hatalar), "uyari": len(self.uyarilar), "sayilar": self.sayilar,
                 "hatalar": self.hatalar[:200], "uyarilar": self.uyarilar[:200],
                 "referansla_tamamlanan": self.referanslar[:500]}
        (self.d / "denetim.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
        return sonuc


if __name__ == "__main__":
    d = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    s = Denetim(d).calistir()
    for h in s["hatalar"][:60]:
        print("HATA ", h)
    for u in s["uyarilar"][:20]:
        print("UYARI", u)
    print(f"denetim: {s['hata']} HATA · {s['uyari']} UYARI · {s['sayilar']}")
    sys.exit(1 if s["hata"] else 0)
