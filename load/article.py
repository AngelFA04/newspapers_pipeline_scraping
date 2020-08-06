from sqlalchemy import Column, String, Integer
from base import Base

class Article(Base):
    __tablename__ = 'articles'
    id = Column(String, primary_key=True)
    title = Column(String)
    body = Column(String)
    host = Column(String)
    newspaper_uid = Column(String)
    n_tokens_body = Column(Integer)
    n_tokens_title = Column(Integer)
    tokens_body = Column(String)
    tokens_title = Column(String)
    url = Column(String, unique=True)

    def __init__(self,    
                 uid,
                 title,
                 body,
                 host,
                 newspaper_uid,
                 n_tokens_body,
                 n_tokens_title,
                 tokens_body,
                 tokens_title,
                 url
                 ):
                self.id = uid
                self.title = title
                self.body = body
                self.host = host
                self.newspaper_uid = newspaper_uid
                self.n_tokens_body = n_tokens_title
                self.n_tokens_title = n_tokens_title
                self.tokens_body = tokens_body
                self.tokens_title = tokens_title 
                self.url = url