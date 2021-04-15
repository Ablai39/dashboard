import pyodbc
import traceback
from datetime import datetime
from dashboard.data.global_functions import nvl, get_prc, get_prc_2, get_all_skills_id, list2str
from dashboard.data import variables
from dashboard.data.skill_groups import main_dashboard
from dashboard.data.config import sectorsDict

def get_service_level ():
    nListOfTime = []
    response_data = {}
    pyodbc.pooling = False
    today = datetime.now()
    month = int(today.strftime('%m'))
    year = int(today.strftime('%Y'))
    daysRange = range(1,32)

    daysLst = []
    for value in daysRange:
        daysLst.append(value)

    def getMonthName(value):
        if value == '01':
            return 'Январь'
        elif value == '02':
            return 'Февраль'
        elif value == '03':
            return 'Март'
        elif value == '04' :
            return 'Апрель'
        elif value == '05':
            return 'Май'
        elif value == '06':
            return 'Июнь'
        elif value == '07':
            return 'Июль'
        elif value == '08':
            return 'Август'
        elif value == '09':
            return 'Сентябрь'
        elif value == '10':
            return 'Октябрь'
        elif value == '11':
            return 'Ноябрь'
        elif value == '12':
            return 'Декабрь'

    try:
        conn = pyodbc.connect(r'%s' % (variables.connect_to_db_cms_cfg))
    except Exception:
        return {'status': variables.connection_error_to_db_cms}

    try:
        context = {}
        graphicSectorsDict = {}
        allSectorsData = {
            'splitsLst': []
        }
        cursor = conn.cursor()
        for sector in sectorsDict:
            
            for split in sectorsDict[sector]['splitsLst']:
                allSectorsData['splitsLst'].append(split)
            
            if sectorsDict[sector]['enableCallBack'] == 'Y':
                for split in sectorsDict[sector]['splits_cbaLst']:
                    allSectorsData['splitsLst'].append(split)

            if 'archive' in sectorsDict[sector]:
                if sectorsDict[sector]['archive'] == 'Y':
                    continue

            if 'enableInGraphicPage' in sectorsDict[sector]:
                if sectorsDict[sector]['enableInGraphicPage'] == 'Y':
                    graphicSectorsDict[sector] = sectorsDict[sector]

        graphicSectorsDict['all'] = {
            'splitsLst': allSectorsData['splitsLst'],
            'splitsStr': list2str(allSectorsData['splitsLst']),
        }

        for sector in graphicSectorsDict:
            splitsStr = graphicSectorsDict[sector]['splitsStr']

            query = "select row_date, \
                    SUM(CALLSOFFERED) CALLSOFFERED, \
                    SUM(ACCEPTABLE) ACCEPTABLE, \
                    SUM(SLVLABNS) SLVLABNS \
                from dsplit \
                where split in (" + splitsStr + ") \
                and to_date(to_char(row_date, '%Y-%m'), '%Y-%m') >= to_date('" + str(year) + "-01', '%Y-%m') \
                group by row_date \
                order by row_date"
            cursor.execute(query)

            for p_row_date, p_callsoffered, p_acceptable, p_slvlabns in cursor:
                nList = []
                
                m_doper = p_row_date.strftime('%m')
                m_key = 'month_' + m_doper
                
                d_doper = p_row_date.strftime('%d')
                d_key = 'day' + str(int(d_doper))

                if sector not in context:
                    context[sector] = {}
                
                if m_key not in context[sector]:
                    context[sector][m_key] = {'name': getMonthName(m_doper)}

                if d_key not in context[sector][m_key]:
                    context[sector][m_key][d_key] = {}

                nPrc = get_prc((int(p_acceptable) + int(p_slvlabns)), int(p_callsoffered))

                if p_callsoffered == 0:
                    nPrc = 100
                
                dateStr = p_row_date.strftime('%d.%m.%Y')

                context[sector][m_key][d_key] = {
                    'doper': dateStr,
                    'sl': nPrc,
                    'callsoffered': int(p_callsoffered),
                    'acceptable': int(p_acceptable),
                    'slvlabns': int(p_slvlabns)
                }          

        cursor.close()
        conn.close()
        context['days_range'] = daysLst
        context['status'] = variables.successful
        return context

    except Exception:
        cursor.close()
        conn.close()
        return {'status': traceback.format_exc()}