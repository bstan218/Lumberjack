from ValueFinder import ValueFinder
import re

class ChargeFinder(ValueFinder):
    def __init__(self) -> None:
        super().__init__()
        self._type = "charge"
    
    def find_value(self, log_file) -> dict:
        with open(log_file, 'r') as inf:
            lines = inf.readlines()
            for line in lines:
                if line.find("Charge = ") != -1:
                    line = re.split(r"\s+",line)
                    return {self._type, int(line[3])}

        return {self._type, None}
