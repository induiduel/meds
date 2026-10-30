"""Kullanım:
  python3 -I ara.py banka "<metin>" [--ders Psikiyatri] [-n 5]   -> çıkmış bankasında en benzer sorular (id, yıl, kurul, kök, şıklar, doğru)
  python3 -I ara.py y25 "<metin>" [--ders psk|noro|tbg|ftr|hepsi] [-n 5] -> 2025-26 arşiv slaytlarında en benzer sayfalar (anahtar/sNN + satır)
  python3 -I ara.py y26 "<metin>" -> 2026-27 orijinal PDF sayfaları (k2-01,02,05,08)
"""
import json, re, sys, os, unicodedata
S=os.environ.get("OGRENCI_ONEM_CALISMA", os.getcwd())  # y25txt/ ve y26txt/ (sayfa sayfa pdftotext) bu klasörde
def norm(t):
    t=unicodedata.normalize("NFC",t).replace("İ","i").replace("I","ı").lower()
    return re.sub(r"[^0-9a-zçğıöşüâîû ]"," ",t)
def tok(t): return [w for w in norm(t).split() if len(w)>2]
def skor(q,t):
    a=set(tok(q)); b=set(tok(t))
    if not a: return 0
    # kısmi kök eşleşmesi (ilk 5 harf)
    bk={w[:5] for w in b}
    return sum(1 for w in a if w in b or w[:5] in bk)/len(a)
args=sys.argv[1:]; kip=args[0]; q=args[1]
n=int(args[args.index("-n")+1]) if "-n" in args else 5
ders=args[args.index("--ders")+1] if "--ders" in args else None
if kip=="banka":
    d=json.load(open("/home/indu/medsor/meds/src/data/pastQuestions.json"))
    r=[]
    for x in d:
        if not x.get("isPastExam"): continue
        if ders and (x.get("discipline") or "")!=ders: continue
        txt=(x.get("stem") or "")+" "+" ".join(o.get("text","") for o in x.get("options") or [])
        r.append((skor(q,txt),x))
    r.sort(key=lambda z:-z[0])
    for s,x in r[:n]:
        dog=[o.get("key")+") "+o.get("text","") for o in x.get("options") or [] if o.get("isCorrect")]
        print(f"[{s:.2f}] id={x['id']} yil={x.get('examYear')} kurul={x.get('kurul')} ders={x.get('discipline')} konu={x.get('topic')} gizli={x.get('hidden') or x.get('mergedInto') or ''}")
        print("   KÖK:",(x.get("stem") or "")[:300])
        print("   ŞIK:"," | ".join(o.get("key","")+") "+o.get("text","")[:60] for o in x.get("options") or []))
        print("   DOĞRU:",dog, "correctAnswer=",x.get("correctAnswer"))
else:
    kok=f"{S}/y25txt" if kip=="y25" else f"{S}/y26txt"
    pref={"psk":["psikiyatri","sizofren","bipolar","depres","kisilik","okb","travma","anksiyete","panik","fobik","damgalama","intihar","dikkat","disa-atim","norogelisim","konsultasyon","psikosomatik","cinsel","semiyoloji","psikiyatrik-tedavi"],
          "noro":["norolojik","bilinc","bas-agri","periferik","bazal","epilepsi","medulla-spinalis-hast","felc","kraniyal","norolojik-muayene"],
          "tbg":["genetig","davranis","psikiyatrik-hastaliklar-ve-genetik"],"ftr":["rehabilitasyon"]}
    r=[]
    for k in sorted(os.listdir(kok)):
        if ders and ders!="hepsi" and kip=="y25" and not any(p in k for p in pref[ders]): continue
        for f in sorted(os.listdir(f"{kok}/{k}")):
            t=open(f"{kok}/{k}/{f}",errors="ignore").read()
            r.append((skor(q,t),k,f,t))
    r.sort(key=lambda z:-z[0])
    for s,k,f,t in r[:n]:
        sat=[l.strip() for l in t.splitlines() if l.strip()]
        best=sorted(sat,key=lambda l:-skor(q,l))[:2]
        print(f"[{s:.2f}] {k}/{f}  ::  "+" // ".join(b[:120] for b in best))
