#pip3 install mysql-connector-python
import mysql.connector

# MySQL 서버에 연결
conn = mysql.connector.connect(
    host='192.168.0.123',      # 호스트 이름
    user='robopalz',       # MySQL 사용자 이름
    password='1234',   # MySQL 사용자 비밀번호
    database='ROBOPALZ',  # 연결할 데이터베이스 이름
    charset='utf8'
)


"""cursor = conn.cursor()

# 쿼리 실행 예시
sql_query = "SELECT * FROM user"
cursor.execute(sql_query)

# 쿼리 결과 가져오기
result = cursor.fetchall()

# 결과 출력
for row in result:
    print(row)

# 연결과 커서 닫기
cursor.close()
conn.close()


"""
