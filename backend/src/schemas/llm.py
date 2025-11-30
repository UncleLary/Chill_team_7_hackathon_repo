from typing import Any, Dict
from pydantic import BaseModel

class LLMRequest(BaseModel):
    template_name: str
    arguments: Dict[str, Any]
