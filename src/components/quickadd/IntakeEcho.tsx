import React, { useEffect, useState } from 'react';
import { Sparkles, X, AlertTriangle } from 'lucide-react';
import { ApiService, QuestionIntakeSummary } from '../../services/api';

/**
 * Gönderilen serbest metnin sunucuda nasıl ayrıştırıldığını öğrenciye gösterir ("Anladığımız").
 * Ayrıştırma arka planda ücretsiz Gemini ile yapılır; kota doluysa girdi kaydedilmiş olarak bekler.
 * Salt okunur: düzeltmeyi yönetici yapar. Olumsuz kök ihtimali yüksekse işaretlenen cevap için uyarır.
 */
const POLL_MS = 3000;
const MAX_POLLS = 25;

export function IntakeEcho({ intakeId, onClose }: { intakeId: string; onClose: () => void }) {
  const [data, setData] = useState<QuestionIntakeSummary | null>(null);
  const [gaveUp, setGaveUp] = useState(false);

  useEffect(() => {
    let alive = true;
    let n = 0;
    let timer: ReturnType<typeof setTimeout>;
    const tick = async () => {
      const r = await ApiService.getQuestionIntake(intakeId).catch(() => null);
      if (!alive) return;
      if (r) setData(r);
      const pending = !r || r.status === 'bekliyor' || r.status === 'isleniyor';
      if (pending && ++n < MAX_POLLS) timer = setTimeout(tick, POLL_MS);
      else if (pending) setGaveUp(true);
    };
    tick();
    return () => { alive = false; clearTimeout(timer); };
  }, [intakeId]);

  const status = data?.status;
  const pending = !data || status === 'bekliyor' || status === 'isleniyor';

  return (
    <div role="status" aria-live="polite" className="ms-pop-in px-4 py-3 rounded-2xl border border-line-soft bg-accent-soft/40 text-base">
      <div className="flex items-center gap-2">
        <Sparkles className="w-4 h-4 text-accent shrink-0" aria-hidden />
        <span className="font-semibold text-ink">Anladığımız</span>
        <button type="button" onClick={onClose} aria-label="Kapat" className="ml-auto p-1 rounded-full text-ink-3 hover:text-ink cursor-pointer">
          <X className="w-4 h-4" />
        </button>
      </div>

      {pending && !gaveUp && <p className="mt-1 text-ink-3">Yazdığın metin ayrıştırılıyor…</p>}
      {(gaveUp || status === 'kota_bekliyor') && (
        <p className="mt-1 text-ink-3">Metnin kaydedildi. Ayrıştırma sırada; tamamlanınca soru havuzuna işlenir.</p>
      )}
      {status === 'hata' && <p className="mt-1 text-ink-3">Metnin kaydedildi; ayrıştırmayı yönetici yeniden başlatacak.</p>}
      {status === 'icerik_yok' && (
        <p className="mt-1 text-ink-3">Metinde soruya ait bir bilgi bulamadık. Kökten, şıklardan ya da bulgulardan hatırladığını yazabilirsin.</p>
      )}

      {status === 'ayristirildi' && data!.units.map((u, i) => (
        <div key={i} className={i > 0 ? 'mt-3 pt-3 border-t border-line-soft' : 'mt-2'}>
          <p className="text-ink-2">
            <span className="font-medium text-ink">{u.ders === 'Belirsiz' ? 'Ders belirlenemedi' : u.ders}</span>
            {u.konu && <> · {u.konu}</>}
            {u.soruNo && <> · Soru {u.soruNo}</>}
          </p>
          {u.odak && <p className="mt-1 text-ink-2">Sorulan: {u.odak}</p>}
          {u.bulgular.length > 0 && <p className="mt-1 text-ink-2">Kökte: {u.bulgular.join(', ')}</p>}
          {u.siklar.length > 0 && (
            <ul className="mt-1 flex flex-wrap gap-1.5">
              {u.siklar.map((s, j) => (
                <li key={j} className="px-2 py-0.5 rounded-full bg-line-soft/60 text-ink-2 text-sm">
                  {s.harf ? `${s.harf}) ` : ''}{s.metin}
                </li>
              ))}
            </ul>
          )}
          {u.cevap && <p className="mt-1 text-ink-2">İşaretlediğin: {u.cevap.harf ? `${u.cevap.harf}) ` : ''}{u.cevap.metin}</p>}
          {u.olumsuzKok >= 0.5 && (
            <p className="mt-2 flex gap-1.5 text-warn text-sm">
              <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" aria-hidden />
              Soru kökü "hangisi yanlıştır / değildir" olabilir. İşaretlediğin cevabın buna uyduğunu kontrol et.
            </p>
          )}
          {u.eksikler.length > 0 && <p className="mt-1 text-ink-3 text-sm">Eksik: {u.eksikler.join('; ')}</p>}
        </div>
      ))}
    </div>
  );
}
