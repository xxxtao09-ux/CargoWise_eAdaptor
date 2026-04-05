from POC_Python_eAdaptor import CargoWise_eAdaptor
from POC_Python_eAdaptor_PH_GEN import CargoWise_eAdaptor_PH_GEN
from POC_Python_eAdaptor_SG import CargoWise_eAdaptor_SG_BOL
from POC_Python_eAdaptor_PH_CTN import CargoWise_eAdaptor_PH_CTN
from POC_Python_eAdaptor_IN import CargoWise_eAdaptor_IN_CargoItineraryData
from POC_Python_eAdaptor_IN import CargoWise_eAdaptor_IN_CargoItemsData
from POC_Python_eAdaptor_IN import CargoWise_eAdaptor_IN_ContainerData
from fastapi import FastAPI, Request
import xml.etree.ElementTree as ET
from fastapi.responses import PlainTextResponse
from datetime import datetime
import os
import pandas as pd
from openpyxl import Workbook
import smtplib
from email.message import EmailMessage

def send_email(recipient, file_paths):
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

    print("Email sent:", recipient)

app = FastAPI()

@app.post("/cw/outbound")
async def receive_xml(request: Request):
    body = await request.body()
    xml_data = body.decode("utf-8")

    # Save XML
    os.makedirs("xml_logs", exist_ok=True)
    os.makedirs("edi_output", exist_ok=True)
    xml_filename = f"xml_logs/cw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"

    with open(xml_filename, "w", encoding="utf-8") as f:
        f.write(xml_data)

    print("XML saved:", xml_filename)
    print("RAW XML:", xml_data[:2000])

    # Parse XML
  
    root = ET.fromstring(xml_data)
    ns = {"cw": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    job_number = root.find(".//cw:Shipment//cw:DataContext/cw:DataSourceCollection/cw:DataSource[cw:Type='ForwardingShipment']/cw:Key", ns)
    company_code =  root.find(".//cw:Shipment//cw:DataContext/cw:Company/cw:Code", ns)
    user_code = root.find(".//cw:Shipment//cw:DataContext/cw:EventUser/cw:Code", ns)
    

    job_number = job_number.text if job_number is not None else ""
    company_code = company_code.text if company_code is not None else ""
    user_code = user_code.text if user_code is not None else ""
    

    print("Job:", job_number)
    print("Company:", company_code)
    print("User:", user_code)
    

    # Bridge: pass parsed values directly into your eAdaptor class
    eAdaptor = CargoWise_eAdaptor(
        key=job_number,
        comp_code=company_code,
        user_code=user_code
    )

    user_email = eAdaptor.get_user_email()
    print("Recipient Email:", user_email)

    # Route to correct transformer (same logic as fetch_eAdaptor_data)
    generated_files = []
    
    if company_code.endswith("PH"):
        file1 = CargoWise_eAdaptor_PH_GEN(eAdaptor).main()
        file2 = CargoWise_eAdaptor_PH_CTN(eAdaptor).main()
        generated_files.extend([file1, file2])
    
    elif company_code.endswith("SG"):
        file1 = CargoWise_eAdaptor_SG_BOL(eAdaptor).main()
        generated_files.append(file1)
    
    elif company_code.endswith("IN"):
        file1 = CargoWise_eAdaptor_IN_CargoItineraryData(eAdaptor).main()
        file2 = CargoWise_eAdaptor_IN_CargoItemsData(eAdaptor).main()
        file3 = CargoWise_eAdaptor_IN_ContainerData(eAdaptor).main()
        generated_files.extend([file1, file2, file3])
    
    if user_email:
        send_email(user_email, generated_files)
    
    return PlainTextResponse("OK")

@app.get("/files")
def list_files():
    import os
    if not os.path.exists("edi_output"):
        return {"files": []}
    return {"files": os.listdir("edi_output")}

