class Error(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundError(Error):
    def __init__(self):
        super().__init__('Ability could not be found')


class NotOwnerError(Error):
    def __init__(self):
        super().__init__('Cannot access another players character.')
