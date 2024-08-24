import json
from typing import List, Union
from uuid import UUID
from sqlmodel import Session

from api.v100.schemas.users import UserRead, UserCreate, UserUpdate
from db.repositories.users import UsersRepository
from dependencies.aws.dynamodb import UsersDynamodb


class BusinessLogicUsers:

    def __init__(self):
        self.users = UsersRepository()
        self.dynamodb = UsersDynamodb()

    def list(self, db: Session) -> List[UserRead]:
        return self.users.list(db=db)

    def get_one(self, db: Session, id: UUID) -> Union[UserRead, None]:
        user_cache = self.dynamodb.get_item(id=str(id))
        print(f"user_cache: {user_cache}")
        if user_cache:
            user_json = json.loads(user_cache["data"]["S"])
            return UserRead(**user_json)

        user_db = self.users.get_one(db=db, id=id)

        if not user_db:
            return None

        user_dict = user_db.model_dump()
        user_dict["id"] = str(user_db.id)

        item = {
            "id": {"S": str(user_db.id)},
            "data": {"S": json.dumps(user_dict)}
        }
        self.dynamodb.put_item(item=item)

        return user_db

    def create(self, db: Session, user: UserCreate) -> UserRead:
        return self.users.create(db=db, user=user)

    def update(self, db: Session, id: UUID, user: UserUpdate) -> UserRead:
        user_db = self.users.update(db=db, id=id, user=user)

        user_cache = self.dynamodb.get_item(id=str(id))
        if user_cache:
            user_dict = user_db.model_dump()
            user_dict["id"] = str(user_db.id)

            item = {
                "id": {"S": str(user_db.id)},
                "data": {"S": json.dumps(user_dict)}
            }
            self.dynamodb.put_item(item=item)

        return user_db

    def delete(self, db: Session, id: UUID) -> None:
        user_cache = self.dynamodb.get_item(id=str(id))
        if user_cache:
            self.dynamodb.delete_item(id=str(id))

        self.users.delete(db=db, id=id)