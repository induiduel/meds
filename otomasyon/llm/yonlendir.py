"""Maliyet katmanlı yönlendirici (ICERIK_MOTORU_V3.md §1.2).

Sıra: görevin `katmanlar` listesi (2026-10-24'ten beri ["A"]). B (betik) katmanı görev modülünün `betik()` işlevidir; yoksa atlanır.
  A — ajan CLI'leri (kullanıcı kararı 2026-10-24): etkin PROFİL (butce.json `profiller`; MEDS_AJAN_PROFIL) sırası —
      karma (OpenCode, yetmezse yerel Claude), opencode, antigravity, claude, commandcode; her profilde yazar ≠ denetçi
      model ailesi.
      (butce.json `ajanlar`: komut, modeller, günlük tavan; sayaç meds_temp/state/ajan_butce.json). Boş klasörde, salt okunur,
      istem stdin'den. Claude bu katmanda da C bütçesini kullanır. Denetimde yazar ajan `haric_aile` ile atlanır.
  Ü — ücretsiz bulut: scripts/altyapi/agents/cloud_llm.py zinciri AİLE AİLE (gemini, groq, zen, openrouter). Her ailede ilk
      cevap + en çok `deneme.Ü` düzeltme turu (hata listesiyle). Aile sırası görevin `yazar_aileleri`; işin meta'sındaki
      `haric_aile` (denetimde yazarın ailesi) atlanır → yazar ≠ denetçi.
  C — Claude (`claude -p`, araçsız, stdin): günlük bütçe (butce.json, sayaç meds_temp/state/claude_butce.json);
      bütçe yoksa iş `bekliyor_butce` olur, sessizce düşmez.
  elle — paket.md insan eliyle herhangi bir LLM'e verilir; cevap `cevap.txt`'ye konur, `gorev.py derle` ile sürer.
Önbellek: aynı paket + aynı aile + aynı tur istemi ikinci kez modele gitmez (meds_temp/llm_onbellek/<gorev>/); anahtar
  2026-11-16'dan beri şablon sürümü + rol + istem karması ("v2-…"); eski anahtarlı dosyalar geriye dönük okunur.
Rol (2026-11-16, varsayılan AÇIK, `MEDS_HAT_ROL=0` kapatır): denetim → model_sec.ajan_model("denetci") (yazardan ayrı aile),
  kısa/biçimsel işler → "hizli" (cekirdek.rol_sec).
Kimlik bazlı yama (`MEDS_HAT_YAMA=1`, varsayılan KAPALI): denetçi bulgusu düzeltmesinde yalnız bulgudaki kimlikler gider.
Çıkış kodları: 0 doğrulandı · 1 reddedildi (tüm katmanlar denendi) · 3 elle bekliyor · 4 bütçe bekliyor · 5 hiçbir model yanıt vermedi.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from . import cekirdek as c

AILELER = ("gemini", "groq", "zen", "openrouter")
SISTEM = ("Sen tıp fakültesi Dönem 3 için içerik hazırlayan titiz bir yazarsın. Yalnız verilen GİRDİ'deki bilgiyi "
          "kullanırsın, KURALLAR'a harfiyen uyarsın ve yalnız istenen ÇIKTI BİÇİMİ'ni yazarsın.")


# ── bütçe ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def _butce() -> dict:
    return (c.oku(c.LLM / "butce.json", {}) or {}).get("claude", {})


def _sayac() -> dict:
    p = c.TEMP / "state" / "claude_butce.json"
    s = c.oku(p, {}) or {}
    bugun = time.strftime("%Y-%m-%d")
    return s if s.get("gun") == bugun else {"gun": bugun, "cagri": 0, "dakika": 0.0}


def profil() -> tuple[str, dict]:
    """Etkin ajan profili (butce.json `profiller`): MEDS_AJAN_PROFIL > etkin_profil. Hattın tamamı tek bir ajanla
    (opencode / antigravity / claude / commandcode) ya da 'karma' (OpenCode, yetmezse Claude) yürüyebilir (2026-10-24)."""
    b = c.oku(c.LLM / "butce.json", {}) or {}
    ad = os.environ.get("MEDS_AJAN_PROFIL") or b.get("etkin_profil") or "karma"
    P = b.get("profiller", {})
    if ad not in P or ad == "aciklama":
        raise SystemExit(f"bilinmeyen ajan profili: {ad} (seçenekler: {', '.join(k for k in P if k != 'aciklama')})")
    return ad, P[ad]


def _claudesuz(ajanlar: list[str]) -> list[str]:
    return [a for a in ajanlar if not (a.startswith("claude") and os.environ.get("MEDS_AJAN_CLAUDE") == "0")]


def claude_kalan() -> int:
    tavan = _butce().get("profil_gunluk_cagri" if profil()[0] == "claude" else "gunluk_cagri", 0)
    return max(0, int(tavan) - int(_sayac()["cagri"]))


def _sayac_artir(sure_sn: float):
    s = _sayac()
    s["cagri"] += 1
    s["dakika"] = round(s["dakika"] + sure_sn / 60, 2)
    c.yaz(c.TEMP / "state" / "claude_butce.json", s)


def _ajan_ayar() -> dict:
    return (c.oku(c.LLM / "butce.json", {}) or {}).get("ajanlar", {})


def _ajan_sayac() -> dict:
    s = c.oku(c.TEMP / "state" / "ajan_butce.json", {}) or {}
    bugun = time.strftime("%Y-%m-%d")
    return s if s.get("gun") == bugun else {"gun": bugun, "cagri": {}, "dakika": {}}


def ajan_kalan(ad: str) -> int:
    if ad.startswith("claude"):
        return claude_kalan()
    return max(0, int(_ajan_ayar().get(ad, {}).get("gunluk_cagri", 0)) - int(_ajan_sayac()["cagri"].get(ad, 0)))


def _ajan_sayac_artir(ad: str, sure_sn: float):
    s = _ajan_sayac()
    s["cagri"][ad] = s["cagri"].get(ad, 0) + 1
    s["dakika"][ad] = round(s["dakika"].get(ad, 0) + sure_sn / 60, 2)
    c.yaz(c.TEMP / "state" / "ajan_butce.json", s)


_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def _rol_modelleri(modeller: list, rol: str) -> list:
    """Rol bağlama (2026-11-16): denetçide yazarın ailesindeki modeller atılır (boş kalırsa ajan_model('denetci')),
    hızlıda ajan_model('hizli') başa alınır. Rol 'yazar' ise liste aynen döner (eski davranış)."""
    from . import opendesign as od
    from .model_sec import ajan_model, aile
    if rol == "denetci":
        yazar_aile = aile(ajan_model("yazar"))
        kalan = [m for m in modeller if od.aile(m) != yazar_aile]
        return kalan or [od.model_id(ajan_model("denetci"))]
    if rol == "hizli":
        h = od.model_id(ajan_model("hizli"))
        return [h] + [m for m in modeller if m != h]
    return list(modeller)


def _opendesign(istem: str, ad: str, rol: str = "yazar") -> tuple[str | None, str | None]:
    """A katmanı — OpenDesign geçidi (2026-11-13): CLI yok, `otomasyon/llm/opendesign.py` doğrudan `/v1/messages`
    gönderir. Yerel köprü ayaktaysa oraya, değilse genel geçide. Modeller `butce.json` › `ajanlar.<ad>.modeller`
    sırasıyla denenir (yazar deepseek, denetçi glm/gpt ailesi). Günlük tavan `gunluk_cagri`."""
    from . import opendesign as od
    a = _ajan_ayar().get(ad) or {}
    if a.get("kapali"):
        return None, None
    if ajan_kalan(ad) <= 0:
        return None, "butce"
    modeller = _rol_modelleri(a.get("modeller") or [od.VARSAYILAN_MODEL], rol)
    for model in modeller:
        t0 = time.time()
        try:
            cevap = od.sohbet(istem, sistem=SISTEM, model=model,
                              max_tokens=int(a.get("max_cikti", 4096)),
                              sicaklik=float(a.get("sicaklik", 0.2)),
                              zaman_asimi=float(a.get("zaman_asimi_sn", 900)),
                              gunluk=lambda m: c.gunluk(olay="model_uyari", ajan=ad, mesaj=m))
        except od.GecitHatasi as e:
            c.gunluk(olay="ajan_hata", ajan=ad, model=model, hata=str(e)[:300])
            continue
        _ajan_sayac_artir(ad, time.time() - t0)
        if not cevap:
            continue
        return cevap, f"{ad}:{od.model_id(model)}"
    return None, None


def _ajan(ad: str, istem: str, rol: str = "yazar") -> tuple[str | None, str | None]:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from llm_kilit import serbest  # LLM kilidi 2026-10-27
    if not serbest():
        return None, "kilit"
    """A katmanı: ajan CLI'si (OpenCode, Command Code, Antigravity; Claude ayrı bütçeyle `_claude`). İstem stdin'den,
    boş bir çalışma klasöründe, salt okunur kipte; cevap metni döner (derleyicinin json_cikar'ı önsöz/ANSI'ye hoşgörülü).
    Ajanın `modeller` listesi sırayla denenir (ilk dolu cevap). Günlük tavan butce.json'dan; dolunca (None, "butce")."""
    if ad.startswith("opendesign"):
        return _opendesign(istem, ad, rol)
    if ad.startswith("claude"):
        model = (_ajan_ayar().get(ad) or {}).get("claude_model")
        if rol in ("denetci", "hizli"):          # rol bağlama: claude_alt (sonnet → deepseek) denetçide yazarla aynı aileydi
            from .model_sec import ajan_model
            model = ajan_model(rol)
        return _claude(istem, model, rol)
    a = _ajan_ayar().get(ad)
    if not a or not a.get("komut") or a.get("kapali"):
        return None, None
    if ajan_kalan(ad) <= 0:
        return None, "butce"
    cwd = c.TEMP / "ajan_cwd"
    cwd.mkdir(parents=True, exist_ok=True)
    tam = SISTEM + "\n\n" + istem
    arg_ile = any("{istem}" in x for x in a["komut"])        # stdin okumayan ajan (agy): istem argümanda
    if arg_ile and len(tam.encode()) > 120_000:               # Linux tek argüman sınırı 128 KB
        c.gunluk(olay="ajan_hata", ajan=ad, hata=f"istem {len(tam.encode())} bayt — argüman sınırı, ajan atlandı")
        return None, None
    for model in a.get("modeller") or [None]:
        kom = [x.replace("{model}", model or "").replace("{istem}", tam) for x in a["komut"]]
        if "{model}" in " ".join(a["komut"]) and not model:
            continue
        if model and a.get("model_bayrak"):
            kom += [x.replace("{model}", model) for x in a["model_bayrak"]]
        t0 = time.time()
        try:
            r = subprocess.run(kom, input="" if arg_ile else tam, capture_output=True, text=True,
                               timeout=int(a.get("zaman_asimi_sn", 900)), cwd=str(cwd),
                               env={**os.environ, "CUDA_VISIBLE_DEVICES": "", "NO_COLOR": "1"})
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            c.gunluk(olay="ajan_hata", ajan=ad, model=model, hata=repr(e)[:300])
            continue
        _ajan_sayac_artir(ad, time.time() - t0)
        cikti = _ANSI.sub("", r.stdout or "").strip()
        if r.returncode != 0 or not cikti:
            c.gunluk(olay="ajan_hata", ajan=ad, model=model, kod=r.returncode, hata=(r.stderr or cikti)[-400:])
            continue
        return cikti, f"{ad}:{model or 'varsayilan'}"
    return None, None


# ── çağrılar ──────────────────────────────────────────────────────────────────────────────────────────────────────
def _gorsel(istem: str, aile: str, k: dict, gorsel: str) -> tuple[str | None, str | None]:
    """Görsel görev (ör. som_sec): şimdilik yalnız Gemini görsel zinciri (cloud_llm.vision_ocr, düşünme kapalı, sıcaklık 0)."""
    import cloud_llm
    if aile != "gemini":
        return None, None
    p = c.Path(gorsel)
    mime = {"webp": "image/webp", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(p.suffix[1:].lower(), "image/png")
    r = cloud_llm.vision_ocr(p.read_bytes(), prompt=SISTEM + "\n\n" + istem, timeout=int(k.get("zaman_asimi_sn", 120)),
                             log=lambda m: c.gunluk(olay="model_uyari", aile=aile, mesaj=m), mime=mime)
    return (r or None), cloud_llm.last_model["ad"]


def _ucretsiz(istem: str, aile: str, k: dict) -> tuple[str | None, str | None]:
    import cloud_llm  # scripts/altyapi/agents (çekirdek yol ekler)
    modeller = [m for m in cloud_llm.chain() if m.split(":", 1)[0] == aile]
    if not modeller:
        return None, None
    json_mu = k.get("cikti") == "json"
    r = cloud_llm.chat(istem, system=SISTEM, as_json=json_mu, max_tokens=int(k.get("max_cikti", 4096)),
                       temperature=float(k.get("sicaklik", 0.2)), timeout=int(k.get("zaman_asimi_sn", 180)),
                       models=modeller, log=lambda m: c.gunluk(olay="model_uyari", aile=aile, mesaj=m),
                       dusunme=k.get("gemini_dusunme", 2048) if aile == "gemini" else None, json_ham=True)
    if r is None:
        return None, None
    import json
    return (json.dumps(r, ensure_ascii=False) if not isinstance(r, str) else r), cloud_llm.last_model["ad"]


def _claude(istem: str, model: str | None = None, rol: str = "yazar") -> tuple[str | None, str | None]:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from llm_kilit import serbest  # LLM kilidi 2026-10-27
    if not serbest():
        return None, "kilit"
    b = _butce()
    if claude_kalan() <= 0:
        return None, "butce"
    model = model or b.get("model", "claude-opus-5-5")
    kom = ["claude-gecit", "-p", "--model", model, "--append-system-prompt", SISTEM,
           "--disallowedTools", "Bash,Edit,Write,Read,Glob,Grep,WebFetch,WebSearch,NotebookEdit,Task"]
    t0 = time.time()
    try:
        r = subprocess.run(kom, input=istem, capture_output=True, text=True, timeout=int(b.get("zaman_asimi_sn", 900)),
                           cwd=str(c.TEMP), env={**os.environ, "CUDA_VISIBLE_DEVICES": ""})
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        c.gunluk(olay="claude_hata", hata=repr(e))
        return _opendesign(istem, "opendesign", rol)      # 2026-11-13: CLI yoksa doğrudan geçit
    _sayac_artir(time.time() - t0)
    if r.returncode != 0 or not r.stdout.strip():
        c.gunluk(olay="claude_hata", kod=r.returncode, hata=r.stderr[-400:])
        return _opendesign(istem, "opendesign", rol)      # 2026-11-13: köprü/CLI düştüyse doğrudan geçit
    return r.stdout.strip(), f"claude:{model}"


def onbellek_anahtari(katman: str, aile: str, istem: str, rol: str = "yazar", gorsel_iz: str = "") -> str:
    """Yeni önbellek anahtarı: şablon sürümü + rol + katman/aile + istem karması (rol değişince başka model → başka kayıt)."""
    return "v2-" + c.sha(f"{c.PAKET_SURUM}|{rol}|{katman}|{aile}|{c.sha(istem, 40)}|{gorsel_iz}", 20)


def _onbellek_oku(gorev: str, anahtarlar: list[str]):
    for a in anahtarlar:
        p = c.ONBELLEK / gorev / f"{a}.txt"
        if p.exists():
            satirlar = p.read_text(encoding="utf-8").split("\n", 1)
            return (satirlar[1] if len(satirlar) > 1 else ""), satirlar[0] + " (önbellek)"
    return None


def _cagir(katman: str, aile: str, istem: str, gorev: str, k: dict, gorsel: str | None = None,
           rol: str = "yazar") -> tuple[str | None, str | None]:
    gorsel_iz = c.sha(c.Path(gorsel).read_bytes().hex(), 12) if gorsel else ""
    yeni = onbellek_anahtari(katman, aile, istem, rol, gorsel_iz)
    eski = c.sha(f"{katman}|{aile}|{istem}|{gorsel_iz}", 20)          # 2026-11-16 öncesi anahtar (geriye dönük okunur)
    # eski anahtar rolsüzdü: yalnız rol 'yazar' iken (o zamanki tek davranış) okunur, denetçi başka modelle çağrılmalı
    bulunan = _onbellek_oku(gorev, [yeni] + ([eski] if rol == "yazar" else []))
    if bulunan:
        return bulunan
    p = c.ONBELLEK / gorev / f"{yeni}.txt"
    if gorsel:
        cevap, model = _gorsel(istem, aile, k, gorsel) if katman == "Ü" else (None, None)
    elif katman == "A":
        cevap, model = _ajan(aile, istem, rol)
    else:
        cevap, model = _ucretsiz(istem, aile, k) if katman == "Ü" else _claude(istem, None, rol)
    if cevap is not None:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"{model}\n{cevap}", encoding="utf-8")
    return cevap, model


def duzeltme_istemi(paket_md: str, onceki: str, hatalar: list[str], tur: int = 1) -> str:
    h = "\n".join(f"- {x}" for x in hatalar[:40])
    # tur numarası istemi değiştirir: aynı en iyi cevap üstüne tekrar istenince önbellekten aynı kötü cevap dönmesin
    return (f"{paket_md}\n# ÖNCEKİ CEVABIN (düzeltme turu {tur})\n{onceki.strip()}\n\n# BETİK DENETİMİNİN BULDUĞU HATALAR\n{h}\n\n"
            "Bu hataların HEPSİNİ düzelterek cevabı ÇIKTI BİÇİMİ'nde baştan, eksiksiz yaz. Hatasız kısımları AYNEN koru.\n")


# ── kısmi düzeltme: yalnız hatalı ögeler (2026-10-24, çağrı/belirteç tasarrufu) ──────────────────────────────────────
# Görev modülü `OGE = (anahtar, "dict"|"liste")` bildirirse ve bütün hatalar ögelere işaret ediyorsa (`Q2: …`, `N1.cumleler…`,
# önemde `2x99-03: …` / `maddeler[2]…`), düzeltme isteminde öteki ögelerin girdisi (`### Q…` bölümleri) ve önceki cevapları
# GÖNDERİLMEZ. Model yalnız hatalı ögeleri yazar; betik onları önceki en iyi cevabın içine yerleştirir, sonra tam kapı çalışır.
# Parça düzeyi hata (biçim, sayı, dağılım) varsa ya da ögelerin hepsi hatalıysa tam düzeltme istemi kullanılır.
def _oge_hatalari(m, hatalar: list[str], meta: dict):
    if hasattr(m, "oge_hatalari"):
        return m.oge_hatalari(hatalar, meta)
    pat = getattr(m, "OGE_ETIKET", r"[A-Z]\d+")
    out = set()
    for h in hatalar:
        mm = re.match(rf"({pat})\b", h)
        if not mm:
            return None
        out.add(mm.group(1))
    return out


def _girdi_suz(md: str, tut: set[str]) -> str:
    """GİRDİ'deki `### <etiket>` bölümlerinden yalnız `tut`takileri bırakır (öteki başlıklar/bölümler aynen kalır)."""
    out, at = [], False
    for satir in md.split("\n"):
        if satir.startswith("# "):
            at = False
        elif satir.startswith("### "):
            et = re.match(r"###\s+([A-Z]\d+)\b", satir)
            at = bool(et) and et.group(1) not in tut
        if not at:
            out.append(satir)
    return "\n".join(out)


def oturuma_birak(is_id: str, tip: str, log=print) -> int:
    """Profil `oturum`: model çağrılmaz; iş kuyruğa yazılır, durum 'elle_bekliyor' (kod 3). Oturum cevabı yazıp
    `gorev.py derle` (tip 'is') ya da `gorev.py duzeltme-derle` (tip 'duzeltme') ile kapılardan geçirir."""
    d = c.is_klasoru(is_id)
    c.durum_yaz(is_id, durum="elle_bekliyor", bekleyen="oturum", bekleyen_tip=tip)
    c.kuyruk_ekle(is_id, tip)
    hedef = d / ("paket.md" if tip == "is" else "duzeltme_paket.md")
    log(f"  oturum kuyruğu: {is_id} → {hedef} (cevap: {d / ('cevap.txt' if tip == 'is' else 'duzeltme_cevap.txt')})")
    return 3


def kismi_duzeltme(m, md: str, onceki: str, hatalar: list[str], tur: int, meta: dict):
    """→ (istem, birlesim) ya da None. birlesim = (anahtar, tip, {etiket: anahtar_ya_da_indis})."""
    spec = getattr(m, "OGE", None)
    if not spec:
        return None
    anahtar, tip = spec
    hedef = _oge_hatalari(m, hatalar, meta)
    j = c.json_cikar(onceki)
    if not hedef or not isinstance(j, dict) or anahtar not in j:
        return None
    ogeler = j[anahtar]
    if tip == "dict":
        if not isinstance(ogeler, dict) or not set(hedef) <= set(ogeler) or len(hedef) >= len(ogeler):
            return None
        yer = {k: k for k in sorted(hedef, key=lambda x: (len(x), x))}
        md_kisa = _girdi_suz(md, set(yer))
    else:
        if not isinstance(ogeler, list) or any(not isinstance(i, int) or not 0 <= i < len(ogeler) for i in hedef) \
                or len(hedef) >= len(ogeler):
            return None
        yer = {f"M{i + 1}": i for i in sorted(hedef)}
        md_kisa = md
    secili = {et: ogeler[i] for et, i in yer.items()}
    hl = "\n".join(f"- {x}" for x in hatalar[:40])
    notu = m.duzeltme_notu(meta) if hasattr(m, "duzeltme_notu") else ""
    ilk = next(iter(secili))
    istem = (f"{md_kisa}\n# ÖNCEKİ CEVABINDAN HATALI ÖGELER (düzeltme turu {tur})\n"
             f"{json.dumps({anahtar: secili}, ensure_ascii=False, indent=1)}\n\n# BETİK DENETİMİNİN BULDUĞU HATALAR\n{hl}\n"
             + (f"{notu}\n" if notu else "") +
             f"\nYalnız bu ögeleri ({', '.join(secili)}) düzelt ve şu biçimde yaz: {{\"{anahtar}\": {{\"{ilk}\": {{…}}, …}}}} — "
             "her öge ÇIKTI BİÇİMİ'ndeki öge yapısında ve eksiksiz. Öteki ögeler kabul edildi; onları YAZMA. "
             "Hatasız kısımları AYNEN koru.\n")
    return istem, (anahtar, tip, yer)


def birlestir_kismi(onceki: str, yeni: str, birlesim) -> str:
    """Kısmi düzeltme cevabını önceki en iyi cevabın içine yerleştirir; ayrıştırılamazsa yeni cevabı aynen döndürür
    (derleyici 'JSON değil' der, düzeltme turu sürer)."""
    anahtar, tip, yer = birlesim
    j, y = c.json_cikar(onceki), c.json_cikar(yeni)
    parca = (y or {}).get(anahtar) if isinstance(y, dict) else None
    if not isinstance(j, dict) or not isinstance(parca, dict):
        return yeni
    for et, i in yer.items():
        if et in parca:
            j[anahtar][i] = parca[et]
    return json.dumps(j, ensure_ascii=False)


# ── değerlendirme (derle + doğrula) ───────────────────────────────────────────────────────────────────────────────
def kapi(is_id: str, cikti: dict) -> list[str]:
    """Derlenmiş çıktının bütün kapıları: görevin kendi `dogrula`sı + ortak kapılar (iç etiket sızıntısı, Türkçe harf
    kaybı). Önceden kabul edilmiş iş yeniden kullanılırken de bu çağrılır (kapı sonradan sıkılaştıysa iş yeniden koşar)."""
    md, pj = c.paket(is_id)
    m = c.modul(pj["gorev"])
    hatalar = m.dogrula(cikti, pj["meta"])
    if getattr(m, "OGRENCI_METNI", True):
        hatalar += c.etiket_sizintisi(cikti, pj["esleme"], md)
        hatalar += c.turkce_katlama(cikti, md)
    return hatalar


def degerlendir(is_id: str, cevap: str) -> tuple[dict | None, list[str]]:
    md, pj = c.paket(is_id)
    m = c.modul(pj["gorev"])
    cikti, hatalar = m.derle(cevap, pj["esleme"], pj["meta"])
    if cikti is not None and getattr(m, "SES_ONAR", False):
        c.ses_onar(cikti)                    # B katmanı: kısaltma/Roma rakamı okunuşu betikle (kapıdan önce)
    if not hatalar and cikti is not None:
        hatalar = kapi(is_id, cikti)
    return cikti, hatalar


def kaydet_sonuc(is_id: str, cikti, hatalar: list[str], **ek):
    d = c.is_klasoru(is_id)
    if cikti is not None:
        c.yaz(d / "cikti.json", cikti)
    c.yaz(d / "rapor.json", {"zaman": c.simdi(), "hata_sayisi": len(hatalar), "hatalar": hatalar, **ek})


# ── ana döngü ─────────────────────────────────────────────────────────────────────────────────────────────────────
def calistir(is_id: str, katman: str | None = None, aile: str | None = None, log=print) -> int:
    md, pj = c.paket(is_id)
    gorev, meta = pj["gorev"], pj["meta"]
    k = c.kayit(gorev)
    m = c.modul(gorev)
    d = c.is_klasoru(is_id)
    rol = c.rol_sec(gorev, k)

    if katman == "elle":
        c.durum_yaz(is_id, durum="elle_bekliyor")
        log(f"elle: {d / 'paket.md'} → herhangi bir LLM'e ver, cevabı {d / 'cevap.txt'} dosyasına koy, sonra:"
            f" gorev.py derle {is_id}")
        return 3

    # B — betik (varsa): modelsiz üretim kapıyı geçerse bitir
    if katman in (None, "B") and hasattr(m, "betik"):
        cevap = m.betik(pj["esleme"], meta)
        if cevap is not None:
            cikti, hatalar = degerlendir(is_id, cevap)
            if not hatalar:
                (d / "cevap.txt").write_text(cevap, encoding="utf-8")
                kaydet_sonuc(is_id, cikti, [], katman="B", model="betik")
                c.durum_yaz(is_id, durum="dogrulandi", katman="B", model="betik", aile="betik")
                return 0
        if katman == "B":
            c.durum_yaz(is_id, durum="reddedildi", neden="betik kapıyı geçemedi")
            return 1

    katmanlar = [katman] if katman in ("A", "Ü", "C") else [x for x in k.get("katmanlar", ["A"]) if x in ("A", "Ü", "C")]
    haric = meta.get("haric_aile")
    deneme = k.get("deneme", {})
    son_hatalar: list[str] = []
    yanit_geldi = butce_yok = False
    n = len(list(d.glob("cevap_*.txt")))
    for kat in katmanlar:
        if kat == "A":       # etkin profilin yazar (denetimde denetçi) sırası; yazar ajanı denetimde atlanır
            pr = profil()[1]
            # "oturum" yazar = denetçi olabilir: denetim paketi oturumda yeni bağlamlı alt ajana verilir (/kuyruk becerisi)
            aileler = [a for a in _claudesuz([aile] if aile else pr["denetci" if gorev == "denetim" else "yazar"])
                       if a != haric or a == "oturum"]
            if aileler and aileler[0] == "oturum":
                return oturuma_birak(is_id, "is", log)
        else:
            aileler = ["claude"] if kat == "C" else [a for a in ([aile] if aile else k.get("yazar_aileleri", AILELER))
                                                     if a != haric]
        if kat == "C" and haric == "claude":
            continue
        for a in aileler:
            istem = md
            en_iyi: tuple[int, str, list] | None = None       # (hata sayısı, cevap, hatalar) — gerileme ilerlemeyi silmesin
            birlesim = None
            for tur in range(1 + int(deneme.get(kat, 1))):
                t0 = time.time()
                cevap, model = _cagir(kat, a, istem, gorev, k, meta.get("gorsel"), rol=rol)
                if cevap is not None and birlesim is not None:
                    (d / f"cevap_{n + 1}_kismi.txt").write_text(cevap, encoding="utf-8")
                    cevap = birlestir_kismi(en_iyi[1], cevap, birlesim)
                if cevap is None:
                    butce_yok |= (model == "butce")
                    log(f"  {kat}/{a}: yanıt yok{' (Claude bütçesi doldu)' if model == 'butce' else ''}")
                    break
                yanit_geldi = True
                n += 1
                (d / f"cevap_{n}.txt").write_text(cevap, encoding="utf-8")
                (d / "cevap.txt").write_text(cevap, encoding="utf-8")
                cikti, hatalar = degerlendir(is_id, cevap)
                c.gunluk(olay="cagri", is_id=is_id, katman=kat, aile=a, model=model, tur=tur,
                         sure_sn=round(time.time() - t0, 1), hata_sayisi=len(hatalar))
                log(f"  {kat}/{model} tur {tur}: {len(hatalar)} HATA")
                if not hatalar:
                    kaydet_sonuc(is_id, cikti, [], katman=kat, model=model, tur=tur)
                    c.durum_yaz(is_id, durum="dogrulandi", katman=kat, aile=a, model=model, cevap_no=n)
                    return 0
                if hasattr(m, "kismi_kabul"):
                    # parti görevleri: geçen öğeler kabul, hatalılar (en çok yarısı) düşer ve bekleyen kalır
                    c2, kalan, dusen = m.kismi_kabul(cikti, hatalar, meta)
                    toplam_oge = len((cikti or {}).get("sorular") or {})
                    if c2 and not kalan and len(dusen) * 2 <= toplam_oge:
                        kaydet_sonuc(is_id, c2, [], katman=kat, model=model, tur=tur, dusen=dusen, dusen_hatalar=hatalar)
                        c.durum_yaz(is_id, durum="dogrulandi", katman=kat, aile=a, model=model, cevap_no=n, kismi=dusen)
                        c.gunluk(olay="kismi_kabul", is_id=is_id, dusen=dusen)
                        return 0
                son_hatalar = hatalar
                kaydet_sonuc(is_id, cikti, hatalar, katman=kat, model=model, tur=tur)
                if en_iyi is None or len(hatalar) <= en_iyi[0]:
                    en_iyi = (len(hatalar), cevap, hatalar)
                kd = kismi_duzeltme(m, md, en_iyi[1], en_iyi[2], tur + 1, meta)
                istem, birlesim = kd if kd else (duzeltme_istemi(md, en_iyi[1], en_iyi[2], tur + 1), None)
                if kd:
                    log(f"  kısmi düzeltme: {', '.join(kd[1][2])} ({len(istem)} karakter, tam istem {len(md) + len(en_iyi[1])})")
    if butce_yok:  # Ü geçemedi ya da yanıt yok; Claude sırası bütçeye takıldı → ertesi gün yeniden (Ü cevapları önbellekte)
        c.durum_yaz(is_id, durum="bekliyor_butce", hatalar=son_hatalar[:20])
        return 4
    if not yanit_geldi:
        c.durum_yaz(is_id, durum="hazir", son_deneme=c.simdi(), neden="hiçbir model yanıt vermedi")
        return 5
    c.durum_yaz(is_id, durum="reddedildi", neden=f"{len(son_hatalar)} HATA", hatalar=son_hatalar[:20])
    return 1


# ── bağımsız denetçi bulgularıyla düzeltme (2026-10-24) ─────────────────────────────────────────────────────────────
def _bulgu_hazirla(is_id: str, bulgular: list[dict]) -> tuple[str, set | None]:
    """Düzeltme istemi: paket (kısmi kabulde yalnız kabul edilen ögelerin girdisi) + önceki çıktı + denetçi bulguları."""
    md, pj = c.paket(is_id)
    m = c.modul(pj["gorev"])
    cikti = c.oku(c.is_klasoru(is_id) / "cikti.json")
    onceki = m.tersine(cikti, pj["esleme"], pj["meta"])
    oge, kabul = getattr(m, "OGE", None), None
    if oge and oge[1] == "dict" and isinstance(cikti.get(oge[0]), list) and cikti[oge[0]] and "_etiket" in cikti[oge[0]][0]:
        kabul = {x["_etiket"] for x in cikti[oge[0]]}
        md = _girdi_suz(md, kabul)
    bl = "\n".join(f"- [{b.get('tur')}] {b.get('yer')}: {b.get('aciklama')} → Öneri: {b.get('oneri')}" for b in bulgular)
    return (f"{md}\n# ÖNCEKİ CEVABIN (betik kapılarından geçti; bağımsız denetçi düzeltme istedi)\n{onceki}\n\n"
            f"# BAĞIMSIZ DENETÇİ BULGULARI\n{bl}\n\nBu bulguların HEPSİNİ GİRDİ'deki ders metnine göre düzelterek cevabı "
            "ÇIKTI BİÇİMİ'nde baştan, eksiksiz yaz. Bulguyla ilgisiz kısımları AYNEN koru. Bir bulgu GİRDİ'ye aykırıysa "
            "GİRDİ'yi esas al.\n"), kabul


# ── kimlik bazlı yama (2026-11-16, `MEDS_HAT_YAMA=1`; varsayılan KAPALI) ─────────────────────────────────────────────
# Denetçi bulgusu düzeltmesinde "cevabı baştan eksiksiz yaz" yerine yalnız bulgunun işaret ettiği kayıtlar (görevin
# OGE_ETIKET şeması: Q<N>, N<N> … — kısa etiket) ve onların GİRDİ dilimi gider; model yalnız o kayıtları döndürür, betik
# önceki çıktıya JSON birleştirmeyle uygular. Birleştirme sonrası kimlik kümesi ve kayıt şeması (alan adları) denetlenir;
# tutmazsa ya da bir bulgu kimliğe işaret etmiyorsa eski tam-yazım yoluna düşülür.
def yama_acik() -> bool:
    return os.environ.get("MEDS_HAT_YAMA") == "1"


def yama_kimlikleri(bulgular: list[dict], gecerli: set[str], desen: str = r"[A-Z]\d+") -> set[str] | None:
    """Her bulgunun `yer`inden (yoksa açıklamasından) önceki çıktıda var olan kimlikler. Kimliksiz bulgu → None (tam yol)."""
    out: set[str] = set()
    for b in bulgular:
        bul = {x for x in re.findall(rf"(?<![\w-])({desen})(?![\w-])", f"{b.get('yer') or ''}") if x in gecerli}
        if not bul:
            bul = {x for x in re.findall(rf"(?<![\w-])({desen})(?![\w-])", f"{b.get('aciklama') or ''}") if x in gecerli}
        if not bul:
            return None
        out |= bul
    return out


def yama_istemi(md: str, onceki: str, bulgular: list[dict], anahtar: str, desen: str = r"[A-Z]\d+"):
    """→ (istem, kimlikler) ya da None. onceki: görevin `tersine` JSON'u ({anahtar: {kimlik: kayıt}})."""
    j = c.json_cikar(onceki)
    if not isinstance(j, dict) or not isinstance(j.get(anahtar), dict) or not j[anahtar]:
        return None
    kim = yama_kimlikleri(bulgular, set(j[anahtar]), desen)
    if not kim or len(kim) >= len(j[anahtar]):
        return None
    sira = sorted(kim, key=lambda x: (len(x), x))
    secili = {k: j[anahtar][k] for k in sira}
    bl = "\n".join(f"- [{b.get('tur')}] {b.get('yer')}: {b.get('aciklama')} → Öneri: {b.get('oneri')}" for b in bulgular)
    istem = (f"{_girdi_suz(md, kim)}\n# ÖNCEKİ CEVABINDAN BULGULU KAYITLAR (betik kapılarından geçti; bağımsız denetçi "
             f"düzeltme istedi)\n{json.dumps({anahtar: secili}, ensure_ascii=False, indent=1)}\n\n# BAĞIMSIZ DENETÇİ "
             f"BULGULARI\n{bl}\n\nYalnız bu kayıtları ({', '.join(sira)}) GİRDİ'deki ders metnine göre düzelt ve şu biçimde "
             f"yaz: {{\"{anahtar}\": {{\"{sira[0]}\": {{…}}, …}}}} — her kayıt aynı alanlarla ve eksiksiz. Öteki kayıtlar "
             "kabul edildi; onları YAZMA. Bulguyla ilgisiz alanları AYNEN koru. Bir bulgu GİRDİ'ye aykırıysa GİRDİ'yi esas al.\n")
    return istem, set(sira)


def yama_birlestir(onceki: str, yeni: str, anahtar: str, kimlikler: set[str]) -> str | None:
    """Yama cevabını önceki çıktıya uygular. Bütünlük: cevap TAM OLARAK istenen kimlikleri içermeli, her kayıt eski kaydın
    alan adlarını korumalı, birleşik çıktının kimlik kümesi değişmemeli. Tutmazsa None (çağıran tam yola düşer)."""
    j, y = c.json_cikar(onceki), c.json_cikar(yeni)
    if not isinstance(j, dict) or not isinstance(j.get(anahtar), dict) or not isinstance(y, dict):
        return None
    parca = y.get(anahtar)
    if not isinstance(parca, dict) or set(parca) != set(kimlikler):
        return None
    once_kim = set(j[anahtar])
    for k, v in parca.items():
        eski = j[anahtar].get(k)
        if not isinstance(v, dict) or not isinstance(eski, dict) or set(v) != set(eski):
            return None
        j[anahtar][k] = v
    if set(j[anahtar]) != once_kim:
        return None
    return json.dumps(j, ensure_ascii=False)


def _yama_dene(is_id: str, bulgular: list[dict], kabul, sira: list[str], katman, gorev: str, k: dict, rol: str, log):
    """Bayrak açıkken tek yama denemesi: kabul → 0, uygulanamaz/geçmez → None (tam yol sürer)."""
    md, pj = c.paket(is_id)
    m = c.modul(gorev)
    oge = getattr(m, "OGE", None)
    if not oge or oge[1] != "dict":
        return None
    cikti = c.oku(c.is_klasoru(is_id) / "cikti.json")
    onceki = m.tersine(cikti, pj["esleme"], pj["meta"])
    if kabul:
        md = _girdi_suz(md, kabul)
    yi = yama_istemi(md, onceki, bulgular, oge[0], getattr(m, "OGE_ETIKET", r"[A-Z]\d+"))
    if not yi:
        log("  yama: bulgular kimliğe bağlanamadı — tam yazım")
        return None
    istem, kim = yi
    d = c.is_klasoru(is_id)
    for a in sira:
        cevap, model = _cagir(katman or "A", a, istem, gorev, k, rol=rol)
        if cevap is None:
            continue
        n = len(list(d.glob("cevap_*.txt"))) + 1
        (d / f"cevap_{n}_yama.txt").write_text(cevap, encoding="utf-8")
        birlesik = yama_birlestir(onceki, cevap, oge[0], kim)
        if birlesik is None:
            log(f"  yama {model}: kimlik/şema bütünlüğü tutmadı — tam yazım"); return None
        yeni, h = bulgu_degerlendir(is_id, birlesik, kabul)
        c.gunluk(olay="bulgu_yama", is_id=is_id, aile=a, model=model, kimlik=sorted(kim), hata_sayisi=len(h))
        log(f"  yama {model} ({', '.join(sorted(kim))}): {len(h)} HATA")
        if not h and yeni is not None:
            bulgu_kabul(is_id, yeni, a, model, 0)
            return 0
        return None
    return None


def bulgu_degerlendir(is_id: str, cevap: str, kabul: set | None) -> tuple[dict | None, list[str]]:
    """Düzeltme cevabı → bütün kapılar (+ kısmi kabulde yalnız kabul edilen ögeler, + görevin `duzeltme_kisiti`)."""
    _, pj = c.paket(is_id)
    m = c.modul(pj["gorev"])
    oge = getattr(m, "OGE", None)
    yeni, h = degerlendir(is_id, cevap)
    if kabul and yeni is not None:               # kısmi kabul edilmiş işte öteki ögeler zaten başka partide
        disari = lambda x: bool(re.match(r"([A-Z]\d+)\b", x)) and re.match(r"([A-Z]\d+)\b", x).group(1) not in kabul  # noqa: E731
        yeni = {**yeni, oge[0]: [x for x in yeni[oge[0]] if x.get("_etiket") in kabul]}
        if h and all(disari(x) for x in h):      # yalnız derleyicinin "kayıt yok" hataları → kapılar şimdi çalışır
            h = kapi(is_id, yeni)
        h = [x for x in h if not disari(x)]
    if yeni is not None and hasattr(m, "duzeltme_kisiti"):
        h += m.duzeltme_kisiti(c.oku(c.is_klasoru(is_id) / "cikti.json"), yeni)
    return yeni, h


def bulgu_kabul(is_id: str, yeni: dict, aile: str, model: str, tur: int = 0) -> None:
    kaydet_sonuc(is_id, yeni, [], katman="A", model=model, tur=tur, denetim_duzeltme=True)
    c.durum_yaz(is_id, durum="dogrulandi", aile=aile, model=model,
                denetim_duzeltme=int(c.durum(is_id).get("denetim_duzeltme", 0)) + 1)


def bulgu_duzelt(is_id: str, bulgular: list[dict], katman: str | None = None, log=print, ajanlar: list[str] | None = None) -> int:
    """Kabul edilmiş bir işin çıktısı, denetçinin bulgularıyla yazara geri gider → yeni cevap → bütün betik kapıları.
    Geçerse çıktı yazılır, durum 'dogrulandi' olur (çağıran yeniden uygular ve yeniden denetletir). Yazar sırası etkin
    profilin `yazar` listesi. Profil `oturum`: düzeltme paketi kuyruğa yazılır (kod 3); oturum `gorev.py duzeltme-derle`
    ile kabul ettirince bir sonraki çağrıda kod 0 döner."""
    _, pj = c.paket(is_id)
    gorev = pj["gorev"]
    k = c.kayit(gorev)
    d = c.is_klasoru(is_id)
    sira = _claudesuz(ajanlar or profil()[1]["yazar"])
    if sira and sira[0] == "oturum":
        if c.durum(is_id).get("oturum_duzeltme") == "hazir":
            c.durum_yaz(is_id, oturum_duzeltme="uygulandi")
            return 0
        taban, _ = _bulgu_hazirla(is_id, bulgular)
        (d / "duzeltme_paket.md").write_text(taban, encoding="utf-8")
        (d / "duzeltme_cevap.txt").unlink(missing_ok=True)
        c.durum_yaz(is_id, oturum_duzeltme="bekliyor")
        return oturuma_birak(is_id, "duzeltme", log)
    taban, kabul = _bulgu_hazirla(is_id, bulgular)
    rol = c.rol_sec(gorev, k)
    if yama_acik() and _yama_dene(is_id, bulgular, kabul, sira, katman, gorev, k, rol, log) == 0:
        return 0
    deneme = int(k.get("deneme", {}).get("A", 2))
    for a in sira:
        istem = taban
        for tur in range(1 + deneme):
            cevap, model = _cagir(katman or "A", a, istem, gorev, k, rol=rol)
            if cevap is None:
                log(f"  bulgu düzeltme {a}: yanıt yok"); break
            n = len(list(d.glob("cevap_*.txt"))) + 1
            (d / f"cevap_{n}_denetim.txt").write_text(cevap, encoding="utf-8")
            yeni, h = bulgu_degerlendir(is_id, cevap, kabul)
            c.gunluk(olay="bulgu_duzeltme", is_id=is_id, aile=a, model=model, tur=tur, hata_sayisi=len(h))
            log(f"  bulgu düzeltme {model} tur {tur}: {len(h)} HATA")
            if not h and yeni is not None:
                bulgu_kabul(is_id, yeni, a, model, tur)
                return 0
            istem = duzeltme_istemi(taban, cevap, h, tur + 1)
    return 1
