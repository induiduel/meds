"""Öğrenci notu PDF'ini okuma için parçalar (200 dpi, 3×2 örtüşmeli parça + Tesseract yardımcı OCR + küçük genel görünüm).

  python3 scripts/ogrenci_onem/parcala.py <not.pdf> <ad> <çalışma klasörü>/hr/<ad>
Okuma yönergesi: scripts/ogrenci_onem/OKUMA_YONERGESI.md.
"""
import sys, os, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
src, name, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
subprocess.run(["pdftoppm","-r","200","-png",src,f"{out}/full"],check=True)
for f in sorted(os.listdir(out)):
    if not f.startswith("full-"): continue
    p=int(f.split("-")[1].split(".")[0])
    im=Image.open(f"{out}/{f}").convert("RGB")
    W,H=im.size; cw,ch=W//3,H//2; ov=60
    for r in range(2):
        for c in range(3):
            box=(max(0,c*cw-ov),max(0,r*ch-ov),min(W,(c+1)*cw+ov),min(H,(r+1)*ch+ov))
            t=im.crop(box); t.save(f"{out}/s{p:02d}_r{r+1}c{c+1}.png")
            txt=subprocess.run(["tesseract",f"{out}/s{p:02d}_r{r+1}c{c+1}.png","-","-l","tur","--psm","3"],capture_output=True,text=True).stdout
            open(f"{out}/s{p:02d}_r{r+1}c{c+1}.ocr.txt","w").write(txt)
    im.resize((W//2,H//2)).save(f"{out}/s{p:02d}_genel.png"); os.remove(f"{out}/{f}")
print(name,"ok")
