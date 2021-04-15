import pyodbc
import requests
import xmltodict
import mysql.connector
from datetime import datetime, date, timedelta
from django.views.decorators.csrf import csrf_exempt
from dashboard.data.global_functions import nvl, get_prc, get_prc_2, get_all_skills_id, list2str
from dashboard.data.global_functions import get_asa_value, get_acr_value, get_aat_value, json_serializer, json_deserializer, needUpdate
from dashboard.data import variables
import traceback
import time
from pymemcache.client.base import Client
from dashboard.data.config import sectorsDict, splitItemsDict, depsDict, widgetOperatorsItemsDict
from dashboard.data import splitsData
from dashboard.data import operatorsData
from dashboard.data.variables import host
from dashboard.data.skill_groups import all_depart_skills_str

def get_SplitsData_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'INDEX_ONLINE', 'second', 10)

def get_OperatorsData_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'INDEX_ONLINE_OPERATORS', 'second', 15)

def get_SplitsData():
    sysdate = datetime.now()
    context = {
        'day': {'total':{}},
        'month': {'total':{}},
        'month_start_date': '01.' + sysdate.strftime('%m.%Y')
    }

    try:
        sysdate = datetime.now()

        dataWS = splitsData.getSplit_WS()
        if dataWS['status'] != variables.successful:
            return dataWS
        else:
            dataWS = dataWS['data']
        
        dataCMS_Day = splitsData.getSplitCMS_Day_MemCache(None)
        if dataCMS_Day['status'] != variables.successful:
            return dataCMS_Day
        else:
            dataCMS_Day = dataCMS_Day['data']
        
        if int(sysdate.strftime('%d')) != 1:
            dataCMS_Month = splitsData.getSplitCMS_Month_MemCache(None)
            if dataCMS_Month['status'] != variables.successful:
                return dataCMS_Month
            else:
                dataCMS_Month = dataCMS_Month['data']

        for sector in sectorsDict:
            if sectorsDict[sector]['archive'] == 'Y':
                continue

            if sectorsDict[sector]['splitsStr'] == None:
                continue

            if sector not in context['day']:
                context['day'][sector] = {}
            
            if 'longname' not in context['day'][sector]:
                context['day'][sector]['longname'] = sectorsDict[sector]['longname']
            
            if sector not in context['month']:
                context['month'][sector] = {}
            
            for splitItem in splitItemsDict:
                if splitItem in dataWS[sector]:
                    valueWS = dataWS[sector][splitItem]
                else:
                    valueWS = 0
                
                if splitItem in dataCMS_Day[sector]:
                    valueDay = dataCMS_Day[sector][splitItem]
                else:
                    valueDay = 0

                context['day'][sector][splitItem] = valueWS + valueDay

                if splitItem not in context['day']['total']:
                    context['day']['total'][splitItem] = 0
                
                if splitItem == 'oldest':
                    if context['day'][sector][splitItem] > context['day']['total'][splitItem]:
                        context['day']['total'][splitItem] = context['day'][sector][splitItem]
                else:
                    context['day']['total'][splitItem] += context['day'][sector][splitItem]
                
                if splitItemsDict[splitItem]['calcMonth'] == 'Y':
                    if int(sysdate.strftime('%d')) == 1:
                        context['month'][sector][splitItem] = context['day'][sector][splitItem]
                        context['month']['total'][splitItem] = context['day']['total'][splitItem]
                    else:
                        if splitItemsDict[splitItem]['calcMonth'] == 'Y':
                            if splitItem in dataCMS_Month[sector]:
                                valueMonth = dataCMS_Month[sector][splitItem]
                            else:
                                valueMonth = 0

                            context['month'][sector][splitItem] = context['day'][sector][splitItem] + valueMonth
                    
                            if splitItem not in context['month']['total']:
                                context['month']['total'][splitItem] = 0
                    
                            context['month']['total'][splitItem] += context['month'][sector][splitItem]
                
            # Если включен Call Back Assists
            if sectorsDict[sector]['enableCallBack'] == 'Y':
                context['day'][sector]['cba'] = dataWS[sector]['cba']
        
        for value in ['day','month']:
            for sector in context[value]:
                try:
                    sl = get_prc(context[value][sector]['acceptable'] + context[value][sector]['slvlabns'], context[value][sector]['callsoffered'])
                    context[value][sector]['sl'] = sl
                
                    if value == 'day':
                        asa = get_asa_value(context[value][sector]['anstime'], context[value][sector]['acdcalls'])
                        context[value][sector]['asa'] = asa

                        att = get_aat_value(context[value][sector]['acdtime'], context[value][sector]['acdcalls'])
                        context[value][sector]['att'] = att
                except Exception:
                    return {
                        'status': traceback.format_exc(),
                        'sector': sector,
                        'value': value
                    }

        return {
            'data': context,
            'status': variables.successful
        }

    except Exception:
        return {'status': traceback.format_exc()}

def get_OperatorsData():
    try:
        sectorsContext = {}
        depsContext = {}
        data = operatorsData.getWS_MemCache(None)

        if data['status'] != variables.successful:
            return data
        else:
            data = data['data']

        # необходимо для обнуления данных на фронте
        for sector in sectorsDict:
            if 'archive' in sectorsDict[sector]:
                if sectorsDict[sector]['archive'] == 'Y':
                    continue

            sectorsContext[sector] = {
                'longname': sectorsDict[sector]['longname'],
                'ModeReasons': {}
            }
            
            for item in widgetOperatorsItemsDict:
                if widgetOperatorsItemsDict[item]['isAgentStatus'] == 'Y':
                    sectorsContext[sector]['ModeReasons'][item] = []

            if sectorsDict[sector]['enableCallBack'] == 'Y':
                sectorsContext[sector]['cba'] = {}
                sectorsContext[sector]['cba']['ModeReasons'] = {}

                for item in widgetOperatorsItemsDict:
                    if widgetOperatorsItemsDict[item]['isAgentStatus'] == 'Y':
                        sectorsContext[sector]['cba']['ModeReasons'][item] = []

        for item in widgetOperatorsItemsDict:
            if widgetOperatorsItemsDict[item]['isAgentStatus'] == 'Y':
                sectorsContext['unknown']['ModeReasons'][item] = []

        # сбор данных по оператору
        for index, agent in enumerate(data):
            agentContext = {}
            agentSectors = []
            agentDepCodes = []

            agentMode = agent['mode']
            agentSector = 'unknown'
            agentDepCode = 'unknown'

            # Определяем управление
            for splits in ['splitsLVL_1','splitsLVL_2','splitsLVL_3','splitsLVL_4','splitsLVL_5','splitsLVL_Other']:
                if len(agent[splits]) == 0:
                    continue

                for depCode in depsDict:
                    for split in agent[splits]:
                        if split in depsDict[depCode]['directSplitsLst']:
                            if depCode not in agentDepCodes:
                                agentDepCodes.append(depCode)
                
                if len(agentDepCodes) > 0:
                    break
            
            if len(agentDepCodes) > 0:
                agentDepCode = agentDepCodes[0]

            # Если состояние равно "Идет разговор", то берем его реальную скилл группу, если она есть
            if agentMode in ['ACD','DACD']:
                for sector in sectorsDict:
                    if 'archive' in sectorsDict[sector]:
                        if sectorsDict[sector]['archive'] == 'Y':
                            continue

                    if agent['workSplit'] in sectorsDict[sector]['splitsLst']:
                        if sector not in agentSectors:
                            agentSectors.append(sector)
                    
                    if sectorsDict[sector]['enableCallBack'] == 'Y':
                        if agent['workSplit'] in sectorsDict[sector]['splits_cbaLst']:
                            if sector + '_cba' not in agentSectors:
                                agentSectors.append(sector + '_cba')
            
            # Иначе смотрим на навыки оператора
            if len(agentSectors) == 0:
                for splits in ['splitsLVL_1','splitsLVL_2','splitsLVL_3','splitsLVL_4','splitsLVL_5','splitsLVL_Other']:
                    if len(agent[splits]) == 0:
                        continue
                
                    for sector in sectorsDict:
                        if 'archive' in sectorsDict[sector]:
                            if sectorsDict[sector]['archive'] == 'Y':
                                continue

                        for split in agent[splits]:
                            if split in sectorsDict[sector]['splitsLst']:
                                if sector not in agentSectors:
                                    agentSectors.append(sector)
                            
                            if sectorsDict[sector]['enableCallBack'] == 'Y':
                                if split in sectorsDict[sector]['splits_cbaLst']:
                                    if sector + '_cba' not in agentSectors:
                                        agentSectors.append(sector + '_cba')
                    
                    if len(agentSectors) > 0:
                        break

            if len(agentSectors) == 0:
                if agentDepCode != 'unknown':
                    if depsDict[agentDepCode]['mainSector'] != None:
                        agentSector = depsDict[agentDepCode]['mainSector']

            if len(agentSectors) == 1:
                agentSector = agentSectors[0]
            
            elif len(agentSectors) > 1:
                if agentDepCode == 'unknown':
                    agentSector = agentSectors[0]
                
                else:
                    for depCode in depsDict:
                        if agentDepCode == depCode:
                            if depsDict[depCode]['mainSector'] == None:
                                agentSector = agentSectors[0]
                            else:
                                if depsDict[depCode]['mainSector'] in agentSectors:
                                    agentSector = depsDict[depCode]['mainSector']
                                    break
                                else:
                                    agentSector = agentSectors[0]
                        
            if agentMode in ['AVAIL']:
                agentModeReason = 'available'

            elif agentMode in ['AUX']:
                if agent['modeReason'] == '-':
                    agentModeReason = 'break'
                else:
                    agentModeReason = agent['modeReason']
            
            elif agentMode in ['ACD','DACD','RINGING']:
                agentModeReason = 'acd'
            
            elif agentMode in ['ACW','DACW']:
                agentModeReason = 'acw'
            
            else:
                agentModeReason = 'system'

            if '_cba' in agentSector:
                mainSector = agentSector[0:len(agentSector)-4]
                sectorsContext[mainSector]['cba']['ModeReasons'][agentModeReason].append({
                    'id': agent['agentID'],
                    'name': agent['name'],
                    'depCode': agentDepCode,
                    'duration': int(agent['duration'])
                })

                sectorLongname = sectorsDict[mainSector]['longname']
            
            else:
                sectorsContext[agentSector]['ModeReasons'][agentModeReason].append({
                    'id': agent['agentID'],
                    'name': agent['name'],
                    'depCode': agentDepCode,
                    'duration': int(agent['duration'])
                })

                sectorLongname = sectorsDict[agentSector]['longname']

            # Сбор операторов в разрезе управлений
            if agentDepCode not in depsContext:
                 depsContext[agentDepCode] = []

            depsContext[agentDepCode].append({
                'id': agent['agentID'],
                'name': agent['name'],
                'sectorLongname': sectorLongname,
                'modeReason': agentModeReason,
                'modeReasonLongname': widgetOperatorsItemsDict[agentModeReason]['agentAction'],
                'duration': int(agent['duration'])
            })

        # Подсчет операторов
        for sector in sectorsContext:
            totalAgents = 0
            totalAgents_CC = 0
            totalAgents_Filial = 0
            totalAgents_Unknown = 0

            for agentModeReason in sectorsContext[sector]['ModeReasons']:
                totalAgents += len(sectorsContext[sector]['ModeReasons'][agentModeReason])
                
                for agent in sectorsContext[sector]['ModeReasons'][agentModeReason]:
                    notFound = True

                    for depCode in depsDict:
                        if agent['depCode'] == depCode:
                            notFound = False
                            if depsDict[depCode]['highDepCode'] == 'ContactCenter':
                                totalAgents_CC += 1

                            elif depsDict[depCode]['highDepCode'] == 'Bank':
                                totalAgents_Filial += 1
                            else:
                                totalAgents_Unknown += 1
                            break
                
                    if notFound:
                        totalAgents_Unknown += 1
            
            if sectorsDict[sector]['enableCallBack'] == 'Y':
                for agentModeReason in sectorsContext[sector]['cba']['ModeReasons']:
                    totalAgents += len(sectorsContext[sector]['cba']['ModeReasons'][agentModeReason])
                    
                    for agent in sectorsContext[sector]['cba']['ModeReasons'][agentModeReason]:
                        notFound = True

                        for depCode in depsDict:
                            if agent['depCode'] == depCode:
                                notFound = False
                                if depsDict[depCode]['highDepCode'] == 'ContactCenter':
                                    totalAgents_CC += 1

                                elif depsDict[depCode]['highDepCode'] == 'Bank':
                                    totalAgents_Filial += 1
                                else:
                                    totalAgents_Unknown += 1
                                break
                    
                        if notFound:
                            totalAgents_Unknown += 1

            sectorsContext[sector]['totalAgents'] = totalAgents
            sectorsContext[sector]['totalAgents_CC'] = totalAgents_CC
            sectorsContext[sector]['totalAgents_Filial'] = totalAgents_Filial
            sectorsContext[sector]['totalAgents_Unknown'] = totalAgents_Unknown
            
        # Сортировка
        for sector in sectorsContext:
            if 'ModeReasons' in sectorsContext[sector]:
                for agentModeReason in sectorsContext[sector]['ModeReasons']:
                    if len(sectorsContext[sector]['ModeReasons'][agentModeReason]) > 1:
                        oldList = sectorsContext[sector]['ModeReasons'][agentModeReason]
                        newList = sorted(oldList, key=lambda k: k['duration'], reverse=True)
                        sectorsContext[sector]['ModeReasons'][agentModeReason] = newList
        
        for depCode in depsContext:
            oldList = depsContext[depCode]
            newList = sorted(oldList, key=lambda k: k['duration'], reverse=True)
            depsContext[depCode] = newList

        return {
            'status': variables.successful,
            'data': {
                'sectors': sectorsContext,
                'deps': depsContext
            }
        }
                
    except Exception:
        return {'status': traceback.format_exc(),
            'agentSector': agentSector,
            'agentModeReason': agentModeReason,
            'agetnID': agent['agentID']}

def get_OtherParametrsData():
    # Подключаемся к CMS
    try:
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))
    except Exception:
        return {'status': variables.connection_error_to_db_cms}
    
    try:    
        cursor = conn.cursor()

        # Считаем общее количество поступивщих звонков в ВКЦ
        query = "select 1, SUM(incalls) from hvdn \
                 where row_date = date(sysdate) \
                 and vdn in (" + variables.cc_incalls_str + ")"
        cursor.execute(query)

        for value in cursor:
            incalls = int(nvl(value[1],0))
        
        # Считаем общее количество поступивщих звонков в ВКЦ по скиллам
        query = "select 1, SUM(CALLSOFFERED) from hsplit \
                  where split in (" + all_depart_skills_str + ") and ROW_DATE = date(sysdate)"
        cursor.execute(query)

        for value in cursor:
            callsoffered = int(nvl(value[1],0))

        # FCR. Счиатем общее количество повторяющихся звонков
        query = "select 1, count(1) \
                   from (select calling_pty, count(1) \
                           from call_rec \
                          where row_date = date(sysdate) \
                            and len(calling_pty) > 7 \
                            and firstvdn != '79599' \
                          group by calling_pty \
                         having count(1) > 1)"
        cursor.execute(query)
        
        for value in cursor:            
            double_rings = int(value[1])
        
        # Считаем общий ACR
        query = "select lastdigits, count(1) \
                   from call_rec \
                  where row_date = date(sysdate) \
                    and dialed_num = '79599' \
                    and lastdigits in ('1','2','3','4','5') \
                    and len(calling_pty) > 7 \
                  group by lastdigits" 
        cursor.execute(query)

        summa = 0
        summa_count = 0
        for osenka, count in cursor:
            summa += int(osenka) * int(count)
            summa_count += int(count)
        
        # Количество оцененных вызовов
        query = "select 1, count(1) \
                   from (select callid \
                           from call_rec \
                          where row_date = date(sysdate) \
                            and dialed_num = '79599' \
                            and lastdigits in ('1','2','3','4','5') \
                            and len(calling_pty) > 7 \
                          group by callid)"
        cursor.execute(query)

        for value in cursor:            
            rated_calls = int(value[1])

        response_data = {
            'data': {
                'acr': {
                    'all': get_acr_value(summa, summa_count)
                },
                'fcr': get_prc(incalls - double_rings, incalls),
                'incalls': incalls,
                'rated_calls': rated_calls,
                'rated_calls_prc': get_prc_2(rated_calls, callsoffered),
                'callsoffered': callsoffered,
                'double_rings': double_rings,
            }
        }

        # Считаем ACR в разрезе скилл групп
        query = "select sum(case when firstvdn = 79599 then 0 else dispsplit end), \
                        sum(case when firstvdn = 79599 then to_number(lastdigits) else 0 end) \
                   from call_rec a \
                  where row_date = date(sysdate) \
                    and len(calling_pty) > 7 \
                    and callid in (select callid from call_rec \
                                    where row_date = date(sysdate) \
                                      and dispsplit is not null \
                                      and len(calling_pty) > 7 \
                                    group by callid) \
                    and callid in (select callid from call_rec \
                                    where row_date = date(sysdate) \
                                      and dialed_num = '79599' \
                                      and lastdigits in ('1','2','3','4','5') \
                                      and len(calling_pty) > 7 \
                                    group by callid) \
                    group by callid"
        cursor.execute(query)
        
        context = {}
        for sector in sectorsDict:
            if sectorsDict[sector]['archive'] == 'Y':
                continue
            
            if len(sectorsDict[sector]['splitsLst']) == 0:
                continue
            
            context[sector] = {
                'sum': 0,
                'count': 0,
                'splitsLst': sectorsDict[sector]['splitsLst']
            }

        for value in cursor:
            split = str(value[0])
            lastdigits = int(value[1])
            
            for sector in context:
                if split in context[sector]['splitsLst']:
                    context[sector]['sum'] += lastdigits
                    context[sector]['count'] += 1
        
        for sector in context: 
            response_data['data']['acr'][sector] = get_acr_value(context[sector]['sum'], context[sector]['count'])
            
        cursor.close()
        conn.close()

    except Exception:
        cursor.close()
        conn.close()        
        return {'status': traceback.format_exc()}        

    response_data['status'] = variables.successful
    return response_data

def get_GraphicData ():
    timeLst = []
    hoursKeys = []
    hoursLabel = []
    sysdate = datetime.now()
    response_data = {'data': {}}

    # Если 12 ночи, то выдаем данные за предыдущий день
    if int(sysdate.strftime("%H")) == 0:
        lastDay = True
        date = sysdate - timedelta(days=1)
        dateStr = date.strftime("%Y-%m-%d")
    # иначе, за сегодня
    else:
        lastDay = False
        dateStr = sysdate.strftime("%Y-%m-%d")

    starttime = datetime.strptime(dateStr + ' 01:00:00', '%Y-%m-%d %H:%M:%S')
    timeLst.append(starttime)

    for value in range(0,23):
        nextime = starttime + timedelta(hours=1)

        if lastDay:
            if starttime.strftime("%H%M") == '2300':
                nextime = datetime.strptime(dateStr + ' 23:59:00', '%Y-%m-%d %H:%M:%S')
        else:
            if int(nextime.strftime("%H")) > int(sysdate.strftime("%H")):
                break
            if starttime.strftime("%H%M") == '2300':
                break

        timeLst.append(nextime)
        starttime = nextime

    try:
        pyodbc.pooling = False
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))
    except Exception:
        return {'status': variables.connection_error_to_db_cms}
        
    try:
        cursor = conn.cursor()
        for date in timeLst:
            hoursKeys.append('hour_' + str(date.strftime("%H")))
            
            if str(date.strftime("%H%M")) == '2359':
                hourLabel = '00:00'
            else:
                hourLabel = str(date.strftime("%H:%M"))

            hoursLabel.append(hourLabel)

            endTimeStr = str(int(date.strftime("%H%M")))
            startTimeDate = date - timedelta(hours=1)
            startTimeStr = str(int(startTimeDate.strftime("%H%M")))

            for sector in sectorsDict:
                if 'archive' in sectorsDict[sector]:
                    if sectorsDict[sector]['archive'] == 'Y':
                        continue

                splits = sectorsDict[sector]['splitsStr']

                if sectorsDict[sector]['enableIndexGraphic'] == 'N':
                    continue

                query = "select count(logid) \
                           from (select logid from hagent \
                                  where row_date =  to_date('" + dateStr + "', '%Y-%m-%d') \
                                    and split in (" + splits + ") \
                                    and starttime >= " + startTimeStr + " \
                                    and starttime < " + endTimeStr + "\
                                    and ringcalls > 0 \
                                    group by logid)"
                
                cursor.execute(query)
                result=cursor.fetchone()
                operatorsCount = int(result[0])

                query = "select sum(CALLSOFFERED),  \
                                sum(ACCEPTABLE),  \
                                sum(SLVLABNS), \
                                sum(ACDCALLS), \
                                sum(ABNCALLS), \
                                sum(OUTFLOWCALLS) \
                           from hsplit \
                          where row_date =  to_date('" + dateStr + "', '%Y-%m-%d') \
                            and split in (" + splits + ") \
                            and starttime >= " + startTimeStr + " \
                            and starttime < " + endTimeStr

                cursor.execute(query)

                for p_callsoffered, p_acceptable, p_slvlabns, p_acdcalls, p_abncalls, p_outflowcalls in cursor:
                    nPrc = get_prc((int(p_acceptable) + int(p_slvlabns)), int(p_callsoffered))

                    if p_callsoffered == 0:
                        nPrc = 100

                    if sector not in response_data['data']:
                        response_data['data'][sector] = {}
                    
                    if 'hours' not in response_data['data'][sector]:
                        response_data['data'][sector]['hours'] = {}
                    
                    response_data['data'][sector]['hours']['hour_' + str(date.strftime("%H"))] = {
                        'time': str(date.strftime("%H:%M")),
                        'sl': nPrc,
                        'callsoffered': int(p_callsoffered),
                        'acceptable': int(p_acceptable),
                        'slvlabns': int(p_slvlabns),
                        'acdcalls': int(p_acdcalls),
                        'abncalls': int(p_abncalls),
                        'outflowcalls': int(p_outflowcalls),
                        'operators_count': operatorsCount
                    }
                
                response_data['data'][sector]['longname'] = sectorsDict[sector]['longname']
                response_data['data'][sector]['graphicLineColor'] = sectorsDict[sector]['graphicLineColor']

        cursor.close()
        conn.close()
        response_data['hours_keys'] = hoursKeys
        response_data['hours'] = hoursLabel
        response_data['status'] = variables.successful
        return response_data

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}