# 필요한 라이브러리 임포트
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini")
prompt_template = """
Translate the following text from {from_lang} to {to_lang}:

"{text}"

Translated text:"""
prompt = PromptTemplate(
    template=prompt_template, input_variables=["from_lang", "to_lang", "text"]
)

translate_chain = LLMChain(llm=llm, prompt=prompt)


def translate_text(from_lang: str, to_lang: str, text: str) -> str:
    """
    지정된 언어로 텍스트를 번역하는 함수입니다.

    Args:
    - from_lang (str): 원본 텍스트의 언어 코드 (예: 'en', 'ko')
    - to_lang (str): 번역 대상 언어 코드
    - text (str): 번역할 텍스트

    Returns:
    - str: 번역된 텍스트
    """
    # 번역 Chain을 통해 번역된 텍스트 가져오기
    response = translate_chain.run(
        {"from_lang": from_lang, "to_lang": to_lang, "text": text}
    )
    return response.strip()
