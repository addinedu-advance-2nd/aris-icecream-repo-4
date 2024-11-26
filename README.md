# RoboPalz - 관리자 친화적 아이스크림 로봇
# 프로젝트 개요
## 프로젝트 소개
ufactory사의 xarm 기반의 다양한 편리 기능이 있는 아이스크림 로봇 시스템
## 팀 구성
|이강찬|김세현|김영배|신정수|안태규|황정민|
|-----|-----|---|----|-----|------|
|프로젝트 기획 <br> 로봇 구동 모션 개발|ROS통합 시스템 개발<br>통합 관리 노드 제작<br>로봇 제어 노드 제작<br>파트 별 연동|UI 기획 및 개발<br>게임 개발|YOLOv8커스텀 모델 학습<br>모니터링 영상 송신부 제작|ArUco Marker 생성 및 ID 부여<br>YOLO 데이터 학습|DB 설계 및 연동<br>게임 랭킹 시스템 개발<br>UI 디자인 수정|
## 기술 스택
|분야|기술|
|---|---|
|개발 환경|<img src="https://img.shields.io/badge/ROS2-22314E?style=for-the-badge&logo=ROS&logoColor=white"> <img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">
|GUI|<img src="https://img.shields.io/badge/pyqt5-41CD52?style=for-the-badge&logo=Qt&logoColor=white">|
|영상 처리|<img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"> <img src="https://img.shields.io/badge/YOLOv8-149EF2?style=for-the-badge&logoColor=white"> <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white">|
|데이터베이스|<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">|
# 프로젝트 설계
## 주요 기능
1. 키오스크 UI를 통한 아이스크림 주문
2. 이미지 인식을 이용한 아이스크림 감지, 아이스크림 종류, 위치 판별
3. 손 감지를 통한 로봇 정지
4. 연속적인 주문을 처리할 수 있는 주문 누적 기능
5. 회원 관리
6. 재고 관리 및 로봇 모니터링
7. 게임 및 랭킹 시스템
## 시스템 구성도
![시스템 구성도](https://github.com/user-attachments/assets/a689e312-f691-4c0f-a343-f4e9ca1d78fe)
## 프로토콜 정의서
![프로토콜 정의](https://github.com/user-attachments/assets/ac8b8cdf-5d82-41c8-b4b0-c17127ae24ec)
## 시나리오 
![시퀀스_다이어그램_주문 drawio](https://github.com/user-attachments/assets/42332830-d4d3-4116-a1c8-202eb78214e4)
# 프로젝트 구현
## 메인 페이지
![01_메인페이지](https://github.com/user-attachments/assets/4f1edf39-383d-4211-8e59-d00224c4c319)
## 주문 페이지
![03_주문하기2](https://github.com/user-attachments/assets/56a688a5-2109-4a72-bc60-b90ac56cf35b)
## 관리자 페이지
[![Video Label](http://img.youtube.com/vi/EaW7wQQOGlU/0.jpg)](https://youtu.be/EaW7wQQOGlU)
## 아이스크림 감지
[![Video Label](http://img.youtube.com/vi/H_7s5r2d2Qw/0.jpg)](https://youtu.be/H_7s5r2d2Qw)
## 손 감지 후 일시정지
[![Video Label](http://img.youtube.com/vi/60pVBx9gwTo/0.jpg)](https://youtu.be/60pVBx9gwTo)
## 데이터베이스 구성
![설명버전](https://github.com/user-attachments/assets/517668af-c82b-4948-a966-2e6b7b3ceaf8)
## ERD
![ROBOPALZ_ARIS_ERD](https://github.com/user-attachments/assets/0d83305e-8659-4b98-af35-61a23bf459b9)
## 전체 동작 (두개 주문 연속)
[![Video Label](http://img.youtube.com/vi/JECAqBjJ6oA/0.jpg)](https://youtu.be/JECAqBjJ6oA)
# 개발 기간
2024.10.30 ~ 2024.11.21 (약 3주)
