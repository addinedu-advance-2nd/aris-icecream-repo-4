#pip3 install mysql-connector-python
from datetime import datetime
from urllib.parse import ParseResultBytes

import mysql.connector
from database.connect.connectMysql import *

# MySQL 서버에 연결
# (재고설정) 아이스크림 종류 가져 오기 - 품절 제외
def selectSaleIceCream():
    result=[]
    tmpResult = getInventoryGroupKeyDate()

    cursor = conn.cursor()
    sql = " SELECT ICE.IceName " 
    sql +="   FROM INVENTORY INV "
    sql +="   LEFT OUTER JOIN ICECREAM ICE ON ICE.useYN = 'Y' AND INV.iceCode = ICE.iceCode "
    sql +="   LEFT JOIN (SELECT iceCode , COUNT(*) AS salesCnt FROM SALES WHERE salesDate > '"+str(tmpResult[1])+"' GROUP BY iceCode) S ON INV.iceCode = S.iceCode "
    sql +="  WHERE (INV.iceCode IS NOT NULL AND INV.iceCode != '') AND INV.inventoryGroupKey = "+str(tmpResult[0])
    sql +="    AND (IFNULL(INV.iceCount,0)-IFNULL(S.salesCnt,0)) > 0 "
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


# (재고설정) 토핑 종류 가져 오기
def selectSaleTopping():  
    result=[]
    tmpResult = getInventoryGroupKeyDate()

    cursor = conn.cursor()
    sql = " SELECT T.toppingName" 
    sql +="   FROM INVENTORY INV "
    sql +="   LEFT OUTER JOIN TOPPING T ON T.useYN = 'Y' AND INV.toppingCode = T.toppingCode "
    sql +="   WHERE ( INV.toppingCode IS NOT NULL AND INV.toppingCode != '' )  AND INV.inventoryGroupKey = "+str(tmpResult[0])
   
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