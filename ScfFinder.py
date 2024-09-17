import ValueFinder

class ScfFinder(ValueFinder.ValueFinder):
    def __init__(self):
        super().__init__()
        self._type = 'scf'
    
    def find_values(self, log_file) -> dict:
        with open(log_file, 'r') as inf:
            lines = inf.readlines()
            subsequent_line = ""
            for line in reversed(lines):
                twolines = line.strip()+subsequent_line.strip()
                if "HF=" in twolines:
                    linelst = twolines.split("\\")
                    for e in linelst:
                        if "HF=" in e:
                            value = float(e.strip("HF="))*627.51
                            return {self.get_type() : value}

                subsequent_line=line
                
                


        return {self.get_type() : None}
    
    def get_type(self) -> str:
        return self._type



if __name__ == "__main__":
    ScfFinder()