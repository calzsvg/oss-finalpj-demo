import cv2
from vidstream_grayscale.preprocessor import (vidgrayscaling,
                                              image_grayscale,
                                              folder_grayscale)


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
            display = vidgrayscaling(frame)
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

    #folder_grayscale("images")
