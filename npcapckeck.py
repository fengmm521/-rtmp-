import winreg
import subprocess
import time
import os 

def is_npcap_installed():
    possible_paths = [
        r"C:\Program Files\Npcap",
        r"C:\Program Files (x86)\Npcap"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return True
    return False

def is_npcap_in_registry():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Npcap"
        )
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False

def npcap_interface_exists():
    try:
        proc = subprocess.Popen(
            ["WiresharkPortable\\App\\Wireshark\\tshark.exe", "-D"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",  # 设置编码
            errors="ignore"   # 忽略非法字符
        )

        output_lines = []
        start_time = time.time()
        timeout = 5

        while True:
            line = proc.stdout.readline()
            if line == '' and proc.poll() is not None:
                break
            if line:
                output_lines.append(line.strip())
                if "NPF_" in line or "Npcap Loopback Adapter" in line:
                    proc.terminate()
                    return True
            if time.time() - start_time > timeout:
                proc.terminate()
                break

        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def list_interfaces():
    try:
        proc = subprocess.Popen(
            ["WiresharkPortable\\App\\Wireshark\\tshark.exe", "-D"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",  # 设置编码
            errors="ignore"   # 忽略非法字符
        )

        output_lines = []
        start_time = time.time()
        timeout = 5
        out = []
        while True:
            line = proc.stdout.readline()
            if line == '' and proc.poll() is not None:
                break
            if line:
                output_lines.append(line.strip())
                # if "NPF_" in line or "Npcap Loopback Adapter" in line:
                #     proc.terminate()
                #     return True
                out.append(line.strip())
            if time.time() - start_time > timeout:
                proc.terminate()
                break

        return out
    except Exception as e:
        print(f"Error: {e}")
        return []

def selectInterface():
    interfaces = list_interfaces()
    if interfaces:
        print("可用接口列表：")
        for i, interface in enumerate(interfaces):
            print(f"{interface}")
        choice = input("请选择一个接口（输入编号）：")
        try:
            choice = int(choice)
            if 1 <= choice <= len(interfaces):
                interface_name = interfaces[choice-1]
                print(f"您选择了接口：{interface_name}")
                return interface_name.split(' ')[1]
            else:
                print("无效的选择，请重新选择。")
                return selectInterface()
        except ValueError:
            print("无效的选择，请重新选择。")
            return selectInterface()
def isNpcapInInstalled():
    if is_npcap_installed():
        print("Npcap 已安装（通过文件夹检测）")
        return True
    elif npcap_interface_exists():
        print("Npcap 已安装（通过tshark检测）")
        return True
    elif is_npcap_in_registry():
        print("Npcap 已安装（通过注册表检测）")
        return True
    else:
        print("Npcap 未安装")
    return False

def main():
    if isNpcapInInstalled():
        devs = list_interfaces()
        for l in enumerate(devs):
            print(list(l)[1])
        interface_name = selectInterface()
        print(f"您选择了接口：{interface_name}")

if __name__ == "__main__":
    main()
