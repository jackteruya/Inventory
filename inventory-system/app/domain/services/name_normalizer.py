from abc import ABC, abstractmethod


class InventoryNameNormalizer(ABC):
    @abstractmethod
    def normalize(self, name: str) -> str:
        raise NotImplementedError
