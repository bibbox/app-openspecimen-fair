import rdflib
import requests
import logging
import json
import datetime

logger = logging.getLogger(__name__)

class FDPClient:
    DATA_FORMATS = {
        'n3': 'text/n3',
        'turtle': 'text/turtle',
        'xml': 'application/rdf+xml',
        'json-ld': 'application/ld+json',
        'nt': 'application/n-triples'
    }


    def __init__(self, baseurl, email, password,publicurl='',
                 catalog_template='./test-data/catalog_template.ttl',
                 dataset_template='./test-data/dataset_template.ttl',
                 distribution_template='./test-data/distribution_template.ttl'
                 ):
        self.baseurl = baseurl.rstrip('/')
        if publicurl is not None and publicurl != "":
            self.publicurl = publicurl.rstrip('/')
        else:
            self.publicurl = self.baseurl
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.headers['Authorization'] = f'Bearer {self.gettoken(email, password)}'
        del self.headers['Accept']
        self.catalog_template = self._load_template(catalog_template)
        self.dataset_template = self._load_template(dataset_template)
        self.distribution_template = self._load_template(distribution_template)


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
        create_headers=self.headers.copy()
        create_headers.update({'Content-Type': self.DATA_FORMATS[format]})
        #print(create_headers)
        try:
            data = self._check_data(data, format)
            r = requests.post(f'{self.baseurl}/{type}', data=data, headers=create_headers)
            return r.headers['Location'].lstrip(f'{self.publicurl}/{type}/')
        except Exception as error:
            print(f'Unexpected error when connecting to {self.baseurl}/{type}\n')
            raise error
        else:
            if r.status_code >= 300:
                print(f'HTTP error: {r.status_code} {r.reason} for {self.baseurl}/{type}',
                      f'\nResponse message: {r.text}')
                raise

    def read(self, type='', id='' , subtype='',format='turtle', **kwargs):
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
        url = f'{self.baseurl}'
        if type is not None and type != "":
            url = f'{url}/{type}'
            if id is not None and id != "":
                url = f'{url}/{id}'
            if subtype is not None and subtype != "":
                url = f'{url}/{subtype}'

        logger.debug(f'Read metadata: {url}')
        read_headers = self.headers.copy()
        read_headers.update({'Content-Type': self.DATA_FORMATS[format]})

        try:
            r = requests.get(url, headers=read_headers, **kwargs)
        except Exception as error:
            print(f'Unexpected error when connecting to {url}\n')
            raise error
        else:
            if r.status_code != 200:
                print(f'HTTP error: {r.status_code} {r.reason} for {url}',
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

    def update(self,type='', id='' , subtype='', data="", format='turtle', **kwargs):
        """Send an update request.
        Args:
            url(str): URL for updating a metadata.
            data(str, bytes, file-like object or :class:`rdflib.Graph`):
                the content of metadata to send in the request body.
            format (str, optional): the format of the metadata.
                This argument overwrites the request header ``content-type``.
                Available options are 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
                Defaults to 'turtle'.
            **kwargs: Optional arguments that :func:`requests.request` takes.
        """
        url = f'{self.baseurl}'
        if type is not None and type != "":
            url = f'{url}/{type}'
            if id is not None and id != "":
                url = f'{url}/{id}'
            if subtype is not None and subtype != "":
                url = f'{url}/{subtype}'

        logger.debug(f'Update metadata on {url} with the content: \n{data}')
        update_headers = self.headers.copy()
        update_headers.update({'Content-Type': self.DATA_FORMATS[format]})

        try:
            data = self._check_data(data, format)
            r = requests.put(f'{url}', data=data, headers=update_headers, **kwargs)
            #print(f'{r.status_code} {r.reason}')
        except Exception as error:
            print(f'Unexpected error when connecting to {url}\n')
            raise error
        else:
            if r.status_code >= 300:
                print(f'HTTP error: {r.status_code} {r.reason} for {url}',
                      f'\nResponse message: {r.text}')
                raise

    def _check_data(self, data, format):
        """Check input data type and convert Graph data to bytes"""
        if isinstance(data, rdflib.Graph):
            return data.serialize(format=format)
        else:
            return data

    def _load_template(self, path):
        with open(path) as f:
            data = f.read()

        return data.replace("§§BASEURL",self.publicurl)
        #graph = rdflib.Graph()
        #graph.parse(path, format='ttl')
        #qres = graph.query("SELECT ?s ?o WHERE { ?s dcterms:hasVersion ?o }")
        #for row in qres:
        #    print(f"{row.s} dcterms:hasVersion {row.o}")

    def createCatalogRDF(self,title,version,publisher,ispartof=None,**kwargs):
        catalog = self.catalog_template
        catalog = catalog.replace(f'§§TITLE', str(title))
        if ispartof is None:
            catalog = catalog.replace(f'§§ISPARTOF', str(self.publicurl))
        else:
            catalog = catalog.replace(f'§§ISPARTOF', str(ispartof))
        catalog = catalog.replace(f'§§VERSION', str(version))
        catalog = catalog.replace(f'§§PUBLISHER', str(publisher))

        for key, value in kwargs.items():
            catalog = catalog.replace(f'§§{key}',str(value))

        result_catalog=""
        for line in catalog.split('\n'):
            if line.find('§§')>0:
                continue
            result_catalog=f'{result_catalog}\n{line}'
        result_catalog=result_catalog.strip()
        return result_catalog

    def createDatasetRDF(self, title, catalogid, version, publisher, themes_list, **kwargs):
        dataset = self.dataset_template
        dataset = dataset.replace(f'§§TITLE', str(title))
        dataset = dataset.replace(f'§§CATALOGID', str(catalogid))
        dataset = dataset.replace(f'§§VERSION', str(version))
        dataset = dataset.replace(f'§§PUBLISHER', str(publisher))

        themes_string = self._join_list_to_string(themes_list, seperator=">, <", prefix="<", suffix=">")
        dataset = dataset.replace('§§THEMES', themes_string)

        for key, value in kwargs.items():
            if key in ['ISSUED','MODIFIED']:
                dataset = dataset.replace(f'§§{key}', self.dateTimeToXSDString(value))
                continue
            if key == "KEYWORDS":
                keywords_string = self._join_list_to_string(value,seperator="\", \"",prefix="\"",suffix="\"")
                dataset = dataset.replace(f'§§{key}', keywords_string)
                continue
            dataset = dataset.replace(f'§§{key}',str(value))

        result_=""
        for line in dataset.split('\n'):
            if line.find('§§')>0:
                continue
            result_=f'{result_}\n{line}'
        result_=result_.strip()
        return result_

    def createDistributionRDF(self, title, datasetid, version, publisher, mediatype, **kwargs):
        dataset = self.distribution_template
        dataset = dataset.replace(f'§§TITLE', str(title))
        dataset = dataset.replace(f'§§DATASETID', str(datasetid))
        dataset = dataset.replace(f'§§VERSION', str(version))
        dataset = dataset.replace(f'§§PUBLISHER', str(publisher))
        dataset = dataset.replace(f'§§MEDIATYPE', str(mediatype))


        for key, value in kwargs.items():
            if key in ['ISSUED','MODIFIED']:
                dataset = dataset.replace(f'§§{key}', self.dateTimeToXSDString(value))
                continue
            dataset = dataset.replace(f'§§{key}',str(value))

        result_=""
        for line in dataset.split('\n'):
            if line.find('§§')>0:
                continue
            result_=f'{result_}\n{line}'
        result_=result_.strip()
        return result_

    def dateTimeToXSDString(self,date_obj):
        if isinstance(date_obj,datetime.datetime):
            return f'"{date_obj.isoformat()}"^^xsd:dateTime'
        return date_obj

    def _join_list_to_string(self, elements,seperator, prefix,suffix):
        if isinstance(elements, list):
            ret_string = seperator.join(elements)
            ret_string = f'{prefix}{ret_string}{suffix}'
            return ret_string

        return str(elements)



