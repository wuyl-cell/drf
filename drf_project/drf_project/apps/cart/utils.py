from django_redis import get_redis_connection

redis_connection = get_redis_connection('cart')


def get_car_len(user_id):
    course_len = redis_connection.hlen('cart_%s' % user_id)
    return course_len

def get_all_status(user_id):
    selected = redis_connection.smembers('selected_%s' % user_id)
    cart_list = redis_connection.hgetall('cart_%s' % user_id)
    data = []
    if len(selected) == len(cart_list):
        checked = True
    else:
        checked = False
    data.append({'checked': checked})
    return data
