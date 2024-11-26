#pip3 install mysql-connector-python
from datetime import datetime
import mysql.connector
from database.connect.connectMysql import *

# MySQL 서버에 연결


# 아이스크림(마스터) 리스트 가져오기
def selectIceCreamList():
    result=[]
    cursor = conn.cursor()
    sql = "SELECT iceName FROM ICECREAM WHERE useYN = 'Y'"
    print(sql)
    cursor.execute(sql)
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result.append(row[0])
    conn.commit()
    cursor.close()
    return result




def insertInventory(param):
    grpkey = getInsertInventoryGroupKey()

    
    print(param['ice'])
    print(param['topping'])
    
    iceDict = param['ice']
    iceKeysList = list(iceDict.keys())
    toppingList = list(param['topping'])
    
    """ 아이스크림 SET """
    cursor = conn.cursor()            
    sql = '''INSERT INTO `ROBOPALZ`.`INVENTORY`(`inventoryGroupKey`,`iceCode`,`iceCount`,`inventoryDate`) VALUES (%s, %s, %s, now());'''
    print(sql)           
    val = []
    for i in iceKeysList:
        val.append((grpkey, i, iceDict[i]))   

    cursor.executemany(sql,val)  
    conn.commit() 
    cursor.close()   


    """ 토핑 SET """
    cursor = conn.cursor()            
    sql = '''INSERT INTO `ROBOPALZ`.`INVENTORY`(`inventoryGroupKey`,`toppingCode`,`inventoryDate`) VALUES (%s, %s, now());'''
    print(sql)           
    val = []
    for t in toppingList:
        val.append((grpkey, t))
   
    cursor.executemany(sql,val)  
    conn.commit() 
    cursor.close()    
        
    

# 아이스크림(마스터) 리스트 가져오기
def selectIceCreamList():
    result=[]
    cursor = conn.cursor()
    sql = "SELECT iceName FROM ICECREAM WHERE useYN = 'Y'"
    print(sql)
    cursor.execute(sql)
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result.append(row[0])
    conn.commit()
    cursor.close()
    return result




# 아이스크림(마스터) 딕셔너리 가져오기
def selectIceCreamDict():
    result={}
    cursor = conn.cursor()
    sql = "SELECT iceName, iceCode FROM ICECREAM WHERE useYN = 'Y'"
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


# 토핑(마스터) 리스트 가져오기
def selectToppingList():
    result=[]
    cursor = conn.cursor()
    sql = "SELECT toppingName FROM TOPPING WHERE useYN = 'Y'"
    print(sql)
    cursor.execute(sql)
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result.append(row[0])
    conn.commit()
    cursor.close()
    return result


 #토핑(마스터) 딕셔너리 가져오기
def selectToppingDict():
    result={}
    cursor = conn.cursor()
    sql = "SELECT toppingName, toppingCode FROM TOPPING WHERE useYN = 'Y'"
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

 

# 당일 재고 관리 - 아이스크림 리스트 
def selectInventoryIceList():
    result=[]
    currentDate = datetime.now().strftime('%Y-%m-%d')
    tmpResult = getInventoryGroupKeyDate()


    cursor = conn.cursor()
    sql = " SELECT ICE.iceCode, ICE.IceName, IFNULL(INV.iceCount,0) AS iceCnt, IFNULL(S.salesCnt,0) AS salesCnt,  (IFNULL(INV.iceCount,0)-IFNULL(S.salesCnt,0))AS inventoryCnt , date_format(INV.inventoryDate, '%Y-%m-%d') AS setDate" 
    sql +="   FROM INVENTORY INV "
    sql +="   LEFT OUTER JOIN ICECREAM ICE ON ICE.useYN = 'Y' AND INV.iceCode = ICE.iceCode "
    #sql +="   LEFT JOIN (SELECT iceCode , COUNT(*) AS salesCnt FROM SALES WHERE salesDate BETWEEN '"+currentDate+" 00:00:00' AND '"+currentDate+" 23:59:59' GROUP BY iceCode) S ON INV.iceCode = S.iceCode "
    sql +="   LEFT JOIN (SELECT iceCode , COUNT(*) AS salesCnt FROM SALES WHERE salesDate > '"+str(tmpResult[1])+"' GROUP BY iceCode) S ON INV.iceCode = S.iceCode "
    sql +="  WHERE (INV.iceCode IS NOT NULL AND INV.iceCode != '') AND INV.inventoryGroupKey = "+str(tmpResult[0])
    print(sql)
    cursor.execute(sql)
    result  = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result


# 당일 재고 관리 - 토핑 리스트 
def selectInventoryToppingList():
    result=[]
    currentDate = datetime.now().strftime('%Y-%m-%d')
    tmpResult = getInventoryGroupKeyDate()


    cursor = conn.cursor()
    sql = " SELECT T.toppingCode, T.toppingName, date_format(INV.inventoryDate, '%Y-%m-%d') AS setDate" 
    sql +="   FROM INVENTORY INV "
    sql +="   LEFT OUTER JOIN TOPPING T ON T.useYN = 'Y' AND INV.toppingCode = T.toppingCode "
    sql +="   WHERE ( INV.toppingCode IS NOT NULL AND INV.toppingCode != '' )  AND INV.inventoryGroupKey = "+str(tmpResult[0]) 
   
    print(sql)
    cursor.execute(sql)
    result  = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result




def getInventoryGroupKeyDate():
    
    cursor = conn.cursor()
    sql = " SELECT inventoryGroupKey, inventoryDate , date_format(inventoryDate, '%Y-%m-%d')"
    sql +="   FROM INVENTORY                   "    
    sql +="  ORDER BY inventoryGroupKey DESC LIMIT 1"

    print(sql)
    cursor.execute(sql)
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result = (row[0], row[1], row[2])
    conn.commit()
    cursor.close()
    return result

def getInsertInventoryGroupKey():
    result=""
    cursor = conn.cursor()
    sql = " SELECT IFNULL(inventoryGroupKey,0)+1"
    sql +="   FROM INVENTORY                   "
    sql +="  GROUP BY inventoryGroupKey         "
    sql +="  ORDER BY inventoryGroupKey DESC LIMIT 1"

    print(sql)
    cursor.execute(sql)
    while (True):
        row = cursor.fetchone()
        if row == None:
            break;
        result = row[0]
    conn.commit()
    cursor.close()
    return result



#from database.gui.inventory.inventoryConnect import insertInventory
#invertoryInfo = {}
#invertoryInfo['ice'] = "'{0}','{1}','{2}','{3}','{4}','{5}'".format(selected_menu,0,selected_menu,10,selected_menu,8)
#invertoryInfo['topping'] = "4,5,6"
#insertInventory(invertoryInfo)
