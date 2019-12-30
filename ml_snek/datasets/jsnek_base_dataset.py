import json
import os
from torch.utils.data import Dataset


class JSnekBaseDataset(Dataset):
    """
    Base dataset, returns dictionary of board state, winner ID, and the move the winner took that turn
    """

    CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(CURR_DIR, "../../data/")

    def __init__(self):
        self._winner_id = None
        self._files = self._existing_files()
        self._n_frames = -1

        # load cached
        counts_filepath = os.path.join(self.DATA_DIR, "valid_indices.json")
        if os.path.exists(counts_filepath):
            with open(counts_filepath, "r") as f:
                self._index_map = json.load(f)
                self._n_frames = len(self._index_map.keys()) - 1

            if len(self._files) == self._index_map["file_count"]:
                return

        # create index map
        self._index_map = {}
        global_index = 0
        for filepath in self._files:
            with open(filepath, "r") as f:
                try:
                    frames = json.load(f)
                    for file_index in range(0, len(frames) - 1):
                        self._get_direction(
                            frames[file_index], frames[file_index + 1],
                        )
                        self._index_map[global_index] = {
                            "index": file_index,
                            "filepath": filepath,
                        }
                except KeyError:
                    pass
                except TypeError:
                    pass
                except json.decoder.JSONDecodeError:
                    pass
        self._index_map["file_count"] = len(self._files)
        self._n_frames = len(self._index_map.keys()) - 1

        # save cache
        with open(counts_filepath, "w") as f:
            f.write(json.dumps(self._index_map))

        print(f"have {len(self._files)} games, and {self._n_frames} frames")

    def _existing_files(self):
        files = []
        for r, d, f in os.walk(self.DATA_DIR):
            for file in f:
                if ".json" in file:
                    files.append(os.path.join(r, file))
        return files

    def _get_direction(self, frame, next_frame):
        head = None
        for snake in frame["board"]["snakes"]:
            if snake["id"] == self._get_winner_id():
                head = snake["body"][0]
                break

        next_head = None
        for snake in next_frame["board"]["snakes"]:
            if snake["id"] == self._get_winner_id():
                next_head = snake["body"][0]
                break

        if head is None or next_head is None:
            raise KeyError

        delta_x = next_head["x"] - head["x"]
        delta_y = next_head["y"] - head["y"]
        direction = {(0, 1): "UP", (0, -1): "DOWN", (1, 0): "RIGHT", (-1, 0): "LEFT"}[
            (delta_x, delta_y)
        ]
        return direction

    def _get_winner_id(self):
        if self._winner_id is not None:
            return self._winner_id

        filepath = self._files[-1]
        with open(filepath) as f:
            content = f.read()
        frames = json.loads(content)

        snakes = frames[-1]["board"]["snakes"]
        winner_id = snakes[0]["id"]
        self._winner_id = winner_id
        return winner_id

    def __len__(self):
        return self._n_frames

    def __getitem__(self, index):

        if 0 > index:
            raise IndexError
        if index >= len(self):
            raise IndexError

        metadata = self._index_map[str(index)]
        filepath = metadata["filepath"]
        frame_index = metadata["index"]
        with open(filepath) as f:
            content = f.read()
        frames = json.loads(content)
        frame = frames[frame_index]
        next_frame = frames[frame_index + 1]
        direction = self._get_direction(frame, next_frame)

        return frame, self._get_winner_id(), direction
