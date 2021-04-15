
import pyodbc
import traceback
from dashboard.data import variables
from datetime import datetime, date, time, timedelta
from django.views.decorators.csrf import csrf_exempt
from dashboard.data.global_functions import get_prc, get_prc_2

def get_online_data():
    try:
        pyodbc.pooling = False
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_ivr_cfg))
    except Exception:
        return {'status': variables.connection_error_to_db_cmsreport}

    try:
        cursor = conn.cursor()
        cursor.execute("select ISNULL(max(TODATE),cast(GetDate() as Date)), \
                               ISNULL(SUM(successful),0), \
                               ISNULL(SUM(transfered),0), \
                               ISNULL(SUM(breaked),0) \
                          from cmsreport.dbo.ivr_hour_history \
                         where cast(FROMDATE as Date) = cast(GETDATE() as Date)")

        result = cursor.fetchone()
        max_todate = result[0]
        arc_successful = result[1]
        arc_transfered = result[2]
        arc_breaked = result[3]

        query = "SELECT VarValue, COUNT(1) AS CNT \
                   FROM EPCDR.dbo.VPAppLog \
                  WHERE ActivityName = 'CallStatus' \
                    AND VarName = 'AppVariables:CallStatus' \
                    AND ApplicationID = 'test redirect' \
                    AND VarValue in ('0','1','2') \
                    AND LogTimestamp >= '" + str(max_todate) + "' \
                    AND LogTimestamp < DATEADD(hour, DATEDIFF(hour, 0, GETDATE() + '01:00:00'), 0) \
                    GROUP BY VarValue"
        
        cursor.execute(query)
        
        p_successful = 0
        p_transfered = 0
        p_breaked = 0

        for VarValue, count in cursor:
            if VarValue == '1':
                p_successful = int(count)
            elif VarValue == '2':
                p_transfered = int(count)
            elif VarValue == '0':
                p_breaked = int(count)

        all_successful = arc_successful + p_successful
        all_transfered = arc_transfered + p_transfered
        all_breaked =  arc_breaked + p_breaked
        p_all = all_successful + all_transfered + all_breaked
        
        response_data = {
            'status': variables.successful,
            'result': {
                'successful': all_successful,
                'successful_prc': get_prc(all_successful, p_all),
                'transfered': all_transfered,
                'transfered_prc': get_prc(all_transfered, p_all),
                'breaked': all_breaked,
                'breaked_prc': get_prc(all_breaked, p_all),
                'all': p_all
            }
        }
        
    except Exception:
        response_data = {'status': traceback.format_exc()}
    
    cursor.close()
    conn.close()     
    return response_data

def get_online_IVR2020():
    try:
        pyodbc.pooling = False
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_ivr_cfg))
    except Exception:
        return {'status': variables.connection_error_to_db_cmsreport}

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT VarValue, COUNT(1) AS CNT \
                        FROM EPCDR.dbo.VPAppLog \
                        WHERE ApplicationID = 'IVR_2020' \
                            AND LogTimestamp >= cast(GetDate() as Date) \
                            AND LogTimestamp < cast(GetDate()+1 as Date) \
                            AND VarName = 'AppLogs:CallStatus' \
                            AND VarValue in ('0','1','2') \
                            GROUP BY VarValue")
                                    
        p_successful = 0
        p_transfered = 0
        p_breaked = 0

        for VarValue, count in cursor:
            if VarValue == '1':
                p_successful = int(count)
            elif VarValue == '2':
                p_transfered = int(count)
            elif VarValue == '0':
                p_breaked = int(count)

        p_all = p_successful + p_transfered + p_breaked
        
        response_data = {
            'status': variables.successful,
            'result': {
                'successful': p_successful,
                'successful_prc': get_prc(p_successful, p_all),
                'transfered': p_transfered,
                'transfered_prc': get_prc(p_transfered, p_all),
                'breaked': p_breaked,
                'breaked_prc': get_prc(p_breaked, p_all),
                'all': p_all
            }
        }
        
    except Exception:
        response_data = {'status': traceback.format_exc()}
    
    cursor.close()
    conn.close()     
    return response_data

def get_history_data():
    try:
        pyodbc.pooling = False
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_ivr_cfg))
    except Exception:
        return {'status': variables.connection_error_to_db_cmsreport}
    
    try:
        nList = []
        cursor = conn.cursor()
        cursor.execute("select top 10 \
                               convert(varchar, calendar_day, 104) 'day', \
                               successful, \
                               transfered, \
                               breaked \
                          from cmsreport.dbo.ivr_day_history \
                         order by calendar_day DESC")

        for p_day, p_successful, p_transfered, p_breaked in cursor:
            p_all = p_successful + p_transfered + p_breaked
            context = {
                'date': str(p_day),
                'all': int(p_all),
                'successful': int(p_successful),
                'successful_prc': get_prc_2(p_successful, p_all),
                'transfer': int(p_transfered),
                'transfer_prc': get_prc_2(p_transfered, p_all),
                'break': int(p_breaked)
            }

            nList.append(context)
        
        response_data = {
            'status': variables.successful,
            'result': nList
        }

    except Exception:
        response_data = {'status': traceback.format_exc()}

    cursor.close()
    conn.close()   
    return response_data

def IVR2020_detail_history(doper):

    doperDT = datetime.strptime(doper, '%d.%m.%Y')
    dateTo = doperDT + timedelta(days=1)
    # sysdate = datetime.now()

    dateFromStr = doperDT.strftime('%Y-%m-%d')
    dateToStr = dateTo.strftime('%Y-%m-%d')

    try:
        pyodbc.pooling = False
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_ivr_cfg))
    except Exception:
        return {'status': variables.connection_error_to_db_cmsreport}

    try:
        allRings = 0
        AppLogs = {'Total': 0}
        CallStatus = {
            'Total': 0,
            'Successful': 0,
            'Transfered': 0,
            'Breaked': 0
        }
        AppLogsMenuTree = {}
        MenuTree_MM = {'Total': 0}
        MenuTree_MCS = {'Total': 0}
        Languages = {}
        context = {}
        DestinationVDN = {}
        PhoneFL = {}

        cursor = conn.cursor()
        query = "select ActivityName, VarName, VarValue \
                    from cmsreport.dbo.IVR2020_detail_history \
                    where LogTimestamp >= '"+dateFromStr+"' and LogTimestamp < '"+dateToStr+"' \
                    and MainFL = 1 and VarName not in ('AppLogs:ANI','AppLogs:IIN')"
        cursor.execute(query)

        for ActivityName, VarName, VarValue in cursor:

            if ActivityName == 'AppLogsMenuTree':
                VarNameModify = VarName[16:]

                if VarNameModify[0:3] == 'MM_':
                    if VarNameModify in ['MM_InfoCredits','MM_InfoCreditCards']:
                        VarNameModify = 'MM_InfoCreditsCredCards'
                    
                    if VarNameModify in ['MM_InfoOvdCredits','MM_InfoOvdCreditCards']:
                        VarNameModify = 'MM_InfoOvdCreditsCredCards'

                    if VarNameModify not in MenuTree_MM:
                        MenuTree_MM[VarNameModify] = 0
                    
                    MenuTree_MM['Total'] += 1
                    MenuTree_MM[VarNameModify] += 1

                elif VarNameModify[0:4] == 'MCS_':
                    if VarNameModify not in MenuTree_MCS:
                        MenuTree_MCS[VarNameModify] = 0
                    
                    MenuTree_MCS['Total'] += 1
                    MenuTree_MCS[VarNameModify] += 1

                else:
                    if VarNameModify not in AppLogsMenuTree:
                        AppLogsMenuTree[VarNameModify] = 0
                
                    AppLogsMenuTree[VarNameModify] += 1
            
            if ActivityName == 'AppLogs':
                VarNameModify = VarName[8:]

                if VarNameModify == 'CallStatus':
                    CallStatus['Total'] += 1

                    if VarValue == '0':
                        CallStatus['Breaked'] += 1
                    if VarValue == '1':
                        CallStatus['Successful'] += 1
                    if VarValue == '2':
                        CallStatus['Transfered'] += 1

                elif VarNameModify == 'Language':
                    VarValueModify = VarValue[0:3]
                    
                    if VarValueModify not in Languages:
                        Languages[VarValueModify] = 0
                    
                    Languages[VarValueModify] += 1
                
                elif VarNameModify == 'DestinationVDN':
                    VarValueModify = 'vdn'+VarValue

                    if VarValueModify not in DestinationVDN:
                        DestinationVDN[VarValueModify] = 0
                    
                    DestinationVDN[VarValueModify] += 1

                elif VarNameModify in ('FL_Mobile','FL_TrustedNumber'):

                    if VarNameModify not in PhoneFL:
                        PhoneFL[VarNameModify] = 0
                    
                    PhoneFL[VarNameModify] += 1
                    
                else:
                    AppLogs['Total'] += 1

                    if VarNameModify not in AppLogs:
                        AppLogs[VarNameModify] = 0
                    
                    AppLogs[VarNameModify] += 1
        
        # сортировка
        # AppLogs
        nList = []
        for value in AppLogs:
            nList.append({
                'code': value,
                'count':AppLogs[value]
            })
        newList = sorted(nList, key=lambda k: k['count'], reverse=True)
        AppLogs = {}

        for value in newList:
            AppLogs[value['code']] = value['count']

        # MenuTree_MM
        nList = []
        for value in MenuTree_MM:
            nList.append({
                'code': value,
                'count':MenuTree_MM[value]
            })
        newList = sorted(nList, key=lambda k: k['count'])
        MenuTree_MM = {}

        for value in newList:
            MenuTree_MM[value['code']] = value['count']

        # MenuTree_MCS
        nList = []
        for value in MenuTree_MCS:
            nList.append({
                'code': value,
                'count':MenuTree_MCS[value]
            })
        newList = sorted(nList, key=lambda k: k['count'], reverse=True)
        MenuTree_MCS = {}

        for value in newList:
            MenuTree_MCS[value['code']] = value['count']

        context = {
            'Doper': doperDT.strftime('%d.%m.%Y'),
            'CallStatus': CallStatus,
            'Languages': Languages,
            'DestinationVDN': DestinationVDN,
            'PhoneFL': PhoneFL,
            'SelfServices': AppLogs,
            'MenuTree_MM': MenuTree_MM,
            'MenuTree_MCS': MenuTree_MCS,
            'MenuTree_Other': AppLogsMenuTree
        }
        
        response_data = {
            'status': variables.successful,
            'data': context
        }

    except Exception:
        response_data = {'status': traceback.format_exc()}
    
    cursor.close()
    conn.close()
    return response_data

