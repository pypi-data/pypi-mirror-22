import os

from core.api.request import Request
from core.services.cache_service import CacheService
from core.services.onyxerp_service import OnyxErpService


class SocialService(Request, OnyxErpService):

    jwt = None

    def __int__(self, base_url):
        super(SocialService, self).__init__(base_url)

    def get_pessoa_fisica(self, pf_cod: int()):

        file_name = "{0}/cache/SocialAPI/pessoa-fisica/{1}.json".format(self.get_api_root(), pf_cod)

        if os.path.isfile(file_name):
            return CacheService.read_file(file_name)

        response = self.get("/v1/pessoa-fisica/{0}/".format(pf_cod))

        status = response.get_status_code()
        data = response.get_decoded()['data']

        if status == 200:
            CacheService.write_file(file_name, data)
            return data
        else:
            return {
                "status": status,
                "response": response.get_content()
            }
