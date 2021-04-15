
import pyodbc
import requests
import traceback
import xmltodict
from datetime import datetime
from dashboard.data import variables
from dashboard.data.global_functions import nvl
from dashboard.data.config import sectorsDict, splitItemsDict

def getWS_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'SPLITS_WS', 'second', 10)

def getSplitCMS_Day_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'SPLITS_CMS_DAY_DATA', 'minute', 1)

def getSplitCMS_Month_MemCache(request):
    from dashboard.data.check_memcache import getMemCache
    return getMemCache(request, 'SPLITS_CMS_MONTH_DATA', 'day', 1)

def getWS():
    splitslst = []

    # Подключаемся к сервису
    try:
        response = requests.get(variables.p_url, auth=variables.auth_values)
        response.raise_for_status()        
    except Exception:
        return {'status': variables.connection_error_to_ws + ': ' + variables.p_url}
        
    if response.status_code == 200:
        try:
            nDict = xmltodict.parse(response.content)
            nDict = nDict['VUDocument']['split']

            for data in nDict:
                splitslst.append({
                    'split': int(data['@no']),
                    'inqueue': int(data['now']['inqueue']),
                    'anstime': int(data['now']['anstime']),
                    'acdtime': int(data['now']['acdtime']),                            
                    'oldest': int(data['now']['oldest']),
                    'callsoffered': int(data['now']['callsoffered']),
                    'acdcalls': int(data['now']['acdcalls']),
                    'abncalls': int(data['now']['abncalls']),
                    'acceptable': int(data['now']['acceptable']),
                    'slvlabns': int(data['now']['slvlabns'])
                })
            
            return {
                'data': splitslst,
                'status': variables.successful
            }
                
        except Exception:
            return {'status': traceback.format_exc()}

    elif response.status_code == 401:
        return {'status': '401 - Ошибка авторизации'}
        
    elif response.status_code == 404:
        return {'status': '404 - Сервис не найден (' + variables.p_url + ')'}

    else:
        return {'status': 'status_code = ' + str(response.status_code)}

def getSplit_WS():
    context = {}
    dataWS = getWS_MemCache(None)

    if dataWS['status'] != variables.successful:
        return dataWS
    else:
        dataWS = dataWS['data']

    try:
        for sector in sectorsDict:
            if 'archive' in sectorsDict[sector]:
                if sectorsDict[sector]['archive'] == 'Y':
                    continue

            splitsLst = sectorsDict[sector]['splitsLst']

            if sector not in context:
                context[sector] = {}

            if sectorsDict[sector]['enableCallBack'] == 'Y':
                splitsCbaLst = sectorsDict[sector]['splits_cbaLst']
                context[sector]['cba'] = {}

            for splitItem in splitItemsDict:
                context[sector][splitItem] = 0

                if sectorsDict[sector]['enableCallBack'] == 'Y':
                    if splitItemsDict[splitItem]['useCBA'] == 'Y':
                        context[sector]['cba'][splitItem] = 0
          
            for value in dataWS:
                if str(value['split']) in splitsLst:
                    for splitItem in splitItemsDict:
                        if splitItem in value:
                            if splitItem == 'oldest':
                                if context[sector][splitItem] < value[splitItem]:
                                    context[sector][splitItem] = value[splitItem]
                            else:
                                context[sector][splitItem] += value[splitItem]
                
                if sectorsDict[sector]['enableCallBack'] == 'Y':
                    if str(value['split']) in splitsCbaLst:
                        for splitItem in splitItemsDict:
                            if splitItemsDict[splitItem]['useCBA'] == 'Y':
                                if splitItem == 'oldest':
                                    if context[sector]['cba'][splitItem] < value[splitItem]:
                                        context[sector]['cba'][splitItem] = value[splitItem]
                                else:
                                    context[sector]['cba'][splitItem] += value[splitItem]
        
        return {
            'data': context,
            'status': variables.successful
        }
    
    except Exception:
        return {'status': traceback.format_exc()}

def getSplit_CMS_Day():
    context = {}
    pyodbc.pooling = False
    sysdate = datetime.now()
    # Подключаемся к базе данных CMS
    try:
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))            
    except Exception:
        return {'status': variables.connection_error_to_db_cms}

    try:
        for sector in sectorsDict:
            if 'archive' in sectorsDict[sector]:
                if sectorsDict[sector]['archive'] == 'Y':
                    continue

            if sectorsDict[sector]['splitsStr'] == None:
                continue

            context[sector] = {}

            cursor = conn.cursor()
            query = "select sum(CALLSOFFERED), \
                            sum(ACDCALLS), \
                            sum(OUTFLOWCALLS), \
                            sum(ABNCALLS)+sum(BUSYCALLS)+sum(DISCCALLS), \
                            sum(ACCEPTABLE), \
                            sum(SLVLABNS), \
                            sum(ANSTIME), \
                            sum(ACDTIME) \
                       from hsplit \
                      where split in (" + sectorsDict[sector]['splitsStr'] + ") and ROW_DATE = date(sysdate)"
            cursor.execute(query)

            for callsoffered, acdcalls, outflowcalls, abncalls, acceptable, slvlabns, anstime, acdtime in cursor:
                context[sector] = {
                    'callsoffered': int(nvl(callsoffered,0)),
                    'acdcalls': int(nvl(acdcalls,0)),
                    'outflowcalls': int(nvl(outflowcalls,0)),
                    'abncalls': int(nvl(abncalls,0)),
                    'acceptable': int(nvl(acceptable,0)),
                    'slvlabns': int(nvl(slvlabns,0)),
                    'anstime': int(nvl(anstime,0)),
                    'acdtime': int(nvl(acdtime,0))
                }

        cursor.close()
        conn.close()

        return {
            'data': context,
            'status': variables.successful
        }

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}

def getSplit_CMS_Month():
    context = {}
    pyodbc.pooling = False
    sysdate = datetime.now()
    # Подключаемся к базе данных CMS
    try:
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))            
    except Exception:
        return {'status': variables.connection_error_to_db_cms}

    try:
        for sector in sectorsDict:
            if 'archive' in sectorsDict[sector]:
                if sectorsDict[sector]['archive'] == 'Y':
                    continue

            if sectorsDict[sector]['splitsStr'] == None:
                continue
                
            context[sector] = {}

            cursor = conn.cursor()
            dateStr = sysdate.strftime("%Y-%m-") + '01'

            if int(sysdate.strftime("%d")) == 1:
                return {'status': 'noDataFound'}
            else:
                query = "select sum(CALLSOFFERED), \
                                sum(ACDCALLS), \
                                sum(OUTFLOWCALLS), \
                                sum(ABNCALLS)+sum(BUSYCALLS)+sum(DISCCALLS), \
                                SUM(ACCEPTABLE), \
                                SUM(SLVLABNS) \
                           from dsplit \
                          where split in (" + sectorsDict[sector]['splitsStr'] + ") and ROW_DATE >= to_date('" + dateStr + "', '%Y-%m-%d')"
                cursor.execute(query)

                for callsoffered, acdcalls, outflowcalls, abncalls, acceptable, slvlabns in cursor:
                    context[sector] = {
                        'callsoffered': int(nvl(callsoffered,0)),
                        'acdcalls': int(nvl(acdcalls,0)),
                        'outflowcalls': int(nvl(outflowcalls,0)),
                        'abncalls': int(nvl(abncalls,0)),
                        'acceptable': int(nvl(acceptable,0)),
                        'slvlabns': int(nvl(slvlabns,0))
                    }

        cursor.close()
        conn.close()

        return {
            'data': context,
            'status': variables.successful
        }

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}
    

