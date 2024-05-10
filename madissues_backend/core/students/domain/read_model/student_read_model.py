from pydantic import BaseModel

from madissues_backend.core.students.domain.student import Student


class StudentReadModel(BaseModel):
    id: str
    organization_id: str
    email: str
    first_name: str
    last_name: str
    password: str
    started_studies_date: str
    is_site_admin: bool
    is_council_member: bool
    is_banned: bool
    degree: str
    joined_courses: list[str]
    theme: str  # Solo puede ser o Dark o Light
    language: str  # Solo puede ser un country code

    @staticmethod
    def of(student: Student):
        return StudentReadModel(
            **student.dict(),
            **student.preferences.dict(),
            **student.profile.dict(),
            id=str(student.id)
        )


