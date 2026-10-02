import json, os, glob, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
OUT = r"C:\Users\indui\Desktop\meds\data\ds_out"
BAT = r"C:\Users\indui\Desktop\meds\data\ds_work\batches"

STATUS = {"onaylandi", "inceleme_gerekli", "kullanilamaz"}
ANSWER = {"dogrulandi", "duzeltildi", "dogrulanamadi", "belirsiz"}
EVID = {"kanitli", "kismi_kanit", "not_yok"}

problems = Counter()
for f in sorted(glob.glob(os.path.join(OUT, "*.json"))):
    bid = os.path.basename(f)[:-5]
    d = json.load(open(f, encoding='utf-8'))
    src = json.load(open(os.path.join(BAT, bid + ".json"), encoding='utf-8'))
    src_ids = [q['id'] for q in src['questions']]
    out_ids = [q.get('id') for q in d.get('questions', [])]
    print(f"\n=== {bid} | girdi={len(src_ids)} çıktı={len(out_ids)}")
    if bid != d.get('batchId'):
        problems['batchId_uyumsuz'] += 1
    if set(src_ids) != set(out_ids):
        problems['id_kumesi_farkli'] += 1
        print("   EKSİK:", set(src_ids) - set(out_ids), "| FAZLA:", set(out_ids) - set(src_ids))
    for q in d.get('questions', []):
        qid = q.get('id')
        if q.get('status') not in STATUS: problems['status_gecersiz'] += 1; print("   status?", qid, q.get('status'))
        if q.get('answerStatus') not in ANSWER: problems['answerStatus_gecersiz'] += 1; print("   answerStatus?", qid, q.get('answerStatus'))
        if q.get('evidenceStatus') not in EVID: problems['evidenceStatus_gecersiz'] += 1; print("   evidenceStatus?", qid, q.get('evidenceStatus'))
        opts = q.get('options') or []
        if len(opts) != 5: problems['sik_sayisi_5_degil'] += 1; print("   şık sayısı", qid, len(opts))
        keys = [o.get('key') for o in opts]
        if keys != ['A', 'B', 'C', 'D', 'E']: problems['sik_anahtar_sirasi'] += 1; print("   anahtarlar", qid, keys)
        corr = [o.get('key') for o in opts if o.get('isCorrect')]
        if len(corr) != 1: problems['dogru_sik_sayisi'] += 1; print("   doğru şık", qid, corr)
        if corr and q.get('correctAnswer') != corr[0]: problems['cevap_tutarsiz'] += 1; print("   cevap tutarsız", qid, q.get('correctAnswer'), corr)
        ex = q.get('explanation') or ''
        if len(ex) < 300: problems['aciklama_kisa'] += 1; print("   kısa açıklama", qid, len(ex))
        if not (q.get('stem') or '').strip(): problems['bos_kok'] += 1
        if re.search(r'[ÃÄÅÂ]|&apos;|&#\d+;', (q.get('stem') or '') + ex + (q.get('topic') or '')):
            problems['mojibake_kaldi'] += 1; print("   mojibake", qid)
        if not (q.get('topic') or '').strip(): problems['konu_yok'] += 1
        for lm in (q.get('lectureMatches') or []):
            if not lm.get('evidenceQuote'): problems['kanit_alintisi_yok'] += 1; print("   alıntı yok", qid)
        if q.get('status') == 'kullanilamaz':
            problems['kullanilamaz'] += 1

print("\n### SORUN ÖZETİ ###")
for k, v in problems.most_common(): print(f"  {k}: {v}")
if not problems: print("  (sorun yok)")

# örnek çıktı
f = sorted(glob.glob(os.path.join(OUT, "*.json")))[0]
d = json.load(open(f, encoding='utf-8'))
print("\n### ÖRNEK ÇIKTI ###")
print(json.dumps(d['questions'][0], ensure_ascii=False, indent=1)[:3200])
