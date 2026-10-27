# Örnek soru üslubu (kullanıcı kararı 2026-10-28; H119)

Amaç: çıkmış sorulara benzer üslupla yazıp sınavda soru yakalama şansını artırmak. Yazar önce dersin
`soru_uslubu.json` dosyasını okur (`scripts/tam_hat/soru_uslup_ornek.py`; 8 çıkmış örnek + kalıp payları).

## Kök
- Bağımsız, tek başına anlaşılır. "Derste", "slaytta", "hocanın", "bu bölümde", "metne göre", "sayfa N" yok.
- Çıkmış kalıpları: "… aşağıdakilerden hangisidir?", olumsuz kök ("… değildir?", "… beklenmez?"), kısa vaka
  ("45 yaşında kadın hasta …"), öncüllü ("I. … II. … III. … ifadelerinden hangileri doğrudur?").
- Kalıp payları çıkmış paylarına ±10 puan içinde yakın olur; kök uzunluğu çıkmış ortalamasına yakın.
- Her soru bir kazanıma bağlıdır (`kazanim`); slaytın rastgele ayrıntısı sorulmaz.

## Şıklar
- 5 şık, aynı türden (hepsi ilaç, hepsi hastalık …), benzer uzunlukta. Doğru şık en uzun ve belirgin ayrıntılı olmaz
  (k2-08'de 18 soruda bu ipucu bulundu).
- En az 2 güçlü çeldirici, dersin öğretilmiş komşu kavramlarından (sınavın klasik karışıklıkları).
- "Hepsi / hiçbiri" kullanılmaz; açıklamalar `SIK_ACIKLAMA_STANDARDI.md`'ye uyar.

## Kapı
`python3 scripts/tam_hat/soru_uslup.py <ornek_sorular.json> --uslup <soru_uslubu.json>` → 0 HATA. HATA alan soru
yalnız kendisi yeniden yazılır.
