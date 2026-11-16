# src/data/ — ön yüze paketlenen veri

- Ders kayıt defteri `dersler/` (`k1.json`, `k2.json`, `branslar.json`); branş klasörleri `*_onem/`, `*_cozucu/`, `*_asistan/`.
- Öğren desteleri `interactive_learning_decks.json` (kaynak) → `decks/items/` (üretilir, git dışı).
- Dev JSON'lar: `pastQuestions.json`, `lecture_notes.json`, `sinav_calisma_k1.json`, `kazanimlar/k1.json`.

## Kurallar
- Sunucu buraya yalnız içerik katmanıyla yazar (`writableContent`, H580/H581; ayrıntı `src/services/CLAUDE.md`).
- Kapı: `python3 scripts/validate_learning_decks.py` 0 HATA (deste); `python3 scripts/kapilar/yapi_koruma.py` 0 HATA.

## Büyük veri dosyaları (2026-11-16)

Tek-satır dev JSON'lar ripgrep aramasından gizlidir (`.ignore`, `src/data/.ignore`, `data/.ignore`; runtime'a etkisi yok) —
eskiden tek terim araması 146 MB döndürüyordu. Bunları **asla bütün okuma**; yolu açıkça verip `jq` ile dilimle:
`src/data/pastQuestions.json` (97 MB), `interactive_learning_decks.json` (85 MB; deste başı okunur kopya derlemede
`src/data/decks/items/<id>.json`), `sinav_calisma_k1.json`, `lecture_notes.json`, `kazanimlar/k1.json`, `data/local_rag_chunks.json`.
Örnek: `jq '.[] | select(.id=="X")' src/data/pastQuestions.json`, `jq 'keys' src/data/lecture_notes.json | head`.
**Desteler tek depodan:** Python `scripts/deste_deposu.py` (`hepsi/oku/duzenle/guncelle/sil`, atomik + kilit), sunucu
`src/services/desteDeposu.ts` (`desteleriOku/desteOku/desteleriYaz`, içerik katmanı üzerinden). Deste dosyasını doğrudan açan
yeni kod YAZMA; fiziksel bölme gerekirse yalnız bu iki modülün arka ucu değişir. lecture_notes: etkin yazıcılar `data/lecture_notes.json`'a yazar.
