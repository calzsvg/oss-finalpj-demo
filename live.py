import cv2
from vidstream_grayscale.preprocessor import vidgrayscaling


def main():
    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        print("오류-웹캠")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("오류")
            break

        gray = vidgrayscaling(frame)

        cv2.imshow("GRAY TEST", gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

from vidstream_grayscale.preprocessor import image_grayscale
image_grayscale("sample.jpg") 
print("이미지 변환 성공")

from vidstream_grayscale.preprocessor import folder_grayscale

folder_grayscale("images")
