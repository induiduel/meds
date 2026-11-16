"""
Adım 5: Doğrulanmış JSONL'i hedef klasöre yaz ve bütünlüğünü doğrula.
Hedef: C:\\Users\\indui\\Desktop\\meds_database\\deepseek_data
"""
import json, os, sys, hashlib, glob, re
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
WORK = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/.meds_ds/work")
SRC = os.path.join(WORK, "meds_donem3_sorulari_duzeltilmis.jsonl")
TARGET_DIR = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')) + "/deepseek_data")
TARGET = os.path.join(TARGET_DIR, "meds_donem3_sorulari_duzeltilmis.jsonl")

MOJI = re.compile(r'[ÃÄÅÂ]|&apos;|&quot;|&#\d+;')

def validate(path):
    rows = []
    bad = 0
    with open(path, encoding='utf-8') as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                bad += 1
                print(f"  SATIR {i} BOZUK: {e}")
    print(f"okunan kayıt: {len(rows)} | bozuk satır: {bad}")
    return rows

def check(rows):
    prob = Counter()
    for r in rows:
        if not r.get('id'):
            prob['id_yok'] += 1
        o = r.get('options') or []
        if len(o) != 5 or [x.get('key') for x in o] != list('ABCDE'):
            prob['sik_yapisi'] += 1
        if sum(1 for x in o if x.get('isCorrect')) != 1:
            prob['dogru_sik_sayisi'] += 1
        if r.get('correctAnswer') not in [x.get('key') for x in o]:
            prob['cevap_uyumsuz'] += 1
        if len(r.get('stem') or '') < 20:
            prob['kisa_kok'] += 1
        if len(r.get('explanation') or '') < 250:
            prob['kisa_aciklama'] += 1
        if MOJI.search((r.get('stem') or '') + (r.get('explanation') or '') +
                       (r.get('topic') or '') + (r.get('optionsText') or '')):
            prob['mojibake'] += 1
        if not r.get('embeddingText'):
            prob['bos_embedding'] += 1
        if not r.get('discipline'):
            prob['brans_yok'] += 1
        if not r.get('topic'):
            prob['konu_yok'] += 1
    return prob

def main():
    if not os.path.exists(SRC):
        print("KAYNAK YOK:", SRC); sys.exit(1)
    print("kaynak:", SRC, "%.2f MB" % (os.path.getsize(SRC) / 1e6))
    rows = validate(SRC)
    prob = check(rows)
    print("\n### BÜTÜNLÜK ###")
    print("sorunlar:", dict(prob) if prob else "yok")
    print("tekil id:", len(set(r['id'] for r in rows)), "/", len(rows))

    os.makedirs(TARGET_DIR, exist_ok=True)
    data = open(SRC, 'rb').read()
    with open(TARGET, 'wb') as fh:
        fh.write(data)
    # doğrulama: byte-identical + tekrar parse
    back = open(TARGET, 'rb').read()
    print("\n### YAZMA DOĞRULAMA ###")
    print("hedef:", TARGET)
    print("boyut: %.2f MB" % (len(back) / 1e6))
    print("md5 eşit:", hashlib.md5(data).hexdigest() == hashlib.md5(back).hexdigest())
    print("byte eşit:", data == back)
    rows2 = validate(TARGET)
    print("yeniden parse edilen kayıt:", len(rows2))
    print("satır sayısı:", len(back.split(b'\n')) - 1)
    st = Counter(r['verification']['status'] for r in rows2)
    print("status:", st.most_common())
    print("kanıtlı soru:", sum(1 for r in rows2 if r.get('lectureMatches')))
    print("ortalama açıklama:", round(sum(len(r['explanation']) for r in rows2) / len(rows2)))
    print("\nTAMAM" if (data == back and len(rows2) == len(rows) and not prob) else "\nDİKKAT: kontrol gerekli")

if __name__ == "__main__":
    main()
