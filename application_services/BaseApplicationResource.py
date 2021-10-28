from abc import ABC, abstractmethod


class BaseApplicationException:

    def __init__(self):
        pass


class BaseApplicationResource(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_links(self, resource_data):
        raise NotImplementedError("Must implement get_links.")
