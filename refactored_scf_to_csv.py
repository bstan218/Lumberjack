import sys
from Table import Table
from LogHarvester import LogHarvester
from ScfFinder import ScfFinder


hexane = -236.8855949*627.51
one_hexene = -235.6565645*627.51
dehydro_states = ['reactants','TS-CH-Add-1-2','Alkyl-Hydride-1-2','TS-BHT-1-2','1olefin','TS-1olefin-diss','products']
scf_dehydro_states = [f'scf:{x}' for x in dehydro_states]

def dehydro_scfs_to_table(ligand_directory:str, table:Table):
    scf_finder = ScfFinder()
    log_harvester = LogHarvester(ligand_directory, scf_finder)

    directory_dictionary = log_harvester.harvest_reaction_directory()

    #print(directory_dictionary)

    for ligand in directory_dictionary:
        for state in directory_dictionary[ligand]:
            value = directory_dictionary[ligand][state]
            if 'ligh2' in state:
                if value:
                    products = value + one_hexene
                    table.update_value(ligand, 'scf:products', products)
            elif 'lig' in state:
                if value:
                    reactants = value + hexane
                    table.update_value(ligand, 'scf:reactants', reactants)
            else:    
                table.update_value(ligand, state, value)
    
    table.minimum_normalization(scf_dehydro_states)







def main():
    if len(sys.argv) > 2:    
        indir = sys.argv[1]
        csv_file = sys.argv[2]
    else:
        indir = 'Output_batch2dehydro_xtb_5102024.125748\\valid_ligands'
        #indir = 'screened ligand log files'
        csv_file = 'refactoredfeatures.csv'
        
    table = Table(csv_file, index_column='ligand')

    dehydro_scfs_to_table(indir, table)

    table.round_df()
    table.write_to_csv(csvpath=csv_file)



if __name__ == "__main__":
    main()