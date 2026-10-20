import React, { useEffect, useMemo, useState } from 'react';
import { SlidersHorizontal, Download, Wrench } from 'lucide-react';
import type { Committee, QuestionItem } from '../../../types';
import { ApiService } from '../../../services/api';
import { Drawer } from '../../manage/consoleUi';
import { AdminPanelModal } from '../../AdminPanelModal';
import { AdminEditQuestionModal } from '../../AdminEditQuestionModal';
import { PageActions, StatRow, Tabs14, SearchField, Toolbar, DataTable, Pill, DetailNav, DetailLayout, FactList, Card14, type Col } from '../pageKit';
import { BulkBar, useSelection, type BulkAction } from '../manageKit';

/**
 * v14 Soru havuzu (canvas SoruHavuzu.dc.html): sayı kartları, durum/kaynak sekmeleri, arama,
 * açıldığında görünen süzgeç alanı, seçimli tablo + sayfalama, toplu işlem, tam alan ayrıntı.
 * Eski araçlar (içe aktarma vb.) "Gelişmiş araçlar" çalışma alanında AdminPanelModal ile korunur.
 */

type Status = QuestionItem['status'];
type StatusTab = 'all' | Status;
type SourceTab = 'all' | 'past' | 'student' | 'other';

const STATUS_LABEL: Record<Status, string> = { completed: 'Tamamlandı', reconstructing: 'Yeniden kuruluyor', gathering: 'Toplanıyor', empty: 'Boş' };
const STATUS_TONE: Record<Status, 'ok' | 'warn' | 'acc' | ''> = { completed: 'ok', reconstructing: 'acc', gathering: 'warn', empty: '' };
const PAGE = 50;

const sourceOf = (q: QuestionItem): Exclude<SourceTab, 'all'> => (q.isPastExam ? 'past' : q.contributedByUid ? 'student' : 'other');
const SOURCE_LABEL: Record<Exclude<SourceTab, 'all'>, string> = { past: 'Çıkmış', student: 'Öğrenci', other: 'Diğer' };
const stemOf = (q: QuestionItem) => q.reconstruction?.stem || q.rawStem || '';
const optionsOf = (q: QuestionItem) => (q.reconstruction?.options?.length ? q.reconstruction.options : q.options || []);
const answerOf = (q: QuestionItem) => q.reconstruction?.correctAnswer || q.correctAnswer || q.claimedAnswer;

const download = (name: string, text: string, type: string) => {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement('a');
  a.href = url; a.download = name; a.click();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
};
const csvCell = (v: unknown) => `"${String(v ?? '').replace(/"/g, '""')}"`;
const toCsv = (rows: QuestionItem[]) => {
  const head = ['id', 'kurul', 'no', 'brans', 'konu', 'durum', 'kaynak', 'soru', 'A', 'B', 'C', 'D', 'E', 'cevap', 'etiketler'];
  const lines = rows.map((q) => {
    const o = optionsOf(q);
    const opt = (k: string) => o.find((x) => x.key === k)?.text || '';
    return [q.id, q.committeeId, q.questionNumber, q.discipline, q.topic, STATUS_LABEL[q.status] || q.status, SOURCE_LABEL[sourceOf(q)], stemOf(q),
      opt('A'), opt('B'), opt('C'), opt('D'), opt('E'), answerOf(q) || '', (q.tags || []).join('; ')].map(csvCell).join(',');
  });
  return '﻿' + [head.join(','), ...lines].join('\n');
};

export const ManagePoolV14: React.FC<{
  adminEmail: string;
  committees: Committee[];
  questions: QuestionItem[];
  selectedCommitteeId: string;
  onRefreshData: () => Promise<void> | void;
  onExit: () => void;
}> = ({ adminEmail, committees, questions, selectedCommitteeId, onRefreshData, onExit }) => {
  const [statusTab, setStatusTab] = useState<StatusTab>('all');
  const [sourceTab, setSourceTab] = useState<SourceTab>('all');
  const [q, setQ] = useState('');
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [discipline, setDiscipline] = useState('');
  const [topic, setTopic] = useState('');
  const [page, setPage] = useState(0);
  const [openId, setOpenId] = useState<string | null>(null);
  const [editing, setEditing] = useState<QuestionItem | null>(null);
  const [advanced, setAdvanced] = useState(false);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState('');
  const [bulkForm, setBulkForm] = useState<null | 'tag' | 'move' | 'status'>(null);
  const [bulkValue, setBulkValue] = useState('');
  const [hidden, setHidden] = useState<Set<string>>(() => new Set());
  const [confirmDel, setConfirmDel] = useState(false);
  const sel = useSelection<string>();

  const base = useMemo(
    () => questions.filter((x) => x.committeeId === selectedCommitteeId && !hidden.has(x.id)),
    [questions, selectedCommitteeId, hidden],
  );
  const disciplines = useMemo(() => Array.from(new Set(base.map((x) => x.discipline).filter(Boolean))).sort((a, b) => a.localeCompare(b, 'tr')), [base]);
  const topics = useMemo(
    () => Array.from(new Set(base.filter((x) => !discipline || x.discipline === discipline).map((x) => x.topic).filter(Boolean))).sort((a, b) => a.localeCompare(b, 'tr')),
    [base, discipline],
  );

  const filtered = useMemo(() => {
    const needle = q.trim().toLocaleLowerCase('tr');
    return base
      .filter((x) => statusTab === 'all' || x.status === statusTab)
      .filter((x) => sourceTab === 'all' || sourceOf(x) === sourceTab)
      .filter((x) => !discipline || x.discipline === discipline)
      .filter((x) => !topic || x.topic === topic)
      .filter((x) => !needle || `${x.id} ${x.questionNumber} ${stemOf(x)} ${x.topic} ${x.discipline} ${(x.tags || []).join(' ')}`.toLocaleLowerCase('tr').includes(needle))
      .sort((a, b) => (a.questionNumber || 0) - (b.questionNumber || 0));
  }, [base, statusTab, sourceTab, discipline, topic, q]);

  useEffect(() => setPage(0), [statusTab, sourceTab, discipline, topic, q, selectedCommitteeId]);
  const pages = Math.max(1, Math.ceil(filtered.length / PAGE));
  const pageRows = filtered.slice(page * PAGE, page * PAGE + PAGE);
  const current = openId ? base.find((x) => x.id === openId) || null : null;
  const picked = useMemo(() => base.filter((x) => sel.has(x.id)), [base, sel]);

  const count = (s: Status) => base.filter((x) => x.status === s).length;
  const committeeName = committees.find((c) => c.id === selectedCommitteeId)?.name || selectedCommitteeId;
  const activeFilters = (discipline ? 1 : 0) + (topic ? 1 : 0);

  const runBulk = async (label: string, list: QuestionItem[], fn: (x: QuestionItem) => Promise<unknown>) => {
    if (!list.length) return;
    setBusy(true);
    let ok = 0, bad = 0;
    for (const x of list) {
      try { await fn(x); ok++; } catch { bad++; }
    }
    setMsg(`${label}: ${ok.toLocaleString('tr-TR')} başarılı, ${bad.toLocaleString('tr-TR')} hata.`);
    setBusy(false);
    await onRefreshData();
  };
  const del = async (list: QuestionItem[]) => {
    setHidden((h) => new Set([...h, ...list.map((x) => x.id)]));
    let failed: string[] = [];
    await runBulk('Silme', list, async (x) => {
      try { await ApiService.adminDeleteQuestion(adminEmail, x.id); } catch (e) { failed = [...failed, x.id]; throw e; }
    });
    if (failed.length) setHidden((h) => { const n = new Set(h); failed.forEach((id) => n.delete(id)); return n; });
    sel.clear();
  };
  const applyBulkForm = async () => {
    const v = bulkValue.trim();
    if (!bulkForm || !v) return;
    if (bulkForm === 'tag') await runBulk('Etiketleme', picked, (x) => ApiService.adminUpdateQuestion(adminEmail, x.id, { tags: Array.from(new Set([...(x.tags || []), v])) }));
    if (bulkForm === 'move') await runBulk('Konuya taşıma', picked, (x) => ApiService.adminUpdateQuestion(adminEmail, x.id, { topic: v }));
    if (bulkForm === 'status') await runBulk('Durum değiştirme', picked, (x) => ApiService.adminUpdateQuestion(adminEmail, x.id, { status: v as Status }));
    setBulkForm(null); setBulkValue('');
  };
  const exportRows = (list: QuestionItem[], kind: 'json' | 'csv') => {
    const stamp = new Date().toISOString().slice(0, 10);
    if (kind === 'json') download(`soru-havuzu-${selectedCommitteeId}-${stamp}.json`, JSON.stringify(list, null, 2), 'application/json');
    else download(`soru-havuzu-${selectedCommitteeId}-${stamp}.csv`, toCsv(list), 'text/csv;charset=utf-8');
    setMsg(`${list.length.toLocaleString('tr-TR')} soru dışa aktarıldı.`);
  };

  const bulkActions: BulkAction[] = [
    { label: 'Onayla', kind: 'main', run: () => runBulk('Onaylama', picked, (x) => ApiService.adminUpdateQuestion(adminEmail, x.id, { status: 'completed' })) },
    { label: 'Durum değiştir', run: () => { setBulkForm('status'); setBulkValue('gathering'); } },
    { label: 'Etiketle', run: () => { setBulkForm('tag'); setBulkValue(''); } },
    { label: 'Konuya taşı', run: () => { setBulkForm('move'); setBulkValue(''); } },
    { label: 'JSON olarak indir', run: () => exportRows(picked, 'json') },
    { label: 'CSV olarak indir', run: () => exportRows(picked, 'csv') },
    { label: 'Sil', kind: 'danger', confirm: `${picked.length} soruyu kalıcı sil`, run: () => del(picked) },
  ];

  const cols: Col<QuestionItem>[] = [
    { key: 'no', label: 'No', render: (x) => x.questionNumber, mono: true, width: 64 },
    { key: 'stem', label: 'Soru', main: true, render: (x) => stemOf(x) || <span className="muted">Soru kökü yok</span> },
    { key: 'lesson', label: 'Ders', render: (x) => [x.discipline, x.topic].filter(Boolean).join(' · ') || '—', muted: true, width: 220 },
    { key: 'src', label: 'Kaynak', render: (x) => SOURCE_LABEL[sourceOf(x)], muted: true, width: 90 },
    { key: 'st', label: 'Durum', render: (x) => <Pill tone={STATUS_TONE[x.status]}>{STATUS_LABEL[x.status] || x.status}</Pill>, width: 150 },
  ];

  const nextOf = (x: QuestionItem) => {
    const i = filtered.findIndex((r) => r.id === x.id);
    return i >= 0 && i < filtered.length - 1 ? filtered[i + 1] : null;
  };
  const approveAndNext = async (x: QuestionItem) => {
    const nx = nextOf(x);
    await runBulk('Onaylama', [x], (r) => ApiService.adminUpdateQuestion(adminEmail, r.id, { status: 'completed' }));
    setOpenId(nx ? nx.id : null);
  };

  return (
    <div className="pk14-page">
      <PageActions note={`${committeeName} · ${base.length.toLocaleString('tr-TR')} soru`}>
        <button type="button" className="m14-btn" onClick={() => exportRows(filtered, 'json')}><Download aria-hidden="true" />JSON</button>
        <button type="button" className="m14-btn" onClick={() => exportRows(filtered, 'csv')}><Download aria-hidden="true" />CSV</button>
        <button type="button" className="m14-btn primary" onClick={() => setAdvanced(true)}><Wrench aria-hidden="true" />Gelişmiş araçlar (içe aktarma vb.)</button>
      </PageActions>

      <StatRow stats={[
        { label: 'Toplam', value: base.length.toLocaleString('tr-TR'), onClick: () => setStatusTab('all') },
        { label: 'Tamamlandı', value: count('completed').toLocaleString('tr-TR'), tone: 'ok', onClick: () => setStatusTab('completed') },
        { label: 'Toplanıyor', value: count('gathering').toLocaleString('tr-TR'), tone: 'warn', onClick: () => setStatusTab('gathering') },
        { label: 'Çıkmış', value: base.filter((x) => x.isPastExam).length.toLocaleString('tr-TR'), tone: 'acc', onClick: () => setSourceTab('past') },
      ]} />

      <Toolbar>
        <Tabs14<StatusTab> label="Durum" value={statusTab} onChange={setStatusTab} options={[
          { id: 'all', label: 'Tümü', n: base.length },
          { id: 'completed', label: 'Tamamlandı', n: count('completed') },
          { id: 'reconstructing', label: 'Yeniden kuruluyor', n: count('reconstructing') },
          { id: 'gathering', label: 'Toplanıyor', n: count('gathering') },
          { id: 'empty', label: 'Boş', n: count('empty') },
        ]} />
        <SearchField value={q} onChange={setQ} placeholder="Soru, numara, konu veya etiket ara" label="Sorularda ara" />
        <button type="button" className={`m14-btn ${filtersOpen ? 'primary' : ''}`} aria-expanded={filtersOpen} onClick={() => setFiltersOpen((v) => !v)}>
          <SlidersHorizontal aria-hidden="true" />Süzgeçler{activeFilters > 0 ? ` (${activeFilters})` : ''}
        </button>
      </Toolbar>

      {filtersOpen && (
        <Card14 title="Süzgeçler" tools={<button type="button" className="m14-btn ghost" onClick={() => { setDiscipline(''); setTopic(''); setSourceTab('all'); setStatusTab('all'); }}>Temizle</button>}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12 }}>
            <label style={{ display: 'grid', gap: 4, minWidth: 0 }}>
              <span className="muted">Branş</span>
              <select className="pk14-sel" value={discipline} onChange={(e) => { setDiscipline(e.target.value); setTopic(''); }}>
                <option value="">Tümü</option>
                {disciplines.map((d) => <option key={d} value={d}>{d}</option>)}
              </select>
            </label>
            <label style={{ display: 'grid', gap: 4, minWidth: 0 }}>
              <span className="muted">Ders / konu</span>
              <select className="pk14-sel" value={topic} onChange={(e) => setTopic(e.target.value)}>
                <option value="">Tümü</option>
                {topics.map((d) => <option key={d} value={d}>{d}</option>)}
              </select>
            </label>
            <label style={{ display: 'grid', gap: 4, minWidth: 0 }}>
              <span className="muted">Durum</span>
              <select className="pk14-sel" value={statusTab} onChange={(e) => setStatusTab(e.target.value as StatusTab)}>
                <option value="all">Tümü</option>
                {(Object.keys(STATUS_LABEL) as Status[]).map((s) => <option key={s} value={s}>{STATUS_LABEL[s]}</option>)}
              </select>
            </label>
            <label style={{ display: 'grid', gap: 4, minWidth: 0 }}>
              <span className="muted">Kaynak</span>
              <select className="pk14-sel" value={sourceTab} onChange={(e) => setSourceTab(e.target.value as SourceTab)}>
                <option value="all">Tümü</option>
                <option value="past">Çıkmış</option>
                <option value="student">Öğrenci</option>
                <option value="other">Diğer</option>
              </select>
            </label>
          </div>
        </Card14>
      )}

      {msg && <p className="pk14-note" role="status">{msg}</p>}

      <BulkBar count={sel.count} noun="soru" actions={bulkActions} onClear={() => { sel.clear(); setBulkForm(null); }} busy={busy} />
      {bulkForm && sel.count > 0 && (
        <div className="pk14-toolbar" role="group" aria-label="Toplu işlem ayrıntısı">
          {bulkForm === 'status' ? (
            <select className="pk14-sel" value={bulkValue} onChange={(e) => setBulkValue(e.target.value)} aria-label="Yeni durum">
              {(Object.keys(STATUS_LABEL) as Status[]).map((s) => <option key={s} value={s}>{STATUS_LABEL[s]}</option>)}
            </select>
          ) : (
            <label className="pk14-search">
              <input
                value={bulkValue}
                onChange={(e) => setBulkValue(e.target.value)}
                list={bulkForm === 'move' ? 'pool14-topics' : undefined}
                placeholder={bulkForm === 'tag' ? 'Eklenecek etiket' : 'Hedef konu adı'}
                aria-label={bulkForm === 'tag' ? 'Eklenecek etiket' : 'Hedef konu adı'}
              />
              <datalist id="pool14-topics">{topics.map((t) => <option key={t} value={t} />)}</datalist>
            </label>
          )}
          <button type="button" className="m14-btn primary" disabled={busy || !bulkValue.trim()} onClick={() => void applyBulkForm()}>Uygula</button>
          <button type="button" className="m14-btn ghost" onClick={() => setBulkForm(null)}>Vazgeç</button>
        </div>
      )}

      <DataTable
        rows={pageRows}
        cols={cols}
        rowKey={(x) => x.id}
        onOpen={(x) => { setOpenId(x.id); setConfirmDel(false); }}
        selection={sel}
        activeKey={openId}
        busy={busy}
        empty="Bu süzgeçlere uyan soru yok."
      />

      <div className="pk14-toolbar" style={{ justifyContent: 'space-between' }}>
        <span className="muted">
          {filtered.length ? `${(page * PAGE + 1).toLocaleString('tr-TR')}–${Math.min(filtered.length, page * PAGE + PAGE).toLocaleString('tr-TR')} / ${filtered.length.toLocaleString('tr-TR')}` : '0 soru'}
          {filtered.length > pageRows.length && !sel.allOf(filtered.map((x) => x.id)) && (
            <> · <button type="button" className="m14-btn ghost" onClick={() => sel.toggleAll(filtered.map((x) => x.id))}>Filtreye uyan tümünü seç ({filtered.length.toLocaleString('tr-TR')})</button></>
          )}
        </span>
        <span style={{ display: 'inline-flex', gap: 8 }}>
          <button type="button" className="m14-btn" disabled={page === 0} onClick={() => setPage((p) => p - 1)}>Önceki</button>
          <button type="button" className="m14-btn" disabled={page >= pages - 1} onClick={() => setPage((p) => p + 1)}>Sonraki</button>
        </span>
      </div>

      <Drawer
        open={!!current}
        onClose={() => setOpenId(null)}
        wide
        title={current ? `Soru #${current.questionNumber}` : ''}
        head={current && <DetailNav list={filtered} current={current} same={(a, b) => a.id === b.id} onGo={(r) => { setOpenId(r.id); setConfirmDel(false); }} />}
        foot={current && (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            <button type="button" className="m14-btn primary" onClick={() => setEditing(current)}>Düzenle</button>
            {current.status !== 'completed' && (
              <button type="button" className="m14-btn" disabled={busy} onClick={() => void approveAndNext(current)}>Onayla ve sonraki</button>
            )}
            <button
              type="button"
              className="m14-btn danger"
              disabled={busy}
              onClick={() => {
                if (!confirmDel) return setConfirmDel(true);
                const nx = nextOf(current);
                setConfirmDel(false);
                setOpenId(nx ? nx.id : null);
                void del([current]);
              }}
            >
              {confirmDel ? 'Kalıcı silmeyi onayla' : 'Sil'}
            </button>
          </div>
        )}
      >
        {current && (
          <DetailLayout
            main={
              <>
                <Card14 title="Soru kökü">
                  <p style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{stemOf(current) || 'Soru kökü yok.'}</p>
                  {current.reconstruction?.oncul_maddeleri?.length ? (
                    <ul>{current.reconstruction.oncul_maddeleri.map((m, i) => <li key={i}>{m}</li>)}</ul>
                  ) : null}
                </Card14>
                <Card14 title="Şıklar">
                  <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'grid', gap: 8 }}>
                    {optionsOf(current).map((o) => {
                      const ok = o.key === answerOf(current);
                      return (
                        <li key={o.key} style={{ display: 'flex', gap: 10, alignItems: 'flex-start', padding: '8px 10px', borderRadius: 8, border: '1px solid var(--color-line)', background: ok ? 'var(--color-ok-soft)' : 'transparent' }}>
                          <b>{o.key})</b>
                          <span style={{ flex: 1, minWidth: 0, overflowWrap: 'anywhere' }}>{o.text}</span>
                          {ok && <Pill tone="ok">Doğru cevap</Pill>}
                        </li>
                      );
                    })}
                    {optionsOf(current).length === 0 && <li className="muted">Şık yok.</li>}
                  </ul>
                </Card14>
                {(current.reconstruction?.explanation || current.reconstruction?.notesAndDiscrepancies) && (
                  <Card14 title="Açıklama">
                    {current.reconstruction?.explanation && <p style={{ whiteSpace: 'pre-wrap', marginTop: 0 }}>{current.reconstruction.explanation}</p>}
                    {current.reconstruction?.notesAndDiscrepancies && <p className="muted" style={{ whiteSpace: 'pre-wrap' }}>{current.reconstruction.notesAndDiscrepancies}</p>}
                  </Card14>
                )}
              </>
            }
            side={
              <FactList items={[
                { k: 'Kimlik', v: <span className="mono" style={{ overflowWrap: 'anywhere' }}>{current.id}</span> },
                { k: 'Kurul', v: committeeName },
                { k: 'Branş', v: current.discipline || '—' },
                { k: 'Konu', v: current.topic || '—' },
                { k: 'Durum', v: <Pill tone={STATUS_TONE[current.status]}>{STATUS_LABEL[current.status] || current.status}</Pill> },
                { k: 'Kaynak', v: SOURCE_LABEL[sourceOf(current)] },
                { k: 'Doğru cevap', v: answerOf(current) || '—' },
                { k: 'Yıl / dönem', v: [current.examYear, current.term].filter(Boolean).join(' · ') || '—' },
                { k: 'Katkı veren', v: current.contributedByName || '—' },
                { k: 'Hafıza parçası', v: (current.fragments?.length || 0).toLocaleString('tr-TR') },
                { k: 'Güven puanı', v: current.reconstruction?.confidenceScore != null ? `%${current.reconstruction.confidenceScore}` : '—' },
                { k: 'Ders notu', v: current.lectureReference ? `${current.lectureReference.noteTitle} · s. ${current.lectureReference.pageNumber}` : '—' },
                { k: 'Etiketler', v: current.tags?.length ? current.tags.join(', ') : '—' },
                { k: 'Kaynak dosya', v: current.sourceFile || '—' },
              ]} />
            }
          />
        )}
      </Drawer>

      {editing && (
        <AdminEditQuestionModal
          isOpen
          onClose={() => setEditing(null)}
          question={editing}
          adminEmail={adminEmail}
          onSaveQuestion={async (updated) => {
            try {
              await ApiService.adminUpdateQuestion(adminEmail, editing.id, updated);
              setMsg(`Soru #${editing.questionNumber} güncellendi.`);
              await onRefreshData();
            } catch (e) {
              setMsg(`Kaydedilemedi: ${e instanceof Error ? e.message : String(e)}`);
            }
          }}
        />
      )}

      <Drawer open={advanced} onClose={() => setAdvanced(false)} wide title="Gelişmiş araçlar">
        <AdminPanelModal
          variant="embedded"
          tab="questions"
          isOpen
          onClose={onExit}
          adminEmail={adminEmail}
          committees={committees}
          questions={questions}
          selectedCommitteeId={selectedCommitteeId}
          onRefreshData={onRefreshData as () => Promise<void>}
        />
      </Drawer>
    </div>
  );
};

export default ManagePoolV14;
