from abc import ABC, abstractmethod



class ValueFinder(ABC):
    @abstractmethod
    def find_values(self, log_file) -> float :
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass

    def job_completed(self, log_file) -> bool:
        with open(log_file, 'r') as inf:
            lines = inf.readlines()
        
        return ("Normal termination of Gaussian 16 " in lines[-1])