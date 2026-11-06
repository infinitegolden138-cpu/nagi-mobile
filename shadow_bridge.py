#!/usr/bin/env python3
"""Nagi v0.2 offline bridge. No network. Never overwrites the existing Nagi installation.
Usage:
  python shadow_bridge.py path/to/nagi-memoire-2026-11-06.json
  python shadow_bridge.py --export
Output is written to the local nagi_data/ folder next to this script.
This is a separate portable memory store, NOT a direct integration with Nagi's existing database.
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent / "nagi_data"
STORE = ROOT / "memory.json"

def load(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != "nagi.memory.v1" or not isinstance(data.get("knowledge"), list) or not isinstance(data.get("messages"), list):
        raise ValueError("Fichier JSON non compatible avec la mémoire Nagi v1")
    return data

def merge(old, incoming):
    by_id = {x["id"]: x for x in old.get("knowledge", []) if isinstance(x, dict) and isinstance(x.get("id"), str)}
    for item in incoming["knowledge"]:
        if not isinstance(item, dict) or not all(isinstance(item.get(k), str) for k in ("id","topic","content")):
            continue
        prev = by_id.get(item["id"])
        if not prev or item.get("updated_at", "") > prev.get("updated_at", ""):
            by_id[item["id"]] = item
    messages = {x["id"]: x for x in old.get("messages", []) if isinstance(x, dict) and isinstance(x.get("id"), str)}
    for item in incoming["messages"]:
        if isinstance(item, dict) and isinstance(item.get("id"), str) and isinstance(item.get("text"), str):
            messages[item["id"]] = item
    return {"schema":"nagi.memory.v1","identity":{"name":"Nagi"},"knowledge":list(by_id.values()),"messages":sorted(messages.values(),key=lambda x:x.get("created_at",""))[-1000:]}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--export", action="store_true")
    args = parser.parse_args()
    ROOT.mkdir(exist_ok=True)
    existing = load(STORE) if STORE.exists() else {"schema":"nagi.memory.v1","knowledge":[],"messages":[]}
    if args.file:
        incoming = load(args.file)
        merged = merge(existing, incoming)
        STORE.write_text(json.dumps(merged,ensure_ascii=False,indent=2),encoding="utf-8")
        print(f"Import terminé : {len(merged['knowledge'])} connaissances, {len(merged['messages'])} messages -> {STORE}")
    elif args.export:
        out = ROOT / ("nagi-export-"+datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")+".json")
        out.write_text(json.dumps(existing,ensure_ascii=False,indent=2),encoding="utf-8")
        print(f"Export : {out}")
    else:
        parser.print_help()

if __name__ == "__main__": main()
