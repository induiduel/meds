#!/usr/bin/env bash
# Faz 14 otomatik ÜCRETSİZ kip (meds-faz14-ucretsiz.timer): yalnız ücretsiz Gemini anahtarları, günlük kota bitene kadar.
# Panelden kapatılabilir: meds_temp/state/otomasyon.json → "faz14_ucretsiz_otomatik": false. Ücretli anahtar burada ASLA kullanılmaz.
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; MEDS="$(cd "$HERE/../.." && pwd)"
STATE="$MEDS/../meds_temp/state/otomasyon.json"
if [ -f "$STATE" ] && python3 -c "import json,sys;sys.exit(0 if json.load(open('$STATE')).get('faz14_ucretsiz_otomatik', True) is False else 1)"; then
  echo "Faz 14 otomatik ücretsiz kip panelden kapalı; çıkılıyor."; exit 0
fi
if pgrep -f "python[^ ]* [^ ]*phase14_cloud_question_editor\.py" >/dev/null; then echo "Faz 14 zaten çalışıyor."; exit 0; fi
exec "$MEDS/.venv-ocr/bin/python" "$MEDS/scripts/advanced_ai/phase14_cloud_question_editor.py" --ucretsiz-otomatik
