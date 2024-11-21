import openpyxl

def excel_query_fetch(sheet):
    questions = []
    for row in range(2, sheet.max_row + 1):
        if sheet[f'A{row}'].value is None:
            break
        questions.append(sheet[f'B{row}'].value)
    return questions

def write_to_excel(sheet, responses, excel_loc):
    workbook = openpyxl.load_workbook(excel_loc)
    for row, response in enumerate(responses, start=2):
        if sheet[f'A{row}'].value is None:
            break
        if "SOURCES" in response:
            actual_response, _, _ = response.partition("SOURCES")
        else:
            actual_response = response
        sheet[f'D{row}'] = actual_response
    workbook.save(excel_loc)

