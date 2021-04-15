import socket
from datetime import datetime
from dashboard.data.global_functions import list2str

successful = 'successful'
unknown_error = 'Неизвестная ошибка'
connection_error_to_ws = 'Ошибка подключения к сервису'
connection_error_to_db = 'Ошибка подключения к базе данных'
connection_error_to_db_cms = 'Ошибка подключения к базе данных CMS'
connection_error_to_db_mysql = 'Ошибка подключения к базе данных MySQL'
connection_error_to_db_cmsreport = 'Ошибка подключения к базе данных cmsreport (AVYA1D002)'
connection_error_to_db_cmsreport98 = 'Ошибка подключения к базе данных cmsreport (AVYA1D001)'
fetching_data_error = 'Ошибка выборки данных'
another_method_error = 'Доступен только GET метод'

connect_to_db_ivr_cfg = 'DSN=cmsreport;UID=udash;PWD=vHe9qwcm_UzRa'
connect_to_cmsreport98_cfg = 'DSN=cmsreport98;UID=udash;PWD=vHe9qwcm_UzRa'
connect_to_db_omilia_cfg = {
    'user': 'maxwell',
    'password': 'fsgyb243!Ss3gav3',
    'host': '10.204.5.11',
    'database': 'diamant',
    'raise_on_warnings': True
}

connect_to_db_cms_cfg = 'DSN=cms;UID=cms;PWD=Avaya_Kh@lyk_cms;ANSI=True'
#connect_to_db_cms_cfg = 'DSN=cms;UID=DidarK;PWD=cmsuser'
p_url = 'http://172.27.48.98:8080/scgi-bin/main'
p_url_agents = 'http://172.27.48.99:8080/scgi-bin/agentrange?range='
auth_values = ('admin','admin')

# ------------------- Карта звонков - VDN ------------------

# ----- Звонки через вектор, попадают напрямую к операторам -----
tran_cm_vdns = [79401,79402,79403,79407,79408,79409,79410,79411,79412,79414,79415,79418,79419,79422,79423,79425,79426,79413,79421,79865]
tran_cm_vdns_str = list2str(tran_cm_vdns)

tran_vdns_operators = [79502,79503,79504,79500,79501,79505,79506,79502,79503,79504,79497,79498,79499,79509,79510,79494]
tran_vdns_operators_str = list2str(tran_vdns_operators)

# ----- Звонки через IVR или Omilia -----
tran_cm_aep = [79404,79405,79406,79416,79417,79424,79533,79495,79600,79496,79866] 
tran_cm_aep_str = list2str(tran_cm_aep)

tran_aep_omilia = [79598]
tran_aep_omilia_str = list2str(tran_aep_omilia)

tran_ivr_omilia = [79854]
tran_ivr_omilia_str = list2str(tran_ivr_omilia)

tran_ivr_operators = [
79460,79461,79462,79463,79464,79465,79466,79467,79468,79469,
79470,79471,79436,79437,79438,79439,79440,79441,79442,79443,
79444,79445,79446,79447,79448,79449,79450,79451,79452,79453,
79454,79456,79457,79458,79459,79482,79483,79484,79485,79486,
79487,79488,79489,79490,79491,79492,79493,79427,79428,79429,
79430,79431,79432,79433,79434,79546,79547,79548,79549]
tran_ivr_operators_str = list2str(tran_ivr_operators)

tran_omilia_operators = [79585,79515,79516,79517,79518,79584,79589,79586,79587,79588,79850,79851,79852,79853]
tran_omilia_operators_str = list2str(tran_omilia_operators)

# ----- Для получения звех входящих звонков -----
cc_incalls = []
for lists in [tran_cm_vdns, tran_cm_aep]:
    for skills_id in lists:
        cc_incalls.append(skills_id)

cc_incalls_str = list2str(cc_incalls)

# ----- Global Dictionaries -----
context_fcr_acr = {}
g_report_acd_abn = {}
g_report_acd_abn_utp = {}
g_test = {}

g_report_acd_abn_time = None
g_report_acd_abn_utp_time = None
g_test_time = None


hostname = socket.gethostname()

if hostname == 'cc-dashboard.halykbank.nb':
    host = 'server'
else:
    host = 'local'

gMemCachedUrl = '/opt/www/memcached/memcached.sock'