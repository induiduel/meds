#!/usr/bin/env python3
"""Güncelleme ve geliştirme günlüğü üretici → src/data/surum_gunlugu.json (/guncellemeler ekranı).

Kaynak: git geçmişi.
  - Sürüm = guncelleme_notu.json'da "onem" sayısının arttığı commit. Öğrenci notu (baslik + maddeler) o commit'teki
    dosyadan okunur; isteğe bağlı "eklenen" / "degisen" / "silinen" / "duzeltilen" dizileri varsa sınıflama onlardan,
    yoksa madde metninden anahtar kelimeyle yapılır.
  - Geliştirme notları = önceki sürümden bu sürüme kadar olan commit konuları (feat/fix/kaldır önekine göre sınıflı)
    + src/ altındaki eklenen / silinen / değişen dosya sayıları.
  - İlk sürümden önceki commit'ler gün gün "ara sürüm" olarak listelenir.
Git yoksa (ör. Oracle) var olan dosya korunur, çıkış 0. `npm run build` öncesinde kendiliğinden çalışır.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / 'src/data/surum_gunlugu.json'
NOT = 'guncelleme_notu.json'
ELLE = KOK / 'scripts/surum_gunlugu_turler.json'   # madde metni → tür (elle gözden geçirilmiş; öncelikli)
TURLER = ('eklenen', 'degisen', 'duzeltilen', 'silinen')


try: ELLE_TUR: dict[str, str] = json.loads(ELLE.read_text(encoding='utf-8'))
except Exception: ELLE_TUR = {}


def git(*a: str) -> str:
    return subprocess.run(['git', '-C', str(KOK), *a], capture_output=True, text=True, check=True).stdout


def madde_turu(m: str) -> str:
    if m in ELLE_TUR: return ELLE_TUR[m]
    s = m.lower()
    if re.search(r'kaldırıldı|silindi|çıkarıldı|artık gösterilmiyor|kaldırdık', s): return 'silinen'
    if re.search(r'düzelt|giderildi|hata|sorun|çökme|donmuyor|kaymıyor|taşm|sıkışmıyor|binmiyor|önlendi', s): return 'duzeltilen'
    if re.search(r'^yeni\b|eklendi|geldi\b|getirildi|kullanıma sunuldu|yayına alındı|entegre edildi|dahil edildi', s): return 'eklenen'
    return 'degisen'


def commit_turu(konu: str) -> str:
    s = konu.lower()
    if re.match(r'(fix|hotfix)\b', s) or re.search(r'düzelt|duzelt|giderildi|\bfix\b', s): return 'duzeltilen'
    if re.search(r'\b(remove|kaldir|kaldır|sil)\w*', s): return 'silinen'
    if re.match(r'feat\b', s) or re.search(r'\byeni\b|eklendi|\bekle\b', s): return 'eklenen'
    return 'degisen'


def temiz_konu(konu: str) -> str:
    konu = re.sub(r'^\w+(\([^)]*\))?!?:\s*', '', konu)           # feat(x): öneki
    konu = re.sub(r'[;,]?\s*\(?onem:?\s*\d+\)?\s*$', '', konu, flags=re.I)
    konu = re.sub(r'\s*\(v\d+\)\s*$', '', konu)
    return konu.strip(' ;,') or konu


def dosya_ozeti(eski: str | None, yeni: str) -> dict:
    aralik = [f'{eski}..{yeni}'] if eski else [f'{yeni}~1', yeni] if git('rev-list', '--count', yeni).strip() != '1' else []
    if not aralik: return {'eklenen': 0, 'silinen': 0, 'degisen': 0, 'ornekEklenen': [], 'ornekSilinen': []}
    sat = git('diff', '--name-status', '--no-renames', *aralik, '--', 'src', 'server.ts', 'scripts').splitlines()
    ek, sil, deg = [], [], 0
    for s in sat:
        p = s.split('\t')
        if len(p) < 2: continue
        if p[0] == 'A': ek.append(p[1])
        elif p[0] == 'D': sil.append(p[1])
        else: deg += 1
    kod = lambda xs: [x for x in xs if re.search(r'\.(tsx?|css|py|mjs|sh)$', x)][:6]
    return {'eklenen': len(ek), 'silinen': len(sil), 'degisen': deg, 'ornekEklenen': kod(ek), 'ornekSilinen': kod(sil)}


def notlar(commitler: list[tuple[str, str, str]]) -> list[dict]:
    return [{'tur': commit_turu(k), 'metin': temiz_konu(k), 'commit': h, 'tarih': t} for h, t, k in commitler]


def main() -> int:
    try:
        sat = git('log', '--reverse', '--format=%h\x1f%cI\x1f%s').splitlines()
    except Exception as e:
        print(f'surum_gunlugu: git yok, dosya korunuyor ({e.__class__.__name__})'); return 0
    commitler = [tuple(s.split('\x1f', 2)) for s in sat]
    not_commitleri = set(git('log', '--format=%h', '--', NOT).split())

    surumler, bekleyen, son_onem, son_hash = [], [], 0, None
    ara: dict[str, list] = {}
    for h, t, k in commitler:
        bekleyen.append((h, t, k))
        if h not in not_commitleri: continue
        try: n = json.loads(git('show', f'{h}:{NOT}'))
        except Exception: continue
        onem = int(n.get('onem') or 0)
        if onem <= son_onem: continue
        if not surumler:                                   # ilk sürüm öncesi → günlük ara sürümler
            for bh, bt, bk in bekleyen[:-1]: ara.setdefault(bt[:10], []).append((bh, bt, bk))
            bekleyen = bekleyen[-1:]
        maddeler = [str(m) for m in n.get('maddeler') or []]
        ogrenci = {tur: [str(x) for x in n.get(tur) or []] for tur in TURLER}
        if not any(ogrenci.values()):
            for m in maddeler: ogrenci[madde_turu(m)].append(m)
        surumler.append({
            'surum': onem, 'tarih': t, 'commit': h, 'baslik': n.get('baslik') or f'Sürüm {onem}',
            'ogrenci': ogrenci, 'gelistirme': notlar(bekleyen), 'dosyalar': dosya_ozeti(son_hash, h),
        })
        son_onem, son_hash, bekleyen = onem, h, []

    yayinlanmamis = notlar(bekleyen)
    ara_surumler = [{'gun': g, 'gelistirme': notlar(cs)} for g, cs in sorted(ara.items(), reverse=True)]
    surumler.reverse()
    veri = {'uretildi': commitler[-1][1] if commitler else None, 'surumler': surumler,
            'yayinlanmamis': list(reversed(yayinlanmamis)), 'oncesi': ara_surumler}
    CIKTI.write_text(json.dumps(veri, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(f'surum_gunlugu: {len(surumler)} sürüm, {len(yayinlanmamis)} yayınlanmamış, {len(ara_surumler)} ara gün → {CIKTI.relative_to(KOK)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
