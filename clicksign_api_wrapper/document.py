from __future__ import annotations
from typing import Dict, List, Union
from .signer import SignatureAsTypes, Signer
from .list_class import ListClass


class Document:
    def __init__(self, click_sign: 'ClickSign', metadata):
        self.metadata = metadata
        self.key = None

        for key, item in metadata["document"].items():
            setattr(self, key, item)

        self.click_sign = click_sign

    def config_doc(self, **kwargs) -> Dict:
        """
        kwargs = [deadline_at, auto_close, locale, sequence_enabled, remind_interval]
        """
        return self.click_sign.config_doc(self.key, **kwargs)

    def finalize(self) -> Document:
        return self.click_sign.finalize_doc(self.key)

    def cancel(self) -> Document:
        return self.click_sign.cancel_doc(self.key)

    def delete(self) -> bool:
        return self.click_sign.delete_doc(self.key)

    def add_signer(self, signer: Union[Signer, str],
                   sign_as: SignatureAsTypes) -> ListClass:
        if isinstance(signer, str):
            signer = Signer(self, signer_key=signer)
        return self.click_sign.add_signer_to_document(document_key=self.key,
                                                      signer_key=signer.key,
                                                      sign_as=sign_as)
