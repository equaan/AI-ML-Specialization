from datasets import load_dataset

print("Downloading MedMCQA dataset...")

dataset = load_dataset("openlifescienceai/medmcqa")

dataset.save_to_disk("data/raw/text/medmcqa")

print("MedMCQA download complete.")
print("Saved to: data/raw/text/medmcqa")