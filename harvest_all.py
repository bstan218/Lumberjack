import sys
from Table import Table
from gap_to_csv import dehydro_gaps_to_table
from refactored_scf_to_csv import dehydro_scfs_to_table





column_order = ['scf:reactants','scf:TS-CH-Add-1-2','scf:Alkyl-Hydride-1-2','scf:TS-BHT-1-2','scf:1olefin','scf:TS-1olefin-diss','scf:products',
                'gap:reactants','gap:TS-CH-Add-1-2','gap:Alkyl-Hydride-1-2','gap:TS-BHT-1-2','gap:1olefin','gap:TS-1olefin-diss','gap:products']


def main():
    if len(sys.argv) > 2:    
        indir = sys.argv[1]
        csv_file = sys.argv[2]
    else:
        #indir = 'Output_batch2dehydro_xtb_5102024.125748\\valid_ligands'
        indir = 'screened ligand log files'
        csv_file = 'allfeatures.csv'
        
    table = Table(csv_file, index_column='ligand')
    table.set_columns(column_order)

    dehydro_scfs_to_table(indir, table)
    table.round_df(1)

    dehydro_gaps_to_table(indir, table)
    table.round_df(3)

    table.write_to_csv()




if __name__ == "__main__":
    main()