# 2025-2026 Kurul 3 arşivi — işletim kılavuzu (GİS)

> Kullanıcı kararı 2026-11-17: Drive'daki geçen yıl (2025-2026) Dönem 3 · **Kurul 3** PDF'leri (GİS) sesli ders
> olarak üretilip **2025-2026 arşivine** eklenecek. Kurul 2 arşivinin eşi: `data/arsiv_25_26/`, `meds_database_25_26/`.
> **Öğren destesi YOK, canlı çizim YOK, ara resim/ara soru YOK.** Var olan: ses, cümle/kelime zamanı, PDF metin
> takibi (vurgu + lazer), terim/kısaltma katmanı, çıkmış chip, `.medspak`.
> 2026-2027 veritabanına (`meds_database_v2`, `data/sesli_anlatim`) **dokunulmaz**.

Kaynak klasör: `https://drive.google.com/drive/folders/14kdfK-kz_Tt3A_SAWCXJD1TzOIjmUBv8` (58 PDF)

## Tek kaynak dosyalar
| Ne | Dosya |
|---|---|
| Ders eşlemesi (PDF → anahtar/başlık/branş/program) | `scripts/uretim/arsiv_25_26/k3_eslesme.py` → `meds_database_25_26/kurul3_eslesme.json` |
| Drive envanteri + indirme + önizleme | `scripts/uretim/arsiv_25_26/k3_hazirla.py` |
| Ders hazırlığı (kaynak.md, sayfalar.json, çıkmış aday, onizleme.md) | `scripts/uretim/arsiv_25_26/k3_ders.py hazirla <key>` |
| Metin üretimi (LLM, madde-madde) | `scripts/uretim/arsiv_25_26/k3_uret.py <key>` |
| TSV → konusma_v2 + kapılar | `scripts/uretim/arsiv_25_26/k3_metin.py <key>` |
| Yayın (ses, zaman, işaret, terim, çıkmış, .medspak) | `scripts/uretim/arsiv_25_26/k3_yayinla.py <key>` |

## Neden "madde-madde" üretim
PDF metin takibi (kullanıcı: "geçen derslerde çoğu metni takip edemiyordun", H605) cümle → slayt satırı çapasına
dayanır. Model her cümleyi **slayttaki bir satıra** bağlayarak yazar (`satir` alanı harfi harfine); betik satırı
sayfa metninde doğrular, uymayanı atar. Böylece cümlelerin "yalnız sayfa"ya düşme oranı T5 eşiğinin (%5) altında kalır.

## Bir dersin tam akışı (komutlar)
```bash
cd /home/indu/medsor/meds
# 0) bir kez: envanter + indirme + önizleme
.venv-ocr/bin/python scripts/uretim/arsiv_25_26/k3_hazirla.py envanter
.venv-ocr/bin/python scripts/uretim/arsiv_25_26/k3_hazirla.py indir
.venv-ocr/bin/python scripts/uretim/arsiv_25_26/k3_hazirla.py onizleme
python3 scripts/uretim/arsiv_25_26/k3_eslesme.py yaz

# 1) hazırlık (PDF kopya + kaynak.md + sayfa görüntüleri + çıkmış aday)
.venv-ocr/bin/python scripts/uretim/arsiv_25_26/k3_ders.py hazirla <key>

# 2) metin (elle verilen komut; kural 20) — MEDS_LLM_ELLE=1 ZORUNLU, INVOCATION_ID kaldırılır
env -u INVOCATION_ID MEDS_LLM_ELLE=1 .venv-ocr/bin/python scripts/uretim/arsiv_25_26/k3_uret.py <key>

# 3) kapılar (0 HATA olmadan 4'e geçilmez)
.venv-ocr/bin/python scripts/uretim/arsiv_25_26/k3_yayinla.py <key> --kapi

# 4) yayın: EMA GPU ses + cümle/kelime zamanı + PDF işareti + takip kapısı + terim + çıkmış + .medspak
.venv-ocr/bin/python scripts/uretim/arsiv_25_26/k3_yayinla.py <key>

# 5) durum
.venv-ocr/bin/python scripts/uretim/arsiv_25_26/k3_ders.py durum [<key>]
```

## Kapılar (hepsi 0 HATA)
1. `konusma_v2.py --dogrula` — şema, kimlik, tek cümle, satır çapası birebir, çapasız cümle ≤ %25, Türkçe üslup
2. `metin_denetle.py` — rakam/simge/kısaltma (seslendirme), dolgu/asılsız vurgu, bağlamsız gönderme (H434), kelime sınırı (≤6000)
3. `kapsam` (k3_yayinla) — her içerik sayfası anlatılmış + görselli/şekilli sayfada `slayt.sekil` dolu (görsel anlatılmış)
4. `takip_kapisi.py` (T1–T6) — kelime/cümle zamanı tutarlılığı + PDF işaretinde "yalnız sayfa" oranı ≤ %5
5. `medspak_dogrula.py` — paket içi kimlik/ses/metin özeti tutarlılığı

## Token disiplini (kullanıcı isteği: tekrar üretim yok)
- `kaynak.md` her aşamada yeniden okunmaz: modele **yalnız** o isteğin sayfaları verilir (`--parca-sayfa 5`).
- Üretim önbelleği: `taslak/<key>/uretim.json` — yalnız eksik sayfalar istenir; `--zorla` ile sıfırlanır.
- Çıkmış aday eşlemesi yerel bge-m3 (CPU); model yalnız bu sayfalara düşen adayları görür.
- Aynı ders ikinci kez uçtan uca üretilmez: `k3_yayinla` mevcut sesi metinHash uyuşuyorsa atlar.

## Notlar
- Şekil/görsel anlatımı metinden yapılır (`sekil` tarifi); ayrı ara resim üretilmez (kullanıcı kararı).
- Kısaltma/rakam kuralı: ses metninde rakam ve büyük harfli kısaltma YASAK (EMA harfi harfine okur); model bunu okunuşla yazar.
- Arşiv dersleri `y25-k3-NN-slug` anahtarıyla `data/arsiv_25_26/sesli_anlatim/dersler.json`'a eklenir; sitede
  "Sesli dersler → 2025-2026 (Geçen Yıl Arşivi)" bölümünde Kurul 3 sekmesinde görünür.
