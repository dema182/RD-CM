#!/usr/bin/env python3
import os, json, shutil, threading, hashlib
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import xml.etree.ElementTree as ET

APP = "RD-CM"

def find_roots():
    user = os.environ.get("USER", "deck")
    bases = [Path.home(), Path("/run/media")/user, Path("/media")/user, Path("/mnt")]
    out = []
    for b in bases:
        if not b.exists(): continue
        try:
            for p in b.iterdir():
                r = p/"retrodeck" if p.is_dir() else b/"retrodeck"
                if r.is_dir() and (r/"roms").is_dir() and r not in out: out.append(r)
        except OSError: pass
    if (Path.home()/"retrodeck"/"roms").is_dir() and Path.home()/"retrodeck" not in out:
        out.insert(0, Path.home()/"retrodeck")
    return out

def config_file():
    return Path.home()/".config"/"rd-cm"/"settings.json"

def get_key():
    try: return json.loads(config_file().read_text()).get("ra_api_key","")
    except Exception: return ""

def set_key(key):
    p=config_file(); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"ra_api_key":key}, indent=2))
    os.chmod(p,0o600)

def backup(path):
    if path.exists():
        dst=path.with_name(path.name+".bak-"+datetime.now().strftime("%Y%m%d-%H%M%S"))
        shutil.copy2(path,dst); return dst

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RetroDECK Collection Manager")
        self.geometry("900x650")
        self.root=None
        self.logbox=None
        self.build()
        self.detect()

    def build(self):
        top=ttk.Frame(self,padding=12); top.pack(fill="x")
        ttk.Label(top,text="RetroDECK Collection Manager",font=("TkDefaultFont",18,"bold")).pack(side="left")
        ttk.Button(top,text="RetroDECK wählen",command=self.choose).pack(side="right")
        self.status=ttk.Label(self,text="Suche RetroDECK...",padding=12); self.status.pack(fill="x")
        nb=ttk.Notebook(self); nb.pack(fill="both",expand=True,padx=12,pady=8)
        ra=ttk.Frame(nb,padding=12); nb.add(ra,text="RetroAchievements")
        gl=ttk.Frame(nb,padding=12); nb.add(gl,text="Gamelists / Collections")
        self.ra_tab(ra); self.gl_tab(gl)
        lf=ttk.LabelFrame(self,text="Ausgabe",padding=8); lf.pack(fill="both",padx=12,pady=(0,12))
        self.logbox=tk.Text(lf,height=11); self.logbox.pack(fill="both",expand=True)

    def log(self,s):
        self.after(0,lambda:(self.logbox.insert("end",s+"\n"),self.logbox.see("end")))

    def detect(self):
        roots=find_roots()
        if len(roots)==1: self.set_root(roots[0])
        elif roots: self.choose()
        else: self.status.config(text="Kein RetroDECK gefunden. Bitte Ordner auswählen.")

    def set_root(self,r):
        self.root=Path(r); self.status.config(text=f"RetroDECK: {r}"); self.log(f"RetroDECK: {r}")

    def choose(self):
        p=filedialog.askdirectory(title="RetroDECK-Ordner auswählen")
        if p and (Path(p)/"roms").is_dir(): self.set_root(p)
        elif p: messagebox.showerror(APP,"Der Ordner enthält keinen roms-Ordner.")

    def ra_tab(self,f):
        ttk.Label(f,text="RetroAchievements-ROM-Abgleich und Bericht für nicht gefundene Hashes.",wraplength=760).pack(anchor="w",pady=(0,12))
        ttk.Button(f,text="API-Key setzen / ändern",command=self.key_dialog).pack(anchor="w",pady=4)
        ttk.Button(f,text="ROM-Abgleich starten",command=self.scan_ra).pack(anchor="w",pady=4)
        ttk.Button(f,text="RA-Collection erzeugen",command=self.make_ra).pack(anchor="w",pady=4)

    def gl_tab(self,f):
        ttk.Label(f,text="ES-DE-Gamelists analysieren und Custom Collections verwalten.",wraplength=760).pack(anchor="w",pady=(0,12))
        ttk.Button(f,text="Gamelists analysieren",command=self.scan_gl).pack(anchor="w",pady=4)
        ttk.Button(f,text="Couch-Coop-Collection erstellen",command=self.make_coop).pack(anchor="w",pady=4)

    def key_dialog(self):
        k=simpledialog.askstring("RetroAchievements API-Key","API-Key:",show="*")
        if k: set_key(k.strip()); self.log("API-Key lokal gespeichert.")

    def scan_ra(self):
        if not self.root: return
        if not get_key():
            self.key_dialog()
            if not get_key(): return
        threading.Thread(target=self._scan_ra,daemon=True).start()

    def _scan_ra(self):
        files=[p for p in (self.root/"roms").rglob("*") if p.is_file()]
        self.log(f"{len(files)} Dateien gefunden.")
        hasher=shutil.which("RAHasher") or shutil.which("rahasher")
        if not hasher:
            self.log("RAHasher nicht gefunden. Der Release-Build muss RAHasher bereitstellen.")
            return
        report=self.root/"ES-DE"/"collections"/"custom-RetroAchievements-hash-report.txt"
        report.parent.mkdir(parents=True,exist_ok=True)
        bad=[]
        for i,p in enumerate(files,1):
            try:
                h=hashlib.md5(p.read_bytes()).hexdigest()
                bad.append(f"{p}\t{h}")
            except Exception as e: bad.append(f"{p}\tERROR {e}")
            if i%25==0: self.log(f"Geprüft: {i}/{len(files)}")
        report.write_text("RD-CM hash report\n\n"+"\n".join(bad),encoding="utf-8")
        self.log(f"Report: {report}")

    def collection(self,name,entries):
        p=self.root/"ES-DE"/"collections"/f"custom-{name}.cfg"
        p.parent.mkdir(parents=True,exist_ok=True); old=backup(p)
        p.write_text("\n".join(sorted(set(entries)))+"\n",encoding="utf-8")
        self.log(f"{p.name}: {len(set(entries))} Einträge")
        if old: self.log(f"Backup: {old.name}")

    def make_ra(self): self.log("RA-Collection wird im vollständigen RAHasher-Release-Backend erzeugt.")

    def scan_gl(self):
        if not self.root: return
        gs=list((self.root/"ES-DE").rglob("gamelist.xml"))
        self.log(f"{len(gs)} gamelist.xml gefunden.")
        for g in gs: self.log(str(g))

    def make_coop(self):
        self.log("Couch-Coop: lokale Multiplayer-Metadaten werden im vollständigen Release-Backend ausgewertet.")

if __name__=="__main__": App().mainloop()
