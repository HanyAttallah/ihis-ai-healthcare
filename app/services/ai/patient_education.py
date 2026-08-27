import json
import os
from functools import lru_cache
from pathlib import Path

from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parents[3]

KNOWLEDGE_PATH = (
    ROOT
    / "data"
    / "patient_education_knowledge.json"
)

RETRIEVER_NAME = "iHIS TF-IDF Knowledge Retriever"
RAG_VERSION = "2.2"


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

    return (
        documents,
        vectorizer,
        matrix,
    )


def retrieve_context(
    question,
    top_k=3,
):
    documents, vectorizer, matrix = load_rag()

    query = vectorizer.transform(
        [question]
    )

    similarities = cosine_similarity(
        query,
        matrix,
    )[0]

    ranked_indices = (
        similarities.argsort()[::-1]
    )

    retrieved = []

    for index in ranked_indices[:top_k]:
        score = float(
            similarities[index]
        )

        # Exclude weak lexical matches that are unlikely
        # to provide useful grounding context.
        if score < 0.10:
            continue

        item = documents[index].copy()
        item["retrieval_score"] = score

        retrieved.append(
            item
        )

    return retrieved


def build_context(
    retrieved,
):
    sections = []

    for position, item in enumerate(
        retrieved,
        start=1,
    ):
        sections.append(
            (
                f"[Source {position}]\n"
                f"Title: {item['title']}\n"
                f"Category: {item['category']}\n"
                f"Content: {item['content']}"
            )
        )

    return "\n\n".join(
        sections
    )


def deterministic_fallback(
    retrieved,
):
    primary = retrieved[0]

    return (
        "Based on the retrieved iHIS "
        "patient-education material: "
        f"{primary['content']}"
    )


def generate_grounded_answer(
    question,
    retrieved,
):
    api_key = os.getenv(
        "GROQ_API_KEY",
        "",
    ).strip()

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b",
    )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    context = build_context(
        retrieved
    )

    instructions = (
        "You are the Patient Education AI inside an "
        "educational hospital information-system prototype. "
        "Answer only from the retrieved local context supplied "
        "by the application. Do not invent facts that are not "
        "contained in the retrieved context. If the context is "
        "insufficient, state that the local knowledge base does "
        "not contain enough information. Use clear patient-friendly "
        "language. Do not diagnose the user, prescribe individualized "
        "treatment, or replace professional medical advice. "
        "Keep the response concise. Return plain text only. "
        "Do not use Markdown formatting, Markdown headings, "
        "asterisk emphasis, or other markup symbols."
    )

    input_text = (
        f"Patient education question:\n"
        f"{question}\n\n"
        f"Retrieved local knowledge-base context:\n"
        f"{context}"
    )

    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=input_text,
        max_output_tokens=500,
    )

    answer = (
        response.output_text
        or ""
    ).strip()

    # Keep browser presentation plain-text even if the
    # external model emits occasional Markdown emphasis.
    answer = (
        answer
        .replace("**", "")
        .replace("__", "")
    )

    if not answer:
        raise RuntimeError(
            "Groq returned no answer text."
        )

    return (
        answer,
        model,
    )


def answer_patient_question(
    question,
):
    retrieved = retrieve_context(
        question
    )

    if not retrieved:
        return {
            "answer": (
                "I could not find sufficiently relevant "
                "information in the local patient-education "
                "knowledge base. Please ask a healthcare "
                "professional for guidance."
            ),

            "sources": [],

            "retrieved_context": [],

            "retriever_name": (
                RETRIEVER_NAME
            ),

            "generator_model": (
                "Not invoked"
            ),

            "generation_status": (
                "No relevant context retrieved"
            ),

            "model_name": (
                "iHIS RAG + Groq LLM"
            ),

            "model_version": (
                RAG_VERSION
            ),

            "provider": "Groq",

            "disclaimer": (
                "Educational patient information only. "
                "This assistant does not provide diagnosis "
                "or replace professional medical advice."
            ),
        }

    try:
        answer, generator_model = (
            generate_grounded_answer(
                question,
                retrieved,
            )
        )

        generation_status = (
            "LLM-generated answer grounded "
            "in retrieved local sources"
        )

    except Exception:
        answer = deterministic_fallback(
            retrieved
        )

        generator_model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b",
        )

        generation_status = (
            "LLM unavailable — deterministic "
            "grounded fallback used"
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

        "retriever_name": (
            RETRIEVER_NAME
        ),

        "generator_model": (
            generator_model
        ),

        "generation_status": (
            generation_status
        ),

        "model_name": (
            "iHIS RAG + Groq LLM"
        ),

        "model_version": (
            RAG_VERSION
        ),

        "provider": "Groq",

        "disclaimer": (
            "Educational patient information only. "
            "The answer is generated from retrieved "
            "local educational material and does not "
            "provide diagnosis or replace professional "
            "medical advice."
        ),
    }
