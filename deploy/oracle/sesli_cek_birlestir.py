#!/usr/bin/env python3
"""sesli_cek.sh yardımcısı: Oracle'daki sesli ders kayıt defterini yereldekiyle anahtar bazında birleştirir.

  dersler.json  liste [{key, …}]      → Oracle'daki kayıt kazanır; yalnız yereldeki kayıt sona eklenir (silinmez)
  kayit.json    {key: [varyant…]}     → ders başına varyantlar `id` ile birleşir; aynı id'de Oracle kazanır

Kullanım: sesli_cek_birlestir.py <dersler.json|kayit.json> <yerel yol> <oracle kopyası> [--kuru]
Yazım atomik (tmp + os.replace); içerik değişmediyse dosyaya dokunulmaz (mtime/git diff oluşmaz).
"""
import json, os, sys
from pathlib import Path


def birlestir_dersler(yerel, oracle):
    o_keys = {x["key"] for x in oracle}
    return list(oracle) + [x for x in yerel if x.get("key") not in o_keys]


def birlestir_kayit(yerel, oracle):
    out = {}
    for key in list(oracle) + [k for k in yerel if k not in oracle]:
        o, y = oracle.get(key) or [], yerel.get(key) or []
        o_id = {v.get("id") for v in o}
        out[key] = list(o) + [v for v in y if v.get("id") not in o_id]
    return out


def main():
    ad, yerel_yol, oracle_yol = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    kuru = "--kuru" in sys.argv
    oracle = json.loads(oracle_yol.read_text(encoding="utf-8"))
    ham = yerel_yol.read_text(encoding="utf-8") if yerel_yol.exists() else ""
    yerel = json.loads(ham) if ham.strip() else ([] if ad == "dersler.json" else {})
    yeni = birlestir_dersler(yerel, oracle) if ad == "dersler.json" else birlestir_kayit(yerel, oracle)
    if yeni == yerel:
        print(f"    {yerel_yol.parent.name}/{ad}: güncel")
        return
    if ad == "dersler.json":
        eklenen = len({x['key'] for x in yeni} - {x.get('key') for x in yerel})
    else:
        eklenen = sum(len(v) for v in yeni.values()) - sum(len(v) for v in yerel.values())
    print(f"    {yerel_yol.parent.name}/{ad}: +{eklenen} kayıt" + (" (KURU)" if kuru else ""))
    if kuru:
        return
    tmp = yerel_yol.with_suffix(".cek.tmp")
    tmp.write_text(json.dumps(yeni, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, yerel_yol)


if __name__ == "__main__":
    main()
