// Tarayıcıda çalışır: her kartta panel/etiket için hata listesi döner (panel_sinama.mjs)
(() => {
  const out = [];
  // öğenin kendi yazısının satır sayısı (hücre yüksekliği komşu hücreyle büyüyebilir; yalnız yazının satırları sayılır)
  const satir = (el) => { const r = document.createRange(); r.selectNodeContents(el); const ust = new Set([...r.getClientRects()].filter((q) => q.width > 1).map((q) => Math.round(q.top))); return ust.size; };
  const kes = (a, b, p = 1) => !(a.right <= b.left + p || b.right <= a.left + p || a.bottom <= b.top + p || b.bottom <= a.top + p);
  for (const k of document.querySelectorAll('.kart')) {
    const pg = k.querySelector('.pdv-page'); const p = pg.getBoundingClientRect();
    const ek = k.querySelector('.pdv-page-ek'); const alt = ek ? ek.getBoundingClientRect().bottom : p.bottom;
    for (const o of k.querySelectorAll('.pdv-cz-sema, .pdv-cz-etiket-kap')) {
      const r = o.getBoundingClientRect(); if (!r.width) continue;
      const panel = o.classList.contains('pdv-cz-sema');
      const ad = (panel ? 'panel' : 'etiket') + ' s.' + k.dataset.s + ' ' + (o.className.replace(/pdv-cz-sema |pdv-sb /g, '').split(' ')[0] || '') + ' «' + o.textContent.slice(0, 40) + '»';
      const s = [];
      if (r.bottom > alt + 1) s.push('alttan taşma ' + Math.round(r.bottom - alt) + 'px');
      if (r.right > p.right + 1 || r.left < p.left - 1) s.push('sayfadan yana taşma');
      const ic = [...o.querySelectorAll('td, th, li, .pdv-sb-kutu, .pdv-cz-dugum, .pdv-sb-bag, .pdv-cz-etiket')].reduce((m, e) => Math.max(m, e.getBoundingClientRect().right), 0);
      if (ic > r.right + 1) s.push('iç taşma ' + Math.round(ic - r.right) + 'px');
      const kh = +k.dataset.kh; if (panel && kh && r.height / p.height > kh * 1.0 + 0.004) s.push('ayrılan yükseklik aşıldı ×' + (r.height / p.height / kh).toFixed(2));
      const fe = panel ? o : o.querySelector('.pdv-cz-etiket'); const fs = parseFloat(getComputedStyle(fe).fontSize);
      if (fs < 7) s.push('yazı çok küçük ' + fs.toFixed(1) + 'px');
      // yatay zincir: kutu tek satır olmalı
      for (const z of o.querySelectorAll('.pdv-sb-zincir:not(.is-dikey) .pdv-sb-kutu, .pdv-cz-zincir .pdv-cz-dugum')) if (satir(z) > 1) s.push('yatay zincirde kutu satıra kırılmış «' + z.textContent.slice(0, 20) + '»');
      // kelime ortasından kırılma: tek kelimelik öğe birden çok satır
      for (const d of o.querySelectorAll('.pdv-sb-kutu, td, li, .pdv-cz-dugum, .pdv-sb-kosul, .pdv-sb-bag')) { const w = d.textContent.trim().split(/\s+/).length; if (w === 1 && satir(d) > 1) s.push('kelime ortasından kırılmış «' + d.textContent.slice(0, 20) + '»'); }
      for (const e of o.querySelectorAll('.pdv-sb-bag, .pdv-cz-etiket, .pdv-cz-bag-etiket')) if (e.scrollWidth > e.clientWidth + 1) s.push('kesik yazı «' + e.textContent.slice(0, 20) + '»');
      // panel içi öğe çakışması (kutu kutunun üstünde)
      const kutu = [...o.querySelectorAll('.pdv-sb-kutu, .pdv-cz-dugum, .pdv-sb-bag')].map((e) => e.getBoundingClientRect()).filter((b) => b.width);
      for (let i = 0; i < kutu.length; i++) for (let j = i + 1; j < kutu.length; j++) if (kes(kutu[i], kutu[j], 2)) { s.push('panel içi öğeler üst üste'); i = kutu.length; break; }
      if (s.length) out.push(ad + ': ' + s.join('; '));
    }
  }
  return out;
})()
