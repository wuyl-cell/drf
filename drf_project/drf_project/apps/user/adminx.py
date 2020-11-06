import xadmin

from user.models import User


class UserInfo(object):
    list_display = ['username', "email", "phone"]


# xadmin.site.register(User, UserInfo)