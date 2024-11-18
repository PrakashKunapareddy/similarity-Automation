Similarity = {
    "system_message": """You are a helpful assistant tasked with comparing two responses to determine their relationship: whether they are in agreement, contradict each other, or are neutral.""",
    "user_message": """Analyze the relationship between the following Expected and Actual responses:

    Expected:
    {expected}

    Actual:
    {actual}

    Determine whether the Actual response:
    - ENTAILMENT (supports or aligns with) the Expected response
    - CONTRADICTION (opposes) the Expected response
    - NEUTRAL (neither supports nor opposes) with respect to the Expected response

    Additionally, calculate a similarity score between the Expected and Actual responses. This score should range from 0 to 1, where 1 indicates perfect similarity and 0 indicates no similarity.

    Ensure that the output is in the following JSON format exactly as shown:
    {{
      "Sentiment": "[ENTAILMENT, CONTRADICTION, or NEUTRAL]",
      "Similarity_Score": [similarity_score],
      "explanation": "[brief explanation for the intent classified reason]"
    }}"""
}
