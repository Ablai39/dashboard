
import pyodbc
import requests
import xmltodict
import traceback
from dashboard.data import variables
from dashboard.data.global_functions import list2str, get_prc, get_prc_2, nvl, get_all_skills_id, get_asa_value, get_aat_value
from dashboard.data.operators import get_operators_list

def get_OnlineData_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'WALLBOARD_ONLINE', 'second', 15)

def get_OnlineData():
    
    context = {'data': {
        'missedCalls': {},
        'acd7min': {}
    }}

    from dashboard.data.index import get_OperatorsData_MemCache
    OperatorsList = get_OperatorsData_MemCache(None)
    
    # пропущенные вызовы
    # Поключаемся к CMS
    try:
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))
        connected_to_db_CMS = True
    except Exception:
        return {'status': variables.connection_error_to_db_cms}        
            
    try:
        contextMissedCalls = {}
        
        if OperatorsList['status'] != variables.successful:
            return {'status': OperatorsList['status']}
        else:
            depsOperators = OperatorsList['data']['deps']
            sectorsOperators = OperatorsList['data']['sectors']

        cursor = conn.cursor()
        
        query = "select a.row_time, s.item_name, s2.item_name, a.logid \
                    from agex a, synonyms s, synonyms s2 \
                    where a.logid = s.value \
                    and s.item_type = 'agname' \
                    and a.split = s2.value \
                    and s2.item_type = 'split' \
                    and row_date = date(sysdate) \
                    and extype = 28 \
                    and s2.item_name != 'Agent Direct Skill' \
                    order by row_time desc"
        cursor.execute(query)

        for time, operatorName, splitCode, logid in cursor:
            operatorID = logid.strip()

            if 'id' + operatorID not in contextMissedCalls:
                contextMissedCalls['id' + operatorID] = {
                    'id': operatorID,
                    'time': time,
                    'operatorName': operatorName.strip(),
                    'splitCode': splitCode.strip(),
                    'count': 1
                }

            else:
                contextMissedCalls['id' + operatorID]['count'] += 1

                if int(time) >  contextMissedCalls['id' + operatorID]['time']:
                    contextMissedCalls['id' + operatorID]['time'] = time
        
        cursor.close()
        conn.close()

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}

    try:
        for depCode in depsOperators:
            for agentContext in depsOperators[depCode]:
                operatorID = agentContext['id']

                if 'id' + operatorID in contextMissedCalls:
                    contextMissedCalls['id' + operatorID]['depCode'] = depCode

                    if depCode not in context['data']['missedCalls']:
                        context['data']['missedCalls'][depCode] = []
                    
                    context['data']['missedCalls'][depCode].append(contextMissedCalls['id' + operatorID])
        
        
        # ОПЕРАТОРЫ С ПРОДОЛЖИТЕЛЬНОСТЬЮ РАЗГОВОРА СВЫШЕ 7-ми мин
        contextACD = {}

        for sectorCode in sectorsOperators:
            if 'acd' in sectorsOperators[sectorCode]['ModeReasons']:
                for agentContext in sectorsOperators[sectorCode]['ModeReasons']['acd']:
                    depCode = agentContext['depCode']
                    
                    # 7 мин
                    if agentContext['duration'] >= 420:
                        
                        if depCode not in context['data']['acd7min']:
                            context['data']['acd7min'][depCode] = []

                        context['data']['acd7min'][depCode].append({
                            'id': agentContext['id'],
                            'name': agentContext['name'],
                            'duration': agentContext['duration']
                        })

        # Сортировка
        for depCode in context['data']['acd7min']:
            if len(context['data']['acd7min'][depCode]) > 1:
                oldList = context['data']['acd7min'][depCode]
                newList = sorted(oldList, key=lambda k: k['duration'], reverse=True)
                context['data']['acd7min'][depCode] = newList

        context['status'] = variables.successful
        return context

    except Exception:
        return {'status': traceback.format_exc()}

def get_best5_operators(p_upravlenie):

    response_data = {}
    pyodbc.pooling = False
    operators_list = get_operators_list()
    operators = operators_list[p_upravlenie]

    logid_list = []
    for value in operators:
        logid_list.append(value[1])
    
    logid_str = list2str(logid_list)

    try:
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))
    except Exception:
        response_data['status'] = variables.connection_error_to_db_cms

    try:
        cursor = conn.cursor()
        query = "select limit 4 starttime from hagent a where a.row_date = date(sysdate) group by starttime order by starttime desc"
        cursor.execute(query)

        starttime_lst = []
        for value in cursor:
            starttime_lst.append(value[0])
        
        starttime_str = list2str(starttime_lst)

        query = "select limit 5 b.item_name, a.logid, a.attrib_id, sum(a.acdcalls) \
                   from hagent a, \
                        synonyms b\
                  where a.row_date = date(sysdate) \
                    and b.item_type = 'agname' \
                    and a.logid = b.value\
                    and a.logid in (" + logid_str + ") \
                    and a.starttime in (" + starttime_str + ") \
                  group by b.item_name, a.logid, a.attrib_id \
                  having sum(a.acdcalls) > 0 \
                  order by sum(a.acdcalls) desc"
        cursor.execute(query)

        nList = []
        for name, logid, usrtab, cnt in cursor:
            nList.append({
                'name': name.strip(),
                'usrtab': int(usrtab.strip()),
                'cnt': int(cnt)
            })

        response_data = {
            'result': nList,
            'status': variables.successful
        }
 
    except Exception:
        response_data['status'] = traceback.format_exc()
    
    cursor.close()
    conn.close()
    return response_data