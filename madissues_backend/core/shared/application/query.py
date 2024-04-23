

from abc import ABC, abstractmethod


class Query(ABC):
    @abstractmethod
    def query(self):
        pass 
        