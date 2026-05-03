# services/dataset_loader.py
# Loads sample risk data from HuggingFace for testing

from datasets import load_dataset

def load_sample_risks():
    """
    Load a small financial dataset from HuggingFace.
    We use 'financial_phrasebank' as it's small and free.
    Returns a list of sample risk scenario strings.
    """
    try:
        dataset = load_dataset(
            "financial_phrasebank",
            "sentences_allagree",
            split="train",
            trust_remote_code=True
        )
        # Take first 10 entries as sample risk scenarios
        samples = []
        for i, item in enumerate(dataset):
            if i >= 10:
                break
            samples.append({
                "id": i + 1,
                "description": item["sentence"],
                "sentiment": item["label"]
            })
        return samples
    except Exception as e:
        # Return mock data if HuggingFace is unavailable
        return [
            {"id": 1, "description": "Credit default risk due to borrower insolvency", "sentiment": 0},
            {"id": 2, "description": "Market volatility causing portfolio losses", "sentiment": 0},
            {"id": 3, "description": "Operational failure in trading systems", "sentiment": 0},
        ]