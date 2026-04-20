import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from scripts.train_ham10000_baseline import _evaluate_predictions


class FixedLogitModel(nn.Module):
    def __init__(self, logits: torch.Tensor) -> None:
        super().__init__()
        self.register_buffer("logits", logits)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        batch_size = inputs.size(0)
        return self.logits[:batch_size]


def test_evaluate_predictions_includes_macro_f1_and_confusion_matrix() -> None:
    inputs = torch.zeros((4, 3, 32, 32), dtype=torch.float32)
    labels = torch.tensor([0, 1, 1, 2], dtype=torch.long)
    loader = DataLoader(TensorDataset(inputs, labels), batch_size=4, shuffle=False)

    logits = torch.tensor(
        [
            [8.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 6.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 6.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 7.0, 0.0, 0.0, 0.0, 0.0],
        ],
        dtype=torch.float32,
    )
    model = FixedLogitModel(logits)

    metrics = _evaluate_predictions(model, loader, device=torch.device("cpu"))

    assert "macro_f1" in metrics
    assert "confusion_matrix" in metrics
    assert "confusion_matrix_labels" in metrics
    matrix = metrics["confusion_matrix"]
    assert len(matrix) == 7
    assert all(len(row) == 7 for row in matrix)
    assert matrix[0][0] == 1
    assert matrix[1][1] == 1
    assert matrix[1][2] == 1
    assert matrix[2][2] == 1
