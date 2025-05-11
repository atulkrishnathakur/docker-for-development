from sqlalchemy import (BigInteger,Column,PrimaryKeyConstraint,Text,String,Integer,DateTime,
BigInteger,SmallInteger,func,UniqueConstraint,ForeignKey,Identity)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.base import Mapped
from app.database.dbconnection import Base

class Empm(Base):
    __tablename__ = 'emp_m'
    __table_args__ = (PrimaryKeyConstraint('id', name='emp_m_pkey'),)

    id: Mapped[BigInteger] = mapped_column('id',BigInteger,Identity(start=1, cycle=False),primary_key=True,nullable=False)
    emp_name: Mapped[String] = mapped_column('emp_name',String(255),nullable=True)
    email: Mapped[String] = mapped_column('email',String(255),unique=True, index=True,nullable=True)
    mobile: Mapped[String] = mapped_column('mobile',String(25),nullable=True)
    status: Mapped[SmallInteger] = mapped_column('status',SmallInteger,nullable=True,default=1,comment="1=Active,0=Inactive")
    password: Mapped[String] = mapped_column('password',String(255),nullable=True)
    remember_token: Mapped[String] = mapped_column('remember_token',String(255),nullable=True)
    created_at: Mapped[DateTime] = mapped_column('created_at',DateTime, nullable=True, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column('updated_at',DateTime,nullable=True)
    deleted_at: Mapped[DateTime] = mapped_column('deleted_at',DateTime,nullable=True,default=None)
    image: Mapped[String] = mapped_column('image',String(255),nullable=True)