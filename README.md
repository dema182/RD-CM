# RD-CM — RetroDECK Collection Manager

Linux-Desktopanwendung für **RetroDECK + ES-DE**: RetroAchievements-ROM-Abgleich mit dem offiziellen **RAHasher**, `custom-RetroAchievements.cfg`, Couch-Coop-Collection, Gamelist-Unterstützung und automatischen Backups.

Endprodukt: **`RD-CM-x86_64.AppImage`** — startbar ohne Python, pip oder Entwicklungsumgebung.

Repository: https://github.com/dema182/RD-CM

---

## Installation (AppImage)

1. `RD-CM-x86_64.AppImage` aus den [Releases](https://github.com/dema182/RD-CM/releases) laden.
2. Ausführbar machen und starten:

```bash
chmod +x RD-CM-x86_64.AppImage
./RD-CM-x86_64.AppImage
```

Kein Root, kein Python, kein pip.

---

## RetroDECK-Erkennung

RD-CM sucht typische Pfade, ohne fest verdrahtete Benutzernamen:

- `/home/$USER/retrodeck`
- `/run/media/$USER/*/retrodeck`
- `/media/$USER/*/retrodeck`
- `/mnt/*/retrodeck`

Eine Installation wird automatisch verwendet, mehrere über eine Auswahl, keine über einen Dateidialog. ROM-Verzeichnis: `<retrodeck>/roms/`.

---

## RetroAchievements API-Key

Jeder Nutzer verwendet **seinen eigenen** Key (RetroAchievements → Settings → Keys).

- lokal: `~/.config/rd-cm/settings.json` (Dateirechte `600`)
- nie im Quellcode, nie im AppImage, nie in Logs, nie in GitHub Actions

Optionaler Benutzername (API-Parameter `z`) ebenfalls nur lokal.

---

## RetroAchievements-Scan

1. RetroDECK erkennen
2. `roms/` direkt scannen (keine Vorab-Textdatei nötig)
3. System aus Ordner/Endung ableiten
4. **RAHasher 1.8.3** hashen (systemabhängig; Archive werden nicht als „ZIP-MD5“ verwendet)
5. Abgleich gegen `API_GetGameList` (`h=1`) inkl. Cache unter `~/.cache/rd-cm/v1/`
6. Ergebnis:

| Status | Bedeutung |
| --- | --- |
| RA unterstützt | Hash eindeutig einem RA-Spiel zugeordnet |
| Kein Treffer | Hash unbekannt — **kein** Beweis für eine falsche Version |
| Möglicherweise falsche Version | Name deutet stark auf ein RA-Spiel, Hash passt nicht (Hinweis, kein Beweis) |
| Fehler | einzelne Datei, Scan läuft weiter |

Anschließend: **`custom-RetroAchievements.cfg`** — nur Hash-Treffer, Pfade als `%ROMPATH%/system/datei`.

---

## Couch Coop

Collection `custom-Couch Coop.cfg`.

Kriterium: **lokales Simultan-Spiel an einem Gerät, mindestens zwei Controller**.

Nicht automatisch: Online, LAN-only, Link Cable, Hotseat-only, Multi-Device-Wireless.

Quellen: ES-DE-Gamelist-Metadaten (`<players>`, Beschreibung) **und** ein kuratierter Katalog. Dateinamen werden nicht als Multiplayer-Beweis verwendet. Unklare Titel werden markiert und **nicht** aufgenommen.

---

## Backup

Vor dem Überschreiben von Collections/Gamelists:

```text
<retrodeck>/backup/YYYY-MM-DD_HHMMSS/
```

---

## Gamelists

ES-DE-`gamelist.xml` wird gelesen. Unbekannte XML-Felder bleiben erhalten, wenn Dateien zurückgeschrieben werden.

---

## Source-Build

```bash
git clone https://github.com/dema182/RD-CM.git
cd RD-CM
python3 -m pip install -r requirements.txt pytest
PYTHONPATH=src python3 -m pytest -q
./packaging/build-appimage.sh
```

Ergebnis: `RD-CM-x86_64.AppImage`.

GitHub Actions (`.github/workflows/build-appimage.yml`) baut bei Tag `v*` oder per *workflow_dispatch* dasselbe AppImage und hängt es an das Release.

---

## Lizenz

MIT — siehe [LICENSE](LICENSE).

RAHasher stammt von [RetroAchievements/RALibretro](https://github.com/RetroAchievements/RALibretro) bzw. [LeXofLeviafan/RAHasher](https://github.com/LeXofLeviafan/RAHasher) und wird zur Build-Zeit heruntergeladen, nicht ins Git eingebettet.
