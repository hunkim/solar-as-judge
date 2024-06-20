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
        template="""You are an AI Language Model evaluator tasked with assessing the quality of 
an AI assistant's response to a user's question. 
Please rate the provided answer on a Likert scale of 1 to 5, 
with 5 indicating a very good answer and 1 indicating a bad answer. 
If there is a ground truth is given, 
take that into consideration when evaluating the response. 
Carefully read and consider the prompt and answer before formulating your evaluation. 
Think through the evaluation step by step. Let’s think step by step.

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
        template="""You are an AI Language Model evaluator responsible for selecting the better answer 
between two options, A or B, provided by an AI assistant in response to a user's question. 
Consider the ground truth, if available, when making your selection. 
Carefully read and consider the prompt and both answers before deciding. 
Choose the answer that best addresses the user's question and provide your selection in the form of JSON,
Let’s think step by step

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


def _judgeAB(
    prompt, A_answer, B_answer, ground_truth_answer=None, judge_llm=None, trials=7
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

def judge(
    prompt, A_answer, B_answer, ground_truth_answer=None, judge_llm=None, trials=7
):
    '''
    Judge the two answers A and B based on the prompt.
    If the answers are consistent, return the scores.
    If the answers are inconsistent, return 0, 0.

    Args:
    - prompt: str
    - A_answer: str
    - B_answer: str
    - ground_truth_answer: str
    - judge_llm: ChatUpstage
    - trials: int

    Returns:
    - A_score: int
    - B_score: int
    '''
    
    A_score1, B_score1 = _judgeAB(
        prompt, A_answer, B_answer, ground_truth_answer, judge_llm, trials
    )

    if A_score1 == 0 and B_score1 == 0:
        return 0, 0
    
    B_score2, A_score2 = _judgeAB(
        prompt, B_answer, A_answer, ground_truth_answer, judge_llm, trials
    )

    if A_score2 == 0 and B_score2 == 0:
        return 0, 0
    
    # Check if their scores are consistent
    if A_score1 > B_score1 and A_score2 > B_score2:
        return A_score1+A_score2, B_score1+B_score2
    elif B_score1 > A_score1 and B_score2 > A_score2:
        return A_score1+A_score2, B_score1+B_score2
    else:
        return 0, 0
