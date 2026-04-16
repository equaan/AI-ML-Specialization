# Manual Test Assets

This folder contains real sample assets copied from `data/raw` for manual UI/API testing.

## Included Data

- `images/ham10000/`
  - 20 real dermatology images (`ISIC_*.jpg`) copied from HAM10000.
- `reports/guidelines/`
  - 3 real clinical guideline PDFs copied from `data/raw/guidelines/`.
- `metadata/HAM10000_metadata.csv`
  - HAM10000 metadata to inspect lesion labels and context.
- `cases/medqa/`
  - `mainland_train_sample_source.jsonl`
  - `mainland_dev_sample_source.jsonl`
  - Real MedQA case/question datasets copied from `data/raw/medqa`.

## How to Use in App

- Upload one image from `images/ham10000/` in the New Analysis flow.
- Upload one PDF from `reports/guidelines/` as the report input.
- Copy symptom/case text from `cases/medqa/*.jsonl` entries into the symptom text area.

## Note on X-ray Data

`data/raw/mimic_cxr/` is currently empty in this workspace, so no genuine chest X-ray files were available to copy yet.
When X-ray files are added there, copy a subset into `manual-test/images/xray/` for chest imaging tests.
