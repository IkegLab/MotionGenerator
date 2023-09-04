from abc import *
from typing import *
import warnings
import socket


warnings.simplefilter('always', UserWarning)
def warn(message):
    print('\033[31m'+'[middleware warning] '+'\033[0m' + message)


class AlterMiddlewareBase(object):
    def __init__(self):
        super(AlterMiddlewareBase, self).__init__()

    @abstractmethod
    def get_axes(self) -> List[int]:
        pass

    @abstractmethod
    def set_axes(self, value_list :List[int]):
    #def set_axes(self, value_list :List[int]) -> bool:
        pass

