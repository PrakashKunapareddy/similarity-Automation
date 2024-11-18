import json

import openpyxl
from ChatGPT4omini import analyze_with_GPT_4oMINI

excel_loc = "/home/saiprakesh/Documents/NU-web-socket_response-comparison/similarity-Automation/response_comparison.xlsx"
workbook = openpyxl.load_workbook(excel_loc)
sheet = workbook.active


def excel_query_fetch():
    questions = []
    for row in range(2, sheet.max_row + 1):
        if sheet[f'A{row}'].value is None:
            break
        questions.append(sheet[f'B{row}'].value)
    return questions


def write_to_excel(response):
    for row in range(2, sheet.max_row + 1):
        if sheet[f'A{row}'].value is None:
            break
        for item in response:
            if "SOURCES" in item:
                actual_response, _, _ = item.partition("SOURCES")
            else:
                actual_response = item
            sheet[f'D{row}'] = actual_response
    workbook.save(excel_loc)
    print(f"Updated Response in {excel_loc}")


def similarity_check():
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
    print(f"Updated Response in {excel_loc}")


similarity_check()