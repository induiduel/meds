import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.auto_curriculum_compiler import compile_deck_from_spec

print("Orchestrator ready to receive deck specs.")
