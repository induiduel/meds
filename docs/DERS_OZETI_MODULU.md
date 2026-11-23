# Ders Özeti modülü (Kurul 2+) — tasarım ve veri biçimi

Kullanıcı isteği (2026-11-23): her dersin özeti ve "akılda kalması gerekenler". Özet, çıkmış ve çıkabilecek bilgileri,
slaytta vurgulananları, tıbben önemli ve ayırıcı/karakteristik (spot) bilgileri derler. Özete çalışan öğrenci dersin
bütün sorularını çözebilmeli ama metin özet kalmalı. Sesli dinlenir, sonunda sorular sesli çözülür.

Adres: **Ders çalış › Ders özeti** — `/dersler/ders-ozeti[/kurul<N>[/<ders>]]` (iç `/ders-ozeti[/<ders>]?kurul=N`, route `ders_ozeti`).

## Hat (yalnız elle komutla, kural 20; LLM işi bu oturumda alt ajanla)
| Adım | Komut | Çıktı |
|---|---|---|
| 1. Topla (read-once) | `python3 scripts/uretim/ders_ozet/topla.py <k>` | `meds_temp/ders_ozet/<k>/girdi.json` |
| 2. Yaz (alt ajan) | `scripts/uretim/ders_ozet/TALIMAT.md` | `meds_temp/ders_ozet/<k>/ozet.json` |
| 3. Kapı | `python3 scripts/uretim/ders_ozet/dogrula.py <k>` → **0 HATA** | — |
| 4. Bağımsız denetçi (yazar dışı alt ajan) | karar GEÇER/KALIR | `meds_temp/ders_ozet/<k>/denetim.json` |
| 5. Ses (EMA, DAİMA GPU) | `bash scripts/uretim/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/uretim/ders_ozet/ses.py <k>` | `data/k<N>ozet_cozucu/ses/<kod>/` |
| 6. Yayın | `python3 scripts/uretim/ders_ozet/yayinla.py <k>` (kapı + GEÇER + ses tam değilse yazmaz) | `src/data/ders_ozet/k<N>/` |

Girdi katmanları (yeniden kullanılır, yeni veri uydurulmaz): slayt metni `meds_temp/ogrenci_ders/<k>/sayfalar.json` (birincil),
doğrulanmış çıkmış `data/sesli_anlatim/cikmis_konum/<key>.json`, çıkmış analizi `src/data/ders_analizi/<k>.json`,
önem `src/data/k<N>*_onem/<kod>.json`, çözücü soruları `src/data/k<N>*_cozucu/<kod>.json`, hoca vurgusu `src/data/hoca_vurgu/`,
öğrenci A/B önem `src/data/ogrenci_onem/`, öğrenci derlemesi `meds_temp/ogrenci_sentez/ders/` (yalnız slaytta karşılığı varsa).

## Veri biçimi
`ozet.json` (yazar): `giris`, `bolumler[{id, baslik, maddeler[{id, tur: bilgi|spot|ayirici|klinik, metin, s[], cikmis[]}]}]`,
`akilda[{metin, s[], cikmis[]}]` (8–15), `cikmis_kapsam{çıkmış id → madde id}`, `onem_kapsam{önem başlığı → madde id}`,
`atlanan_cikmis[{id, gerekce}]`.

Kapı (`dogrula.py`): her madde geçerli slayt sayfasına bağlı; her doğrulanmış çıkmış bir maddeyle kapsanır ya da gerekçeyle
atlanır (en çok %20); puanı 85+ önem maddelerinin hepsi kapsanır; bölüm 4–12, madde 3–12/bölüm, madde 6–45 kelime,
toplam 500–2500 kelime; yasak işaret/markdown, iç süreç dili ve `turkce_uslup` yok; "hoca vurguladı" en çok 3.

Yayın `src/data/ders_ozet/k<N>/<k>.json`: ekran verisi + `cikmis[]` (kök/cevap) + `cozucu{brans, kod, soru, cikmis}` +
`ses{brans, kod, klipler{klip: {v, sure, oge{öğe id: [bas, son]}}}}`; `index.json` ders listesi.

## Ses
Klip başına bir bölüm: `g` giriş, `b-i` i. bölüm (başlık + maddeler), `a` akılda kalması gerekenler. Ekran metni rakamlıdır;
okunuş `ses_metin` (yol: `k<N>ozet_cozucu`) ile yazıya döner, kısaltmalar `kisaltma_ses.uzat`. Klip üretimi `ses_klip.klasor`
(değişmeyen klip yeniden üretilmez). Sunucu değişikliği yok: `/api/cozucu-ses/k<N>ozet/ema/<kod>/<klip>.mp3`.
Ses dosyaları git dışı (`data/*_cozucu/ses/`); Oracle'a çözücü sesleriyle aynı yoldan taşınır.
Cümle → öğe eşlemesi tek kaynak `ses.klip_cumleleri()` (yayinla.py aynı işlevi kullanır).

## Ekran (`src/components/dersOzet/`)
Liste: branşa göre dersler (madde, çıkmış, sesli süre, soru sayısı). Ders: giriş · "Sesli dinle" · "Sesli soru çöz" (dersin
mevcut çözücüsü, EMA klipli) · "Yalnız çıkmışlar" · bölüm atlama çipleri · maddeler (tür rozeti Spot/Ayırıcı/Klinik,
"Çıkmış" rozeti, slayt sayfası) · Akılda kalması gerekenler · açılır çıkmış soru listesi (kök + cevap). Alt oynatıcı:
önceki/sonraki bölüm, hız (1–1,75×, tarayıcıda hatırlanır), ilerleme; okunan madde işaretlenir ve görünür tutulur;
dinleme başladıktan sonra maddeye dokununca oradan okur.
İlerleme `medsoru_ders_ozet_v1` ({ders: {klip, t, bitti, at}}) profil eşitlemesindedir (`userKvSync` SYNC_PATTERNS + ders başına en yeni `at` birleştirmesi); hesaptan gelen değişiklik `storage` olayıyla ekrana yansır.

## Durum (2026-11-23)
Pilot k2-15 onaylandı; 50 Kurul 2 dersi yayında (2.435 madde, ~7,8 sa ses, denetçi 50/50 GEÇER). Sesli dersi/slayt metni olmayan
dersler (k2-25, 32, 47, 48, 51–57, 59–61, 63) kapsam dışı; sesli dersleri gelince aynı hat (`topla.py` hizalamadaki PDF'i okur).
İlerleme hesaba eşitlenir (2026-11-23, onem 870). Farmakoloji yazımında Opus `[bio]` filtresi → alt ajan `model: sonnet`. Kapı ayrıntıları ve tuzaklar: H646.
