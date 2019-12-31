from torch.utils.data import DataLoader


def test_flat_dataloader(dataset_jsnek):

    batch_size = 32

    dataloader = DataLoader(dataset_jsnek, batch_size=batch_size)

    first_item = dataloader.__iter__().__next__()

    assert type(first_item) == list

    assert len(first_item) == 2

    for i in range(len(first_item)):

        assert len(first_item[i]) == batch_size
