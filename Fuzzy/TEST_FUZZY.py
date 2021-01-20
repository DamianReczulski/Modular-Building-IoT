import FUZZY
import time
import mysql.connector
from mysql.connector import Error

def test_fuzzy(fuzzy, fuzzy1):

    while 1:
        connection = mysql.connector.connect(host='mysql.cba.pl',
                                             database='cargoalgps',
                                             user='dbmaster',
                                             password='Admin123')
        cursor = connection.cursor()
        cursor.execute('select id from device where _auto = 1')
        records = cursor.fetchall()
        x = []
        for row in records:
            x.append(row[0])
        print(x)
        if x.__contains__(101):
            cursor.execute('SELECT _data AS data FROM devicedata WHERE device_id = 71 ORDER BY _date desc LIMIT 1')
            records = cursor.fetchall()
            for row in records:
                feedback = int(float(row[0]))
            fuzzy.update(feedback)
            output = fuzzy.output
            if output > 255:
                output = 255
            cursor.execute('UPDATE devicesettings SET value =' + str(int(output)) + ' WHERE device_id=101')
            connection.commit()

            print('101 send')
        if x.__contains__(100):
            ###
            cursor.execute('SELECT _data AS data FROM devicedata WHERE device_id = 74 ORDER BY _date desc LIMIT 1')
            records = cursor.fetchall()
            for row in records:
                feedback = int(float(row[0]))
            fuzzy1.update(feedback)
            output1 = fuzzy1.output
            if output1 > 255:
                output1 = 255
            cursor.execute('UPDATE devicesettings SET value =' + str(int(output1)) + ' WHERE device_id=100')
            connection.commit()
            print('100 send')
        if x.__contains__(100) or x.__contains__(101):
            cursor.close()
            connection.close()
            time.sleep(30)
        else:
            cursor.close()
            connection.close()
            time.sleep(60)


if __name__ == "__main__":

    li = [
        [[-50, -50, 5], [4, 5, 16], [15, 22, 22], [21, 31, 31], [30, 50, 50],
         [0, 1, 87], [86, 89, 110], [109, 109, 125], [124, 147, 150], [149, 250, 255]],
        [[0, 29, 30], [29, 59, 60], [59, 80, 85], [84, 88, 90], [89, 90, 100],
         [0, 70, 77], [77, 150, 154], [154, 155, 217], [217, 229, 230], [230, 255, 255]]
    ]
    fuzzy = FUZZY.FUZZY()
    fuzzy.set(0,li)
    fuzzy1 = FUZZY.FUZZY()
    fuzzy1.set(1, li)
    test_fuzzy(fuzzy, fuzzy1)
