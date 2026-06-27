# Bundle_src
Easily bundle source files from a live project

# Bundle SRC

Bundle SRC is a small terminal app that copies your current project into a clean `src` folder, writes a file tree, and optionally zips it up. It looks like an old phosphor-green DOS utility, runs full-screen, and respects your `.gitignore`.

I built it because I got tired of manually cleaning out `__pycache__`, venvs, and node_modules before sending source to someone.

## What it does

- Runs from whatever folder you're in — that folder becomes the "project"
- Creates `./src` with a copy of everything except junk
- Writes `FILETREE.TXT` inside src
- Skips: `__pycache__`, `*.pyc`, `.git`, `node_modules`, `venv`, `.venv`, `dist`, `build`, `.DS_Store`, and anything in your `.gitignore`
- Optional one-click ZIP or TAR.GZ, named after your project
- Full-screen green-on-black interface, no scrolling back to your shell

## Install

### Linux (Debian/Ubuntu)
1. Download `b-src_1.3_amd64.deb` from Releases
2. Install:sudo dpkg -i b-src_1.3_amd64.deb
3. 3. The command `b_src` is now available anywhere.

### Windows
1. Download `b_src.exe` from Releases
2. Put it in your project folder, or put it somewhere in your PATH (like `C:\Windows`)
3. Open cmd or PowerShell in your project and type `b_src`

