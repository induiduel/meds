# Hastalıklar bilgi tabanı — veri modeli (şema 2)

Kaynak dosya: `src/data/diseases.json` (tek doğruluk kaynağı). Tipler: `src/types/disease.ts`.
Ortak yardımcılar (tarayıcı + sunucu): `src/services/diseaseModel.ts`. JSON Schema: `$MEDS_DATABASE_DIR/schema/disease.schema.json`.

## Neden madde (fact) modeli?

Eski profiller düz metin dizileriydi ve alanların çoğu tüm hastalıklarda aynı şablon cümleydi
("Standart medikal protokol ve klinik rehber kılavuzları"). Şema 2'de her bilgi bir nesnedir:

```json
{ "label": "Akıntı", "text": "Bol, ==köpüklü, sarı-yeşil== ve kötü kokulu vajinal akıntı.", "key": true,
  "entities": [{ "name": "vajinal akıntı", "type": "belirti", "qualifier": "köpüklü, sarı-yeşil" }] }
```

- `text`: tek bilgi; `==terim==` arayüzde fosforlu kalemle vurgulanır.
- `label`: kalın alt başlık. `key`: sınavda sorulan kritik bilgi ("Sınav" işareti, ★).
- `entities`: maddedeki tıbbi varlıklar. Bölümle birlikte okunur: `symptoms` bölümündeki `belirti:ateş` = "bu hastalık ateş yapar".
  Böylece "ateş yapan hastalıklar", "metronidazolle tedavi edilenler", "VHL geniyle ilişkili olanlar" veriden çıkar.
- `source`: ders notundan alınan maddede kaynak dosya (`lecture` bölümünde zorunlu).

## Profil

| alan | açıklama |
|---|---|
| `kind` | `hastalik`, `bulgu`, `patolojik_surec`, `mekanizma`, `molekul_hucre`, `ilac`, `kavram`, `yontem` — bölüm başlıkları türe göre değişir (`sectionTitle`) |
| `category` | sabit uzmanlık listesi (`DISEASE_CATEGORIES`) |
| `hallmarks` | karakteristik özellik ("Çilek serviks", "Reed-Sternberg hücresi") |
| `sections` | `definition, etiology, physiology, pathology, symptoms, pathognomonic, diagnosis, imaging, treatment, complications, epidemiology, lecture` |
| `references` | `{label, url?}` — web kaynakları gerçekten açılmış URL'lerdir; ders kitabı künyesi bölüm numarasız |
| `aliases` / `altNames` | birleştirilen çift kayıtların kimlikleri / adları (derin bağlantı, favori ve arama bunlarla çözülür) |
| `schemaVersion: 2`, `curation` | üretim/denetim yöntemi ve zamanı |

Varlık türleri: `belirti, bulgu, laboratuvar, goruntuleme, histopatoloji, patojen, gen_protein, ilac, tedavi, test, hastalik,
anatomi, risk_faktoru, hucre, mekanizma`. Ad normalizasyonu: Türkçe, küçük harf, yalın, tekil ("ateş"); niteleyici `qualifier`'da
("yüksek, titremeli"). Eş anlamlılar `scripts/diseases/varlik_esanlamlari.json` ile kanonik ada çevrilir.

## Akış

1. Profiller yeniden yazılır/düzenlenir (yönetici formu ya da toplu iş) → `scripts/diseases/hastalik_profilleri.py birlestir --yaz`
   (eski dosya `meds_temp/hastalik_yedek/<zaman>/` altına yedeklenir).
2. `hastalik_profilleri.py denetle` → 0 HATA (şablon cümle, eksik bölüm, geçersiz varlık türü).
3. `hastalik_profilleri.py disa-aktar` → veri havuzu `$MEDS_DATABASE_DIR/derived/hastaliklar/`:
   `profiller.jsonl` (model), `maddeler.jsonl` (madde başına satır: profil, bölüm, etiket, metin, varlıklar), `varlik_dizini.json`
   (varlık → profiller ve bölümler), `rapor.json`.
4. Arama dizini (`localRagEngine.chunkDiseases`: profil başına 3 parça) ve bilgi grafiği (`diseaseGraphBuild`, `toFlatView` ile)
   sunucu açılışında / sorgu zekâsı derlemesinde yeniden kurulur.

`scripts/akbc_disease_pipeline.py` şema 2 profilleri ezmez ve şablon (deterministik yedek) profil yazmaz.
Eski (şema 1) yerel katkılar `normalizeDisease` ile okunur; şema 1 düzenlemesi yeniden yazılmış kanonik kaydı ezmez.
