from abc import abstractmethod, ABC


class TokenGenerator(ABC):
    @abstractmethod
    def generate(self):
        pass