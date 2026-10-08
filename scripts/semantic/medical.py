"""Tıbbi sözlük & ICD eşlemesi (TR/EN) — salt okunur kaynaklardan, deterministik.

- ICD-10: `meds_database_v2/reference/icd10.tsv` (kod ↔ ad)
- Kanıtlı sözlük: `evidence_thesaurus/kanitli_sozluk.json`
- Kavram kimlikleri: `concept_ids/kavramlar.json` (QID, UMLS CUI, DOID)
"""
from __future__ import annotations

import json

from . import config, nlp


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def load_icd() -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        for line in config.ICD_TSV.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            code, name = parts[0].strip(), parts[1].strip()
            if code and name:
                out.setdefault(nlp.fold(name), code)
    except Exception:  # noqa: BLE001
        pass
    return out


def load_thesaurus() -> dict[str, dict]:
    data = _read_json(config.THESAURUS) or {}
    out: dict[str, dict] = {}
    for key, val in data.items():
        forms = {key}
        for f in (val.get("esanlamlilar") or []):
            forms.add(nlp.fold(f))
        if val.get("turkce"):
            forms.add(nlp.fold(val["turkce"]))
        info = {"kanon": val.get("turkce") or key, "kaynak": "sozluk"}
        if val.get("latin"):
            info["latin"] = val["latin"]
        for f in forms:
            if len(f) > 2:
                out.setdefault(f, info)
    return out


def load_concepts() -> dict[str, dict]:
    data = _read_json(config.CONCEPT_IDS) or {}
    out: dict[str, dict] = {}
    for _k, v in data.items():
        forms = set(v.get("uyeler") or [])
        for f in (v.get("tr"), v.get("en"), v.get("terim")):
            if f:
                forms.add(f)
        info = {"kaynak": "kavram", "qid": v.get("qid")}
        kim = v.get("kimlik") or {}
        if kim.get("umls_cui"):
            info["umls"] = kim["umls_cui"]
        if kim.get("disease_ontology"):
            info["do"] = kim["disease_ontology"]
        for f in forms:
            f = nlp.fold(f)
            if len(f) > 2:
                out.setdefault(f, info)
    return out


def build_lexicon() -> dict[str, dict]:
    """Tüm tıbbi terimleri (ICD + sözlük + kavram) tek sözlükte birleştirir."""
    lex: dict[str, dict] = {}
    for term, code in load_icd().items():
        lex.setdefault(term, {})["icd"] = code
    for term, info in load_thesaurus().items():
        lex.setdefault(term, {}).update(info)
    for term, info in load_concepts().items():
        lex.setdefault(term, {}).update({k: v for k, v in info.items() if k not in lex.get(term, {})})
    return {k: v for k, v in lex.items() if len(k) > 2}


if __name__ == "__main__":
    lex = build_lexicon()
    print("terim:", len(lex))
