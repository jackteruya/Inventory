class InvalidInventoryOperationError(Exception):
    def __init__(self, message: str = "Invalid inventory operation.") -> None:
        super().__init__(message)
