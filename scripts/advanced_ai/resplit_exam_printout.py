#!/usr/bin/env python3
"""
Sınav sistemi çıktısını ("combinepdf (28)", sinav.karabuk.edu.tr analiz sayfaları) KURALLA yeniden böler.

Dil modeliyle bölmede sınır kaçınca birden çok soru kökü/şık tek soruda birleşmişti. Tablo yapısı:
    <Ders> / <Ders> (aynı satır iki kez) / <Konu (1–3 satır)> / <Soru kökü … ?> / "No" | "Sıra No"
    / <şıklar — sarılmış satırlar, ayırıcı yok> / <öğrencinin cevabı: kırpılmış dar sütun parçaları>
Kurallar:
  * Soru başlangıcı: art arda iki AYNI satır ve bu satır bilinen bir ders adı (dosyadaki tekrar sıklığından çıkarılır).
  * Kök: konu satırlarından sonra "?" ile biten satıra kadar; "No"/"Sıra No" başlığı kökü kapatır.
  * Şıklar: yeni şık = büyük harf/rakamla başlayan satır VE (önceki satır noktayla bitiyor ya da önceki satır ≤ 28
    karakterlik tek satırlık şık); küçük harfle başlayan satır öncekine eklenir.
  * Öğrenci cevabı sütunu: şık bloğundan sonra gelen ve bir şıkkın başı olan ≤ 12 karakterlik kırpılmış satırlar → atılır
    (öğrencinin seçimi olarak ayrıca kaydedilir; DOĞRU CEVAP DEĞİLDİR).
  * Geçerlilik: 4–5 şık, kök ≥ 25 karakter ve "?" / soru kalıbı içerir, şıklarda başka soru yok. Geçmeyen atılır.
Çıktı: $MEDS_DATABASE_DIR/derived/resplit/combinepdf_sorular.jsonl (+ rapor.json). Kaynak veriye yazmaz.
Cevap anahtarı yok → hakem "anahtar" kuyruğu slayt kanıtıyla doğrular.
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase8_curriculum_graph as P8  # noqa: E402

SRC = "c4259dc9087e"
OUT = P8.DB / "derived" / "resplit"
HEADER = re.compile(r"^(No|S[ıi]ra No|Duru|Durum|Du|,|\+|[-]+|\d{1,2}\.\d{1,2}\.\d{4}|\d{4}/\s*\S+/\s*\S+|"
                    r"s[ıi෈]nav\.karab.*|https?://.*|.*\.html)$", re.I)
QWORD = re.compile(r"\?\s*$|hangisi|nedir\s*$|değildir\s*$|doğrudur\s*$|yanlıştır\s*$", re.I)


JUNK_IN = re.compile(r"S[ıi]nav Karnesi|T[ıi]klay[ıi]n[ıi]z|s[ıi]nav\.karab|Sonucu \||Anasayfa|D[öo]nem \d Kurul \d|[\uf000-\uf8ff]", re.I)
JUNK_TAIL = re.compile(r"\s*(\bhttps?\S*|s[ıi\u0dc8\u0d88]?n?a?v?\.?k?a?r?\S*karab\S*|s[ıi\u0dc8\u0d88]nav\.?\S*|\bs[ıi]n?$|[\uf000-\uf8ff]+)\s*$", re.I)
# Sayfa altı menüsü ve öğrenci adı (KİŞİSEL VERİ): bu satırları içeren soru tamamen atılır
PERSONAL = re.compile(r"^(Ogrenci|Öğrenci|İşlemler|Islemler)$|^[A-ZÇĞİÖŞÜ]{2,}( [A-ZÇĞİÖŞÜ]{2,}){1,3}$")


def lines_of(text: str) -> list[str]:
    # "Farmakolojඈ" → "Farmakoloji"; bu dosyada "fi" bitişik harfi "Õ" olarak çıkmış (Õ Türkçede yok)
    text = text.replace("\u200f", "").replace("\u200e", "").replace("\u0dc8", "i").replace("\u0d88", "i").replace("Õ", "fi")
    # kelime içi bitişik harf glifleri: "İnÖamatuar"/"İn#amasyon" → fl, "Diàüz" → ff (Türkçede kelime içi büyük Ö yok)
    text = re.sub(r"(?<=[a-zçğıöşü])[Ö#](?=[a-zçğıöşü])", "fl", text)
    text = re.sub(r"(?<=[a-zçğıöşü])à(?=[a-zçğıöşü])", "ff", text)
    text = re.sub(r'(?<=[a-zçğıöşü])"(?=[a-zçğıöşü])', "fi", text)               # "Dermato"tik" → "Dermatofitik"
    text = re.sub(r"\s+https?:?/*\S*\s*$", "", text, flags=re.M)
    return [JUNK_TAIL.sub("", l).strip() for l in text.split("\n")]


def main():
    chunks = [c for c in P8.read_jsonl(P8.DB / "chunks" / f"{SRC}.jsonl")]
    chunks.sort(key=lambda c: (c.get("page") or 0))
    all_lines = []
    for c in chunks:
        for l in lines_of(c.get("text") or ""):
            all_lines.append((l, c.get("page")))
    # ders adları: art arda iki kez geçen kısa satırlar (≥ 5 kez)
    pair = collections.Counter(a for (a, _), (b, _) in zip(all_lines, all_lines[1:]) if a and a == b and len(a) <= 40)
    dersler = {d for d, n in pair.items() if n >= 5 and not HEADER.match(d)}
    starts = [i for i in range(len(all_lines) - 1) if all_lines[i][0] in dersler and all_lines[i + 1][0] == all_lines[i][0]]
    # konu satırları: ders çiftinden hemen sonra gelen ve dosyada ≥ 2 kez aynı konumda tekrar eden satır dizileri
    pos = collections.Counter()
    for st in starts:
        for k in range(1, 4):
            pos[tuple(all_lines[j][0] for j in range(st + 2, min(st + 2 + k, len(all_lines))))] += 1

    def konu_len(st: int) -> int:
        best = 0
        for k in range(1, 4):
            seq = tuple(all_lines[j][0] for j in range(st + 2, min(st + 2 + k, len(all_lines))))
            if pos[seq] >= 2 and not any(QWORD.search(x) for x in seq):
                best = k
        return best or 1
    out, stats = [], collections.Counter()
    for si, st in enumerate(starts):
        end = starts[si + 1] if si + 1 < len(starts) else len(all_lines)
        kl = konu_len(st)
        konu = " ".join(all_lines[j][0] for j in range(st + 2, st + 2 + kl))
        block = [(l, p) for l, p in all_lines[st + 2 + kl:end]]
        ders, page = all_lines[st][0], all_lines[st][1]
        body = [l for l, _ in block if l and not HEADER.match(l) and not JUNK_IN.search(l)]
        # kök sonu: "?" ya da soru kalıbıyla biten ilk satır (en çok 14 satır içinde)
        qend = next((k for k, l in enumerate(body[:16]) if l.rstrip().endswith("?")), None)
        if qend is None:
            qend = next((k for k, l in enumerate(body[:16]) if QWORD.search(l)), None)
        if qend is None:
            stats["kok_sonu_yok"] += 1
            continue
        head = body[:qend + 1]
        stem = " ".join(head)
        stem = re.sub(r"\s+", " ", stem).strip()
        rest = body[qend + 1:]
        opts: list[str] = []
        for l in rest:
            if not opts:
                opts.append(l)
                continue
            prev = opts[-1]
            starts_new = bool(re.match(r"^[A-ZÇĞİÖŞÜ0-9(%<>≤≥]", l))
            if starts_new and (prev.endswith(".") or len(prev) <= 28 or prev.endswith(")")):
                opts.append(l)
            else:
                opts[-1] = prev + " " + l
        # kök şıkka taşmışsa ("artmaz? SLE"): "?"e kadar olan kısım köke
        if opts and "?" in opts[0]:
            before, after = opts[0].split("?", 1)
            stem = (stem + " " + before.strip() + "?").strip()
            opts[0] = after.strip()
            if not opts[0]:
                opts.pop(0)
        # kırpılmış öğrenci-cevabı parçalarını ayıkla: ≤ 12 karakter ve bir şıkkın başı
        clean, student = [], []
        for o in opts:
            if any(x != o and x.startswith(o) for x in opts):          # kırpılmış öğrenci-cevabı parçası
                student.append(o)
                continue
            clean.append(o)
        # öğrenci cevabı tam metin olarak da tekrar edebilir: son öğe önceki bir şıkla aynıysa at
        while len(clean) > 5 and clean[-1] in clean[:-1]:
            student.append(clean.pop())
        if len(clean) > 5:                    # sarılma belirsiz: tahmin yerine soru atılır (yanlış şık üretmemek için)
            stats["sik_sayisi_belirsiz"] += 1
            continue
        bad_opt = any(("?" in o) or re.search(r"\bhangisi|\başağıdaki", o, re.I) for o in clean)
        if any(PERSONAL.match(o.strip()) and not re.search(r"\d|[a-zçğıöşü]", o) and len(o) <= 40 and len(o.split()) >= 2
               or o.strip() in ("Ogrenci", "Öğrenci", "İşlemler") for o in clean):
            stats["kisisel_veri_menu"] += 1
            continue
        ok = (4 <= len(clean) <= 5 and len(stem) >= 25 and not bad_opt and len(set(clean)) == len(clean)
              and re.match(r"^[A-ZÇĞİÖŞÜ0-9(“\"']", stem) is not None and QWORD.search(stem) is not None)
        if not ok:
            stats["gecersiz"] += 1
            continue
        qid = "rs-" + hashlib.sha1((stem + "|".join(clean)).encode()).hexdigest()[:12]
        out.append({"soru_id": qid, "kaynak": SRC, "sayfa": page, "ders": ders, "konu": konu, "stem": stem,
                    "options": {"ABCDE"[i]: o for i, o in enumerate(clean)},
                    "ogrenci_cevabi_parca": student[:3], "cevap": None, "cevap_durumu": "dogrulanmadi",
                    "yontem": "kural_tablo_ayristirma"})
        stats["gecerli"] += 1
    seen, uniq = set(), []
    for r in out:
        k = P8.fold(r["stem"])[:120]
        if k in seen:
            stats["yinelenen"] += 1
            continue
        seen.add(k)
        uniq.append(r)
    OUT.mkdir(parents=True, exist_ok=True)
    if not uniq:
        print("geçerli soru yok; önceki çıktı korunuyor")
        return 1
    tmp = OUT / "combinepdf_sorular.jsonl.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in uniq:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, OUT / "combinepdf_sorular.jsonl")
    rep = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "soru_baslangici": len(starts), "ders_adi": len(dersler),
           "tekil_gecerli": len(uniq), **dict(stats)}
    json.dump(rep, open(OUT / "rapor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
