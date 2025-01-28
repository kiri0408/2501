##### シンプルチャット #####

# 1.ライブラリのインポート
import chainlit as cl
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 2.LLMモデルの定義
model = AzureChatOpenAI( deployment_name="gpt-4o-3"
                        ,openai_api_version="2024-10-21"
                        ,max_tokens= 100     # LLMからの回答の最大トークン数  (LLMからの回答が長くなってしまうことがあるので試行では上限を設定する)
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

# 5.メイン処理
# 5.1 ブラウザを開いたときの処理
@cl.on_chat_start
def start():
    cl.user_session.set("chain", chain)

# 5.2 ユーザが入力したときの処理
@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    response = await cl.make_async(chain.invoke)({"user_message": message.content})
    await cl.Message(content=response).send()


