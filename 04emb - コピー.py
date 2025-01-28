
##### Embedding(埋め込み) ベクトルDBを作成 #####

# 1.ライブラリの読み込み 
import os
from langchain_openai import AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  

# 2.embedding(埋め込み)用のﾓﾃﾞﾙを定義
embeddings = AzureOpenAIEmbeddings(
                        azure_deployment="text-embedding-3-small-2"
                        ,openai_api_version="2024-06-01"
                    )   

# 3.テキストファイルの読み込み
documents = []
for file in os.listdir("./news"):
    if file.endswith(".txt"):
        loader = TextLoader(f"./news/{file}", encoding="utf-8")
        documents.extend(loader.load()) 

# 4.テキストの分割
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# 5.ベクトルDBの作成
db = Chroma.from_documents(texts,embeddings, persist_directory="vector_db" )

# 6.保存したデータベースを読み込んで、データが作成されているかを確認する
loaded_db = Chroma(persist_directory="vector_db", embedding_function=embeddings)
print(f"データベース作成完了。チャンク{loaded_db._collection.count()} 件を保存しています")




