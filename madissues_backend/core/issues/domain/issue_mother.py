import random
from datetime import datetime, timedelta
from typing import List
from madissues_backend.core.shared.domain.value_objects import GenericUUID

# Suponiendo que las definiciones de Issue y IssueComment ya están disponibles en tu entorno
from madissues_backend.core.issues.domain.issue import Issue, Title, Details, Status, Description, LinkToImage
from madissues_backend.core.issues.domain.issue_comment import IssueComment, Content


class IssueMother:
    @staticmethod
    def random_title() -> Title:
        words = ["Issue", "Problem", "Error", "Bug", "Task"]
        return f"{random.choice(words)} #{random.randint(1, 10000)}"

    @staticmethod
    def random_description() -> Description:
        descriptions = ["Description of the issue", "Detailed explanation", "Summary of the problem"]
        return random.choice(descriptions)

    @staticmethod
    def random_details() -> Details:
        detail_samples = [
            "The system crashes when clicking on the save button.",
            "An error message appears when the page loads.",
            "Users are unable to log in after recent updates.",
            "The application is unresponsive after a few minutes of use.",
            "The issue is intermittent and hard to reproduce.",
            "The error occurs on both Windows and macOS.",
            "The bug is present in the latest version of the software.",
            "The problem is related to the network connection.",
            "The issue is critical and affects all users."
        ]
        return random.choice(detail_samples)

    @staticmethod
    def random_status() -> Status:
        return random.choice(["Queued", "In progress", "Solved", "Not Solved"])

    @staticmethod
    def random_image_links() -> List[LinkToImage]:
        image_url = "http://example.com/image",
        image_ext = [".png", ".jpg", ".jpeg"]
        return [f"{image_url}{ext}" for ext in random.choices(image_ext, k=random.randint(1, 10))]

    @staticmethod
    def random_uuid_list(n: int) -> List[GenericUUID]:
        return [GenericUUID.next_id() for _ in range(n)]

    @staticmethod
    def random_issue() -> Issue:
        return Issue(
            id=GenericUUID.next_id(),
            title=IssueMother.random_title(),
            description=IssueMother.random_description(),
            details=IssueMother.random_details(),
            proofs=IssueMother.random_image_links(),
            status=IssueMother.random_status(),
            timestamp=datetime.now() - timedelta(days=random.randint(0, 365)),
            course=GenericUUID.next_id(),
            teachers=IssueMother.random_uuid_list(random.randint(1, 3)),
            student=GenericUUID.next_id(),
            task_manager_id=GenericUUID.next_id(),
            assigned_to=GenericUUID.next_id()
        )

    @staticmethod
    def random_content() -> Content:
        contents = [
            "This is a critical issue that needs immediate attention.",
            "Please find the attached screenshots for more details.",
            "The error has been persistent across multiple systems."
        ]
        return random.choice(contents)

    @staticmethod
    def random_issue_comment(issue_id: GenericUUID, author: GenericUUID) -> IssueComment:
        return IssueComment(
            id=GenericUUID.next_id(),
            issue_id=issue_id,
            author=author,
            likes=IssueMother.random_uuid_list(random.randint(0, 10)),
            content=IssueMother.random_content(),
            timestamp=datetime.now(),
            response_to=None if random.choice([True, False]) else GenericUUID.next_id()
        )


# Ejemplo de uso
random_issue = IssueMother.random_issue()
random_comment = IssueMother.random_issue_comment(random_issue.id, random_issue.student)

print(random_issue)
print(random_comment)
