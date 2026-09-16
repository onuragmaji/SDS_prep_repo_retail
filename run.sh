#!/usr/bin/env bash
set -e

chmod +x "$0"

cd "$(dirname "$0")"

python3 -m pip install -r requirements.txt

streamlit run app.py \
  --server.headless true \
  --server.port 8501 \
  --browser.gatherUsageStats false
