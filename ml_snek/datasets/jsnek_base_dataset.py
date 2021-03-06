import json
import os
from torch.utils.data import Dataset


class JSnekBaseDataset(Dataset):

    CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(CURR_DIR, "../../data/")
    CACHED_FRAMES = {}

    def __init__(self, max_frames=-1):
        self._files = self._existing_files()
        self._n_frames = max_frames

        # load cached
        counts_filepath = os.path.join(self.DATA_DIR, "valid_indices.json")
        if os.path.exists(counts_filepath):
            with open(counts_filepath, "r") as f:
                self._index_map = json.load(f)
                self._n_frames = len(self._index_map.keys()) - 1
                if max_frames != -1:
                    self._n_frames = max_frames

            if len(self._files) == self._index_map[str(-1)]:
                return

        # create index map
        self._index_map = {}
        global_index = 0
        for filepath in self._files:
            with open(filepath, "r") as f:

                try:
                    frames = json.load(f)
                except json.decoder.JSONDecodeError:
                    continue

                try:
                    winner_id = self._get_winner_id(frames)

                except:
                    # print(filepath, frames)
                    raise

                if winner_id is None:
                    continue

                for file_index in range(0, len(frames) - 1):
                    try:
                        self._get_direction(
                            frames[file_index], frames[file_index + 1], winner_id
                        )
                    except KeyError as e:
                        continue
                    self._index_map[global_index] = {
                        "index": file_index,
                        "filepath": filepath,
                    }
                    global_index += 1
        self._index_map[-1] = len(self._files)
        self._n_frames = len(self._index_map.keys()) - 1

        # save cache
        with open(counts_filepath, "w") as f:
            f.write(json.dumps(self._index_map, indent=4, sort_keys=True))

        if max_frames != -1:
            self._n_frames = max_frames

        print(f"have {len(self._files)} games, and {self._n_frames} frames")

    def __len__(self):
        return self._n_frames

    def _existing_files(self):
        files = []
        for r, d, f in os.walk(self.DATA_DIR):
            for file in f:
                if ".json" in file and file != "valid_indices.json":
                    files.append(os.path.join(r, file))
        return files

    def _get_direction(self, frame, next_frame, winner_id):
        head = None
        for snake in frame["board"]["snakes"]:
            if snake["id"] == winner_id:
                head = snake["body"][0]
                break

        next_head = None
        for snake in next_frame["board"]["snakes"]:
            if snake["id"] == winner_id:
                next_head = snake["body"][0]
                break

        if head is None or next_head is None:
            raise KeyError("missing head")

        delta_x = next_head["x"] - head["x"]
        delta_y = next_head["y"] - head["y"]
        direction = {(0, 1): "UP", (0, -1): "DOWN", (1, 0): "RIGHT", (-1, 0): "LEFT"}[
            (delta_x, delta_y)
        ]
        return direction

    def _get_winner_id(self, frames):
        snakes = frames[-1]["board"]["snakes"]
        try:
            winner_id = snakes[0]["id"]
        except IndexError:
            return None
        return winner_id

    def _get_frames_from_file(self, global_index):
        metadata = self._index_map[str(global_index)]
        filepath = metadata["filepath"]
        frame_index = metadata["index"]

        results = self.CACHED_FRAMES.get(filepath)
        if results is not None:
            return results

        with open(filepath) as f:
            content = f.read()
        frames = json.loads(content)

        self.CACHED_FRAMES[filepath] = (frames, frame_index)
        return frames, frame_index

    def __getitem__(self, index):

        if 0 > index:
            raise IndexError
        if index >= len(self):
            raise IndexError

        frames, frame_index = self._get_frames_from_file(index)
        frame = frames[frame_index]
        next_frame = frames[frame_index + 1]
        direction = self._get_direction(frame, next_frame, self._get_winner_id(frames))

        return frame, self._get_winner_id(frames), direction
