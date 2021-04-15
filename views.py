import json
import traceback
from dashboard.data import omilia
from dashboard.data import config
from dashboard.data import ivr
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dashboard.data.check_memcache import getMemCache

# --------------- Pages ---------------
def page_index(request):   
    return render(request, 'index.html', {
        'page':'index', 
        'sectorsDict': config.sectorsDict, 
        'widgetOperatorsItemsDict': config.widgetOperatorsItemsDict,
        'depsDict': config.depsDict
        })

def page_graphics(request):
    return render(request, 'graphics.html', {
        'page':'graphics',
        'sectorsDict': config.sectorsDict
        })

def page_reports(request):
    return render(request, 'reports.html', {
        'page':'reports',
        'sectorsDict': config.sectorsDict
        })    

def page_wallboard(request):
    return render(request, 'wallboard.html', {'page':'home_wallboard'})

def page_ivr(request):    
    return render(request, 'ivr.html', {'page':'home_ivr'})

def page_omilia(request):
    return render(request, 'omilia.html', {'page':'home_omilia'})

def page_logs(request):
    return render(request, 'logs.html', {'page':'logs'})

# ------------- Web Services -------------

# splits
@csrf_exempt
def splits_getWS(request):
    from dashboard.data.splitsData import getWS_MemCache
    return JsonResponse(getWS_MemCache(request))

@csrf_exempt
def splits_getWSData(request):
    from dashboard.data.splitsData import getSplit_WS
    return JsonResponse(getSplit_WS())

@csrf_exempt
def splits_getCMS_Day(request):
    from dashboard.data.splitsData import getSplitCMS_Day_MemCache
    return JsonResponse(getSplitCMS_Day_MemCache(request))

@csrf_exempt
def splits_getCMS_Month(request):
    from dashboard.data.splitsData import getSplitCMS_Month_MemCache
    return JsonResponse(getSplitCMS_Month_MemCache(request))

# операторы
@csrf_exempt
def operators_list (request):
    from dashboard.data.operatorsData import getOperatorsList_MemCache
    return JsonResponse(getOperatorsList_MemCache(request))

@csrf_exempt
def operators_getWS(request):
    from dashboard.data.operatorsData import getWS_MemCache
    return JsonResponse(getWS_MemCache(request))

# index
@csrf_exempt
def index_online(request):
    from dashboard.data.index import get_SplitsData_MemCache
    return JsonResponse(get_SplitsData_MemCache(request))

@csrf_exempt
def index_online_operators(request):
    from dashboard.data.index import get_OperatorsData_MemCache
    return JsonResponse(get_OperatorsData_MemCache(request))

@csrf_exempt
def index_online_other_parametrs (request):
    return JsonResponse(getMemCache(request, 'INDEX_ONLINE_OHTER_PARAMETRS', 'minute', 5))

@csrf_exempt
def index_online_graphic (request):
    return JsonResponse(getMemCache(request, 'INDEX_ONLINE_GRAPHIC', 'hour', 104))

@csrf_exempt
def graphics_service_level (request):
    return JsonResponse(getMemCache(request, 'GRAPHICS_SERVICE_LEVEL', 'day', 1))

# wallboard
@csrf_exempt
def wallboard_online (request):
    from dashboard.data.wallboard import get_OnlineData_MemCache
    return JsonResponse(get_OnlineData_MemCache(request))

@csrf_exempt
def wallboard_best5 (request):

    try:
        p_upravlenie = request.GET.get('upravlenie', '')
        if p_upravlenie == None:
            return JsonResponse({'status': 'необходимо указать управление в теге <<upravlenie>>'})
    except Exception:
        return JsonResponse({'status': traceback.format_exc()})
    
    if p_upravlenie == 'upib':
        dictCode = 'WALLBOARD_UPIB_BEST5'
    elif p_upravlenie == 'rubs':
        dictCode = 'WALLBOARD_RUBS_BEST5'
    elif p_upravlenie == 'uprk':
        dictCode = 'WALLBOARD_UPRK_BEST5'
    else: 
        return JsonResponse({'status': 'необходимо указать управление в теге <<upravlenie>>'})
    
    return JsonResponse(getMemCache(request, dictCode, 'minute', 15))

# omilia
@csrf_exempt
def omilia_online (request):
    return JsonResponse(getMemCache(request, 'OMILIA_ONLINE', 'second', 10))

@csrf_exempt
def omilia_online_graphic (request):
    return JsonResponse(getMemCache(request, 'OMILIA_ONLINE_GRAPHIC', 'minute', 5))

@csrf_exempt
def omilia_history_data (request):
    return JsonResponse(getMemCache(request, 'OMILIA_HISTORY_DATA', 'day', 1))

@csrf_exempt
def omilia_hst_day_transfers (request):
    if request.method != "GET":
        return JsonResponse({'status': another_method_error})

    try:
        doper = request.GET.get("doper", "")
        context = omilia.get_hst_day_transfers(doper)
    except Exception:
        context = {'status': traceback.format_exc()}

    return JsonResponse(context)

@csrf_exempt
def omilia_topic_th_app(request):
    if request.method != "GET":
        return JsonResponse({'status': another_method_error})
        
    try:
        doper = request.GET.get("doper", "")
        context = omilia.get_topic_th_app(doper)
    except Exception:
        context = {'status': traceback.format_exc()}

    return JsonResponse(context)

# ivr
@csrf_exempt
def ivr_online (request):
    return JsonResponse(getMemCache(request, 'IVR_ONLINE', 'second', 10))

@csrf_exempt
def ivr_history_data (request):
    return JsonResponse(getMemCache(request, 'IVR_HISTORY_DATA', 'day', 1))

@csrf_exempt
def IVR2020_detail_history (request):
    if request.method != "GET":
        return JsonResponse({'status': another_method_error})
    
    try:
        doper = request.GET.get("doper", "")

        if doper is None or doper == "":
            return JsonResponse({'status': 'doper not Exist'})

    except Exception:
        return JsonResponse({'status': traceback.format_exc()})

    return JsonResponse(ivr.IVR2020_detail_history(doper))

# отчеты
@csrf_exempt
def report_incoming_calls (request):
    return JsonResponse(getMemCache(request, 'REPORT_INCOMING_CALLS', 'day', 1))

@csrf_exempt
def report_MainReport(request):
    from dashboard.data.reports import get_MainReportData_MemCache
    return JsonResponse(get_MainReportData_MemCache(request))

@csrf_exempt
def report_UTPCalls(request):
    from dashboard.data.reports import get_ReportUTPCalls_MemCache
    return JsonResponse(get_ReportUTPCalls_MemCache(request))

@csrf_exempt
def importPlan (request):

    if request.method != "GET":
        return JsonResponse({'status': another_method_error})
        
    try:
        doper = request.GET.get("doper", "")
        upravlenie = request.GET.get("upravlenie", "")
        operators_cnt = request.GET.get("operators", "")
        context = operators.import_plan(doper, upravlenie, operators_cnt)
    except Exception:
        context = {'status': traceback.format_exc()}

    return JsonResponse(context)

@csrf_exempt
def getPlan (request):
    return JsonResponse(getMemCache(request, 'GET_OPERATORS_CNT_PLAN', 'minute', 30))

@csrf_exempt
def getChatsData (request):
    return JsonResponse(getMemCache(request, 'CHATS_DATA', 'second', 10))


