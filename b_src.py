#!/usr/bin/env python3
"""
bundle_source.py – Hassle‑free source bundler.

Copies all files from the current project folder into a new 'src'
subfolder, creates a plain‑text tree listing of the original files,
and optionally packs the folder into a .tar.gz or .zip archive.

No terminal wizardry required – just run it and follow the prompts.
"""

import os
import sys
import shutil
import tarfile
import zipfile
from pathlib import Path
from datetime import datetime


# ------------------------------------------------------------
#  User‑friendly console helpers
# ------------------------------------------------------------

def ok(msg):    print(f"  ✔ {msg}")
def err(msg):   print(f"  ✘ {msg}")
def info(msg):  print(f"  {msg}")
def warn(msg):  print(f"  ⚠ {msg}")


def ask_yes_no(prompt, default=None):
    """Ask a yes/no question. Return True for yes, False for no."""
    while True:
        if default is True:
            hint = " [Y/n] "
        elif default is False:
            hint = " [y/N] "
        else:
            hint = " [y/n] "
        answer = input(prompt + hint).strip().lower()
        if answer == '' and default is not None:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print("  Please answer y or n.")


def ask_choice(prompt, options, default=None):
    """
    Ask the user to pick one of several options.
    options: list of strings like ["tar.gz", "zip"]
    Returns the selected option string.
    """
    print(prompt)
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")
    while True:
        sel = input("  Enter number: ").strip()
        if sel == '' and default is not None:
            return default
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print(f"  Please enter a number between 1 and {len(options)}.")


def pause():
    input("\n  Press Enter to continue...")


# ------------------------------------------------------------
#  Tree generation
# ------------------------------------------------------------

def generate_tree(root_dir, prefix=""):
    """
    Recursively build a text tree of the directory structure.
    Returns a string.
    """
    lines = []
    root_path = Path(root_dir)
    items = sorted(root_path.iterdir(), key=lambda p: (not p.is_dir(), p.name))

    for idx, item in enumerate(items):
        is_last = (idx == len(items) - 1)
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + item.name)

        if item.is_dir():
            extension = "    " if is_last else "│   "
            lines.append(generate_tree(item, prefix + extension))

    return "\n".join(lines) if lines else ""


# ------------------------------------------------------------
#  Main logic
# ------------------------------------------------------------

def main():
    print("\n  📦  Source Bundler  📦\n")

    root = Path.cwd()
    src_dir = root / "src"

    # ---- 1. Create / prepare the src folder ----
    if src_dir.exists():
        warn(f"Folder '{src_dir.name}' already exists.")
        if not ask_yes_no("  Overwrite it? (all contents will be deleted)", default=False):
            info("  Aborted.")
            return
        shutil.rmtree(src_dir)
        ok("Removed existing src folder.")

    src_dir.mkdir(parents=True)
    ok(f"Created {src_dir}")

    # ---- 2. Copy everything (except src and this script) ----
    print("\n  Copying files...")

    def ignore_func(directory, contents):
        """Ignore the destination src folder itself and this script."""
        ignored = []
        for item in contents:
            item_path = Path(directory) / item
            # Skip the src folder (only at the top level)
            if directory == root and item == src_dir.name:
                ignored.append(item)
            # Skip this script itself
            if directory == root and item == Path(__file__).name:
                ignored.append(item)
        return ignored

    try:
        # dirs_exist_ok=True allows copying into an existing directory (we just created it)
        shutil.copytree(root, src_dir, ignore=ignore_func,
                        copy_function=shutil.copy2, dirs_exist_ok=True)
        ok("All files copied successfully.")
    except Exception as e:
        err(f"Copy failed: {e}")
        return

    # ---- 3. Write the file tree ----
    tree_text = generate_tree(root)
    tree_file = src_dir / "original_file_tree.txt"
    try:
        tree_file.write_text(tree_text, encoding="utf-8")
        ok(f"File tree written to {tree_file.name}")
    except Exception as e:
        err(f"Could not write tree file: {e}")

    # ---- 4. Ask about archiving ----
    print()
    if ask_yes_no("  Archive the src folder?", default=True):
        fmt = ask_choice("  Choose archive format:", ["tar.gz", "zip"], default="tar.gz")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if fmt == "tar.gz":
            archive_name = root / f"src_{timestamp}.tar.gz"
            try:
                with tarfile.open(archive_name, "w:gz") as tar:
                    tar.add(src_dir, arcname=src_dir.name)
                ok(f"Created {archive_name.name}")
            except Exception as e:
                err(f"Tar creation failed: {e}")
        else:  # zip
            archive_name = root / f"src_{timestamp}.zip"
            try:
                with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zf:
                    for file_path in src_dir.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(root)
                            zf.write(file_path, arcname)
                ok(f"Created {archive_name.name}")
            except Exception as e:
                err(f"Zip creation failed: {e}")

        # Optionally remove the src folder after archiving
        if ask_yes_no("  Delete the src folder now? (the archive contains everything)", default=False):
            try:
                shutil.rmtree(src_dir)
                ok("Deleted src folder.")
            except Exception as e:
                err(f"Could not delete src folder: {e}")

    else:
        info("No archive created. The src folder remains.")

    print("\n  ✅ All done!")
    pause()


# ------------------------------------------------------------
#  Entry point
# ------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 Exited by user.")
        sys.exit(0)
