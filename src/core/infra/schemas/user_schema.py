from beanie import Document
from beanie.odm.actions import Update, before_event
from pydantic import Field
from datetime import datetime


class UserDocument(Document):
    name: str
    email: str
    password: str
    status: str
    salt: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

    @before_event([Update])
    def update_timestamp(self):
        self.updated_at = datetime.now()

    class Settings:
        name = "users"
