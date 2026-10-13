# Arşiv: "4 aşamalı saf NLP" kitle kaynak motoru (2026-10-13, commit 7682859)

Hiçbir yerden çağrılmıyordu; 2026-10-13 denetiminde ölçümlerinin yanıltıcı olduğu görüldü ve arşive alındı.
Yerine geçen motor: `src/services/recall/` (belge: `docs/SORU_HAVUZU_MOTORU.md`).

Denetim bulguları:
- **Küme sayısı cevap anahtarından:** `reconstruct_questions` KMeans'e `k = len(gerçek soru sayısı)` veriyor. Gerçek
  kullanımda kaç farklı soru olduğu bilinmez; %96–98 ARI bu sızıntıyla elde edilmiş.
- **"Yeniden inşa" sabit şablon:** spaCy/Stanza/NLTK "adayları" kümenin en sık 3 sözcüğünün üç sabit cümle kalıbına
  yerleştirilmesi ("Aşağıdakilerden hangisi {x y z} ile ilişkili durumlardan … biri değildir?"). Stanza hiç
  kullanılmıyor; her soru olumsuz köklü kalıba dönüşüyor. `tr_core_news_md` yoksa `spacy.blank("tr")`.
- **Hakem İngilizce özetleyici:** `sshleifer/distilbart-cnn-6-6` İngilizce haber özetleme modeli; Türkçe adaylar
  arasındaki kayıp farkı anlamlı değil.
- **Gerçek sınav sonuçları elle yazılmış:** `reconstruct_pdf_exam.py`'deki "spacy/stanza/nltk" adayları özgün soruların
  elle yazılmış açıklamaları (koda gömülü); %95,9 benzerlik bu metinlerin özgün soruya benzerliğidir. Sonuç dosyası
  başka bir ajanın geçici klasörüne yazılıyordu.
- `results/*.json` dosyalarındaki "distilbart_sorusu" metinleri `master_nlp_crowdsource.py` çıktısı olamaz (kalıp dışı).

Veri setleri (`synthetic_10q_500v`, `challenging_14q_650v`) değerli: `scripts/eval/datasets/kitle_kaynak/` altına
taşındı. Yeni motor bu iki sette küme sayısı verilmeden: kesinlik %99,8 / %98,0, duyarlılık %57 / %40
(eski canlı motor kume-v2: kesinlik %99,8 / %82, duyarlılık %16 / %9).
