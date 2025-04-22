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
    
    cap = pyshark.LiveCapture(interface=interface_name, display_filter="", tshark_path=TSHARK_PATH)
    f = open('log.txt','w')
    fnds = open('found.txt','w')
    # for packet in cap.sniff_continuously(packet_count=100):  # 控制数量以便测试
    for packet in cap.sniff_continuously(packet_count=10000):  # 控制数量以便测试
        if 'TCP' in packet and packet.tcp.port == 1935:
            # if packet.tcp.port == 1935:
            raw = str(packet.rtmp)
            if "stream-" in raw and "auth_key" in raw:
                print("[+] 捕获到 RTMP 地址：")
                print(raw)
                break
            else:
                print(raw)
            f.write(str(packet))
        elif 'DNS' in packet:
            dns_layer = packet.dns
            # print(packet.dns._all_fields)
            # 判断是请求还是响应
            if dns_layer.qry_type == '0':  # 0: query
                print(f"[Query] {packet.ip.src} -> {dns_layer.qry_name}")

            elif dns_layer.qry_type == '1':  # 1: response
                print(f"[Response] {packet.ip.dst} <- {dns_layer.qry_name}")
                savestr = f"{packet.ip.dst} <- {dns_layer.qry_name}"
                # 打印 A/AAAA 记录中的 IP 地址
                if hasattr(dns_layer, 'a'):
                    print(f"  A Record: {dns_layer.a}")
                    savestr += f"  A Record: {dns_layer.a}" + "\n"
                    fnds.write(savestr)
                if hasattr(dns_layer, 'aaaa'):
                    print(f"  AAAA Record: {dns_layer.aaaa}")
                    savestr += f"  AAAA Record: {dns_layer.aaaa}" + "\n"
                    fnds.write(savestr)
                
        # else:
        #     print(packet)
    f.close()
    fnds.close()

if __name__ == "__main__":
    interface_name = ''
    if not is_npcap_installed():
        install_npcap()
    else:
        print('is insalled npcap')
        interface_name = npcapckeck.selectInterface()
    start_capture_and_extract_rtmp(interface_name)
