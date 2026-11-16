import json

with open('src/data/study_questions/index.json', encoding='utf-8') as f:
    idx = json.load(f)

print('Index totalQuestions:', idx['totalQuestions'])
print('Index totalChunks:', len(idx['chunks']))
for c in idx['chunks']:
    with open('src/data/study_questions/' + c['filename'], encoding='utf-8') as cf:
        cd = json.load(cf)
        print(f"{c['filename']}: {len(cd)} questions (manifest count: {c['questionCount']})")
