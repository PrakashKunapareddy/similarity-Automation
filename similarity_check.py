import asyncio
import json
import openpyxl
from ChatGPT4omini import analyze_with_GPT_4oMINI
from response_fetch_web_socket import fetch_responses_from_websocket

def analyze_responses(sheet, excel_loc):
    for row in range(2, sheet.max_row + 1):
        if sheet[f'A{row}'].value is None:
            break
        expected = sheet[f'C{row}'].value
        actual = sheet[f'D{row}'].value
        label_and_reason = analyze_with_GPT_4oMINI(expected, actual)
        sheet[f'E{row}'] = json.loads(label_and_reason).get("Sentiment", "")
        sheet[f'F{row}'] = json.loads(label_and_reason).get("Similarity_Score", "")
        sheet[f'G{row}'] = json.loads(label_and_reason).get("explanation", "")
    workbook.save(excel_loc)

def similarity_check(excel_loc):
    global workbook
    workbook = openpyxl.load_workbook(excel_loc)
    sheet = workbook.active
    asyncio.run(fetch_responses_from_websocket(sheet, excel_loc))
    analyze_responses(sheet, excel_loc)
    print(f"Updated Analysis Results in {excel_loc}")


similarity_check("/home/saiprakesh/Documents/NU-web-socket_response-comparison/similarity-Automation/response_comparison.xlsx")




