import os
import warnings
import pickle

from .base_model import BaseModel
from sklearn.ensemble import RandomForestClassifier


class RandomForest(BaseModel):
    def __init__(self, **kwargs):
        self.model = RandomForestClassifier(**kwargs)

    def train(self, input_values, expected_output):
        self.model.fit(input_values, expected_output)

    def __call__(self, input_values):

        if len(input_values.size()) == 1:
            input_values = input_values.view(1, len(input_values))

        return self.model.predict(input_values)

    def save(self, save_path, overwrite=False):

        if os.path.exists(save_path):
            warnings.warn(
                "Save path {} already exists and overwrite=False. The model was not saved.".format(
                    save_path
                )
            )
            return

        with open(save_path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, save_path):

        with open(save_path, "rb") as f:
            self.model = pickle.load(f)
