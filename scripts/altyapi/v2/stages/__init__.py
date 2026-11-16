"""Ingest aşamaları (s1..s7). Her aşama bağımsız çağrılabilir ve `cli.py` tarafından sıraya konur."""

from . import (s1_extract, s2_normalize, s3_validate, s4_dedupe, s5_match, s6_enrich, s7_publish,
               s8_curriculum, s9_answer, s10_notes, s11_link, s12_verify)  # noqa: F401
