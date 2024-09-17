from ValueFinder import ValueFinder
import os

class LogHarvester() :

    def __init__(self, directory:str, value_finder:ValueFinder) -> None:
        self.value_finder = value_finder
        self.filetype='.log'
        self.directory = directory

    def harvest_file(self, state_file_path:str) -> dict:
        values = self.value_finder.find_values(state_file_path)
        statename = state_file_path.split("\\")[-1].split(".")[0]
        file_dict = {}
        for key in values:
            filekey = key + ":" + statename
            file_dict[filekey] = values[key]

        return file_dict

    def harvest_reaction(self, reaction_file_path:str) -> dict:
        reaction_dict = {}
        for state in os.listdir(reaction_file_path):
            if state.endswith(self.filetype):
                #print(statename)
                state_file_path = reaction_file_path + "\\" + state
                values = self.harvest_file(state_file_path)
                for key in values:
                    if values[key]:
                        reaction_dict[key] = values[key]

        return reaction_dict

    def harvest_reaction_directory(self) -> dict:
        directory_dictionary = {}

        for ligand_name in os.listdir(self.directory):
            #print(ligname)
            reaction_file_path = self.directory + "\\" + ligand_name
            reaction_dict = self.harvest_reaction(reaction_file_path)
            directory_dictionary[ligand_name] = reaction_dict
        
        return directory_dictionary

