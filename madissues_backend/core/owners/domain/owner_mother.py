
import random
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OwnerMother:
    # Almacena las combinaciones únicas de nombres y apellidos
    generated_names_last_names = set()

    @classmethod
    def generate_owner(cls) -> Owner:
        while True:
            # Genera nombres y apellidos aleatorios como strings random
            name = cls.random_string(length=random.randint(5, 10))
            last_name = cls.random_string(length=random.randint(5, 10))
            full_name = f"{name}_{last_name}"

            # Verifica si la combinación ya ha sido generada
            if full_name not in cls.generated_names_last_names:
                cls.generated_names_last_names.add(full_name)
                break

        return Owner(
            id=GenericUUID.next_id(),
            email=f"{name}_{last_name}@email.com",
            first_name=name,
            last_name=last_name,
            phone_number="922922922"
        )

    @staticmethod
    def random_string(length: int) -> str:
        # Genera una cadena de texto aleatoria de longitud dada
        letters = "abcdefghijklmnopqrstuvwxyz"
        return ''.join(random.choice(letters) for _ in range(length))