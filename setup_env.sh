#!/usr/bin/env bash
# Rebuild the Debian toolchain + Python ML stack used by the manual build and
# the experiment harness.  Safe to re-run after a container reset.
set -u
TGT=/usr/local/lib/python3.13/dist-packages

echo "[1/3] Debian packages"
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
  python3-torch python3-torchvision python3-docx python3-numpy python3-scipy \
  python3-matplotlib python3-pil python3-sklearn python3-pandas python3-pytest \
  python3-sentencepiece python3-nltk \
  libreoffice-writer poppler-utils fonts-liberation fonts-dejavu

echo "[2/3] Python ML stack into $TGT"
sudo uv pip install --python /usr/bin/python3.13 --target "$TGT" --quiet \
  transformers datasets peft sentence_transformers accelerate google-genai

# uv pulls its own numpy/torch/cuda wheels which shadow the Debian builds and
# make the Debian torchvision segfault.  Remove them; the Debian ones are used.
echo "[3/3] removing shadowing numpy/torch/cuda wheels from $TGT"
sudo find "$TGT" -maxdepth 1 \
  \( -name 'numpy*' -o -name 'torch*' -o -name 'nvidia*' -o -name 'triton*' \
     -o -name 'cuda*' -o -name 'cusparselt*' \) -exec rm -rf {} + 2>/dev/null

/usr/bin/python3.13 -c "
import torch, torchvision, numpy, docx, sklearn, matplotlib, transformers, peft, datasets
print('torch', torch.__version__, '| torchvision', torchvision.__version__,
      '| numpy', numpy.__version__, '| transformers', transformers.__version__,
      '| peft', peft.__version__)"
