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

   Ensure that the output is in the following JSON format exactly as shown:
    {{
      "Sentiment": "[ENTAILMENT, CONTRADICTION, or NEUTRAL]",
      "explanation": "[brief explanation for the intent classified reason]"
    }}"""
}