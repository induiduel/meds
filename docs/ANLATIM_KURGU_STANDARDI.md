# Sesli ders anlatım kurgusu — hikâye gibi, neden-sonuçlu (kullanıcı kararı 2026-10-28)

Tam içerik işçisinin yazdığı her yeni sesli ders metni (konuşma metni / `konusma_v2.json`) bu belgeye uyar.
Dolgu yasağı (H22), Türkçe üslup ve kaynak sadakati aynen geçerlidir; buradaki kurallar **yeni bilgi eklemez**, var olan
bilgiyi öğrencinin neye çalıştığını anlayacağı sırayla bağlar.

## 1. Neden (belirti)

Slayt bazen başlık vermeden yeni konuya geçiyor; anlatım bunu söylemeyince öğrenci yeni konuyu öncekinin devamı sanıyor,
kafası karışıyor. Dersin genel amacı, listeleri, sıralamaları ve giriş–gelişme–sonuç düzeni anlatımda görünmüyordu.

## 2. Önce plan, sonra metin (tek geçişte doğru)

Yazar metne başlamadan önce kısa bir **anlatım planı** çıkarır (taslak klasöründe `anlatim_plani.md`, yayına girmez):

1. **Dersin amacı** (1 cümle): bu ders öğrenciye neyi kazandırıyor, sınavda nereye bağlanıyor.
2. **Hiyerarşi:** giriş (tanım, neden önemli) → gelişme (bölümler, her bölümün alt başlıkları) → sonuç (ana fikirlerin bağı).
   PDF'in kendi başlık ağacı ve numaralı/harfli listeleri buraya aynen taşınır.
3. **Bölüm geçişleri:** her bölüm sınırında bir önceki bölümle ilişki türü: *devam* (aynı konunun alt başlığı),
   *neden → sonuç*, *karşılaştırma*, *genelden özele*, *yeni konu* (ilişkisiz). Başlıksız slayt geçişleri de işaretlenir.
4. **Örnek yerleri:** soyut kavramın anlaşılmasını kolaylaştıracak 3–8 yer; örnek kaynaktaki vaka/hoca örneğinden,
   yoksa kaynaktaki bilgiden kurulan kısa klinik tablo (kaynak dışı bilgi YOK).
5. **Kapsam bütçesi:** bölüm başına yaklaşık cümle sayısı (sayfa_haritasi bilgi maddelerinden).

Plan doğru kurulursa metin bir kez yazılır; kapı ya da denetçi yalnız hatalı bölümü geri gönderir (TAM_HAT_HIZLI_AKIS §3).

## 3. Metinde zorunlu kurgu ögeleri

- **Ders girişi (ilk 2–3 cümle):** dersin konusu ve neyi neden öğreneceğimiz; selam/tanıtım yok, doğrudan tıbbi çerçeve.
  Ör.: "İnme, beyne giden kanın aniden kesilmesiyle ortaya çıkar; önce damar yapısını, sonra inme türlerini, en sonda
  acil yaklaşımı göreceğiz, çünkü tedavi kararı türe göre değişir."
- **Bölüm girişi:** her `@@` bölümün ilk cümlesi bu bölümün neden geldiğini ve öncekiyle ilişkisini söyler.
  - devam: "İskemik inmenin nedenlerini gördük; şimdi bu nedenlerin beyinde nasıl hasar yaptığına geçiyoruz."
  - yeni konu: "Burada konu değişiyor: inmeden ayrı olarak sinüs ven trombozunu anlatacağız; ortak noktaları yalnız ani
    nörolojik bulgu vermeleri." — **Başlıksız slayt geçişinde bu cümle zorunludur.**
- **Liste ve sıralama:** PDF'te numaralı/harfli liste ya da evre sırası varsa önce kaç madde olduğu söylenir, sonra sırayla
  anlatılır ("dört evre var: birincisi…, ikincisi…"). Sıra değiştirilmez; sıralamanın mantığı (şiddet, zaman, sıklık)
  biliniyorsa bir kez söylenir.
- **Neden-sonuç:** her mekanizma "çünkü / bu yüzden / bunun sonucu" bağıyla bir öncekine bağlanır; kopuk bilgi dizilmez.
- **Örnek:** planlanan yerlerde 1–2 cümlelik örnek ("Örneğin, sabah uyandığında sağ kolunu kaldıramayan altmış yaşında bir
  hasta düşünün…"). Örnek bilgi tekrarına dönüşmez, yeni bir bilgi ya da ayrım öğretir; derste en çok ~8 örnek.
- **Bölüm sonu bağı (isteğe bağlı, en çok 1 cümle):** bir sonraki bölüme köprü; "şimdi gelelim" gibi boş geçiş değil,
  ilişkiyi söyleyen cümle.
- **Ders sonu:** 3–5 cümlelik toparlama: dersin amacına dönülür, bölümlerin birbirine bağı söylenir (yeni bilgi yok).

Bu cümleler dolgu sayılmaz, çünkü içerik taşırlar (ilişki türü, sıra, amaç). "Şimdi gelelim", "bir kez daha hatırlatalım"
gibi içeriksiz geçişler yine yasaktır (`metin_denetle.py` H22).

## 4. Sayısal hedeflerde tolerans

Kelime, cümle, süre, örnek sayısı gibi sayısal hedeflerde **±%20'ye kadar** sapma kabul edilir; yeniden yazım
gerekçesi değildir. Hedef aşıldı diye bütün metin baştan yazılmaz; yalnız ±%20 dışına çıkan bölüm kısaltılır/genişletilir.
Tıbbi yanlış, kaynak dışı bilgi, üslup ve okunuş hatasında tolerans yoktur.

## 5. Denetçi soruları (bağımsız denetçi, öğrenci rolünde)

1. Dersin amacını ilk dakikada anladım mı?
2. Her konu değişiminde yeni konuya geçildiğini ve öncekiyle ilişkisini duydum mu? (başlıksız slaytlar dahil)
3. Listeler kaç maddeli ve hangi sırayla anlatıldı, takip edebildim mi?
4. En az birkaç yerde kavramı somutlaştıran örnek var mı, örnekler kaynağa dayanıyor mu?
5. Ders sonunda bölümlerin birbirine nasıl bağlandığını söyleyebiliyor muyum?

Birine "hayır" diyen denetçi yalnız ilgili bölümün kimliğini ve eksik ögeyi yazar.

## 6. Seslendirme (EMA) okunuşu

Yabancı terim (eponim, Latince tür adı, İngilizce klinik terim, ilaç ticari adı) metinde standart yazımla kalabilir;
EMA'ya giderken `scripts/sesli_anlatim/terim_okunus.py` Türkçedeki yaygın okunuşa çevirir (Wernicke → Vernike,
Staphylococcus → stafilokokus, locked-in → lokt in). Yazar seslendirmeden önce
`python3 scripts/sesli_anlatim/terim_okunus.py --denetle <anahtar>` çalıştırır; `KURAL` satırlarında yanlış okunuş varsa
`data/sesli_anlatim/okunus/terim_okunus.json`'a ekler (sözlük büyüdükçe sonraki derslerde hata kalmaz).
