# i.am — Vibe Wizzards Wyrd (vww 3³)

> *Framework of E.C.Pabel — Raw Orbit*

Welcome to the **Raw Orbit vww 3³** repository. Knowledge is powerful and life is strange — let's find out together what this can become.

---

## About

**i.am** is an experimental framework by an independent researcher based in Germany. This project explores ideas at the intersection of creativity, structure, and technology.

> "I dare you to learn." — E.C.Pabel

---

## Project Structure

```
Vibe-Wizzards-Wyrd/
├── README.md          # You are here
├── CONTRIBUTING.md    # How to contribute
├── GIST.md            # What is a GitHub Gist and how to use one
├── LEARNING.md        # Roadmap: how computers & AI work
├── iam_sim.py         # IAM simulation & visualisation script
└── requirements.txt   # Python dependencies
```

---

## IAM Simulation

`iam_sim.py` is a Python script that simulates and visualises **IAM (i.am) grids** in 2-D and 3-D.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Usage

| Command | Description |
|---------|-------------|
| `python iam_sim.py 2d` | 2-D final-state heatmap (32×32) |
| `python iam_sim.py 2d-live` | 2-D live animated heatmap |
| `python iam_sim.py 3d` | 3-D CLI slice at X=8 (16³) |
| `python iam_sim.py 3d-cosmos` | 3-D COSMOS slice at Y=8 (16³) |
| `python iam_sim.py --help` | Full option reference |

Each sub-command accepts `--size`, `--steps` / `--frames`, `--axis`, `--idx`, and `--init` flags — see `--help` for details.

---

## Goals

- [x] Organize and document the repository
- [x] Add IAM simulation script (`iam_sim.py`)
- [ ] Define the core framework concepts
- [ ] Build a structured foundation for collaboration
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
