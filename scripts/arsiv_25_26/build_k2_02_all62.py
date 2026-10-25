import sys, json, re, subprocess
from pathlib import Path

REPO_ROOT = Path('/home/indu/medsor')
TASLAK = REPO_ROOT / 'meds_database_25_26/taslak/y25-k2-02-bilinc-bozuklugu-olan-hastaya-yaklasim'

sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/sesli_anlatim'))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/ders_isci'))
sys.path.insert(0, str(REPO_ROOT / 'meds/scripts/cizim'))

import konusma_v2 as KV
import denetle as D
import isle as IS
import cizim_dogrula as CD
import sablon

# Load existing generate_deep_k2_02.py to reuse the existing rich paragraphs
with open(REPO_ROOT / 'meds/scripts/arsiv_25_26/generate_deep_k2_02.py') as f:
    orig_code = f.read()

# Let's extract the PARAGRAPHS list from original code using ast or exec
local_ns = {}
exec(compile(orig_code[:orig_code.find('cizim_komutlari = [')], '<string>', 'exec'), {}, local_ns)
old_paras = local_ns['PARAGRAPHS']
old_para_map = {p[3]: p for p in old_paras}

print(f"Loaded {len(old_para_map)} existing paragraphs from generate_deep_k2_02.py")
