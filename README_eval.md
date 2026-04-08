# voice_test 直接运行说明

现在这个目录已经补齐了可直接跑评测需要的基础文件：

- `eval_cases.csv`：测试用例表
- `voice_input_file/`：输入音频目录
- `output_recording.wav`：前后静音样本
- `run_eval.py` / `run_eval.bat`：直接启动评测

## 运行前

1. 先启动 `testChatBot/vedio` 的 WebSocket 服务
2. 在仓库根目录安装依赖：

```powershell
pip install websockets
pip install pandas openpyxl
```

如果你只用 `csv` 用例，可以不装 `openpyxl`；但当前结果保存和后续扩展，装上更稳。

## 直接运行

```powershell
cd C:\Users\silin\Desktop\audio\voice_test
python run_eval.py
```

或者双击：

```bat
run_eval.bat
```

## 你现在放新音频时怎么做

1. 把 `.wav` 文件放到 `voice_input_file/`
2. 在 `eval_cases.csv` 新增一行，填写：
   - `用例子编号`
   - `音频文件路径`
3. 重新执行 `python run_eval.py`
