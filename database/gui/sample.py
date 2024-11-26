#pip3 install mysql-connector-python
import mysql.connector

from database.connect.connectMysql import *



# MySQL 서버에 연결
def selectUser():
    # 커서 생성
    cursor = conn.cursor()
    # 쿼리 실행 예시
    sql_query = "SELECT * FROM USER"
    cursor.execute(sql_query)

    # 쿼리 결과 가져오기
    result = cursor.fetchall()

    # 결과 출력
    for row in result:
        print(row)

    # 연결과 커서 닫기
    cursor.close()
    conn.close()

