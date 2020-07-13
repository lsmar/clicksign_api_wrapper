import requests
import json
from exceptions import Forbidden, WrongArgument, UnProcessableEntity, check_response
from typing import Dict


class ApiEnv():
    PROD= "production"
    SANDBOX = "sandbox"

class ClickSign:

    PROD_URL= "https://app.clicksign.com/api/v1/"
    SANDBOX_URL = "https://sandbox.clicksign.com/api/v1/"

    def __init__(self, token:str, api_env=ApiEnv.SANDBOX, timeout = 10):
        self.query_string = {'access_token': token}
        self.timeout = timeout
        self._url = self.PROD_URL if api_env==ApiEnv.PROD else self.SANDBOX_URL

    def __url(self, url):
        url = f'{self._url}{url}'
        return url

    def check_token(self)->Dict:
        resp = check_response(requests.get(self.__url('accounts'), params=self.query_string))
        return resp.json()

    def document(self):
        return self.Document(self)

    class Document:

        def __init__(self, click_sign, document_key = None):
            self.click_sign = click_sign
            if document_key:
                self.document_key = document_key

        def list_documents(self)->Dict:
            resp = check_response(requests.get(self.click_sign.__url(f'documents'), params=self.click_sign.query_string))
            return resp.json()

        def get_document(self, document_key:str = None)->Dict:
            if not self.document_key and not document_key:
                raise WrongArgument( 'document_key')    
            if not document_key:
                document_key = self.document_key

            resp = check_response(requests.get(self.click_sign.__url(f'documents/{document_key}'), params=self.click_sign.query_string))
            self.metadata = resp.json()
            self.document_key = self.metadata.get('document').get('key')
            return self.metadata
            

        def create_new_doc_from_template(self, template_key:str, doc_path:str, data:Dict)->Dict:
            # Add / to begin of doc_path and .docx to the end
            doc_path = doc_path if doc_path.startswith("/") else f'/{doc_path}'
            doc_path = doc_path if doc_path.endswith(".docx") else f'{doc_path}.docx'
            
            body = {'document':{
                'path': doc_path,
                'template':{'data':data}
            }} 

            resp = check_response(requests.post(self.click_sign._ClickSign__url(f'templates/{template_key}/documents'),json=body, params=self.click_sign.query_string))
            self.metadata = resp.json()
            self.document_key = self.metadata.get('document').get('key')
            return self.metadata

        
        def config_doc(self, **kwargs)->Dict:
            """
            kwargs = [deadline_at, auto_close, locale, sequence_enabled, remind_interval]
            """
            if not self.document_key:
                raise WrongArgument( 'document_key')    
            
            resp = check_response(requests.patch(self.click_sign._ClickSign__url(f'documents/{self.document_key}'),json=locals().get('kwargs'), params=self.click_sign.query_string))
            self.metadata = resp.json()
            return self.metadata

        def finalize(self)->bool:
            if not self.document_key:
                raise WrongArgument( 'document_key')    
            
            resp = check_response(requests.patch(self.click_sign._ClickSign__url(f'documents/{self.document_key}/finish'), params=self.click_sign.query_string))
            self.metadata = resp.json()
            return True        

        def cancel(self)->bool:
            if not self.document_key:
                raise WrongArgument( 'document_key')    
            
            resp = check_response(requests.patch(self.click_sign._ClickSign__url(f'documents/{self.document_key}/cancel'), params=self.click_sign.query_string))
            self.metadata = resp.json()
            return True

        def delete(self)->bool:
            if not self.document_key:
                raise WrongArgument( 'document_key')    
            
            resp = check_response(requests.delete(self.click_sign._ClickSign__url(f'documents/{self.document_key}'), params=self.click_sign.query_string))
            self.metadata = None
            self.document_key = None
            return True
            


try:
    print("testing")
    click_sign_api=ClickSign(token="28a706ff-55aa-4eda-8c87-fa38e322ccfd")
    data = {"Estado": "MS"}
    doc = click_sign_api.document()
    resp_doc = doc.create_new_doc_from_template(data=data, template_key="03947577-c501-44c1-837c-017f09134d54",doc_path="PFED-004/Lucas_Martins_PFED-004")
    print(doc)
    doc.config_doc(auto_close=True)
    finish = doc.finalize()
    cancelled_doc = doc.cancel()
    deleted = doc.delete()
    
except Exception as error:
    print(f'Error: {error}')
