from waffledotcom.src.apps.common.exceptions import WacruitException


class UserNotFoundException(WacruitException):
    def __init__(self):
        super().__init__(status_code=404, detail="존재하지 않는 유저입니다.")


class UserAlreadyExistsException(WacruitException):
    def __init__(self):
        super().__init__(status_code=409, detail="이미 존재하는 유저입니다.")


class UserPermissionDeniedException(WacruitException):
    def __init__(self):
        super().__init__(status_code=403, detail="권한이 없습니다.")
