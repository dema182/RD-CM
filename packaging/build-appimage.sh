#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT_NAME="RD-CM-x86_64.AppImage"

python3 packaging/make-icon.py packaging/rd-cm.png
if [[ ! -x vendor/RAHasher ]]; then
  python3 packaging/fetch-rahasher.py
fi

python3 -m pip install --user --quiet -r requirements.txt pyinstaller
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m PyInstaller \
  --noconfirm --clean --windowed --name RD-CM \
  --paths src \
  --add-data "src/rdcm/data/couch_coop.json:rdcm/data" \
  --add-binary "vendor/RAHasher:vendor" \
  --hidden-import py7zr \
  --hidden-import rdcm \
  --hidden-import rdcm.gui \
  src/retrodeck_collection_manager.py

rm -rf AppDir
mkdir -p AppDir/usr/bin AppDir/usr/share/icons/hicolor/256x256/apps
cp dist/RD-CM AppDir/usr/bin/RD-CM
cp packaging/AppRun AppDir/AppRun
cp packaging/RD-CM.desktop AppDir/RD-CM.desktop
cp packaging/rd-cm.png AppDir/rd-cm.png
cp packaging/rd-cm.png AppDir/usr/share/icons/hicolor/256x256/apps/rd-cm.png
chmod +x AppDir/AppRun AppDir/usr/bin/RD-CM

if [[ ! -x ./appimagetool ]]; then
  wget -q https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage -O appimagetool
  chmod +x appimagetool
fi
ARCH=x86_64 ./appimagetool --appimage-extract-and-run AppDir "$OUT_NAME"
test -s "$OUT_NAME"
file "$OUT_NAME"
echo "Built $ROOT/$OUT_NAME"
