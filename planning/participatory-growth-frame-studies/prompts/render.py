#!/usr/bin/env python3
"""Resolve shared JSON specifications into a prompt; never run image generation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

TOKEN = re.compile(r"\{\{([a-z]+)#(/[^{}]*)\}\}")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def pointer(value, path):
    for part in path.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def expand(text, sources):
    if not isinstance(text, str) or not text.strip() or text.strip() == "undefined":
        raise ValueError("Empty or invalid instruction")
    def substitute(match):
        value = pointer(sources[match[1]], match[2])
        return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    result = TOKEN.sub(substitute, text)
    if "{{" in result or "}}" in result:
        raise ValueError(f"Unresolved token: {result}")
    return result


def load(path):
    data = read(path)
    if data["schemaVersion"] != 1 or not data["scenes"]:
        raise ValueError("Expected schemaVersion 1 and nonempty scenes")
    shared_path = (path.parent / data["defaults"]["shared"]).resolve()
    shared = read(shared_path)
    source_paths = {k: (shared_path.parent / v).resolve() for k, v in shared["sources"].items()}
    sources = {k: read(v) for k, v in source_paths.items()}
    history_path = (path.parent / data["defaults"]["history"]).resolve()
    history = read(history_path)
    if history["character"] != data["character"]:
        raise ValueError("History character does not match")
    for name, record in history["records"].items():
        if hashlib.sha256(record["text"].encode()).hexdigest() != record["sha256"]:
            raise ValueError(f"History digest mismatch: {name}")
        expected = "invalid" if record["text"].strip() in ("", "undefined") else "recorded"
        if record["status"] != expected:
            raise ValueError(f"Incorrect history status: {name}")
    if data.get("policyVersion") != shared["policy"]["version"]:
        raise ValueError("Scene policy version does not match shared policy")
    for instruction in shared["policy"]["instructions"]:
        expand(instruction, sources)
    for value in shared["blocks"].values():
        expand(value, sources)
    for blocks in shared["modes"].values():
        for key in blocks:
            if key not in shared["blocks"]:
                raise ValueError(f"Unknown block: {key}")
    used = set(data["defaults"].get("historyRecords", []))
    if not used <= set(history["records"]):
        raise ValueError("Missing character-level history")
    character_blocks = data["defaults"].get("blocks", {})
    for instruction in character_blocks.values():
        expand(instruction, sources)
    for scene_id, scene in data["scenes"].items():
        if not scene["title"] or scene["mode"] not in shared["modes"]:
            raise ValueError(f"Invalid scene: {scene_id}")
        if not (path.parent / scene["image"]).is_file():
            raise ValueError(f"Missing scene image: {scene_id}")
        for block in scene.get("blocks", []):
            if block not in character_blocks:
                raise ValueError(f"Unknown character block: {block}")
        if "sourcePrompt" in scene:
            source = scene["sourcePrompt"]
            if source not in scene["history"] or history["records"][source]["status"] != "recorded":
                raise ValueError(f"Invalid source prompt: {source}")
        for source in scene.get("decisionSources", []):
            if source not in scene["history"] or history["records"][source]["status"] != "recorded":
                raise ValueError(f"Invalid decision source: {source}")
        for decision in scene.get("decisions", {}).values():
            expand(decision, sources)
        for instruction in scene["instructions"]:
            expand(instruction, sources)
        for name in scene["history"]:
            if name not in history["records"]:
                raise ValueError(f"Missing history: {name}")
            used.add(name)
    if used != set(history["records"]):
        raise ValueError(f"Unassigned history: {set(history['records']) - used}")
    for instruction in data["defaults"]["instructions"]:
        expand(instruction, sources)
    for reference in data["defaults"]["referenceImages"].values():
        if not (path.parent / reference).is_file():
            raise ValueError(f"Missing reference image: {reference}")
    return data, shared, sources, [path, shared_path, history_path, *source_paths.values()]


def render(data, shared, sources, scene_id):
    scene = data["scenes"][scene_id]
    lines = [f"Scene: {scene['title']} ({data['character']}/{scene_id})."]
    lines += shared["policy"]["instructions"]
    lines += [shared["blocks"][key] for key in shared["modes"][scene["mode"]]]
    # Color-only and human-only edits must not silently restyle the animal.
    if scene["mode"] == "local-guideline":
        lines += data["defaults"]["instructions"]
    lines += [data["defaults"]["blocks"][key] for key in scene.get("blocks", [])]
    lines += scene["instructions"]
    lines += list(scene.get("decisions", {}).values())
    return "\n\n".join(expand(line, sources) for line in lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Animal JSON, e.g. gen.json")
    parser.add_argument("--validate", action="store_true", help="Validate every scene and reference")
    parser.add_argument("--scene", help="Scene ID to render")
    parser.add_argument("--output", type=Path, help="Write prompt TXT and a .snapshot.json sidecar")
    args = parser.parse_args()
    if not args.validate and not args.scene:
        parser.error("Specify --validate or --scene")
    if args.output and not args.scene:
        parser.error("--output requires --scene")
    try:
        path = args.file.resolve()
        data, shared, sources, inputs = load(path)
        for scene_id in data["scenes"]:
            render(data, shared, sources, scene_id)
        if args.validate:
            print(f"OK: {len(data['scenes'])} scenes; all references and history digests valid", file=sys.stderr)
        if args.scene:
            prompt = render(data, shared, sources, args.scene)
            if args.output:
                snapshot_path = args.output.with_suffix(args.output.suffix + ".snapshot.json")
                protected = {p.resolve() for p in inputs}
                if args.output.resolve() in protected or snapshot_path.resolve() in protected:
                    raise ValueError("Output would overwrite a source file")
                snapshot = {
                    "schemaVersion": 1, "character": data["character"], "scene": args.scene,
                    "prompt": prompt,
                    "sceneImage": str((path.parent / data['scenes'][args.scene]['image']).resolve()),
                    "referenceImages": {k: str((path.parent / v).resolve()) for k, v in data['defaults']['referenceImages'].items()},
                    "inputs": {str(p): {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "data": read(p)} for p in inputs if p != inputs[2]},
                }
                args.output.write_text(prompt, encoding="utf-8")
                snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            else:
                print(prompt, end="")
    except (KeyError, ValueError, TypeError, OSError, IndexError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
