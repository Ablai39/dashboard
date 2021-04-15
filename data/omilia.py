import traceback
import mysql.connector
from datetime import datetime, date, time, timedelta
from dashboard.data import variables
from dashboard.data.global_functions import get_prc, get_prc_1

APP_NAME = "'Halyk_Bank_Prod','Halyk_Pilot'"

def get_online_data():  
    try:
        response_data = {}
        conn = mysql.connector.connect(**variables.connect_to_db_omilia_cfg)
        cursor = conn.cursor()
    except Exception:
        return {'status': variables.connection_error_to_db_mysql}
    
    # Основные данные
    try:
        query = ("SELECT END_TYPE, count(1) \
                    FROM diamant.DIALOGS \
                    WHERE APP_NAME in (" + APP_NAME + ") \
                        AND STEPS_NUM !='0' \
                        AND DIALOG_DATE >= CURDATE() \
                        AND END_TYPE IS NOT NULL \
                    GROUP BY END_TYPE \
                    UNION ALL \
                    SELECT 'DURATION', ROUND(AVG(DURATION)) \
                    FROM diamant.DIALOGS \
                    WHERE APP_NAME in (" + APP_NAME + ") \
                        AND STEPS_NUM !='0' \
                        AND DIALOG_DATE >= CURDATE() \
                        AND DURATION > 5000")   

        total = 0
        context = {}
        cursor.execute(query)
    
        for p_type, p_cnt in cursor:
            if p_type == 'DURATION':
                context['AVG_DURATION'] = int(p_cnt)
            else:
                context[p_type] = int(p_cnt)
                total = total + int(p_cnt)
        
        for p_type in ['FAR_HUP','NEAR_HUP','TRANSFER']:
            context[p_type + '_PRC'] = get_prc_1(context[p_type], total)

        context['TOTAL_SUM'] = total
        context['SERVICE_LEVEL'] = get_prc((int(context['FAR_HUP']) + int(context['NEAR_HUP'])), total)      
        response_data['main'] = context

    except Exception:
        return {'status': traceback.format_exc()}

    # Переводы на операторов
    try:
        query = ("SELECT EXIT_POINT, COUNT(DIALOG_ID) \
                    FROM diamant.DIALOGS \
                    WHERE APP_NAME Like '%Halyk%' \
                        AND STEPS_NUM !='0' \
                        AND DIALOG_DATE >= CURDATE() \
                        AND END_TYPE = 'TRANSFER' \
                    GROUP BY EXIT_POINT")
        
        total = 0
        nList = []
        cursor.execute(query)

        for p_exit_point, p_cnt in cursor:
            nList.append({
                'vdn': str(p_exit_point),
                'cnt': int(p_cnt)
            })
            total += int(p_cnt)
        
        for index, value in enumerate(nList):
            nList[index]['prc'] = get_prc(value['cnt'], total)
        
        response_data['transfers'] = nList

    except Exception:
        return {'status': traceback.format_exc()}
    
    # Темы обращения
    try:
        query = ("SELECT ACTIVE_INTENT, COUNT(DISTINCT(DIALOG_ID)) \
                    FROM diamant.DIALOG_STEP_EVENTS \
                    WHERE APP_NAME in (" + APP_NAME + ") \
                        AND ACTIVE_INTENT NOT IN ('EndDialog','Transfer','Transfer-Card-Num-Incorrect','undefined') \
                        AND DIALOG_DATE >= CURDATE() \
                    GROUP BY ACTIVE_INTENT")
        
        total = 0
        nList = []
        cursor.execute(query)
    
        for p_intent, p_cnt in cursor:
            nList.append({
                'theme': str(p_intent),
                'cnt': int(p_cnt)
            })
            total += int(p_cnt)
        
        for index, value in enumerate(nList):
            nList[index]['prc'] = get_prc_1(value['cnt'], total)

        # сортировка
        newlist = sorted(nList, key=lambda k: k['cnt'], reverse=True)
        response_data['themes'] = newlist

    except Exception:
        return {'status': traceback.format_exc()}

    conn.close()
    cursor.close()
    response_data['status'] = variables.successful
    return response_data

def get_graphic_data():  
    try:
        response_data = {}
        conn = mysql.connector.connect(**variables.connect_to_db_omilia_cfg)
        cursor = conn.cursor()
    except Exception:
        return {'status': variables.connection_error_to_db_mysql}
    
    try:
        nList = []
        nListOfTime = []
        sysdate = datetime.now()
        delta = sysdate.minute % 5
        last_string_time = sysdate - timedelta(hours=0, minutes=delta, seconds=sysdate.second, microseconds=sysdate.microsecond)

        for index in range(7):
            if index == 0:
                value = last_string_time - timedelta(minutes=30)
                nListOfTime.append(value)
            else:
                nListOfTime.append(nListOfTime[index - 1] + timedelta(hours=0, minutes=5, seconds=0))
        
        for date in nListOfTime:
            total = 0
            context = {}
            p_date = date.strftime("%Y-%m-%d %H:%M:%S")

            query = ("SELECT END_TYPE, COUNT(1) \
                    FROM diamant.DIALOGS \
                   WHERE APP_NAME= '" + APP_NAME + "' \
                     AND STEPS_NUM !='0' \
                     AND DIALOG_DATE >= CURDATE() \
                     AND DIALOG_DATE <= '" + p_date + "'\
                     AND END_TYPE IS NOT NULL \
                GROUP BY END_TYPE")

            cursor.execute(query)
            context['TIME'] = date.strftime("%H:%M")

            for p_type, p_cnt in cursor:
                context[p_type] = p_cnt
                total = total + p_cnt
            
            context['TOTAL'] = total
            nList.append(context)
            response_data['result'] = nList

    except Exception:
        return {'status': traceback.format_exc()}

    conn.close()
    cursor.close()
    response_data['status'] = variables.successful
    return response_data

def get_history_data():

    try:
        conn = mysql.connector.connect(**variables.connect_to_db_omilia_cfg)
    except Exception:
        return {'status': variables.connection_error_to_db_mysql}   
    
    try:
        response_data = {}
        cursor = conn.cursor()
        
        # Основные данные
        res = [{}]
        query = ("SELECT a.END_TYPE, a.DDATE, a.CNT  \
                    FROM (SELECT END_TYPE, DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d') as 'DDATE', count(1) as 'CNT' \
                            FROM diamant.DIALOGS \
                           WHERE APP_NAME in (" + APP_NAME + ") \
                             AND STEPS_NUM !='0' \
                             AND DIALOG_DATE >= DATE_SUB(CURDATE(), INTERVAL 10 DAY) \
                             AND DIALOG_DATE < CURDATE() \
                           GROUP BY END_TYPE, DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d') \
                           ORDER BY DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d') DESC) a") 
        cursor.execute(query)

        for p_type, p_date, p_cnt in cursor:
            date_exists = False            

            for index, value in enumerate(res):
                key_exists = 'date' in value

                if key_exists:
                    if p_date == value['date']:
                        date_exists = True
                        break
            
            if date_exists:
                res[index][p_type] = p_cnt
            else:
                res.append ({
                    'date' : p_date,
                    p_type : p_cnt
                })
        
        del res[0]
        response_data['main'] = res

        # Трансферы
        total = 0
        nList = []
        query = ("SELECT EXIT_POINT, COUNT(DIALOG_ID) \
                    FROM diamant.DIALOGS \
                   WHERE APP_NAME in (" + APP_NAME + ") \
                     AND STEPS_NUM !='0' \
                     AND DIALOG_DATE \
                     AND DIALOG_DATE >= DATE_SUB(CURDATE(), INTERVAL 10 DAY) \
                     AND DIALOG_DATE < CURDATE() \
                     AND END_TYPE = 'TRANSFER' \
                   GROUP BY EXIT_POINT")
        cursor.execute(query)
    
        for p_exit_point, p_cnt in cursor:
            context = {
                'point': p_exit_point,
                'cnt': p_cnt
            }

            total = total + p_cnt
            nList.append(context)
        
        response_data['transfers'] = {
            'result': nList,
            'total': total
        }

        # Темы обращения
        total = 0
        nList = []
        query = ("SELECT ACTIVE_INTENT, COUNT(DISTINCT(DIALOG_ID)) \
                    FROM diamant.DIALOG_STEP_EVENTS \
                   WHERE APP_NAME in (" + APP_NAME + ") \
                     AND DIALOG_DATE >= DATE_SUB(CURDATE(), INTERVAL 10 DAY) \
                     AND DIALOG_DATE < CURDATE() \
                     AND ACTIVE_INTENT NOT IN ('EndDialog','Transfer','Transfer-Card-Num-Incorrect','undefined') \
                   GROUP BY ACTIVE_INTENT")
        cursor.execute(query)

        for p_intent, p_cnt in cursor:
            context = {
                'intent': p_intent,
                'cnt': p_cnt
            }

            total = total + p_cnt
            nList.append(context)
        
        # сортировка
        newlist = sorted(nList, key=lambda k: k['cnt'], reverse=True)        
        
        response_data['themes'] = {
            'result': newlist,
            'total': total
        }

        response_data['status'] = variables.successful

    except Exception:
        response_data = {'status': traceback.format_exc()}

    conn.close()
    cursor.close()
    return response_data

def get_hst_day_transfers(doper):

    try:
        conn = mysql.connector.connect(**variables.connect_to_db_omilia_cfg)
    except Exception:
        return {'status': variables.connection_error_to_db_mysql}

    try:
        total = 0
        nList = []
        response_data = {}
        cursor = conn.cursor()

        query = ("SELECT EXIT_POINT, COUNT(DIALOG_ID) \
                    FROM diamant.DIALOGS \
                WHERE APP_NAME in (" + APP_NAME + ") \
                    AND STEPS_NUM !='0' \
                    AND DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d') = '" + doper + "'\
                    AND END_TYPE = 'TRANSFER' \
                GROUP BY EXIT_POINT")
        cursor.execute(query)

        for p_exit_point, p_cnt in cursor:
            context = {
                'point': p_exit_point,
                'cnt': p_cnt
            }

            total = total + p_cnt
            nList.append(context)
        
        response_data['transfers'] = {
            'result': nList,
            'total': total
        }

    except Exception:
        response_data = {'status': traceback.format_exc()}
    
    conn.close()
    cursor.close()
    return response_data

def get_topic_th_app(doper):

    try:
        conn = mysql.connector.connect(**variables.connect_to_db_omilia_cfg)
    except Exception:
        return {'status': variables.connection_error_to_db_mysql}

    try:
        total = 0
        nList = []
        response_data = {}
        cursor = conn.cursor()

        query = ("SELECT ACTIVE_INTENT, COUNT(DISTINCT(DIALOG_ID)) \
                    FROM diamant.DIALOG_STEP_EVENTS \
                    WHERE APP_NAME in (" + APP_NAME + ") \
                        AND ACTIVE_INTENT NOT IN ('EndDialog','Transfer','Transfer-Card-Num-Incorrect','undefined') \
                        AND DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d') = '" + doper + "' \
                    GROUP BY ACTIVE_INTENT")
        cursor.execute(query)

        for p_intent, p_cnt in cursor:
            context = {
                'intent': p_intent,
                'cnt': p_cnt
            }

            total = total + p_cnt
            nList.append(context)
        
        response_data['themes'] = {
            'result': nList,
            'total': total
        }

        response_data['status'] = variables.successful

    except Exception:
        response_data = {'status': traceback.format_exc()}
    
    conn.close()
    cursor.close()
    return response_data