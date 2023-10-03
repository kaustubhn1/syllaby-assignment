from __future__ import annotations
from typing import List, Optional
from pydantic import (
    BaseModel,
    StrictStr,
    Field,
    ConfigDict
)


class Section(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    section: StrictStr
    content: StrictStr 
    sub_sections: Optional[List[Section]] = Field(default=[])


class BookSchema(BaseModel):
    sections: List[Section]