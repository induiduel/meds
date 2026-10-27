import React from 'react';
import { ChevronRight, Search } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { NAV_ITEMS, openSearch } from '../shell/navModel';
import { MERKEZ_ARACLARI } from '../merkez/merkezModel';
import { useV15Baslik } from './baslik';
import '../../styles/v15/dersler.css';

/**
 * v15 · Başvuru merkezi (tasarım sistemi v15 › G01). Kurulsuz: üstte genel arama girişi (terim, hastalık, ilaç; arama
 * paletini açar), altında "ne zaman kullanılır" cümleli kaynak kartları (merkezModel.MERKEZ_ARACLARI.kaynaklar).
 */
const TON: Partial<Record<AppRoute, string>> = { oncelikli_dersler: '', glossary: 'is-c', diseases: 'is-b', health_ministry: 'is-ok', kazanimlar: 'is-ai', gecmis_kurullar: 'is-w', guncellemeler: '' };
const git = (url: string) => linkClick(() => navigateTo(url));

export default function KaynaklarMerkezV15() {
  useV15Baslik({ baslik: 'Başvuru', alt: 'Sözlük, hastalıklar, resmî veriler ve geçmiş kurullar' });
  const araclar = MERKEZ_ARACLARI.kaynaklar.filter((a) => NAV_ITEMS[a.id]);
  return (
    <div className="d15 k15">
      <h1 className="sr-only">Başvuru</h1>
      <button type="button" className="g15-ara" onClick={openSearch}>
        <Search aria-hidden />
        <span>Terim, hastalık, ilaç ya da kazanım ara</span>
        <kbd>⌘K</kbd>
      </button>
      <div className="k15-alan">
        <ul className="k15-izgara" role="list">
          {araclar.map((a) => {
            const it = NAV_ITEMS[a.id];
            const url = pathFor(a.id);
            return (
              <li key={a.id}>
                <a className="k15-kart v15-card" href={url} onClick={git(url)}>
                  <span className={`v15-tile ${TON[a.id] ?? ''}`}><it.icon aria-hidden /></span>
                  <span className="k15-kart-t">
                    <b>{it.label}{a.oner && <span className="v15-tag is-a">Önerilen</span>}</b>
                    <span>{a.ne}</span>
                  </span>
                  <ChevronRight className="v15-chev" aria-hidden />
                </a>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
