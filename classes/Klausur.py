class Klausur:
    name = None
    description = None
    professor = None
    courseID = None
    semesterID = None
    type = None

    def __init__(self, name, description, professor, courseID, semesterID, type):
        self.name = name
        self.description = description
        self.professor = professor
        self.courseID = courseID
        self.semesterID = semesterID
        self.type = type