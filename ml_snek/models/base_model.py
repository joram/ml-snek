class BaseModel(object):
    def save(self, save_path):
        raise NotImplementedError()

    def load(self, save_path):
        raise NotImplementedError()

    def train(self, input_values, expected_output):
        raise NotImplementedError()
