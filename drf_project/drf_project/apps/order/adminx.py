import xadmin

from order.models import Order, OrderDetail

xadmin.site.register(Order)
xadmin.site.register(OrderDetail)
