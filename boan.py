import machine
import time
import uos
import ubinascii
import sys

# ADC 핀 설정 (예: GP26 = ADC0)
adc_pin = machine.ADC(26)

def read_voltage():
    # 16비트 범위(0 ~ 65535)로 읽기
    val = adc_pin.read_u16()
    voltage = (val / 65535.0) * 3.3
    return voltage

def is_usb_connected():
    # 전압을 읽어 특정 조건으로 USB 연결 판단
    v = read_voltage()
    # 3.3V 이상 혹은 3.18V 이하일 때 USB 연결로 가정
    # 필요하다면 로직 변경 가능
    if v >= 3.3 or v <= 3.18:
        return True
    return False

def create_log_file(log_path="/log.txt"):
    try:
        with open(log_path, "w") as f:
            # 시간 정보
            t = time.localtime()
            timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                t[0], t[1], t[2], t[3], t[4], t[5]
            )
            
            # 디바이스 ID(16진수 변환)
            device_id = None
            if hasattr(machine, 'unique_id'):
                raw_id = machine.unique_id()
                device_id = ubinascii.hexlify(raw_id).decode('utf-8').upper()
            
            # 시스템, 기기 정보 얻기
            uname_info = uos.uname()
            sys_name = uname_info.sysname
            node_name = uname_info.nodename
            release = uname_info.release
            version = uname_info.version
            machine_info = uname_info.machine
            
            platform_info = sys.platform
            
            # IP 정보(예: 실제 환경에 맞게 수정)
            ip_info = ("192.168.0.10", "255.255.255.0", "192.168.0.1", "8.8.8.8")
            
            f.write("=== USB Connection Log ===\n")
            f.write("Time: {}\n".format(timestamp))
            if device_id:
                f.write("Device ID: {}\n".format(device_id))
            f.write("System Name: {}\n".format(sys_name))
            f.write("Node Name: {}\n".format(node_name))
            f.write("Release: {}\n".format(release))
            f.write("Version: {}\n".format(version))
            f.write("Machine Info: {}\n".format(machine_info))
            f.write("Platform: {}\n".format(platform_info))
            f.write("IP Info: {}\n".format(ip_info))
            f.write("USB connected and preparing to delete files.\n")
    except Exception as e:
        print("Error creating log file:", e)

def delete_files(path, exclude_file="log.txt"):
    try:
        for entry in uos.ilistdir(path):
            entry_name = entry[0]
            entry_type = entry[1]
            full_path = f"{path}/{entry_name}"
            
            if entry_name == exclude_file:
                continue

            if entry_type == 0x4000:  # Directory
                try:
                    delete_files(full_path, exclude_file)
                    uos.rmdir(full_path)
                except Exception as e:
                    print(f"Error deleting directory {entry_name}: {e}")
            elif entry_type == 0x8000:  # File
                try:
                    uos.remove(full_path)
                except Exception as e:
                    print(f"Error deleting file {entry_name}: {e}")
    except Exception as e:
        # 디렉토리에 파일이 없을 경우 등의 예외는 무시
        pass

# 부팅 후 ADC 안정화를 위해 대기(필요 시)
time.sleep(1)

while True:
    v = read_voltage()
    print("Measured Voltage:", v)

    if is_usb_connected():
        print("USB connected. Creating log and deleting files...")
        create_log_file("/log.txt")
        delete_files("/", exclude_file="log.txt")
        machine.reset()
    else:
        print("USB not connected.")
        # USB가 연결되지 않은 경우 serve.py 실행 시도
        try:
            import serve
            serve.main()  # serve.py 내부 구현에 맞게 함수명 또는 로직 변경 필요
        except Exception as e:
            print(f"Error running serve.py: {e}")
    
    time.sleep(1)
