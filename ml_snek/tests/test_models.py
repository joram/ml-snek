import os

from ..models.random_forest_model import RandomForest


def save_load_tests(model, save_path):
    # right now do this without throwing an error
    model.save(save_path)

    assert os.path.exists(save_path)

    model.load(save_path)


def test_random_forest(tmpdir):
    model = RandomForest()

    save_load_tests(model, "{}/model.pkl".format(tmpdir))
