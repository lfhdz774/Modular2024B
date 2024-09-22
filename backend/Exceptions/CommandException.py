from Exceptions.BaseCustomError import BaseCustomError


class TextProcessingError(BaseCustomError):
    """Exception raised for errors in text processing."""
    def __init__(self, message="Error in text processing"):
        super().__init__(message=message, code=500)

class ModelLoadingError(BaseCustomError):
    """Exception raised when loading the neural network model fails."""
    def __init__(self, model_name):
        super().__init__(message=f"Error loading model: {model_name}", code=501)
        self.model_name = model_name

class InvalidTextInputError(BaseCustomError):
    """Exception raised for invalid text input."""
    def __init__(self, text):
        super().__init__(message="Invalid text input", code=422)
        self.text = text

class PredictionError(BaseCustomError):
    """Exception raised during the prediction phase."""
    def __init__(self, message="Error during prediction"):
        super().__init__(message=message, code=502)

class RemoteServerError(BaseCustomError):
    """Exception raised when executing code on the remote server fails."""
    def __init__(self, server_url):
        super().__init__(message=f"Error executing on remote server: {server_url}", code=503)
        self.server_url = server_url

class InvalidCommandError(Exception):
    """Exception raised for invalid commands."""
    def __init__(self, command):
        self.code = 400
        self.message = f'Comando inválido: {command}'
        super().__init__(self.message)