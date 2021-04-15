import traceback
from pymemcache.client.base import Client
from datetime import datetime, date, time, timedelta
from dashboard.data.variables import host, gMemCachedUrl, another_method_error
from dashboard.data.global_functions import needUpdate, nvl, json_serializer, json_deserializer
from dashboard.data.dashboardFunctions import getData

def getMemCache(nRequest, nDictCode, nDateTimeType, nDateTimeValue):

    if nRequest != None:
        if nRequest.method != "GET":
            return {'status': another_method_error}
        
        nRootConn = nRequest.GET.get('root', '')
        if len(nRootConn) == 0:
            nRootConn = 'pNull'
    else:
        nRootConn = 'pNull'

    try:
        global host
        if host == 'server':
            client = Client((gMemCachedUrl), serializer=json_serializer, deserializer=json_deserializer)
    except Exception:
        return {'status': traceback.format_exc()}
        
    try:
        context = {}
        need_update = False
        
        if host == 'server':
            context = client.get(nDictCode)

            if context is None:
                need_update = True
            else:
                last_updated_datetime = datetime.strptime(context['updated_datetime'], '%Y-%m-%d %H:%M:%S')
                need_update = needUpdate(nRootConn, last_updated_datetime, nDateTimeType, nDateTimeValue)
        else:
            need_update = True

        if need_update:
            if host == 'server':
                if context is not None:
                    if nDictCode in ['INDEX_ONLINE_OPERATORS']:
                        updated_datetime = datetime.today()
                        context['updated_datetime'] = updated_datetime.strftime('%Y-%m-%d %H:%M:%S')
                        client.set(nDictCode, context)

            context = getData(nRequest, nDictCode)
            updated_datetime = datetime.today()
            context['updated_datetime'] = updated_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if host == 'server':
                client.set(nDictCode, context)
    
    except Exception:
        context = {'status': traceback.format_exc()}

    if host == 'server':
        client.close()
    return context