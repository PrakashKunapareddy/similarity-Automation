import json
import websockets
from excel_task import excel_query_fetch, write_to_excel

async def fetch_responses_from_websocket(sheet, excel_loc):
    link = "wss://uat.ce.vassardigital.ai/ws/chatbot/?customer_uuid=adade888-13b2-4bab-9455-73ed48d48833&application_uuid=9c3b5a57-4ce8-476d-8399-feaa76f36716"
    message_payload_template = {
        "message": "{\"id\":\"746f17a2-8631-409e-9133-9affe6e2a795\",\"csr_id\":null,\"source\":\"user\",\"message_marker\":\"LOGGED\",\"dimension_action_json\":{},\"message_text\":\"hi\",\"media_url\":[],\"parent_message_uuid\":null,\"created_at\":\"2024-11-18T11:07:36.509Z\"}"
    }
    questions = excel_query_fetch(sheet)
    updated_message_payloads = []
    actual_responses = []

    for item in questions:
        updated_payload = message_payload_template.copy()
        updated_message_payload_gen = updated_payload.get("message").replace("hi", item)
        updated_message_payload = {
            "message": updated_message_payload_gen
        }
        updated_message_payloads.append(updated_message_payload)

    try:
        async with websockets.connect(link) as websocket:
            for message in updated_message_payloads:
                print("Sending message:", message)
                await websocket.send(json.dumps(message))

                while True:
                    response = await websocket.recv()
                    actual_response_json = json.loads(response)
                    print(f"Received: {response}")

                    if actual_response_json.get("message") and actual_response_json["message"].get("message_text"):
                        actual_responses.append(actual_response_json["message"]["message_text"])
                        break

        write_to_excel(sheet, actual_responses, excel_loc)

    except Exception as e:
        print(f"An error occurred: {e}")
