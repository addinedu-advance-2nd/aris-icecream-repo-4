#pip3 install mysql-connector-python
from datetime import datetime
from urllib.parse import ParseResultBytes

import mysql.connector
from database.connect.connectMysql import *

# MySQL 서버에 연결
# 전체 게임 랭킹 가져오기
def selectTotalRank(rank):
    result=[]
    
    cursor = conn.cursor()
    sql = " SELECT R.userCode " 
    sql +="   , (SELECT id FROM USER U WHERE U.userCode = R.userCode ) AS userId "
    sql +="   , (SELECT gameName FROM GAME G WHERE G.gameCode = R.gameCode) AS gameName"
    sql += " ,  R.gameCode" 
    sql += " , SUM(score) AS TOTAL_SCORE  " 
    sql += " FROM GAME_PLAY_RANK R   " 
    sql += " GROUP BY  userCode " 
    sql += " ORDER BY TOTAL_SCORE DESC  " 
    sql += "  LIMIT "+rank+";" 

   
    print(sql)
    cursor.execute(sql)
    """
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result.append(row)
    """
    result  = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result



# 게임별 랭킹 가져오기
def selectGameByRank(gameCode, rank):
    result=[]
    
    cursor = conn.cursor()
    sql = " SELECT R.userCode " 
    sql +="   , (SELECT id FROM USER U WHERE U.userCode = R.userCode ) AS userId "
    sql +="   , (SELECT gameName FROM GAME G WHERE G.gameCode = R.gameCode) AS gameName"
    sql += " ,  R.gameCode" 
    sql += " , SUM(score) AS TOTAL_SCORE  " 
    sql += " FROM GAME_PLAY_RANK R   " 
    sql += " WHERE R.gameCode  = "+gameCode+"" 
    sql += " GROUP BY  userCode " 
    sql += " ORDER BY TOTAL_SCORE DESC  " 
    sql += "  LIMIT "+rank+"" 

   
    print(sql)
    cursor.execute(sql)
    result  = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result


#게임 기록 저장하기
def insertGamePlayInfo(gameCode, score, userCode):    
    try:
        result = {}                  
        cursor = conn.cursor()
        sql = '''INSERT INTO `ROBOPALZ`.`GAME_PLAY_RANK`(`userCode`,`gameCode`,`score`,`useYN`,`playDate`)VALUES(%s,%s,%s,'Y',NOW());'''
        print(sql)           
        cursor.execute(sql,(userCode, gameCode, score))  
        conn.commit()   
        cursor.close()    
 
        
    except Exception as e:
        print(e)      

    return result




#게임(게임명, 게임코드) 마스터 딕셔너리 가져오기
def selectGameNameCodeDict():
    result={}
    cursor = conn.cursor()
    sql = "SELECT gameName, gameCode FROM GAME WHERE useYN = 'Y'"
    print(sql)
    cursor.execute(sql)
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result[row[0]] = row[1]
    conn.commit()
    cursor.close()
    return result


#게임(게임코드, 게임코드 ) 마스터 딕셔너리 가져오기
def selectGameNameCodeDict():
    result={}
    cursor = conn.cursor()
    sql = "SELECT gameCode , gameName FROM GAME WHERE useYN = 'Y'"
    print(sql)
    cursor.execute(sql)
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result[row[0]] = row[1]
    conn.commit()
    cursor.close()
    return result