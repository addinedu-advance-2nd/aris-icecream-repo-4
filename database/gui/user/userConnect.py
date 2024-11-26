#pip3 install mysql-connector-python
import mysql.connector
from database.connect.connectMysql import *
from datetime import datetime

# MySQL 서버에 연결
def checkLogin(param):    
    try:
        result = {}
        tmpResult=""    
        cursor = conn.cursor()
        id = param['id']
        pw = param['pw']

        #ID 확인
        mpResult = ""
        msg=""
        cursor = conn.cursor()
        sql = "SELECT userCode FROM USER WHERE id = '"+id+"' AND useYN = 'Y';"
        print(sql)
        cursor.execute(sql)        
        while (True):
            row = cursor.fetchone()
            if row == None:
                break;
            tmpResult = row[0]    
        conn.commit()
        cursor.close()
        print(tmpResult)

        #비밀번호 확인
        if(tmpResult!=""):    
            cursor = conn.cursor()
            sql = "SELECT  auth  FROM USER WHERE userCode =  %s AND pw = MD5(%s)"
            print(sql)
            cursor.execute(sql,(tmpResult, pw)) 
            
            result['userCode'] = tmpResult
            result['auth'] = cursor.fetchone()[0]

            conn.commit()
            cursor.close()
            if(len(result)>0):
                msg = "로그인에 성공하였습니다."
            else:
                msg ="비밀번호가 일치하지 않습니다."
        else:
            msg = "해당 ID는 존재하지 않습니다. 회원가입을 진행해주세요:)"

       
    except Exception as e:
        msg ="로그인에 실패하였습니다."
        print(e)       

    result['msg'] = msg
    return result


def insertSignUp(param):    
    try:
        result = {}
        tmpResult=""    
        cursor = conn.cursor()
        id = param[0]
        msg=""
        #ID 확인
        tmpResult = ""
        cursor = conn.cursor()
        sql = "SELECT userCode FROM USER WHERE id = '"+id+"' AND useYN = 'Y';"
        print(sql)
        cursor.execute(sql)         
        rows = cursor.fetchall()
        for row in rows:
            tmpResult = row[0]           
        conn.commit()
        cursor.close()
        print(tmpResult)

        #비밀번호 확인
        if(tmpResult==""):    
            cursor = conn.cursor()            
            sql = '''INSERT INTO `ROBOPALZ`.`USER`(`id`,`pw`,`name`,`mail`,`phone`,`joinDate`) VALUES (%s, MD5(%s), %s, %s, %s, now());'''
            print(sql)           
            cursor.execute(sql,(id, param[1], param[3], param[5], param[4]))  
            conn.commit()     
             
            if(cursor.rowcount>0):
                msg = "회원가입에 성공하였습니다."
            else :
                msg = "회원가입에 실패하였습니다. 정보를 다시 입력 부탁드립니다."

            cursor.close()    
        else:
            msg = "해당 ID는 이미 존재합니다. 다른 ID를 사용해주세요 :)"     
        
    except Exception as e:
        print(e)      

    result['msg'] = msg
    return result