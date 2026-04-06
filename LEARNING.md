# Learning Roadmap — How Computers & AI Work

> *"I want to understand how PCs and AI truly work — not because they are bad,*
> *because I know I might be able to do something good."* — E.C.Pabel

This file is a honest, beginner-friendly map. You don't need to follow every link — pick what sparks curiosity.

---

## 1. How a computer actually works

Everything starts here. A computer is a machine that moves and transforms numbers very fast.

| Topic | What to look for | Why it matters |
|---|---|---|
| Binary / bits | "How computers work — binary" | All data — images, text, code — is ones and zeros |
| CPU | "What does a CPU do" | The brain: fetches, decodes, executes instructions |
| Memory (RAM) | "RAM vs storage explained" | Fast scratchpad the CPU uses while working |
| Storage (SSD/HDD) | "How SSDs work" | Permanent memory — survives power-off |
| Operating system | "What does an OS do" | Manages hardware so your programs don't have to |

**Free starting point:** [cs.stanford.edu/people/eroberts/courses/soco/projects/2000-01/digital-computer-basics](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2000-01/digital-computer-basics/index.html)

---

## 2. How software / programming works

A program is a sequence of precise instructions that a CPU can eventually execute.

### Concepts to explore (in order)
1. **Variables & types** — storing a value with a name (`x = 42`)
2. **Conditions** — `if` / `else`
3. **Loops** — repeat something N times
4. **Functions** — give a block of logic a name so you can reuse it
5. **Data structures** — lists, grids, dictionaries
6. **Files & I/O** — reading/writing data

### Where to start
- **Python** is the best first language for this kind of project (it's what `iam_sim.py` uses).
- [python.org/about/gettingstarted](https://www.python.org/about/gettingstarted/) — official start
- [learnpython.org](https://www.learnpython.org) — interactive browser-based exercises, free

---

## 3. How AI / Machine Learning works

AI is not magic. At its core it's **optimising numbers** so that a system gets better at a task.

### The basic idea
```
Data → Model (lots of maths) → Predictions → Compare with truth → Adjust → Repeat
```

### Key concepts
| Term | Plain English |
|---|---|
| **Model** | A function with many parameters (numbers to tune) |
| **Training** | Showing the model examples so it can tune its parameters |
| **Neural network** | Many layers of simple "neurons" that each do a weighted sum + activation |
| **Loss** | How wrong the model is — we try to make this smaller |
| **Gradient descent** | The algorithm that nudges parameters in the direction that reduces loss |
| **Inference** | Using the trained model to make a new prediction |

### Connection to this project
The `iam_sim.py` grid already does something AI-like: it applies a **local rule** (averaging neighbours) repeatedly and the system "settles" into a stable state. This is the core idea behind **cellular automata** and is related to **Hopfield networks** — some of the oldest neural network models.

### Good next reads
- [3blue1brown.com/neural-networks](https://www.3blue1brown.com/topics/neural-networks) — visual, no maths required
- [ml-for-humans.medium.com](https://medium.com/machine-learning-for-humans/why-machine-learning-matters-6164faf1df12) — "Machine Learning for Humans" series
- [fast.ai](https://www.fast.ai) — practical deep learning, free, project-based

---

## 4. How to connect your research to code

You have already written about **governance frameworks**, **societal tensions**, and **narrative orientation**. These ideas map naturally to computational concepts:

| Your research concept | Computational parallel |
|---|---|
| Systemic boundary | Grid boundary condition in `iam_sim.py` |
| Tension between nodes | Gradient between neighbouring cells |
| Crisis propagation | Wave spreading through a grid over time |
| Equilibrium / resolution | Stable state after many `step()` iterations |
| Meta-framework | The `iam_sim.py` CLI with pluggable modes |

A next concrete step: modify `iam_sim.py` to seed the grid with a *non-uniform* initial state (e.g. a "crisis" region with value 1500 surrounded by "normal" regions at 1000) and watch how the tension diffuses. That simulation *is* your framework running as code.

---

## 5. Practical next steps for this repository

- [ ] Run `python iam_sim.py 2d` — see your simulation working
- [ ] Read `iam_sim.py` line by line and add a comment to every function you understand
- [ ] Try changing `INIT_STANDARD = 1000.0` to `1500.0` in one patch of the grid and re-run
- [ ] Write a short `.md` note in this repo about what you observe
- [ ] Share a snippet on a [GitHub Gist](GIST.md)

---

> "I dare you to learn." — E.C.Pabel  
> You already started. Keep going.
