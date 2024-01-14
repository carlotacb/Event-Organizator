class ProfileNotComplete(Exception):
    pass


class ApplicationAlreadyExists(Exception):
    pass


class UserIsNotAParticipant(Exception):
    pass


class UserIsNotStudent(Exception):
    pass


class UserIsTooYoung(Exception):
    pass


class ApplicationNotFound(Exception):
    pass


class NotApplied(Exception):
    pass


class StatusNotFound(Exception):
    pass


class ApplicationCanNotBeCancelled(Exception):
    pass


class ApplicationIsNotFromUser(Exception):
    pass


class ApplicationCanNotBeConfirmed(Exception):
    pass


class ApplicationCanNotBeAttended(Exception):
    pass


class EventAlreadyStarted(Exception):
    pass
