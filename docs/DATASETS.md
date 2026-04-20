# DATASETS.md - MediAgent Dataset Download Guide

This file tells you exactly what to download, from where, and where to place it.

## 1) Canonical local dataset folders

Run from repo root:

```powershell
mkdir data\raw\text\medqa -Force
mkdir data\raw\text\medmcqa -Force
mkdir data\raw\skin\ham10000 -Force
mkdir data\raw\cxr\kaggle_pneumonia -Force
mkdir data\raw\mri\utsw_glioma -Force
mkdir data\raw\guidelines -Force
```

Recommended canonical paths used by the repo now:

- `data/raw/text/medqa/`
- `data/raw/text/medmcqa/`
- `data/raw/skin/ham10000/`
- `data/raw/cxr/kaggle_pneumonia/`
- `data/raw/mri/utsw_glioma/`
- `data/raw/guidelines/`

## 2) Required datasets and sources

### A. MedQA (for RAG knowledge base)
- Purpose: Populate Chroma collection `medqa_chunks`
- Source: Hugging Face `bigbio/med_qa`
- URL: https://huggingface.co/datasets/bigbio/med_qa
- Local target folder: `data/raw/text/medqa/`

Recommended (no manual download needed):
- Use ingestion script directly:

```powershell
.\venv\Scripts\python scripts\ingest_medqa.py --limit 500 --split train
```

Optional (cache datasets locally):

```powershell
.\venv\Scripts\python -c "from datasets import load_dataset; ds=load_dataset('bigbio/med_qa', name='med_qa_en_source', split='train'); print(len(ds))"
```

### B. PubMed abstracts (live retrieval)
- Purpose: Populate Chroma collection `pubmed_abstracts`
- Source: NCBI E-utilities (PubMed)
- URL: https://pubmed.ncbi.nlm.nih.gov/
- Local target folder: Stored into Chroma directly (no raw files required)

Run:

```powershell
.\venv\Scripts\python scripts\ingest_pubmed.py --queries "pneumonia,covid pneumonitis,pulmonary edema" --max-results-per-query 20
```

### C. MedMCQA (for evaluation)
- Purpose: End-to-end benchmark in Phase 5
- Source: Hugging Face `medmcqa`
- URL: https://huggingface.co/datasets/medmcqa
- Local target folder: `data/raw/text/medmcqa/`

Quick check:

```powershell
.\venv\Scripts\python -c "from datasets import load_dataset; ds=load_dataset('medmcqa', split='train'); print(len(ds))"
```

### D. HAM10000 (for vision evaluation)
- Purpose: Skin lesion image evaluation
- Sources:
  - Kaggle (official): https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
  - Hugging Face mirrors (if needed)
- Local target folder: `data/raw/skin/ham10000/`

Kaggle CLI steps:

```powershell
pip install kaggle
# Put kaggle.json at: C:\Users\<you>\.kaggle\kaggle.json
kaggle datasets download -d kmader/skin-cancer-mnist-ham10000 -p data\raw\ham10000
Expand-Archive -Path data\raw\ham10000\skin-cancer-mnist-ham10000.zip -DestinationPath data\raw\ham10000 -Force
```

### E. MIMIC-CXR (optional, access-gated)
- Purpose: Chest X-ray evaluation (advanced)
- Source: PhysioNet
- URL: https://physionet.org/content/mimic-cxr/
- Notes: Requires credentialing and data use agreement
- Local target folder: `data/raw/mri/utsw_glioma/` for MRI work, or `data/raw/mimic_cxr/` if you later obtain MIMIC-CXR access.

### F. Clinical guideline PDFs (recommended)
- Purpose: Knowledge grounding and citations
- Sources:
  - WHO: https://www.who.int/publications
  - CDC: https://www.cdc.gov/guidelines/
  - NICE: https://www.nice.org.uk/guidance
- Local target folder: `data/raw/guidelines/`

Suggested starter files:
- Community-acquired pneumonia guideline PDF
- Sepsis recognition guideline PDF
- Acute chest pain evaluation guideline PDF

## 3) Minimal dataset set to start now

If you want the fastest path to unblock development, do this first:
1. Put MedQA under `data/raw/text/medqa/`
2. Put MedMCQA under `data/raw/text/medmcqa/`
3. Put HAM10000 under `data/raw/skin/ham10000/`
4. Put the Kaggle pneumonia dataset under `data/raw/cxr/kaggle_pneumonia/`
5. Put guideline PDFs under `data/raw/guidelines/`
6. Run `python scripts/audit_local_datasets.py`

## 4) Verification checklist

After ingestion/download:

```powershell
.\venv\Scripts\python scripts\setup_chromadb.py
.\venv\Scripts\python -m pytest -q
```

Then start API:

```powershell
.\venv\Scripts\python -m uvicorn backend.main:app --reload --port 8000
```

When Ollama is installed and models are pulled, validate:
- `GET /api/models/status`
- `POST /api/analyze` with real image + symptoms

## 5) Practical notes
- `MIMIC-CXR` is optional for now due access overhead.
- Start with `llava:7b` if RAM is limited, upgrade to `llava:13b` later.
- Keep raw downloads under `data/raw/` only and prefer the canonical subfolders above.
- Chroma data is generated under `data/chromadb/` and is gitignored.
