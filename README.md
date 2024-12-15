# 마이크로파이썬 라즈베리 파이 피코 보안 자동 삭제 기능

해당 프로젝트는 **보안 강화**를 위해 USB 장치 연결 시 Pico 내부에 존재하는 파일들을 **자동으로 삭제**하는 기능을 제공합니다.

## 기능 개요

- **자동 삭제 트리거**: USB 케이블이 연결되면, Pico 내부 파일 시스템을 자동으로 초기화(삭제)합니다.
- **Fallback 처리**: USB 연결이 감지되지 않는 경우, 자동으로 `serve.py` 파일로 포워딩하여 다른 동작을 수행합니다.

## 사용 방법

1. **하드웨어 연결**:  
   Pico의 **Pin22**와 **USB D+ (TP3)** 단자를 쇼트(연결)합니다.  
   이를 통해 USB 연결 상태를 감지할 수 있습니다.

2. **코드 적용**:  
   해당 리포지토리에 있는 코드를 **main.py**로 복사 또는 저장합니다.  
   Pico를 리셋하거나 재부팅하면, USB 연결 시 자동 삭제 기능이 동작합니다.

3. **동작 확인**:  
   USB가 연결될 경우, Pico 내부의 파일 시스템이 자동으로 삭제됩니다.  
   USB가 연결되지 않으면 `serve.py` 파일이 실행되며 다른 동작(웹 서버 시작 등)을 수행할 수 있습니다.

## 주의사항

- **데이터 유실 경고**:  
  본 기능을 활성화하면 USB 연결 시 기존 내부 데이터가 **영구 삭제**됩니다.  
  중요 데이터는 외부 백업을 권장합니다.

- **하드웨어 변경 주의**:  
  Pin2와 USB D+를 단순 쇼트하는 것만으로 충분하며, 다른 핀이나 단자와의 잘못된 연결은 시스템 손상을 야기할 수 있습니다.
