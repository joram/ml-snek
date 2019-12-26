

class BaseTrainer(object):

    def save(self):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()

    def train(self):
        raise NotImplementedError()
