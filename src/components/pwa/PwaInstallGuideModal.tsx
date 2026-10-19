import React, { useEffect, useId, useState } from 'react';
import { Check, Copy, Download, Maximize2, PlusSquare, Smartphone, Sparkles, X } from 'lucide-react';
import {
  PWA_GUIDE_OPEN_EVENT,
  pwaService,
  type PwaState,
} from '../../services/pwaService';
import { enterFullscreen } from '../../utils/fullscreen';
import { EntryDialogV12 } from '../v12/OnboardingV12';

type GuideTab = 'ios-safari' | 'ios-chrome' | 'other';

function defaultTabFor(state: PwaState): GuideTab {
  if (state.isIos) {
    return state.iosBrowser === 'crios' ? 'ios-chrome' : 'ios-safari';
  }
  return 'other';
}

/** iOS Paylaş (yukarı oklu kare) simgesi — Apple sistem simgesiyle birebir */
const IosShareGlyph: React.FC = () => (
  <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <path d="M12 3v12" />
    <path d="m8 7 4-4 4 4" />
    <path d="M5 11v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8" />
  </svg>
);

export const PwaInstallGuideModal: React.FC = () => {
  const id = useId();
  const [open, setOpen] = useState(false);
  const [pwaState, setPwaState] = useState<PwaState>(() => pwaService.getState());
  const [tab, setTab] = useState<GuideTab>(() => defaultTabFor(pwaService.getState()));
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const unsub = pwaService.subscribe((s) => {
      setPwaState(s);
      if (s.isInstalled) setOpen(false);
    });
    const onOpen = () => {
      const cur = pwaService.getState();
      setPwaState(cur);
      setTab(defaultTabFor(cur));
      setOpen(true);
    };
    window.addEventListener(PWA_GUIDE_OPEN_EVENT, onOpen);
    return () => {
      unsub();
      window.removeEventListener(PWA_GUIDE_OPEN_EVENT, onOpen);
    };
  }, []);

  if (!open) return null;

  const copyUrl = async () => {
    try {
      await navigator.clipboard.writeText(window.location.origin);
      setCopied(true);
      setTimeout(() => setCopied(false), 2200);
    } catch {
      /* ignore */
    }
  };

  const handleNativeInstall = async () => {
    const res = await pwaService.promptInstall({ silentIfUnsupported: true });
    if (res === 'accepted') setOpen(false);
  };

  const handleEnterFullscreen = () => {
    void enterFullscreen();
    setOpen(false);
  };

  return (
    <EntryDialogV12
      labelledBy={`${id}-t`}
      describedBy={`${id}-d`}
      onClose={() => setOpen(false)}
      width={480}
    >
      <div className="e12-dlg-h">
        <span className="e12-lead is-acc" aria-hidden="true">
          <Smartphone />
        </span>
        <div>
          <h2 id={`${id}-t`}>Uygulamayı Cihaza Yükle (Tam Ekran PWA)</h2>
          <p id={`${id}-d`}>
            Tarayıcı adres çubuğu olmadan gerçek tam ekran ve çevrimdışı çalışma
          </p>
        </div>
        <button
          type="button"
          className="e12-btn is-ghost is-icon is-sm"
          onClick={() => setOpen(false)}
          aria-label="Kapat"
        >
          <X aria-hidden="true" />
        </button>
      </div>

      <div className="e12-dlg-b">
        {pwaState.hasNativePrompt && (
          <div
            style={{
              padding: '12px 14px',
              borderRadius: 10,
              background: 'var(--color-accent-soft)',
              border: '1px solid color-mix(in srgb, var(--color-accent) 28%, transparent)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: 12,
              flexWrap: 'wrap',
            }}
          >
            <div style={{ flex: '1 1 180px', minWidth: 0 }}>
              <strong style={{ display: 'block', fontSize: 13.5 }}>
                Tek Dokunuşla Kurulum Hazır
              </strong>
              <span style={{ fontSize: 12.5, color: 'var(--color-ink-2)' }}>
                Tarayıcın doğrudan uygulama kurulumunu destekliyor.
              </span>
            </div>
            <button
              type="button"
              className="e12-btn is-pri is-sm"
              onClick={handleNativeInstall}
            >
              <Download aria-hidden="true" />
              Şimdi Yükle
            </button>
          </div>
        )}

        {/* Tarayıcı seçici sekmeler */}
        <div
          role="tablist"
          aria-label="Tarayıcı seçimi"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, minmax(0, 1fr))',
            gap: 4,
            padding: 3,
            borderRadius: 9,
            background: 'var(--color-field)',
          }}
        >
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'ios-safari'}
            onClick={() => setTab('ios-safari')}
            style={{
              height: 32,
              border: 0,
              borderRadius: 7,
              fontSize: 12.5,
              fontWeight: tab === 'ios-safari' ? 600 : 500,
              background: tab === 'ios-safari' ? 'var(--color-white)' : 'transparent',
              color: tab === 'ios-safari' ? 'var(--color-ink)' : 'var(--color-ink-2)',
              boxShadow: tab === 'ios-safari' ? 'var(--shadow-xs)' : 'none',
              cursor: 'pointer',
            }}
          >
            iOS Safari
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'ios-chrome'}
            onClick={() => setTab('ios-chrome')}
            style={{
              height: 32,
              border: 0,
              borderRadius: 7,
              fontSize: 12.5,
              fontWeight: tab === 'ios-chrome' ? 600 : 500,
              background: tab === 'ios-chrome' ? 'var(--color-white)' : 'transparent',
              color: tab === 'ios-chrome' ? 'var(--color-ink)' : 'var(--color-ink-2)',
              boxShadow: tab === 'ios-chrome' ? 'var(--shadow-xs)' : 'none',
              cursor: 'pointer',
            }}
          >
            iOS Chrome
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'other'}
            onClick={() => setTab('other')}
            style={{
              height: 32,
              border: 0,
              borderRadius: 7,
              fontSize: 12.5,
              fontWeight: tab === 'other' ? 600 : 500,
              background: tab === 'other' ? 'var(--color-white)' : 'transparent',
              color: tab === 'other' ? 'var(--color-ink)' : 'var(--color-ink-2)',
              boxShadow: tab === 'other' ? 'var(--shadow-xs)' : 'none',
              cursor: 'pointer',
            }}
          >
            Android / PC
          </button>
        </div>

        {tab === 'ios-safari' && (
          <ul className="e12-perks">
            <li>
              <span className="e12-lead is-acc" aria-hidden="true">
                <IosShareGlyph />
              </span>
              <span>
                <b>1. “Paylaş” düğmesine dokun</b>
                <span>
                  Safari’de ekranın <strong>alt orta kısmındaki</strong> (iPad’de sağ üstteki){' '}
                  <strong>Paylaş</strong> (yukarı oklu kare) simgesine dokun.
                </span>
              </span>
            </li>
            <li>
              <span className="e12-lead is-ok" aria-hidden="true">
                <PlusSquare />
              </span>
              <span>
                <b>2. “Ana Ekrana Ekle” seçeneğine dokun</b>
                <span>
                  Açılan paylaşım menüsünü biraz aşağı kaydır ve{' '}
                  <strong>“Ana Ekrana Ekle”</strong> (Add to Home Screen) satırını seç.
                </span>
              </span>
            </li>
            <li>
              <span className="e12-lead" aria-hidden="true">
                <Sparkles />
              </span>
              <span>
                <b>3. Sağ üstten “Ekle”ye dokun ve Ana Ekrandan aç</b>
                <span>
                  Ana ekranına yerleşen <strong>MeDSor</strong> simgesinden açtığında Safari adres
                  çubuğu tamamen kalkar ve <strong>%100 gerçek tam ekran</strong> çalışır.
                </span>
              </span>
            </li>
          </ul>
        )}

        {tab === 'ios-chrome' && (
          <>
            <ul className="e12-perks">
              <li>
                <span className="e12-lead is-acc" aria-hidden="true">
                  <IosShareGlyph />
                </span>
                <span>
                  <b>1. Adres çubuğundaki “Paylaş” simgesine dokun</b>
                  <span>
                    iPhone/iPad Chrome’da <strong>sağ üstte adres çubuğunun sağındaki</strong>{' '}
                    <strong>Paylaş</strong> (yukarı oklu kare) düğmesine dokun.
                  </span>
                </span>
              </li>
              <li>
                <span className="e12-lead is-ok" aria-hidden="true">
                  <PlusSquare />
                </span>
                <span>
                  <b>2. “Ana Ekrana Ekle” satırına dokun</b>
                  <span>
                    Açılan menüde aşağı kaydırıp <strong>“Ana Ekrana Ekle”</strong> seçeneğine,
                    ardından sağ üstteki <strong>“Ekle”</strong> düğmesine dokun.
                  </span>
                </span>
              </li>
              <li>
                <span className="e12-lead" aria-hidden="true">
                  <Sparkles />
                </span>
                <span>
                  <b>3. Ana ekranındaki MeDSor simgesinden başlat</b>
                  <span>
                    Uygulamayı ana ekrandan açtığında Chrome sekme ve adres çubukları tamamen
                    gizlenir, <strong>gerçek tam ekran</strong> modunda açılır.
                  </span>
                </span>
              </li>
            </ul>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: 10,
                padding: '8px 12px',
                borderRadius: 9,
                background: 'var(--color-field)',
                fontSize: 12,
                color: 'var(--color-ink-2)',
              }}
            >
              <span>Menüde görünmüyorsa adresi kopyalayıp Safari’den de ekleyebilirsin:</span>
              <button
                type="button"
                className="e12-btn is-sm"
                style={{ flexShrink: 0 }}
                onClick={copyUrl}
              >
                {copied ? <Check aria-hidden="true" /> : <Copy aria-hidden="true" />}
                {copied ? 'Kopyalandı' : 'Kopyala'}
              </button>
            </div>
          </>
        )}

        {tab === 'other' && (
          <ul className="e12-perks">
            <li>
              <span className="e12-lead is-acc" aria-hidden="true">
                <Download />
              </span>
              <span>
                <b>1. Tarayıcı menüsünü veya adres çubuğunu aç</b>
                <span>
                  Android Chrome’da sağ üstteki <strong>⋮</strong> menüsüne, bilgisayarda ise adres
                  çubuğunun sağındaki <strong>Yükle</strong> simgesine tıkla.
                </span>
              </span>
            </li>
            <li>
              <span className="e12-lead is-ok" aria-hidden="true">
                <PlusSquare />
              </span>
              <span>
                <b>2. “Uygulamayı yükle” / “Ana ekrana ekle”</b>
                <span>
                  Onay penceresinde <strong>Yükle</strong> düğmesine basarak MeDSor’u bağımsız tam
                  ekran uygulama olarak cihazına kur.
                </span>
              </span>
            </li>
          </ul>
        )}
      </div>

      <div className="e12-dlg-f">
        <button
          type="button"
          className="e12-btn is-ghost is-sm"
          onClick={handleEnterFullscreen}
          title="Uygulama içi tam ekran görünümünü aç"
        >
          <Maximize2 aria-hidden="true" />
          Tam Ekran Modu
        </button>
        <span className="e12-grow" />
        {pwaState.hasNativePrompt ? (
          <button type="button" className="e12-btn is-pri" onClick={handleNativeInstall}>
            <Download aria-hidden="true" />
            Uygulamayı Yükle
          </button>
        ) : (
          <button type="button" className="e12-btn is-pri" onClick={() => setOpen(false)}>
            Anladım
          </button>
        )}
      </div>
    </EntryDialogV12>
  );
};

export default PwaInstallGuideModal;
