# IE305 — product launch through word of mouth

Mihir Vasave and Vaibhav Mathur · Simulation Lab

We are building a synthetic campus market for a new reusable bottle. The decision is which price and fixed-budget free-sample strategy produces the most modeled profit, and how random versus similar-contact recommendations affect diffusion.

**Current build is in progress.** See [PROJECT_JOURNAL.md](PROJECT_JOURNAL.md) for progress, issues, lessons and fixes, and [the product model specification](handoff_output/product_launch/MODEL_SPEC.md) for the exact assumptions. Existing opinion/network experiments are a foundation, not simulated sales results.

All inputs are synthetic. No claim is made to predict actual campus customers. AI assistance is used for research, programming, experiments and drafting. Actual AnyLogic compilation and runtime evidence must be obtained by the students; prepared Java text is not evidence that AnyLogic ran.

## Repository commands in this managed workspace

The workspace's root `.git` directory is read-only. Git metadata therefore lives in `.git-storage`, using Git's supported alternate metadata option. The tracked working directory is still this project:

```sh
./project-git status
./project-git log --oneline
```

Commits use the user's configured identity. To publish the explicitly requested **public** GitHub repository, use:

```sh
./publish_github.sh
```

The current tool environment cannot connect to `api.github.com`. Run publishing from a normal terminal with GitHub connectivity and an authenticated `gh` session. If necessary authenticate with `gh auth login` first. No token should be pasted into project files or chat. Once cloned from GitHub, the repository will use an ordinary `.git` directory.

The original supplied handoff is preserved in `handoff/`; upgraded research and reproducibility evidence are in `handoff_output/`. Final product-specific results and presentation material will be under `handoff_output/product_launch/`.
