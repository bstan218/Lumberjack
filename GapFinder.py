from ValueFinder import ValueFinder

class GapFinder(ValueFinder):
    def __init__(self) -> None:
        super().__init__()
        self._type = "gap"

    def get_type(self) -> str:
        return self._type

    def find_values(self, log_file) -> dict:
        if not self.job_completed(log_file):
            return {self.get_type() : None}
        
        with open(log_file, 'r') as inf:
            lines = inf.readlines()
            unoccupied = ""
            for line in reversed(lines):
                if "Alpha  occ. eigenvalues" in line:
                    occupied=line
                    
                    homo = float(occupied.split()[-1])
                    lumo = float(unoccupied.split()[4])
                    gap = lumo-homo

                    return {self._type : gap}

                unoccupied = line
        
        return {self._type : None}
        



if __name__ == "__main__":
    gf = GapFinder()

    inf = "Output_batch2dehydro_xtb_5102024.125748\\valid_ligands\\ABOPOX_Ni_2_3_CNN\\1olefin.log"

    print(gf.find_values(inf))