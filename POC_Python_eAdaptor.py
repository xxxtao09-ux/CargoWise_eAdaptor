import os
from dotenv import load_dotenv
import http.client 
import base64 
import csv 
from logging import root
import xml.etree.ElementTree as ET
import smtplib
from email.message import EmailMessage
import pandas as pd

load_dotenv()

class CargoWise_eAdaptor(): 
    def __init__(self,key,comp_code):

        self.username = os.getenv("CARGOWISE_EADAPTOR_USERNAME")
        self.password = os.getenv("CARGOWISE_EADAPTOR_PASSWORD")
        self.auth = base64.b64encode(f"{self.username}:{self.password}".encode()).decode() 
        self.endpoint = os.getenv("CARGOWISE_EADAPTOR_ENDPOINT") 
        self.namespace = os.getenv("CARGOWISE_NAMESPACE")
        self.key = key
        self.comp_code = comp_code
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

    def get_job_number(self):
        return self.get_text(
            ".//cw:Shipment//cw:DataContext/cw:DataSourceCollection"
            "/cw:DataSource[cw:Type='ForwardingShipment']/cw:Key"
        )

    def get_company_code(self):
        return self.get_text(
            ".//cw:Shipment//cw:DataContext/cw:Company/cw:Code"
        )

    def get_user_email(self):
        user_code = self.get_text(
            ".//cw:Shipment//cw:DataContext/cw:EventUser/cw:Code"
        )
        df = pd.read_excel("User_Account_Details.xlsx")
        result = df[df["Code"] == user_code]
        return result.iloc[0]["Email Address"] if not result.empty else None

    def extract_header_details(self):
        return {
            "job_number":   self.get_job_number(),
            "company_code": self.get_company_code(),
            "user_email":   self.get_user_email(),
        }

    def send_email(recipient, file_path):
        msg = EmailMessage()
        msg["Subject"] = "CargoWise EDI Output"
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = recipient
        msg.set_content("Please find attached EDI output files.")
    
        for file_path in file_paths:
            with open(file_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=os.path.basename(file_path)
                )
    
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            smtp.send_message(msg)
    
        print("Email sent to:", recipient)
    
if __name__ == "__main__":
    eAdaptor = CargoWise_eAdaptor()

    
