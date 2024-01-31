from ete3 import NCBITaxa
import numpy as np
import pandas as pd
import sys

#чтение файла с консоли
file_path = sys.argv[1]
df_start = pd.read_table(file_path)
#с компьютера
#df_start = pd.read_table("mammals.tsv")
#удаление копий
df_first_occurrence = df_start.drop_duplicates(subset='Genus/Species', keep='first')
#удаление надписей с spp
df_first_occurrence = df_first_occurrence[~df_first_occurrence['Genus/Species'].str.contains('spp|spp.', case=False)]
#дополнительная чистка имен от надписей (= ...)
def clean_species_name(name):
    if '(=' in name and ')' in name:
        start_index = name.index('(=')
        end_index = name.index(')')
        name = name[:start_index] + name[end_index+1:]
    return ' '.join(name.split())  # используем join() для удаления лишних пробелов

# Применяем функцию к столбцу 'Genus/Species'
df_first_occurrence['Genus/Species'] = df_first_occurrence['Genus/Species'].apply(clean_species_name)
df_first_occurrence = df_first_occurrence.reset_index(drop=True)
print(df_first_occurrence)

ncbi = NCBITaxa()
df = pd.DataFrame(columns=['taxid'])
i = 0
while i < (len(df_first_occurrence['Genus/Species'])):
    if (ncbi.get_name_translator([df_first_occurrence['Genus/Species'][i]]) != {}):
        name2taxid = ncbi.get_name_translator([df_first_occurrence['Genus/Species'][i]])
        df.loc[i] = [name2taxid[df_first_occurrence['Genus/Species'][i]]]
        #print(name2taxid[df_first_occurrence['Genus/Species'][i]], i)
        i += 1
    else:
        df_first_occurrence = df_first_occurrence.drop(i)
        df_first_occurrence = df_first_occurrence.reset_index(drop=True)
print(df)

df['taxid'] = df['taxid'].apply(lambda x: x[0])

df_sorted = df.sort_values(by='taxid')
print(df_sorted)

df_sorted.to_csv('resourses/taxa_for_script.txt', sep='\t', index=False, header=False)