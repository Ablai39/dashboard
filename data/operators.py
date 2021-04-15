import pyodbc
import traceback
from pymemcache.client.base import Client
from datetime import datetime, date, time, timedelta
from dashboard.data.global_functions import nvl, needUpdate, json_serializer, json_deserializer
from dashboard.data.variables import host, gMemCachedUrl, connect_to_db_cms_cfg, connection_error_to_db_cms, successful
from pymemcache.client.base import Client
from datetime import datetime

def operators():

    # подключаемся к CMS
    try:
        conn = pyodbc.connect(r'%s' % (connect_to_db_cms_cfg))
    except Exception:
        return {'status': connection_error_to_db_cms}

    try:
        upib = []
        rubs = []
        uprk = []
        utp = []
        cursor = conn.cursor()

        query = "select item_name, value \
                   from synonyms s1 \
                  where s1.item_type = 'agname' \
                    and item_name not in ('test TSI 1','Test TSI 2','Vadim','test_Oleg','Salavat test','test_Terrasoft','Salavat','Oleg','Agent_for_learning') \
                    and value like '78%' \
                    and SUBSTR(value, 3, 1) in (0,1,2,3,4,5,6,7,8)"
        cursor.execute(query)

        for name, logid in cursor:
            if str(logid[2]) in ['0','1','2','3']:
                uprk.append([name.strip(), logid.strip()])
            
            elif str(logid[2]) == '4':
                if str(logid[3]) not in ['0','1']:
                    rubs.append([name.strip(), logid.strip()])

            elif str(logid[2]) == '5':
                upib.append([name.strip(), logid.strip()])

            elif str(logid[2]) in ['6','7']:
                utp.append([name.strip(), logid.strip()])
            
            elif str(logid[2]) == '8':
                if str(logid[3]) in ['0','5']:
                    rubs.append([name.strip(), logid.strip()])
        
        context = {
            'upib': upib,
            'rubs': rubs,
            'uprk': uprk,
            'utp': utp
        }

    except Exception:        
        context = {'status': traceback.format_exc()}

    cursor.close()
    conn.close()
    return context

def get_operators_list():

    try:
        global host
        if host == 'server':
            client = Client((gMemCachedUrl), serializer=json_serializer, deserializer=json_deserializer)
    except Exception:
        return {'status': traceback.format_exc()}

    try:
        need_update = False
        dictCode = 'OPERATORS_LIST'
        
        if host == 'server':
            context = client.get(dictCode)

            if context is None:
                need_update = True
            else:
                last_updated_datetime = datetime.strptime(context['updated_datetime'], '%Y-%m-%d %H:%M:%S')
                need_update = needUpdate('', last_updated_datetime, 'day', 0)
        else:
            need_update = True
        
        if need_update:
            context = operators()
            updated_datetime = datetime.today()
            context['updated_datetime'] = updated_datetime.strftime('%Y-%m-%d %H:%M:%S')

        if host == 'server':
            if need_update:
                client.set(dictCode, context)
            client.close()

        return context

    except Exception:
        if host == 'server':
            client.close()
        return {'status': traceback.format_exc()}


def import_plan(doper, upravlenie, operators_cnt):
    # подключаемся к CMS
    try:
        conn = pyodbc.connect('%s' % (connect_to_db_cms_cfg))
    except Exception:
        return {'status': connection_error_to_db_cms}

    try:
        context = {'status': successful}
        starttimeLst = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','09:30','10:00','11:00', \
                        '12:00','13:00','14:00','15:00','16:00','17:00','18:00','18:30','19:00','20:00','21:00','22:00','23:00']
        
        endtimeLst = ['01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','09:30','10:00','11:00','12:00', \
                      '13:00','14:00','15:00','16:00','17:00','18:00','18:30','19:00','20:00','21:00','22:00','23:00','23:59']
        
        if len(starttimeLst) != len(endtimeLst):
            return {'status': 'Время старта и время окончания не равны'}
        
        cursor = conn.cursor()
        query = "select count(1) from z_hagent_plan where doper = to_date('"+ doper +"','%Y-%m-%d') and upravlenie = '" + upravlenie + "'"
        cursor.execute(query)

        for value in cursor:
            cnt = int(value[0])
        
        if cnt > 0:
            context = {'status': 'Данные за '+ doper + ' уже имеются по управлению ' + upravlenie}
        else:
            operatorsCnt = operators_cnt
            
            oprCnt = []
            while 1 == 1:
                index = operatorsCnt.find(',')
                if index == -1:
                    oprCnt.append(int(operatorsCnt.strip()))
                    break

                value = operatorsCnt[0:index]
                oprCnt.append(int(value))
                operatorsCnt = operatorsCnt[index+1:]
            
            if len(oprCnt) != len(starttimeLst):
                context = {'status': 'Некорректные данные по количеству операторов'}
            else:
                for index in range(len(starttimeLst)):
                    query = "insert into z_hagent_plan (doper, starttime, endtime, upravlenie, operators) \
                        values (to_date('"+ doper +"','%Y-%m-%d'),'"+ starttimeLst[index] +"','"+ endtimeLst[index] +"','"+ upravlenie +"',"+ str(oprCnt[index]) +")"
                    cursor.execute(query)
            
        cursor.close()
        conn.close()
        return context

    except Exception:
        cursor.close()
        conn.close()
        return {'status':  traceback.format_exc()}

def get_plan():
    # подключаемся к CMS
    try:
        conn = pyodbc.connect(r'%s' % (connect_to_db_cms_cfg))
    except Exception:
        return {'status': connection_error_to_db_cms}

    try:
        context = {}
        cursor = conn.cursor()
        today = datetime.today()
        today_date_str = today.strftime('%Y-%m-%d')
        fromdate = "to_date('"+ today_date_str +" '||starttime, '%Y-%m-%d %H:%M')"
        todate = "to_date('"+ today_date_str +" '||endtime, '%Y-%m-%d %H:%M')"

        query = "select doper, starttime, endtime, upravlenie, operators from z_hagent_plan where doper = date(sysdate) and sysdate between "+ fromdate +" and " + todate 
        cursor.execute(query)

        context['doper'] = today_date_str
        context['operators'] = {'others': 0}
        for doper, starttime, endtime, upravlenie, operators  in cursor:
            context['starttime'] = starttime.strip()
            context['endtime'] = endtime.strip()
            context['operators'][upravlenie.strip()] = operators

        cursor.close()
        conn.close()
        return context

    except Exception:
        cursor.close()
        conn.close()
        return {'status':  traceback.format_exc()}
        