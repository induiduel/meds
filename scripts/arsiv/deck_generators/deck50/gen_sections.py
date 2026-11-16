import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.builder_helper import (
    make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz
)

# We will define Section 1 to 10 for Deck 50
print("Section builder module template ready.")
