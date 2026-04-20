# 3³OS — Roadmap

> *"You think we could forge my stuff into an individual IAM OS or call it the 3³OS?"*

**Short answer: yes.**

Not as a traditional operating system (kernel, device drivers, bootloader) — but as an **operating framework**: a modular, extensible toolkit that runs your IAM model, processes your research concepts, and visualises them. Think of it less like Linux and more like how NASA calls a mission control room an "operating system" — the thing that makes a complex system legible and steerable.

---

## What 3³OS is (in this context)

```
3³OS = IAM simulation engine
     + modular concept layer (your research as data)
     + visualisation dashboard
     + CLI interface
     + (future) web or local GUI
```

The simulation engine already exists in four forms (NASM, C, `.iam` language, Rust — see `asm/`, `c/`, `lang/`, `rust/`). The goal of this roadmap is to grow it into something that feels like a coherent, personal operating framework.

---

## Current state

```
iam_universe/
├── asm/               ← Option 1: NASM engine          (done ✅)
├── c/                 ← Option 2: C engine              (done ✅)
├── lang/              ← Option 3: .iam language         (done ✅)
├── rust/              ← Option 4: Rust engine           (done ✅)
├── README.md
├── CONTRIBUTING.md
├── GIST.md
├── LEARNING.md
└── ROADMAP.md
```

---

## Phase 1 — Modular core ✅

The four engines are complete and independently buildable:

```
iam_universe/
├── asm/    # nasm -f elf64 iam.asm -o iam.o && ld iam.o -o iam
├── c/      # gcc -O2 iam_sim.c -o iam_sim -lm
├── lang/   # gcc -O2 iamrun.c -o iamrun -lm  →  ./iamrun scenario.iam
└── rust/   # cargo build --release
```

Each engine accepts the same scenarios and writes PPM output. The `.iam` language (Option 3) is the long-term extensible interface.

**Why:** having the engine in four languages means you can always drop to the level you understand, and the `.iam` scripting layer hides the complexity when you just want to run a scenario.

---

## Phase 2 — Concept layer ✅ (your research as data)

Your research papers describe governance crises, societal tensions, and systemic boundaries. These map directly to grid configurations:

| Research concept | Grid representation |
|---|---|
| Stable society | uniform grid at 1000.0 |
| Local crisis | patch of cells set to 1500.0 |
| Systemic boundary | hard wall (cells fixed at a boundary value) |
| Tension propagation | watch values diffuse over `RUN` iterations |
| Equilibrium / resolution | grid converges to a uniform value |

**Done:** `lang/scenarios/` contains named `.iam` scenario files:

```
lang/scenarios/
├── baseline.iam          # uniform 1000.0
├── local_crisis.iam      # 5×5 patch at 1500, rest 1000
├── boundary_stress.iam   # fixed left wall at 1500, right at 500
└── cosmos.iam            # 3-D COSMOS slice
```

Run any scenario:
```bash
cd lang && ./iamrun scenarios/local_crisis.iam
```

---

## Phase 3 — Dashboard (see everything at once)

Instead of one image at a time, generate a composite view:

```
┌──────────────────┬──────────────────┐
│  2D final state  │  local crisis    │
├──────────────────┼──────────────────┤
│  3D CLI slice    │  3D COSMOS slice │
└──────────────────┴──────────────────┘
```

This becomes your "mission control" — one command, full picture.

```bash
cd lang && ./iamrun scenarios/local_crisis.iam
```

**Planned:** a shell script (`dashboard.sh`) that runs all four scenarios and tiles the PPM outputs side by side using `montage` (ImageMagick) or similar.

---

## Phase 4 — Export & share

- Outputs are already PPM — convert to PNG with `convert out.ppm out.png` (ImageMagick)
- Export grid state to CSV for use in other tools
- Generate a Gist-ready code snippet from a scenario

---

## Phase 5 — Web interface (optional, later)

A local web dashboard using [Streamlit](https://streamlit.io) or [Gradio](https://gradio.app):
- No web development knowledge needed
- Sliders for grid size, init value, steps
- Live animation in the browser

```bash
pip install streamlit
streamlit run iam_dashboard.py
```

---

## Naming

`iam_universe` + `3³OS` work together as the project identity. A few ways to use it:

- **Repository name:** `iam_universe` (already set ✅)
- **Tagline:** *"The system that makes systemic thinking legible."*
- **CLI feel:** `./iamrun scenario.iam` — your language, your commands

---

## Immediate next step

1. Run `cd lang && ./iamrun scenarios/local_crisis.iam`
2. Open `local_crisis.ppm` in any image viewer
3. Watch the tension gradient — that is your governance crisis model, running as compiled code with zero Python, zero dependencies

---

*See also: [LEARNING.md](LEARNING.md) for the foundational concepts behind this.*
