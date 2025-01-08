from pydantic import BaseModel


class MusicLink(BaseModel):
    """
    A class representing a music link."""

    title: str
    link: str


class MusicDetails(BaseModel):
    """
    A class representing music details."""

    links: list[MusicLink]
