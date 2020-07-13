import requests
from .exceptions import Forbidden, UnProcessableEntity, check_response
from .signer import SignatureAuthTypes, Signer
from typing import Dict, List
from .document import Document
from .batch import Batch
from .list_class import ListClass


class ApiEnv():
    """Class used just to set Api Environment types PROD and SANDBOX
    """
    PROD = "production"
    SANDBOX = "sandbox"


class ClickSign:
    """Initiate a instance of this  class to interact with the Click Sign service.
    """
    PROD_URL = "https://app.clicksign.com/api/v1/"
    SANDBOX_URL = "https://sandbox.clicksign.com/api/v1/"

    def __init__(self,
                 token: str,
                 api_env=ApiEnv.SANDBOX,
                 timeout: float = 10):
        """Class constructor

        Args:
            token (str): Your ClickSign token
            api_env ([type], optional): Set the environment as ApiEnv.SANDBOX or ApiEnv.PROD. Defaults to ApiEnv.SANDBOX.
            timeout (float, optional): Set a time out in seconds for all api requests. Defaults to 10.
        """
        self.query_string = {'access_token': token}
        self.timeout = timeout
        self.signers_list = []
        self._url = self.PROD_URL if api_env == ApiEnv.PROD else self.SANDBOX_URL

    def __url(self, url: str) -> str:
        """Helper function to format API endpoints.

        Args:
            url (str): The service that you want to access in the API.

        Returns:
            str: Complete url to access the API
        """
        url = f'{self._url}{url}'
        return url

    def check_token(self) -> Dict:
        """Check if the token that was used to initialize the service is valid.

        Returns:
            Dict: Some data about the account, that is related with the provide token
        """
        resp = check_response(
            requests.get(self.__url('accounts'), params=self.query_string))
        return resp.json()

    def create_new_batch(self,
                         docs_list: List[str],
                         signer_key: str,
                         summary: bool = True) -> Batch:
        """New Batch constructor. Use this when the signer have more than one document to sign 

        Args:
            docs_list (List[str]): A List of documents key to sign all in one.
            signer_key (str): The signer key, to create the batch.
            summary (bool, optional): Show the documents list as a summary `True` or show each document `False`. Defaults to True.

        Returns:
            Batch: With all data related.
        """

        body = {
            'batch': {
                'signer_key': signer_key,
                'document_keys': docs_list,
                'summary': summary
            }
        }

        resp = check_response(
            requests.post(self.__url('batches'),
                          json=body,
                          params=self.query_string))
        metadata = resp.json()
        return Batch(metadata)

    def list_documents(self) -> List[Document]:
        """Get all Documents

        Returns:
            List[Document]: All Documents
        """
        resp = check_response(
            requests.get(self.__url(f'documents'), params=self.query_string))
        list_of_metadata = resp.json()
        return List(
            map(lambda metadata: Document(self, metadata), list_of_metadata))

    def get_document(self, document_key: str) -> Document:
        """Get one document.

        Args:
            document_key (str): The key of the document that you want.

        Returns:
            Document: The required Document
        """
        resp = check_response(
            requests.get(self.__url(f'documents/{document_key}'),
                         params=self.query_string))
        metadata = resp.json()

        return Document(self, metadata)

    #region ### Document Methods ###
    def create_new_doc_from_template(self, template_key: str, doc_path: str,
                                     data: Dict) -> Document:
        """Create a new document from a template.

        Args:
            template_key (str): The template key that you want to use as base document.
            doc_path (str): The new document path (folder location and file name)
            data (Dict): A dict with all customizable fields in the template.

        Returns:
            Document: The new Document with all custom data provide. 
        """

        # Add / to begin of doc_path and .docx to the end
        doc_path = doc_path if doc_path.startswith("/") else f'/{doc_path}'
        doc_path = doc_path if doc_path.endswith(
            ".docx") else f'{doc_path}.docx'

        body = {'document': {'path': doc_path, 'template': {'data': data}}}

        resp = check_response(
            requests.post(self.__url(f'templates/{template_key}/documents'),
                          json=body,
                          params=self.query_string))
        metadata = resp.json()
        return Document(self, metadata)

    def config_doc(self, document_key: str, **kwargs) -> Document:
        """Use the configure a document.

        Args:
            document_key (str): The document key that you want to configure
            kwargs: Pass those vars as kwargs [deadline_at, auto_close, locale, sequence_enabled, remind_interval] to set the configuration
        
        Returns:
            Document: The Document with the new configuration. 
        """
        resp = check_response(
            requests.patch(self.__url(f'documents/{document_key}'),
                           json=locals().get('kwargs'),
                           params=self.query_string))
        metadata = resp.json()

        return Document(self, metadata)

    def finalize_doc(self, document_key: str) -> Document:
        """Manually finalize a Document

        Args:
            document_key (str): The document key that you want to finalize

        Returns:
            Document: The Document that was finalized 
        """
        resp = check_response(
            requests.patch(self.__url(f'documents/{self.document_key}/finish'),
                           params=self.query_string))
        metadata = resp.json()
        return Document(self, metadata)

    def cancel_doc(self, document_key: str) -> Document:
        resp = check_response(
            requests.patch(self.__url(f'documents/{self.document_key}/cancel'),
                           params=self.query_string))
        metadata = resp.json()
        return Document(self, metadata)

    def delete_doc(self, document_key: str) -> bool:
        resp = check_response(
            requests.delete(self.__url(f'documents/{self.document_key}'),
                            params=self.query_string))
        metadata = None
        document_key = None
        return True

    #endregion ### Document Methods ###

    #region ### Signer Methods ###
    def create_new_signer(self,
                          auths: SignatureAuthTypes,
                          name: str = None,
                          email: str = None,
                          phone_number: str = None,
                          documentation: str = None,
                          birthday: str = None,
                          has_documentation: bool = True) -> Signer:

        body = {
            'signer': {
                'email': email,
                'phone_number': phone_number,
                'auths': [auths],
                'name': name,
                'documentation': documentation,
                'birthday': birthday,
                'has_documentation': has_documentation
            }
        }

        resp = check_response(
            requests.post(self.__url('signers'),
                          json=body,
                          params=self.query_string))
        metadata = resp.json()
        return Signer(self, metadata)

    def add_signer_to_document(self, document_key: str, signer_key: str,
                               sign_as: str) -> ListClass:
        body = {
            "list": {
                "document_key": document_key,
                "signer_key": signer_key,
                "sign_as": sign_as
            }
        }
        resp = check_response(
            requests.post(self.__url('lists'),
                          json=body,
                          params=self.query_string))
        metadata = resp.json()
        return ListClass(metadata)

    def get_signer(self, signer_key: str) -> Signer:
        resp = check_response(
            requests.get(self.__url(f'signers/{signer_key}'),
                         params=self.query_string))
        metadata = resp.json()
        return Signer(self, metadata)

    #endregion ### Signer Methods ###