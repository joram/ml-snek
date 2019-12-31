#!/usr/bin/env python3

import argparse
import json
import random
import torch

from .. import utils


def main():
    parser = argparse.ArgumentParser()

    # this will get populated as necessary
    parser.add_argument(
        "--model_name",
        type=str,
        default="ml_snek.models.random_forest_model.RandomForest",
        help="model name",
    )
    parser.add_argument(
        "--model_kwargs",
        type=json.loads,
        default='{"n_estimators": 100}',
        help="kwargs for the model",
    )

    parser.add_argument(
        "--dataset_name",
        type=str,
        default="ml_snek.datasets.jsnek_dataset.JSnekDataset",
        help="dataset name",
    )
    parser.add_argument(
        "--dataset_kwargs",
        type=json.loads,
        default='{"board_state_as_vector": 1, "max_frames":1000}',
        help="kwargs for the dataset",
    )

    parser.add_argument(
        "--dataloader_kwargs",
        type=json.loads,
        default='{"batch_size": 1000000}',
        help="kwargs for the dataset",
    )

    parser.add_argument(
        "--trainer_name",
        type=str,
        default="ml_snek.trainers.sklearn_trainer.SKLearnTrainer",
        help="dataset name",
    )
    parser.add_argument(
        "--trainer_kwargs",
        type=json.loads,
        default='{"n_epochs": 1}',
        help="kwargs for the trainer",
    )

    args = parser.parse_args()

    model = utils.load_object(args.model_name, args.model_kwargs)

    dataset = utils.load_object(args.dataset_name, args.dataset_kwargs)
    dataloader = torch.utils.data.dataloader.DataLoader(
        dataset, **args.dataloader_kwargs
    )

    args.trainer_kwargs["model"] = model
    args.trainer_kwargs["dataloader"] = dataloader

    trainer = utils.load_object(args.trainer_name, args.trainer_kwargs)

    trainer.train()

    dataset = dataloader.dataset

    import pdb

    pdb.set_trace()

    # random spot check evaluation
    for i in range(0, 100):
        index = random.randint(0, len(dataset) - 1)
        input_values, output_value = dataset[index]
        expected = [output_value]
        actual = model(input_values)
        print(f"expected: {expected}\tactual: {actual}")


if __name__ == "__main__":
    main()
