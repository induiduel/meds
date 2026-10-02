import dotenv from 'dotenv';
dotenv.config();
import { createClient } from '@supabase/supabase-js';

const url = process.env.SUPABASE_URL!;
const key = (process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY)!;
const client = createClient(url, key);

// Common medical syndrome & disease concept banks
const MEDICAL_CONCEPT_BANKS: Array<{
  id: string;
  name: string;
  discipline?: string;
  terms: string[];
}> = [
  {
    id: 'trizomi21_down',
    name: 'Down Sendromu (Trizomi 21)',
    discipline: 'Tıbbi Genetik',
    terms: [
      'down', 'trizomi 21', '21 kromozom', 'ense saydamligi', 'nt', 'av kanal',
      'endokardiyal yastik', 'cift kabarcik', 'double bubble', 'simian',
      'brushfield', 'hipotoni', 'makroglossi', 'burun kemigi', 'basik burun',
      'edwards sendromu', 'patau sendromu', 'fetal ultrason', 'birinci trimester',
      'anne yasi', 'duodenal atrezi'
    ]
  },
  {
    id: 'amiloidoz_kongo',
    name: 'Amiloidoz & Kongo Kırmızısı',
    discipline: 'Tıbbi Patoloji',
    terms: [
      'amiloid', 'kongo kirmizisi', 'congo red', 'elma yesili', 'cift kirinim',
      'polarize isik', 'birefringence', 'apple green', 'al amiloid', 'aa amiloid'
    ]
  },
  {
    id: 'legionella_klima',
    name: 'Legionella Pnömonisi',
    discipline: 'Tıbbi Mikrobiyoloji',
    terms: [
      'legionella', 'klima', 'bcye', 'hiponatremi', 'atipik pnomoni', 'lejyone'
    ]
  }
];

function normalizeText(text: string = ''): string {
  if (!text) return '';
  return text
    .toLocaleLowerCase('tr-TR')
    .replace(/ı/g, 'i')
    .replace(/ğ/g, 'g')
    .replace(/ü/g, 'u')
    .replace(/ş/g, 's')
    .replace(/ö/g, 'o')
    .replace(/ç/g, 'c')
    .replace(/[^a-z0-9\s]/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function detectConcepts(text: string, discipline?: string): string[] {
  const norm = normalizeText(text);
  const matchedConcepts: string[] = [];

  for (const bank of MEDICAL_CONCEPT_BANKS) {
    if (discipline && bank.discipline && !discipline.toLowerCase().includes(bank.discipline.toLowerCase()) && !bank.discipline.toLowerCase().includes(discipline.toLowerCase())) {
      continue;
    }
    const matchedTerms = bank.terms.filter(t => norm.includes(t));
    if (matchedTerms.length >= 1) {
      matchedConcepts.push(bank.id);
    }
  }

  return matchedConcepts;
}

async function test() {
  const { data: questions } = await client.from('questions').select('*').eq('committee_id', 'donem3-kurul1');
  if (!questions) return;
  
  const downQuestions = questions.filter(x => x.id.includes('1790967'));
  console.log('Testing concept detection on 3 Down questions:');

  downQuestions.forEach((q, idx) => {
    const allText = [
      q.topic,
      ...q.fragments.map((f: any) => f.text),
      ...(q.options || []).map((o: any) => o.text)
    ].join(' ');

    console.log(`Q${idx + 1} (${q.id}):`);
    console.log(`  Concepts:`, detectConcepts(allText, q.discipline));
  });

  const amyloidQuestions = questions.filter(x => x.id.includes('179095'));
  console.log('\nTesting concept detection on 5 Amyloid questions:');
  amyloidQuestions.forEach((q, idx) => {
    const allText = [
      q.topic,
      ...q.fragments.map((f: any) => f.text),
      ...(q.options || []).map((o: any) => o.text)
    ].join(' ');

    console.log(`Q${idx + 1} (${q.id}):`);
    console.log(`  Concepts:`, detectConcepts(allText, q.discipline));
  });

  process.exit(0);
}

test();
