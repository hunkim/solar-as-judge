from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_upstage import ChatUpstage


# Define your desired data structure.
class Score(BaseModel):
    score: int = Field(
        description="A Likert scale 1 to 5. 1 is very negative, 5 is very positive."
    )


def get_judge_score(
    prompt, answer, ground_truth_answer, judge_llm=None, trials=3
):
    if judge_llm is None:
        judge_llm = ChatUpstage()

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Score)

    prompt_template = PromptTemplate(
        template="""You are an excellent judge.
For the given prompt and answer, please give a Likert scale 1 to 5.
5 is a very good answer, and 1 is bad.
If there is a ground truth, please consider it.
Please read the prompt and answer very carefully.
Think of it step by step.

The output should be json like this:
{{"score": 3}}
{{"score": 5}}
{{"score": 1}}

Only include the json output.
---
Prompt: {prompt}
Ground Truth: {ground_truth}
---
Answer: {answer}
---
""",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt_template | judge_llm | parser

    for _ in range(trials):
        try:
            score = chain.invoke(
                input={
                    "prompt": prompt,
                    "answer": answer,
                    "ground_truth": ground_truth_answer,
                }
            )
            return int(score["score"])
        except Exception as e:
            print(e)
    return -1


class Winner(BaseModel):
    winner: str = Field(description="Select the winer A or B")


def get_winner(
    prompt, A_answer, B_answer, ground_truth_answer, judge_llm=None, trials=3
):
    if judge_llm is None:
        judge_llm = ChatUpstage()
    
    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Score)

    prompt_template = PromptTemplate(
        template="""You are an excellent judge.
For the given prompt and answer A and answer B, please select which one is the better answer.
If there is a ground truth, please consider it when you select the winner.
Please read the prompt and answer very carefully.
Think of it step by step.

The output should be json like this:
{{"winner": "A"}}
{{"winner": "B"}}

Just include "A" or "B" in the json output.
Only include the json output, and do not include explnation or others.

---
Prompt: {prompt}
Ground Truth: {ground_truth}
---
Answer A: {A_answer}
---
Answer B: {B_answer}
---
""",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt_template | judge_llm | parser

    for _ in range(trials):
        try:
            winner = chain.invoke(
                input={
                    "prompt": prompt,
                    "A_answer": A_answer,
                    "B_answer": B_answer,
                    "ground_truth": ground_truth_answer,
                }
            )
            return winner["winner"]
        except Exception as e:
            print(e)
    return -1


def judge(
    prompt, A_answer, B_answer, ground_truth_answer=None, judge_llm=None, trials=3
):
    if judge_llm is None:
        judge_llm = ChatUpstage()
        
    for _ in range(trials):
        A_score = get_judge_score(prompt, A_answer, ground_truth_answer, judge_llm)
        B_score = get_judge_score(prompt, B_answer, ground_truth_answer, judge_llm)

        winner = get_winner(prompt, A_answer, B_answer, ground_truth_answer)
        if winner == "A" and A_score > B_score or winner == "B" and B_score > A_score:
            return A_score, B_score

    # Not conclusive
    return 0, 0
