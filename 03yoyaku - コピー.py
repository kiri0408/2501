##### 文書の要約 #####

# 1.ライブラリの読み込み 
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# 2.LLMの定義
model = AzureChatOpenAI( deployment_name="gpt-4o-3"
                        ,openai_api_version="2024-10-21"
                        ,max_tokens= 100     # LLMからの回答の最大トークン数  (LLMからの回答が長くなってしまうことがあるので試行では上限を設定する)
                        )  

# 3.プロンプトの型を定義 
prompt = ChatPromptTemplate.from_messages(
  [ "次の文章を100文字以内に要約してください。\n\n  {content}"] )  

# 4.処理ステップの連結
chain = prompt | model | StrOutputParser()

# 5.メイン処理
# 5.1  フォルダ内のファイルのパスを取得
folder_path = 'news'  # ここにフォルダパスを指定
files = os.listdir(folder_path)

# 5.2 ファイルを一つずつ要約し別名で保存
for file_name in files:
    if file_name.startswith("news") and file_name.endswith(".txt"):
        file_path = os.path.join(folder_path, file_name)
        
        # テキストの読み込み
        with open(file_path, 'r', encoding='utf8') as f:
            text = f.read()

        # 読み込んだテキストを chainへ渡して、要約を実行 
        response = chain.invoke({"content": text})
        
        # 新しいファイル名を作成
        new_file_name = f'要約_{file_name}'
        new_file_path = os.path.join(folder_path, new_file_name)

        # 保存
        with open(new_file_path, 'w', encoding='utf8') as f:
            f.write(response)
        print(f'要約した内容を {folder_path}/{new_file_name} に保存しました。')



