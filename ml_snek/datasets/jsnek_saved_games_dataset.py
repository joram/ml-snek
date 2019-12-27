import json
import os
from torch.utils.data import Dataset


class JSnekDataset(Dataset):

    CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(CURR_DIR, "../data/")

    def __init__(self):
        self._files = self._existing_files()
        self._counts = []
        self._n_frames = -1

        # load cached
        counts_filepath = os.path.join(self.DATA_DIR, "counts.json")
        if os.path.exists(counts_filepath):
            with open(counts_filepath, "r") as f:
                self._counts = json.load(f)
                self._n_frames = sum(self._counts)
            if len(self._files) == len(self._counts):
                return
        self._counts = []

        # count
        for filepath in self._files:
            try:
                with open(filepath, "r") as f:
                    frames = json.load(f)
                    self._counts.append(len(frames)-1)
            except:
                self._counts.append(0)
        self._n_frames = sum(self._counts)

        # save cache
        with open(counts_filepath, "w") as f:
            f.write(json.dumps(self._counts))

        print(f"have {len(self._files)} games, and {self._n_frames} frames")

    def _existing_files(self):
        files = []
        for r, d, f in os.walk(self.DATA_DIR):
            for file in f:
                if '.json' in file:
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

        delta_x = next_head["x"] - head["x"]
        delta_y = next_head["y"] - head["y"]
        direction = {
            (0, 1): "UP",
            (0, -1): "DOWN",
            (1, 0): "RIGHT",
            (-1, 0): "LEFT"
        }[(delta_x, delta_y)]
        return direction

    def __len__(self):

        return self._n_frames

    def __getitem__(self, index):
        try:
            file_index = 0
            frame_index = index
            for count in self._counts:
                if frame_index - count > 0:
                    file_index += 1
                    frame_index -= count

            filepath = self._files[file_index]
            with open(filepath) as f:
                content = f.read()
            frames = json.loads(content)

            snakes = frames[-1]["board"]["snakes"]
            winner_id = snakes[0]["id"]

            frame = frames[frame_index]
            next_frame = frames[frame_index+1]
            return frame, winner_id, self._get_direction(frame, next_frame, winner_id)
        except Exception as e:
            return self.__getitem__(index-1)
