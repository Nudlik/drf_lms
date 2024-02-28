from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from lms.pagination import LMSPagination
from lms.selializers.subscription import SubscriptionSerializer

subscription_post = \
    swagger_auto_schema(
        responses={
            201: 'Created',
            404: 'Not Found'
        },
        operation_description='Добавить курс в подписки',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='id курса',
                type=openapi.TYPE_INTEGER
            ),
        ],
    )

subscription_delete = \
    swagger_auto_schema(
        responses={
            201: 'Created',
            404: 'Not Found'
        },
        operation_description='Удалить курс из подписок',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="id курса",
                type=openapi.TYPE_STRING
            ),
        ],
    )

subscription_get = \
    swagger_auto_schema(
        responses={
            200: SubscriptionSerializer(many=True)
        },
        operation_description='Получить подписки',
        paginator_inspectors=[LMSPagination],
    )
