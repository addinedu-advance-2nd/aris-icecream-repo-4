#pip3 install mysql-connector-python
from datetime import datetime
from urllib.parse import ParseResultBytes

import mysql.connector
from database.connect.connectMysql import *

# MySQL 서버에 연결
# 긴급 정지 시, 로그 저장
def insertEmergencyLog(logMsg):    
    try:
        result = {}                  
        cursor = conn.cursor()
        sql = '''INSERT INTO `ROBOPALZ`.`ARIS_EMERGENCY_LOG`(`log`,`logDate`)VALUES ( %s , now() );'''
        print(sql)           
        cursor.execute(sql,(logMsg))  
        conn.commit()   
        cursor.close()     
        
    except Exception as e:
        print(e)      

    return result


def selectEmergencyLog():
    result=[]
    
    cursor = conn.cursor()
    sql = " SELECT log, logDate " 
    sql +="   FROM ARIS_EMERGENCY_LOG"
    sql +="  ORDER BY logNum DESC"
    sql += " LIMIT 10" 

    print(sql)
    cursor.execute(sql)
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result.append(row[0], row[1])
    conn.commit()
    cursor.close()
    return result