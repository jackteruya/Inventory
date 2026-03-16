import re
import unicodedata

from app.domain.services.name_normalizer import InventoryNameNormalizer


class UnicodeInventoryNameNormalizer(InventoryNameNormalizer):
    def normalize(self, name: str) -> str:
        normalized = name.strip().lower()
        normalized = unicodedata.normalize("NFD", normalized)
        normalized = normalized.encode("ascii", "ignore").decode("utf-8")
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized


if __name__ == "__main__":
    n = UnicodeInventoryNameNormalizer()
    r = n.normalize("Banana")
    print(r)
