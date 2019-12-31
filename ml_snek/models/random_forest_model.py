from .base_model import BaseModel
from sklearn.ensemble import RandomForestClassifier


class RandomForest(BaseModel):

    def __init__(self, **kwargs):
        self.model = RandomForestClassifier(**kwargs)

    def train(self, input_values, expected_output):
        self.model.fit(input_values, expected_output)
