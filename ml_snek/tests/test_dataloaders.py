from torch.utils.data import DataLoader


def test_flat_dataloader(dataset_jsnek):

    dataloader = DataLoader(dataset_jsnek)
    first_item = dataloader.__iter__().__next__()

    assert type(first_item) == tuple

    assert len(first_item) == 2

    assert len(first_item[0]) == 484

    assert type(first_item[1]) == int
