class InsufficientStockError(Exception):
    def __init__(self, message: str = "Insufficient stock.") -> None:
        super().__init__(message)
