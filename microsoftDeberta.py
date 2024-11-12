
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name = "roberta-large-mnli"  # Or use "microsoft/deberta-v3-large-mnli"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

nli_model = pipeline("text-classification", model=model, tokenizer=tokenizer)

# [Example_1]
# Expected = "The Product is In Stock"
# Actual = "The Product Is Out Of Stock"
# Expected_Relationship = "CONTRADICTION"


# [Example_2]
# Expected = """Dear Marti,\nThank you for your order #296587. Unfortunately, due to unforeseen circumstances, your product shipment has been delayed. We expect your order to ship around mid November. We truly value you as a customer and apologize for any disappointment this may cause. We will be sure to keep you updated on any changes to the timing of your order shipment.
# \nThank you for being a part of the Wisteria family!"""
# Actual = "The order is delayed due to unforeseen circumstances order will arrive in November"
# Expected_Relationship = "ENTAILMENT"

# [Example_3]
Expected = """Dear Customer,\nWe are delighted to inform you that we have a new selection of products available for the holiday season. Check out our latest collection on the Wisteria website and enjoy exclusive discounts!"""
Actual = "The order was received and is being processed. Thank you for shopping with us."
Expected_Relationship = "NEUTRAL"

# [Example_4]
# Expected = """Hi Amy,\nThank you for reaching out to Wisteria, my name is Cassy, I am happy to assist you.\nI have checked on your order, and unfortunately due to unforeseen circumstances, your item is on back order at this time with the manufacturer, and is due to ship January 15, 2025.\nWe certainly apologize for this. Feel free to reply to this email at any time for updates, sometimes these dates can change./\nWe will provide a tracking link as soon as it is available."""
# Actual = """Hi Amy,\nYour order details are as follows:\nOrder number: #296496\nOrder Date: 10/7/2024\nItem Number: 118-111307\nItem Name: Ingalls Chest\nESD: The item is currently scheduled for delivery on January 15, 2025.\nWe will provide a tracking link as soon as it is available.\nIs there anything else I can assist you with?\nBest regards,\nSophia"""
# Expected_Relationship = "NEUTRAL"

# [Example_5]
# Expected = "We do not allow exchanges for sale items."
# Actual =  "Sale items can be exchanged for store credit."
# Expected_Relationship = "CONTRADICTION"


input_text = f"{Expected} </s></s> {Actual}"
result = nli_model(input_text)[0]
print(f"Expected Relationship: {Expected_Relationship}")
print(f"Predicted Relationship: {result['label']} (Confidence: {result['score']:.2f})\n")
if result['label'] == 'CONTRADICTION':
    print("Interpretation: The actual response contradicts the expected response.")
elif result['label'] == 'ENTAILMENT':
    print("Interpretation: The actual response supports the expected response.")
else:
    print("Interpretation: The actual response is neutral with respect to the expected response.")
print("= " * 50)
