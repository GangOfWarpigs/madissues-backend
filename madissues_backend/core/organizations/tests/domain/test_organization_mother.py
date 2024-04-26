import unittest

from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse
from madissues_backend.core.organizations.domain.organization_mother import OrganizationMother
from madissues_backend.core.organizations.domain.organization_teacher import OrganizationTeacher


class MyTestCase(unittest.TestCase):

    def test_create_1000_organizations(self):
        for _ in range(1000):
            org = OrganizationMother.generate_organization()
            self.assertIsInstance(org, Organization)

    def test_create_1000_courses(self):
        for _ in range(1000):
            course = OrganizationMother.generate_organization_course()
            self.assertIsInstance(course, OrganizationCourse)

    def test_create_1000_teachers(self):
        for _ in range(1000):
            teacher = OrganizationMother.generate_organization_teacher()
            self.assertIsInstance(teacher, OrganizationTeacher)


if __name__ == '__main__':
    unittest.main()
