import asyncio
import websockets
import json


async def send_text_message():
    client_id = "test_client"
    uri = f"ws://localhost:8765/ws/{client_id}"

    async with websockets.connect(uri) as websocket:


        # 发送文本消息
        message = {
            "type": "text",
            "text": "你好，今天天气怎么样？"
        }
        await websocket.send(json.dumps(message))
        print("已发送文本消息")

        # 接收服务器返回的消息
        while True:
            try:
                response = await websocket.recv()
                print("收到服务器消息:", response)
            except websockets.exceptions.ConnectionClosed:
                print("连接已关闭")
                break


# 运行客户端
asyncio.run(send_text_message())