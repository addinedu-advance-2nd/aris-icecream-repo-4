import cv2
import cv2.aruco as aruco

# 웹캠 설정
cap = cv2.VideoCapture(4)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ArUco 딕셔너리 정의
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters()
parameters.adaptiveThreshConstant = 3  # 기본값을 조금 낮춤
parameters.minMarkerPerimeterRate = 0.1
parameters.maxMarkerPerimeterRate = 10.0
parameters.polygonalApproxAccuracyRate = 0.03
parameters.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX  # 서브픽셀 정밀도

flavorDict = {0:'strawberry', 1:'vanilla', 2:'chocolate', 3:'mintchoco',4:'apple',5:'grape',6:'grape'}

while True:
    # 프레임 캡처
    ret, frame = cap.read()
    if not ret:
        break
    
    # ArUco 마커 탐지
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    # 마커를 감지한 경우
    if ids is not None:
        print("Detected marker IDs:", ids)  # 콘솔에 감지된 ID 출력
        # 마커 그리기
        aruco.drawDetectedMarkers(frame, corners, ids)
        
        # 마커 ID 텍스트 표시
        for i in range(len(ids)):
            c = corners[i][0]
            x, y = int(c[:, 0].mean()), int(c[:, 1].mean())
            cv2.putText(frame, f"ID: {flavorDict[ids[i][0]]}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        print("No markers detected")  # 마커가 감지되지 않는 경우
        
    # 화면에 표시
    cv2.imshow('ArUco Marker Detection', frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 정리
cap.release()
cv2.destroyAllWindows()
