import fs from 'fs';

const raw = fs.readFileSync('src/services/driveAutomation.ts', 'utf8');

// Rich multi-page medical details template generator
function generateFullPages(title, discipline) {
  const pages = [];
  
  // Page 1: Giriş & Terminoloji
  pages.push({
    pageNumber: 1,
    content: `[Slayt 1-6 / Giriş & Terminoloji] ${title}: Konunun tıp eğitimindeki ve klinik uygulamadaki yeri. Temel patofizyolojik tanımlar, etyolojik faktörler (genetik, çevresel, enfeksiyöz, immünolojik nedenler) ve risk grupları.`,
    keywords: [title.toLowerCase(), 'etyoloji', 'tanımlar', 'risk faktörleri', 'patogenez']
  });

  // Page 2: Patofizyoloji & Hücresel Mekanizmalar
  pages.push({
    pageNumber: 2,
    content: `[Slayt 7-14 / Hücresel ve Moleküler Mekanizmalar] Hücre düzeyindeki sinyal iletim yolakları, sitokin ve kemokin salınımları, membran geçirgenlik değişiklikleri, serbest radikal hasarı veya immün kompleks aracılı doku hasarı mekanizmaları.`,
    keywords: ['moleküler mekanizma', 'sitokinler', 'hücre hasarı', 'sinyal iletimi', 'reseptör']
  });

  // Page 3: Morfoloji & Histopatoloji
  pages.push({
    pageNumber: 3,
    content: `[Slayt 15-22 / Makroskopi ve Mikroskopik Bulgular] Doku düzeyindeki karakteristik lezyonlar: Işık mikroskopisi ve immünhistokimya bulguları, hücre infiltrasyonu, nükleer atipi, apoptoz/nekroz alanları ve spesifik boyanma paternleri (H&E, PAS, Masson Trikrom vb.).`,
    keywords: ['histopatoloji', 'makroskopi', 'mikroskopi', 'immünhistokimya', 'biyopsi', 'boyanma']
  });

  // Page 4: Klinik Tablo & Tanı
  pages.push({
    pageNumber: 4,
    content: `[Slayt 23-30 / Klinik Bulgular ve Tanı Kriterleri] Hastada ortaya çıkan semptomlar ve fizik muayene bulguları. Laboratuvar testleri (tam kan, biyokimya, seroloji), radyolojik görüntüleme (USG, BT, MR) ve altın standart tanı kriterleri.`,
    keywords: ['klinik bulgular', 'semptomlar', 'fizik muayene', 'laboratuvar', 'radyoloji', 'tanı']
  });

  // Page 5: Sınav Vurguları & Çıkmış Soru İpuçları
  pages.push({
    pageNumber: 5,
    content: `[Slayt 31-Son / Kurul Sınavı Vurguları & Çıkmış Sorular] Kurul sınavlarında hocaların en çok üzerinde durduğu kilit ayrımlar: En sık görülen tip, patognomonik bulgu, ilk tercih edilecek ilaç/yöntem ve vaka sorularındaki çeldirici tuzaklar.`,
    keywords: ['kurul sınavı', 'çıkmış soru', 'patognomonik', 'en sık', 'altın standart', 'ayırıcı tanı']
  });

  return pages;
}

console.log('Script ready to enrich slide pages');
