import React, { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Combine, RefreshCw, Send, ShieldCheck, Sparkles, TriangleAlert } from 'lucide-react';
import { ApiService } from '../../services/api';
import { YonetimApi } from '../../services/api/yonetim';
import { toast } from '../ui/Toast';
import { Sheet } from '../ui/Sheet';
import { confirmDialog } from '../ui/ConfirmDialog';
import { AppUser } from '../../services/auth';
import { disciplineClass, disciplineLabel } from '../../utils/discipline';
import './clusterPool.css';

export interface QuestionClusterItem {
  id: string;
  clusterTitle: string;
  committeeId: string;
  discipline: string;
  sourceQuestionIds: string[];
  mergedQuestionCount: number;
  mergedStem: string;
  mergedOptions: Array<{ key: string; text: string; votes?: number; conflict?: string[]; source?: 'ogrenci' | 'ders_notu' | 'eksik'; isAiFilled?: boolean }>;
  claimedAnswer: string;
  explanation: string;
  // kume-v2 alanları (src/services/poolClusterService.ts); eski kayıtlarda yok
  questionNumber?: number | null;
  anchorQuestionId?: string | null;
  sourceIntakeUnits?: string[];
  stemFragments?: { key: string; text: string }[];
  unplacedOptions?: { text: string; votes: number }[];
  answerVotes?: Record<string, number>;
  negativeStemLikely?: boolean;
  sharedTerms?: string[];
  cohesion?: number;
  aiMerged?: boolean;
  aiAnswerSuggestion?: string;
  sources?: { title?: string; documentTitle?: string; source?: string }[];
  // kume-v3 (src/services/recall/): temsilci öğrenci cümlesi, ders güveni, önceki yıllarda çıkmış eşleşme
  stemSource?: 'ogrenci' | 'yapay_zeka';
  draft?: {
    stem: string;
    discipline?: { name: string; p: number } | null;
    konu?: string | null;
    answerTextVotes?: { text: string; votes: number }[];
    bankMatch?: { id: string; score: number; margin: number; support: number; stem: string; options: { key: string; text: string }[]; correctAnswer: string } | null;
  };
  status: 'proposal';
  isLockedForDeletion: boolean;
  studentContributions: Array<{
    id: string;
    studentName: string;
    studentUid?: string;
    text: string;
    createdAt: string;
  }>;
  createdAt: string;
  updatedAt: string;
}

interface QuestionClusterAutomationModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentUser?: AppUser | null;
  isAdmin?: boolean;
  /** Yalnız bu kurulun kümeleri (soru havuzunda seçili kurul) */
  committeeId?: string;
  /** Açılınca doğrudan bu kümenin ayrıntısı */
  focusClusterId?: string | null;
}

const FAILED = /^\s*\[BİRLEŞTİRİLEMEDİ\]\s*/i;

/** Kümenin durumu: birleştirilemedi (yönetici bakmalı) · birleştirme bekliyor · öneri taslağı */
function clusterState(c: QuestionClusterItem): { label: string; tone: string } {
  if (FAILED.test(c.mergedStem || '')) return { label: 'İnceleme gerekli', tone: 'is-bad' };
  if (!c.aiMerged) return { label: 'Birleştirme bekliyor', tone: 'is-warn' };
  return { label: 'Öneri taslağı', tone: 'is-accent' };
}

const initials = (name: string) =>
  name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0]?.toLocaleUpperCase('tr-TR'))
    .join('') || '?';

/**
 * Öneri taslak havuzu (soru havuzu → "Öneri Taslak Havuzu"). Aynı soruyu hatırlayan parçaların birleştirildiği
 * kümeler listelenir; birine dokununca sayfa içinde ayrıntıya geçilir (kök, şıklar ve oylar, birleştirme gerekçesi,
 * öğrenci katkıları). Öğrenci yalnız katkı ekler; silme/onay yöneticidedir. Renkler yalnız token + ders rengi (.d-*).
 */
export const QuestionClusterAutomationModal: React.FC<QuestionClusterAutomationModalProps> = ({ isOpen, onClose, currentUser, isAdmin, committeeId, focusClusterId }) => {
  const [clusters, setClusters] = useState<QuestionClusterItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningPipeline, setRunningPipeline] = useState(false);
  const [openId, setOpenId] = useState<string | null>(null);
  const [draft, setDraft] = useState<Record<string, string>>({});
  const [submittingId, setSubmittingId] = useState<string | null>(null);
  const bodyTop = useRef<HTMLDivElement>(null);

  const fetchClusters = async () => {
    setLoading(true);
    try {
      const all: QuestionClusterItem[] = await ApiService.getPoolQuestionClusters();
      setClusters(committeeId ? all.filter((c) => c.committeeId === committeeId) : all);
    } catch (e: any) {
      toast.error('Hata', 'Kümeler yüklenemedi: ' + (e.message || ''));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      setOpenId(focusClusterId || null);
      fetchClusters();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, committeeId, focusClusterId]);

  // Liste ↔ ayrıntı geçişinde kaydırmayı başa al
  useEffect(() => {
    bodyTop.current?.scrollIntoView({ block: 'start' });
  }, [openId]);

  const handleRunPipeline = async () => {
    setRunningPipeline(true);
    try {
      const res = await YonetimApi.runPoolQuestionClusterPipeline();
      toast.success('Otomasyon başlatıldı', res.message);
      window.setTimeout(fetchClusters, 3000);
    } catch (e: any) {
      toast.error('Hata', e.message || 'Otomasyon başlatılamadı.');
    } finally {
      setRunningPipeline(false);
    }
  };

  const handleAddContribution = async (clusterId: string) => {
    const text = (draft[clusterId] || '').trim();
    if (!text) return;
    setSubmittingId(clusterId);
    try {
      const studentName = currentUser?.displayName || currentUser?.email || 'Tıp Öğrencisi';
      const res = await YonetimApi.contributeToPoolCluster(clusterId, studentName, text, currentUser?.uid);
      toast.success('Katkın eklendi', 'Öneri taslağına eklemen kaydedildi.');
      setDraft((prev) => ({ ...prev, [clusterId]: '' }));
      setClusters((prev) =>
        prev.map((c) =>
          c.id === clusterId ? res.cluster || { ...c, studentContributions: [...(c.studentContributions || []), res.contribution] } : c,
        ),
      );
    } catch (e: any) {
      toast.error('Hata', e.message || 'Katkı eklenemedi.');
    } finally {
      setSubmittingId(null);
    }
  };

  // Yönetici: yanlış birleşmiş parçayı ayır (kalıcı "farklı soru" kısıtı; kümeler sunucuda baştan kurulur)
  const [splittingKey, setSplittingKey] = useState<string | null>(null);
  const handleSplit = async (clusterId: string, key: string, text: string) => {
    const ok = await confirmDialog({
      title: 'Bu parça farklı bir soru mu?',
      message: `“${text.slice(0, 160)}” bu kümeden çıkarılır ve kümedeki diğer parçalarla bir daha birleştirilmez.`,
      confirmLabel: 'Ayır',
    });
    if (!ok) return;
    setSplittingKey(key);
    try {
      const all: QuestionClusterItem[] = await YonetimApi.splitPoolClusterMember(clusterId, key);
      const list = committeeId ? all.filter((c) => c.committeeId === committeeId) : all;
      setClusters(list);
      // Küme ikiye bölünüp tekile düştüyse ayrıntı kapanır
      if (!list.some((c) => c.id === clusterId && c.mergedQuestionCount >= 2)) setOpenId(null);
      toast.success('Parça ayrıldı', 'Bu parça artık bu kümedeki diğer parçalarla birleştirilmeyecek.');
    } catch (e: any) {
      toast.error('Hata', e.message || 'Parça ayrılamadı.');
    } finally {
      setSplittingKey(null);
    }
  };

  const current = openId ? clusters.find((c) => c.id === openId) || null : null;
  const pending = clusters.filter((c) => clusterState(c).tone !== 'is-accent').length;

  return (
    <Sheet
      open={isOpen}
      onClose={onClose}
      size="full"
      width={760}
      title="Öneri taslak havuzu"
      subtitle={
        loading
          ? 'Kümeler yükleniyor…'
          : clusters.length
            ? `${clusters.length} küme${pending ? ` · ${pending} tanesi inceleme bekliyor` : ''}`
            : 'Henüz küme yok'
      }
      actions={
        <button type="button" className="qpool-iconbtn" onClick={fetchClusters} disabled={loading} aria-label="Yenile" title="Yenile">
          <RefreshCw className={loading ? 'animate-spin' : ''} />
        </button>
      }
      footer={
        isAdmin ? (
          <button type="button" className={`ui-btn is-primary ${runningPipeline ? 'is-loading' : ''}`} disabled={runningPipeline} onClick={handleRunPipeline}>
            <Sparkles /> Otomasyonu çalıştır
          </button>
        ) : undefined
      }
    >
      <div className="qpool" ref={bodyTop}>
        {current ? (
          <ClusterDetail
            cluster={current}
            draft={draft[current.id] || ''}
            submitting={submittingId === current.id}
            onDraft={(v) => setDraft((p) => ({ ...p, [current.id]: v }))}
            onSubmit={() => handleAddContribution(current.id)}
            onBack={() => setOpenId(null)}
            onSplit={isAdmin && current.mergedQuestionCount >= 2 ? (key, text) => handleSplit(current.id, key, text) : undefined}
            splittingKey={splittingKey}
          />
        ) : (
          <>
            <div className="ui-callout">
              <ShieldCheck aria-hidden />
              <div>
                Aynı soruyu hatırlayan parçalar ders, soru numarası ve ortak terimlerle birleştirilir; şıklar öğrenci oylarıyla
                kurulur. Yapay zekâ kökü ders notuyla tamamlar, cevabı kendisi seçmez.
                <span className="qpool-callout-sub">Taslaklara yalnız ekleme yapabilirsin; silme ve onay yöneticidedir.</span>
              </div>
            </div>

            {loading ? (
              <div className="ui-group" aria-busy="true">
                {[0, 1, 2].map((i) => (
                  <div key={i} className="qpool-row">
                    <span className="ui-skel qpool-skel-ico" />
                    <span className="qpool-row-main">
                      <span className="ui-skel" style={{ height: 14, width: '62%' }} />
                      <span className="ui-skel" style={{ height: 11, width: '38%', marginTop: 6 }} />
                    </span>
                  </div>
                ))}
              </div>
            ) : clusters.length === 0 ? (
              <div className="qpool-empty">
                <span className="qpool-empty-ic"><Combine aria-hidden /></span>
                <b>Henüz birleştirilmiş küme yok</b>
                <span>
                  {isAdmin
                    ? 'Aşağıdaki “Otomasyonu çalıştır” ile havuzdaki parçaları eşleştirebilirsin.'
                    : 'Havuza yeterince parça girildiğinde kümeler burada görünür.'}
                </span>
              </div>
            ) : (
              <div className="ui-group">
                {clusters.map((c) => {
                  const st = clusterState(c);
                  const meta = [
                    c.questionNumber ? `Soru ${c.questionNumber}` : null,
                    `${c.mergedQuestionCount} parça`,
                    typeof c.cohesion === 'number' ? `uyum %${Math.round(c.cohesion * 100)}` : null,
                    c.studentContributions?.length ? `${c.studentContributions.length} katkı` : null,
                  ].filter(Boolean);
                  return (
                    <button key={c.id} type="button" className={`qpool-row is-btn ${disciplineClass(c.discipline)}`} onClick={() => setOpenId(c.id)}>
                      <span className="qpool-count" aria-label={`${c.mergedQuestionCount} parça`}>{c.mergedQuestionCount}</span>
                      <span className="qpool-row-main">
                        <span className="qpool-eyebrow">
                          {disciplineLabel(c.discipline)} · {c.committeeId}
                        </span>
                        <b>{c.clusterTitle}</b>
                        <span className="qpool-meta">{meta.join(' · ')}</span>
                      </span>
                      <span className="qpool-row-end">
                        <span className={`ui-tag ${st.tone}`}>{st.label}</span>
                        <ChevronRight aria-hidden className="qpool-chev" />
                      </span>
                    </button>
                  );
                })}
              </div>
            )}
          </>
        )}
      </div>
    </Sheet>
  );
};

const ClusterDetail: React.FC<{
  cluster: QuestionClusterItem;
  draft: string;
  submitting: boolean;
  onDraft: (v: string) => void;
  onSubmit: () => void;
  onBack: () => void;
  /** Yalnız yöneticide: parçayı "farklı soru" diye ayır. */
  onSplit?: (key: string, text: string) => void;
  splittingKey?: string | null;
}> = ({ cluster: c, draft, submitting, onDraft, onSubmit, onBack, onSplit, splittingKey }) => {
  const st = clusterState(c);
  const failed = FAILED.test(c.mergedStem || '');
  const stem = (c.mergedStem || '').replace(FAILED, '');
  const totalVotes = Math.max(1, ...c.mergedOptions.map((o) => o.votes || 0));
  const answer = (c.claimedAnswer || '').toUpperCase();
  const contributions = c.studentContributions || [];

  return (
    <div className={`qpool-detail ${disciplineClass(c.discipline)}`}>
      <button type="button" className="qpool-back" onClick={onBack}>
        <ChevronLeft aria-hidden /> Tüm kümeler
      </button>

      <header className="qpool-head">
        <div className="qpool-tags">
          <span className="ui-tag qpool-disc">{disciplineLabel(c.discipline)}</span>
          <span className="ui-tag">{c.committeeId}</span>
          {c.questionNumber ? <span className="ui-tag">Soru {c.questionNumber}</span> : null}
          <span className={`ui-tag ${st.tone}`}>{st.label}</span>
        </div>
        <h3>{c.clusterTitle}</h3>
        <dl className="qpool-stats">
          <div><dt>Parça</dt><dd>{c.mergedQuestionCount}</dd></div>
          {typeof c.cohesion === 'number' && <div title="Üyelerin ortalama benzerliği"><dt>Uyum</dt><dd>%{Math.round(c.cohesion * 100)}</dd></div>}
          <div><dt>Katkı</dt><dd>{contributions.length}</dd></div>
        </dl>
      </header>

      {failed && (
        <div className="ui-callout is-bad">
          <TriangleAlert aria-hidden />
          <div>{stem || 'Parçalar birleştirilemedi.'}</div>
        </div>
      )}

      {!failed && (
        <section className="ui-section">
          <div className="ui-section-h">
            <h2>
              {c.aiMerged && c.stemSource !== 'ogrenci'
                ? 'Önerilen kök · ders notuyla birleştirildi'
                : c.stemSource === 'ogrenci'
                  ? 'En kapsamlı hatırlama · yazımı düzeltildi'
                  : 'Önerilen kök · birleştirme bekliyor'}
            </h2>
          </div>
          <div className="ui-card qpool-stem">{stem}</div>
          {c.draft?.discipline && (
            <p className="ui-section-foot">
              Ders tahmini: {c.draft.discipline.name} (%{Math.round(c.draft.discipline.p * 100)})
              {c.draft.konu ? ` · konu: ${c.draft.konu}` : ''}
            </p>
          )}
        </section>
      )}

      {c.draft?.bankMatch && (
        <section className="ui-section">
          <div className="ui-section-h"><h2>Önceki yıllarda çıkmış benzer soru</h2></div>
          <div className="ui-card qpool-bank">
            <p className="qpool-bank-stem">{c.draft.bankMatch.stem}</p>
            {c.draft.bankMatch.options.length > 0 && (
              <ol className="qpool-bank-opts">
                {c.draft.bankMatch.options.map((o) => (
                  <li key={o.key} className={o.key === c.draft!.bankMatch!.correctAnswer ? 'is-ok' : ''}><i>{o.key}</i>{o.text}</li>
                ))}
              </ol>
            )}
            <p className="qpool-bank-note">
              Hatırlamaların %{Math.round(c.draft.bankMatch.support * 100)}'i bu soruya yaslanıyor (benzerlik {c.draft.bankMatch.score.toFixed(2)}).
              Aynı soru tekrar sorulmuş olabilir; şıkları ve cevabı öğrencilerin hatırladıklarıyla karşılaştır.
            </p>
          </div>
        </section>
      )}

      {c.negativeStemLikely && (
        <div className="ui-callout is-warn">
          <TriangleAlert aria-hidden />
          <div>Kök büyük olasılıkla olumsuz (“hangisi yanlıştır / değildir”); oyları doğrudan cevap sayma.</div>
        </div>
      )}

      <section className="ui-section">
        <div className="ui-section-h"><h2>Şıklar</h2></div>
        <ol className="ui-group qpool-opts">
          {c.mergedOptions.map((o) => {
            const isAnswer = !!answer && o.key.toUpperCase() === answer;
            const missing = o.source === 'eksik' || o.text === '[EKSİK ŞIK]';
            const votes = o.source === 'ogrenci' && !o.isAiFilled ? o.votes || 0 : 0;
            const origin = votes ? `${votes} öğrenci` : o.source === 'ders_notu' ? 'ders notundan' : o.isAiFilled ? 'yapay zekâ' : '';
            return (
              <li key={o.key} className={`qpool-opt ${isAnswer ? 'is-answer' : ''} ${missing ? 'is-missing' : ''}`}>
                <i>{o.key}</i>
                <div className="qpool-opt-main">
                  <span>{missing ? 'Hatırlanmayan şık' : o.text}</span>
                  {o.conflict && o.conflict.length > 0 && <small className="qpool-conflict">Çelişen hatıra: {o.conflict.join(' · ')}</small>}
                  {votes > 0 && <span className="qpool-bar" aria-hidden><s style={{ width: `${(votes / totalVotes) * 100}%` }} /></span>}
                </div>
                {origin && <span className="qpool-opt-end">{origin}</span>}
              </li>
            );
          })}
        </ol>
        <p className="ui-section-foot">
          {c.answerVotes && Object.keys(c.answerVotes).length ? (
            <>
              İşaretlenen cevap oyları: {Object.entries(c.answerVotes).map(([k, v]) => `${k} ${v}`).join(' · ')}
              {c.claimedAnswer ? ` → çoğunluk ${c.claimedAnswer}` : ' → çoğunluk yok'}
            </>
          ) : (
            'İşaretlenen cevap bildirilmedi.'
          )}
          {c.aiAnswerSuggestion && <> · Ders notuna göre öneri: <b>{c.aiAnswerSuggestion}</b></>}
          {c.unplacedOptions && c.unplacedOptions.length > 0 && (
            <><br />Harfi hatırlanmayan şıklar: {c.unplacedOptions.map((o) => `${o.text} (${o.votes})`).join(' · ')}</>
          )}
        </p>
      </section>

      {c.explanation && (
        <section className="ui-section">
          <div className="ui-section-h"><h2>Birleştirme notu</h2></div>
          <div className="ui-card qpool-prose">{c.explanation}</div>
        </section>
      )}

      <section className="ui-section">
        <div className="ui-section-h"><h2>Neden birleşti</h2></div>
        <div className="ui-card qpool-why">
          {c.sharedTerms && c.sharedTerms.length > 0 && (
            <div className="qpool-terms">
              {c.sharedTerms.map((t) => <span key={t} className="ui-tag">{t}</span>)}
            </div>
          )}
          {c.stemFragments && c.stemFragments.length > 0 ? (
            <ul className="qpool-frags">
              {c.stemFragments.map((f) => (
                <li key={f.key} className={onSplit ? 'has-act' : undefined}>
                  <span>“{f.text}”{f.key.startsWith('u:') && <em> · serbest girdi</em>}</span>
                  {onSplit && (
                    <button
                      type="button"
                      className={`ui-btn is-ghost is-sm ${splittingKey === f.key ? 'is-loading' : ''}`}
                      disabled={!!splittingKey}
                      onClick={() => onSplit(f.key, f.text)}
                      title="Bu parça farklı bir soruyu anlatıyor: kümeden çıkar, bir daha birleştirme"
                    >
                      Farklı soru
                    </button>
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <p className="qpool-muted">Kayıtlar: {c.sourceQuestionIds.join(', ')}</p>
          )}
          {c.sources && c.sources.length > 0 && (
            <p className="qpool-muted">Ders notu kaynakları: {c.sources.map((x) => x.documentTitle || x.title || x.source).filter(Boolean).join(' · ')}</p>
          )}
        </div>
      </section>

      <section className="ui-section">
        <div className="ui-section-h">
          <h2>Katkılar{contributions.length ? ` (${contributions.length})` : ''}</h2>
        </div>
        <div className="ui-group">
          {contributions.map((k) => (
            <div key={k.id} className="qpool-contrib">
              <span className="qpool-av" aria-hidden>{initials(k.studentName)}</span>
              <div className="qpool-contrib-main">
                <div><b>{k.studentName}</b><time>{new Date(k.createdAt).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}</time></div>
                <p>{k.text}</p>
              </div>
            </div>
          ))}
          {contributions.length === 0 && <p className="qpool-contrib-empty">Henüz katkı yok. Hatırladığın bir şık, ayrıntı ya da kaynak ekleyebilirsin.</p>}
          <form
            className="qpool-compose"
            onSubmit={(e) => {
              e.preventDefault();
              onSubmit();
            }}
          >
            <input
              className="ui-input"
              value={draft}
              onChange={(e) => onDraft(e.target.value)}
              placeholder="Ekleme ya da hatırlatma notu yaz…"
              aria-label="Katkı notu"
            />
            <button type="submit" className={`ui-btn is-primary ${submitting ? 'is-loading' : ''}`} disabled={submitting || !draft.trim()}>
              <Send /> Ekle
            </button>
          </form>
        </div>
        <p className="ui-section-foot">Katkılar taslağa eklenir; taslağı değiştirmez ya da onaylamaz.</p>
      </section>
    </div>
  );
};
