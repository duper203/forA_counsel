import chromadb
import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import fitz  # PyMuPDF
import os

## ------- setting ------- ##

# OpenAI API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# ChromaDB 클라이언트 초기화
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # 로컬 DB 저장
embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY)
# ChromaDB 컬렉션 생성
collection = chroma_client.get_or_create_collection(name="adhd_docs", embedding_function=embedding_function)


# 1. extract pdf


def extract_text_from_pdf(pdf_path):
    """PDF에서 텍스트 추출"""
    doc = fitz.open(pdf_path)
    text_list = []
    
    for page in doc:
        text = page.get_text("text")
        text_list.append(text)
    
    return text_list  # 페이지별 텍스트 리스트 반환


def store_paper_in_chromadb(pdf_path, doc_id_prefix="adhd_paper"):
    """PDF 논문에서 텍스트 추출 후 ChromaDB에 저장"""
    text_list = extract_text_from_pdf(pdf_path)

    for idx, text in enumerate(text_list):
        collection.add(documents=[text], ids=[f"{doc_id_prefix}_{idx}"])
    
    print(f"📚 {len(text_list)}개의 페이지가 ChromaDB에 저장되었습니다.")

# 예제 논문 저장
store_paper_in_chromadb("./data/doc1.pdf")
