# Sesli ders ara soruları — "Hocanın sorabileceği soru" (yazar talimatı)

Kullanıcı kararı 2026-10-29, AGENTS.md kural 27. Bundan sonra eklenen **her** derste (branş fark etmez) tam içerik hattının
parçasıdır; mevcut derslere toplu uygulanmaz. LLM adımları yalnız kullanıcı komutuyla (kural 20/22).

## Ne üretilir
- Hoca üslubuna göre soru çıkabilecek slaytın son paragrafı bitince derste ses durur ve **yapay bir soru sayfası** açılır
  (`src/components/canliDers/CdHocaAra.tsx`). EMA soruyu okur (`q-N`), 5 sn düşünme payından sonra doğru cevabı ve çözümü
  söyler (`c-N`; öğrenci kendi seçerse `d-N` ya da "Yanlış." + `s-N-<harf>` + `c-N`), ardından çözümü **önceki slaytlara
  dayanarak** anlatır (`a-N`). Sayfa kapanınca ders bir sonraki slayttan sürer; sayfa yalnız o adımda görünür.
- PDF araç çubuğundaki ünlem (`CdHocaAraDugme`) dersin tüm ara sorularını ardışık okur, çözer, anlatır.
- Aynı sorular ders dışında çözülür: ders sayfası › Soru çöz › "Hocanın sorabileceği sorular" kartı →
  `/soru-cozucu?brans=k<N>hocaara&ders=<kod>&coz=1` (normal çözücü; sesler aynı klipler).
- Öğrenci ders içinde çözmek zorunda değildir: sayfada "Atla", "Derste kendiliğinden göster" anahtarı vardır.

## Kimlikler
- Branş `k<kurul>hocaara`, kod `<kurul>a<sıra>` (k2-07 → `2a07`). Çalışma klasörü `meds_temp/spot_cozucu/k<N>hocaara/`.
- Sesler `data/k<N>hocaara_cozucu/ses/<kod>/` (git dışı), veri `src/data/k<N>hocaara_cozucu/{index,<kod>}.json`.
- Ders sesiyle ara ses ayrı klasör ve ayrı oynatıcıdır; aynı anda çalmaz (ara sayfa açılınca ders duraklar, ders sesi
  başlatılırsa ara ses susar ve sayfa kalkar).

## Akış (sırayla, her kapı 0 HATA)
1. **Önkoşul:** ders `ders-ekle` ile eklenmiş, `data/sesli_anlatim/hizalama/<key>.json` hazır (paragraf → slayt eşlemesi).
2. **Yer seçimi (betik, LLM yok):** `python3 meds/scripts/hoca_profili/profil_oku.py --ders "<ders adı>" --konu "<konu>"` +
   `meds/.venv-ocr/bin/python meds/scripts/hoca_profili/tahmin_girdisi.py <ders.md> --ders … --konu … --cikti <klasör>`.
   Yer = çıkmışla eşleşmiş slayt (`kanit: cikmis`) ya da profilin ilk iki bilgi türüne uyan, `HOCA_TAHMIN_REHBERI.md`
   ile seçilmiş slayt (`kanit: profil`, yazılı gerekçe). Kanıtsız "hoca sorar" damgası yasak (kural 26). Ders başına
   tipik 6–14 soru; slayt başına en çok 2; peş peşe slaytlara yığma.
3. **Kaynak dosyası** `kaynak/<kod>.json` (yazar):
   ```json
   {"ders_adi": "Tıbbi Farmakoloji", "baslik": "<sesli ders başlığı>", "sayfa_metin": {"3": "<slayt 3 metni>", "…": "…"},
    "sorular": [{"ara": {"dosya": 0, "sayfa": 7}, "dayanak": [4, 6, 7], "kanit": "profil",
                 "gerekce": "Hoca bu derste eşik değerleri ve ilaç–yan etki eşleşmesini soruyor; slayt 7 tam bu türden",
                 "kok": "…", "secenekler": {"A": "…", "B": "…", "C": "…", "D": "…", "E": "…"}, "dogru": "C", "zorluk": "orta"}]}
   ```
   - `ara.sayfa` sorunun açılacağı slayt; `dayanak` yalnız o slayt ve öncekiler (ileriye sızıntı = HATA, kural 7).
   - Soru kökü ve çeldiriciler hoca üslubunda (`profil_oku.py` kalıp/düzey/çeldirici stratejisi), Patolojide ayrıca
     `PATOLOJI_HOCA_SORU_MANTIGI.md`. Çeldiriciler aynı dersin **o ana kadar anlatılmış** komşu kavramları; doğru şık en uzun
     olmaz; "hepsi/hiçbiri" yok. Tıbbi bilgi yalnız slayt metninden (kural 4); kaynakta olmayan değer yazılmaz.
4. `python3 meds/scripts/hoca_ara_soru/kur.py iskele <key>` → `cozucu/<kod>_iskelet.json`.
5. **Yazım** `cozucu/<kod>.json` (iskeleti doldur): `TALIMAT_COZUCU.md` biçimi aynen (`kok_ses`, `secenek_ses`, `ipucu`,
   `siklar` {A..E: {metin, ses}}, `cozum`), ek olarak:
   - `anlatim` {metin, ses}: 3–6 cümle, 35–130 kelime. Çözümü dayanak slaytlara **numarasıyla** bağlar
     ("4. slaytta gördüğümüz gibi …", "6. slayttaki tabloda …"); yalnız dayanaktaki slaytlara atıf. Önce sorunun neyi
     ölçtüğü, sonra doğru cevabın slayttaki dayanağı, sonra en güçlü çeldiricinin neden tuzak olduğu. Dolgu, "hoca
     vurguladı" gibi asılsız meta cümle yok (H22); doğal Türkçe (`TURKCE_USLUP_STANDARDI.md`).
   - `siklar`: her şık 2–3 cümle — kavram ne, ne işe yarar, bu soruda neden doğru/yanlış (`SIK_ACIKLAMA_STANDARDI.md`).
6. `python3 meds/scripts/hoca_ara_soru/kur.py dogrula <key>` → 0 HATA (çözücü kapısı + ara kapıları + şık/üslup + profil).
7. **Bağımsız denetçi** (ayrı alt ajan, yalnız kaynak + çıktı): tıbbi doğruluk, tek doğru cevap, açıklamaların kaynağa
   sadakati, ileriye sızıntı. GEÇER olmadan sürmez; yalnız hatalı soru yeniden yazılır.
8. `python3 meds/scripts/hoca_ara_soru/kur.py birlestir <kurul>` (numara = ders akış sırası, `ara.paragraf` hizalamadan).
9. **EMA ses (DAİMA GPU, kural 10):**
   `bash meds/scripts/patoloji_cozucu/cozucu_ses_gpu.sh meds/scripts/spot_cozucu/ses.py --brans k<N>hocaara <kod>`
   (koruyucu kapalıysa açılır; açılamazsa CPU'ya düşülmez, çıkış 75). Sonra yeniden `birlestir` (klipler veriye girer) ve
   `kur.py dogrula <key> --ses` → 0 HATA (her soruda q/i/c/d/a + 5 şık klibi). Sesi eksik ders tamamlanmış sayılmaz.
10. `npx vite build`; yerelde sesli derste soru sayfasını ve ünlem modunu dinleyerek sına; ders sayfasındaki kartı aç.
11. Yayın: git'e işle, `guncelleme_notu.json` `onem`+1, `bash meds/deploy/oracle/dagit.sh`; ses klasörü
    `data/k<N>hocaara_cozucu/ses/` Oracle'a rsync (diğer çözücü sesleriyle aynı yol).

## Uygulamada öğrenilenler (Kurul 2, 2026-10-29)
- Çözücü kapısı `meds_temp/spot_cozucu/k<N>hocaara/pdf_metin/<kod>.md` (PDF sayfa metni, `=== SAYFA n ===`) ister; yazımdan önce oluştur.
- Öğrenciye dönük şık açıklaması ve ipucunda "slayt"/"şık" sözcüğü kapıda HATA; slayt numarası yalnız `anlatim`'da.
- İleriye sızıntı şık açıklamalarında betikle yakalanmaz: denetçi her açıklamayı slayt slayt arar (H436). Ders akış metninden terim/sayı alınmaz (Whisper).
- `ses.py` her `d-N` klibinde "Doğru!" için "süre tutarsız" notu yazar; bilinen ve zararsızdır (öteki çözücülerde de var).
