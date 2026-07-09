class DuplicateRunError(Exception):
    def __init__(self, filename:str):
        self.filename = filename
        super().__init__(f"Rularea pentru \"{filename}\" exista deja")
class InvalidLogError(Exception):
    def __init__(self, info:str):
        self.info = info
        super().__init__(f"Log invalid: {info}")
class RunNotFound(Exception):
    def __init__(self):
        super().__init__("Nu exista acest Run")
