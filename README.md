# solar-as-judge
<img width="1422" alt="image" src="https://github.com/hunkim/solar-as-judge/assets/901975/738be829-1d20-4b9a-baad-e3f2c8d066c5">


## How to use
Set the UPSTAGE_API_KEY environment variable. Obtain your key from the Upstage console at <https://console.upstage.ai>.

```python
import solar_as_judge as saj

# test prompt with an optional ground truth.
prompt = "Please extract one keyword from this text: I love you so much"
ground_truth = "love"

# The outcome of the A and B language models (AB testing).
A_answer = "love"
B_answer = "so much"

# Check the scores and the winner. 
# If they are consistent, then determine the final score.
a_score, b_score = saj.judge(prompt, A_answer, B_answer, ground_truth)
print(a_score, b_score)

```

## Get detailed scores

```python
import solar_as_judge as saj

# test prompt with an optional ground truth.
prompt = "Please extract one keyword from this text: I love you so much"
ground_truth = "love"

# The outcome of the A and B language models (AB testing).
A_answer = "love"
B_answer = "so much"


# Get scores separately.
A_score = saj.get_judge_score(prompt, A_answer, ground_truth)
B_score = saj.get_judge_score(prompt, B_answer, ground_truth)

# Determine the winner.
winner = saj.get_winner(prompt, A_answer, B_answer, ground_truth)
print(A_score, B_score, winner)
```
