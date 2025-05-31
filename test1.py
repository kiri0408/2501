import polars as pl

df_shain = pl.read_excel('test社員マスタ.xlsx',sheet_name='Sheet1')

print(df_shain)


