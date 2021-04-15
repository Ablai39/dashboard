import pyodbc
import mysql.connector
import traceback
from dashboard.data.variables import connect_to_db_cms_cfg, connection_error_to_db_cms, connection_error_to_db_cmsreport, connect_to_db_ivr_cfg, \
    connect_to_db_omilia_cfg, successful, connection_error_to_db_mysql, another_method_error
from datetime import datetime, date, time, timedelta
from dashboard.data.global_functions import get_prc, get_prc_1, list2str
import time
from dashboard.data.vdnGroup import incomingCallsVdnDict
from dashboard.data.config import sectorsDict

from dashboard.data.skill_groups import all_depart_skills_str

# ------------------------------------------------------------------------
def get_MainReportData_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'REPORTS_MAIN_REPORT', 'day', 1)

def get_ReportUTPCalls_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'REPORTS_UTP_SPLIT_CALLS', 'day', 1)

# ------------------------------------------------------------------------

def get_MainReportData():
   
    p_days = '7'
    nList = []

    # Подключаемся к CMS
    try:
        conn = pyodbc.connect(r'%s' % (connect_to_db_cms_cfg))
    except Exception:
        return {'status': connection_error_to_db_cms}
    
    try:
        cursor = conn.cursor()

        allSectorsSplitsLst = [] 
        for sector in sectorsDict:
            for split in sectorsDict[sector]['splitsLst']:
                allSectorsSplitsLst.append(split)

            if sectorsDict[sector]['enableCallBack'] == 'Y':
                for split in sectorsDict[sector]['splits_cbaLst']:
                    allSectorsSplitsLst.append(split)

        allSectorsSplitsLstStr = list2str(allSectorsSplitsLst)

        # Собираем данные принятым/потерянным звонкам
        query = "select row_date, \
                    sum(acceptable) as acceptable, \
                    sum(slvlabns) as slvlabns, \
                    sum(callsoffered) as callsoffered, \
                    sum(acdcalls) acdcalls, \
                    sum(abncalls) abncalls, \
                    (sum(acdcalls1) + sum(acdcalls2) + sum(acdcalls3) + sum(acdcalls4) + sum(acdcalls5)) acd_do_40sec, \
                    sum(acdcalls6) acd_do_60sec, \
                    sum(acdcalls7) acd_do_2min, \
                    sum(acdcalls8) acd_do_5min, \
                    sum(acdcalls9) acd_do_10min, \
                    sum(acdcalls10) acd_ot_10min, \
                    sum(abncalls1) abn_do_10sec, \
                    sum(abncalls2) abn_do_15sec, \
                    sum(abncalls3) abn_do_20sec, \
                    sum(abncalls4) abn_do_30sec, \
                    sum(abncalls5) abn_do_40sec, \
                    sum(abncalls6) abn_do_60sec, \
                    sum(abncalls7) abn_do_2min, \
                    sum(abncalls8) abn_do_5min, \
                    sum(abncalls9) abn_do_10min, \
                    sum(abncalls10) abn_ot_10min \
                from dsplit \
                where split in (" + allSectorsSplitsLstStr + ") \
                and row_date < date(sysdate) \
                and row_date >= date(sysdate) - " + p_days + " \
                group by row_date \
                order by row_date desc"
               
        cursor.execute(query)
        for doper, acceptable, slvlabns, callsoffered, acdcalls, abncalls, \
            acd_do_40sec, acd_do_60sec, acd_do_2min, acd_do_5min, acd_do_10min, acd_ot_10min, \
            abn_do_10sec, abn_do_15sec, abn_do_20sec, abn_do_30sec, \
            abn_do_40sec, abn_do_60sec, abn_do_2min, abn_do_5min, abn_do_10min, abn_ot_10min in cursor:

            nList.append({
               'doper': str(doper),
               'service_level': get_prc(int(acceptable) + int(slvlabns), int(callsoffered)),
               'callsoffered': int(callsoffered),
               'acdcalls': int(acdcalls),
               'abncalls': int(abncalls),

               'acd_do_40sec': int(acd_do_40sec),
               'acd_do_60sec': int(acd_do_60sec),
               'acd_do_2min': int(acd_do_2min),
               'acd_do_5min': int(acd_do_5min),
               'acd_do_10min': int(acd_do_10min),
               'acd_ot_10min': int(acd_ot_10min),
               
               'abn_do_10sec': int(abn_do_10sec),
               'abn_do_15sec': int(abn_do_15sec),
               'abn_do_20sec': int(abn_do_20sec),
               'abn_do_30sec': int(abn_do_30sec),
               
               'abn_do_40sec': int(abn_do_40sec),
               'abn_do_60sec': int(abn_do_60sec),
               'abn_do_2min': int(abn_do_2min),
               'abn_do_5min': int(abn_do_5min),
               'abn_do_10min': int(abn_do_10min),
               'abn_ot_10min': int(abn_ot_10min),
               
               'ivr_successful': 0,
               'ivr_breaked': 0
            })
        
        allIncomingCallsVdn = []
        for number in incomingCallsVdnDict:
            for vdn in incomingCallsVdnDict[number]['vdnLst']:
                allIncomingCallsVdn.append(vdn)

        allIncomingCallsVdnStr = list2str(allIncomingCallsVdn)

        # Собираем данные по объему входящих звонков
        query = "select row_date, SUM(incalls)\
                 from dvdn \
                 where row_date >= date(sysdate) - " + p_days + " \
                 and row_date < date(sysdate) \
                 and vdn in (" + allIncomingCallsVdnStr + ") \
                 group by row_date \
                 order by row_date"
        cursor.execute(query)

        for doper, incalls in cursor:
            for index, values in enumerate(nList):
                if str(doper) == str(values['doper']):
                    nList[index]['vdn_incalls'] = int(incalls)
                    break

        # Собираем данные по пропущенным звонкам
        # из cm прямое подключение к операторам = 79401,79402,79403,79407,79408,79409,79410,79411,79412,79413,79414,79415,79418,79419,79421,79422,79423,79425,79426,79865, \
        # из cm в aep = 79404,79405,79406,79416,79417,79424,79533,79495,79600,79496,79866
        # из aep в omilia = 79598
        # из ivr в omilia = 79854

        query = "select row_date, SUM(abncalls) abncalls \
                   from dvdn \
                  where row_date >= date(sysdate) - " + p_days + " \
                    and row_date < date(sysdate) \
                    and vdn in ( \
                    79401,79402,79403,79407,79408,79409,79410,79411,79412,79413,79414,79415,79418,79419,79421,79422,79423,79425,79426,79865, \
                    79404,79405,79406,79416,79417,79424,79533,79495,79600,79496,79866, \
                    79598,79854)  \
                  group by row_date \
                  order by row_date"
        cursor.execute(query)
        
        for doper, abncalls in cursor:
            for index, values in enumerate(nList):
                if str(doper) == str(values['doper']):
                    nList[index]['vdn_abncalls'] = int(abncalls)

        cursor.close()
        conn.close()

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}
    
    # Подключаемся к IVR
    try:
        pyodbc.pooling = False
        conn = pyodbc.connect(r'%s' % (connect_to_db_ivr_cfg))
    except Exception:
        return {'status': connection_error_to_db_cmsreport}

    try:
        cursor = conn.cursor()
        cursor.execute("select top " + p_days + " \
                               calendar_day, \
                               successful, \
                               breaked \
                          from cmsreport.dbo.ivr_day_history \
                         order by calendar_day DESC")

        for doper, ivr_successful, ivr_breaked in cursor:
            for index, values in enumerate(nList):
                if str(doper) == str(values['doper']):
                    nList[index]['ivr_successful'] = int(ivr_successful)
                    nList[index]['ivr_breaked'] = int(ivr_breaked)
                    break
        
        cursor.close()
        conn.close()

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}
    
    # Подключаемся к Omilia
    try:
        conn = mysql.connector.connect(**connect_to_db_omilia_cfg)
    except Exception:
        return {'status': connection_error_to_db_mysql}

    try:        
        cursor = conn.cursor()
        query = ("SELECT DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d') as 'DATE', END_TYPE, count(1) as 'CNT' \
                  FROM diamant.DIALOGS \
                  WHERE APP_NAME in ('Halyk_Bank_Prod','Halyk_Pilot') \
                  AND STEPS_NUM !='0' \
                  AND DIALOG_DATE >= DATE_SUB(CURDATE(), INTERVAL " + p_days + " DAY) \
                  AND DIALOG_DATE < CURDATE() \
                  AND END_TYPE in ('FAR_HUP','NEAR_HUP') \
                  GROUP BY DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d'), END_TYPE \
                  ORDER BY DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d') DESC")
        cursor.execute(query)

        for doper, end_type, count in cursor:
            for index, values in enumerate(nList):
                if str(doper) == str(values['doper']):
                    nList[index]['omilia_' + end_type.swapcase()] = int(count)

        cursor.close()
        conn.close()        

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}
    
    # Расчет процентов
    try:
        for index, values in enumerate(nList):
            for tag in ['omilia_far_hup','omilia_near_hup','ivr_successful','callsoffered','acdcalls','abncalls','vdn_incalls']:
                if tag not in values:
                    nList[index][tag] = 0

            nList[index]['omilia_prc'] = get_prc_1(values['omilia_far_hup'] + values['omilia_near_hup'], values['vdn_incalls'])
            nList[index]['ivr_successful_prc'] = get_prc_1(values['ivr_successful'], values['vdn_incalls'])
            nList[index]['callsoffered_prc'] = get_prc_1(values['callsoffered'], values['vdn_incalls'])
            nList[index]['acdcalls_prc'] = get_prc_1(values['acdcalls'], values['callsoffered'])
            nList[index]['abncalls_prc'] = get_prc_1(values['abncalls'], values['callsoffered'])

            for tag in ['acd_do_40sec','acd_do_60sec','acd_do_2min','acd_do_5min','acd_do_10min','acd_ot_10min']:
                nList[index][tag + '_prc'] = get_prc_1(values[tag],values['acdcalls'])
            
            for tag in ['abn_do_10sec','abn_do_15sec','abn_do_20sec','abn_do_30sec','abn_do_40sec','abn_do_60sec','abn_do_2min','abn_do_5min','abn_do_10min','abn_ot_10min']:
                nList[index][tag + '_prc'] = get_prc_1(values[tag],values['abncalls'])

    except Exception:
        return {'status': traceback.format_exc()}

    return {
        'status': successful,
        'allSectorsSplitsLstStr': allSectorsSplitsLstStr,
        'allIncomingCallsVdnStr': allIncomingCallsVdnStr,
        'result': nList,
    }

def get_ReportUTPCalls():
   
    p_days = '7'
    nList = []

    # Подключаемся к CMS
    try:
        conn = pyodbc.connect(r'%s' % (connect_to_db_cms_cfg))
    except Exception:
        return {'status': connection_error_to_db_cms}
    
    try:
        cursor = conn.cursor()
        # Собираем данные принятым/потерянным звонкам       
        query = "select row_date as doper, \
                    sum(acceptable) as acceptable, \
                    sum(slvlabns) as slvlabns, \
                    sum(callsoffered) as callsoffered, \
                    sum(acdcalls) acdcalls, \
                    sum(abncalls) abncalls, \
                    (sum(acdcalls1) + sum(acdcalls2) + sum(acdcalls3) + sum(acdcalls4) + sum(acdcalls5)) acd_do_40sec, \
                    sum(acdcalls6) acd_do_60sec, \
                    sum(acdcalls7) acd_do_2min, \
                    sum(acdcalls8) acd_do_5min, \
                    sum(acdcalls9) acd_do_10min, \
                    sum(acdcalls10) acd_ot_10min, \
                    sum(abncalls1) abn_do_10sec, \
                    sum(abncalls2) abn_do_15sec, \
                    sum(abncalls3) abn_do_20sec, \
                    sum(abncalls4) abn_do_30sec, \
                    sum(abncalls5) abn_do_40sec, \
                    sum(abncalls6) abn_do_60sec, \
                    sum(abncalls7) abn_do_2min, \
                    sum(abncalls8) abn_do_5min, \
                    sum(abncalls9) abn_do_10min, \
                    sum(abncalls10) abn_ot_10min \
                from dsplit \
                where split in (" + sectorsDict['sales']['splitsStr'] + ") \
                    and row_date < date(sysdate) \
                    and row_date >= date(sysdate) - " + p_days + " \
                    group by row_date \
                    order by row_date desc"
        
        cursor.execute(query)
        for doper, acceptable, slvlabns, callsoffered, acdcalls, abncalls, \
            acd_do_40sec, acd_do_60sec, acd_do_2min, acd_do_5min, acd_do_10min, acd_ot_10min, \
            abn_do_10sec, abn_do_15sec, abn_do_20sec, abn_do_30sec, \
            abn_do_40sec, abn_do_60sec, abn_do_2min, abn_do_5min, abn_do_10min, abn_ot_10min in cursor:

            nList.append({
               'doper': str(doper),
               'callsoffered': int(callsoffered),
               'service_level': get_prc(int(acceptable) + int(slvlabns), int(callsoffered)),
               'acdcalls': int(acdcalls),
               'acdcalls_prc': get_prc_1(int(acdcalls), int(callsoffered)),
               'abncalls': int(abncalls),
               'abncalls_prc': get_prc_1(int(abncalls), int(callsoffered)),

               'acd_do_40sec': int(acd_do_40sec),
               'acd_do_60sec': int(acd_do_60sec),
               'acd_do_2min': int(acd_do_2min),
               'acd_do_5min': int(acd_do_5min),
               'acd_do_10min': int(acd_do_10min),
               'acd_ot_10min': int(acd_ot_10min),
               
               'abn_do_10sec': int(abn_do_10sec),
               'abn_do_15sec': int(abn_do_15sec),
               'abn_do_20sec': int(abn_do_20sec),
               'abn_do_30sec': int(abn_do_30sec),
               
               'abn_do_40sec': int(abn_do_40sec),
               'abn_do_60sec': int(abn_do_60sec),
               'abn_do_2min': int(abn_do_2min),
               'abn_do_5min': int(abn_do_5min),
               'abn_do_10min': int(abn_do_10min),
               'abn_ot_10min': int(abn_ot_10min)
            })

    except Exception:
        return {'status': traceback.format_exc()}
    
    # Расчет процентов
    try:
        for index, values in enumerate(nList):           
            for tag in ['acd_do_40sec','acd_do_60sec','acd_do_2min','acd_do_5min','acd_do_10min','acd_ot_10min']:
                nList[index][tag + '_prc'] = get_prc_1(values[tag],values['acdcalls'])
            
            for tag in ['abn_do_10sec','abn_do_15sec','abn_do_20sec','abn_do_30sec','abn_do_40sec','abn_do_60sec','abn_do_2min','abn_do_5min','abn_do_10min','abn_ot_10min']:
                nList[index][tag + '_prc'] = get_prc_1(values[tag],values['abncalls'])

    except Exception:
        return {'status': traceback.format_exc()}

    return {
        'status': successful,
        'result': nList,
    }

def report_incoming_split_calls(ndate):   
    
    context = {}
    nSplits_VDNs = [
        # 0 элемент - наименование скилла
        # 1 элемент - список VDN, входящие вызовы (прямые) из внешних номеров
        # 2 элемент - список тестовых VDN, вызовы направленные напрямую в очередь
        # 3 элемент - список VDN, регистрация в очереди
        # 4 элемент - список VDN, трансферы из других скиллов в очередь
        # 5 элемент - список VDN, трансферы из Omilia
        # 6 элемент - список VDN, трансферы из IVR
        # 7 элемент - список Splits, номера скилл групп
        ['premium',[79401,79402,79403,79414],[],[79502,79503,79504],[79551,79552,79553],[],[],[2,3,4]],

        ['onlinebank',[79407,79408,79409,79419,79425,79496,79865],[79874],[79500,79501],[79559,79560],[79850,79851],[],[26,27,28]],

        ['pos',[79410,79411,79412,79422,79426],[],[79505,79506],[79562,79563],[79852,79853],[],[17,18,19]],

        ['amex',[79415,79423],[79497,79498,79499],[],[79554,79555,79556],[],[],[5,6,7]],

        ['vip_onlinebank',[79418],[79509,79510],[],[79557,79558],[],[],[65,66]],

        ['vip_pos',[79421],[],[],[79561],[],[],[8,64]],

        ['H&M',[79494],[],[],[],[],[],[40]],

        ['VIP',[79413],[],[],[79550],[],[],[36]],

        ['minipos',[],[],[],[79576,79577,79578],[],[],[37,38,39]],

        ['card',[79532],[79873,79592],[],[79564,79565,79566],[79515,79584],[79427,79428,79429,79430,79431,79432,79433,79434,79546,79547,79548,79549],[11,12,13]],

        ['homebank',[],[79871],[],[79579,79580,79581],[79516,79585],[79482,79483,79484,79485,79486,79487,79488,79489,79490,79491,79492,79493],[14,15,16]],

        ['retail',[79595,79597],[79872],[],[79570,79571,79572,79475,79476],[79517,79586],[79448,79449,79450,79451,79452,79453,79454,79455,79456,79457,79458,79459],[20,21,22]],

        ['payments',[],[],[],[79567,79568,79569],[79518,79587],[79436,79437,79438,79439,79440,79441,79442,79443,79444,79445,79446,79447],[30,31,32]],

        # ['sales',[79511],[],[79463,79467,79471],[79573,79574,79575],[79519,79588],[79460,79461,79462,79464,79465,79466,79468,79469,79470],[33,34,35]]
    ]

    nIVR_VDNs = [
        # 0 элемент - список VDN, входящие вызовы
        # 1 элемент - список VDN, балансер
        # 2 элемент - VDN IVR Avaya
        [79404,79405,79406,79416,79417,79424,79533,79495,79600,79866],[79598],[79538]
    ]
    
    # примечание
    # "doper": Дата
    # "incomingCalls": Общее количество входящих вызовов
    # "incomingCalls_Outflowcalls": Общее количество переведенных вызовов на другой VDN на уровне первого VDN (только прямые вызовы)
    # "abandonedCalls": Общее количество потерянных вызовов
    # "incomingCalls_inQueue": Общее количество поставленных на очередь вызовов (только прямые вызовы)
    # "tranFromOperator_inQueue": Общее количество вызовов переведенных с других скилл групп
    # "tranFromOmilia_inQueue": Общее количество вызовов переведенных с Омилия
    # "tranFromIVR_inQueue": Общее количество вызовов переведенных с IVR
    # "service_level": Service Level
    # "callsoffered": Общее количество вызовов на уровне очереди (SPLIT)
    # "acdcalls": Общее количество принятых вызовов на уровне очереди
    # "abncalls": Общее количество потерянных вызово на уровне очереди

    def getQuery_vdn(strvdn, indate):
        return "select row_date, sum(incalls), sum(outflowcalls) \
                  from dvdn \
                 where row_date = to_date('" + ndate + "', '%Y-%m-%d')  \
                   and vdn in (" + strvdn + ")  \
                 group by row_date"

    # Подключаемся к CMS
    try:
        conn = pyodbc.connect(r'%s' % (connect_to_db_cms_cfg))
    except Exception:
        return {'status': connection_error_to_db_cms}
    
    try:
        cursor = conn.cursor()
        context['doper'] = ndate
        # Собираем данные принятым/потерянным звонкам
        for split in nSplits_VDNs:               
            name = split[0]
            context[name] = {}

            tmpContext = {
                'incomingCalls': 0,
                'incomingCalls_Outflowcalls': 0,
                'abandonedCalls': 0,
                'incomingCalls_inQueue': 0,
                'incomingCalls_Outflowcalls_inQueue': 0,
                'tranFromOperator_inQueue': 0,
                'tranFromOperator_Outflowcalls': 0,
                'tranFromOmilia_inQueue': 0,
                'tranFromOmilia_Outflowcalls': 0,
                'tranFromIVR_inQueue': 0,
                'tranFromIVR_Outflowcalls': 0,
                'all_Outflowcalls': 0,
                'service_level': 0,
                'callsoffered': 0,
                'acdcalls': 0,
                'prc_acdcalls': 0,
                'abncalls': 0,
                'prc_abncalls': 0,
                'acd_do_40sec': 0,
                'acd_do_60sec': 0,
                'acd_do_2min': 0,
                'acd_do_5min': 0,
                'acd_do_10min': 0,
                'acd_ot_10min': 0,
                'abn_do_10sec': 4,
                'abn_do_15sec': 0,
                'abn_do_20sec': 0,
                'abn_do_30sec': 0,
                'abn_do_40sec': 0,
                'abn_do_60sec': 0,
                'abn_do_2min': 0,
                'abn_do_5min': 0,
                'abn_do_10min': 0,
                'abn_ot_10min': 0,
            }
          
            # Сбор данных по элементу 1
            # список VDN, входящие вызовы (прямые) из внешних номеров
            if len(split[1]) > 0:
                tmpStrVDNs = list2str(split[1])
                query = getQuery_vdn(tmpStrVDNs, str(ndate))
                cursor.execute(query)

                for doper, incalls, outflowcalls in cursor:
                    # Если между VDN номера является VDN-ом очереди
                    if len(split[3]) == 0:
                        inQueue = int(incalls)
                    else:
                        inQueue = 0
                    
                    tmpContext['incomingCalls'] = int(incalls)
                    tmpContext['incomingCalls_Outflowcalls'] = int(outflowcalls)
                    tmpContext['incomingCalls_inQueue'] = inQueue
            
            # Сбор данных по элементу 2
            # вызовы направленные напрямую в очередь, для увеличения общего входа
            if len(split[2]) > 0:
                tmpStrVDNs = list2str(split[2])
                query = getQuery_vdn(tmpStrVDNs, ndate)
                cursor.execute(query)
                for doper, incalls, outflowcalls in cursor:
                    tmpContext['incomingCalls'] += int(incalls)

            # Сбор данных по элементу 3
            # постановка в очередь
            if len(split[3]) > 0:
                tmpStrVDNs = list2str(split[3])
                query = getQuery_vdn(tmpStrVDNs, ndate)
                cursor.execute(query)
                for doper, incalls, outflowcalls in cursor:
                    tmpContext['incomingCalls_inQueue'] = int(incalls)
                    tmpContext['incomingCalls_Outflowcalls_inQueue'] = int(outflowcalls)
                
                if name == 'sales':
                    tmpContext['incomingCalls_inQueue'] -= int(outflowcalls)
            
            # Сбор данных по элементу 4
            # трансферы из других скиллов в очередь
            if len(split[4]) > 0:
                tmpStrVDNs = list2str(split[4])
                query = getQuery_vdn(tmpStrVDNs, ndate)
                cursor.execute(query)
                for doper, incalls, outflowcalls in cursor:
                    tmpContext['tranFromOperator_inQueue'] = int(incalls)
                    tmpContext['tranFromOperator_Outflowcalls'] = int(outflowcalls)
                
                if name == 'sales':
                    tmpContext['tranFromOperator_inQueue'] -= int(outflowcalls)

            # Сбор данных по элементу 5
            # трансферы из Omilia
            if len(split[5]) > 0:
                tmpStrVDNs = list2str(split[5])
                query = getQuery_vdn(tmpStrVDNs, ndate)
                cursor.execute(query)
                for doper, incalls, outflowcalls in cursor:
                    tmpContext['tranFromOmilia_inQueue'] = int(incalls)
                    tmpContext['tranFromOmilia_Outflowcalls'] = int(outflowcalls)
                
                if name == 'sales':
                    tmpContext['tranFromOmilia_inQueue'] -= int(outflowcalls)

            # Сбор данных по элементу 6
            # трансферы из IVR
            if len(split[6]) > 0:
                tmpStrVDNs = list2str(split[6])
                query = getQuery_vdn(tmpStrVDNs, ndate)
                cursor.execute(query)
                for doper, incalls, outflowcalls in cursor:
                    tmpContext['tranFromIVR_inQueue'] = int(incalls)
                    tmpContext['tranFromIVR_Outflowcalls'] = int(outflowcalls)
                
                if name == 'sales':
                    tmpContext['tranFromIVR_inQueue'] -= int(outflowcalls)

            # Только для УТП
            if name == 'sales':
                ivr_sales = tmpContext['incomingCalls_inQueue'] - tmpContext['incomingCalls_Outflowcalls']
                tmpContext['tranFromIVR_inQueue'] += ivr_sales
                tmpContext['incomingCalls_inQueue'] -= ivr_sales

            # Сбор данных по элементу 7
            tmpStrSplits = list2str(split[7])
            query = "select sum(acceptable) as acceptable, \
                            sum(slvlabns) as slvlabns, \
                            sum(callsoffered) as callsoffered, \
                            sum(acdcalls) acdcalls, \
                            sum(abncalls) abncalls, \
                            (sum(acdcalls1) + sum(acdcalls2) + sum(acdcalls3) + sum(acdcalls4) + sum(acdcalls5)) acd_do_40sec, \
                            sum(acdcalls6) acd_do_60sec, \
                            sum(acdcalls7) acd_do_2min, \
                            sum(acdcalls8) acd_do_5min, \
                            sum(acdcalls9) acd_do_10min, \
                            sum(acdcalls10) acd_ot_10min, \
                            sum(abncalls1) abn_do_10sec, \
                            sum(abncalls2) abn_do_15sec, \
                            sum(abncalls3) abn_do_20sec, \
                            sum(abncalls4) abn_do_30sec, \
                            sum(abncalls5) abn_do_40sec, \
                            sum(abncalls6) abn_do_60sec, \
                            sum(abncalls7) abn_do_2min, \
                            sum(abncalls8) abn_do_5min, \
                            sum(abncalls9) abn_do_10min, \
                            sum(abncalls10) abn_ot_10min \
                       from dsplit \
                      where split in (" + tmpStrSplits + ") \
                        and row_date = to_date('" + ndate + "', '%Y-%m-%d')"
            cursor.execute(query)

            for acceptable, slvlabns, callsoffered, acdcalls, abncalls, \
                acd_do_40sec, acd_do_60sec, acd_do_2min, acd_do_5min, acd_do_10min, acd_ot_10min, \
                abn_do_10sec, abn_do_15sec, abn_do_20sec, abn_do_30sec, \
                abn_do_40sec, abn_do_60sec, abn_do_2min, abn_do_5min, abn_do_10min, abn_ot_10min in cursor:

                # Считаем потерянные вызовы
                sumInQueue = tmpContext['incomingCalls_inQueue'] + \
                             tmpContext['tranFromOperator_inQueue'] + \
                             tmpContext['tranFromOmilia_inQueue'] + \
                             tmpContext['tranFromIVR_inQueue']

                if name == 'sales':
                    incomingCalls_abn = tmpContext['incomingCalls'] - tmpContext['incomingCalls_Outflowcalls']

                    all_outflow = tmpContext['incomingCalls_Outflowcalls_inQueue'] + \
                                  tmpContext['tranFromOperator_Outflowcalls'] + \
                                  tmpContext['tranFromOmilia_Outflowcalls'] + \
                                  tmpContext['tranFromIVR_Outflowcalls']
                    
                    tmpContext['all_Outflowcalls'] = all_outflow
                    tmpContext['abandonedCalls'] = sumInQueue - all_outflow - int(callsoffered) + incomingCalls_abn
                else:
                    incomingCalls_abn = tmpContext['incomingCalls'] - tmpContext['incomingCalls_inQueue']
                    tmpContext['abandonedCalls'] = (sumInQueue - int(callsoffered)) + incomingCalls_abn

                tmpContext['service_level'] = get_prc(int(acceptable) + int(slvlabns), int(callsoffered))
                tmpContext['callsoffered'] = int(callsoffered)
                tmpContext['acdcalls'] = int(acdcalls)
                tmpContext['prc_acdcalls'] = get_prc(int(acdcalls), int(callsoffered))
                tmpContext['abncalls'] = int(abncalls)
                tmpContext['prc_abncalls'] = get_prc(int(abncalls), int(callsoffered))
                tmpContext['acceptable'] = int(acceptable)
                tmpContext['slvlabns'] = int(slvlabns)
                tmpContext['acd_do_40sec'] = int(acd_do_40sec)
                tmpContext['acd_do_60sec'] = int(acd_do_60sec)
                tmpContext['acd_do_2min'] = int(acd_do_2min)
                tmpContext['acd_do_5min'] = int(acd_do_5min)
                tmpContext['acd_do_10min'] = int(acd_do_10min)
                tmpContext['acd_ot_10min'] = int(acd_ot_10min)
                tmpContext['abn_do_10sec'] = int(abn_do_10sec)
                tmpContext['abn_do_15sec'] = int(abn_do_15sec)
                tmpContext['abn_do_20sec'] = int(abn_do_20sec)
                tmpContext['abn_do_30sec'] = int(abn_do_30sec)
                tmpContext['abn_do_40sec'] = int(abn_do_40sec)
                tmpContext['abn_do_60sec'] = int(abn_do_60sec)
                tmpContext['abn_do_2min'] = int(abn_do_2min)
                tmpContext['abn_do_5min'] = int(abn_do_5min)
                tmpContext['abn_do_10min'] = int(abn_do_10min)
                tmpContext['abn_ot_10min'] = int(abn_ot_10min)
        
            context[name] = tmpContext
        
        # Сбор данных по VDN IVR-ов
        ivrContext = {
            'ivrVDN_IncomingCalls': 0,
            'ivrVDN_IncomingCalls_balancer': 0,
            'ivrVDN_AbandonedCalls': 0,
            'ivrVDN_Omilia': 0,
            'ivrVDN_Avaya': 0,
            'ivrAvaya_totalCalls': 0,
            'ivrAvaya_successfulCalls': 0,
            'ivrAvaya_breakedCalls': 0,
            'ivrAvaya_transferedCalls': 0,
            'ivrOmilia_totalCalls': 0,
            'ivrOmilia_farHupCalls': 0,
            'ivrOmilia_NearHupCalls': 0,
            'ivrOmilia_TeardownCalls': 0,
            'ivrOmilia_TransfersCalls': 0
        }
        
        # 0 элемент - список VDN, входящие вызовы
        tmpStrVDNs = list2str(nIVR_VDNs[0])
        query = getQuery_vdn(tmpStrVDNs, str(ndate))
        cursor.execute(query)

        for doper, incalls, outflowcalls in cursor:
            ivrContext['ivrVDN_IncomingCalls'] = int(incalls)

        # 1 элемент - список VDN, балансер
        tmpStrVDNs = list2str(nIVR_VDNs[1])
        query = getQuery_vdn(tmpStrVDNs, str(ndate))
        cursor.execute(query)

        for doper, incalls, outflowcalls in cursor:
            ivrContext['ivrVDN_IncomingCalls_balancer'] = int(incalls)

        # 2 элемент - VDN IVR Avaya
        tmpStrVDNs = list2str(nIVR_VDNs[2])
        query = getQuery_vdn(tmpStrVDNs, str(ndate))
        cursor.execute(query)

        for doper, incalls, outflowcalls in cursor:
            ivrContext['ivrVDN_Avaya'] = int(incalls)
        
        # Расчет потерянных вызовов
        ivrContext['ivrVDN_AbandonedCalls'] = ivrContext['ivrVDN_IncomingCalls'] - ivrContext['ivrVDN_IncomingCalls_balancer']
        
        cursor.close()
        conn.close()
    
    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}
    
    # Подключаемся к IVR
    try:
        pyodbc.pooling = False
        conn = pyodbc.connect(r'%s' % (connect_to_db_ivr_cfg))
    except Exception:
        return {'status': connection_error_to_db_cmsreport}

    try:
        cursor = conn.cursor()
        cursor.execute("select successful, breaked, transfered \
                          from cmsreport.dbo.ivr_day_history \
                         where calendar_day = '" + ndate + "'")

        for ivr_successful, ivr_breaked, ivr_transfered in cursor:
            ivrContext['ivrAvaya_successfulCalls'] = int(ivr_successful)
            ivrContext['ivrAvaya_breakedCalls'] = int(ivr_breaked)
            ivrContext['ivrAvaya_transferedCalls'] = int(ivr_transfered)
        
        ivrContext['ivrAvaya_totalCalls'] = ivrContext['ivrAvaya_successfulCalls'] + \
                                            ivrContext['ivrAvaya_breakedCalls'] + \
                                            ivrContext['ivrAvaya_transferedCalls']
        
        cursor.close()
        conn.close()

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}
    
    # Подключаемся к Omilia
    try:
        conn = mysql.connector.connect(**connect_to_db_omilia_cfg)
    except Exception:
        return {'status': connection_error_to_db_mysql}

    try:        
        cursor = conn.cursor()
        query = ("SELECT IFNULL(END_TYPE,'TEARDOWN'), count(1) as 'CNT' \
                  FROM diamant.DIALOGS \
                  WHERE APP_NAME in ('Halyk_Bank_Prod','Halyk_Pilot') \
                  AND STEPS_NUM !='0' \
                  AND DATE_FORMAT(DIALOG_DATE, '%Y-%m-%d') = DATE_FORMAT('" + ndate + "', '%Y-%m-%d') \
                  GROUP BY IFNULL(END_TYPE,'TEARDOWN')")
        cursor.execute(query)

        for end_type, count in cursor:
            if end_type == 'FAR_HUP':
                ivrContext['ivrOmilia_farHupCalls'] = int(count)
            elif end_type == 'NEAR_HUP':
                ivrContext['ivrOmilia_NearHupCalls'] = int(count)
            elif end_type == 'TEARDOWN':
                ivrContext['ivrOmilia_TeardownCalls'] = int(count)
            elif end_type == 'TRANSFER':
                ivrContext['ivrOmilia_TransfersCalls'] = int(count)
        
        ivrContext['ivrOmilia_totalCalls'] = ivrContext['ivrOmilia_farHupCalls'] + \
                                             ivrContext['ivrOmilia_NearHupCalls'] + \
                                             ivrContext['ivrOmilia_TeardownCalls'] + \
                                             ivrContext['ivrOmilia_TransfersCalls']
        cursor.close()
        conn.close()        

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}

    # Расчет потерянных вызовов
    ivrContext['ivrVDN_AbandonedCalls'] = ivrContext['ivrVDN_IncomingCalls'] - \
                                          ivrContext['ivrAvaya_totalCalls'] - \
                                          ivrContext['ivrOmilia_totalCalls']

    context['ivr'] = ivrContext

    # Собираем свод
    splitsLst = []
    for rec in nSplits_VDNs:
        splitsLst.append(rec[0])
    
    context['total'] = {
        'incomingCalls': 0,
        'abandonedCalls': 0,
        'tranFromOperator_inQueue': 0,
        'tranFromOmilia_inQueue': 0,
        'tranFromIVR_inQueue': 0,        
        'all_Outflowcalls': 0,
        'callsoffered': 0,
        'acdcalls': 0,
        'abncalls': 0,
        'acceptable': 0,
        'slvlabns': 0,
        'acd_do_40sec': 0,
        'acd_do_60sec': 0,
        'acd_do_2min': 0,
        'acd_do_5min': 0,
        'acd_do_10min': 0,
        'acd_ot_10min': 0,
        'abn_do_10sec': 0,
        'abn_do_15sec': 0,
        'abn_do_20sec': 0,
        'abn_do_30sec': 0,
        'abn_do_40sec': 0,
        'abn_do_60sec': 0,
        'abn_do_2min': 0,
        'abn_do_5min': 0,
        'abn_do_10min': 0,
        'abn_ot_10min': 0
    }

    for split in splitsLst:
        for key in context['total']:
            context['total'][key] += context[split][key]
    
    context['total']['service_level'] = get_prc(context['total']['acceptable'] + context['total']['slvlabns'], context['total']['callsoffered'])
    context['total']['prc_acdcalls'] = get_prc(context['total']['acdcalls'], context['total']['callsoffered'])
    context['total']['prc_abncalls'] = get_prc(context['total']['abncalls'], context['total']['callsoffered'])
    context['total']['incomingCalls'] += context['ivr']['ivrVDN_IncomingCalls']
    context['total']['ivrAvaya_processedCalls'] = context['ivr']['ivrAvaya_successfulCalls'] + \
                                                  context['ivr']['ivrAvaya_breakedCalls']
    context['total']['ivrOmilia_processedCalls'] = context['ivr']['ivrOmilia_farHupCalls'] + \
                                                   context['ivr']['ivrOmilia_NearHupCalls'] + \
                                                   context['ivr']['ivrOmilia_TeardownCalls']



    return {
        'status': successful,
        'result': context
    }