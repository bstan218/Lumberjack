import sys
import os
import re

import pandas as pd
from Table import Table
 
#load excel file
 
#open workbook
 
#modify the desired cell
#sheet["A1"] = "Full Name"
#print(sheet["A2"].row) 
#save the file


#sheet.cell(5,5).value = "writing to 5,5"
#need to do .save() after!
#workbook.save(filename="Dehydrogenation.xlsx")

def extractCharge(file):
    with open(file, 'r') as inf:
        lines = inf.readlines()
        for line in lines:
            if line.find("Charge = ") != -1:
                line = re.split(r"\s+",line)
                return line[3]

    return None
    
    print(line)

def extractSCF(file):
    linefound = False
    with open(file, 'r') as inf:
        lines = inf.readlines()
        breaknext=False
        for line in lines:
            if breaknext:
                secondline=line
                break

            if line.find("HF=") != -1:
                firstline=line
                breaknext=True
                linefound = True
    
    if linefound:
        #print("*SCF found!")
        line = firstline.strip() + secondline.strip()
        for item in line.split("\\"):
            if item.startswith("HF="):
                return float(item.strip("HF="))
    
    #print("SCF NOT FOUND")
    return None


def create_scf_nested_dictionary(indir):
    filepath1 = f"{indir}//valid_ligands"
    master_dict = {}
    


    for ligname in os.listdir(filepath1):
        valuesdict = {}
        charge = None
        chargefound = False


        print(ligname)
        filepath2 = filepath1 + "\\" + ligname
        for state in os.listdir(filepath2):
            if state.endswith('.log'):
                statename = state.split(".")[0]
                #print(statename)
                filepath3 = filepath2 + "\\" + state
                scfvalue = extractSCF(filepath3)
                if not chargefound:
                    charge = extractCharge(filepath3)
                    if charge:
                        chargefound = True
                        valuesdict['charge'] = (charge)
                if scfvalue:
                    valuesdict[statename] = scfvalue*627.51
                #print(scfval)
        master_dict[ligname] = valuesdict
    
    return master_dict

hexane = -236.8855949*627.51
one_hexene = -235.6565645*627.51
dehydro_states = ['reactants','TS-CH-Add-1-2','Alkyl-Hydride-1-2','TS-BHT-1-2','1olefin','TS-1olefin-diss','products']

def main():
    if len(sys.argv) > 2:    
        indir = sys.argv[1]
        csv_file = sys.argv[2]
    else:
        #indir = 'Output_batch3dehydro_xtb_5132024.14728'
        indir = 'Output_batch4dehydro_xtb_5152024.15430'
        csv_file = 'features.csv'
        
    table = Table(csv_file)

    scf_dictionary = create_scf_nested_dictionary(indir)

    for ligand_name in scf_dictionary:
        for state in scf_dictionary[ligand_name]:
            value = scf_dictionary[ligand_name][state]
            if state == 'lig':
                if value:
                    reactants = value + hexane
                    table.update_value(ligand_name, 'reactants', reactants)
            elif state == 'ligh2':
                if value:
                    products = value + one_hexene
                    table.update_value(ligand_name, 'products', products)
            else:
                table.update_value(ligand_name, state, value)
        print(f'{ligand_name}: {table.df.loc[ligand_name]}')

    table.minimum_normalization(dehydro_states)

    #table.print()
    table.write_to_csv(csv_file)
    table.print()


if __name__ == "__main__":
    main()
    