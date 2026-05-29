# Project Log

Cross-session log for tracking pattern recognition, open follow-ups, and structural changes. See `tools/session-retro.md` for the convention.

---

## 2026-05-28 — Reasoning frameworks expansion

**Type:** feature + docs

**What changed:**
- Added 5 reasoning frameworks to `pipeline/frameworks.json`: INV (Inversion), SOT (Second-Order Thinking), BAY (Bayesian / Probabilistic), CYN (Cynefin), STL (Steelman). Total now 13.
- Added 4 pipeline variants to `pipeline/pipeline.py`: `classify-first` (CYN opener), `inversion` (INV-led), `uncertainty` (BAY opener), `dialectic` (STL + AdR). Total now 10.
- Documented the stage-accumulation mechanism in `reasoning-pipeline.md`: each stage reasons over the original problem plus everything earlier stages discovered, so the lead framework determines the category of the final answer.
- Encoded the rule that CYN/BAY/SOT are diagnostic (characterize but don't recommend) and must be followed by a generative closer (ToT or GoT). STL is redundant when SMR + AdR are both already in the chain.

**Verification:**
- `python3 pipeline/pipeline.py frameworks` lists 13.
- `python3 pipeline/pipeline.py pipelines` lists 10 (6 existing + 4 new).
- `frameworks.json` parses cleanly.
- `pytest` not runnable in the local sandbox (no module); rerun in a Python env with pytest installed to confirm 13/13.

**Open follow-ups:**
- Per `EVIDENCE.md` discipline, each new framework should be shown on real runs to surface material the existing 8 miss before being treated as validated. Right now they are **plausible, not validated**. The package was tested for loading/listing, not for output quality.
- The shipped CLI is still the directional v3-style reference (per `pipeline/README.md` banner). These additions extend the directional shape; they do not move the CLI toward being the v4 harness the experiments ran on.
