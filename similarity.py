import spacy
from datetime import datetime
from langchain.chains import LLMChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
import json

lang = spacy.load("en_core_web_md")

# file_path = ''
# workbook = openpyxl.load_workbook(file_path)
# sheet = workbook.active
# for row in range(2, sheet.max_row + 1):
#     if sheet[f'A{row}'].value is None:
#         break
#     Expected = sheet[f'C{row}'].value
Expected = "The product is available"

current_time1 = datetime.now()
formatted_time1 = current_time1.strftime("%H:%M:%S")
print("Before Prompt Input Time:", formatted_time1)

ProductAvailability = {
    "SYSTEM": """You are a helpful AI assistant for Wisteria, assisting customers with product availability inquiries. Based on the context provided, determine the availability status of the product in question. If the product is unavailable, include the expected restock date if applicable, and suggest alternative products if relevant.""",
    "CONTEXT": """
    CUSTOMER_QUERY:
    {customer_query}

    ADDITIONAL PRODUCT INFORMATION:
    {product_info}
    """,
    "DISPLAY": """Provide the response in the following JSON format:
    {{
      "availability_status": "[Availability status of the product]",
      "restock_date": "[Expected restock date if applicable]",
      "alternative_suggestions": "[Suggested alternatives if product is unavailable]",
      "customer_query": "[Original customer query]",
      "resp": "[Explanation for the response provided]"
    }}
    """,
    "REMEMBER": """Always provide the availability status first, followed by restock dates if relevant. If the product is unavailable, offer alternatives whenever possible. Answer clearly and directly."""
}


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

    OPENAI_API_KEY = config["OPENAI_API_KEY"]
    OPENAI_DEPLOYMENT_NAME = config["OPENAI_DEPLOYMENT_NAME"]
    OPENAI_EMBEDDING_MODEL_NAME = config["OPENAI_EMBEDDING_MODEL_NAME"]
    OPENAI_API_BASE = config["OPENAI_API_BASE"]
    MODEL_NAME = config["MODEL_NAME"]
    OPENAI_API_TYPE = config["OPENAI_API_TYPE"]
    OPENAI_API_VERSION = config["OPENAI_API_VERSION"]

    llm = AzureChatOpenAI(
        deployment_name=OPENAI_DEPLOYMENT_NAME,
        model_name=MODEL_NAME,
        azure_endpoint=OPENAI_API_BASE,
        openai_api_type=OPENAI_API_TYPE,
        openai_api_key=OPENAI_API_KEY,
        openai_api_version=OPENAI_API_VERSION,
        temperature=0.0
    )
    return llm


def ProdAvail(product_info, GPT):
    customer_query = "Is glass table Available"
    llm = gpt_call(GPT)
    prompt_template = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(ProductAvailability.get("SYSTEM")),
            HumanMessagePromptTemplate.from_template(ProductAvailability.get("CONTEXT")),
            SystemMessagePromptTemplate.from_template(ProductAvailability.get("DISPLAY")),
            SystemMessagePromptTemplate.from_template(ProductAvailability.get("REMEMBER"))
        ]
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=False)
    result = llm_chain.run({"customer_query": customer_query, "product_info": product_info})
    return json.loads(result)


product_info = {
    "availability_status": "In Stock",
    "restock_date": "Null",
    "alternative_suggestions": "NA",
    "customer_query": "Is glass table Available",
    "resp": ""
}

response = ProdAvail(product_info, GPT="4omini")
# print(type(response))
print(response)
current_time2 = datetime.now()
formatted_time2 = current_time2.strftime("%H:%M:%S")
print("After Prompt Response:", formatted_time2)

time_gap = current_time2 - current_time1
print(f"TimeGap: {time_gap}")


doc1 = lang(Expected)
doc2 = lang(response['resp'])

similarity = doc1.similarity(doc2)

print(f"Similarity between the responses: {similarity:.2f}")


