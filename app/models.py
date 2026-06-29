from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column
from sqlalchemy.types import String


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: MappedColumn[int] = mapped_column(primary_key=True)
    username: MappedColumn[str] = mapped_column(String(256))
    first_name: MappedColumn[str] = mapped_column(String())
    last_name: MappedColumn[str] = mapped_column(String())
    email: MappedColumn[str] = mapped_column(String(), unique=True)
    phone: MappedColumn[str] = mapped_column(String(), unique=True)
