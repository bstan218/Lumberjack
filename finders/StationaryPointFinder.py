from ValueFinder import ValueFinder

class StationaryPointFinder(ValueFinder):

    def __init__(self):
        super().__init__()
        self._type = 'stationary_point'
    
    def find_values(self, log_file) -> bool:
        found=False
        with open(log_file, 'r') as inf:
            lines = inf.readlines()
            subsequent_line = ""
            for line in reversed(lines):
                twolines = line.strip()+subsequent_line.strip()
                #print(twolines)
                if "stationary point found" in twolines:
                    found=True
                subsequent_line=line

        return found
    
    def get_type(self) -> str:
        return self._type
