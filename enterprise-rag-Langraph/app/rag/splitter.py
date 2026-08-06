from abc import abstractmethod

class BaseTextSplitter():
    @abstractmethod
    def split(self,text:str)-> list[str]:
        pass