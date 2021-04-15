from dashboard import views
from django.urls import path
from dashboard.data import ivr, omilia, reports, test

app_name = 'dashboard'

urlpatterns = [
    path('', views.page_index, name='index'),
    path('wallboard/', views.page_wallboard, name='wallboard'),
    path('graphics/', views.page_graphics, name='graphics'),
    path('reports/', views.page_reports, name='reports'),
    path('ivr/', views.page_ivr, name='ivr'),
    path('omilia/', views.page_omilia, name='omilia'),
    path('logs/', views.page_logs, name='logs'),

    path('api/splits/ws', views.splits_getWS),
    path('api/splits/ws/data', views.splits_getWSData),
    path('api/splits/cms/day', views.splits_getCMS_Day),
    path('api/splits/cms/month', views.splits_getCMS_Month),

    path('api/operators/list', views.operators_list),
    path('api/operators/ws', views.operators_getWS),

    path('api/index/online', views.index_online),
    path('api/index/online/graphic', views.index_online_graphic),
    path('api/index/online/operators', views.index_online_operators),
    path('api/index/online/other_parametrs', views.index_online_other_parametrs),
    
    path('api/index/setPlan', views.importPlan),
    path('api/index/getPlan', views.getPlan),
    path('api/index/chats', views.getChatsData),

    path('api/graphics/service-level', views.graphics_service_level),

    path('api/wallboard/online', views.wallboard_online),
    path('api/wallboard/online/best5', views.wallboard_best5),

    path('api/ivr/online', views.ivr_online),
    path('api/ivr/history', views.ivr_history_data),
    path('api/ivr2020/history', views.IVR2020_detail_history),

    path('api/omilia/online', views.omilia_online),
    path('api/omilia/online/graphic', views.omilia_online_graphic),
    path('api/omilia/history', views.omilia_history_data),
    path('api/omilia/history/transfers', views.omilia_hst_day_transfers),
    path('api/omilia/history/separated', views.omilia_topic_th_app),

    path('api/reports/main-report', views.report_MainReport),
    path('api/reports/utp-calls', views.report_UTPCalls),
    path('api/reports/incoming-calls', views.report_incoming_calls),

    path('api/test/set', test.set_test, name='set_test'),
    path('api/test/get', test.get_test, name='get_test'),
]