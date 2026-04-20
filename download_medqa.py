from datasets import load_dataset

print("Downloading MedQA dataset...")

dataset = load_dataset("fzkuji/MedQA")

dataset.save_to_disk("data/raw/text/medqa")

print("MedQA download complete.")
print("Saved to: data/raw/text/medqa")