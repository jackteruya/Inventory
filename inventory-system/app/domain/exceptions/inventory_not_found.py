class InventoryNotFoundError(Exception):
    def __init__(self, message: str = "Item not found.") -> None:
        super().__init__(message)
