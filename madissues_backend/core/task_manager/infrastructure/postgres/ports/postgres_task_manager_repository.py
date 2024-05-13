from typing import List

from sqlalchemy.orm import Session, joinedload

from madissues_backend.core.organizations.domain.postgres.postgres_organization import PostgresOrganization
from madissues_backend.core.shared.domain.entity import EntityId
from madissues_backend.core.task_manager.domain.board import Board
from madissues_backend.core.task_manager.domain.member import Member
from madissues_backend.core.task_manager.domain.postgres.postgres_board import PostgresBoard
from madissues_backend.core.task_manager.domain.postgres.postgres_member import PostgresMember
from madissues_backend.core.task_manager.domain.postgres.postgres_task_manager import PostgresTaskManager
from madissues_backend.core.task_manager.domain.postgres.postgres_task_manager_config import PostgresTaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager import TaskManager
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.application.ports.task_manager_repository import TaskManagerRepository
from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig


class PostgresTaskManagerRepository(TaskManagerRepository):
    def __init__(self, session: Session):
        self.session = session

    def _map_to_model(self, task_manager: TaskManager, config, faqs_board=None, issue_board=None,
                      members=None) -> PostgresTaskManager:
        # Creación de un nuevo objeto PostgresTaskManager a partir del objeto de dominio TaskManager
        return PostgresTaskManager(
            id=task_manager.id,
            organization_id=task_manager.organization_id,
            task_manager_project_id=str(task_manager.task_manager_project_id),
            faqs_board_id=faqs_board.id if faqs_board else None,
            issue_board_id=issue_board.id if issue_board else None,
        )

    def _map_config_to_model(self, config: TaskManagerConfig, task_manager_id: GenericUUID) -> PostgresTaskManagerConfig:
        return PostgresTaskManagerConfig(
            id=GenericUUID.next_id(),
            service=config.service,
            api_key=config.api_key,
            api_token=config.api_token,
            task_manager_id=task_manager_id
        )

    def _map_board_to_model(self, board: Board, board_type: str) -> PostgresBoard:
        if board is None:
            return None
        return PostgresBoard(
            id=board.id,
            queued_list_id=board.queued_list_id,
            in_progress_list_id=board.in_progress_list_id,
            solved_list_id=board.solved_list_id,
            not_solved_list_id=board.not_solved_list_id,
            board_id=board.board_id,
            # Dynamically assign the relationship based on type
            faqs_task_manager_id=board.id if board_type == 'faqs' else None,
            issue_task_manager_id=board.id if board_type == 'issues' else None
        )

    def _map_members_to_model(self, members: List[Member], task_manager_id: GenericUUID) -> List[PostgresMember]:
        return [
            PostgresMember(
                id=member.id,
                student_id=member.student_id,
                task_manager_email=member.task_manager_email,
                task_manager_id=task_manager_id
            ) for member in members
        ]

    def add(self, task_manager: TaskManager):
        # Primero mapeamos y añadimos las dependencias requeridas
        postgres_config = self._map_config_to_model(task_manager.config, task_manager.id)
        self.session.add(postgres_config)
        self.session.commit()  # Garantizamos que la config está guardada para obtener el ID generado

        # Mapeamos y añadimos los boards si existen
        if task_manager.faqs_board:
            postgres_faqs_board = self._map_board_to_model(task_manager.faqs_board, 'faqs')
            self.session.add(postgres_faqs_board)
            self.session.commit()  # Aseguramos su creación para obtener el ID

        if task_manager.issue_board:
            postgres_issue_board = self._map_board_to_model(task_manager.issue_board, 'issues')
            self.session.add(postgres_issue_board)
            self.session.commit()  # Aseguramos su creación para obtener el ID

        # Mapeamos los miembros y los añadimos
        postgres_members = self._map_members_to_model(task_manager.members, task_manager.id)
        for member in postgres_members:
            self.session.add(member)
        self.session.commit()  # Guardamos los miembros para asegurar sus IDs

        # Finalmente, mapeamos y añadimos el TaskManager
        postgres_task_manager = self._map_to_model(task_manager, postgres_config, postgres_faqs_board,
                                                   postgres_issue_board, postgres_members)
        self.session.add(postgres_task_manager)
        self.session.commit()

    def check_can_integrate_organization(self, organization_id, user_id) -> bool:
        organization = self.session.query(PostgresOrganization).filter_by(id=organization_id).one_or_none()
        if organization is None or str(organization.owner_id) != str(user_id):
            return False
        return True

    def remove(self, task_manager_id: EntityId):
        task_manager = self.session.query(PostgresTaskManager).filter_by(id=task_manager_id).one_or_none()
        if task_manager is None:
            raise ValueError("TaskManager does not exist")
        self.session.delete(task_manager)
        self.session.commit()

    def get_by_id(self, task_manager_id: EntityId) -> TaskManager:
        task_manager = self.session.query(PostgresTaskManager).filter_by(id=task_manager_id).one_or_none()
        if task_manager is None:
            raise ValueError("TaskManager not found")
        return task_manager

    def save(self, task_manager: TaskManager):
        existing_task_manager = self.session.query(PostgresTaskManager).filter_by(id=task_manager.id).one_or_none()
        if existing_task_manager is None:
            raise ValueError("TaskManager not found")
        existing_task_manager.update(**task_manager.__dict__)
        self.session.commit()

    def is_there_a_task_manager_for_organization(self, organization_id: str) -> bool:
        return self.session.query(PostgresTaskManager).filter_by(organization_id=organization_id).count() > 0

    def get_by_organization_id(self, organization_id: str) -> TaskManager | None:
        print("@@@@@@@@@@@@@@ GET BY ORG ID")
        # Carga ansiosa de las entidades relacionadas
        task_manager_record = (
            self.session.query(PostgresTaskManager)
            .options(
                joinedload(PostgresTaskManager.config),
                joinedload(PostgresTaskManager.members).joinedload(PostgresMember.student),
                joinedload(PostgresTaskManager.faqs_board),
                joinedload(PostgresTaskManager.issue_board),
            )
            .filter_by(organization_id=organization_id)
            .one_or_none()
        )

        if not task_manager_record:
            return None

        print("@@@@@@@@@@@@@@ GET BY ORG ID pre task manager")
        # Construcción del objeto de dominio TaskManager
        return TaskManager(
            id=GenericUUID(str(task_manager_record.id)),
            organization_id=GenericUUID(str(task_manager_record.organization_id)),
            task_manager_project_id=str(task_manager_record.task_manager_project_id),
            config=TaskManagerConfig(
                service=str(task_manager_record.config.service),
                api_key=str(task_manager_record.config.api_key),
                api_token=str(task_manager_record.config.api_token)
            ),
            faqs_board=self._create_board_model(task_manager_record.faqs_board),
            issue_board=self._create_board_model(task_manager_record.issue_board),
            members=[
                Member(
                    id=GenericUUID(str(member.id)),
                    student_id=GenericUUID(str(member.student_id)),
                    task_manager_email=str(member.student.email)  # Asumiendo que la entidad estudiantil tiene un email
                )
                for member in task_manager_record.members
            ]
        )

    def _create_board_model(self, board_record):
        if not board_record:
            return None
        return Board(
            id=GenericUUID(str(board_record.id)),
            queued_list_id=str(board_record.queued_list_id),
            in_progress_list_id=str(board_record.in_progress_list_id),
            solved_list_id=str(board_record.solved_list_id),
            not_solved_list_id=str(board_record.not_solved_list_id),
            board_id=str(board_record.board_id)
        )

    def get_organization(self, organization_id: str):
        return self.session.query(PostgresOrganization).filter_by(id=organization_id).one_or_none()
