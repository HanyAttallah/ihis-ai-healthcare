import json
from functools import lru_cache
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parents[3]

KNOWLEDGE_PATH = (
    ROOT
    / "data"
    / "patient_education_knowledge.json"
)


@lru_cache(maxsize=1)
def load_rag():
    with open(
        KNOWLEDGE_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        documents = json.load(f)

    texts = [
        f"{item['title']} {item['category']} {item['content']}"
        for item in documents
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    matrix = vectorizer.fit_transform(
        texts
    )

    return documents, vectorizer, matrix


def answer_patient_question(question):
    documents, vectorizer, matrix = load_rag()

    query = vectorizer.transform(
        [question]
    )

    similarities = cosine_similarity(
        query,
        matrix,
    )[0]

    ranked_indices = similarities.argsort()[::-1]

    retrieved = []

    for index in ranked_indices[:3]:
        score = float(similarities[index])

        if score <= 0:
            continue

        item = documents[index].copy()
        item["retrieval_score"] = score
        retrieved.append(item)

    if not retrieved:
        return {
            "answer": (
                "I could not find sufficiently relevant information "
                "in the local patient-education knowledge base. "
                "Please ask a healthcare professional for guidance."
            ),
            "sources": [],
            "retrieved_context": [],
            "model_name": "iHIS Local TF-IDF RAG",
            "model_version": "1.0",
            "disclaimer": (
                "Educational patient information only. "
                "This assistant does not provide diagnosis or replace "
                "professional medical advice."
            ),
        }

    primary = retrieved[0]

    answer = (
        f"Based on the retrieved iHIS patient-education material: "
        f"{primary['content']}"
    )

    if len(retrieved) > 1:
        answer += (
            " Additional related information was retrieved from: "
            + ", ".join(
                item["title"]
                for item in retrieved[1:]
            )
            + "."
        )

    return {
        "answer": answer,
        "sources": [
            {
                "title": item["title"],
                "category": item["category"],
                "score": item["retrieval_score"],
            }
            for item in retrieved
        ],
        "retrieved_context": retrieved,
        "model_name": "iHIS Local TF-IDF RAG",
        "model_version": "1.0",
        "disclaimer": (
            "Educational patient information only. "
            "This assistant does not provide diagnosis or replace "
            "professional medical advice."
        ),
    }
