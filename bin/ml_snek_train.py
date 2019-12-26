#!/usr/bin/env python3
from torch.utils.data import DataLoader
from dataloaders.dataloader import Dataloader
from datasets.jsnek_saved_games_dataset import JSnekDataset
from models.random_forest_model import RandomForestModel
from trainers.basic_trainer import BasicTrainer

dataset = JSnekDataset()
# dataloader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=0)
dataloader = Dataloader(dataset)
model = RandomForestModel()
trainer = BasicTrainer(model, dataloader)
trainer.train(epocs=5)
