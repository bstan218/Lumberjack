from Table import Table
import sys

#indir is a directory of ligand directories, each of which contains log files
def main():
    if len(sys.argv) > 2:    
        indir = sys.argv[1]
        csv_file = sys.argv[2]
    else:
        #indir = 'Output_batch3dehydro_xtb_5132024.14728'
        indir = 'Output_batch4dehydro_xtb_5152024.15430/valid_ligands'
        csv_file = 'features.csv'
        
    table = Table(csv_file)


if __name__ == "__main__":
    main()