"""
jsnek_saved_games_dataset that returns flat (vectorized) data
"""

from .jsnek_base_dataset import JSnekBaseDataset
from .. import utils


class JSnekDataset(JSnekBaseDataset):
    """Represents a board state in the following way:

    board_state: `torch.Tensor`
        Board state in torch.Tensor format. Board state can either be
        C x H x W
        or
        (C*H*W) if board_state_as_vector = True

    direction: `torch.Tensor`
        Direction taken in one-hot format

    """

    def __init__(
        self, board_state_as_vector=False, direction_as_index=False, max_frames=-1
    ):
        super().__init__(max_frames=max_frames)

        self.board_state_as_vector = board_state_as_vector
        self.direction_as_index = direction_as_index

    def __getitem__(self, index):
        """
        Parameters
        ----------
        index : int
            Index of datum

        Returns
        -------
        board_state: `torch.Tensor`
            Board state in torch.Tensor format. Board state can either be
            C x H x W
            or
            (C*H*W) if board_state_as_vector = True

        direction: `torch.Tensor`
            Direction taken in one-hot format
            or
            Index if direction_as_index = True
        """

        frame, winner_id, direction = super().__getitem__(index)

        board_state = utils.frame_to_image(frame, winner_id)

        if self.board_state_as_vector:
            board_state = board_state.view([board_state.numel()])

        if self.direction_as_index:
            direction = utils.direction_to_index(direction)
        else:
            direction = utils.direction_to_onehot(direction)

        return board_state, direction
