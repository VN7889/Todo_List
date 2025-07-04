class ItemNotFoundException(Exception):
    
    def __init__(self, name: str, id: int):
        message = f"{name} with id '{id}' not found"
        super().__init__(message)