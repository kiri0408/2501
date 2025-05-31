import polars as pl

# Excelデータの読み込み
df_shain  = pl.read_excel('test社員マスタ.xlsx',sheet_name='Sheet1')
df_shohin = pl.read_excel('test商品マスタ.xlsx',sheet_name='Sheet1')
df_hanbai = pl.read_excel('test販売実績.xlsx'  ,sheet_name='Sheet1',read_options={"header_row": 2})

# 結合
df_all = df_hanbai.join(df_shain,on='社員番号',how='left')  #販売実績に社員ﾏｽﾀを結合
df_all = df_all.join(df_shohin,on='商品番号',how='left')    #販売実績に商品ﾏｽﾀを結合

#金額を計算
df_all = df_all.with_columns( (pl.col('数量') * pl.col('単価')).alias('金額'))
print(df_all)


