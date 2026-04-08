from aw.com.excel import Excel

def read_excel_rows(file_name, sheet_name, start_row, end_row=None):
    """
    读取 Excel 中指定 sheet 的指定行范围，并将每一行数据存入一个字典列表中。

    参数:
        file_name (str): Excel 文件名
        sheet_name (str): Sheet 名称
        start_row (int): 起始行号（从1开始）
        end_row (int or None): 结束行号（包含该行），如果为 None，则读取到空行为止

    返回:
        list: 二维列表，每一行是一个字典，键为列名，值为对应单元格内容
    """
    excel = Excel(file_name)
    excel.get_sheet(sheet_name)

    # 获取第一行作为列名
    header_row = excel.get_row_values(1)
    if not header_row:
        return []

    result = []
    current_row = start_row

    while True:
        row_data = excel.get_row_values(current_row)

        # 如果当前行全为空，或者 end_row 不为 None 且 current_row 超过 end_row，停止读取
        if all(cell == "" for cell in row_data):
            break
        if end_row is not None and current_row > end_row:
            break

        # 将当前行转换为字典
        row_dict = {header: value for header, value in zip(header_row, row_data)}
        result.append(row_dict)
        current_row += 1

    return result     