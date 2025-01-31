from upload_data_1 import collection

def retrieve_relevant_info(query, top_k=3):
    """사용자 질문을 벡터화 후 ChromaDB에서 가장 관련 있는 문서 검색"""
    results = collection.query(
        query_texts=[query],
        n_results=top_k  # 검색 결과 상위 3개 가져오기
    )
    
    retrieved_texts = results["documents"][0] if "documents" in results else []
    return "\n".join(retrieved_texts)  # 검색된 문서를 하나의 문자열로 반환
