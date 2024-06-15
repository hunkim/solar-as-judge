# Test the solar_as_judge package


import solar_as_judge as saj

def test_solar_as_judge():
    prompt = "Please extract one keyword from this text: I love you so much"
    ground_truth = "love"
    A_answer = "love"
    B_answer = "so much"

    A_score = saj.get_judge_score(prompt, A_answer, ground_truth)
    B_score = saj.get_judge_score(prompt, B_answer, ground_truth)

    winner = saj.get_winner(prompt, A_answer, B_answer, ground_truth)
    print(A_score, B_score, winner)

    a_score, b_score = saj.judge(prompt, A_answer, B_answer, ground_truth)
    print(a_score, b_score)

if __name__ == "__main__":
    test_solar_as_judge()