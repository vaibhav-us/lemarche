import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lemarche.settings")
print(f'DJANGO_SETTINGS_MODULE: {os.environ.get("DJANGO_SETTINGS_MODULE")}')
django.setup()

import core.routing


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
         "websocket": 
            AuthMiddlewareStack(URLRouter(core.routing.websocket_urlpatterns))
        
    }
)




# import os

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lemarche.settings')

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
# })