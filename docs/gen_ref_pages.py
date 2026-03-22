from pathlib import Path
import mkdocs_gen_files

SRC = Path("src")

for path in SRC.rglob("*.py"):
    # Skip __init__.py if you want cleaner output
    if path.name == "__init__.py":
        continue

    module_path = path.relative_to(SRC).with_suffix("")
    module = ".".join(module_path.parts)

    doc_path = Path("reference", *module_path.parts).with_suffix(".md")

    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"::: {module}")
