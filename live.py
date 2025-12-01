import cv2
from grayscale.preprocessor import (grayscale_frame, grayscale_image, grayscale_folder, resize_image, resize_folder, is_gray, remove_background, remove_background_img)


def main():
    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        print("웹캠에서 오류가 발생했습니다.")
        return
    
    is_gray = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("오류가 발생했습니다.")
            break

        if is_gray:
            display = grayscale_frame(frame)
        else:
            display = frame

        cv2.imshow("GRAY TEST", display)

        key = cv2.waitKey(1) & 0xff

        if key == ord('q'):
            break
        elif key == ord('c'):
            is_gray = not is_gray

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

    #image_grayscale("sample.jpg") 
    print("이미지 변환에 성공하였습니다!")

