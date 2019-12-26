#!/usr/bin/env python3
from torch.utils.data import DataLoader
from datasets.jsnek_saved_games_dataset import JSnekDataset

# Parameters
params = {
    'batch_size': 64,
    'shuffle': True,
    'num_workers': 6,
}


dataset = JSnekDataset()
dataloader = DataLoader(dataset, **params)
# model =
# trainer =