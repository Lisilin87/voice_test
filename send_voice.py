import asyncio
import base64
import json
import os
import random
import time
from datetime import datetime

import pandas as pd
import websockets
from pydub import AudioSegment

from voice_test.config_ini import *

SHOULD_FINALIZE = False
RESULT_LIST = []



async def send_no_voice(websocket,chunk_size,silence_duration = 1000):
    sample_rate = 16000
    num_samples = int(sample_rate * silence_duration / 1000)
    silence_pcm = bytes(num_samples * 2)  # 16bit PCM，每个样本 2 字节

    # 分块发送静音音频
    for i in range(0, len(silence_pcm), chunk_size):
        chunk = silence_pcm[i:i + chunk_size]
        await websocket.send(chunk)
        await asyncio.sleep(0.1)

async def send_audio(websocket,case_dict):
    AUDIO_FILES = [PRE_WAV_PATH,PRE_WAV_PATH,PRE_WAV_PATH, AUDIO_NAME_COL_PRE+case_dict[AUDIO_NAME_COL],PRE_WAV_PATH,PRE_WAV_PATH,PRE_WAV_PATH]
    # 检查所有文件是否存在
    for file in AUDIO_FILES:
        if not os.path.exists(file):
            print(f"错误：文件 {file} 不存在！")
            return

    # 加载并拼接音频
    combined_audio = AudioSegment.empty()
    for file in AUDIO_FILES:
        audio = AudioSegment.from_wav(file)
        # 统一格式：16kHz，单通道，16bit PCM
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        combined_audio += audio

    # 获取原始 PCM 数据
    pcm_data = combined_audio._data

    # 设置每次发送的数据块大小
    chunk_size = 4096
    # 分块发送音频数据
    for i in range(0, len(pcm_data), chunk_size):
        chunk = pcm_data[i:i + chunk_size]  # 提取当前数据块
        await websocket.send(chunk)  # 发送音频块
    print("音频发送完成")
    await asyncio.sleep(2)
    # await websocket.send(json.dumps({"type": "finalize"}))
    await send_no_voice(websocket, chunk_size, silence_duration=1000)
    print("静音发送完成")



async def receive_response(websocket, case_dict):
    audio = ""
    timeout = 30  # 设置超时时间为30秒
    start_time = time.time()
    audio_list = []
    # 接收服务器返回的响应
    while True:
        try:
            # 设置超时时间
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=timeout)
            except asyncio.TimeoutError:
                print("接收响应超时，主动退出")
                break

            data = json.loads(response)
            if "latency_update" == data["type"]:
                continue
            if "audio_chunk" == data["type"]:
                # 获取当前时间
                current_time = datetime.now()
                # 格式化为时_分_秒
                time_str = current_time.strftime("%H_%M_%S")
                # base64 解码
                audio_bytes = base64.b64decode(data['data']['audio'])
                audio_list.append(audio_bytes)
                print("返回音频流"+str(data)[0:300])
            else:
                print("收到服务器响应：", data)

            if "result" == data["type"]:
                print("用例完成")
                print(data)
                case_dict[RESPONSE_COL] = data['data']['response']
                case_dict[EMOTION_COL_1] = data['data']['emotion']
                case_dict[EMOTION_COL_2] = data['data']['llm_emotion']
                case_dict[SAVE_WAV_COL] = case_dict[CASE_SON_ID] + "_output.wav"
                save_excel([case_dict])
                print("最终结果-----", str(case_dict))
                audio = b''.join(audio_list)
                # 保存音频文件
                if audio:
                    try:
                        # 保存为 wav 文件
                        output_path = os.path.join(os.path.dirname(SAVE_WAV_PATH), case_dict[CASE_SON_ID] + "_output.wav")
                        with open(output_path, "wb") as f:
                            f.write(audio)
                        print(f"音频已保存至: {output_path}")
                        audio = b''
                    except Exception as e:
                        print("保存音频文件时出错:", e)
                return data

        except websockets.exceptions.ConnectionClosed:
            print("连接已关闭")
            break


async def action_voice_test(case_dict):
    # 客户端 ID
    client_id = "test_client"
    # WebSocket 服务器地址
    uri = f"ws://localhost:8765/ws/{client_id}"

    # 连接 WebSocket 服务器
    async with websockets.connect(uri) as websocket:
        # 创建并行任务：发送音频和接收响应
        send_task = asyncio.create_task(send_audio(websocket,case_dict))
        receive_task = asyncio.create_task(receive_response(websocket,case_dict))

        # 等待两个任务完成
        await send_task
        await receive_task
    return receive_task

def save_excel(output_list):
    """
    将数据追加保存到同一个 Excel 文件。
    文件名为 EXCEL_SAVE_NAME + "_实时保存.xlsx"，避免与原有输出混淆。
    """
    output_file = EXCEL_SAVE_NAME + ".xlsx"  # 固定文件名，所有结果存于此文件
    new_df = pd.DataFrame(output_list)

    # 如果文件已存在，则读取原有数据并合并
    if os.path.exists(output_file):
        existing_df = pd.read_excel(output_file, engine='openpyxl')
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    # 保存为 Excel 文件
    combined_df.to_excel(output_file, index=False, engine='openpyxl')


