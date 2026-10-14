import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..', '..');
const SUMMARIES_CATALOG_FILE = path.resolve(ROOT_DIR, 'src', 'data', 'lectureSummariesCatalog.json');

interface LectureSummary {
  id: string;
  kurul: number | string;
  committeeId?: string;
  discipline: string;
  title: string;
  instructor?: string;
  fileName?: string;
  keyPoints?: string[];
  charCount?: number;
  readingTimeMinutes?: number;
  content?: string;
}

const KURUL_NAMES: Record<string, string> = {
  '1': 'Ürogenital ve Obstetrik Kurulu',
  '2': 'Kardiyovasküler ve Solunum Kurulu',
  '3': 'Hematoloji ve İmmünoloji Kurulu',
  '4': 'Gastrointestinal Sistem Kurulu',
  '5': 'Endokrin ve Metabolizma Kurulu',
  '6': 'Sinir Sistemi ve Psikiyatri Kurulu',
};

function readSummaries(): LectureSummary[] {
  try {
    if (fs.existsSync(SUMMARIES_CATALOG_FILE)) {
      return JSON.parse(fs.readFileSync(SUMMARIES_CATALOG_FILE, 'utf-8'));
    }
  } catch (e) {
    console.error('[Portal] Özetler okunamadı:', e);
  }
  return [];
}

function escapeHtml(str: string): string {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatMarkdownToHtmlText(text: string): string {
  if (!text) return '';
  let html = escapeHtml(text);
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Italic
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  // Line breaks
  html = html.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');
  return `<p>${html}</p>`;
}

// Common CSS for all portal pages
const PORTAL_CSS = `
  :root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-bg: #eff6ff;
    --text-main: #0f172a;
    --text-muted: #475569;
    --border: #e2e8f0;
    --card-bg: #ffffff;
    --bg-page: #f8fafc;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: var(--bg-page);
    color: var(--text-main);
    line-height: 1.65;
    padding: 0;
  }
  .container {
    max-width: 960px;
    margin: 0 auto;
    padding: 32px 20px 60px 20px;
  }
  header.portal-header {
    background: #ffffff;
    border-bottom: 1px solid var(--border);
    padding: 28px 20px;
    margin-bottom: 32px;
  }
  .header-inner {
    max-width: 960px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
  }
  .brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #f1f5f9;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: 8px;
  }
  h1.portal-title {
    font-size: 26px;
    font-weight: 700;
    color: var(--text-main);
    line-height: 1.3;
  }
  p.portal-subtitle {
    font-size: 14px;
    color: var(--text-muted);
    margin-top: 4px;
  }
  .alert-box {
    background: var(--primary-bg);
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 28px;
  }
  .alert-box h4 {
    color: #1e40af;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .alert-box p, .alert-box ol {
    font-size: 13.5px;
    color: #1e3a8a;
    line-height: 1.6;
  }
  .alert-box ol {
    margin-left: 20px;
    margin-top: 6px;
  }
  .kurul-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
  }
  .kurul-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px;
    transition: transform 0.15s, box-shadow 0.15s;
    display: flex;
    flex-col: column;
    justify-content: space-between;
  }
  .kurul-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
    border-color: #cbd5e1;
  }
  .kurul-num {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--primary);
    letter-spacing: 0.5px;
  }
  .kurul-title {
    font-size: 17px;
    font-weight: 700;
    color: var(--text-main);
    margin: 4px 0 10px 0;
  }
  .kurul-meta {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 18px;
  }
  .btn-group {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    border: none;
    transition: background 0.15s;
  }
  .btn-primary {
    background: var(--primary);
    color: #ffffff;
  }
  .btn-primary:hover {
    background: var(--primary-dark);
  }
  .btn-outline {
    background: #f8fafc;
    color: var(--text-main);
    border: 1px solid var(--border);
  }
  .btn-outline:hover {
    background: #e2e8f0;
  }
  .lecture-list-sec {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px;
  }
  .lecture-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 14px;
    font-size: 13.5px;
  }
  .lecture-table th {
    text-align: left;
    padding: 10px 12px;
    background: #f8fafc;
    color: var(--text-muted);
    font-weight: 600;
    border-bottom: 1px solid var(--border);
  }
  .lecture-table td {
    padding: 12px;
    border-bottom: 1px solid #f1f5f9;
  }
  .lecture-table tr:hover td {
    background: #f8fafc;
  }
  .tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11.5px;
    font-weight: 600;
    background: #f1f5f9;
    color: #334155;
  }
  /* Single Lecture and Kurul full view */
  article.lecture-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 28px;
    margin-bottom: 32px;
  }
  h2.lecture-heading {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-main);
    border-bottom: 2px solid #f1f5f9;
    padding-bottom: 10px;
    margin-bottom: 14px;
  }
  .lecture-sub {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 18px;
  }
  .spots-box {
    background: #fffbeb;
    border: 1px solid #fef3c7;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .spots-box h4 {
    color: #b45309;
    font-size: 14px;
    margin-bottom: 8px;
  }
  .spots-box ul {
    margin-left: 18px;
    font-size: 13.5px;
    color: #78350f;
  }
  .lecture-body {
    font-size: 14.5px;
    line-height: 1.7;
    color: #334155;
    margin-top: 18px;
  }
  .lecture-body p {
    margin-bottom: 12px;
  }
  .toc-box {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 30px;
  }
  .toc-box h3 {
    font-size: 15px;
    margin-bottom: 10px;
  }
  .toc-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 8px;
    font-size: 13px;
  }
  .toc-grid a {
    color: var(--primary);
    text-decoration: none;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .toc-grid a:hover {
    text-decoration: underline;
  }
`;

/**
 * 1. Portal Home Page (Directory of all kurullar & lectures)
 */
export function renderPortalIndexHtml(baseUrl: string = ''): string {
  const summaries = readSummaries();
  const kurullar = ['1', '2', '3', '4', '5', '6'];

  const kurulCardsHtml = kurullar.map((k) => {
    const kList = summaries.filter((s) => String(s.kurul) === k);
    const kName = KURUL_NAMES[k] || `Kurul ${k}`;
    const kurulUrl = `${baseUrl}/notebooklm/ozetler/kurul-${k}`;
    const downloadUrl = `${baseUrl}/api/notebooklm/download/ders_ozetleri_kurul${k}.md`;

    return `
      <div class="kurul-card">
        <div>
          <span class="kurul-num">DÖNEM 3 · KURUL ${k}</span>
          <h3 class="kurul-title">${escapeHtml(kName)}</h3>
          <p class="kurul-meta">📚 ${kList.length} Amfi Dersi · NotebookLM Web &amp; MD Uyumlu</p>
        </div>
        <div class="btn-group">
          <a href="${kurulUrl}" class="btn btn-primary" title="NotebookLM için web sitesi görünümünü aç">Siteyi Aç</a>
          <a href="${downloadUrl}" class="btn btn-outline" download title="Markdown dosyasını doğrudan indir">.md İndir</a>
        </div>
      </div>
    `;
  }).join('\n');

  const lectureRowsHtml = summaries.slice(0, 100).map((s) => {
    const lectureUrl = `${baseUrl}/notebooklm/ozet/${encodeURIComponent(s.id)}`;
    return `
      <tr>
        <td><span class="tag">Kurul ${s.kurul}</span></td>
        <td><span class="tag">${escapeHtml(s.discipline)}</span></td>
        <td><strong><a href="${lectureUrl}" style="color:var(--primary);text-decoration:none;">${escapeHtml(s.title)}</a></strong></td>
        <td><small style="color:var(--text-muted);">${escapeHtml(s.instructor || 'Belirtilmemiş')}</small></td>
        <td><a href="${lectureUrl}" class="btn btn-outline" style="padding:4px 8px;font-size:11.5px;">Görüntüle</a></td>
      </tr>
    `;
  }).join('\n');

  return `<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MeDSor · NotebookLM İçin Ders Özetleri Portalı</title>
  <meta name="description" content="Tıp fakültesi amfi ders özetleri, sınav spotları ve fizyopatolojik mekanizma notları NotebookLM için optimize edilmiş açık web portalı.">
  <style>${PORTAL_CSS}</style>
</head>
<body>
  <header class="portal-header">
    <div class="header-inner">
      <div>
        <div class="brand-badge">⚡ MeDSor AI · Tıp Eğitimi</div>
        <h1 class="portal-title">NotebookLM İçin Ders Özetleri Portalı</h1>
        <p class="portal-subtitle">Tüm amfi ders özetleri, sınav spotları ve kilit tıp bilgileri Google NotebookLM ile tam uyumlu.</p>
      </div>
      <div>
        <a href="${baseUrl}/api/notebooklm/download/tum_ders_ozetleri_master.md" class="btn btn-primary" download>📥 Tüm Arşivi İndir (359 Ders)</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="alert-box">
      <h4>💡 Google NotebookLM ile Nasıl Kullanılır?</h4>
      <ol>
        <li><strong>Web Sitesi Ekle (Önerilen):</strong> Aşağıdaki kurullardan ilgilendiğiniz kurulun <em>"Siteyi Aç"</em> bağlantısına tıklayın ve tarayıcınızdaki adresi kopyalayıp NotebookLM'de <em>"Kaynak Ekle &rarr; Web Sitesi"</em> kısmına yapıştırın.</li>
        <li><strong>Dosya Yükle:</strong> İlgili kurulun yanındaki <em>".md İndir"</em> butonuna basarak dosyayı kaydedin ve NotebookLM'e sürükleyip bırakın (500.000 kelimeye kadar sıfır kayıpla aktarılır).</li>
      </ol>
    </div>

    <h2 style="font-size: 20px; font-weight: 700; margin-bottom: 16px;">Kurul Bazlı Özet Siteleri</h2>
    <div class="kurul-grid">
      ${kurulCardsHtml}
    </div>

    <section class="lecture-list-sec">
      <h3 style="font-size: 18px; font-weight: 700;">Tüm Amfi Dersleri Dizini (359 Ders)</h3>
      <p style="font-size: 13px; color: var(--text-muted); margin-top: 2px;">Dilediğiniz dersin üzerine tıklayarak tekil ders özet sayfasını NotebookLM kaynağı olarak alabilirsiniz.</p>
      
      <table class="lecture-table">
        <thead>
          <tr>
            <th>Kurul</th>
            <th>Branş</th>
            <th>Ders Başlığı</th>
            <th>Öğretim Üyesi</th>
            <th>İşlem</th>
          </tr>
        </thead>
        <tbody>
          ${lectureRowsHtml}
        </tbody>
      </table>
    </section>
  </main>
</body>
</html>`;
}

/**
 * 2. Full Kurul Page (All lectures of a Kurul in one semantic HTML page for NotebookLM)
 */
export function renderKurulPortalHtml(kurulNum: string, baseUrl: string = ''): string {
  const summaries = readSummaries();
  const kList = summaries.filter((s) => String(s.kurul) === String(kurulNum));
  const kName = KURUL_NAMES[kurulNum] || `Kurul ${kurulNum}`;
  const downloadUrl = `${baseUrl}/api/notebooklm/download/ders_ozetleri_kurul${kurulNum}.md`;

  const tocHtml = kList.map((s, idx) => `
    <a href="#ders-${encodeURIComponent(s.id)}">${idx + 1}. ${escapeHtml(s.title)}</a>
  `).join('\n');

  const lecturesHtml = kList.map((s, idx) => {
    const keyPointsHtml = s.keyPoints && s.keyPoints.length > 0 ? `
      <div class="spots-box">
        <h4>⚡ Sınav Spotları &amp; Kilit Noktalar:</h4>
        <ul>
          ${s.keyPoints.map((kp) => `<li>${escapeHtml(kp.replace(/^[-\s*]+/, ''))}</li>`).join('\n')}
        </ul>
      </div>
    ` : '';

    const contentHtml = s.content ? `
      <div class="lecture-body">
        ${formatMarkdownToHtmlText(s.content)}
      </div>
    ` : '<p><em>Bu ders için detaylı özet metni bulunmuyor.</em></p>';

    return `
      <article class="lecture-card" id="ders-${encodeURIComponent(s.id)}">
        <span class="tag" style="margin-bottom:8px;">Ders #${idx + 1} · TIP 3${kurulNum}0</span>
        <h2 class="lecture-heading">${escapeHtml(s.title)}</h2>
        <div class="lecture-sub">
          <strong>Branş:</strong> ${escapeHtml(s.discipline)} | 
          <strong>Öğretim Üyesi:</strong> ${escapeHtml(s.instructor || 'Belirtilmemiş')}
        </div>
        ${keyPointsHtml}
        ${contentHtml}
      </article>
    `;
  }).join('\n');

  return `<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kurul ${kurulNum}: ${escapeHtml(kName)} · MeDSor NotebookLM Kaynağı</title>
  <style>${PORTAL_CSS}</style>
</head>
<body>
  <header class="portal-header">
    <div class="header-inner">
      <div>
        <a href="${baseUrl}/notebooklm/ozetler" style="font-size:13px;color:var(--primary);text-decoration:none;font-weight:600;">&larr; Tüm Kurullara Dön</a>
        <h1 class="portal-title" style="margin-top:6px;">Dönem 3 · Kurul ${kurulNum}: ${escapeHtml(kName)}</h1>
        <p class="portal-subtitle">${kList.length} Amfi Dersi · NotebookLM Web Crawl Uyumlu Temiz Kaynak</p>
      </div>
      <div class="btn-group">
        <a href="${downloadUrl}" class="btn btn-primary" download>📥 Kurul ${kurulNum} .md İndir</a>
        <a href="${baseUrl}/notebooklm/ozetler" class="btn btn-outline">Ana Portal</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="alert-box">
      <h4>📌 NotebookLM İpucu</h4>
      <p>Bu sayfanın URL'sini kopyalayıp NotebookLM'de <strong>"Kaynak Ekle &rarr; Web Sitesi"</strong> kısmına yapıştırabilirsiniz. Sayfa botların doğrudan metin taraması için optimize edilmiştir.</p>
    </div>

    <nav class="toc-box">
      <h3>İçindekiler (${kList.length} Ders)</h3>
      <div class="toc-grid">
        ${tocHtml}
      </div>
    </nav>

    <section>
      ${lecturesHtml}
    </section>
  </main>
</body>
</html>`;
}

/**
 * 3. Single Lecture Page (Pure semantic HTML for a single lecture)
 */
export function renderSingleLectureHtml(lectureId: string, baseUrl: string = ''): string {
  const summaries = readSummaries();
  const s = summaries.find((item) => String(item.id) === String(lectureId)) ||
            summaries.find((item) => String(item.title).toLowerCase().includes(String(lectureId).toLowerCase()));

  if (!s) {
    return `<!DOCTYPE html>
<html lang="tr">
<head><meta charset="utf-8"><title>Ders Bulunamadı</title><style>${PORTAL_CSS}</style></head>
<body style="padding: 50px; text-align: center;">
  <h2>Ders Özeti Bulunamadı</h2>
  <p>Aradığınız ders kimliği: <code>${escapeHtml(lectureId)}</code></p>
  <a href="${baseUrl}/notebooklm/ozetler" class="btn btn-primary" style="margin-top:20px;">Portala Dön</a>
</body>
</html>`;
  }

  const kName = KURUL_NAMES[String(s.kurul)] || `Kurul ${s.kurul}`;

  const keyPointsHtml = s.keyPoints && s.keyPoints.length > 0 ? `
    <div class="spots-box">
      <h4>⚡ Sınav Spotları &amp; Kilit Noktalar:</h4>
      <ul>
        ${s.keyPoints.map((kp) => `<li>${escapeHtml(kp.replace(/^[-\s*]+/, ''))}</li>`).join('\n')}
      </ul>
    </div>
  ` : '';

  const contentHtml = s.content ? `
    <div class="lecture-body">
      ${formatMarkdownToHtmlText(s.content)}
    </div>
  ` : '<p><em>Bu ders için detaylı özet metni bulunmuyor.</em></p>';

  return `<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(s.title)} · MeDSor NotebookLM Özeti</title>
  <style>${PORTAL_CSS}</style>
</head>
<body>
  <header class="portal-header">
    <div class="header-inner">
      <div>
        <a href="${baseUrl}/notebooklm/ozetler/kurul-${s.kurul}" style="font-size:13px;color:var(--primary);text-decoration:none;font-weight:600;">&larr; Kurul ${s.kurul} (${escapeHtml(kName)}) Sayfasına Dön</a>
        <h1 class="portal-title" style="margin-top:6px;">${escapeHtml(s.title)}</h1>
        <p class="portal-subtitle">Branş: ${escapeHtml(s.discipline)} | Eğitmen: ${escapeHtml(s.instructor || 'Belirtilmemiş')}</p>
      </div>
      <div>
        <a href="${baseUrl}/notebooklm/ozetler" class="btn btn-outline">Tüm Özetler</a>
      </div>
    </div>
  </header>

  <main class="container">
    <article class="lecture-card">
      <span class="tag" style="margin-bottom:8px;">Kurul ${s.kurul} · ${escapeHtml(s.discipline)}</span>
      <h2 class="lecture-heading">${escapeHtml(s.title)}</h2>
      <div class="lecture-sub">
        <strong>Öğretim Üyesi:</strong> ${escapeHtml(s.instructor || 'Belirtilmemiş')} | 
        <strong>Okuma Süresi:</strong> ~${s.readingTimeMinutes || 5} dk
      </div>
      ${keyPointsHtml}
      ${contentHtml}
    </article>
  </main>
</body>
</html>`;
}
