"""
Extract structured DiseaseReport fields from disease-reports JSONL/JSON
input(s) and write enriched JSONL output(s).

Input can be a single file or a folder containing many .jsonl / .json files.
For each input record (one line in .jsonl, or one object / each item in an
array in .json) one output line is written. Original record is preserved,
extracted fields are merged in. Errors land in a `_error` field.

The empty-record shape is loaded from a generated dataclass file
(see gen_schema.py), so this script does not hardcode the field list.
"""

import importlib.util
import json
from pathlib import Path

from openai import OpenAI
import requests
import httpx


# --------------------------------------------------------------------------
# Client setup
# --------------------------------------------------------------------------

with open("TS-Scanner.json") as f:
    env = json.load(f)

with open("llm.codebar.net.json") as f:
    codebar = json.load(f)

access = {v["name"]: v["value"] for v in env["variables"] if v.get("enabled", True)}


class ScrubTransport(httpx.HTTPTransport):
    def handle_request(self, request):
        request.headers["user-agent"] = "Mozilla/5.0"
        for name in [h for h in request.headers if h.lower().startswith("x-stainless")]:
            del request.headers[name]
        return super().handle_request(request)


client = OpenAI(
    base_url=access["url"],
    api_key=access["token"],
    http_client=httpx.Client(transport=ScrubTransport()),
)


def chat(prompt, model="qwen3.5:4b", system=None, stream=False, **kwargs):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    if stream:
        text = ""
        for chunk in client.chat.completions.create(
            model=model, messages=messages, stream=True, **kwargs
        ):
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            text += delta
        print()
        return text

    resp = client.chat.completions.create(model=model, messages=messages, **kwargs)
    return resp.choices[0].message.content


# --------------------------------------------------------------------------
# Extraction pipeline
# --------------------------------------------------------------------------

def load_schema(path: Path):
    """Dynamically import the dataclass schema file and return its class."""
    spec = importlib.util.spec_from_file_location("_schema", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ExtractionSchema


def parse(text: str, system: str) -> dict:
    """Run the extraction prompt on one text and return parsed JSON."""
    prompt = f'# Text to parse\n"""\n{text.strip()}\n"""'
    raw = chat(
        prompt,
        system=system,
        temperature=0,
        # response_format={"type": "json_object"},  # uncomment if your server supports it
    ).strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.lstrip().startswith("json"):
            raw = raw.lstrip()[4:]
    return json.loads(raw.strip())


def iter_records(path: Path):
    """
    Stream records from a .jsonl or .json file.

    Yields tuples (record, error_msg, raw_text):
      - On success: (dict, None, None)
      - On parse error: (None, str, str-or-None)
    """
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        with path.open(encoding="utf-8") as f:
            for line in f:
                stripped = line.rstrip("\n")
                if not stripped.strip():
                    continue
                try:
                    obj = json.loads(stripped)
                except json.JSONDecodeError as e:
                    yield None, f"jsonl parse: {e}", stripped
                    continue
                if isinstance(obj, str):           # bare-string record
                    obj = {"fulltext": obj}
                yield obj, None, None
    elif suffix == ".json":
        try:
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            yield None, f"json parse: {e}", None
            return
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, str):              # bare-string record
                item = {"fulltext": item}
            yield item, None, None
    else:
        raise ValueError(f"unsupported file extension: {path.suffix}")


def extract_file(
    in_path: Path,
    out_path: Path,
    system: str,
    empty_labels: dict,
    resume: bool = True,
    progress_every: int = 10,
) -> None:
    """Process one input file -> one output JSONL file."""
    already = 0
    if resume and out_path.exists():
        with out_path.open(encoding="utf-8") as f:
            already = sum(1 for _ in f)
        if already:
            print(f"  resuming after {already} already-processed records")

    mode = "a" if already else "w"
    with out_path.open(mode, encoding="utf-8") as fout:
        for i, (record, err, raw) in enumerate(iter_records(in_path)):
            if i < already:
                continue

            if err:
                out = {"_raw": raw or "", **empty_labels, "_error": err}
                fout.write(json.dumps(out, ensure_ascii=False) + "\n")
                fout.flush()
                continue

            text = record.get("fulltext")
            if not text:
                labels = {**empty_labels, "_error": "missing fulltext"}
            else:
                try:
                    labels = parse(text, system)
                except Exception as e:
                    labels = {**empty_labels,
                              "_error": f"extraction: {type(e).__name__}: {e}"}

            fout.write(json.dumps({**record, **labels}, ensure_ascii=False) + "\n")
            fout.flush()

            if progress_every and (i + 1) % progress_every == 0:
                print(f"  processed {i + 1}")


def extract_path(
    in_path: Path,
    out_path: Path,
    system: str,
    empty_labels: dict,
    resume: bool = True,
    progress_every: int = 10,
) -> None:
    """Dispatch on whether in_path is a file or a directory."""
    if in_path.is_file():
        out_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"processing {in_path} -> {out_path}")
        extract_file(in_path, out_path, system, empty_labels, resume, progress_every)

    elif in_path.is_dir():
        sources = sorted([*in_path.glob("*.jsonl"), *in_path.glob("*.json")])
        if not sources:
            print(f"no .jsonl or .json files found in {in_path}")
            return
        out_path.mkdir(parents=True, exist_ok=True)
        print(f"found {len(sources)} input file(s) in {in_path}")
        for src in sources:
            dst = out_path / f"{src.stem}.jsonl"
            print(f"\nprocessing {src.name} -> {dst}")
            extract_file(src, dst, system, empty_labels, resume, progress_every)

    else:
        raise FileNotFoundError(f"input not found: {in_path}")

    print("\nall done")


if __name__ == "__main__":
    import argparse

    print([m.id for m in client.models.list().data])

    p = argparse.ArgumentParser(
        description="Extract DiseaseReport fields from JSONL/JSON disease reports."
    )
    p.add_argument("-s", "--system-prompt", default="SystemPrompt.md",
                   help="Path to the SystemPrompt markdown file. Default: %(default)s")
    p.add_argument("--schema", default=None,
                   help="Path to the dataclass schema .py file produced by "
                        "gen_schema.py. Default: schema.py next to the prompt.")
    p.add_argument("-i", "--input", default="disease_reports.jsonl",
                   help="Input file OR directory. If directory, every .jsonl and "
                        ".json file inside is processed. Default: %(default)s")
    p.add_argument("-o", "--output", default="disease_reports_embeddings.jsonl",
                   help="Output file (if -i is a file) or directory (if -i is a "
                        "directory). Parent dirs are created. Default: %(default)s")
    p.add_argument("--no-resume", action="store_true",
                   help="Overwrite existing output(s) instead of resuming.")
    p.add_argument("--progress-every", type=int, default=10,
                   help="Print progress every N records (0 disables). Default: %(default)s")
    args = p.parse_args()

    prompt_path = Path(args.system_prompt)
    schema_path = Path(args.schema) if args.schema else prompt_path.parent / "schema.py"

    if not prompt_path.exists():
        raise FileNotFoundError(f"system prompt not found: {prompt_path}")
    if not schema_path.exists():
        raise FileNotFoundError(
            f"schema file not found: {schema_path}\n"
            f"  generate it with:  python gen_schema.py {prompt_path}"
        )

    system = prompt_path.read_text(encoding="utf-8")
    Schema = load_schema(schema_path)

    extract_path(
        in_path=Path(args.input),
        out_path=Path(args.output),
        system=system,
        empty_labels=Schema.empty(),
        resume=not args.no_resume,
        progress_every=args.progress_every,
    )