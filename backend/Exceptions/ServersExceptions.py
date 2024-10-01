from Exceptions.BaseCustomError import BaseCustomError


class InvalidEmailError(BaseCustomError):
    """Exception raised for invalid email errors."""
    def __init__(self, email):
        super().__init__(message="Invalid Email", code=423)
        self.email = email

class AccessAlreadyExistsError(BaseCustomError):
    def __init__(self, access):
        super().__init__(message="User already exists", code=424)
        self.access = access

class ServerNotFoundError(BaseCustomError):
    """Exception raised when a user is not found."""
    def __init__(self, server_id):
        super().__init__(message="Server not found", code=404)
        self.server_id = server_id
        


class UpdateUserInfoError(BaseCustomError):
    """Exception raised for errors in updating user info."""
    def __init__(self, username):
        super().__init__(message="Error updating user info", code=500)
        self.username = username
