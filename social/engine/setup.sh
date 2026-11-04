#!/bin/bash
# Prepara el entorno para generar reels: voz gratis (edge-tts) y fuentes.
set -e
if ! python3 -c "import edge_tts" 2>/dev/null; then NO_PROXY= no_proxy= pip install --break-system-packages -q edge-tts; fi
python3 -c "import PIL, numpy, scipy" && command -v ffmpeg >/dev/null && ls /usr/share/fonts/opentype/inter/InterDisplay-Black.otf >/dev/null && echo "setup ok"
