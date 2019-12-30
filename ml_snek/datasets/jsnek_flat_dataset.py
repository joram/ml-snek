"""
jsnek_saved_games_dataset that returns flat (vectorized) data
"""

from .jsnek_saved_games_dataset import JSnekDataset


class JSnekFlatDataset(JSnekDataset):

    def __init__(self, jsnek_dataset=None):
        super(self)

        if jsnek_dataset is None:
            jsnek_dataset = JSnekDataset

    def __getitem__(self, index):
        item = super(self)[index]

        # flatten this somehow

        return

