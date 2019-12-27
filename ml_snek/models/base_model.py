

class BaseModel(object):

    def save(self):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

    def train(self, input_values, expected_output):
        raise NotImplementedError()
