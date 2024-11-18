from transformers import pipeline

nli_model = pipeline("text-classification", model="roberta-large-mnli")


result = nli_model(f"{Expected} </s></s> {Actual}")

print(result)

print(f"Relationship: {result[0]['label']} (Confidence: {result[0]['score']:.2f})")

if result[0]['label'] == 'CONTRADICTION':
    print("The actual response is opposite to the expected response.")
elif result[0]['label'] == 'ENTAILMENT':
    print("The actual response supports the expected response.")
else:
    print("The actual response is neutral with respect to the expected response.")
