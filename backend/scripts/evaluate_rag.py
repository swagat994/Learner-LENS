import asyncio
import json
import sys
from pathlib import Path

from ragas.metrics.collections import (
    Faithfulness,
    ResponseRelevancy,
    ContextPrecision,
    ContextRecall,
)

from src.rag.retriever import retrieve_relevant_chunks
from src.ai.chat import answer_question


# --------------------------------------------------
# Configuration
# --------------------------------------------------

USER_ID = "6a7252157d896039b0392a0a"
COURSE_ID = "6a93ff6afeb75fa65515223e"

QUESTIONS_FILE = Path(
    "learnerlens_ragas_benchmark/evaluation_questions.json"
)

OUTPUT_FILE = Path(
    "learnerlens_ragas_benchmark/ragas_results.json"
)


# --------------------------------------------------
# Load benchmark questions
# --------------------------------------------------

def load_questions():

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# --------------------------------------------------
# Run LearnerLens RAG
# --------------------------------------------------

async def generate_rag_response(question):

    chunks = retrieve_relevant_chunks(
        question=question,
        user_id=USER_ID,
        course_id=COURSE_ID,
        n_results=5,
    )

    contexts = [
        chunk["text"]
        for chunk in chunks
    ]

    context = "\n\n".join(contexts)

    answer = await answer_question(
        question=question,
        context=context,
    )

    return answer, contexts


# --------------------------------------------------
# Evaluate one question
# --------------------------------------------------

async def evaluate_question(
    question_data,
    faithfulness,
    response_relevancy,
    context_precision,
    context_recall,
):

    question = question_data["question"]

    reference = question_data["reference_answer"]

    print()
    print("=" * 70)
    print(f"Question: {question}")
    print("=" * 70)

    answer, contexts = await generate_rag_response(
        question
    )

    print()
    print("Generated Answer:")
    print(answer)

    print()
    print(
        f"Retrieved Contexts: {len(contexts)}"
    )

    # ----------------------------------------------
    # Faithfulness
    # ----------------------------------------------

    faithfulness_result = await faithfulness.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts,
    )

    # ----------------------------------------------
    # Response Relevancy
    # ----------------------------------------------

    relevancy_result = await response_relevancy.ascore(
        user_input=question,
        response=answer,
    )

    # ----------------------------------------------
    # Context Precision
    # ----------------------------------------------

    precision_result = await context_precision.ascore(
        user_input=question,
        reference=reference,
        retrieved_contexts=contexts,
    )

    # ----------------------------------------------
    # Context Recall
    # ----------------------------------------------

    recall_result = await context_recall.ascore(
        user_input=question,
        reference=reference,
        retrieved_contexts=contexts,
    )

    result = {
        "id": question_data["id"],
        "lecture": question_data["lecture"],
        "question": question,
        "reference_answer": reference,
        "generated_answer": answer,
        "retrieved_contexts": contexts,
        "faithfulness": faithfulness_result.value,
        "response_relevancy": relevancy_result.value,
        "context_precision": precision_result.value,
        "context_recall": recall_result.value,
    }

    print()
    print("Metrics:")
    print(
        f"Faithfulness:       {faithfulness_result.value:.4f}"
    )
    print(
        f"Response Relevancy:  {relevancy_result.value:.4f}"
    )
    print(
        f"Context Precision:   {precision_result.value:.4f}"
    )
    print(
        f"Context Recall:      {recall_result.value:.4f}"
    )

    return result


# --------------------------------------------------
# Main evaluation
# --------------------------------------------------

async def main():

    print()
    print("=" * 70)
    print("LearnerLens RAG Evaluation")
    print("=" * 70)

    questions = load_questions()

    print(
        f"Loaded {len(questions)} evaluation questions."
    )

    # --------------------------------------------------
    # IMPORTANT:
    # These metric objects require an evaluator LLM.
    # We configure that separately below.
    # --------------------------------------------------

    faithfulness = Faithfulness()

    response_relevancy = ResponseRelevancy()

    context_precision = ContextPrecision()

    context_recall = ContextRecall()

    results = []

    for question_data in questions:

        result = await evaluate_question(
            question_data=question_data,
            faithfulness=faithfulness,
            response_relevancy=response_relevancy,
            context_precision=context_precision,
            context_recall=context_recall,
        )

        results.append(result)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print("=" * 70)
    print("Evaluation completed.")
    print("=" * 70)

    print(
        f"Results saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    asyncio.run(main())