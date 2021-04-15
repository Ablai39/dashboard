import os
import time
import pyodbc
import pyexcel
import requests
import xmltodict
import traceback
from datetime import datetime
from dashboard.data import variables

def getOperatorsList_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'OPERATORS_CMS_DATA', 'minute', 5)

def getWS_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'OPERATORS_WS', 'second', 15)

def getWS():
    
    tempLst = []
    context = {
        'data': []
    }
    operatorsList = getOperatorsList_MemCache(None)

    if operatorsList['status'] != variables.successful:
        return {'status': operatorsList['status']}
    else:
        operatorsList = operatorsList['data']

    operatorsIDList = operatorsList['lists']
    operatorsData = operatorsList['operators']

    breakTypes = {
        'id0': 'system',
        'id1': 'break',
        'id2': 'lunch',
        'id3': 'training',
        'id4': 'supervisorCons',
        'id5': 'technicalBreak',
        'id6': 'supervisorWork',
        'id7': 'break', #coffeeBreak
        'id8': 'manualDial',
        'id9': 'break',
        'id10': 'supervisorWork'
    }

    for index, listNumber in enumerate(operatorsIDList):
        if len(operatorsIDList[listNumber]) > 0:
            if index > 0:
                time.sleep(0.2)
            
            for idx, values in enumerate(operatorsIDList[listNumber]):
                if idx == 0:
                    idRange = str(values)
                else:
                    idRange += ',' + str(values)
            
            # Подключаемся к WEB сервису по спискам Lists
            try:
                response = requests.get(variables.p_url_agents + idRange, auth=variables.auth_values)
                response.raise_for_status()
            except Exception:
                return {'status': variables.connection_error_to_ws + ': ' + variables.p_url_agents}
            
            if response.status_code != 200:
                if response.status_code == 401:
                    return {'status': '401 - Ошибка авторизации. URL = (' + variables.p_url + ')'}
                elif response.status_code == 404:
                    return {'status': '404 - Сервис не найден. URL = (' + variables.p_url + ')'}
                else:
                    return {'status': 'status_code = ' + str(response.status_code)}
            
            try:
                nDict = xmltodict.parse(response.content)

                if nDict['AgentDocument']['agents'] is None:
                    continue
                nDict = nDict['AgentDocument']['agents']['agent']

                # если в выборке только запись по одному оператору
                if type(nDict) != list:
                    nDict = [nDict,]
                
                for data in nDict:
                    agentID = str(data['@no'])

                    # защита от дублей
                    if agentID not in tempLst:
                        tempLst.append(agentID)
                    else:
                        continue

                    splitsLVL_1 = []
                    splitsLVL_2 = []
                    splitsLVL_3 = []
                    splitsLVL_4 = []
                    splitsLVL_5 = []
                    splitsLVL_Other = []
                    agentContext = {}

                    data = data['now']

                    if 'id'+agentID in operatorsData:
                        name = operatorsData['id'+agentID]['name']
                    else:
                        name = '-'

                    # номер телефона
                    if 'ext' in data:
                        phoneNum = data['ext']

                        if phoneNum is None:
                            phoneNum = '-'
                    else:
                        phoneNum = '-'
                    
                    # текущий навык
                    if 'workskill' in data:
                        workSplit = data['workskill']

                        if workSplit is None:
                            workSplit = '-'
                    else:
                        workSplit = '-'
                    
                    # текущее состояние
                    if 'mode' in data:
                        if isinstance(data['mode'], str):
                            mode = data['mode']
                            modeReason = '-'
                        elif isinstance(data['mode'], dict):
                            mode = data['mode']['#text']
                            
                            if len(data['mode']['@reason']) == 0:
                                modeReason = '-'
                            else:
                                modeReasonID = str(data['mode']['@reason'])
                                modeReason = breakTypes['id' + modeReasonID]
                        else:
                            mode = '-'
                            modeReason = '-'
                    else:
                        mode = '-'
                        modeReason = '-'
                    
                    # направление вызова
                    if 'direction' in data:
                        direction = data['direction']

                        if direction is None:
                            direction = '-'
                    else:
                        direction = '-'

                    # продолжительность
                    if 'duration' in data:
                        duration = data['duration']
                    else:
                        duration = '-'
                    
                    # навыки оператора
                    if 'skill' in data:
                        splits = data['skill']
                    else:
                        splits = '-'
                    
                    if splits != '-':
                        if type(splits) != list:
                            splits = [splits,]
                    
                        for split in splits:
                            if split['@lvl'] == '1':
                                splitsLVL_1.append(split['@no'])
                            elif split['@lvl'] == '2':
                                splitsLVL_2.append(split['@no'])
                            elif split['@lvl'] == '3':
                                splitsLVL_3.append(split['@no'])
                            elif split['@lvl'] == '4':
                                splitsLVL_4.append(split['@no'])
                            elif split['@lvl'] == '5':
                                splitsLVL_5.append(split['@no'])
                            else:
                                splitsLVL_Other.append(split['@no'])

                    agentContext = {
                        'agentID': agentID,
                        'name': name,
                        'phoneNum': phoneNum,
                        'workSplit': workSplit,
                        'mode': mode,
                        'modeReason': modeReason,
                        'direction': direction,
                        'duration': duration,
                        'splitsLVL_1': splitsLVL_1,
                        'splitsLVL_2': splitsLVL_2,
                        'splitsLVL_3': splitsLVL_3,
                        'splitsLVL_4': splitsLVL_4,
                        'splitsLVL_5': splitsLVL_5,
                        'splitsLVL_Other': splitsLVL_Other
                    }

                    context['data'].append(agentContext)

            except Exception:
                return {'status': traceback.format_exc()}
    
    context['status'] = variables.successful
    return context

def getOperatorsList():
    pyodbc.pooling = False

    # Подключаемся к базе CMS
    try:
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))
    except Exception:
        return {'status': variables.connection_error_to_db_cms}

    try:
        nList = []
        allList = []
        context = {
            'data': {
                'operators': {},
                'lists': {}
            }
        }
        lists = {}
        
        cursor=conn.cursor()
        query = "select item_name, value from synonyms \
                where item_type = 'agname' \
                and item_name not in ('test TSI 1','Test TSI 2','Vadim','test_Oleg','test_Terrasoft','Salavat','Oleg','Agent_for_learning') \
                and (value like '78%' or value like '76%')\
                order by value"
        cursor.execute(query)

        i = 0
        for name, user_id in cursor:
            i += 1

            id = user_id.strip() 

            context['data']['operators']['id'+id] = {
                'id': id,
                'name': name.strip()
            }

            if i <= 250:
                if 'list1' not in lists:
                    lists['list1'] = []
                lists['list1'].append(id)
                
            elif i <= 500:
                if 'list2' not in lists:
                    lists['list2'] = []
                lists['list2'].append(id)

            elif i <= 750:
                if 'list3' not in lists:
                    lists['list3'] = []
                lists['list3'].append(id)

            elif i <= 1000:
                if 'list4' not in lists:
                    lists['list4'] = []
                lists['list4'].append(id)

            elif i <= 1250:
                if 'list5' not in lists:
                    lists['list5'] = []
                lists['list5'].append(id)

            else:
                if 'list6' not in lists:
                    lists['list6'] = []
                lists['list6'].append(id)
        
        context['data']['lists'] = lists
        context['status'] = variables.successful
        
        cursor.close()
        conn.close()
        return context
    
    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}

def importOperatorsFromXLS(fileName):

    # create table agents (rec_num SERIAL PRIMARY KEY, 
	# 			 code integer,
    #            phone integer,
	# 			 arcfl integer default 0, 
	# 			 tab_number integer, 
	# 			 name varchar(30), 
	# 			 dep_code varchar(10), 
	# 			 dep_longname varchar(60),
	# 			 correctdt DATETIME YEAR TO SECOND)

    # Подключаемся к базе CMS
    try:
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))
        # conn.setencoding(encoding='CP1251')
        conn.autocommit = True
    except Exception:
        errTxt = traceback.format_exc().splitlines()        
        strErrTxt = errTxt[1].strip() + '->' + errTxt[2].strip() + '->' + errTxt[3].strip()
        print(strErrTxt)
        
    try:
        os.chdir(r"c:/import")
        print(os.getcwd())
        array = pyexcel.get_array(file_name=fileName)

        start = datetime.today()
        print('---> Started on ' + start.strftime('%Y-%m-%d %H:%M:%S'))
        
        cursor=conn.cursor()

        i = 0
        for index, values in enumerate(array):
            if index == 0:
                continue
            i += 1
            sysdate = datetime.today()
            depLongname = (values[1]).strip()
            tabNum = str(values[2])
            name = (values[3]).strip()
            phone = str(values[4])
            code = str(values[5])
            depCode = ''
            
            if depLongname == 'Управление Soft Collection':
                depCode = 'usc'
            elif depLongname == 'Управление поддержки розничных клиентов':
                depCode = 'uprk'
            elif depLongname == 'Региональное управление банковского сервиса':
                depCode = 'rubs'
            elif depLongname == 'Управление поддержки интернет банкинга':
                depCode = 'upib'

            query = "INSERT INTO AGENTS (code, phone, tab_number, dep_code, correctdt) \
                        VALUES ('"+code+"','"+phone+"','"+tabNum+"','"+depCode+"',sysdate)"
            cursor.execute(query)
        
        end = datetime.today()
        print('---> Ended on ' + end.strftime('%Y-%m-%d %H:%M:%S'))
        print('---> Inserted ' + str(i) + ' rows') 
                
    except Exception:
        errTxt = traceback.format_exc().splitlines()
        strErrTxt = errTxt[1].strip() + '->' + errTxt[2].strip() + '->' + errTxt[3].strip()
        print(strErrTxt)

    cursor.close()
    conn.close()