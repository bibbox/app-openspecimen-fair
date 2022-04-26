import rdflib
import requests
import logging
import json

logger = logging.getLogger(__name__)

class FDPClient:
    DATA_FORMATS = {
        'n3': 'text/n3',
        'turtle': 'text/turtle',
        'xml': 'application/rdf+xml',
        'json-ld': 'application/ld+json',
        'nt': 'application/n-triples'
    }


    def __init__(self, baseurl, email, password):
        self.baseurl = baseurl.rstrip('/')
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.headers['Authorization'] = f'Bearer {self.gettoken(email, password)}'
        del self.headers['Accept']


    def gettoken(self, email, password):
        login = {"email":email,
               "password": password}
        #logger.info(json.dumps(login))
        response = requests.post(f"{self.baseurl}/tokens",
                      data=json.dumps(login), headers=self.headers)
        #response = requests.post(f"{self.baseurl}/tokens", data={"email": email, "password": password})
        if response.status_code == 200:
            return response.json()['token']

        logger.error ("Problem with the login: " + str(response))
        raise Exception("Problem with the login",response)
        # return response['token']

    def create(self, type, data, format='turtle'):
        """Send a create request.
        Args:
            url(str): URL for creating a metadata.
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        logger.debug(f'Create metadata on {self.baseurl}/{type} with the content: \n{data}')
        create_headers=self.headers
        create_headers.update({'Content-Type': self.DATA_FORMATS[format]})
        #print(create_headers)
        try:
            data = self._check_data(data, format)
            r = requests.post(f'{self.baseurl}/{type}', data=data, headers=create_headers)
            return r.headers['Location'].lstrip(f'{self.baseurl}/{type}/')
        except Exception as error:
            print(f'Unexpected error when connecting to {self.baseurl}/{type}\n')
            raise error
        else:
            if r.status_code >= 300:
                print(f'HTTP error: {r.status_code} {r.reason} for {self.baseurl}/{type}',
                      f'\nResponse message: {r.text}')
                raise

    def read(self, type, id, format='turtle', **kwargs):
        """Send a read request.
        Args:
            url(str): URL for reading a metadata.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``accept``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        Returns:
            :class:`rdflib.Graph`:  RDF graph of the requested metadata.
        """
        logger.debug(f'Read metadata: {self.baseurl}/{type}/{id}')
        read_headers = self.headers.copy()
        read_headers.update({'Content-Type': self.DATA_FORMATS[format]})

        try:
            r = requests.get(f'{self.baseurl}/{type}/{id}', headers=read_headers, **kwargs)
        except Exception as error:
            print(f'Unexpected error when connecting to {self.baseurl}/{type}/{id}\n')
            raise error
        else:
            if r.status_code != 200:
                print(f'HTTP error: {r.status_code} {r.reason} for {self.baseurl}/{type}/{id}',
                      f'\nResponse message: {r.text}')
                raise

        g = rdflib.Graph()
        g.parse(data=r.text, format=format)
        return g

    def delete(self,type, id, **kwargs):
        """Send a delete request.
        Args:
            url(str): URL for deleting a metadata.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        logger.debug(f'Delete metadata: {self.baseurl}/{type}/{id}')
        del_headers = self.headers.copy()
        del del_headers['Content-Type']

        try:
            r = requests.delete(f'{self.baseurl}/{type}/{id}', headers = del_headers ,**kwargs)
        except Exception as error:
            print(f'Unexpected error when connecting to {self.baseurl}/{type}/{id}\n')
            raise error
        else:
            if r.status_code >= 300:
                print(f'HTTP error: {r.status_code} {r.reason} for {self.baseurl}/{type}/{id}',
                      f'\nResponse message: {r.text}')
                raise

    def _check_data(self, data, format):
        """Check input data type and convert Graph data to bytes"""
        if isinstance(data, rdflib.Graph):
            return data.serialize(format=format)
        else:
            return data


