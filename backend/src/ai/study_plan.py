from typing import TypedDict

from pydantic import BaseModel

from langgraph.graph import StateGraph, START, END

from src.ai.langchain_llm import llm


class StudyDay(BaseModel):
    day: int
    topics: list[str]
    tasks: list[str]


class StudyPlan(BaseModel):
    plan: list[StudyDay]


class StudyPlanState(TypedDict):
    text: str
    duration_days: int
    plan: dict


plan_llm = llm.with_structured_output(StudyPlan)


async def generate_plan_node(
    state: StudyPlanState,
):

    prompt = f"""
Create a {state["duration_days"]}-day study plan
based ONLY on the lecture material below.

For each day provide:
- day number
- topics to study
- specific study tasks

Make it realistic for a college student.

Lecture material:

{state["text"]}
"""

    result = await plan_llm.ainvoke(prompt)

    return {
        "plan": result.model_dump()
    }


builder = StateGraph(StudyPlanState)

builder.add_node(
    "generate_plan",
    generate_plan_node,
)

builder.add_edge(
    START,
    "generate_plan",
)

builder.add_edge(
    "generate_plan",
    END,
)

study_plan_graph = builder.compile()


async def generate_study_plan(
    text: str,
    duration_days: int,
):

    result = await study_plan_graph.ainvoke(
        {
            "text": text,
            "duration_days": duration_days,
            "plan": {},
        }
    )

    return result["plan"]