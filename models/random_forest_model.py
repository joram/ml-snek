from models.base_model import BaseModel
from sklearn.ensemble import RandomForestClassifier


class RandomForestModel(BaseModel):

    def __init__(self):
        self.model = RandomForestClassifier(n_jobs=2, random_state=0)

    def train(self, input_values, expected_output):
        self.model.fit(input_values, expected_output)
