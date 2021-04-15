from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, time, timedelta
from dashboard.data.variables import successful, another_method_error, g_test, g_test_time
from dashboard.data.global_functions import nvl, needUpdate, json_serializer, json_deserializer
from pymemcache.client.base import Client



@csrf_exempt
def test (request):
    if request.method == "GET":
        global g_test
        global g_test_time
        sysdate = datetime.today()
        root_conn = nvl(request.GET.get('root', ''), 'pNull')
        last_updated_datetime = nvl(g_test_time, 'pNull')
        need_update = needUpdate(root_conn, last_updated_datetime, 'second', 0)

        if need_update:
            g_test = {
                'status': successful,
                'updated_datetime': sysdate.strftime("%d.%m.%Y %H:%M:%S")
            }
            g_test_time = sysdate

        return JsonResponse(g_test)
       
    else:
        return JsonResponse({'status': another_method_error})

@csrf_exempt
def set_test (request):
    client = Client(('/opt/www/memcached/memcached.sock'), serializer=json_serializer,
                deserializer=json_deserializer)
    client.set('new', {'status':'updated'})
    # result = client.get('key')


    
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def get_test (request):
    client = Client(('/opt/www/memcached/memcached.sock'), serializer=json_serializer,
                deserializer=json_deserializer)


    result = client.get('INDEX_ONLINE')

    if result is None:
        result = {'status': 'NotFound'}

    print(result)
    return JsonResponse(result)