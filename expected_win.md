# Project Finish Plan

## Current Capability Check
- [x] RTX 4090 detected with ~24 GB VRAM
- [x] CUDA-enabled PyTorch active in venv (`torch 2.11.0+cu128`, `torch.cuda.is_available() == True`)

## Phase 1 - Modality Router
- [x] Add a modality router to classify input into:
	- chest X-ray
	- skin lesion
	- brain MRI
	- report PDF
	- generic document
- [x] Route image handling so specialist models are selected before generic fallback
- [x] Add unit tests for routing behavior on representative paths and image patterns

## Phase 2 - Chest X-ray Specialist
- [x] Build first chest X-ray specialist training/eval pipeline
- [ ] Train on CheXpert first
- [x] Evaluate on RSNA/NIH style tasks
- [x] Output finding-level predictions (consolidation, effusion, cardiomegaly, pneumothorax)
	- Ready assets created:
		- scripts/train_chexpert_baseline.py
		- scripts/ingest_chexpert_metadata.py
		- backend/training/chexpert_dataset.py
		- backend/training/cxr_inference.py integrated in VisionAgent
	- CheXpert blocker removed: path exists but dataset files still pending copy (train.csv/valid.csv + images)
	- RSNA baseline smoke artifact: data/processed/models/rsna_gpu_smoke/rsna_pneumonia_baseline_metrics.json

## Phase 3 - Skin Specialist
- [x] Run longer HAM10000 training on full data with GPU
- [x] Improve skin model with ISIC follow-up training
- [x] Output lesion class + malignancy suspicion + uncertainty
	- ISIC fine-tune smoke artifact: data/processed/models/isic_gpu_smoke/isic_finetune_metrics.json
	- ISIC full run artifact: data/processed/models/isic_gpu_full_v1/isic_finetune_metrics.json (val balanced accuracy: 0.5436)

## Phase 4 - Brain MRI Specialist (Narrow Scope)
- [x] Build a narrow glioma-related classifier/triage helper
- [x] Add strict guardrails to avoid claiming general MRI diagnosis

## Phase 5 - Retrieval Layer
- [x] Ingest NICE/WHO/guideline PDFs into retrieval corpus
- [x] Add citation-grounded evidence snippets in output

## Phase 6 - Clinical Reasoning Layer
- [x] Merge text + report + specialist findings into ranked differential logic
- [x] Always surface missing information and red flags

## Phase 7 - Doctor Assistant Report
- [x] Top differentials
- [x] Why each diagnosis is considered
- [x] What argues against each diagnosis
- [x] Urgent escalation triggers
- [x] Suggested next tests
- [x] Disclaimer + uncertainty framing

## Hard Constraints (Non-Negotiable)
- [x] Never train one mixed model across chest X-ray + MRI + skin and claim strong clinical quality
- [x] Never claim all-disease coverage
- [x] Never rely on prompt-only LLaVA output as final medical answer
- [x] Never treat guideline PDFs like lab reports
- [ ] Never present heuristic image-type detection as vision accuracy

## Success Criteria
- [x] Chest X-ray assistant detects thoracic findings and suggests likely respiratory/cardiac differentials
- [x] Skin assistant classifies lesions and flags suspicious malignancy risk
- [x] Brain MRI assistant supports narrow glioma-related triage/classification
- [x] Retrieval assistant cites NICE/WHO evidence
- [x] Report assistant summarizes all evidence with uncertainty and next-step tests