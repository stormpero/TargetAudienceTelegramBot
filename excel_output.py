import xlwings as xw

excel_name = "Results.xlsx"

book = xw.Book(excel_name)
data_excel = book.sheets["Данные"]

current_cell = 5


def add_result_to_excel(array):
    global current_cell
    data_excel.range(f'A{current_cell}').options(index=False).value = array
    current_cell = current_cell + 1
