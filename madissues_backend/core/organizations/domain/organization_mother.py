import random
from uuid import uuid4

from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse
from madissues_backend.core.organizations.domain.organization_degree import OrganizationDegree
from madissues_backend.core.organizations.domain.organization_teacher import OrganizationTeacher
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationMother:
    @staticmethod
    def generate_organization():
        organization = Organization(
            id=GenericUUID.next_id(),
            owner_id=GenericUUID.next_id(),
            name=OrganizationMother.generate_company_name(),
            logo=OrganizationMother.generate_image_link(),
            description=OrganizationMother.generate_description(),
            contact_info=OrganizationMother.generate_phone_number(),
            primary_color=OrganizationMother.generate_hex_color(),
            secondary_color=OrganizationMother.generate_hex_color(),
            teachers=[OrganizationMother.generate_organization_teacher() for _ in range(random.randint(1, 5))],
            courses=[OrganizationMother.generate_organization_course() for _ in range(random.randint(1, 5))],
            degrees=[OrganizationMother.generate_organization_degree() for _ in range(random.randint(1, 5))]
        )
        return organization

    @staticmethod
    def generate_organization_course():
        course = OrganizationCourse(
            id=GenericUUID.next_id(),
            name=OrganizationMother.generate_course_name(),
            code=OrganizationMother.generate_course_code(),
            icon=OrganizationMother.generate_image_link(),
            primary_color=OrganizationMother.generate_hex_color(),
            secondary_color=OrganizationMother.generate_hex_color()
        )
        return course

    @staticmethod
    def generate_organization_teacher():
        teacher = OrganizationTeacher(
            id=GenericUUID.next_id(),
            first_name=OrganizationMother.generate_first_name(),
            last_name=OrganizationMother.generate_last_name(),
            email=OrganizationMother.generate_email(),
            office_link=OrganizationMother.generate_dis_link(),
            courses=[GenericUUID.next_id() for _ in range(random.randint(1, 5))]
        )
        return teacher

    @staticmethod
    def generate_organization_degree():
        degree = OrganizationDegree(
            id=GenericUUID.next_id(),
            name=OrganizationMother.generate_degree_name(),
        )
        return degree

    @staticmethod
    def generate_company_name():
        return f"Organization {str(uuid4())[:8]}"

    @staticmethod
    def generate_degree_name():
        return f"Degree {str(uuid4())[:8]}"

    @staticmethod
    def generate_course_name():
        return f"Course {str(uuid4())[:8]}"

    @staticmethod
    def generate_course_code():
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(2, 8)))

    @staticmethod
    def generate_description():
        return f"Description {str(uuid4())[:8]}"

    @staticmethod
    def generate_first_name():
        return f"First Name {str(uuid4())[:8]}"

    @staticmethod
    def generate_last_name():
        return f"Last Name {str(uuid4())[:8]}"

    @staticmethod
    def generate_phone_number():
        return ''.join(random.choices('0123456789', k=10))

    @staticmethod
    def generate_email():
        return f"{str(uuid4())[:8]}@example.com"

    @staticmethod
    def generate_image_link():
        return f"https://www.example.com/{str(uuid4())[:8]}.{'png' if random.random() > 0.5 else 'jpg'}"

    @staticmethod
    def generate_hex_color():
        return f"#{str(uuid4())[:6]}"

    @staticmethod
    def generate_dis_link():
        return f"https://www.dis.ulpgc.es/{str(uuid4())[:8]}"
