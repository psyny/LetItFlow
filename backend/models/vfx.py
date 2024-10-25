from typing import Dict, Optional

class Vfx:
    def __init__(self, vfxId: str, vfxKeysVals: Optional[Dict[str, int]] = None):
        """Initialize the Vfx object with immutable vfxId."""
        self._vfxId = vfxId  # Vfx ID is fixed and immutable
        self.vfxKeysVals: Dict[str, int] = vfxKeysVals if vfxKeysVals else {}  # Dictionary to store vfxKey and vfxVal pairs

    @property
    def vfxId(self) -> str:
        """Get the vfxId (immutable)."""
        return self._vfxId

    def set_vfx_key_val(self, key: str, value: int):
        """Set a vfxKey and vfxVal pair."""
        self.vfxKeysVals[key] = value

    def get_vfx_value(self, key: str) -> Optional[int]:
        """Get the vfxVal corresponding to the given vfxKey."""
        return self.vfxKeysVals.get(key, None)

    def remove_vfx_key_val(self, key: str):
        """Remove a vfxKey and its corresponding vfxVal."""
        if key in self.vfxKeysVals:
            del self.vfxKeysVals[key]

    def to_primitive(self) -> Dict:
        """Convert the Vfx object to a dictionary."""
        return {
            "vfxId": self._vfxId,
            "vfxKeysVals": self.vfxKeysVals
        }

    @staticmethod
    def from_primitive(data: Dict) -> "Vfx":
        """Create a Vfx object from a dictionary."""
        return Vfx(
            vfxId=data["vfxId"],
            vfxKeysVals=data.get("vfxKeysVals", {})
        )
