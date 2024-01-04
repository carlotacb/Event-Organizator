class UserAlreadyExists(Exception):
    pass


class UserNotFound(Exception):
    pass


class UserNotLoggedIn(Exception):
    pass


class InvalidPassword(Exception):
    pass


class OnlyAuthorizedToOrganizerAdmin(Exception):
    pass

class OnlyAuthorizedToOrganizer(Exception):
    pass