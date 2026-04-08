import pyaudio
import wave

# 录音参数
FORMAT = pyaudio.paInt16  # 16位PCM格式
CHANNELS = 1              # 单声道
RATE = 16000              # 采样率 16kHz
CHUNK = 1024              # 每次读取的音频块大小
RECORD_SECONDS = 2        # 录音时长（秒）
OUTPUT_FILENAME = "output_recording.wav"  # 输出文件名

# 初始化 pyaudio
audio = pyaudio.PyAudio()

# 打开音频流
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("开始录音，请说话...")

# 存储音频数据
frames = []

# 录音循环
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录音结束。")

# 停止并关闭音频流
stream.stop_stream()
stream.close()
audio.terminate()

# 保存为 .wav 文件
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"音频已保存为：{OUTPUT_FILENAME}")