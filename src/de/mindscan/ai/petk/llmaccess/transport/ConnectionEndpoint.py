'''
Created on 09.11.2024

@author: JohnDoe
'''

class ConnectionEndpoint(object):
    '''
    classdocs
    '''

    def __init__(self, remote_api_type, endpoint_url, endpoint_name, endpoint_uuid):
        self.__remote_api_type = remote_api_type
        self.__endpoint_url = endpoint_url
        self.__endpoint_name = endpoint_name
        self.__endpoint_uuid = endpoint_uuid
    
    @property
    def remote_api_type(self):
        return self.__remote_api_type
    
    @property
    def endpoint_url(self):
        return self.__endpoint_url
    
    @property
    def endpoint_name(self):
        return self.__endpoint_name
    
    @property
    def endpoint_uuid(self):
        return self.__endpoint_uuid
    
    