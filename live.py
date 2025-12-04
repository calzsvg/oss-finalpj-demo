import os
os.environ['MPL_LOG_LEVEL'] = 'CRITICAL'

import cv2
import sys

try:
    from grayscale.preprocessor import (
        grayscale_frame, grayscale_image, grayscale_folder, 
        resize_image, resize_folder, is_gray, 
        remove_background, remove_background_img
    )
except ImportError:
    print("오류: grayscale 패키지나 preprocessor.py를 찾을 수 없습니다.")
    sys.exit(1)

def run_webcam_demo():
    print("웹캠 초기화 중...")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("웹캠을 열 수 없습니다.")
            return

    mode_gray = False
    mode_bg_remove = False

    print("--- 조작 방법 ---")
    print("[Q] : 종료 및 메뉴 복귀")
    print("[G] : 흑백 모드 토글 (ON/OFF)")
    print("[B] : 배경 제거 모드 토글 (ON/OFF)")
    print("-----------------")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        if mode_bg_remove:
            frame = remove_background(frame)

        if mode_gray:
            frame = grayscale_frame(frame)

        status_text = f"Mode: {'GRAY' if mode_gray else 'COLOR'} | BG: {'REMOVE' if mode_bg_remove else 'ORIGINAL'}"
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("OSS Final Project Demo", frame)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
        elif key == ord('g'):
            mode_gray = not mode_gray
            print(f"흑백 모드: {mode_gray}")
        elif key == ord('b'):
            mode_bg_remove = not mode_bg_remove
            print(f"배경 제거: {mode_bg_remove}")

    cap.release()
    cv2.destroyAllWindows()
    print("웹캠 데모를 종료합니다.")


def run_file_tool():
    while True:
        print("1. 이미지 한 장 -> 흑백 변환")
        print("2. 이미지 한 장 -> 배경 제거")
        print("3. 이미지 한 장 -> 리사이즈 (크기 조절)")
        print("4. 이미지/폴더 -> 흑백/컬러 판별 (is_gray)")
        print("5. 폴더 전체 -> 흑백 변환")
        print("6. 폴더 전체 -> 리사이즈")
        print("0. 메인 메뉴로 돌아가기")
        
        choice = input("기능 선택: ").strip()

        if choice == '0':
            break

        path = input("파일 또는 폴더 경로를 입력하세요: ").strip().strip("'").strip('"')
        
        try:
            if choice == '1':
                grayscale_image(path)
                print(f"변환 완료! (원본 경로에 _gray 파일 생성됨)")

            elif choice == '2':
                print("배경 제거 처리 중... (시간이 조금 걸릴 수 있습니다)")
                result = remove_background_img(path)
                
                file_root, file_ext = os.path.splitext(path)
                output_path = f"{file_root}_bgrm{file_ext}"
                cv2.imwrite(output_path, result)
                print(f"저장 완료: {output_path}")

            elif choice == '3':
                w = int(input("목표 너비(px): "))
                h = int(input("목표 높이(px): "))
                resize_image(path, w, h)
                print("리사이즈 완료")
            elif choice == '4':
                is_gray(path)

            elif choice == '5':
                grayscale_folder(path)

            elif choice == '6':
                w = int(input("목표 너비(px): "))
                h = int(input("목표 높이(px): "))
                resize_folder(path, w, h)
            
            else:
                print("잘못된 선택입니다.")

        except Exception as e:
            print(f"오류 발생: {e}")
        
        input("\n enter를 누르면 메뉴로 돌아갑니다 ")


def main():
    while True:
        print("\n==============================")
        print("   OSS Final Project Demo")
        print("==============================")
        print("1. 웹캠 라이브 데모 (Live)")
        print("2. 파일 변환 도구 (File Tools)")
        print("q. 프로그램 종료")
        print("==============================")
        
        selection = input("선택하세요: ").strip().lower()

        if selection == '1':
            run_webcam_demo()
        elif selection == '2':
            run_file_tool()
        elif selection == 'q':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()