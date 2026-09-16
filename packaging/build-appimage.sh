#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPDIR="$ROOT/AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/rd-cm" "$APPDIR/usr/share/applications"
cp "$ROOT/src/retrodeck_collection_manager.py" "$APPDIR/usr/share/rd-cm/"
cp "$ROOT/packaging/AppRun" "$APPDIR/"
cp "$ROOT/packaging/RD-CM.desktop" "$APPDIR/usr/share/applications/rd-cm.desktop"
chmod +x "$APPDIR/AppRun"
# Python is supplied by the CI build image / runtime packaging step.
# appimagetool turns AppDir into the final Type-2 AppImage.
echo "AppDir prepared: $APPDIR"
