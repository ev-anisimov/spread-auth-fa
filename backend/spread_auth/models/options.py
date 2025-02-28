from sqlmodel import SQLModel


class Options(SQLModel):
    name: str = "Сервис авторизации AWADA"
    project_id: int | None = None
