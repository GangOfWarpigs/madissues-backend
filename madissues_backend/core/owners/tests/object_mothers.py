
import random
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OwnerObjectMother:
    names = ["Antonio", "Carlos", "Juan", "Luis", "Pedro", "Pablo", "Miguel", "Francisco", "Jose", "Manuel"]
    last_names = ["Garcia", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Gonzalez", "Rodriguez", "Hernandez",
                  "Diaz"]

    def generate_owner(self) -> Owner:
        name = self.names.pop(random.randint(0, len(self.names) - 1))
        last_name = self.last_names.pop(random.randint(0, len(self.names) - 1))
        return Owner(
            id=GenericUUID.next_id(),
            email=f"{name}_{last_name}@email.com",
            first_name=name,
            last_name=last_name,
            phone_number="922922922"
        )
