import numpy as np
import pandas as pd


class Table():

    def __init__(self, csvpath, index_column=None) -> None:
        self.csvpath = csvpath
        self.index_column = index_column
        if index_column:
            self.df = pd.read_csv(csvpath, index_col=index_column)
        else:
            self.df = pd.read_csv(csvpath)

    def get_dataframe(self):
        return self.df
    
    def add_row(self, rowname):
        if rowname not in self.df.index:
            self.df.loc[rowname] = [None] * len(self.df.columns)

    def add_column(self, column):
        if column not in self.df.columns:
            self.df[column] = [None] * len(self.df.index)

    def set_columns(self, column_list):
        for column in column_list:
            self.add_column(column)

    def update_value(self, row, column, value, override=True):
        if row not in self.df.index:
            self.add_row(row)
        if column not in self.df.columns:
            self.add_column(column)
        
        if (self.df.at[row,column] == None) | (override==True):
            self.df.at[row,column] = value

    def write_to_csv(self, csvpath:str=None, index_col:str=None):
        if not csvpath:
            csvpath = self.csvpath
        
        if not index_col:
            index_col = self.index_column

        self.df.to_csv(csvpath, index_label="ligand", na_rep='None')
    
    def minimum_normalize_row(self, row, columns):    
        row_series = self.df.loc[row]
        #print(row_series)
        considered_values = []
        for index in row_series.index:
            if index in columns:
                value = row_series.at[index]
                if isinstance(value, (float,int)) and not pd.isna(value) :
                    considered_values.append(value)
        
        minimum_value = 0
        if len(considered_values) > 0:
            minimum_value = min(considered_values)

        for index in row_series.index:
            if (index in columns) and isinstance(row_series.at[index], (float,int)) and not pd.isna(row_series.at[index]):
                self.df.at[row,index] -= minimum_value

    def minimum_normalization(self, columns):
        for row in self.df.index:
            self.minimum_normalize_row(row, columns)
    
    def round_df(self, roundto=1, restrict_columns_to:list=None):
        for row in self.df.index:
            if not restrict_columns_to or row in restrict_columns_to:
                for col in self.df.columns:
                    value = self.df.at[row,col]
                    if isinstance(value,float):
                        self.df.at[row,col] = round(value, roundto)

    def find_max_value(self, row, column_list, allow_null_values):
        #finds the maximum value in a row from a list of columns
        max_value = 0
        
        for column in column_list:
            val = self.df.at[row,column]
            if pd.isna(val):
                return np.nan
            else:
                if val > max_value:
                    max_value = val
        
        return max_value
    
    def create_max_value_column(self, column_name, column_list, allow_null_values=True):
        #the allow_null_values parameter, when false, will only add a value to the max value column if all column values contain a value
        self.add_column(column_name)

        for row in self.df.index:
            max_value = self.find_max_value(row, column_list, allow_null_values)
            self.update_value(row, column_name, max_value)

    def __str__(self):
        return self.df.__str__()


            

def main():
    infile='features.csv'
    table = Table(infile)
    #for line in open(infile, 'r'):
        #print(line)

    print(table)

if __name__ == '__main__':
    main()


