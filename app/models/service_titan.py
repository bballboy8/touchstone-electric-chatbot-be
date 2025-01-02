from pydantic import BaseModel
from datetime import datetime

class ContactTypeEnum(str):
    Phone = "Phone"
    Email = "Email"
    Fax = "Fax"
    MobilePhone = "MobilePhone"



class ServiceTitanCustomerAddress(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    country: str

class ServiceTitanCustomerNewLocation(BaseModel):
    name: str
    address: ServiceTitanCustomerAddress

class ServiceTitanCustomerContact(BaseModel):
    type: str
    value: str


class ServiceTitanCustomer(BaseModel):
    name: str
    type: str
    locations: list[ServiceTitanCustomerNewLocation]
    address: ServiceTitanCustomerAddress

class ServiceTitanBookingRequest(BaseModel):
    source: str
    name: str
    summary: str
    isFirstTimeClient: bool
    contacts: list[ServiceTitanCustomerContact]
    start: str
    isSendConfirmationEmail: bool

class CreateContact(BaseModel):
    name: str
