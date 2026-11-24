from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP,text
class Post (Base):
    __tablename__ = 'posts'
    id = Column (Integer, primary_key=True, nullable = False)
    content = Column (String, nullable = False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default= text("now()"))