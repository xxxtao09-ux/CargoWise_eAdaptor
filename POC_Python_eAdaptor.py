import os
from dotenv import load_dotenv
import http.client 
import base64 
import csv 
from logging import root
import xml.etree.ElementTree as ET

load_dotenv()

class CargoWise_eAdaptor(): 
    def __init__(self):

        self.username = os.getenv("CARGOWISE_EADAPTOR_USERNAME")
        self.password = os.getenv("CARGOWISE_EADAPTOR_PASSWORD")
        self.auth = base64.b64encode(f"{self.username}:{self.password}".encode()).decode() 
        self.endpoint = os.getenv("CARGOWISE_EADAPTOR_ENDPOINT") 
        self.namespace = os.getenv("CARGOWISE_NAMESPACE")
        self.key = input("Enter Job Number: ") 
        self.comp_code = input("Enter Company Code: ") 
        self.root = self.get_data()

    def get_data(self):

        self.ns = {"cw": self.namespace}
        conn = http.client.HTTPSConnection(os.getenv("CARGOWISE_EADAPTOR_URL"))    
        data_context = "CustomsDeclaration" if self.key.startswith("B") else "ForwardingShipment" 
        conn.request( 
            "POST", 
            self.endpoint, 
            body=f""" <UniversalShipmentRequest xmlns="{self.namespace}" version="1.1"> 
                        <ShipmentRequest>
                            <DataContext> 
                                <DataTargetCollection> 
                                    <DataTarget> 
                                    <Type>{data_context}</Type> 
                                    <Key>{self.key}</Key> </DataTarget> 
                                </DataTargetCollection> 
                                <Company> 
                                    <Code>{self.comp_code}</Code> 
                                </Company> 
                                <EnterpriseID>H56</EnterpriseID> 
                                <ServerID>PRD</ServerID> 
                            </DataContext> 
                        </ShipmentRequest> 
                    </UniversalShipmentRequest>""", 
            
            headers={ "Authorization": f"Basic {self.auth}", "Content-Type": "text/xml" } ) 
        response = conn.getresponse() 
        xml_response = response.read().decode() 
        return ET.fromstring(xml_response)
    
    def get_text(self, xpath):
        element = self.root.find(xpath, self.ns)
        return element.text if element is not None else "Not Found"
    
if __name__ == "__main__":
    eAdaptor = CargoWise_eAdaptor()

    
