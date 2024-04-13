from pydantic import BaseModel


class CreateEmail(BaseModel):
    to: str
    subject: str
    body: str