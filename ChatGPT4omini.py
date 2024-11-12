import json

from langchain.chains import LLMChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

from ChatGPT4ominiPrompt import Similarity

examples = [
    {
        "Expected": "The Product is In Stock",
        "Actual": "The Product Is Out Of Stock",
        "Expected_Relationship": "CONTRADICTION"
    },
    {
        "Expected": """Dear Marti,\nThank you for your order #296587. Unfortunately, due to unforeseen circumstances, your product shipment has been delayed. We expect your order to ship around mid November. We truly value you as a customer and apologize for any disappointment this may cause. We will be sure to keep you updated on any changes to the timing of your order shipment.\nThank you for being a part of the Wisteria family!""",
        "Actual": "The order is delayed due to unforeseen circumstances and will arrive in November",
        "Expected_Relationship": "ENTAILMENT"
    },
    {
        "Expected": """Dear Customer,\nWe are delighted to inform you that we have a new selection of products available for the holiday season. Check out our latest collection on the Wisteria website and enjoy exclusive discounts!""",
        "Actual": "The order was received and is being processed. Thank you for shopping with us.",
        "Expected_Relationship": "NEUTRAL"
    },
    {
        "Expected": """Hi Amy,\nThank you for reaching out to Wisteria, my name is Cassy and I am happy to assist you.\nI have checked on your order, and unfortunately due to unforeseen circumstances, your item is on back order at this time with the manufacturer, and is due to ship January 15, 2025.\nWe certainly apologize for this. Feel free to reply to this email at any time for updates, sometimes these dates can change.\nWe will provide a tracking link as soon as it is available.""",
        "Actual": """Hi Amy,\nYour order details are as follows:\nOrder number: #296496\nOrder Date: 10/7/2024\nItem Number: 118-111307\nItem Name: Ingalls Chest\nESD: The item is currently scheduled for delivery on January 15, 2025.\nWe will provide a tracking link as soon as it is available.\nIs there anything else I can assist you with?\nBest regards,\nSophia""",
        "Expected_Relationship": "NEUTRAL"
    },
    {
        "Expected": "We do not allow exchanges for sale items.",
        "Actual": "Sale items can be exchanged for store credit.",
        "Expected_Relationship": "CONTRADICTION"
    }
]



def gpt_call(GPT):
    gpt_config = {
        "4omini": {
            "OPENAI_API_KEY": "95058a9e99794e4689d179dd726e7eec",
            "OPENAI_DEPLOYMENT_NAME": "vassar-4o-mini",
            "OPENAI_EMBEDDING_MODEL_NAME": "vassar-text-ada002",
            "OPENAI_API_BASE": "https://vassar-openai.openai.azure.com/",
            "MODEL_NAME": "gpt-4o-mini",
            "OPENAI_API_TYPE": "azure",
            "OPENAI_API_VERSION": "2024-02-15-preview",
        }
    }

    config = gpt_config.get(GPT)
    if not config:
        print("Invalid GPT version specified")
        return None

    llm = AzureChatOpenAI(
        deployment_name=config["OPENAI_DEPLOYMENT_NAME"],
        model_name=config["MODEL_NAME"],
        azure_endpoint=config["OPENAI_API_BASE"],
        openai_api_type=config["OPENAI_API_TYPE"],
        openai_api_key=config["OPENAI_API_KEY"],
        openai_api_version=config["OPENAI_API_VERSION"],
        temperature=0.0
    )
    return llm


def analyze_nli_with_4omini(expected, actual):
    llm = gpt_call("4omini")
    if llm is None:
        return "Error: GPT model could not be initialized."
    prompt_template = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(Similarity.get("system_message")),
            HumanMessagePromptTemplate.from_template(Similarity.get("user_message")),
        ]
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=False)
    response = llm_chain.run({"expected": expected, "actual": actual})
    print("response::",response)
    return response


for example in examples:
    expected = example["Expected"]
    actual = example["Actual"]
    label_and_reason = analyze_nli_with_4omini(expected, actual)
    print(f"Expected Relationship: {example['Expected_Relationship']}")
    print(f"ChatGPT-4o-mini Relationship: {json.loads(label_and_reason).get("Sentiment","")}")
    print(f"ChatGPT-4o-mini reason: {json.loads(label_and_reason).get("explanation","")}")
    print("=" * 50)
