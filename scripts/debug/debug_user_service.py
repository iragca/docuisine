from sqlalchemy.orm import Session

from docuisine.db.database import SessionLocal
from docuisine.services import UserService

session: Session = SessionLocal()

user_service = UserService(db_session=session)


user = user_service._get_user_by_id(user_id=1)
print(user.__dict__)


