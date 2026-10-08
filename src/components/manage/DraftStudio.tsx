import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  GitBranch,
  Columns3,
  Workflow,
  Tags,
  Plus,
  Search,
  Sparkles,
  Undo2,
  Redo2,
  Download,
  Upload,
  Trash2,
  ChevronRight,
  ChevronDown,
  GripVertical,
  X,
  Check,
  FolderPlus,
  Unlink,
  EyeOff,
  Eye,
  ArrowRight,
  ZoomIn,
  ZoomOut,
  Maximize,
  Merge,
  CircleDot,
  ListChecks,
  Bot,
  Cpu,
  Cloud,
  Loader2,
  Star,
} from 'lucide-react';
import type { QuestionItem, ReconstructedQuestion } from '../../types';
import { ApiService, StudioAiModels, StudioAiResultLite } from '../../services/api';
import {
  StudioState,
  StudioFragment,
  StudioCandidate,
  StudioGroup,
  FragKind,
  OptKey,
  OPT_KEYS,
  KIND_LABEL,
  loadStudio,
  saveStudio,
  emptyState,
  fragmentsFromDrafts,
  newCandidate,
  autoCluster,
  similarity,
  canonical,
  suggestSynonyms,
  parseOption,
  candidateToQuestionPatch,
  uid,
  fold,
} from '../../services/draftStudioService';

/**
 * Taslak stüdyosu: öğrencilerin eklediği soru parçalarını elle bir araya getirip
 * soru adaylarına eşlemek için tam kontrollü editör.
 *  - Sol: parça havuzu (ara, süz, çoklu seç, sürükle)
 *  - Orta: Ağaç (Ders › Konu › Aday › Parça) · Pano · Akış şeması · Terimler
 *  - Sağ: seçili aday / parça / grup düzenleyicisi
 * Durum cihazda kurul başına saklanır; "Soruya dönüştür" taslakları birleştirip sunucuya yazar.
 */

type View = 'tree' | 'board' | 'flow' | 'terms';
type Sel = { t: 'cand' | 'frag' | 'group'; id: string } | null;
type DragItem = { t: 'frag' | 'cand'; id: string; ids?: string[] };

const DT = 'application/x-medsoru-studio';

const KIND_STYLE: Record<FragKind, string> = {
  stem: 'bg-accent-soft text-accent',
  option: 'bg-violet-50 text-violet-700',
  clue: 'bg-warn-soft text-warn',
  answer: 'bg-ok-soft text-ok',
};

const STATUS: Record<StudioCandidate['status'], { label: string; dot: string }> = {
  open: { label: 'Açık', dot: 'bg-line-2' },
  ready: { label: 'Hazır', dot: 'bg-accent' },
  done: { label: 'Soru oldu', dot: 'bg-ok' },
};

interface Props {
  adminEmail: string;
  committeeId: string;
  committeeName?: string;
  questions: QuestionItem[];
  onRefreshData: () => Promise<void>;
  notify: (msg: string) => void;
}

export const DraftStudio: React.FC<Props> = ({ adminEmail, committeeId, committeeName, questions, onRefreshData, notify }) => {
  // ---------------------------------------------------------------- durum + geçmiş
  const [state, setStateRaw] = useState<StudioState>(() => loadStudio(committeeId));
  const past = useRef<StudioState[]>([]);
  const future = useRef<StudioState[]>([]);
  useEffect(() => {
    setStateRaw(loadStudio(committeeId));
    past.current = [];
    future.current = [];
  }, [committeeId]);
  useEffect(() => saveStudio(committeeId, state), [committeeId, state]);

  const commit = useCallback((fn: (s: StudioState) => StudioState) => {
    setStateRaw((s) => {
      const next = fn(s);
      if (next === s) return s;
      past.current = [...past.current.slice(-49), s];
      future.current = [];
      return next;
    });
  }, []);
  const undo = () =>
    setStateRaw((s) => {
      const prev = past.current.pop();
      if (!prev) return s;
      future.current.push(s);
      return prev;
    });
  const redo = () =>
    setStateRaw((s) => {
      const nxt = future.current.pop();
      if (!nxt) return s;
      past.current.push(s);
      return nxt;
    });

  // ---------------------------------------------------------------- arayüz durumu
  const [view, setView] = useState<View>(() => {
    try {
      return (localStorage.getItem('medsoru_studio_view') as View) || 'tree';
    } catch {
      return 'tree';
    }
  });
  useEffect(() => {
    try {
      localStorage.setItem('medsoru_studio_view', view);
    } catch {
      /* ignore */
    }
  }, [view]);
  const [sel, setSel] = useState<Sel>(null);
  const [q, setQ] = useState('');
  const [kindF, setKindF] = useState<FragKind | 'all'>('all');
  const [discF, setDiscF] = useState('all');
  const [onlyFree, setOnlyFree] = useState(true);
  const [showHidden, setShowHidden] = useState(false);
  const [picked, setPicked] = useState<string[]>([]);
  const [dragging, setDragging] = useState<DragItem | null>(null);
  const [overZone, setOverZone] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [inspectorOpen, setInspectorOpen] = useState(false);
  const [poolOpen, setPoolOpen] = useState(true);
  const importRef = useRef<HTMLInputElement>(null);
  const [openCands, setOpenCands] = useState<Set<string>>(new Set());
  const [editingGroup, setEditingGroup] = useState<string | null>(null);
  const [termDraft, setTermDraft] = useState('');
  const [mergeFrom, setMergeFrom] = useState<string | null>(null);
  // AI ile dönüştür
  const [aiFor, setAiFor] = useState<string | null>(null);
  const [aiModels, setAiModels] = useState<StudioAiModels | null>(null);
  const [aiTargets, setAiTargets] = useState<string[]>([]);
  const [aiResults, setAiResults] = useState<Record<string, StudioAiResultLite | 'loading'>>({});
  const [aiPick, setAiPick] = useState<string[]>([]);
  const [aiPrimary, setAiPrimary] = useState<string | null>(null);
  const [aiSaving, setAiSaving] = useState(false);

  // ---------------------------------------------------------------- türetilmiş veri
  const drafts = useMemo(
    () =>
      questions.filter(
        (x) =>
          (!committeeId || x.committeeId === committeeId) &&
          x.status !== 'completed' &&
          ((x.fragments || []).some((f) => f?.text?.trim()) || (x.options || []).some((o) => o?.text?.trim()))
      ),
    [questions, committeeId]
  );
  const allFrags = useMemo(() => fragmentsFromDrafts(drafts), [drafts]);
  const fragById = useMemo(() => new Map(allFrags.map((f) => [f.id, f])), [allFrags]);
  const hidden = useMemo(() => new Set(state.hiddenFragmentIds), [state.hiddenFragmentIds]);
  const ownerOf = useMemo(() => {
    const m = new Map<string, string>();
    state.candidates.forEach((c) => c.fragmentIds.forEach((id) => m.set(id, c.id)));
    return m;
  }, [state.candidates]);
  const candById = useMemo(() => new Map(state.candidates.map((c) => [c.id, c])), [state.candidates]);
  const groupById = useMemo(() => new Map(state.groups.map((g) => [g.id, g])), [state.groups]);
  const disciplines = useMemo(() => [...new Set(allFrags.map((f) => f.discipline))].sort((a, b) => a.localeCompare(b, 'tr')), [allFrags]);

  const fq = fold(q.trim());
  const pool = useMemo(
    () =>
      allFrags.filter(
        (f) =>
          (showHidden || !hidden.has(f.id)) &&
          (!onlyFree || !ownerOf.has(f.id)) &&
          (kindF === 'all' || f.kind === kindF) &&
          (discF === 'all' || f.discipline === discF) &&
          (!fq || fold(f.text).includes(fq) || f.terms.some((t) => fold(canonical(t, state.synonyms)) === fq))
      ),
    [allFrags, showHidden, hidden, onlyFree, ownerOf, kindF, discF, fq, state.synonyms]
  );

  const termIndex = useMemo(() => {
    const m = new Map<string, { count: number; frags: Set<string>; forms: Set<string> }>();
    allFrags.forEach((f) =>
      f.terms.forEach((t) => {
        const c = canonical(t, state.synonyms);
        const e = m.get(c) || { count: 0, frags: new Set<string>(), forms: new Set<string>() };
        e.count++;
        e.frags.add(f.id);
        e.forms.add(t);
        m.set(c, e);
      })
    );
    return [...m.entries()].sort((a, b) => b[1].count - a[1].count);
  }, [allFrags, state.synonyms]);

  const stats = {
    frags: allFrags.length,
    free: allFrags.filter((f) => !ownerOf.has(f.id) && !hidden.has(f.id)).length,
    cands: state.candidates.length,
    ready: state.candidates.filter((c) => c.status === 'ready').length,
    done: state.candidates.filter((c) => c.status === 'done').length,
  };

  // ---------------------------------------------------------------- işlemler
  const termsOf = (ids: string[]) => {
    const count = new Map<string, number>();
    ids.forEach((id) => fragById.get(id)?.terms.forEach((t) => {
      const c = canonical(t, state.synonyms);
      count.set(c, (count.get(c) || 0) + 1);
    }));
    return [...count.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([t]) => t);
  };

  /** Parçaları adaya yerleştirir: kök boşsa kökle doldurur, şıkları boş yuvaya koyar. */
  const placeInto = (c: StudioCandidate, ids: string[]): StudioCandidate => {
    const next = { ...c, options: { ...c.options }, optionSources: { ...c.optionSources }, fragmentIds: [...c.fragmentIds] };
    ids.forEach((id) => {
      const f = fragById.get(id);
      if (!f || next.fragmentIds.includes(id)) return;
      next.fragmentIds.push(id);
      if (f.kind === 'stem' && !next.stem.trim()) next.stem = f.text;
      if (f.kind === 'option') {
        const p = parseOption(f.text);
        const slot = p.key && !next.options[p.key].trim() ? p.key : OPT_KEYS.find((k) => !next.options[k].trim());
        if (slot) {
          next.options[slot] = p.text;
          next.optionSources[slot] = id;
        }
      }
      if (f.kind === 'answer' && !next.answer) {
        const m = f.text.match(/\b([A-E])\b/i);
        if (m) next.answer = m[1].toUpperCase() as OptKey;
      }
      if (!next.questionNumber && f.questionNumber) next.questionNumber = f.questionNumber;
    });
    next.terms = [...new Set([...next.terms, ...termsOf(next.fragmentIds)])].slice(0, 12);
    if (!next.title.trim()) next.title = (next.stem || fragById.get(ids[0])?.text || 'Yeni aday').slice(0, 70);
    next.updatedAt = new Date().toISOString();
    return next;
  };

  const detachFrom = (s: StudioState, ids: string[], exceptCand?: string): StudioState => ({
    ...s,
    candidates: s.candidates.map((c) => {
      if (c.id === exceptCand || !c.fragmentIds.some((id) => ids.includes(id))) return c;
      const optionSources = { ...c.optionSources };
      const options = { ...c.options };
      OPT_KEYS.forEach((k) => {
        if (optionSources[k] && ids.includes(optionSources[k]!)) {
          options[k] = '';
          delete optionSources[k];
        }
      });
      return { ...c, fragmentIds: c.fragmentIds.filter((id) => !ids.includes(id)), options, optionSources, updatedAt: new Date().toISOString() };
    }),
  });

  const attach = (ids: string[], candId: string) =>
    commit((s) => {
      const s2 = detachFrom(s, ids, candId);
      return { ...s2, candidates: s2.candidates.map((c) => (c.id === candId ? placeInto(c, ids) : c)) };
    });

  const createCandidate = (ids: string[] = [], groupId: string | null = null) => {
    const c0 = newCandidate({ groupId });
    const c = ids.length ? placeInto(c0, ids) : { ...c0, title: 'Yeni aday' };
    commit((s) => {
      const s2 = detachFrom(s, ids);
      return { ...s2, candidates: [c, ...s2.candidates] };
    });
    setSel({ t: 'cand', id: c.id });
    setPicked([]);
    setInspectorOpen(true);
    return c.id;
  };

  const updateCand = (id: string, patch: Partial<StudioCandidate>) =>
    commit((s) => ({ ...s, candidates: s.candidates.map((c) => (c.id === id ? { ...c, ...patch, updatedAt: new Date().toISOString() } : c)) }));

  const deleteCand = (id: string) => {
    commit((s) => ({ ...s, candidates: s.candidates.filter((c) => c.id !== id) }));
    if (sel?.id === id) setSel(null);
  };

  const moveCand = (candId: string, groupId: string | null) => updateCand(candId, { groupId });

  const createGroup = (parentId: string | null = null, discipline = '') => {
    const parent = parentId ? groupById.get(parentId) : null;
    const g: StudioGroup = { id: uid('gr'), label: parent ? 'Alt konu' : discipline || 'Yeni konu', discipline: parent?.discipline || discipline, parentId };
    commit((s) => ({ ...s, groups: [...s.groups, g] }));
    setSel({ t: 'group', id: g.id });
    setInspectorOpen(true);
  };

  const updateGroup = (id: string, patch: Partial<StudioGroup>) =>
    commit((s) => ({ ...s, groups: s.groups.map((g) => (g.id === id ? { ...g, ...patch } : g)) }));

  const deleteGroup = (id: string) => {
    const g = groupById.get(id);
    commit((s) => ({
      ...s,
      groups: s.groups.filter((x) => x.id !== id).map((x) => (x.parentId === id ? { ...x, parentId: g?.parentId ?? null } : x)),
      candidates: s.candidates.map((c) => (c.groupId === id ? { ...c, groupId: g?.parentId ?? null } : c)),
    }));
    if (sel?.id === id) setSel(null);
  };

  const isDescendant = (gid: string, ofId: string): boolean => {
    let cur = groupById.get(gid);
    while (cur) {
      if (cur.parentId === ofId) return true;
      cur = cur.parentId ? groupById.get(cur.parentId) : undefined;
    }
    return false;
  };

  const toggleHide = (ids: string[]) =>
    commit((s) => {
      const h = new Set(s.hiddenFragmentIds);
      const allHidden = ids.every((id) => h.has(id));
      ids.forEach((id) => (allHidden ? h.delete(id) : h.add(id)));
      return { ...s, hiddenFragmentIds: [...h] };
    });

  /** Eşlenmemiş parçaları benzerliğe göre kümeleyip her ders için bir konu altında aday açar. */
  const autoGroup = () => {
    const free = allFrags.filter((f) => !ownerOf.has(f.id) && !hidden.has(f.id));
    const clusters = autoCluster(free, state.synonyms);
    if (!clusters.length) {
      notify('Gruplanacak benzer parça bulunamadı.');
      return;
    }
    commit((s) => {
      const groups = [...s.groups];
      const findOrMake = (disc: string) => {
        let g = groups.find((x) => x.parentId === null && x.discipline === disc);
        if (!g) {
          g = { id: uid('gr'), label: disc, discipline: disc, parentId: null };
          groups.push(g);
        }
        return g.id;
      };
      const made = clusters.map((cl) => placeInto(newCandidate({ groupId: findOrMake(cl[0].discipline) }), cl.map((f) => f.id)));
      return { ...s, groups, candidates: [...made, ...s.candidates] };
    });
    notify(`${clusters.length} aday önerildi. Gözden geçirip düzenleyebilirsin; Geri al ile tamamı geri döner.`);
  };

  const mergeTerms = (from: string, into: string) =>
    commit((s) => {
      if (from === into) return s;
      const syn = { ...s.synonyms };
      const fromSet = [from, ...(syn[from] || [])];
      delete syn[from];
      Object.keys(syn).forEach((k) => (syn[k] = syn[k].filter((t) => !fromSet.includes(t))));
      syn[into] = [...new Set([...(syn[into] || []), ...fromSet])].filter((t) => t !== into);
      return { ...s, synonyms: syn };
    });
  const splitTerm = (head: string) =>
    commit((s) => {
      const syn = { ...s.synonyms };
      delete syn[head];
      return { ...s, synonyms: syn };
    });

  const groupPath = (gid: string | null): string => {
    const parts: string[] = [];
    let cur = gid ? groupById.get(gid) : undefined;
    while (cur) {
      parts.unshift(cur.label);
      cur = cur.parentId ? groupById.get(cur.parentId) : undefined;
    }
    return parts.join(' › ');
  };

  /** Adayı gerçek soruya dönüştürür: parçaların taslaklarını birleştirir, alanları yazar. */
  const convert = (c: StudioCandidate) => convertWith(c);
  const convertWith = async (c: StudioCandidate, extra: Partial<QuestionItem> = {}, quiet = false): Promise<string | null> => {
    if (!c.fragmentIds.length) {
      notify('Önce adaya en az bir parça ekle.');
      return null;
    }
    const draftIds = [...new Set(c.fragmentIds.map((id) => fragById.get(id)?.draftId).filter(Boolean) as string[])];
    const stemFrag = c.fragmentIds.map((id) => fragById.get(id)).find((f) => f?.kind === 'stem');
    const anchor = stemFrag?.draftId || draftIds[0];
    const others = draftIds.filter((d) => d !== anchor);
    const g = c.groupId ? groupById.get(c.groupId) : undefined;
    const discipline = g?.discipline || fragById.get(c.fragmentIds[0])?.discipline || 'Belirsiz';
    setBusy(c.id);
    try {
      if (others.length) await ApiService.mergeDraftCluster(adminEmail, anchor, others, 'Taslak stüdyosu');
      await ApiService.adminUpdateQuestion(adminEmail, anchor, { ...candidateToQuestionPatch(c, discipline, groupPath(c.groupId)), ...extra });
      updateCand(c.id, { status: 'done', convertedQuestionId: anchor });
      if (!quiet) {
        notify(others.length ? `${draftIds.length} taslak tek soruda birleşti ve kaydedildi.` : 'Soru kaydedildi.');
        await onRefreshData();
      }
      return anchor;
    } catch (e: any) {
      notify('Dönüştürülemedi: ' + (e?.message || 'bilinmeyen hata'));
      return null;
    } finally {
      setBusy(null);
    }
  };

  // ---------------------------------------------------------------- Grubu birleştirip AI ile dönüştür
  // Tek aday dönüştürülünce AI gruptaki diğer parçaları görmüyordu. Bu işlem konudaki (alt konular
  // dahil) tüm açık adayların köklerini, şıklarını ve parçalarını tek adayda toplar, sonra AI'ya verir.
  // Geri al (Ctrl+Z) ile birleştirme öncesine dönülebilir.
  const mergeGroupForAi = (gid: string) => {
    const descend = (id: string): string[] => [id, ...state.groups.filter((x) => x.parentId === id).flatMap((x) => descend(x.id))];
    const gids = new Set(descend(gid));
    const members = state.candidates.filter((c) => c.groupId && gids.has(c.groupId) && c.status !== 'done');
    if (members.length === 0) {
      notify('Bu konuda dönüştürülecek açık aday yok.');
      return;
    }
    if (members.length === 1) {
      void openAi(members[0]);
      return;
    }
    const g = groupById.get(gid);
    const fragmentIds = Array.from(new Set(members.flatMap((c) => c.fragmentIds)));
    const stems = Array.from(new Set(members.map((c) => c.stem.trim()).filter(Boolean)));
    const options = { A: '', B: '', C: '', D: '', E: '' } as StudioCandidate['options'];
    const extraOptions: string[] = [];
    members.forEach((c) =>
      OPT_KEYS.forEach((k) => {
        const t = (c.options[k] || '').trim();
        if (!t) return;
        if (!options[k]) options[k] = t;
        else if (options[k] !== t) extraOptions.push(`${k}) ${t}`);
      })
    );
    const answerVotes: Record<string, number> = {};
    members.forEach((c) => c.answer && (answerVotes[c.answer] = (answerVotes[c.answer] || 0) + 1));
    const answer = (Object.entries(answerVotes).sort((a, b) => b[1] - a[1])[0]?.[0] as StudioCandidate['answer']) || undefined;
    const notes = [
      stems.length > 1 ? `Diğer kök adayları:\n${stems.slice(1).map((x) => `- ${x}`).join('\n')}` : '',
      extraOptions.length ? `Farklı yazılmış şıklar:\n${extraOptions.map((x) => `- ${x}`).join('\n')}` : '',
      ...members.map((c) => c.notes.trim()).filter(Boolean),
    ].filter(Boolean).join('\n\n');
    const merged = newCandidate({
      groupId: gid,
      title: `Birleşik · ${g?.label || 'grup'}`,
      stem: stems[0] || '',
      options,
      answer,
      fragmentIds,
      optionSources: Object.assign({}, ...members.map((c) => c.optionSources)),
      terms: Array.from(new Set(members.flatMap((c) => c.terms))),
      notes,
      questionNumber: members.find((c) => c.questionNumber)?.questionNumber,
    });
    const memberIds = new Set(members.map((c) => c.id));
    commit((st) => ({ ...st, candidates: [merged, ...st.candidates.filter((c) => !memberIds.has(c.id))] }));
    setSel({ t: 'cand', id: merged.id });
    notify(`${members.length} aday tek adayda birleştirildi; AI tüm parçaları birlikte görecek. Geri al ile ayırabilirsin.`);
    void openAi(merged);
  };

  // ---------------------------------------------------------------- AI ile dönüştür
  const openAi = async (c: StudioCandidate) => {
    setAiFor(c.id);
    setAiResults({});
    setAiPick([]);
    setAiPrimary(null);
    const m = aiModels || (await ApiService.getStudioAiModels(adminEmail));
    if (m) {
      setAiModels(m);
      setAiTargets((prev) => (prev.length ? prev : ['cloud', ...m.local.filter((x) => x.available).map((x) => x.target)]));
    } else setAiTargets(['cloud']);
  };

  const aiInputOf = (c: StudioCandidate) => {
    const g = c.groupId ? groupById.get(c.groupId) : undefined;
    return {
      committeeId,
      discipline: g?.discipline || fragById.get(c.fragmentIds[0])?.discipline,
      topic: groupPath(c.groupId) || c.title,
      stem: c.stem,
      options: c.options,
      answer: c.answer,
      fragments: c.fragmentIds.map((id) => fragById.get(id)).filter((f): f is StudioFragment => !!f).map((f) => ({ kind: KIND_LABEL[f.kind], text: f.text })),
      terms: c.terms,
      notes: c.notes,
    };
  };

  const runAi = (c: StudioCandidate) => {
    if (!c.fragmentIds.length && !c.stem.trim()) {
      notify('AI için önce adaya parça ekle ya da kök yaz.');
      return;
    }
    const input = aiInputOf(c);
    const targets = aiTargets.length ? aiTargets : ['cloud'];
    setAiResults(Object.fromEntries(targets.map((t) => [t, 'loading' as const])));
    setAiPick([]);
    setAiPrimary(null);
    // Hepsi aynı anda istenir; sunucu yerel modelleri sıraya koyar, sonuçlar geldikçe görünür
    targets.forEach((t) =>
      ApiService.studioAiGenerate(adminEmail, t, input).then((r) => {
        setAiResults((prev) => ({ ...prev, [t]: r }));
        if (r.ok) {
          setAiPick((p) => (t === 'cloud' && !p.includes(t) ? [t, ...p] : p));
          setAiPrimary((p) => p ?? (t === 'cloud' ? t : p));
        }
      })
    );
  };

  const reconOf = (r: StudioAiResultLite): ReconstructedQuestion => ({
    stem: r.question!.stem,
    options: r.question!.options.map((o) => ({ ...o, isAiFilled: true, isCorrect: o.key === r.question!.correctAnswer })),
    correctAnswer: r.question!.correctAnswer,
    explanation: r.question!.explanation,
    confidenceScore: r.question!.confidence,
    lastUpdated: new Date().toISOString(),
    isAiRefined: true,
    notesAndDiscrepancies: `Taslak stüdyosunda üretildi · ${r.label}`,
    sources: r.sources as ReconstructedQuestion['sources'],
  });

  const saveAi = async (c: StudioCandidate) => {
    const picks = aiPick.filter((t) => {
      const r = aiResults[t];
      return r && r !== 'loading' && r.ok;
    });
    if (!picks.length) {
      notify('Kaydetmek için en az bir sonucu işaretle.');
      return;
    }
    const primary = aiPrimary && picks.includes(aiPrimary) ? aiPrimary : picks[0];
    const g = c.groupId ? groupById.get(c.groupId) : undefined;
    const discipline = g?.discipline || fragById.get(c.fragmentIds[0])?.discipline || 'Belirsiz';
    setAiSaving(true);
    let saved = 0;
    try {
      const pr = aiResults[primary] as StudioAiResultLite;
      const anchor = await convertWith(
        c,
        {
          reconstruction: reconOf(pr),
          rawStem: pr.question!.stem,
          options: pr.question!.options.map((o) => ({ key: o.key, text: o.text, upvotes: 0, isAiGenerated: true })),
          claimedAnswer: pr.question!.correctAnswer,
          status: 'reconstructing',
        },
        true
      );
      if (anchor) saved++;
      for (const t of picks.filter((x) => x !== primary)) {
        const r = aiResults[t] as StudioAiResultLite;
        const q: QuestionItem = {
          id: uid('alt'),
          committeeId,
          questionNumber: c.questionNumber || 0,
          isUnassignedNumber: !c.questionNumber,
          discipline,
          topic: groupPath(c.groupId) || c.title || discipline,
          status: 'reconstructing',
          fragments: [],
          options: r.question!.options.map((o) => ({ key: o.key, text: o.text, upvotes: 0, isAiGenerated: true })),
          claimedAnswer: r.question!.correctAnswer,
          rawStem: r.question!.stem,
          reconstruction: reconOf(r),
          tags: [...c.terms, 'ai-alternatif', `model:${t}`],
          placementNotes: `Alternatif · ${r.label} · kaynak aday: ${c.title}${anchor ? ` · ana soru ${anchor}` : ''}`,
          contributedByName: 'Taslak stüdyosu',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        await ApiService.adminCreateQuestion(adminEmail, q);
        saved++;
      }
      notify(`${saved} soru kaydedildi (ana: ${(aiResults[primary] as StudioAiResultLite).label}). Hepsi “inceleniyor” durumunda.`);
      setAiFor(null);
      await onRefreshData();
    } catch (e: any) {
      notify('Kaydedilemedi: ' + (e?.message || 'bilinmeyen hata'));
    } finally {
      setAiSaving(false);
    }
  };

  const AiPanel = ({ c }: { c: StudioCandidate }) => {
    const targets: { target: string; label: string; available: boolean; local: boolean }[] = [
      { target: 'cloud', label: aiModels?.cloud.label || 'Bulut AI (Gemini → Groq)', available: true, local: false },
      ...(aiModels?.local || []).map((m) => ({ ...m, local: true })),
    ];
    const results = Object.entries(aiResults);
    const loadingCount = results.filter(([, r]) => r === 'loading').length;
    const okCount = results.filter(([, r]) => r !== 'loading' && r.ok).length;
    return (
      <div className="ms-overlay fixed inset-0 z-[70] bg-[rgba(14,26,38,0.45)] flex items-center justify-center p-3" onMouseDown={(e) => e.target === e.currentTarget && !aiSaving && setAiFor(null)}>
        <div role="dialog" aria-modal="true" aria-label="AI ile dönüştür" className="ms-modal-panel bg-white rounded-2xl shadow-xl w-full max-w-[1180px] max-h-[92dvh] flex flex-col overflow-hidden">
          <div className="flex items-center gap-3 px-5 py-3.5 border-b border-line">
            <Bot className="w-5 h-5 text-accent" />
            <div className="flex-1 min-w-0">
              <b className="text-[15px]">AI ile dönüştür</b>
              <div className="text-[12.5px] text-ink-3 truncate">{c.title || 'Adsız aday'} · {c.fragmentIds.length} parça · kaynaklara dayalı</div>
            </div>
            <button type="button" aria-label="Kapat" onClick={() => !aiSaving && setAiFor(null)} className="ms-btn is-ghost is-icon"><X className="w-4 h-4" /></button>
          </div>
          <div className="flex-1 min-h-0 overflow-y-auto overscroll-contain p-4 flex flex-col gap-4">
            <section className="flex flex-col gap-2">
              <span className={label}>Modeller · birden çok seçilebilir</span>
              <div className="flex flex-wrap gap-2">
                {targets.map((m) => {
                  const on = aiTargets.includes(m.target);
                  return (
                    <button
                      key={m.target}
                      type="button"
                      disabled={!m.available}
                      onClick={() => setAiTargets((p) => (on ? p.filter((x) => x !== m.target) : [...p, m.target]))}
                      aria-pressed={on}
                      title={m.available ? '' : 'Ollama’da bu model yüklü değil'}
                      className={`h-9 px-3 rounded-full text-[13px] inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed ${on ? 'bg-ink text-white font-semibold' : 'bg-field text-ink-2'}`}
                    >
                      {m.local ? <Cpu className="w-4 h-4" /> : <Cloud className="w-4 h-4" />}
                      {m.label}
                      {on && <Check className="w-3.5 h-3.5" />}
                    </button>
                  );
                })}
              </div>
              <span className="text-[12px] text-ink-3">
                {aiModels?.embed?.available ? `${aiModels.embed.model}: kaynakları anlam benzerliğine göre sıralar (gömme modeli, soru yazmaz). ` : ''}
                {aiModels && !aiModels.ollamaReachable ? 'Ollama’ya ulaşılamadı; yalnız bulut çalışır. ' : ''}
                Yerel modeller sırayla çalışır; ilk sonuç bulut ya da ilk biten modelden gelir.
              </span>
              <div className="flex items-center gap-2">
                <button type="button" onClick={() => runAi(c)} disabled={loadingCount > 0} className="ms-btn is-primary">
                  {loadingCount > 0 ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                  {loadingCount > 0 ? `${loadingCount} model çalışıyor…` : results.length ? 'Yeniden üret' : 'Soruları üret'}
                </button>
                {results.length > 0 && <span className="text-[12.5px] text-ink-3">{okCount} sonuç hazır</span>}
              </div>
            </section>

            {results.length > 0 && (
              <section className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                {results.map(([t, r]) => {
                  const picked = aiPick.includes(t);
                  if (r === 'loading')
                    return (
                      <div key={t} className="rounded-2xl bg-field p-4 flex items-center gap-3 text-[13px] text-ink-2 min-h-[120px]">
                        <Loader2 className="w-5 h-5 animate-spin text-accent" />
                        <span><b className="text-ink">{t === 'cloud' ? 'Bulut AI' : t}</b> soru yazıyor…</span>
                      </div>
                    );
                  if (!r.ok)
                    return (
                      <div key={t} className="ms-pop-in rounded-2xl bg-bad-soft p-4 text-[13px] flex flex-col gap-1">
                        <b className="text-bad-text">{r.label} · başarısız</b>
                        <span className="text-ink-2">{r.error}</span>
                        <button type="button" onClick={() => { setAiResults((p) => ({ ...p, [t]: 'loading' })); ApiService.studioAiGenerate(adminEmail, t, aiInputOf(c)).then((x) => setAiResults((p) => ({ ...p, [t]: x }))); }} className="self-start h-8 px-3 rounded-full bg-white text-[12.5px] font-semibold cursor-pointer mt-1">Tekrar dene</button>
                      </div>
                    );
                  const q = r.question!;
                  return (
                    <article key={t} className={`ms-pop-in rounded-2xl p-4 flex flex-col gap-2.5 border-2 transition-colors ${picked ? 'border-accent bg-accent-soft/30' : 'border-line bg-white'}`}>
                      <div className="flex items-center gap-2">
                        <label className="inline-flex items-center gap-2 cursor-pointer flex-1 min-w-0">
                          <input type="checkbox" checked={picked} onChange={() => setAiPick((p) => (picked ? p.filter((x) => x !== t) : [...p, t]))} className="w-4 h-4 accent-[var(--color-accent)]" />
                          <span className="text-[13px] font-semibold truncate">{r.label}</span>
                        </label>
                        <span className="text-[11.5px] text-ink-3 font-mono">%{q.confidence} · {(r.ms / 1000).toFixed(1)} sn</span>
                        <button
                          type="button"
                          onClick={() => {
                            setAiPrimary(t);
                            setAiPick((p) => (p.includes(t) ? p : [...p, t]));
                          }}
                          title="Ana soru: adayın taslağına yazılır; diğer seçilenler alternatif olarak ayrı kaydedilir"
                          className={`h-7 px-2.5 rounded-full text-[12px] inline-flex items-center gap-1 cursor-pointer ${aiPrimary === t ? 'bg-warn-soft text-warn font-semibold' : 'bg-field text-ink-3 hover:text-ink'}`}
                        >
                          <Star className="w-3.5 h-3.5" /> {aiPrimary === t ? 'Ana soru' : 'Ana yap'}
                        </button>
                      </div>
                      {(() => {
                        // Editörde iddia edilen cevap varsa ve model başka bir seçeneği doğru saydıysa uyar
                        const claimed = c.answer ? fold(c.options[c.answer] || '').trim() : '';
                        const modelText = fold(q.options.find((o) => o.key === q.correctAnswer)?.text || '');
                        return claimed && modelText && !modelText.includes(claimed) && !claimed.includes(modelText) ? (
                          <span className="self-start text-[12px] font-semibold px-2 py-0.5 rounded-full bg-warn-soft text-warn">
                            Cevabı editördekiyle çelişiyor ({c.answer}: {c.options[c.answer!]})
                          </span>
                        ) : null;
                      })()}
                      <p className="m-0 text-[14px] leading-relaxed text-ink font-medium">{q.stem}</p>
                      <ol className="list-none m-0 p-0 flex flex-col gap-1">
                        {q.options.map((o) => (
                          <li key={o.key} className={`flex gap-2 px-2.5 py-1.5 rounded-lg text-[13px] ${o.key === q.correctAnswer ? 'bg-ok-soft text-ok font-semibold' : 'bg-field text-ink-2'}`}>
                            <b className="font-mono">{o.key}</b>
                            <span>{o.text}</span>
                          </li>
                        ))}
                      </ol>
                      {q.explanation && <p className="m-0 text-[12.5px] text-ink-2 leading-relaxed line-clamp-5" title={q.explanation}>{q.explanation}</p>}
                      {r.sources.length > 0 && (
                        <div className="flex flex-wrap gap-1">
                          {r.sources.map((src, i) => (
                            <span key={i} className="text-[11.5px] px-2 py-0.5 rounded-full bg-field text-ink-3 truncate max-w-[260px]" title={src.snippet}>
                              {src.title}{src.pageNumber ? ` · s.${src.pageNumber}` : ''}
                            </span>
                          ))}
                          {r.reranked && <span className="text-[11px] text-ink-3">· bge-m3 ile sıralandı</span>}
                        </div>
                      )}
                      <button
                        type="button"
                        onClick={() => {
                          updateCand(c.id, {
                            stem: q.stem,
                            options: Object.fromEntries(OPT_KEYS.map((k) => [k, q.options.find((o) => o.key === k)?.text || ''])) as StudioCandidate['options'],
                            answer: q.correctAnswer,
                          });
                          notify('Sonuç editöre aktarıldı; dilediğin gibi düzenleyebilirsin.');
                        }}
                        className="self-start h-8 px-3 rounded-full text-accent hover:bg-accent-soft text-[12.5px] font-semibold cursor-pointer"
                      >
                        Editöre aktar
                      </button>
                    </article>
                  );
                })}
              </section>
            )}
          </div>
          <div className="flex flex-wrap items-center gap-2 px-5 py-3 border-t border-line">
            <span className="text-[12.5px] text-ink-3 flex-1 min-w-[200px]">
              {aiPick.length ? `${aiPick.length} seçili · ana soru adayın taslağına yazılır, diğerleri alternatif olarak ayrı kaydedilir.` : 'Kaydetmek için sonuçları işaretle; birden çok seçebilirsin.'}
            </span>
            <button type="button" onClick={() => setAiFor(null)} disabled={aiSaving} className="ms-btn">Kapat</button>
            <button type="button" onClick={() => void saveAi(c)} disabled={aiSaving || aiPick.length === 0} className="ms-btn is-primary">
              {aiSaving && <Loader2 className="w-4 h-4 animate-spin" />}
              Seçilenleri kaydet{aiPick.length ? ` (${aiPick.length})` : ''}
            </button>
          </div>
        </div>
      </div>
    );
  };

  const exportJson = () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `taslak-studyosu-${committeeId || 'genel'}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  };
  const importJson = async (file: File) => {
    try {
      const s = JSON.parse(await file.text());
      if (s?.v !== 1 || !Array.isArray(s.candidates)) throw new Error('Biçim tanınmadı');
      commit(() => ({ ...emptyState(), ...s }));
      notify('Stüdyo içe aktarıldı.');
    } catch (e: any) {
      notify('İçe aktarılamadı: ' + (e?.message || ''));
    }
  };

  // Klavye: Ctrl+Z / Ctrl+Shift+Z, Delete, Esc
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      const typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z' && !typing) {
        e.preventDefault();
        e.shiftKey ? redo() : undo();
      } else if (e.key === 'Escape') {
        setSel(null);
        setPicked([]);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  // ---------------------------------------------------------------- sürükle bırak
  const dragProps = (item: DragItem) => ({
    draggable: true,
    onDragStart: (e: React.DragEvent) => {
      const it = item.t === 'frag' && picked.includes(item.id) && picked.length > 1 ? { ...item, ids: picked } : item;
      e.dataTransfer.setData(DT, JSON.stringify(it));
      e.dataTransfer.effectAllowed = 'move';
      setDragging(it);
    },
    onDragEnd: () => {
      setDragging(null);
      setOverZone(null);
    },
  });
  const dropProps = (zone: string, accept: DragItem['t'][], onDrop: (it: DragItem) => void) => ({
    onDragOver: (e: React.DragEvent) => {
      if (dragging && accept.includes(dragging.t)) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        if (overZone !== zone) setOverZone(zone);
      }
    },
    onDragLeave: (e: React.DragEvent) => {
      if (!(e.currentTarget as HTMLElement).contains(e.relatedTarget as Node)) setOverZone((z) => (z === zone ? null : z));
    },
    onDrop: (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      try {
        const it = JSON.parse(e.dataTransfer.getData(DT)) as DragItem;
        if (accept.includes(it.t)) onDrop(it);
      } catch {
        /* ignore */
      }
      setDragging(null);
      setOverZone(null);
    },
  });
  const zoneCls = (zone: string, accept: DragItem['t'][]) =>
    dragging && accept.includes(dragging.t)
      ? overZone === zone
        ? 'ring-2 ring-accent bg-accent-soft/60'
        : 'ring-1 ring-dashed ring-accent/40'
      : '';
  const fragIds = (it: DragItem) => (it.ids && it.ids.length ? it.ids : [it.id]);

  // ---------------------------------------------------------------- küçük parçalar
  const FragChip = ({ f, compact, inCand }: { f: StudioFragment; compact?: boolean; inCand?: string }) => {
    const on = sel?.t === 'frag' && sel.id === f.id;
    const isPicked = picked.includes(f.id);
    return (
      <div
        {...dragProps({ t: 'frag', id: f.id })}
        onClick={(e) => {
          e.stopPropagation();
          if (e.shiftKey || e.metaKey || e.ctrlKey) setPicked((p) => (p.includes(f.id) ? p.filter((x) => x !== f.id) : [...p, f.id]));
          else {
            setSel({ t: 'frag', id: f.id });
            setInspectorOpen(true);
          }
        }}
        className={`group/frag relative flex items-start gap-2 rounded-xl border bg-white px-2.5 py-2 text-[13px] leading-snug cursor-grab active:cursor-grabbing select-none transition-colors ${
          on ? 'border-accent ring-2 ring-accent-soft' : isPicked ? 'border-accent bg-accent-soft/40' : 'border-line hover:border-line-2'
        } ${hidden.has(f.id) ? 'opacity-50' : ''}`}
        title="Sürükle: adaya bırak · Shift/Ctrl+tık: çoklu seç"
      >
        <GripVertical className="w-3.5 h-3.5 mt-0.5 text-ink-3 shrink-0 opacity-0 group-hover/frag:opacity-100" aria-hidden="true" />
        <span className="flex-1 min-w-0">
          <span className="flex items-center gap-1.5 mb-0.5">
            <span className={`text-[11px] font-semibold px-1.5 rounded-md ${KIND_STYLE[f.kind]}`}>{KIND_LABEL[f.kind]}</span>
            {!compact && <span className="text-[11.5px] text-ink-3 truncate">{f.discipline}{f.questionNumber ? ` · No ${f.questionNumber}` : ''}</span>}
          </span>
          <span className={compact ? 'line-clamp-2 text-ink-2' : 'line-clamp-3 text-ink'}>{f.text}</span>
        </span>
        {inCand && (
          <button
            type="button"
            aria-label="Adaydan çıkar"
            title="Adaydan çıkar"
            onClick={(e) => {
              e.stopPropagation();
              commit((s) => detachFrom(s, [f.id]));
            }}
            className="w-6 h-6 -mr-1 rounded-md flex items-center justify-center text-ink-3 hover:text-bad-text hover:bg-bad-soft opacity-0 group-hover/frag:opacity-100 shrink-0"
          >
            <Unlink className="w-3.5 h-3.5" />
          </button>
        )}
      </div>
    );
  };

  const optCount = (c: StudioCandidate) => OPT_KEYS.filter((k) => c.options[k].trim()).length;

  // ---------------------------------------------------------------- AĞAÇ görünümü
  const CandRow = ({ c, depth }: { c: StudioCandidate; depth: number }) => {
    const open = openCands.has(c.id);
    const setOpen = (fn: (v: boolean) => boolean) =>
      setOpenCands((prev) => {
        const n = new Set(prev);
        fn(prev.has(c.id)) ? n.add(c.id) : n.delete(c.id);
        return n;
      });
    const zone = `cand-${c.id}`;
    const on = sel?.t === 'cand' && sel.id === c.id;
    return (
      <li className="relative">
        <div
          {...dragProps({ t: 'cand', id: c.id })}
          {...dropProps(zone, ['frag'], (it) => attach(fragIds(it), c.id))}
          onClick={() => {
            setSel({ t: 'cand', id: c.id });
            setInspectorOpen(true);
          }}
          style={{ marginLeft: depth * 20 }}
          className={`flex items-center gap-2 min-h-11 pl-1 pr-2 py-1.5 rounded-xl cursor-pointer transition-colors ${
            on ? 'bg-accent-soft' : 'hover:bg-field'
          } ${zoneCls(zone, ['frag'])}`}
        >
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setOpen((v) => !v);
            }}
            aria-label={open ? 'Parçaları gizle' : 'Parçaları göster'}
            className="w-7 h-7 rounded-lg flex items-center justify-center text-ink-3 hover:bg-white shrink-0"
          >
            {open ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
          <span className={`w-2 h-2 rounded-full shrink-0 ${STATUS[c.status].dot}`} title={STATUS[c.status].label} />
          <span className="flex-1 min-w-0">
            <span className="block text-[13.5px] font-medium text-ink truncate">{c.title || 'Adsız aday'}</span>
            <span className="block text-[12px] text-ink-3 truncate">
              {c.fragmentIds.length} parça · {optCount(c)}/5 şık{c.answer ? ` · cevap ${c.answer}` : ''}
              {c.questionNumber ? ` · No ${c.questionNumber}` : ''}
            </span>
          </span>
          {c.status !== 'done' && c.stem.trim() && optCount(c) >= 4 && c.answer && (
            <span className="text-[11px] font-semibold text-ok bg-ok-soft px-1.5 rounded-md shrink-0">tam</span>
          )}
        </div>
        {open && (
          <div className="ms-pop-in flex flex-col gap-1.5 py-1.5 pr-1 border-l-2 border-line ml-[18px]" style={{ marginLeft: depth * 20 + 18, paddingLeft: 12 }}>
            {c.fragmentIds.length === 0 && <span className="text-[12.5px] text-ink-3 py-1">Parça yok — havuzdan sürükleyip buraya bırak.</span>}
            {c.fragmentIds.map((id) => {
              const f = fragById.get(id);
              return f ? <React.Fragment key={id}>{FragChip({ f: f, compact: true, inCand: c.id })}</React.Fragment> : null;
            })}
          </div>
        )}
      </li>
    );
  };

  const GroupNode = ({ g, depth }: { g: StudioGroup | null; depth: number }): React.ReactElement | null => {
    const gid = g?.id ?? null;
    const zone = `grp-${gid ?? 'none'}`;
    const kids = state.groups.filter((x) => x.parentId === gid && gid !== null);
    const cands = state.candidates.filter((c) => c.groupId === gid);
    const editing = !!g && editingGroup === g.id;
    const setEditing = (v: boolean) => setEditingGroup(v && g ? g.id : null);
    const collapsed = !!g?.collapsed;
    const on = sel?.t === 'group' && sel.id === gid;
    if (!g && cands.length === 0) return null;
    return (
      <li>
        <div
          {...dropProps(zone, ['frag', 'cand'], (it) => {
            if (it.t === 'cand') moveCand(it.id, gid);
            else createCandidate(fragIds(it), gid);
          })}
          style={{ marginLeft: depth * 20 }}
          onClick={() => {
            if (g) {
              setSel({ t: 'group', id: g.id });
              setInspectorOpen(true);
            }
          }}
          className={`flex items-center gap-2 min-h-10 pl-1 pr-2 rounded-xl cursor-pointer ${on ? 'bg-accent-soft' : 'hover:bg-field'} ${zoneCls(zone, ['frag', 'cand'])}`}
        >
          {g ? (
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                updateGroup(g.id, { collapsed: !collapsed });
              }}
              aria-label={collapsed ? 'Aç' : 'Kapat'}
              className="w-7 h-7 rounded-lg flex items-center justify-center text-ink-2 hover:bg-white shrink-0"
            >
              {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
          ) : (
            <span className="w-7 shrink-0" />
          )}
          <GitBranch className="w-4 h-4 text-accent shrink-0" />
          {g && editing ? (
            <input
              autoFocus
              defaultValue={g.label}
              onClick={(e) => e.stopPropagation()}
              onBlur={(e) => {
                updateGroup(g.id, { label: e.target.value.trim() || g.label });
                setEditing(false);
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
                if (e.key === 'Escape') setEditing(false);
              }}
              className="flex-1 min-w-0 h-8 px-2 rounded-lg bg-white border border-accent text-[14px] font-semibold outline-0"
            />
          ) : (
            <span
              className="flex-1 min-w-0 truncate text-[14px] font-semibold text-ink"
              onDoubleClick={(e) => {
                e.stopPropagation();
                if (g) setEditing(true);
              }}
              title={g ? 'Çift tıkla: yeniden adlandır' : undefined}
            >
              {g ? g.label : 'Gruplanmamış adaylar'}
            </span>
          )}
          {g?.discipline && depth === 0 && g.discipline !== g.label && (
            <span className="text-[11.5px] text-ink-3 bg-field px-2 rounded-full truncate max-w-[140px]">{g.discipline}</span>
          )}
          <span className="text-[12px] font-mono text-ink-3 shrink-0">{cands.length}</span>
          {g && (
            <span className="flex items-center gap-0.5 shrink-0" onClick={(e) => e.stopPropagation()}>
              <button type="button" title="Alt konu ekle" aria-label="Alt konu ekle" onClick={() => createGroup(g.id)} className="w-7 h-7 rounded-lg flex items-center justify-center text-ink-3 hover:text-ink hover:bg-white">
                <FolderPlus className="w-4 h-4" />
              </button>
              <button type="button" title="Bu konuda aday aç" aria-label="Aday ekle" onClick={() => createCandidate([], g.id)} className="w-7 h-7 rounded-lg flex items-center justify-center text-ink-3 hover:text-ink hover:bg-white">
                <Plus className="w-4 h-4" />
              </button>
              <button
                type="button"
                title="Gruptaki tüm adayları (kök, şık, parça) birleştir ve AI ile tek soruya dönüştür"
                aria-label="Grubu AI ile dönüştür"
                onClick={() => mergeGroupForAi(g.id)}
                className="h-7 px-2 rounded-lg flex items-center gap-1 text-[12px] font-semibold text-accent hover:bg-white"
              >
                <Bot className="w-4 h-4" /> <span className="hidden xl:inline">Grubu dönüştür</span>
              </button>
            </span>
          )}
        </div>
        {!collapsed && (
          <ul className="list-none m-0 p-0 flex flex-col gap-0.5 relative">
            {kids.map((k) => (
              <React.Fragment key={k.id}>{GroupNode({ g: k, depth: depth + 1 })}</React.Fragment>
            ))}
            {cands.map((c) => (
              <React.Fragment key={c.id}>{CandRow({ c: c, depth: depth + 1 })}</React.Fragment>
            ))}
            {g && kids.length === 0 && cands.length === 0 && (
              <li className="text-[12.5px] text-ink-3 py-1.5" style={{ marginLeft: (depth + 1) * 20 + 36 }}>
                Boş — parça ya da aday sürükle.
              </li>
            )}
          </ul>
        )}
      </li>
    );
  };

  const TreeView = () => (
    <div className="flex flex-col gap-2">
      <ul className="list-none m-0 p-0 flex flex-col gap-0.5">
        {state.groups
          .filter((g) => g.parentId === null)
          .map((g) => (
            <React.Fragment key={g.id}>{GroupNode({ g: g, depth: 0 })}</React.Fragment>
          ))}
        {GroupNode({ g: null, depth: 0 })}
      </ul>
      {state.groups.length === 0 && state.candidates.length === 0 && (EmptyHint())}
      <div
        {...dropProps('new-cand', ['frag'], (it) => createCandidate(fragIds(it)))}
        className={`mt-1 min-h-14 rounded-2xl border-2 border-dashed border-line flex items-center justify-center gap-2 text-[13px] text-ink-3 ${zoneCls('new-cand', ['frag'])}`}
      >
        <Plus className="w-4 h-4" /> Parçaları buraya bırak: yeni aday
      </div>
    </div>
  );

  const EmptyHint = () => (
    <div className="rounded-2xl bg-field px-5 py-6 text-[13.5px] text-ink-2 flex flex-col gap-2">
      <b className="text-ink">Nasıl çalışır?</b>
      <span>1. Soldaki havuzdan parçaları sürükleyip “yeni aday” alanına bırak ya da <b>Otomatik grupla</b> ile öneri al.</span>
      <span>2. Adayları konulara topla: <b>Konu ekle</b>, alt konu, sürükle bırak.</span>
      <span>3. Sağdaki düzenleyicide kökü, şıkları ve cevabı tamamla; terimleri etiketle.</span>
      <span>4. <b>Soruya dönüştür</b>: parçaların geldiği taslaklar tek soruda birleşir.</span>
    </div>
  );

  // ---------------------------------------------------------------- PANO görünümü
  const BoardView = () => {
    const list = state.candidates.filter((c) => c.status !== 'done' || sel?.id === c.id);
    return (
      <div className="flex gap-3 overflow-x-auto pb-3 items-start min-h-[420px]">
        {list.map((c) => {
          const zone = `col-${c.id}`;
          const on = sel?.t === 'cand' && sel.id === c.id;
          const byKind = (k: FragKind) => c.fragmentIds.map((id) => fragById.get(id)).filter((f): f is StudioFragment => !!f && f.kind === k);
          return (
            <section
              key={c.id}
              {...dropProps(zone, ['frag'], (it) => attach(fragIds(it), c.id))}
              className={`w-[280px] shrink-0 rounded-2xl bg-field p-2.5 flex flex-col gap-2 ${on ? 'ring-2 ring-accent' : ''} ${zoneCls(zone, ['frag'])}`}
            >
              <button
                type="button"
                onClick={() => {
                  setSel({ t: 'cand', id: c.id });
                  setInspectorOpen(true);
                }}
                className="text-left px-1 flex items-start gap-2 cursor-pointer"
              >
                <span className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${STATUS[c.status].dot}`} />
                <span className="flex-1 min-w-0">
                  <span className="block text-[13.5px] font-semibold text-ink line-clamp-2">{c.title || 'Adsız aday'}</span>
                  <span className="block text-[11.5px] text-ink-3 truncate">{groupPath(c.groupId) || 'Gruplanmamış'}</span>
                </span>
              </button>
              {(['stem', 'option', 'clue', 'answer'] as FragKind[]).map((k) => {
                const fs = byKind(k);
                if (!fs.length) return null;
                return (
                  <div key={k} className="flex flex-col gap-1.5">
                    <span className="text-[11px] font-semibold uppercase tracking-[.06em] text-ink-3 px-1">{KIND_LABEL[k]} · {fs.length}</span>
                    {fs.map((f) => (
                      <React.Fragment key={f.id}>{FragChip({ f: f, compact: true, inCand: c.id })}</React.Fragment>
                    ))}
                  </div>
                );
              })}
              <div className="text-[11.5px] text-ink-3 px-1">{optCount(c)}/5 şık · {c.answer ? `cevap ${c.answer}` : 'cevap yok'}</div>
            </section>
          );
        })}
        <section
          {...dropProps('board-new', ['frag'], (it) => createCandidate(fragIds(it)))}
          className={`w-[240px] shrink-0 min-h-[160px] rounded-2xl border-2 border-dashed border-line flex flex-col items-center justify-center gap-2 text-[13px] text-ink-3 p-4 text-center ${zoneCls('board-new', ['frag'])}`}
        >
          <Plus className="w-5 h-5" />
          Parçayı bırak: yeni aday sütunu
          <button type="button" onClick={() => createCandidate([])} className="h-8 px-3 rounded-full bg-white text-accent font-semibold cursor-pointer">
            Boş aday
          </button>
        </section>
      </div>
    );
  };

  // ---------------------------------------------------------------- AKIŞ görünümü
  const [zoom, setZoom] = useState(1);
  const FlowView = () => {
    const NODE_W = 240, FRAG_H = 64, CAND_H = 72, GAP = 14;
    const cands = state.candidates;
    const usedFrags = cands.flatMap((c) => c.fragmentIds).map((id) => fragById.get(id)).filter((f): f is StudioFragment => !!f);
    const groupsUsed = [...new Set(cands.map((c) => c.groupId).filter(Boolean) as string[])].map((id) => groupById.get(id)!).filter(Boolean);
    const pos = (id: string, x: number, y: number) => state.positions[id] || { x, y };
    // Katmanlı yerleşim: parçalar | adaylar | konular
    let yF = 20, yC = 20, yG = 20;
    const fragPos = new Map<string, { x: number; y: number }>();
    const candPos = new Map<string, { x: number; y: number }>();
    const grpPos = new Map<string, { x: number; y: number }>();
    cands.forEach((c) => {
      const fs = c.fragmentIds.filter((id) => fragById.has(id));
      const startF = yF;
      fs.forEach((id) => {
        fragPos.set(id, pos(id, 20, yF));
        yF += FRAG_H + GAP;
      });
      const center = fs.length ? (startF + yF - GAP) / 2 - CAND_H / 2 : yC;
      const yy = Math.max(yC, center);
      candPos.set(c.id, pos(c.id, 340, yy));
      yC = yy + CAND_H + GAP * 2;
      yF = Math.max(yF, yC);
    });
    groupsUsed.forEach((g) => {
      const ys = cands.filter((c) => c.groupId === g.id).map((c) => candPos.get(c.id)!.y);
      const yy = Math.max(yG, ys.length ? ys.reduce((a, b) => a + b, 0) / ys.length : yG);
      grpPos.set(g.id, pos(g.id, 660, yy));
      yG = yy + 60 + GAP;
    });
    const H = Math.max(yF, yC, yG, 400) + 40;
    const W = 940;
    const curve = (x1: number, y1: number, x2: number, y2: number) => {
      const mx = (x1 + x2) / 2;
      return `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`;
    };

    const dragNode = (id: string, start: { x: number; y: number }) => (e: React.PointerEvent) => {
      if ((e.target as HTMLElement).closest('button')) return;
      e.preventDefault();
      const el = e.currentTarget as HTMLElement;
      el.setPointerCapture(e.pointerId);
      const ox = e.clientX, oy = e.clientY;
      let last = start;
      const move = (ev: PointerEvent) => {
        last = { x: Math.max(0, start.x + (ev.clientX - ox) / zoom), y: Math.max(0, start.y + (ev.clientY - oy) / zoom) };
        el.style.left = `${last.x}px`;
        el.style.top = `${last.y}px`;
      };
      const up = () => {
        el.removeEventListener('pointermove', move);
        el.removeEventListener('pointerup', up);
        if (last !== start) commit((s) => ({ ...s, positions: { ...s.positions, [id]: last } }));
      };
      el.addEventListener('pointermove', move);
      el.addEventListener('pointerup', up);
    };

    return (
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-1.5 text-[12.5px] text-ink-3">
          <span className="flex-1">Parçalar → aday → konu. Düğümleri tutup taşı; parçayı aday düğümüne bırak.</span>
          <button type="button" aria-label="Uzaklaş" onClick={() => setZoom((z) => Math.max(0.5, +(z - 0.1).toFixed(2)))} className="w-8 h-8 rounded-lg hover:bg-field flex items-center justify-center"><ZoomOut className="w-4 h-4" /></button>
          <span className="font-mono w-10 text-center">{Math.round(zoom * 100)}%</span>
          <button type="button" aria-label="Yakınlaş" onClick={() => setZoom((z) => Math.min(1.6, +(z + 0.1).toFixed(2)))} className="w-8 h-8 rounded-lg hover:bg-field flex items-center justify-center"><ZoomIn className="w-4 h-4" /></button>
          <button type="button" title="Yerleşimi sıfırla" aria-label="Yerleşimi sıfırla" onClick={() => commit((s) => ({ ...s, positions: {} }))} className="w-8 h-8 rounded-lg hover:bg-field flex items-center justify-center"><Maximize className="w-4 h-4" /></button>
        </div>
        <div className="relative overflow-auto rounded-2xl bg-field" style={{ height: 'min(70vh, 640px)', backgroundImage: 'radial-gradient(var(--color-line-2) 1px, transparent 1px)', backgroundSize: '20px 20px' }}>
          {cands.length === 0 ? (
            <div className="p-6">{EmptyHint()}</div>
          ) : (
            <div className="relative origin-top-left" style={{ width: W, height: H, transform: `scale(${zoom})` }}>
              <svg width={W} height={H} className="absolute inset-0 pointer-events-none" aria-hidden="true">
                {cands.map((c) => {
                  const cp = candPos.get(c.id)!;
                  return (
                    <g key={c.id}>
                      {c.fragmentIds.map((id) => {
                        const fp = fragPos.get(id);
                        if (!fp) return null;
                        const f = fragById.get(id)!;
                        const stroke = f.kind === 'stem' ? 'var(--color-accent)' : f.kind === 'option' ? '#8B5CF6' : f.kind === 'clue' ? 'var(--color-warn)' : 'var(--color-ok)';
                        return <path key={id} d={curve(fp.x + NODE_W, fp.y + FRAG_H / 2, cp.x, cp.y + CAND_H / 2)} fill="none" stroke={stroke} strokeWidth={1.6} strokeOpacity={0.55} />;
                      })}
                      {c.groupId && grpPos.get(c.groupId) && (
                        <path d={curve(cp.x + NODE_W, cp.y + CAND_H / 2, grpPos.get(c.groupId)!.x, grpPos.get(c.groupId)!.y + 28)} fill="none" stroke="var(--color-ink-3)" strokeWidth={1.4} strokeDasharray="4 4" />
                      )}
                    </g>
                  );
                })}
              </svg>
              {usedFrags.map((f) => {
                const p = fragPos.get(f.id)!;
                return (
                  <div
                    key={f.id}
                    onPointerDown={dragNode(f.id, p)}
                    onClick={() => {
                      setSel({ t: 'frag', id: f.id });
                      setInspectorOpen(true);
                    }}
                    className={`absolute rounded-xl bg-white shadow-sm px-2.5 py-1.5 text-[12px] leading-snug cursor-move touch-none ${sel?.id === f.id ? 'ring-2 ring-accent' : ''}`}
                    style={{ left: p.x, top: p.y, width: NODE_W, height: FRAG_H }}
                  >
                    <span className={`text-[11.5px] font-semibold px-1.5 rounded-md ${KIND_STYLE[f.kind]}`}>{KIND_LABEL[f.kind]}</span>
                    <span className="block line-clamp-2 text-ink-2 mt-0.5">{f.text}</span>
                  </div>
                );
              })}
              {cands.map((c) => {
                const p = candPos.get(c.id)!;
                const zone = `flow-${c.id}`;
                return (
                  <div
                    key={c.id}
                    {...dropProps(zone, ['frag'], (it) => attach(fragIds(it), c.id))}
                    onPointerDown={dragNode(c.id, p)}
                    onClick={() => {
                      setSel({ t: 'cand', id: c.id });
                      setInspectorOpen(true);
                    }}
                    className={`absolute rounded-2xl bg-white shadow-md px-3 py-2 cursor-move touch-none border-l-4 ${
                      c.status === 'done' ? 'border-ok' : c.status === 'ready' ? 'border-accent' : 'border-line-2'
                    } ${sel?.id === c.id ? 'ring-2 ring-accent' : ''} ${zoneCls(zone, ['frag'])}`}
                    style={{ left: p.x, top: p.y, width: NODE_W, height: CAND_H }}
                  >
                    <span className="block text-[13px] font-semibold text-ink line-clamp-2">{c.title || 'Adsız aday'}</span>
                    <span className="block text-[11.5px] text-ink-3">{c.fragmentIds.length} parça · {optCount(c)}/5 şık · {STATUS[c.status].label}</span>
                  </div>
                );
              })}
              {groupsUsed.map((g) => {
                const p = grpPos.get(g.id)!;
                return (
                  <div
                    key={g.id}
                    onPointerDown={dragNode(g.id, p)}
                    onClick={() => {
                      setSel({ t: 'group', id: g.id });
                      setInspectorOpen(true);
                    }}
                    className={`absolute rounded-full bg-ink text-white px-4 h-14 flex items-center gap-2 text-[13px] font-semibold cursor-move touch-none shadow-md ${sel?.id === g.id ? 'ring-2 ring-accent' : ''}`}
                    style={{ left: p.x, top: p.y, width: NODE_W }}
                  >
                    <GitBranch className="w-4 h-4 shrink-0" />
                    <span className="truncate">{groupPath(g.id)}</span>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    );
  };

  // ---------------------------------------------------------------- TERİMLER görünümü
  const TermsView = () => {
    const suggestions = suggestSynonyms(termIndex.map(([t]) => t), state.synonyms).slice(0, 12);
    return (
      <div className="flex flex-col gap-4">
        {suggestions.length > 0 && (
          <section className="rounded-2xl bg-field p-3 flex flex-col gap-2">
            <b className="text-[13px] text-ink">Eş anlamlı öneriler · aynı kök</b>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((g) => (
                <button
                  key={g.join('|')}
                  type="button"
                  onClick={() => g.slice(1).forEach((t) => mergeTerms(t, g[0]))}
                  className="h-8 px-3 rounded-full bg-white text-[12.5px] text-ink-2 hover:text-accent inline-flex items-center gap-1.5 cursor-pointer"
                  title="Tek terimde birleştir"
                >
                  <Merge className="w-3.5 h-3.5" />
                  {g.join(' · ')}
                </button>
              ))}
            </div>
          </section>
        )}
        {mergeFrom && (
          <div className="rounded-xl bg-accent-soft text-accent px-3 py-2 text-[13px] flex items-center gap-2">
            <b>“{mergeFrom}”</b> hangi terimle birleşsin? Listeden bir terime tıkla.
            <button type="button" onClick={() => setMergeFrom(null)} className="ml-auto h-7 px-2 rounded-lg hover:bg-white cursor-pointer">Vazgeç</button>
          </div>
        )}
        <div className="overflow-auto rounded-2xl bg-white shadow-sm">
          <table className="w-full text-[13px] border-collapse">
            <thead>
              <tr className="text-left text-[12px] text-ink-3">
                <th className="px-3 h-9 font-semibold sticky top-0 bg-white">Terim</th>
                <th className="px-3 h-9 font-semibold sticky top-0 bg-white">Biçimler</th>
                <th className="px-3 h-9 font-semibold sticky top-0 bg-white">Parça</th>
                <th className="px-3 h-9 font-semibold sticky top-0 bg-white">Adaylar</th>
                <th className="px-3 h-9 sticky top-0 bg-white" />
              </tr>
            </thead>
            <tbody>
              {termIndex.slice(0, 200).map(([t, e]) => {
                const inCands = state.candidates.filter((c) => c.terms.includes(t)).length;
                return (
                  <tr key={t} className="border-t border-line-soft hover:bg-field">
                    <td className="px-3 py-1.5">
                      <button
                        type="button"
                        onClick={() => (mergeFrom ? (mergeTerms(mergeFrom, t), setMergeFrom(null)) : setQ(t))}
                        className="font-semibold text-ink hover:text-accent cursor-pointer"
                        title={mergeFrom ? 'Bu terimle birleştir' : 'Havuzu bu terime göre süz'}
                      >
                        {t}
                      </button>
                    </td>
                    <td className="px-3 py-1.5 text-ink-3 max-w-[260px] truncate">{[...e.forms].filter((x) => x !== t).join(', ') || '—'}</td>
                    <td className="px-3 py-1.5 font-mono">{e.frags.size}</td>
                    <td className="px-3 py-1.5 font-mono">{inCands || '—'}</td>
                    <td className="px-3 py-1.5 text-right whitespace-nowrap">
                      <button type="button" onClick={() => setMergeFrom(t)} className="h-7 px-2 rounded-lg text-[12px] text-ink-2 hover:bg-white cursor-pointer">Birleştir…</button>
                      {state.synonyms[t] && (
                        <button type="button" onClick={() => splitTerm(t)} className="h-7 px-2 rounded-lg text-[12px] text-ink-2 hover:bg-white cursor-pointer">Ayır</button>
                      )}
                      <button
                        type="button"
                        onClick={() => {
                          const ids = [...e.frags].filter((id) => !ownerOf.has(id));
                          if (ids.length) createCandidate(ids);
                          else notify('Bu terimdeki parçaların hepsi zaten bir adayda.');
                        }}
                        className="h-7 px-2 rounded-lg text-[12px] text-accent font-semibold hover:bg-accent-soft cursor-pointer"
                      >
                        Aday yap
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // ---------------------------------------------------------------- DÜZENLEYİCİ
  const selCand = sel?.t === 'cand' ? candById.get(sel.id) : undefined;
  const selFrag = sel?.t === 'frag' ? fragById.get(sel.id) : undefined;
  const selGroup = sel?.t === 'group' ? groupById.get(sel.id) : undefined;

  const groupOptions = (excludeId?: string) =>
    state.groups
      .filter((g) => !excludeId || (g.id !== excludeId && !isDescendant(g.id, excludeId)))
      .map((g) => ({ id: g.id, label: groupPath(g.id) }))
      .sort((a, b) => a.label.localeCompare(b.label, 'tr'));

  const label = 'text-[11.5px] font-semibold uppercase tracking-[.06em] text-ink-3';
  const input = 'w-full rounded-xl bg-field border border-transparent px-3 py-2 text-[14px] text-ink outline-0 focus:border-accent focus:bg-white';

  const CandidateEditor = ({ c }: { c: StudioCandidate }) => {
    const frs = c.fragmentIds.map((id) => fragById.get(id)).filter((f): f is StudioFragment => !!f);
    const stems = frs.filter((f) => f.kind === 'stem' || f.kind === 'clue');
    const suggestedTerms = termsOf(c.fragmentIds).filter((t) => !c.terms.includes(t));
    return (
      <div className="flex flex-col gap-4">
        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${STATUS[c.status].dot}`} />
          <input value={c.title} onChange={(e) => updateCand(c.id, { title: e.target.value })} placeholder="Aday adı" aria-label="Aday adı" className="flex-1 min-w-0 bg-transparent text-[16px] font-semibold text-ink outline-0 border-b border-transparent focus:border-accent py-1" />
        </div>
        <div className="grid grid-cols-2 gap-2">
          <label className="flex flex-col gap-1">
            <span className={label}>Konu</span>
            <select value={c.groupId || ''} onChange={(e) => moveCand(c.id, e.target.value || null)} className={input}>
              <option value="">Gruplanmamış</option>
              {groupOptions().map((g) => (
                <option key={g.id} value={g.id}>{g.label}</option>
              ))}
            </select>
          </label>
          <label className="flex flex-col gap-1">
            <span className={label}>Soru no</span>
            <input inputMode="numeric" value={c.questionNumber ?? ''} onChange={(e) => updateCand(c.id, { questionNumber: Number(e.target.value.replace(/\D/g, '')) || undefined })} placeholder="?" className={`${input} font-mono`} />
          </label>
        </div>

        <div className="flex flex-col gap-1.5">
          <div className="flex items-center gap-2">
            <span className={`${label} flex-1`}>Soru kökü</span>
            {stems.length > 0 && (
              <button
                type="button"
                onClick={() => updateCand(c.id, { stem: stems.map((f) => f.text).join(' ') })}
                className="text-[12px] text-accent font-semibold hover:underline cursor-pointer"
                title="Kök ve ipucu parçalarını birleştirip kökü doldur"
              >
                Parçalardan doldur
              </button>
            )}
          </div>
          <textarea value={c.stem} onChange={(e) => updateCand(c.id, { stem: e.target.value })} rows={4} placeholder="Parçalardan soru kökünü yaz ya da doldur…" className={`${input} resize-y leading-relaxed`} />
        </div>

        <div className="flex flex-col gap-1.5">
          <span className={label}>Şıklar · cevabı seç</span>
          {OPT_KEYS.map((k) => {
            const zone = `opt-${c.id}-${k}`;
            const src = c.optionSources[k];
            return (
              <div
                key={k}
                {...dropProps(zone, ['frag'], (it) => {
                  const f = fragById.get(it.id);
                  if (!f) return;
                  const p = parseOption(f.text);
                  commit((s) => {
                    const s2 = detachFrom(s, [f.id], c.id);
                    return {
                      ...s2,
                      candidates: s2.candidates.map((x) =>
                        x.id === c.id
                          ? {
                              ...x,
                              options: { ...x.options, [k]: p.text },
                              optionSources: { ...x.optionSources, [k]: f.id },
                              fragmentIds: x.fragmentIds.includes(f.id) ? x.fragmentIds : [...x.fragmentIds, f.id],
                            }
                          : x
                      ),
                    };
                  });
                })}
                className={`flex items-center gap-2 rounded-xl ${zoneCls(zone, ['frag'])}`}
              >
                <button
                  type="button"
                  onClick={() => updateCand(c.id, { answer: c.answer === k ? undefined : k })}
                  aria-pressed={c.answer === k}
                  aria-label={`Cevap ${k}`}
                  className={`w-8 h-8 shrink-0 rounded-full text-[12.5px] font-semibold font-mono cursor-pointer transition-colors ${c.answer === k ? 'bg-ok text-white' : 'bg-field text-ink-2 hover:bg-line'}`}
                >
                  {k}
                </button>
                <input value={c.options[k]} onChange={(e) => updateCand(c.id, { options: { ...c.options, [k]: e.target.value } })} placeholder="Şık metni ya da şık parçasını bırak" className={`${input} py-1.5`} />
                {src && <span className="text-[11px] text-violet-700 shrink-0" title="Bu şık bir parçadan geldi">●</span>}
              </div>
            );
          })}
        </div>

        <div className="flex flex-col gap-1.5">
          <span className={label}>Terimler</span>
          <div className="flex flex-wrap gap-1.5">
            {c.terms.map((t) => (
              <span key={t} className="h-7 pl-2.5 pr-1 rounded-full bg-accent-soft text-accent text-[12.5px] inline-flex items-center gap-1">
                {t}
                <button type="button" aria-label={`${t} kaldır`} onClick={() => updateCand(c.id, { terms: c.terms.filter((x) => x !== t) })} className="w-5 h-5 rounded-full hover:bg-white flex items-center justify-center cursor-pointer">
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}
            <input
              value={termDraft}
              onChange={(e) => setTermDraft(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && termDraft.trim()) {
                  updateCand(c.id, { terms: [...new Set([...c.terms, termDraft.trim().toLocaleLowerCase('tr')])] });
                  setTermDraft('');
                }
              }}
              placeholder="+ terim"
              className="h-7 w-24 px-2 rounded-full bg-field text-[12.5px] outline-0 focus:ring-1 focus:ring-accent"
            />
          </div>
          {suggestedTerms.length > 0 && (
            <div className="flex flex-wrap gap-1 text-[12px] text-ink-3">
              Öneri:
              {suggestedTerms.map((t) => (
                <button key={t} type="button" onClick={() => updateCand(c.id, { terms: [...c.terms, t] })} className="hover:text-accent cursor-pointer">
                  {t}
                </button>
              ))}
            </div>
          )}
        </div>

        <label className="flex flex-col gap-1">
          <span className={label}>Not</span>
          <textarea value={c.notes} onChange={(e) => updateCand(c.id, { notes: e.target.value })} rows={2} placeholder="Yerleştirme notu, şüpheler…" className={`${input} resize-y`} />
        </label>

        <div className="flex flex-col gap-1.5">
          <span className={label}>Bağlı parçalar · {frs.length}</span>
          <div
            {...dropProps(`insp-${c.id}`, ['frag'], (it) => attach(fragIds(it), c.id))}
            className={`flex flex-col gap-1.5 rounded-xl min-h-12 ${zoneCls(`insp-${c.id}`, ['frag'])}`}
          >
            {frs.length === 0 && <span className="text-[12.5px] text-ink-3 p-2">Parça sürükleyip buraya bırak.</span>}
            {frs.map((f) => (
              <React.Fragment key={f.id}>{FragChip({ f: f, compact: true, inCand: c.id })}</React.Fragment>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-line">
          <div role="radiogroup" aria-label="Durum" className="ms-seg">
            {(['open', 'ready'] as const).map((s) => (
              <button key={s} type="button" role="radio" aria-checked={c.status === s} onClick={() => updateCand(c.id, { status: s })}>
                {STATUS[s].label}
              </button>
            ))}
          </div>
          <span className="flex-1" />
          <button type="button" onClick={() => deleteCand(c.id)} className="ms-btn is-danger">
            <Trash2 /> Sil
          </button>
          <button
            type="button"
            onClick={() => void openAi(c)}
            className="ms-btn is-tonal"
            title="Bulut ve yerel AI modelleriyle soru ve alternatifler üret"
          >
            <Bot /> AI ile dönüştür
          </button>
          <button
            type="button"
            disabled={busy === c.id}
            onClick={() => void convert(c)}
            className="ms-btn is-primary"
            title="Parçaların geldiği taslakları tek soruda birleştirip bu alanlarla kaydeder"
          >
            {busy === c.id ? 'Kaydediliyor…' : c.status === 'done' ? 'Yeniden kaydet' : 'Soruya dönüştür'}
            <ArrowRight />
          </button>
        </div>
        {c.convertedQuestionId && <span className="text-[12px] text-ok">Kaydedildi · {c.convertedQuestionId}</span>}
      </div>
    );
  };

  const FragmentInspector = ({ f }: { f: StudioFragment }) => {
    const owner = ownerOf.get(f.id);
    const similar = allFrags
      .filter((x) => x.id !== f.id)
      .map((x) => ({ x, s: similarity(f.terms, x.terms, state.synonyms) }))
      .filter((r) => r.s > 0.1)
      .sort((a, b) => b.s - a.s)
      .slice(0, 6);
    return (
      <div className="flex flex-col gap-4">
        <div className="flex items-center gap-2">
          <span className={`text-[12px] font-semibold px-2 rounded-md ${KIND_STYLE[f.kind]}`}>{KIND_LABEL[f.kind]}</span>
          <span className="text-[12.5px] text-ink-3 truncate">{f.discipline}{f.questionNumber ? ` · No ${f.questionNumber}` : ''}</span>
        </div>
        <p className="m-0 text-[15px] leading-relaxed text-ink whitespace-pre-wrap">{f.text}</p>
        <div className="text-[12.5px] text-ink-3">
          {f.author}
          {f.timestamp ? ` · ${new Date(f.timestamp).toLocaleDateString('tr-TR')}` : ''} · taslak <span className="font-mono">{f.draftId}</span>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {f.terms.slice(0, 14).map((t) => (
            <button key={t} type="button" onClick={() => setQ(canonical(t, state.synonyms))} className="h-7 px-2.5 rounded-full bg-field text-[12.5px] text-ink-2 hover:text-accent cursor-pointer">
              {canonical(t, state.synonyms)}
            </button>
          ))}
        </div>
        <div className="flex flex-col gap-1.5">
          <span className={label}>Aday</span>
          <select
            value={owner || ''}
            onChange={(e) => {
              if (e.target.value === '__new') createCandidate([f.id]);
              else if (e.target.value) attach([f.id], e.target.value);
              else commit((s) => detachFrom(s, [f.id]));
            }}
            className={input}
          >
            <option value="">Eşlenmemiş</option>
            <option value="__new">+ Yeni aday oluştur</option>
            {state.candidates.map((c) => (
              <option key={c.id} value={c.id}>{c.title || 'Adsız aday'}</option>
            ))}
          </select>
        </div>
        {similar.length > 0 && (
          <div className="flex flex-col gap-1.5">
            <span className={label}>Benzer parçalar</span>
            {similar.map(({ x, s }) => (
              <div key={x.id} className="flex items-start gap-2">
                <span className="w-9 shrink-0 text-[11.5px] font-mono text-ink-3 pt-2">%{Math.round(s * 100)}</span>
                <div className="flex-1 min-w-0">{FragChip({ f: x, compact: true })}</div>
                <button
                  type="button"
                  title={owner ? 'Aynı adaya ekle' : 'İkisiyle aday oluştur'}
                  aria-label="Birlikte eşle"
                  onClick={() => (owner ? attach([x.id], owner) : createCandidate([f.id, x.id]))}
                  className="w-8 h-8 mt-1 rounded-lg text-accent hover:bg-accent-soft flex items-center justify-center cursor-pointer shrink-0"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
        <button type="button" onClick={() => toggleHide([f.id])} className="self-start h-8 px-3 rounded-full bg-field text-[12.5px] text-ink-2 inline-flex items-center gap-1.5 cursor-pointer">
          {hidden.has(f.id) ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
          {hidden.has(f.id) ? 'Gizlemeyi kaldır' : 'Gizle (çöp/anlamsız)'}
        </button>
      </div>
    );
  };

  const GroupEditor = ({ g }: { g: StudioGroup }) => (
    <div className="flex flex-col gap-4">
      <label className="flex flex-col gap-1">
        <span className={label}>Konu adı</span>
        <input value={g.label} onChange={(e) => updateGroup(g.id, { label: e.target.value })} className={input} />
      </label>
      <label className="flex flex-col gap-1">
        <span className={label}>Ders</span>
        <input list="studio-disc" value={g.discipline} onChange={(e) => updateGroup(g.id, { discipline: e.target.value })} className={input} />
        <datalist id="studio-disc">{disciplines.map((d) => <option key={d} value={d} />)}</datalist>
      </label>
      <label className="flex flex-col gap-1">
        <span className={label}>Üst konu</span>
        <select value={g.parentId || ''} onChange={(e) => updateGroup(g.id, { parentId: e.target.value || null })} className={input}>
          <option value="">— En üst —</option>
          {groupOptions(g.id).map((x) => (
            <option key={x.id} value={x.id}>{x.label}</option>
          ))}
        </select>
      </label>
      <div className="text-[13px] text-ink-2">
        {state.candidates.filter((c) => c.groupId === g.id).length} aday · {state.groups.filter((x) => x.parentId === g.id).length} alt konu
      </div>
      <div className="flex gap-2">
        <button type="button" onClick={() => createGroup(g.id)} className="ms-btn"><FolderPlus /> Alt konu</button>
        <button type="button" onClick={() => createCandidate([], g.id)} className="ms-btn"><Plus /> Aday</button>
        <span className="flex-1" />
        <button type="button" onClick={() => deleteGroup(g.id)} className="ms-btn is-danger"><Trash2 /> Sil</button>
      </div>
      <span className="text-[12px] text-ink-3">Silince içindeki adaylar ve alt konular bir üst seviyeye taşınır.</span>
    </div>
  );

  // ---------------------------------------------------------------- yerleşim
  const VIEWS: { id: View; label: string; icon: React.ElementType }[] = [
    { id: 'tree', label: 'Ağaç', icon: GitBranch },
    { id: 'board', label: 'Pano', icon: Columns3 },
    { id: 'flow', label: 'Akış', icon: Workflow },
    { id: 'terms', label: 'Terimler', icon: Tags },
  ];
  const chip = (on: boolean) => `h-8 px-3 rounded-full text-[12.5px] whitespace-nowrap cursor-pointer transition-colors ${on ? 'bg-ink text-white font-semibold' : 'bg-field text-ink-2 hover:text-ink'}`;

  return (
    <div className="flex flex-col gap-3 min-w-0">
      {/* Başlık + araç çubuğu */}
      <div className="flex flex-wrap items-center gap-2">
        <div className="min-w-0 mr-auto">
          <p className="m-0 text-[13px] text-ink-2">
            {committeeName || 'Kurul'} · {stats.frags} parça · <b className="text-ink">{stats.free}</b> eşlenmemiş · {stats.cands} aday · {stats.ready} hazır · {stats.done} soru oldu
          </p>
        </div>
        <div role="tablist" aria-label="Görünüm" className="ms-seg">
          {VIEWS.map((v) => {
            const Icon = v.icon;
            return (
              <button key={v.id} type="button" role="tab" aria-selected={view === v.id} onClick={() => setView(v.id)}>
                <Icon className="w-4 h-4" /> {v.label}
              </button>
            );
          })}
        </div>
        <button type="button" onClick={autoGroup} className="ms-btn is-primary" title="Eşlenmemiş benzer parçalardan aday öner">
          <Sparkles /> Otomatik grupla
        </button>
        <button type="button" onClick={() => createGroup(null, discF !== 'all' ? discF : '')} className="ms-btn">
          <FolderPlus /> Konu
        </button>
        <span className="inline-flex">
          <button type="button" onClick={undo} disabled={!past.current.length} aria-label="Geri al" title="Geri al (Ctrl+Z)" className="ms-btn is-ghost is-icon"><Undo2 className="w-4 h-4" /></button>
          <button type="button" onClick={redo} disabled={!future.current.length} aria-label="Yinele" title="Yinele (Ctrl+Shift+Z)" className="ms-btn is-ghost is-icon"><Redo2 className="w-4 h-4" /></button>
          <button type="button" onClick={exportJson} aria-label="Dışa aktar" title="Stüdyoyu JSON olarak indir" className="ms-btn is-ghost is-icon"><Download className="w-4 h-4" /></button>
          <button type="button" onClick={() => importRef.current?.click()} aria-label="İçe aktar" title="JSON içe aktar" className="ms-btn is-ghost is-icon"><Upload className="w-4 h-4" /></button>
          <input ref={importRef} type="file" accept="application/json" hidden onChange={(e) => e.target.files?.[0] && void importJson(e.target.files[0])} />
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[300px_minmax(0,1fr)] xl:grid-cols-[300px_minmax(0,1fr)_380px] gap-3 items-start">
        {/* Sol: parça havuzu */}
        <aside className="bg-white rounded-2xl shadow-sm flex flex-col min-h-0 lg:sticky lg:top-3 lg:max-h-[calc(100dvh-140px)]" aria-label="Parça havuzu">
          <button type="button" onClick={() => setPoolOpen((v) => !v)} className="lg:hidden flex items-center gap-2 px-4 h-12 text-[14px] font-semibold cursor-pointer">
            Parça havuzu · {pool.length} {poolOpen ? <ChevronDown className="w-4 h-4 ml-auto" /> : <ChevronRight className="w-4 h-4 ml-auto" />}
          </button>
          <div className={`${poolOpen ? 'flex' : 'hidden'} lg:flex flex-col gap-2 p-3 border-b border-line-soft`}>
            <label className="flex items-center gap-2 h-9 px-3 rounded-full bg-field">
              <Search className="w-4 h-4 text-ink-3" />
              <span className="sr-only">Parçalarda ara</span>
              <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Metin ya da terim" className="flex-1 min-w-0 bg-transparent outline-0 text-[13.5px]" />
              {q && <button type="button" aria-label="Temizle" onClick={() => setQ('')} className="cursor-pointer"><X className="w-4 h-4 text-ink-3" /></button>}
            </label>
            <div className="flex flex-wrap gap-1">
              {(['all', 'stem', 'option', 'clue', 'answer'] as const).map((k) => (
                <button key={k} type="button" onClick={() => setKindF(k)} className={chip(kindF === k)}>
                  {k === 'all' ? 'Tümü' : KIND_LABEL[k]}
                </button>
              ))}
            </div>
            <select value={discF} onChange={(e) => setDiscF(e.target.value)} aria-label="Ders" className="h-9 px-3 rounded-full bg-field text-[13px] outline-0 cursor-pointer">
              <option value="all">Tüm dersler</option>
              {disciplines.map((d) => <option key={d} value={d}>{d}</option>)}
            </select>
            <div className="flex items-center gap-3 text-[12.5px] text-ink-2">
              <label className="inline-flex items-center gap-1.5 cursor-pointer"><input type="checkbox" checked={onlyFree} onChange={(e) => setOnlyFree(e.target.checked)} /> Yalnız eşlenmemiş</label>
              <label className="inline-flex items-center gap-1.5 cursor-pointer"><input type="checkbox" checked={showHidden} onChange={(e) => setShowHidden(e.target.checked)} /> Gizlileri göster</label>
            </div>
          </div>
          {picked.length > 0 && (
            <div className="ms-pop-in mx-3 mt-2 rounded-xl bg-ink text-white px-3 py-2 flex items-center gap-2 text-[12.5px]">
              <ListChecks className="w-4 h-4" /> {picked.length} seçili
              <span className="flex-1" />
              <button type="button" onClick={() => createCandidate(picked)} className="h-7 px-2.5 rounded-full bg-white/15 hover:bg-white/25 font-semibold cursor-pointer">Aday yap</button>
              <button type="button" onClick={() => { toggleHide(picked); setPicked([]); }} className="h-7 px-2 rounded-full hover:bg-white/15 cursor-pointer">Gizle</button>
              <button type="button" aria-label="Seçimi temizle" onClick={() => setPicked([])} className="w-7 h-7 rounded-full hover:bg-white/15 flex items-center justify-center cursor-pointer"><X className="w-4 h-4" /></button>
            </div>
          )}
          <div className={`${poolOpen ? 'flex' : 'hidden'} lg:flex flex-col gap-1.5 p-3 overflow-y-auto overscroll-contain min-h-0 max-h-[60dvh] lg:max-h-none`}>
            {pool.length === 0 && <span className="text-[13px] text-ink-3 py-6 text-center">{allFrags.length ? 'Bu süzgeçte parça yok.' : 'Bu kurulda taslak parça yok.'}</span>}
            {pool.slice(0, 400).map((f) => (
              <React.Fragment key={f.id}>{FragChip({ f: f })}</React.Fragment>
            ))}
            {pool.length > 400 && <span className="text-[12px] text-ink-3 text-center py-2">İlk 400 parça gösteriliyor; süzgeçle daralt.</span>}
          </div>
        </aside>

        {/* Orta: görünüm */}
        <section aria-label="Stüdyo görünümü" className="min-w-0 bg-white rounded-2xl shadow-sm p-3 sm:p-4" onClick={() => setPicked([])}>
          {view === 'tree' && TreeView()}
          {view === 'board' && BoardView()}
          {view === 'flow' && FlowView()}
          {view === 'terms' && TermsView()}
        </section>

        {/* Sağ: düzenleyici (geniş ekranda sabit, dar ekranda çekmece) */}
        {(sel && (selCand || selFrag || selGroup)) ? (
          <>
            {inspectorOpen && <button type="button" aria-label="Düzenleyiciyi kapat" onClick={() => setInspectorOpen(false)} className="xl:hidden ms-fade-in fixed inset-0 z-40 bg-[rgba(14,26,38,0.35)] cursor-default" />}
            <aside
              aria-label="Düzenleyici"
              className={`${inspectorOpen ? 'flex' : 'hidden'} xl:flex ms-slide-left xl:animate-none fixed xl:sticky z-50 xl:z-auto top-0 xl:top-3 right-0 bottom-0 xl:bottom-auto w-[min(420px,94vw)] xl:w-auto xl:max-h-[calc(100dvh-140px)] flex-col bg-white xl:rounded-2xl shadow-xl xl:shadow-sm overflow-y-auto overscroll-contain p-4`}
            >
              <div className="flex items-center gap-2 mb-3">
                <CircleDot className="w-4 h-4 text-accent" />
                <span className="text-[13px] font-semibold text-ink-2 flex-1">
                  {selCand ? 'Soru adayı' : selFrag ? 'Parça' : 'Konu'}
                </span>
                <button type="button" aria-label="Kapat" onClick={() => { setSel(null); setInspectorOpen(false); }} className="ms-btn is-ghost is-icon is-sm"><X /></button>
              </div>
              {selCand && <React.Fragment key={selCand.id}>{CandidateEditor({ c: selCand })}</React.Fragment>}
              {selFrag && <React.Fragment key={selFrag.id}>{FragmentInspector({ f: selFrag })}</React.Fragment>}
              {selGroup && <React.Fragment key={selGroup.id}>{GroupEditor({ g: selGroup })}</React.Fragment>}
            </aside>
          </>
        ) : (
          <aside className="hidden xl:flex flex-col gap-2 bg-white rounded-2xl shadow-sm p-4 text-[13px] text-ink-2 sticky top-3">
            <Check className="w-5 h-5 text-accent" />
            <b className="text-ink text-[14px]">Bir şey seç</b>
            Aday, parça ya da konuya tıkla; tüm alanları burada düzenlersin.
            <span className="text-ink-3 text-[12px] mt-2">Kısayollar: Ctrl+Z geri al · Ctrl+Shift+Z yinele · Shift+tık çoklu seç · Esc seçimi bırak</span>
          </aside>
        )}
      </div>
      {aiFor && candById.get(aiFor) && AiPanel({ c: candById.get(aiFor)! })}
    </div>
  );
};
