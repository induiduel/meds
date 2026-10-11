/**
 * src/hooks/useOptimisticMutation.ts
 *
 * 4. Madde: İyimser Güncellemeler (Optimistic UI Updates)
 *
 * Kullanıcı bir veriyi güncellediğinde, sildiğinde veya eklediğinde arayüzü
 * güncellemek için sunucudan listenin tamamını tekrar çekme (refetch) ihtiyacını
 * ortadan kaldırır.
 *
 * Çalışma Mantığı:
 * 1. İstemci, sunucudan yanıt beklemeden yerel arayüzü anında günceller (0ms gecikme).
 * 2. Arka planda sunucuya sadece küçük bir PATCH veya PUT isteği atılır.
 * 3. İstek başarısız olursa arayüz anında eski haline geri döndürülür (Rollback).
 * 4. Başarılı veya başarısız olduğunda önbellek tutarlılığı doğrulanır.
 */

import { useMutation, useQueryClient, QueryKey } from '@tanstack/react-query';
import { ApiService } from '../services/api';
import { pastQuestionsCache } from '../services/pastQuestionsCache';
import { StudyNote, saveNotes, getNotes } from '../services/studyStore';
import { QuestionItem } from '../types';

export interface OptimisticMutationOptions<TData, TVariables, TSnapshot> {
  queryKey: QueryKey;
  mutationFn: (variables: TVariables) => Promise<TData>;
  optimisticUpdater: (previousData: TSnapshot | undefined, variables: TVariables) => TSnapshot;
  onSuccess?: (data: TData, variables: TVariables) => void;
  onError?: (error: Error, variables: TVariables, context?: { previousData?: TSnapshot }) => void;
  onSettled?: () => void;
}

/**
 * Genel Amaçlı İyimser Güncelleme Kancası (useOptimisticMutation)
 */
export function useOptimisticMutation<TData, TVariables, TSnapshot = any>(
  options: OptimisticMutationOptions<TData, TVariables, TSnapshot>
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: options.mutationFn,
    onMutate: async (variables: TVariables) => {
      // 1. Olası çakışan arka plan sorgularını iptal et
      await queryClient.cancelQueries({ queryKey: options.queryKey });

      // 2. Geri alma (rollback) için mevcut durumun anlık görüntüsünü (snapshot) al
      const previousData = queryClient.getQueryData<TSnapshot>(options.queryKey);

      // 3. Arayüzü anında güncelle (Optimistic UI)
      queryClient.setQueryData<TSnapshot>(options.queryKey, (old) =>
        options.optimisticUpdater(old, variables)
      );

      return { previousData };
    },
    onError: (err: any, variables: TVariables, context) => {
      // 4. Hata durumunda derhal eski duruma geri dön (Rollback)
      if (context?.previousData !== undefined) {
        queryClient.setQueryData(options.queryKey, context.previousData);
      }
      options.onError?.(err, variables, context);
    },
    onSuccess: (data: TData, variables: TVariables) => {
      options.onSuccess?.(data, variables);
    },
    onSettled: () => {
      // 5. İşlem bitiminde önbelleği sunucuyla doğrula
      queryClient.invalidateQueries({ queryKey: options.queryKey });
      options.onSettled?.();
    },
  });
}

/**
 * Çıkmış Soru Beğeni / Oy İçin İyimser Güncelleme Kancası
 */
export function useOptimisticPastQuestionVote(questionId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ isUpvote, voterId }: { isUpvote: boolean; voterId?: string }) => {
      if (isUpvote) {
        return ApiService.upvotePastQuestion(questionId, voterId);
      } else {
        return ApiService.downvotePastQuestion(questionId, voterId);
      }
    },
    onMutate: async ({ isUpvote, voterId }) => {
      const qKey = ['past-question-detail', questionId];
      await queryClient.cancelQueries({ queryKey: qKey });
      const previous = queryClient.getQueryData<QuestionItem>(qKey);

      // IndexedDB ve bellek önbelleğinde anında güncelle
      const cached = await pastQuestionsCache.getCachedQuestionById(questionId);
      if (cached) {
        const updated = { ...cached };
        if (isUpvote) {
          updated.upvotes = (updated.upvotes || 0) + 1;
        } else {
          (updated as any).downvotes = ((updated as any).downvotes || 0) + 1;
        }
        await pastQuestionsCache.saveQuestion(updated);
      }

      if (previous) {
        queryClient.setQueryData<QuestionItem>(qKey, {
          ...previous,
          upvotes: isUpvote ? (previous.upvotes || 0) + 1 : previous.upvotes,
        });
      }

      return { previous, cached };
    },
    onError: async (_err, _vars, context) => {
      // Rollback
      if (context?.cached) {
        await pastQuestionsCache.saveQuestion(context.cached);
      }
      if (context?.previous) {
        queryClient.setQueryData(['past-question-detail', questionId], context.previous);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['past-question-detail', questionId] });
    },
  });
}

/**
 * Soru Havuzu Sorusu İçin Kısmi Yama (PATCH) İyimser Güncelleme Kancası
 */
export function useOptimisticQuestionPatch(questionId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (patch: Partial<QuestionItem>) => {
      const res = await fetch(`/api/questions/${encodeURIComponent(questionId)}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patch),
      });
      if (!res.ok) throw new Error('Yama uygulanamadı');
      return (await res.json()) as { success: boolean; question: QuestionItem };
    },
    onMutate: async (patch) => {
      const key = ['questions'];
      await queryClient.cancelQueries({ queryKey: key });
      const previousList = queryClient.getQueryData<QuestionItem[]>(key);

      if (previousList) {
        queryClient.setQueryData<QuestionItem[]>(
          key,
          previousList.map((q) => (q.id === questionId ? { ...q, ...patch } : q))
        );
      }

      return { previousList };
    },
    onError: (_err, _patch, context) => {
      if (context?.previousList) {
        queryClient.setQueryData(['questions'], context.previousList);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['questions'] });
    },
  });
}

/**
 * Kişisel Çalışma Notu İyimser Güncelleme Kancası
 */
export function useOptimisticNoteUpdate() {
  return useMutation({
    mutationFn: async (updatedNote: StudyNote) => {
      const notes = getNotes();
      const idx = notes.findIndex((n) => n.id === updatedNote.id);
      let nextList: StudyNote[];
      if (idx >= 0) {
        nextList = [...notes];
        nextList[idx] = updatedNote;
      } else {
        nextList = [updatedNote, ...notes];
      }
      saveNotes(nextList);
      return updatedNote;
    },
    onMutate: async (updatedNote) => {
      const previousNotes = getNotes();
      return { previousNotes };
    },
    onError: (_err, _vars, context) => {
      if (context?.previousNotes) {
        saveNotes(context.previousNotes);
      }
    },
  });
}
