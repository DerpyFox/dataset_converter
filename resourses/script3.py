import numpy as np
import pandas as pd
import sys

file_path = sys.argv[1]
file_path2 = sys.argv[2]

#"D:\\Jupiter_Lab\\mammals.tsv"
df_start = pd.read_table(file_path)
#"D:\\Jupiter_Lab\\res_for_script3_taxid.csv"
df_many = pd.read_csv(file_path2)
###
print("Стартовое количество Wild")
temp = 0
temp = df_start['Wild'].value_counts()
print(temp)

print("Стартовое количество Capt")
temp = df_start['Capt.'].value_counts()
print(temp)

print("Стартовое количество M/F")
temp = df_start['M/F'].value_counts()
print(temp)
df_start = df_start.drop_duplicates(subset='Genus/Species', keep='first')

df_start['Wild'] = pd.to_numeric(df_start['Wild'], errors='coerce')
df_start['Capt.'] = pd.to_numeric(df_start['Capt.'], errors='coerce')
print("Стартовая корреляция без копий значений")
correlation1 = df_start['Wild'].corr(df_start['Capt.'])
print(correlation1)

count_both_not_nan = df_start[df_start['Wild'].notna() & df_start['Capt.'].notna()].shape[0]
print("Количество элементов, для которых оба признака не NaN:", count_both_not_nan)

print("Получившийся датафрейм после преобразования двумя скриптами")
print(df_many)

df_many = df_many.dropna(subset=['ftp_path'])
#df_many = df_many[df_many['refseq_category'] != 'na']

df_many = df_many.reset_index(drop=True)

df_start = df_start.rename(columns={'Genus/Species': 'organism_name'})
merged_df = pd.merge(df_many, df_start, on='organism_name', how='left')

print("Измененное количество Wild")
temp = merged_df['Wild'].value_counts()
print("Всего элементов", len(merged_df['Wild'].dropna()))
print(temp)

print("Измененное количество Capt")
temp = merged_df['Capt.'].value_counts()
print("Всего элементов", len(merged_df['Capt.'].dropna()))
print(temp)

#######################

merged_df = merged_df[merged_df['refseq_category'] != 'na']
merged_df = merged_df.reset_index(drop=True)

print("Количество уникальных записей для каждого организма (должно быть по 1), нужны еще фильтры/что то работает неправильно")
counts = merged_df['organism_name'].value_counts()
print(counts)

#######################
merged_df = merged_df.dropna(subset=['Wild', 'Capt.'], how='all')
merged_df = merged_df.reset_index(drop=True)

print("Конечное количество Wild")
temp = merged_df['Wild'].value_counts()
print("Всего элементов", len(merged_df['Wild'].dropna()))
print(temp)

print("Конечное количество Capt")
temp = merged_df['Capt.'].value_counts()
print("Всего элементов", len(merged_df['Capt.'].dropna()))
print(temp)


merged_df['Wild'] = pd.to_numeric(merged_df['Wild'], errors='coerce')
merged_df['Capt.'] = pd.to_numeric(merged_df['Capt.'], errors='coerce')

correlation = merged_df['Wild'].corr(merged_df['Capt.'])

import matplotlib.pyplot as plt

merged_df['Wild'] = pd.to_numeric(merged_df['Wild'], errors='coerce')
merged_df['Capt.'] = pd.to_numeric(merged_df['Capt.'], errors='coerce')


plt.scatter(merged_df['Wild'], merged_df['Capt.'])
plt.title('Scatterplot между Wild и Capt на итоговых данных')
plt.xlabel('Wild')
plt.ylabel('Capt')
plt.show()
print("Финальная корреляция")
print(correlation)

#file_path = 'resourses/three_sc_res.csv'
#merged_df.to_csv(file_path, index=False)

counts = merged_df['organism_name'].value_counts()
print("Количество найденных геномов с копиями\n" ,counts)

import pandas as pd

def clean_dataframe(df):
    unique_organisms = df['organism_name'].unique()
    
    for organism in unique_organisms:
        organism_indices = df[df['organism_name'] == organism].index
        
        if len(organism_indices) == 1:
            continue
        
        gcf_indices = [i for i in organism_indices if df.loc[i, 'gbrs_paired_asm'].startswith('GCF')]
        gca_indices = [i for i in organism_indices if df.loc[i, 'gbrs_paired_asm'].startswith('GCA')]
        na_indices = [i for i in organism_indices if df.loc[i, 'gbrs_paired_asm'] == 'na']
        
        if gcf_indices:
            df.drop(gcf_indices[1:] + gca_indices + na_indices, inplace=True)
        elif gca_indices:
            df.drop(gca_indices[1:] + na_indices, inplace=True)
        else:
            df.drop(na_indices[1:], inplace=True)
    
    return df

cleaned_df = clean_dataframe(merged_df)

counts = cleaned_df['organism_name'].value_counts()
print("Количество найденных геномов без копий\n", counts)

cleaned_df = cleaned_df.reset_index(drop=True)
file_path = 'no_copy_res_final.csv'
cleaned_df.to_csv(file_path, index=False)