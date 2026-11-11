
import datetime as dt
from pydantic import BaseModel, ConfigDict
from pydantic import Field



class Task(BaseModel) :
    """ """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(gt=0, strict=True)
    title: str = Field(min_length=1, max_length=255, strict=True)
    description: str = Field()
    created_at: dt.datetime = Field()
    completed: bool = Field(default=False, strict=True)
    owner_id: int = Field(gt=0, strict=True)