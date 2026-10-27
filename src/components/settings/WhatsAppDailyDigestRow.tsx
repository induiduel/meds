import React, { useEffect, useState } from 'react';
import {
  MessageCircle,
  Clock,
  Send,
  Sparkles,
  Check,
  AlertCircle,
  Smartphone,
  CheckCircle2,
  BookOpen,
  FileQuestion,
  HelpCircle,
} from 'lucide-react';
import {
  useWhatsAppPrefs,
  fetchWhatsAppStatus,
  sendTestWhatsAppMessage,
  triggerDailyDigestNow,
  type WhatsAppServerStatus,
} from '../../services/whatsappPrefsStore';
import { getYildizliParagraflar } from '../../services/yildizliParagrafStore';
import { getFavoriteCards, getFavorites } from '../../services/studyStore';
import { toast } from '../ui/Toast';

const HOURS = [
  { val: 7, label: '07:00 (Sabah erken)' },
  { val: 8, label: '08:00 (Güne başlarken)' },
  { val: 9, label: '09:00' },
  { val: 12, label: '12:00 (Öğle molası)' },
  { val: 17, label: '17:00' },
  { val: 19, label: '19:00 (Akşam)' },
  { val: 20, label: '20:00' },
  { val: 21, label: '21:00 (Varsayılan · Gece tekrarı)' },
  { val: 22, label: '22:00' },
  { val: 23, label: '23:00' },
];

export const WhatsAppDailyDigestRow: React.FC = () => {
  const [prefs, updatePrefs] = useWhatsAppPrefs();
  const [serverStatus, setServerStatus] = useState<WhatsAppServerStatus | null>(null);
  const [phoneInput, setPhoneInput] = useState(prefs.phone || '');
  const [testing, setTesting] = useState(false);
  const [sendingDigest, setSendingDigest] = useState(false);
  const [expandSettings, setExpandSettings] = useState(prefs.enabled);
  const [statusMessage, setStatusMessage] = useState<{ text: string; isError?: boolean } | null>(null);

  // Mevcut içerik sayıları
  const yildizliSayisi = getYildizliParagraflar().length;
  const kartSayisi = getFavoriteCards().length;
  const soruSayisi = getFavorites().size;

  useEffect(() => {
    void fetchWhatsAppStatus().then(setServerStatus);
  }, []);

  useEffect(() => {
    setPhoneInput(prefs.phone || '');
    if (prefs.enabled) {
      setExpandSettings(true);
    }
  }, [prefs.phone, prefs.enabled]);

  const onToggleEnabled = () => {
    const nextState = !prefs.enabled;
    updatePrefs({ enabled: nextState });
    setExpandSettings(nextState);
    if (nextState) {
      toast.success('WhatsApp günlük tekrarı açıldı', 'Lütfen telefon numaranızı ve gönderim saatinizi kontrol edin.');
    } else {
      toast.info('WhatsApp günlük tekrarı kapatıldı');
    }
  };

  const handlePhoneBlur = () => {
    if (phoneInput !== prefs.phone) {
      updatePrefs({ phone: phoneInput.trim() });
    }
  };

  const handleTestMessage = async () => {
    const phone = (phoneInput || prefs.phone).trim();
    if (!phone) {
      toast.error('Numara eksik', 'Lütfen önce telefon numaranızı girin.');
      return;
    }
    updatePrefs({ phone });
    setTesting(true);
    setStatusMessage(null);
    try {
      const res = await sendTestWhatsAppMessage(phone);
      if (res.success) {
        toast.success('Mesaj Gönderildi', res.message);
        setStatusMessage({ text: '✅ ' + res.message });
      } else {
        toast.error('Gönderilemedi', res.message);
        setStatusMessage({ text: '❌ ' + res.message, isError: true });
      }
    } finally {
      setTesting(false);
    }
  };

  const handleSendDigestNow = async () => {
    const phone = (phoneInput || prefs.phone).trim();
    if (!phone) {
      toast.error('Numara eksik', 'Lütfen önce telefon numaranızı girin.');
      return;
    }
    updatePrefs({ phone });
    setSendingDigest(true);
    setStatusMessage(null);
    try {
      const res = await triggerDailyDigestNow(phone, {
        ...prefs,
        phone,
      });
      if (res.success) {
        toast.success('Günlük Tekrar Gönderildi', res.message);
        setStatusMessage({ text: '✅ ' + res.message });
      } else {
        toast.error('Gönderilemedi', res.message);
        setStatusMessage({ text: '❌ ' + res.message, isError: true });
      }
    } finally {
      setSendingDigest(false);
    }
  };

  const acik = prefs.enabled;

  return (
    <div className="u12-wa-block" style={{ borderBottom: '1px solid var(--color-line)', paddingBottom: '16px', marginBottom: '16px' }}>
      {/* Üst Başlık Satırı */}
      <div className="ui-row has-icon" style={{ alignItems: 'flex-start' }}>
        <span
          className="ui-ico"
          style={
            {
              '--ico-bg': acik ? '#25D366' : 'var(--color-field)',
              '--ico-fg': acik ? '#ffffff' : 'var(--color-ink-3)',
              backgroundColor: acik ? '#25D366' : 'rgba(37, 211, 102, 0.12)',
              color: acik ? '#ffffff' : '#25D366',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '38px',
              height: '38px',
              borderRadius: '10px',
              flexShrink: 0,
            } as React.CSSProperties
          }
        >
          <MessageCircle size={20} strokeWidth={2.2} />
        </span>

        <span className="ui-row-main" style={{ flex: 1, minWidth: 0, paddingRight: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <b style={{ fontSize: '15px' }}>WhatsApp Günlük Tekrarı</b>
            {serverStatus?.configured && (
              <span
                style={{
                  fontSize: '11px',
                  fontWeight: 600,
                  padding: '2px 7px',
                  borderRadius: '12px',
                  background: 'rgba(37, 211, 102, 0.15)',
                  color: '#128C7E',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <CheckCircle2 size={12} /> Meta Cloud API
              </span>
            )}
          </div>
          <span style={{ fontSize: '13px', color: 'var(--color-ink-3)', display: 'block', marginTop: '3px' }}>
            {acik
              ? `Açık — Her gün saat ${String(prefs.hour).padStart(2, '0')}:00'de beğendiğin paragraflar ve kartlar WhatsApp'ına gelir.`
              : `Yıldızladığın (beğendiğin) paragrafları ve favorilerini her gün seçtiğin saatte WhatsApp mesajı olarak al.`}
          </span>
        </span>

        <button
          type="button"
          role="switch"
          aria-checked={acik}
          className={`ui-btn is-sm ${acik ? 'is-tonal' : 'is-primary'}`}
          onClick={onToggleEnabled}
          style={{ alignSelf: 'flex-start' }}
        >
          {acik ? 'Kapat' : 'Aç'}
        </button>
      </div>

      {/* Tercih ve Yapılandırma Paneli */}
      {expandSettings && (
        <div
          style={{
            marginTop: '16px',
            marginLeft: '46px',
            padding: '16px',
            borderRadius: '12px',
            background: 'var(--color-bg-subtle, rgba(0,0,0,0.03))',
            border: '1px solid var(--color-line)',
            display: 'flex',
            flexDirection: 'column',
            gap: '14px',
          }}
        >
          {/* Telefon Numarası Alanı */}
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '6px', color: 'var(--color-ink)' }}>
              WhatsApp Telefon Numarası
            </label>
            <div style={{ display: 'flex', gap: '8px', maxWidth: '360px' }}>
              <div style={{ position: 'relative', flex: 1 }}>
                <input
                  type="tel"
                  placeholder="05xx xxx xx xx"
                  value={phoneInput}
                  onChange={(e) => setPhoneInput(e.target.value)}
                  onBlur={handlePhoneBlur}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    border: '1px solid var(--color-line)',
                    background: 'var(--color-field)',
                    fontSize: '14px',
                    outline: 'none',
                  }}
                />
              </div>
            </div>
            <p style={{ margin: '4px 0 0', fontSize: '11px', color: 'var(--color-ink-3)' }}>
              Türkiye için 05xx veya 905xx formatında girebilirsiniz.
            </p>
          </div>

          {/* Gönderim Saati */}
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '6px', color: 'var(--color-ink)' }}>
              <Clock size={13} style={{ display: 'inline', verticalAlign: '-2px', marginRight: '4px' }} />
              Günlük Gönderim Saati
            </label>
            <select
              value={prefs.hour}
              onChange={(e) => updatePrefs({ hour: parseInt(e.target.value, 10) })}
              style={{
                maxWidth: '360px',
                width: '100%',
                padding: '8px 10px',
                borderRadius: '8px',
                border: '1px solid var(--color-line)',
                background: 'var(--color-field)',
                fontSize: '13px',
                outline: 'none',
              }}
            >
              {HOURS.map((h) => (
                <option key={h.val} value={h.val}>
                  {h.label}
                </option>
              ))}
            </select>
          </div>

          {/* İçerik Seçenekleri (Öğrencinin Özelleştirebileceği Kutular) */}
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, marginBottom: '8px', color: 'var(--color-ink)' }}>
              Mesajda Yer Alacak İçerikler
            </label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {/* Yıldızlı Paragraflar */}
              <label
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  fontSize: '13px',
                  cursor: 'pointer',
                  userSelect: 'none',
                }}
              >
                <input
                  type="checkbox"
                  checked={prefs.includeStarredParagraphs}
                  onChange={(e) => updatePrefs({ includeStarredParagraphs: e.target.checked })}
                  style={{ width: '16px', height: '16px', accentColor: '#25D366' }}
                />
                <span>
                  <b>Yıldızlı / Beğenilen Paragraflar</b>{' '}
                  <span style={{ fontSize: '11px', color: 'var(--color-ink-3)' }}>
                    ({yildizliSayisi} adet kayıtlı)
                  </span>
                </span>
              </label>

              {/* Favori Bilgi Kartları */}
              <label
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  fontSize: '13px',
                  cursor: 'pointer',
                  userSelect: 'none',
                }}
              >
                <input
                  type="checkbox"
                  checked={prefs.includeFavoriteCards}
                  onChange={(e) => updatePrefs({ includeFavoriteCards: e.target.checked })}
                  style={{ width: '16px', height: '16px', accentColor: '#25D366' }}
                />
                <span>
                  <b>Favori Bilgi Kartları (Flashcards)</b>{' '}
                  <span style={{ fontSize: '11px', color: 'var(--color-ink-3)' }}>
                    ({kartSayisi} adet kayıtlı)
                  </span>
                </span>
              </label>

              {/* Favori Sorular */}
              <label
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  fontSize: '13px',
                  cursor: 'pointer',
                  userSelect: 'none',
                }}
              >
                <input
                  type="checkbox"
                  checked={prefs.includeFavoriteQuestions}
                  onChange={(e) => updatePrefs({ includeFavoriteQuestions: e.target.checked })}
                  style={{ width: '16px', height: '16px', accentColor: '#25D366' }}
                />
                <span>
                  <b>Favori Çıkmış Sorular</b>{' '}
                  <span style={{ fontSize: '11px', color: 'var(--color-ink-3)' }}>
                    ({soruSayisi} adet kayıtlı)
                  </span>
                </span>
              </label>
            </div>
          </div>

          {/* Miktar Tercihi */}
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
            {prefs.includeStarredParagraphs && (
              <div style={{ flex: '1 1 140px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, marginBottom: '4px', color: 'var(--color-ink-3)' }}>
                  Günde kaç paragraf?
                </label>
                <select
                  value={prefs.paragraphCount || 1}
                  onChange={(e) => updatePrefs({ paragraphCount: parseInt(e.target.value, 10) })}
                  style={{
                    width: '100%',
                    padding: '6px 8px',
                    borderRadius: '6px',
                    border: '1px solid var(--color-line)',
                    background: 'var(--color-field)',
                    fontSize: '12px',
                  }}
                >
                  <option value={1}>1 paragraf</option>
                  <option value={2}>2 paragraf</option>
                  <option value={3}>3 paragraf</option>
                </select>
              </div>
            )}

            {prefs.includeFavoriteCards && (
              <div style={{ flex: '1 1 140px' }}>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, marginBottom: '4px', color: 'var(--color-ink-3)' }}>
                  Günde kaç bilgi kartı?
                </label>
                <select
                  value={prefs.cardCount || 1}
                  onChange={(e) => updatePrefs({ cardCount: parseInt(e.target.value, 10) })}
                  style={{
                    width: '100%',
                    padding: '6px 8px',
                    borderRadius: '6px',
                    border: '1px solid var(--color-line)',
                    background: 'var(--color-field)',
                    fontSize: '12px',
                  }}
                >
                  <option value={1}>1 bilgi kartı</option>
                  <option value={2}>2 bilgi kartı</option>
                  <option value={3}>3 bilgi kartı</option>
                </select>
              </div>
            )}
          </div>

          {/* Durum / Geri Bildirim Notu */}
          {statusMessage && (
            <div
              style={{
                fontSize: '12px',
                padding: '8px 12px',
                borderRadius: '8px',
                background: statusMessage.isError ? 'rgba(239, 68, 68, 0.1)' : 'rgba(34, 197, 94, 0.1)',
                color: statusMessage.isError ? '#dc2626' : '#16a34a',
                border: `1px solid ${statusMessage.isError ? 'rgba(239, 68, 68, 0.2)' : 'rgba(34, 197, 94, 0.2)'}`,
              }}
            >
              {statusMessage.text}
            </div>
          )}

          {/* Test Butonları */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', paddingTop: '4px' }}>
            <button
              type="button"
              className="u12-btn is-sm"
              disabled={testing || !phoneInput}
              onClick={handleTestMessage}
              style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            >
              <Send size={13} />
              {testing ? 'Gönderiliyor…' : 'Test Mesajı Gönder'}
            </button>

            <button
              type="button"
              className="u12-btn is-sm is-pri"
              disabled={sendingDigest || !phoneInput}
              onClick={handleSendDigestNow}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                backgroundColor: '#25D366',
                borderColor: '#25D366',
                color: '#062A14', // WhatsApp yeşilinde beyaz yazı 2:1 kalıyordu
              }}
            >
              <Sparkles size={13} />
              {sendingDigest ? 'Hazırlanıyor…' : 'Şimdi Günlük Tekrar Gönder'}
            </button>
          </div>

          {/* Alt bilgilendirme */}
          <div style={{ fontSize: '11px', color: 'var(--color-ink-3)', lineHeight: 1.4 }}>
            {!serverStatus?.configured ? (
              <span style={{ color: '#d97706' }}>
                ⚠️ Sunucuda Meta WhatsApp Cloud API anahtarları henüz girilmemiş (.env: <code>WHATSAPP_PHONE_NUMBER_ID</code> ve <code>WHATSAPP_ACCESS_TOKEN</code>). Tercihleriniz profilinize kaydedilir; API bağlandığında otomatik gönderilir.
              </span>
            ) : (
              <span>
                💡 Yıldızlı paragraflarınız ve favori kartlarınızdan her gün rastgele seçim yapılarak doğrudan WhatsApp numaranıza iletilir.
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
