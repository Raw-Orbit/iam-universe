# What is a GitHub Gist — and what can you use it for?

> *"Is that something for a gist? For what can I use a gist?"* — E.C.Pabel

---

## What is a Gist?

A **GitHub Gist** is a lightweight way to share code, text, or notes with the world — without needing a full repository.

Think of it as a **single-file (or small multi-file) pastebin with version history**, owned by your GitHub account.

- Gists live at: [gist.github.com](https://gist.github.com)
- Every gist is secretly a **git repository** — so it has full version history.
- Gists can be **public** (discoverable, shareable) or **secret** (only accessible via the direct link).

---

## When should you use a Gist vs. a Repository?

| Situation | Gist ✅ | Repository ✅ |
|---|---|---|
| Share a quick code snippet | ✅ | |
| Share a single config file | ✅ | |
| Write a short note / idea draft | ✅ | |
| Build a full project with multiple files | | ✅ |
| Track issues, pull requests, wikis | | ✅ |
| Collaborate with a team on a codebase | | ✅ |

**Rule of thumb:** if it fits in one file and you just want to share it, use a Gist. If it's a project, use a repository.

---

## Practical uses for this project (i.am / Vibe Wizzards Wyrd)

Here are concrete things you could put in a Gist right now:

### 1. Share a standalone simulation snippet
Paste just the core `step()` function from `iam_sim.py` so people can copy-paste it into their own notebooks.

### 2. Share a research note or concept draft
You can write a `.md` file in a Gist. Great for sharing early-stage ideas before they belong in a repo.

### 3. Log experiment results
Run the simulation, copy the terminal output, paste it in a Gist. Share the link in a GitHub Issue as a reference.

### 4. Share configuration examples
A short `config.json` or `.env.example` — things too small to need their own repo.

### 5. Create an embeddable code demo
Gists can be embedded in websites and blog posts:
```html
<script src="https://gist.github.com/MaxLvNPC/YOUR_GIST_ID.js"></script>
```

---

## How to create your first Gist

1. Go to [gist.github.com](https://gist.github.com)
2. Log in with your GitHub account (@MaxLvNPC)
3. Give the file a name (e.g. `iam_step.py`) and paste your content
4. Choose **Public** or **Secret**
5. Click **Create public gist** (or secret)

That's it — you get a shareable URL instantly.

---

## The difference in one sentence

> A **repository** is a project home. A **Gist** is a sticky note you can share with the world.

---

*See also: [LEARNING.md](LEARNING.md) — a roadmap for understanding how computers and AI work.*
