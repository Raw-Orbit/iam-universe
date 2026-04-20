# iam_universe — 3³OS

> *Framework of E.C.Pabel — Raw-Orbit*

Welcome to the **iam_universe** repository. Knowledge is powerful and life is strange — let's find out together what this can become.

---

## About

**i.am** is an experimental framework by an independent researcher based in Germany. This project explores ideas at the intersection of creativity, structure, and technology.

> "I dare you to learn." — E.C.Pabel

---

## Project Structure

```
iam_universe/
├── README.md          # You are here
├── CONTRIBUTING.md    # How to contribute
├── GIST.md            # What is a GitHub Gist and how to use one
├── LEARNING.md        # Roadmap: how computers & AI work
├── ROADMAP.md         # 3³OS vision and phased development plan
├── asm/               # Option 1: pure x86-64 NASM implementation
├── c/                 # Option 2: C implementation
├── lang/              # Option 3: .iam language interpreter + scenarios
└── rust/              # Option 4: Rust implementation
```

---

## IAM Simulation — four implementations

All four engines simulate the same diffusion model and write PPM images. Open any `.ppm` output with `feh`, `eog`, GIMP, or macOS Preview.

### Option 1 — NASM (pure x86-64 Assembly)

```bash
cd asm
make                # nasm -f elf64 iam.asm -o iam.o && ld iam.o -o iam
./iam > out.ppm
```

### Option 2 — C

```bash
cd c
make                # gcc -O2 iam_sim.c -o iam_sim -lm
./iam_sim 2d                          # 32×32 heatmap, 60 steps
./iam_sim local-crisis                # crisis patch, watch it diffuse
./iam_sim 3d --axis x --idx 8        # 3-D slice
./iam_sim 3d-cosmos                   # plasma-coloured COSMOS slice
./iam_sim --help                      # full option reference
```

### Option 3 — .iam language

```bash
cd lang
make                # gcc -O2 iamrun.c -o iamrun -lm
./iamrun scenarios/local_crisis.iam
./iamrun scenarios/boundary_stress.iam
./iamrun scenarios/cosmos.iam
```

`.iam` script syntax:

```
GRID 2D 32 INIT 1000
PATCH 14 14 5 5 SET 1500
RUN 60
SAVE out.ppm
```

### Option 4 — Rust

```bash
cd rust
cargo build --release
./target/release/iam_sim 2d
./target/release/iam_sim local-crisis
./target/release/iam_sim 3d-cosmos
./target/release/iam_sim --help
```

---

## Goals

- [x] Organize and document the repository
- [x] Option 1 — NASM pure assembly engine (`asm/`)
- [x] Option 2 — C engine (`c/`)
- [x] Option 3 — `.iam` language interpreter (`lang/`)
- [x] Option 4 — Rust engine (`rust/`)
- [ ] Build a modular 3³OS package structure
- [ ] Invite contributors to co-develop the vision

---

## Contributing

Community contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before getting started.

---

## Author

**E.C.Pabel** — Independent researcher, Germany
- GitHub: [@MaxLvNPC](https://github.com/MaxLvNPC)
- Organization: [Raw-Orbit](https://github.com/Raw-Orbit)

---

*Thanks to the community. More to come.*
