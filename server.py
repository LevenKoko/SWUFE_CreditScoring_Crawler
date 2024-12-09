import subprocess
import time
import os

def run_streamlit():
    # 使用subprocess.Popen启动Streamlit进程
    process1 = subprocess.Popen(['streamlit', 'run', 'web_new.py', '--server.port', '9001'])
    process2 = subprocess.Popen(['streamlit', 'run', 'web_high.py', '--server.port', '9002'])
    print("Streamlit is running...")

    try:
        # 等待30秒
        time.sleep(30)
    except KeyboardInterrupt:
        # 如果在20秒内按下Ctrl+C，则结束进程
        print("Streamlit is interrupted by user.")
        process1.kill()
        process2.kill()
        return

    # 20秒后结束Streamlit进程
    process1.terminate()
    process2.terminate()
    print("Streamlit process terminated.")

    return_code = process1.wait()
    print(f"Streamlit exited with code {return_code}")

# 无限循环，每隔20秒执行一次
while True:
    run_streamlit()
    # 等待2秒以避免日志输出太快
    time.sleep(2)