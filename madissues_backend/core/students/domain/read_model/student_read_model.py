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
            id=str(student.id),
            organization_id=str(student.organization_id),
            email=student.email,
            first_name=student.first_name,
            last_name=student.last_name,
            password=student.password,
            started_studies_date=student.started_studies_date.isoformat(),
            is_site_admin=student.is_site_admin,
            is_council_member=student.is_council_member,
            is_banned=student.is_banned,
            degree=str(student.profile.degree),
            joined_courses=student.profile.joined_courses,
            theme=student.preferences.theme,
            language=student.preferences.language
        )


