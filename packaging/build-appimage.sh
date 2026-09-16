#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 -m PyInstaller --noconfirm --clean --onefile --windowed --name RD-CM src/retrodeck_collection_manager.py

rm -rf AppDir
mkdir -p AppDir/usr/bin
cp dist/RD-CM AppDir/usr/bin/RD-CM
cp packaging/AppRun AppDir/AppRun
cp packaging/RD-CM.desktop AppDir/RD-CM.desktop
chmod +x AppDir/AppRun AppDir/usr/bin/RD-CM

./appimagetool AppDir RD-CM-x86_64.AppImage
