import asyncio
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

class UserDocument(Document):
    name: str
    email: str
    password: str
    status: str
    
async def main():
    client = AsyncIOMotorClient("mongodb://admin:secret@localhost:27017")
    await init_beanie(database=client.db_name, document_models=[UserDocument])
    # user = UserDocument(name="John")
    # await user.insert()


if __name__ == "__main__":
    asyncio.run(main())
