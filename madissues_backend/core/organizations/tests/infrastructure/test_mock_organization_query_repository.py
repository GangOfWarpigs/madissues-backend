import unittest
from unittest.mock import Mock

from madissues_backend.core.organizations.domain.read_models.organization_course_read_model import \
    OrganizationCourseReadModel
from madissues_backend.core.organizations.domain.read_models.organization_degree_read_model import \
    OrganizationDegreeReadModel
from madissues_backend.core.organizations.domain.read_models.organization_teacher_read_model import \
    OrganizationTeacherReadModel
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_query_repository import \
    MockOrganizationQueryRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.organizations.domain.organization_mother import OrganizationMother
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestMockOrganizationQueryRepository(unittest.TestCase):
    def setUp(self):
        self.entity_table = EntityTable()
        self.organization_query_repository = MockOrganizationQueryRepository(self.entity_table)

        # Set up initial data
        self.organization = OrganizationMother.generate_organization()
        self.entity_table.tables["organizations"][self.organization.id] = self.organization

    def test_get_all_courses_from_organization(self):
        courses = self.organization_query_repository.get_all_courses_from_organization(str(self.organization.id))
        self.assertEqual(len(courses), len(self.organization.courses))
        for course in courses:
            self.assertIn(course, [OrganizationCourseReadModel.of(x) for x in self.organization.courses])

    def test_get_all_teachers_from_organization(self):
        teachers = self.organization_query_repository.get_all_teachers_from_organization(str(self.organization.id))
        self.assertEqual(len(teachers), len(self.organization.teachers))
        for teacher in teachers:
            self.assertIn(teacher, [OrganizationTeacherReadModel.of(x) for x in self.organization.teachers])

    def test_get_all_teachers_degrees_organization(self):
        degrees = self.organization_query_repository.get_all_teachers_degrees_organization(str(self.organization.id))
        self.assertEqual(len(degrees), len(self.organization.degrees))
        for degree in degrees:
            self.assertIn(degree, [OrganizationDegreeReadModel.of(x) for x in self.organization.degrees])

    def test_get_all_by_owner(self):
        owner_id = str(GenericUUID.next_id())
        self.organization.owner_id = GenericUUID(owner_id)
        organizations = self.organization_query_repository.get_all_by_owner(owner_id)
        self.assertTrue(any(org.id == str(self.organization.id) for org in organizations))

    def test_get_by_id(self):
        org_read_model = self.organization_query_repository.get_by_id(str(self.organization.id))
        self.assertEqual(org_read_model.id, str(self.organization.id))

    def test_get_organization_task_manager(self):
        task_manager_id = GenericUUID.next_id()

        mock_task_manager = Mock()
        mock_task_manager.task_manager_project_id = task_manager_id
        mock_task_manager.organization_id = self.organization.id

        self.entity_table.tables["task_managers"][task_manager_id] = mock_task_manager

        task_manager = self.organization_query_repository.get_organization_task_manager(str(self.organization.id))
        self.assertIsNotNone(task_manager)
        self.assertEqual(task_manager.task_manager_id, str(task_manager_id))

    def test_get_nonexistent_organization(self):
        org_read_model = self.organization_query_repository.get_by_id(str(GenericUUID.next_id()))
        self.assertIsNone(org_read_model)


if __name__ == '__main__':
    unittest.main()
