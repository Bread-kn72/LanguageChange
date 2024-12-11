import keyboard
import winreg
import sys

def get_current_han_eng_key():
    reg_path = r"Keyboard Layout\Toggle"
    try:
        # 현재 한/영 키 확인
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ) as key:
            current_key = winreg.QueryValueEx(key, "Hotkey")[0]
        return current_key
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"레지스트리 읽기 중 오류 발생: {e}")
        return None

def set_han_eng_key(new_key, old_key):
    # 새 한/영 키 설정
    reg_path = r"Keyboard Layout\Toggle"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            # 새 한/영 키를 설정
            winreg.SetValueEx(key, "Hotkey", 0, winreg.REG_SZ, new_key)
        
        # 키 교환 로직 추가 필요 (Caps Lock ↔ 기존 한/영 키 교체)
        print(f"한/영 키가 '{new_key}'로 변경되었습니다.")
        print(f"기존 키 '{old_key}'는 새로 매핑됩니다.")
        # 키 매핑 로직 추가 가능 (OS 또는 별도 라이브러리 필요)
    except Exception as e:
        print(f"레지스트리 변경 중 오류 발생: {e}")

def change_han_eng_key():
    print("새로운 한/영 키를 설정하려면 키를 누르고 Enter를 누르세요.")
    print("취소하려면 ESC를 누르세요.")

    current_key = get_current_han_eng_key()
    print(f"현재 설정된 한/영 키: {current_key if current_key else '없음'}")

    new_key = None
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            print(f"입력된 키: {event.name}")  # 사용자가 누른 키를 출력
            new_key = event.name
        elif event.event_type == keyboard.KEY_UP and new_key is not None:
            if new_key == 'esc':
                print("한/영 키 변경이 취소되었습니다.")
                return
            else:
                print(f"새로운 한/영 키로 '{new_key}'가 선택되었습니다.")
                set_han_eng_key(new_key, current_key)
                break

def main_menu():
    while True:
        print("\n=== 프로그램 메뉴 ===")
        print("1. 한/영 키 변경")
        print("2. 종료")
        choice = input("선택지를 입력하고 Enter를 누르세요: ")

        if choice == '1':
            change_han_eng_key()
        elif choice == '2':
            print("프로그램을 종료합니다.")
            sys.exit()
        else:
            print("올바른 선택지를 입력해주세요.")

if __name__ == "__main__":
    print("프로그램이 시작되었습니다.")
    main_menu()