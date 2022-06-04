from dataclasses import dataclass

@dataclass
class Klausur:
    name: str
    description: str
    professor: str
    courseID: int
    semesterID: int
    type: int