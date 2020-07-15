from __future__ import annotations
from typing import Dict


class SignatureAuthTypes():
    """Methods of sign auth:
    - API: Via API
    - EMAIL: Via e-mail
    - SMS: Via SMS
    - WHATSAPP: Via whatsapp
    """
    API = 'api'
    EMAIL = 'email'
    SMS = 'sms'
    WHATSAPP = 'whatsapp'


class SignatureAsTypes():
    """Sign as Types:

    - SIGN: Assinar
    - APPROVE: Assinar para aprovar
    - PARTY: Assinar como parte
    - WITNESS: Assinar como testemunha
    - INTERVENING: Assinar como interveniente
    - RECEIPT: Assinar para acusar recebimento
    - ENDORSER: Assinar como endossante
    - ENDORSEE: Assinar como endossatário
    - ADMINISTRATOR: Assinar como administrador
    - GUARANTOR: Assinar como avalista
    - TRANSFEROR: Assinar como cedente
    - TRANSFEREE: Assinar como cessionário
    - CONTRACTEE: Assinar como contratada
    - CONTRACTOR: Assinar como contratante
    - JOINT_DEBTOR: Assinar como devedor solidário
    - ISSUER: Assinar como emitente
    - MANAGER: Assinar como gestor
    - BUYER: Assinar como parte compradora
    - SELLER: Assinar como parte vendedora
    - ATTORNEY: Assinar como procurador
    - LEGAL_REPRESENTATIVE: Assinar como representante legal
    - CO_RESPONSIBLE: Assinar como responsável solidário
    - VALIDATOR: Assinar como validador
    - RATIFY: Assinar para homologar
    """
    ACKNOWLEDGE = 'acknowledge'
    ADMINISTRATOR = 'administrator'
    APPROVE = 'approve'
    ATTORNEY = 'attorney'
    BUYER = 'buyer'
    CO_RESPONSIBLE = 'co_responsible'
    CONTRACTEE = 'contractee'
    CONTRACTOR = 'contractor'
    ENDORSEE = 'endorsee'
    ENDORSER = 'endorser'
    GUARANTOR = 'guarantor'
    INTERVENING = 'intervening'
    ISSUER = 'issuer'
    JOINT_DEBTOR = 'joint_debtor'
    LEGAL_REPRESENTATIVE = 'legal_representative'
    MANAGER = 'manager'
    PARTY = 'party'
    RATIFY = 'ratify'
    RECEIPT = 'receipt'
    SELLER = 'seller'
    SIGN = 'sign'
    TRANSFEROR = 'transferor'
    VALIDATOR = 'validator'
    WITNESS = 'witness'


class Signer:
    def __init__(self,
                 click_sign: 'ClickSign',
                 metadata: Dict = None,
                 signer_key: str = None):
        self.click_sign = click_sign
        if signer_key and not metadata:
            self.key = signer_key
        if metadata:
            for key, item in metadata["signer"].items():
                setattr(self, key, item)
