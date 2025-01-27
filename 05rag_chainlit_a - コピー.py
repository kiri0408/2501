##### RAG検索 ##### 

# 1.ライブラリの読み込み 
import chainlit as cl
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 2.LLMモデルの定義
model = AzureChatOpenAI( deployment_name="gpt-4o-3"
                        ,openai_api_version="2024-10-21"
                        ,max_tokens= 100     # LLMからの回答の最大トークン数 (LLMからの回答が長くなってしまうことがあるので試行では上限を設定する)
                        )  

# 3.embedding(埋め込み)用のﾓﾃﾞﾙを定義
embeddings = AzureOpenAIEmbeddings(
                        azure_deployment="text-embedding-3-small-2"
                        ,openai_api_version="2024-06-01"
                    )   

# 4.ベクトルDBをセット
db = Chroma(persist_directory=r"./vector_db", embedding_function=embeddings)
retriever = db.as_retriever()

# 5.プロンプトの定義
prompt = ChatPromptTemplate.from_template('''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
''')

# 6.chainの定義
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 7.処理開始時にchainをセット 
@cl.on_chat_start
def start():
    cl.user_session.set("chain", chain)

# 8.メッセージ入力時
@cl.on_message
async def main(message: cl.Message):

    # chainを使ってRAGを実行。LLMで回答を生成してブラウザに表示 
    chain = cl.user_session.get("chain")
    answer = await cl.make_async(chain.invoke)(message.content)
    await cl.Message(content=answer).send()

    # 引用文の表示 
    query_results = db.similarity_search_with_score(message.content, k=3)
    if query_results:
        source_elements = []
        for i, (source, score) in enumerate(query_results):
            content = f"誤差: {score}\n\n{source.page_content}"
            source_elements.append(cl.Text(name=f"引用文", content=content))
        await cl.Message(content="参考:", elements=source_elements).send()

