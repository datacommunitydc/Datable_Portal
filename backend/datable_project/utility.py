from django.conf import settings
from django.contrib.auth.models import User


def create_user(user_data):
    """
    :param user_data:
    :return:
    """

    user = User.objects.create(
        username=user_data['username'],
        email=user_data['email'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )
    if user_data.get('password', None):
        user.set_password(user_data['password'])
    else:
        user.set_password('somerandomnumber')
    user.save()
    return user


def prepare_user_dict_from_social_data(user_data):
    """
    :param user_data:
    :return:
    """
    serialize_user_data = {}
    for key, value in settings.SOCIAL_USER_DATA_MAPPER.iteritems():
        serialize_user_data[key] = ''
        for i in value:
            if user_data.get(i, None):
                serialize_user_data[key] = user_data[i]
    return serialize_user_data

