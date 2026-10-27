#!/usr/bin/env python3
"""Ders işçisi çıktı denetleyicisi: python3 denetle.py <taslak_klasörü>  → çıkış kodu 0 = HATA yok.

Denetimler:
  - Her çıktı dosyası var ve şemaya uygun.
  - KANIT: her `kanit.alinti` `kaynak.md`'nin belirtilen sayfasında (±1 sayfa) kelimesi kelimesine geçiyor
    (Türkçe katlama + boşluk normalize). Geçmeyen kayıt HATA'dır (uydurma bilgi reddedilir).
  - deck.json: /app/scripts/validate_learning_decks.py --oyun-zorunlu 0 HATA (son slayt ders sonu oyunları).
  - sayfa_haritasi.json: her kaynak sayfası tam bir kez; içerik/şekil/tablo sayfası ≥1 adım + ≥1 bilgi_paketi maddesi;
    şekil sayfalarında görsel anlatımı; ana başlık 1–20 içerik adımı, aralıklar sıralı/boşluksuz; her içerik adımı
    bir sayfada; slayt `pdfSayfalari`/`bolum` haritayla tutarlı; `sayfaHaritasi: "teyitli"` yalnız HATA yoksa.
    Sonda ders_ozeti.md derlenir (ozet_derle.py).
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
        _sv = json.loads((d / "sayfalar.json").read_text(encoding="utf-8")) if (d / "sayfalar.json").exists() else []
        self.gorsel_sayfalar = {x["sayfa"] for x in _sv if x.get("goruntu")}
        self.vurgu_sayisi = {x["sayfa"]: sum(1 for v in x.get("vurgulu", []) if v.get("tur") in ("renk", "kalin")) for x in _sv}
        # hafif revize (yalnız "ikisini tut" V2 destesi): ders notu, örnek soru, hastalık, bilgi havuzu üretilmez
        self.hafif = bool(json.loads((d / "baglam.json").read_text(encoding="utf-8")).get("hafif")) \
            if (d / "baglam.json").exists() else False
        # yenileme (2026-10-12): hafif taslağa sonradan ders notu + sitedeki sayı kadar örnek soru üretilir
        self.yenileme = (json.loads((d / "baglam.json").read_text(encoding="utf-8")).get("yenileme") or {}) \
            if (d / "baglam.json").exists() else {}

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
        if isinstance(k, dict) and k.get("gorsel") and not k.get("alinti"):
            # Görsel kanıt (2026-10-20): metni olmayan şekil/mikroskopi sayfası. Yalnız sayfalar.json'da görüntüsü
            # çıkarılmış sayfa için geçerli; onay ekranı ve raporda ayrıca listelenir.
            s = int(k.get("sayfa") or 0)
            if s not in self.gorsel_sayfalar:
                self.hata(f"{yer}: görsel kanıt s.{s} için sayfa görüntüsü yok (sayfalar.json)")
                return False
            if len(str(k["gorsel"]).split()) < 4:
                self.hata(f"{yer}: görsel kanıtta görüleni en az 4 kelimeyle yaz")
                return False
            self.sayilar["gorsel_kanit"] = self.sayilar.get("gorsel_kanit", 0) + 1
            self.referanslar.append(f"{yer}: görsel s.{s} — {str(k['gorsel'])[:100]}")
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

    ICERIK = {"icerik", "sekil", "tablo"}
    BOS = {"kapak", "icindekiler", "kaynakca", "bos", "uyari"}

    def harita_denetle(self, paket: dict, deck):
        """sayfa_haritasi.json: başlık yapısı + teyitli sayfa kaydı (TALIMAT §1b)."""
        h = self.json_oku("sayfa_haritasi.json")
        if not isinstance(h, dict):
            return
        n0 = len(self.hatalar)
        bilgi_no = {b.get("no") for b in paket.get("bilgi_paketi") or []}
        slides = (deck or {}).get("slides") or [] if isinstance(deck, dict) else []
        sn = {s.get("slideNumber"): s for s in slides}
        icerik_adim = [s.get("slideNumber") for s in slides
                       if not (s.get("isCheckpoint") or s.get("isGameFinale") or str(s.get("title", "")).startswith("["))]
        basliklar = h.get("basliklar") or []
        bno = {str(b.get("no")): b for b in basliklar}
        # sayfalar
        goruldu, adim_sayfa, bilgi_sayfa = {}, {}, {}
        for i, s in enumerate(h.get("sayfalar") or []):
            p, tur = s.get("sayfa"), s.get("tur")
            yer = f"sayfa_haritasi s.{p}"
            if p in goruldu:
                self.hata(f"{yer}: iki kez yazılmış")
            goruldu[p] = s
            if tur not in self.ICERIK | self.BOS:
                self.hata(f"{yer}: tur geçersiz ({tur})")
                continue
            if not str(s.get("ne_anlatiliyor") or "").strip():
                self.hata(f"{yer}: ne_anlatiliyor boş")
            if tur in self.BOS:
                # H9 (2026-10-20): görsel ağırlıklı ya da hoca vurgulu sayfa boş/kapak diye atlanamaz
                if (tur == "bos" or (tur == "kapak" and int(p or 0) > 2)) and \
                        (p in self.gorsel_sayfalar or self.vurgu_sayisi.get(p, 0) >= 3):  # gerçek kapak (s.1–2) logolu olur
                    self.hata(f"{yer}: '{tur}' dendi ama sayfa görsel ağırlıklı/hoca vurgulu (sayfalar.json) — "
                              "görüntüyü aç, içerik sayfası olarak anlat")
                if tur in ("bos", "kapak") and len(self.sp.get(p, "").split()) > 60:
                    self.uyarilar.append(f"{yer}: '{tur}' dendi ama sayfada {len(self.sp.get(p, '').split())} kelime var")
                continue
            if str(s.get("baslik")) not in bno:
                self.hata(f"{yer}: baslik '{s.get('baslik')}' basliklar'da yok")
            ad = s.get("adimlar") or []
            if not ad:
                self.hata(f"{yer}: içerik sayfası hiçbir adımda anlatılmıyor (adimlar boş)")
            for a in ad:
                if slides and a not in sn:
                    self.hata(f"{yer}: adım {a} destede yok")
                adim_sayfa.setdefault(a, []).append(p)
            bl = s.get("bilgi") or []
            if not bl:
                self.hata(f"{yer}: hiçbir bilgi_paketi maddesiyle eşlenmemiş (bilgi boş)")
            for b in bl:
                if b not in bilgi_no:
                    self.hata(f"{yer}: bilgi #{b} bilgi_paketi'nde yok")
                bilgi_sayfa.setdefault(b, []).append(p)
            if tur in ("sekil", "tablo"):
                sk = [g for g in s.get("sekiller") or [] if len(str(g).split()) >= 8 or "süs görseli" in str(g).lower()]
                if not sk:
                    self.hata(f"{yer}: şekil/tablo sayfası — sekiller[] boş ya da anlatım <8 kelime (görseller atlanamaz)")
            if len(self.sp.get(p, "").split()) >= 15:
                self.kanit(s.get("kanit"), yer)
        eksik = sorted(set(self.sp) - set(goruldu))
        if eksik:
            self.hata(f"sayfa_haritasi: kayıtsız sayfa(lar): {eksik[:30]}")
        fazla = sorted(set(goruldu) - set(self.sp)) if self.sp else []
        if fazla:
            self.hata(f"sayfa_haritasi: kaynakta olmayan sayfa(lar): {fazla[:30]}")
        # bilgi_paketi ↔ sayfa
        for b in paket.get("bilgi_paketi") or []:
            no, ks = b.get("no"), int((b.get("kanit") or {}).get("sayfa") or 0)
            ps = bilgi_sayfa.get(no)
            if not ps:
                self.hata(f"bilgi_paketi #{no}: hiçbir sayfada eşlenmemiş")
            elif ks and not any(abs(ks - p) <= 1 for p in ps):
                self.hata(f"bilgi_paketi #{no}: kanıt s.{ks} ama harita s.{ps} diyor")
        # başlıklar
        ana = [b for b in basliklar if not b.get("ust")]
        if not ana:
            self.hata("sayfa_haritasi: başlık yok")
        if slides:
            sira = {a: i for i, a in enumerate(icerik_adim)}
            beklenen = 0
            for b in ana:
                ar = b.get("adimlar") or []
                if len(ar) != 2 or ar[0] not in sira or ar[1] not in sira:
                    self.hata(f"başlık {b.get('no')}: adimlar [ilk, son] içerik adımı olmalı ({ar})")
                    continue
                i0, i1 = sira[ar[0]], sira[ar[1]]
                if i0 != beklenen:
                    self.hata(f"başlık {b.get('no')}: aralık {ar} öncekinin hemen ardından başlamıyor (boşluk/çakışma)")
                k = i1 - i0 + 1
                if not 1 <= k <= 20:
                    self.hata(f"başlık {b.get('no')} '{b.get('baslik')}': {k} içerik adımı (1–20 olmalı)")
                beklenen = i1 + 1
            if beklenen != len(icerik_adim):
                self.hata(f"sayfa_haritasi: ana başlıklar içerik adımlarının hepsini kapsamıyor ({beklenen}/{len(icerik_adim)})")
            for b in basliklar:
                u = bno.get(str(b.get("ust"))) if b.get("ust") else None
                if b.get("ust") and not u:
                    self.hata(f"başlık {b.get('no')}: üst başlık '{b.get('ust')}' yok")
                if not (b.get("ozet") or []):
                    self.hata(f"başlık {b.get('no')}: ozet maddeleri yok (ders özeti bundan derlenir)")
            # adım ↔ sayfa
            for a in icerik_adim:
                s = sn[a]
                ps = sorted(adim_sayfa.get(a, []))
                if not ps:
                    self.hata(f"adım {a}: hiçbir PDF sayfasında anlatıldığı yazılmamış")
                    continue
                ex = s.get("pdfSayfalari")
                if ex != [ps[0], ps[-1]]:
                    self.hata(f"adım {a}: pdfSayfalari {ex} ama harita [{ps[0]}, {ps[-1]}] diyor")
                bol = str(s.get("bolum") or "")
                if bol not in bno:
                    self.hata(f"adım {a}: bolum '{bol}' basliklar'da yok")
                sp_ = s.get("sourcePdf") or {}
                if sp_.get("startPage") != ps[0] % 1000 or sp_.get("endPage") != ps[-1] % 1000:
                    self.hata(f"adım {a}: sourcePdf startPage/endPage haritayla aynı değil")
        teyit = isinstance(deck, dict) and deck.get("sayfaHaritasi") == "teyitli"
        if len(self.hatalar) > n0 and teyit:
            self.hata("deck.json: sayfaHaritasi 'teyitli' yazılmış ama harita denetimi HATA veriyor")
        elif len(self.hatalar) == n0 and isinstance(deck, dict) and not teyit:
            self.hata("deck.json: harita denetimi temiz — deste nesnesine \"sayfaHaritasi\": \"teyitli\" ekle")
        self.sayilar["harita_sayfa"] = len(goruldu)
        self.sayilar["baslik"] = len(basliklar)

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
            if not self.hafif or self.yenileme:
                self.hata("ders_notu.md yok")
        else:
            t = nt.read_text(encoding="utf-8")
            if t.count("\n## ") < 3:
                self.hata("ders_notu.md: en az 3 '## ' bölümü olmalı")
            if "SPOT B" not in t.upper():
                self.uyarilar.append("ders_notu.md: SPOT BİLGİLER bölümü yok")

        if (self.d / "deck.json").exists():
            r = subprocess.run([sys.executable, str(APP / "scripts" / "validate_learning_decks.py"), str(self.d / "deck.json")]
                               + ([] if self.yenileme else ["--oyun-zorunlu"])  # yenilemede deste önceden üretilmiş
                               # Kurul 2+: Türkçe üslup + şık açıklama kapıları HATA (AGENTS.md 14); Kurul 1 eski kural
                               + (["--kurul2"] if int((paket or {}).get("kurul") or 0) >= 2 else []),
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

        if not self.yenileme:
            self.harita_denetle(paket if isinstance(paket, dict) else {},
                                self.json_oku("deck.json", False) if (self.d / "deck.json").exists() else None)

        os_ = self.json_oku("ornek_sorular.json", not self.hafif or bool(self.yenileme))
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
                if int((paket or {}).get("kurul") or 0) >= 2:  # H86: Kurul 2+ şık açıklama + Türkçe üslup standardı
                    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
                    from sik_aciklama import denetle as _sik
                    from turkce_uslup import denetle as _uslup
                    for h, v in sa.items():
                        for e in _sik(str(v), f"soru {qid}/{h}") + _uslup(str(v), f"soru {qid}/{h}"):
                            self.hata(e)
                if q.get("zorluk") not in ("kolay", "orta", "zor"):
                    self.hata(f"soru {qid}: zorluk kolay|orta|zor olmalı")
                if not isinstance(q.get("kazanim"), int) or not isinstance(q.get("bilgi"), list):
                    self.hata(f"soru {qid}: kazanim tamsayı, bilgi liste olmalı")
                if len(str(q.get("soru", "")).strip()) < 15:
                    self.hata(f"soru {qid}: soru kökü kısa")
                _kok = str(q.get("soru", "")).lower()
                for _y in ("dersin ", "derste ", "bu derse", "slayt", "bölümüne göre", "notlara göre", "notlarına göre",
                           "hocaya göre", "yukarıdaki bilgi", "anlatıldığına göre", "sunumda", "kazanıma göre"):
                    if _y in _kok:
                        self.hata(f"soru {qid}: kökte ders/slayt göndermesi yasak ('{_y.strip()}'); soru bağımsız sınav sorusu olmalı (H119)")
                        break
                self.kanit(q.get("kanit"), f"soru {qid}")
                per.setdefault(q.get("kazanim"), []).append(q.get("zorluk"))
            for k, zs in per.items():
                if not 3 <= len(zs) <= (10_000 if self.yenileme else 10):
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

        hs = self.json_oku("hastaliklar.json", not self.hafif)
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

        bh = self.json_oku("bilgi_havuzu.jsonl", not self.hafif)
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
        try:  # ders özeti (maliyetsiz derleme)
            from ozet_derle import derle
            derle(self.d)
        except Exception as e:  # noqa: BLE001
            self.uyarilar.append(f"ders_ozeti.md derlenemedi: {e}")
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
