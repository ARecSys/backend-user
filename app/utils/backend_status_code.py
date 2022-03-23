from enum import IntEnum, unique

@unique
class BackendStatusCode( IntEnum ):
    """ Backend Status Code Enum.

    Example usage:
        BackendStatusCode.OK.value  # 0
    """

    ERROR = -1
    OK = 0
    DATA_NOT_FOUND = 1
    USER_NOT_FOUND = 2
