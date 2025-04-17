import os
import subprocess
import pyshark
import shutil
import npcapckeck

NPCAP_PATH = "npcap_installer.exe"
TSHARK_PATH = os.path.abspath("WiresharkPortable\\App\\Wireshark\\tshark.exe")

def is_npcap_installed():
    return npcapckeck.isNpcapInInstalled()

def install_npcap():
    print("[*] 安装 Npcap 中...")
    subprocess.run([NPCAP_PATH, "/S"], check=True)
    print("[+] Npcap 安装完成。")

def start_capture_and_extract_rtmp(interface_name = 'Wi-Fi'):
    print("[*] 开始抓包，请开始直播软件...")
    
    cap = pyshark.LiveCapture(interface=interface_name, display_filter="rtmp", tshark_path=TSHARK_PATH)
    
    for packet in cap.sniff_continuously(packet_count=50):  # 控制数量以便测试
        try:
            if 'RTMP' in packet:
                raw = str(packet.rtmp)
                if "stream-" in raw and "auth_key" in raw:
                    print("[+] 捕获到 RTMP 地址：")
                    print(raw)
                    break
        except Exception:
            continue

if __name__ == "__main__":
    interface_name = ''
    if not is_npcap_installed():
        install_npcap()
    else:
        print('is insalled npcap')
        interface_name = npcapckeck.selectInterface()
    start_capture_and_extract_rtmp(interface_name)
