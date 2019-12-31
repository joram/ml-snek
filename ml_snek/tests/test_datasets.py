import pytest

from ..datasets.jsnek_base_dataset import JSnekBaseDataset
from ..datasets.jsnek_dataset import JSnekDataset


def dataset_tests(dataset):
    assert len(dataset)

    assert dataset[0]

    assert dataset[len(dataset) - 1]

    with pytest.raises(IndexError):
        dataset[-1]

    with pytest.raises(IndexError):
        dataset[len(dataset)]


def test_jsnek_base_dataset():
    jsnek_dataset = JSnekBaseDataset()
    dataset_tests(jsnek_dataset)

    assert len(jsnek_dataset) > 1000

    jsnek_dataset = JSnekBaseDataset(10)

    assert len(jsnek_dataset) == 10


def test_jsnek_dataset():
    jsnek_flat_dataset = JSnekDataset(board_state_as_vector=False)
    dataset_tests(jsnek_flat_dataset)

    board_state, direction = jsnek_flat_dataset[0]
    assert len(board_state.shape) == 3
    assert len(direction) == 4

    jsnek_flat_dataset = JSnekDataset(board_state_as_vector=True)
    dataset_tests(jsnek_flat_dataset)

    board_state, direction = jsnek_flat_dataset[0]
    assert len(board_state.shape) == 1
    assert len(direction) == 4

    jsnek_flat_dataset = JSnekDataset(
        board_state_as_vector=False, direction_as_index=True
    )
    dataset_tests(jsnek_flat_dataset)

    board_state, direction = jsnek_flat_dataset[0]
    assert len(direction) == 1

    assert len(jsnek_flat_dataset) > 1000

    jsnek_flat_dataset = JSnekDataset(max_size=10)

    assert len(jsnek_flat_dataset) == 10
