import sys
from Table import Table
from LogHarvester import LogHarvester
from GapFinder import GapFinder

def dehydro_gaps_to_table(ligand_directory:str, table:Table):
    gap_finder = GapFinder()
    log_harvester = LogHarvester(ligand_directory, gap_finder)

    directory_dictionary = log_harvester.harvest_reaction_directory()

    for ligand in directory_dictionary:
        for state in directory_dictionary[ligand]:
            value = directory_dictionary[ligand][state]
            if "ligh2" in state:
                state = state.replace("ligh2","products")
            elif "lig" in state:
                state = state.replace("lig","reactants")
            table.update_value(ligand, state, value)


def main():
    if len(sys.argv) > 2:    
        indir = sys.argv[1]
        csv_file = sys.argv[2]
    else:
        indir = 'Output_batch2dehydro_xtb_5102024.125748\\valid_ligands'
        #indir = 'screened ligand log files'
        csv_file = 'refactoredfeatures.csv'
        
    table = Table(csv_file, index_column='ligand')

    dehydro_gaps_to_table(indir, table)

    table.round_df(roundto=3)
    table.write_to_csv()





if __name__ == "__main__":
    main()
