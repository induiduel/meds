/**
 * ==============================================================================
 * Soru Eşleştirme ve Gelişmiş Soruya Dönüştürme Servisi
 * (src/services/questionUpgradeService.ts)
 * ==============================================================================
 * Bu servis:
 * 1. Eski/Ham soru (rawQuestion - öğrenci hatırlaması, eksik şıklar) ile
 *    Redakte edilmiş kurul sorusunu (reconstruction) bir araya getirir.
 * 2. Eşleşen amfi ders notlarını, redakte özetleri ve DeepSeek veri havuzunu
 *    birincil referans zemin (ground truth) olarak alır.
 * 3. Yapay zeka modellerini (Gemini 3.8 Flash, Groq DeepSeek R1, Llama 3.3)
 *    kullanarak soruyu çok basamaklı, USMLE / TUS formatında ileri düzey
 *    klinik vaka sorusuna (Advanced Clinical Case Question) çevirir.
 * 4. Oluşturulan gelişmiş soruyu kalıcı veri tabanına ve RAG indeksine kaydeder.
 * ==============================================================================
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { QuestionItem } from '../types';
import { loadDeepSeekContributions } from './deepseekDataService.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.resolve(PROJECT_ROOT, 'data');
const PAST_QUESTIONS_FILE = path.resolve(DATA_DIR, 'pastQuestions.json');

export interface AdvancedQuestionData {
  stem: string;
  clinicalScenario: string;
  options: Array<{
    key: 'A' | 'B' | 'C' | 'D' | 'E';
    text: string;
    rationale?: string;
    isCorrect: boolean;
  }>;
  correctAnswer: 'A' | 'B' | 'C' | 'D' | 'E';
  explanation: string;
  distractorAnalysis: Record<string, string>;
  clinicalPearl: string;
  difficulty: 'İleri Düzey (TUS / USMLE)' | 'Klinik Vaka' | 'Çok Basamaklı Muhakeme';
  generatedAt: string;
  modelUsed: string;
  upgradedFrom: {
    questionId: string;
    rawStem?: string;
    redactedStem?: string;
    examYear?: string;
    discipline?: string;
  };
}

/**
 * Build rich dual prompt for AI to upgrade matched question to advanced case
 */
export function buildUpgradePrompt(
  question: any,
  lectureSnippet?: string,
  deepseekContext?: string
): string {
  const rawStem = question.rawQuestion?.stem || question.rawStem || question.fragments?.[0]?.text || '';
  const rawOptions = (question.rawQuestion?.options || []).map((o: any) => typeof o === 'string' ? o : `${o.key || o.label || ''}) ${o.text || ''}`).join('\n');

  const recStem = question.reconstruction?.stem || question.stem || '';
  const recOptions = (question.reconstruction?.options || question.options || []).map((o: any) => typeof o === 'string' ? o : `${o.key || o.label || ''}) ${o.text || ''}`).join('\n');
  const claimedAns = question.reconstruction?.correctAnswer || question.claimedAnswer || '';
  const recExpl = question.reconstruction?.explanation || question.explanation || '';

  return `Sen Türkiye'deki Tıp Fakültesi Kurul ve TUS Komisyonunda görevli kıdemli bir Tıp Profesörüsün.
Aşağıda tıp öğrencilerinin sınav hafızasından derlenmiş "ESKİ/HAM SORU" ile fakülte amfi ders notlarıyla doğrulanmış "REDAKTE EDİLMİŞ ÇIKMIŞ SORU" verilmiştir.

GÖREVİN:
Bu soru çiftini alarak, ölçülen tıbbi kazanımı kaybetmeden USMLE Step 2 CK / TUS düzeyinde çok daha gelişmiş, çok basamaklı ve öğretici bir "İLERİ DÜZEY KLİNİK VAKA SORUSU (Advanced Clinical Scenario)" haline getirmektir.

--- BİLGİ KAYNAKLARI (BİRİNCİL ZEMİNLEME) ---
1. [ESKİ / HAM ÖĞRENCİ SORUSU]:
Soru Kökü: ${rawStem || 'Eski soru metni yok.'}
Şıklar:
${rawOptions || 'Ham şıklar belirtilmemiş.'}

2. [REDAKTE EDİLMİŞ KURUL SORUSU]:
Ders / Branş: ${question.discipline || 'Tıp'}
Kurul: ${question.committeeId || 'donem3-kurul1'}
Konu: ${question.topic || 'Kurul Sorusu'}
Redakte Soru:
${recStem}
Seçenekler:
${recOptions}
Doğru Cevap: ${claimedAns}
Akademik Açıklama: ${recExpl}

${lectureSnippet ? `3. [DOĞRULANMIŞ AMFİ DERS NOTU BAĞLAMI]:\n${lectureSnippet}\n` : ''}
${deepseekContext ? `4. [TOPLANAN DEEPSEEK BİLGİ HAVUZU]:\n${deepseekContext}\n` : ''}

--- İLERİ DÜZEY SORU GELİŞTİRME KURALLARI ---
1. Soruyu ezberden çıkartıp gerçekçi bir klinik senaryoya (yaş, cinsiyet, başvuru şikayeti, vital bulgular, fizik muayene, lab/görüntüleme bulguları) dönüştür.
2. Çok Basamaklı Mantık (Multi-step Reasoning) uygula: Öğrenci önce hastanın tanısını koymalı, ardından soru kökünde bu hastalığın patofizyolojik mekanizmasını, altın standart tedavisini veya komplikasyonunu yanıtlamalıdır.
3. 5 seçenek oluştur (A, B, C, D, E). Çeldiricilerin her biri klinikte sıkça karışan ayırıcı tanıları temsil etmelidir.
4. Her seçeneğin neden doğru veya neden yanlış olduğunu detaylıca gerekçelendir.
5. Sınavda tam puan aldıracak "Klinik İnci / Altın İpucu (High-Yield Pearl)" ekle.

Lütfen yanıtını KESİNLİKLE aşağıdaki geçerli JSON formatında döndür (JSON dışı hiçbir metin yazma):
{
  "clinicalScenario": "Hastanın klinik öyküsü, vitalleri ve muayenesi...",
  "stem": "Klinik senaryo sonrası asıl soru cümlesi...",
  "options": [
    { "key": "A", "text": "...", "rationale": "Neden elendiği veya neden doğru olduğu...", "isCorrect": false },
    { "key": "B", "text": "...", "rationale": "...", "isCorrect": false },
    { "key": "C", "text": "...", "rationale": "...", "isCorrect": true },
    { "key": "D", "text": "...", "rationale": "...", "isCorrect": false },
    { "key": "E", "text": "...", "rationale": "...", "isCorrect": false }
  ],
  "correctAnswer": "C",
  "explanation": "Detaylı klinik patofizyolojik çözüm...",
  "clinicalPearl": "Öğrencinin mutlaka hatırlaması gereken hap bilgi...",
  "difficulty": "İleri Düzey (TUS / USMLE)"
}`;
}

/**
 * Save an upgraded question to data/pastQuestions.json
 */
export function saveUpgradedQuestion(questionId: string, advancedData: AdvancedQuestionData): boolean {
  if (!fs.existsSync(PAST_QUESTIONS_FILE)) return false;

  try {
    const list: any[] = JSON.parse(fs.readFileSync(PAST_QUESTIONS_FILE, 'utf-8'));
    const idx = list.findIndex(q => q.id === questionId);
    if (idx === -1) return false;

    list[idx].advancedQuestion = advancedData;
    list[idx].hasAdvancedVersion = true;
    list[idx].updatedAt = new Date().toISOString();

    fs.writeFileSync(PAST_QUESTIONS_FILE, JSON.stringify(list, null, 2), 'utf-8');
    return true;
  } catch (err: any) {
    console.error('[QuestionUpgradeService] Soru kaydedilemedi:', err.message);
    return false;
  }
}
