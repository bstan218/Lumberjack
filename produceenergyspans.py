from Table import Table
import sys


feature_table = Table('features.csv')

states = ['reactants','Alkyl-Hydride-1-2','TS-BHT-1-2','1olefin','TS-1olefin-diss','products']

out_table = 'energyspans.csv'

feature_table.create_max_value_column('energy_span', states, False)

df = feature_table.get_dataframe()

states.append('charge')
states.append('TS-CH-Add-1-2')
df_dropped = df.drop(states, axis=1)
df_sorted = df_dropped.sort_values(by='energy_span')


df_sorted.to_csv(out_table, index_label="ligand", na_rep='None')