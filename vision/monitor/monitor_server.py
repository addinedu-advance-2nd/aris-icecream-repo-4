# pip install flask

from flask import Flask, render_template, Response
from time import sleep
import cv2
import time

app = Flask(__name__)
capture = cv2.VideoCapture(0) 
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 320
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 240


def GenerateFrames():
    while True:
        sleep(0.05)  # 프레임 생성 간격을 잠시 지연 (fps 낮추기)
        ref, frame = capture.read()  
        if not ref: 
            break
        else:
            ref, buffer = cv2.imencode('.jpg', frame)  # JPEG 형식으로 이미지를 인코딩
            frame = buffer.tobytes()  # 인코딩된 이미지를 바이트 스트림으로 변환
            # multipart/x-mixed-replace 포맷으로 비디오 프레임을 클라이언트에게 반환
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def Index():
    return render_template('index.html')  # index.html 파일을 렌더링하여 반환


@app.route('/stream')
def Stream():
    # GenerateFrames 함수를 통해 비디오 프레임을 클라이언트에게 실시간으로 반환
    return Response(GenerateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    # 서버의 IP 번호와 포트 번호를 지정하여 Flask 앱을 실행
    app.run(host="192.168.0.8", port="5757")
