#!/usr/bin/env python3
from ..dataloaders.dataloader import Dataloader
from ..datasets.jsnek_saved_games_dataset import JSnekDataset
from ..models.random_forest_model import RandomForestModel
from ..trainers.basic_trainer import BasicTrainer


def main():
    dataset = JSnekDataset()
    # dataloader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=0)
    dataloader = Dataloader(dataset)
    model = RandomForestModel()
    trainer = BasicTrainer(model, dataloader)
    trainer.train(epochs=500)

    i = 0
    for data in dataloader:
        input_values = [list(data["input"][key].values()) for key in ['body', 'food', 'my_head', 'their_heads']]
        output_value = {
            "UP": 0,
            "DOWN": 1,
            "LEFT": 2,
            "RIGHT": 3,
        }[data["output"]]
        expected = [output_value] * 4
        actual = model.model.predict(input_values)
        print(f"expected: {expected}\tactual: {actual}")
        if i > 10:
            break
        i += 1


if __name__ == '__main__':
    main()
