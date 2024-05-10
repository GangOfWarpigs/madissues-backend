from madissues_backend.core.issues.infrastructure.mocks.mock_issue_repository import MockIssueRepository
from madissues_backend.core.organizations.domain.organization_mother import OrganizationMother
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.owners.domain.owner_mother import OwnerMother
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.shared.infrastructure.uuid.uuid_token_generator import UUIDTokenGenerator
from madissues_backend.core.students.infrastructure.mocks.mock_student_repository import MockStudentRepository


class SnapshotsMother:
    def __init__(self):
        self.db = EntityTable()
        self.organization_repository = MockOrganizationRepository(self.db)
        self.student_repository = MockStudentRepository(self.db)
        self.event_bus = MockEventBus()
        self.issue_repository = MockIssueRepository(self.db)
        self.owner_repository = MockOwnerRepository(self.db)

    def create_organization(self):
        organization = OrganizationMother.generate_organization()
        organization.id = GenericUUID("cc164174-07f7-4cd4-8a7e-43c96d9b825a")

        owner = OwnerMother.generate_owner()
        owner.id = GenericUUID("83d150fe-84f4-4a22-a109-5704342c589c")
        owner.generate_auth_token(UUIDTokenGenerator())
        organization.owner_id = owner.id

        other_owner = OwnerMother.generate_owner()
        other_owner.id = GenericUUID("ca7b384c-0ae9-489f-90c6-a18a6781dcd0")
        other_owner.generate_auth_token(UUIDTokenGenerator())

        organization.courses = []
        organization.degrees = []
        organization.teachers = []

        course = OrganizationMother.generate_organization_course()
        course.id = GenericUUID("2b3d1324-346b-40cb-9b7f-f744fe06b59d")
        organization.courses.append(course)

        degree = OrganizationMother.generate_organization_degree()
        degree.id = GenericUUID("f3b3b3b3-346b-40cb-9b7f-f744fe06b59d")
        organization.degrees.append(degree)

        self.owner_repository.add(owner)
        self.owner_repository.add(other_owner)
        self.organization_repository.add(organization)
        self.db.save_snapshot("with_organization_created")

    def load_with_organization_created(self):
        self.db.load_snapshot("with_organization_created")
        print("Snapshot loaded, ", self.db.tables)


if __name__ == '__main__':
    db = EntityTable()
    snapshots = SnapshotsMother()
    snapshots.create_organization()
    snapshots.load_with_organization_created()
    print("Snapshots created")
