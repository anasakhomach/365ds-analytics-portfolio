# Streamlit Cloud Portfolio Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the complete 365DS repository and deploy one Streamlit Community Cloud multipage portfolio with stable deep links to all five dashboards and the Learning Hub.

**Architecture:** Keep `apps/learning-hub/streamlit_app.py` as the single router. Register existing dashboard scripts as internal `st.Page` pages, resolve committed Gold-only cloud snapshots before local warehouses, and build the local TF-IDF index automatically when missing or stale. Preserve standalone local dashboards and Gold-only executable SQL guardrails.

**Tech Stack:** Python 3.13, Streamlit 1.58+, DuckDB 1.5+, pandas, Plotly, scikit-learn, OpenAI-compatible provider adapter, pytest, GitHub, Streamlit Community Cloud.

---

## Chunk 1: Cloud Data And Index Foundations

### Task 1: Cloud warehouse resolver

**Files:**
- Create: `apps/learning-hub/learning_hub/cloud_data.py`
- Create: `apps/learning-hub/tests/test_cloud_data.py`
- Modify: `apps/learning-hub/learning_hub/catalog.py`

- [ ] Write tests proving committed cloud snapshots override local warehouses and local warehouses remain the fallback.
- [ ] Run the focused test and confirm it fails before implementation.
- [ ] Implement `cloud_snapshot_path()` and `resolve_warehouse_path()`.
- [ ] Update catalog projects to retain source warehouse paths while exposing the resolved runtime path.
- [ ] Run focused catalog/cloud-data tests.

### Task 2: Gold-only snapshot builder

**Files:**
- Create: `apps/learning-hub/scripts/build_cloud_snapshots.py`
- Extend: `apps/learning-hub/tests/test_cloud_data.py`
- Modify: `.gitignore`

- [ ] Write a failing test that generates a snapshot from a temporary DuckDB source.
- [ ] Require the output to contain only the `gold` schema and approved tables.
- [ ] Implement snapshot generation and validation.
- [ ] Add a narrow gitignore exception for `apps/learning-hub/data/*.duckdb`.
- [ ] Generate and validate five release snapshots.

### Task 3: Automatic TF-IDF bootstrap

**Files:**
- Modify: `apps/learning-hub/learning_hub/indexing.py`
- Modify: `apps/learning-hub/streamlit_app.py`
- Extend: `apps/learning-hub/tests/test_indexing.py`

- [ ] Write tests for missing and stale local indexes.
- [ ] Implement `ensure_local_index()` using manifest source hashes.
- [ ] Make the cached Streamlit index call ensure the local index before loading it.
- [ ] Run focused index tests.

## Chunk 2: Multipage Dashboard Integration

### Task 4: Stable navigation registry

**Files:**
- Create: `apps/learning-hub/learning_hub/navigation.py`
- Create: `apps/learning-hub/tests/test_navigation.py`
- Modify: `apps/learning-hub/streamlit_app.py`

- [ ] Write tests for unique stable pathnames and all five project pages.
- [ ] Define page metadata for root, explorer, five dashboards, AI helper, quiz/data, and lineage.
- [ ] Register project dashboard files with `st.Page` and explicit `url_path` values.
- [ ] Keep existing function pages for Learning Hub views.

### Task 5: Dashboard cloud path resolution and proof links

**Files:**
- Modify: each `projects/*/dashboard/app.py`
- Modify: `apps/learning-hub/catalog/projects.yaml`

- [ ] Add a small shared resolver import/bootstrap that works when dashboard scripts run standalone or as pages.
- [ ] Keep local project warehouse behavior when no cloud snapshot exists.
- [ ] Add project GitHub/report/retrospective links using `LEARNING_HUB_REPO_URL`.
- [ ] Verify every dashboard still compiles and only references Gold tables.

## Chunk 3: Community Cloud Packaging

### Task 6: Dependencies, config, and secrets contract

**Files:**
- Create: `apps/learning-hub/requirements.txt`
- Create: `.streamlit/config.toml`
- Modify: `.env.example`
- Modify: `apps/learning-hub/README.md`

- [ ] Add a minimal pinned runtime dependency set.
- [ ] Add one root Streamlit theme/server config without secrets.
- [ ] Document Community Cloud entrypoint, Python version, secrets, and subdomain setup.
- [ ] Document that the complete repo is public while executable SQL remains Gold-only.

### Task 7: Cloud-parity tests and smoke checks

**Files:**
- Modify/Create tests under `apps/learning-hub/tests/`

- [ ] Run the full Learning Hub test suite.
- [ ] Compile the hub and all dashboard entrypoints.
- [ ] Build/index check and generate cloud snapshots.
- [ ] Start Streamlit from the repository root and verify root plus all deep links.
- [ ] Run mobile/desktop browser screenshots if browser automation is available.

## Chunk 4: Publication And Deployment

### Task 8: Git history and public repository

**Files:** Git metadata only.

- [ ] Review all staged/untracked changes and scan for secrets.
- [ ] Commit the existing Learning Hub/provider/retrospective work in coherent commits.
- [ ] Commit cloud deployment foundations and navigation separately.
- [ ] Create a public GitHub repository under `anasakhomach`.
- [ ] Add `origin`, push the stable branch, and verify repository visibility.

### Task 9: Streamlit Community Cloud deployment

- [ ] Create one Community Cloud app from `apps/learning-hub/streamlit_app.py`.
- [ ] Select Python 3.13 if the build supports it; fall back to 3.12 only if dependency compatibility requires it.
- [ ] Configure owner provider key and public repo URL through Streamlit secrets.
- [ ] Choose a stable subdomain and record it in docs/environment examples.
- [ ] Verify all LinkedIn deep links, dashboard queries, AI fallback, BYOK, and Gold SQL validation.

## Completion Gate

- [ ] Five dashboards are internal pages in one app.
- [ ] Standalone local dashboard commands still work.
- [ ] All project code and source assets are present in the public GitHub repo.
- [ ] Cloud runtime uses validated Gold-only snapshots.
- [ ] Missing/stale TF-IDF index rebuilds automatically.
- [ ] Full tests, compile checks, snapshot checks, and HTTP/deep-link smoke checks pass.
- [ ] No secrets are committed or printed.
- [ ] Repo memory and deployment README are current.

