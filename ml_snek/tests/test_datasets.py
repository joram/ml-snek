import pytest

from ..datasets.jsnek_saved_games_dataset import JSnekDataset


def test_jsnek_dataset():
    dataset = JSnekDataset()

    assert len(dataset)

    assert dataset[0]

    assert dataset[len(dataset) - 1]

    with pytest.raises(IndexError):
        dataset[-1]

    with pytest.raises(IndexError):
        dataset[len(dataset)]
