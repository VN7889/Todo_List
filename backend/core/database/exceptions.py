class ItemNotFoundException(Exception):
    
    def __init__(self, id: int):
        message = f"'{id}' not found"
        super().__init__(message)