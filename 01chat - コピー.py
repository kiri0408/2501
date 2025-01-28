##### シンプルチャット #####

# 1.ライブラリの読み込み 
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 2.LLMモデルの定義
model = AzureChatOpenAI( deployment_name="gpt-4o-3"
                        ,openai_api_version="2024-10-21"
                        ,max_tokens= 100     # LLMからの回答の最大トークン数 (LLMからの回答が長くなってしまうことがあるので試行では上限を設定する)
                        )  

# 3.プロンプトの型を定義 
prompt = ChatPromptTemplate.from_messages(
    ["""
    あなたはフレンドリーなお笑い芸人です。
    以下の質問に簡潔に答えてください。
    質問： {user_message}
    """  ] ) 

# 4.処理ステップの連結
chain = prompt | model | StrOutputParser()  

# 5.処理実行  （チャットを３回繰り返す） 
for i in range(3) :    
    str_user = input("質問をどうぞ: ")    
    response = chain.invoke({"user_message": str_user})    
    print(response)


