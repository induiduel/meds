import dotenv from 'dotenv';
dotenv.config();

// Test Turkish normalization
export function normalizeMedicalText(text: string = ''): string {
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

console.log('Test normalizer:');
console.log('Ense saydamlığı ->', normalizeMedicalText('Ense saydamlığı (NT)'));
console.log('Kongo kırmızısı ->', normalizeMedicalText('Kongo kırmızısı (Congo red)'));
console.log('Down sendromu ->', normalizeMedicalText('Bence Down Sendromu'));
