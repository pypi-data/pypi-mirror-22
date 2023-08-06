from clink import stamp, mapper, Controller
from clink.service.auth import OAuthService
from clink import Http400Error


@stamp(OAuthService)
@mapper.path('auth')
class AuthCtl(Controller):
    def __init__(self, oauth_sv):
        self._oauth_sv = oauth_sv

    @mapper.post('token')
    def get_token(self, req, res):
        info = req.body
        grant_type = info['grant_type']

        if grant_type == 'password':
            res.body = self._oauth_sv.mktoken_pwd(
                info['username'], info['password']
            )
        elif grant_type == 'refresh_token':
            res.body = self._oauth_sv.mktoken_rtoken(info['refresh_token'])
        else:
            raise Http400Error(req, 'Not support grant_type=' + grant_type)
