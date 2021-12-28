import pandas as pd

DB_FT = pd.DataFrame()

for i in range(1,10) :
    globals()[f'df_{i}'] = pd.DataFrame()
    DB_FT = pd.concat([DB_FT, globals()[f'df_{i}']])


listduSN = DB_FT.loc[DB_FT['SPEC_NO'].duplicated(), 'SPEC_NO'].drop_duplicates()

print('done')