from typing import Dict, Optional

class Condition:
    def __init__(self, conditionId: str, name: Optional[str] = None, endTrigger: Optional[str] = None, 
                 endValue: Optional[int] = None, effectTrigger: Optional[str] = None, effectValue: Optional[str] = None):
        """Initialize the Condition object with immutable conditionId."""
        self._conditionId = conditionId  # Condition ID is fixed and immutable
        self.name: Optional[str] = name
        self.endTrigger: Optional[str] = endTrigger
        self.endValue: Optional[int] = endValue
        self.effectTrigger: Optional[str] = effectTrigger
        self.effectValue: Optional[str] = effectValue

    @property
    def conditionId(self) -> str:
        """Get the conditionId (immutable)."""
        return self._conditionId

    def set_name(self, new_name: str):
        """Update the condition's name."""
        self.name = new_name

    def set_endTrigger(self, new_endTrigger: str):
        """Update the condition's end trigger."""
        self.endTrigger = new_endTrigger

    def set_endValue(self, new_endValue: int):
        """Update the condition's end value."""
        self.endValue = new_endValue

    def set_effectTrigger(self, new_effectTrigger: str):
        """Update the condition's effect trigger."""
        self.effectTrigger = new_effectTrigger

    def set_effectValue(self, new_effectValue: str):
        """Update the condition's effect value."""
        self.effectValue = new_effectValue

    def to_primitive(self) -> Dict:
        """Convert the Condition object to a dictionary."""
        return {
            "conditionId": self._conditionId,
            "name": self.name,
            "endTrigger": self.endTrigger,
            "endValue": self.endValue,
            "effectTrigger": self.effectTrigger,
            "effectValue": self.effectValue
        }

    @staticmethod
    def from_primitive(data: Dict) -> "Condition":
        """Create a Condition object from a dictionary."""
        return Condition(
            conditionId=data["conditionId"],
            name=data.get("name"),
            endTrigger=data.get("endTrigger"),
            endValue=data.get("endValue"),
            effectTrigger=data.get("effectTrigger"),
            effectValue=data.get("effectValue")
        )
