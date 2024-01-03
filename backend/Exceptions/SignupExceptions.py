class InvalidEmailError(Exception):
    """Exception raised for invalid email errors."""
    def __init__(self, email, message="Invalid email"):
        self.email = email
        self.message = message
        self.code = 422
        super().__init__(self.message)

class InvalidPasswordError(Exception):
    """Exception raised for invalid password errors."""
    def __init__(self, password, message="Invalid password"):
        self.password = password
        self.message = message
        self.code = 423
        super().__init__(self.message)

class UserAlreadyExistsError(Exception):
    """Exception raised for invalid password errors."""
    def __init__(self, username, message="User already exists"):
        self.username = username
        self.message = message
        self.code = 424
        super().__init__(self.message)