import traceback
from dashboard.data import index
from dashboard.data import wallboard
from dashboard.data import ivr
from dashboard.data import omilia
from dashboard.data import operators
from dashboard.data import reports
from dashboard.data import graphics
from dashboard.data import chats
from dashboard.data import splitsGroup
from dashboard.data import splitsData
from dashboard.data import operatorsData

def getData(nRequest, nDictCode):
    
    try:
        # splits
        if nDictCode == 'SPLITS_WS':
            return splitsData.getWS()
        elif nDictCode == 'SPLITS_CMS_DAY_DATA':
            return splitsData.getSplit_CMS_Day()
        elif nDictCode == 'SPLITS_CMS_MONTH_DATA':
            return splitsData.getSplit_CMS_Month()
        
        # index
        elif nDictCode == 'INDEX_ONLINE':
            return index.get_SplitsData()
        elif nDictCode == 'INDEX_ONLINE_OHTER_PARAMETRS':
            return index.get_OtherParametrsData()
        elif nDictCode == 'INDEX_ONLINE_GRAPHIC':
            return index.get_GraphicData()
        elif nDictCode == 'INDEX_ONLINE_OPERATORS':
            return index.get_OperatorsData()
        
        # graphics
        elif nDictCode == 'GRAPHICS_SERVICE_LEVEL':
            return graphics.get_service_level()

        # wallboard
        elif nDictCode == 'WALLBOARD_ONLINE':
            return wallboard.get_OnlineData()

        elif nDictCode == 'WALLBOARD_UPIB_BEST5':
            return wallboard.get_best5_operators('upib')
        elif nDictCode == 'WALLBOARD_RUBS_BEST5':
            return wallboard.get_best5_operators('rubs')
        elif nDictCode == 'WALLBOARD_UPRK_BEST5':
            return wallboard.get_best5_operators('uprk')
        
        # ivr
        elif nDictCode == 'IVR_ONLINE':
            return ivr.get_online_IVR2020()
        elif nDictCode == 'IVR_HISTORY_DATA':
            return ivr.get_history_data()

        # omilia
        elif nDictCode == 'OMILIA_ONLINE':
            return omilia.get_online_data()
        elif nDictCode == 'OMILIA_ONLINE_GRAPHIC':
            return omilia.get_graphic_data()
        elif nDictCode == 'OMILIA_HISTORY_DATA':
            return omilia.get_history_data()
        
        # operators
        elif nDictCode == 'OPERATORS_CMS_DATA':
            return operatorsData.getOperatorsList()
        elif nDictCode == 'OPERATORS_WS':
            return operatorsData.getWS()
        elif nDictCode == 'GET_OPERATORS_CNT_PLAN':
            return operators.get_plan()
        
        # reports
        elif nDictCode == 'REPORT_INCOMING_CALLS':
            if nRequest != None:
                getDate = nRequest.GET.get('date', '')

                if len(getDate) == 0:
                    return {'status': 'Отсутствует параметр date'}
                elif len(getDate) != 10:
                    return {'status': 'Некорректный формат параметра date. Пример: 2020-01-01'}
                
                return reports.report_incoming_split_calls(getDate)
            else:
                return {'status': 'Отсутствует параметр date'}
        elif nDictCode == 'REPORTS_MAIN_REPORT':
            return reports.get_MainReportData()
        elif nDictCode == 'REPORTS_UTP_SPLIT_CALLS':
            return reports.get_ReportUTPCalls()
        
        # chatbot
        elif nDictCode == 'CHATS_DATA':
            return chats.getData()

        else:
            return {'status': 'Функция не определена'}

    except Exception:
        return {'status': traceback.format_exc()}