from .value_objects import ValueObject

class Board(ValueObject):
    board_id : str
    done_list_id : str
    todo_list_id : str
    in_progress_list_id : str
