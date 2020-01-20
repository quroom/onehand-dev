from django.contrib.auth.middleware import AuthenticationMiddleware
from django.conf import settings
import datetime

class LogoutMiddleware(AuthenticationMiddleware):

    def process_response(self, request, response):
        #You have access to request.user in this method
        if(request.path.startswith("/accounts/logout/")):
            if not request.user.is_authenticated:
                response.cookies['islogin'] = False
                response.cookies['islogin']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
                response.cookies['islogin']['Path'] = '/'
                response.cookies['islogin']['SameSite'] = 'Lax'
        elif(request.method=='POST'):
            if(response.status_code == 302):
                if(request.path.startswith("/accounts/login/")):
                    response.cookies['islogin'] = True
                    response.cookies['islogin']['expires'] = datetime.datetime.now()+datetime.timedelta(0,1)
                    response.cookies['islogin']['Path'] = '/'
                    response.cookies['islogin']['SameSite'] = 'Lax'
        return response