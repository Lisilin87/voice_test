from read_case import *
from config_ini import *
from voice_test.send_voice import *

# 读取用例表格
case_dict_in_list = read_excel_rows(FILE_NAME, SHEET_NAME, START_ROW, end_row=None)
# 遍历
for case_dict in case_dict_in_list:
    print(case_dict)
    # 启动客户端
    result = asyncio.run(action_voice_test(case_dict))


