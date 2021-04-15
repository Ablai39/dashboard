import json
from datetime import datetime, date, time, timedelta

def nvl(value1, value2):
    if value1 == None:
        return value2
    else:
        return value1

def list2str(value):
    for index, v in enumerate(value):
        if index == 0:
            new_str = str(v)
        else:
            new_str = new_str + ',' + str(v)
    return new_str

def get_prc(acceptable_slvlabns, callsoffered):
    if int(callsoffered) != 0:
        return  round(100*(acceptable_slvlabns/callsoffered))
    else:
        return 100

def get_prc_1(value1, value2):
    if int(value2) != 0:
        if value1 == None:
            return round(100*(0/value2),1)
        else:    
            return round(100*(value1/value2),1)
    else:
        return 100

def get_prc_2(acceptable_slvlabns, callsoffered):
    if int(callsoffered) != 0:
        return  round(100*(acceptable_slvlabns/callsoffered),2)
    else:
        return 100

def get_asa_value(anstime, acdcalls):
    if int(acdcalls) != 0:
        return round(anstime / acdcalls)
    else:
        return 0

def get_aat_value(acdtime, acdcalls):
    if int(acdcalls) != 0:
        return round(acdtime / acdcalls)
    else:
        return 0

def get_acr_value(summa, count):
    if int(count) != 0:
        return round((summa / (count * 5)) * 5, 1)
    else:
        return 5

def get_all_skills_id(sector):
    all_skills_list_local = []

    for skills in sector:
        for index, skills_id in enumerate(skills):
            if index != 0:
                all_skills_list_local.append(skills_id)
        
    return all_skills_list_local

def return_utf(s):
    if isinstance(s, str):
        return s.encode('utf-8')
    if isinstance(s, (int, float, complex)):
        return str(s).encode('utf-8')
    try:
        return s.encode('utf-8')
    except TypeError:
        try:
            return str(s).encode('utf-8')
        except AttributeError:
            return s
    except AttributeError:
        return s
    return s # assume it was already utf-8

def needUpdate (p_root, p_last_updated_datetime, p_type, p_value):
    sysdate = datetime.today()

    if p_root == '1':
        return True
    elif p_root == '0':
        return False
    else:
        if p_last_updated_datetime == 'pNull':
            return True
        else:
            if p_type == 'day':
                if sysdate.day != p_last_updated_datetime.day:
                    return True
                else:                        
                    if p_last_updated_datetime.hour < 8:
                        if sysdate.hour >= 8:
                            return True

            elif p_type == 'hour':
                if sysdate.hour != p_last_updated_datetime.hour:
                    if p_value == 104:
                        if sysdate.minute >= 4:
                            return True
                    else:
                        return True
            else:
                delta = sysdate - p_last_updated_datetime

                if p_type == 'second':
                    if int(delta.seconds) >= p_value:
                        return True
                elif p_type == 'minute':
                    p_value = p_value * 60

                    if int(delta.seconds) >= p_value:
                        return True
    return False

def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2

def json_deserializer(key, value, flags):
    if flags == 1:
        return value.decode('utf-8')
    if flags == 2:
        return json.loads(value.decode('utf-8'))
    raise Exception("Unknown serialization format")