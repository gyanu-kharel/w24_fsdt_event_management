from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from typing import Optional
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    full_name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId:str},
        arbitrary_types_allowed=True
    )
