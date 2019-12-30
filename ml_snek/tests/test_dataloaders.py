from torch.utils.data import DataLoader


def test_flat_dataloader(dataset_jsnek):

    dataloader = DataLoader(dataset_jsnek, batch_size=32, shuffle=True)

    # import pdb

    # pdb.set_trace()

    pass
