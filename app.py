from fastapi import FastAPI, Request
import xml.etree.ElementTree as ET
from fastapi.responses import PlainTextResponse
from datetime import datetime
import os



app = FastAPI()

@app.post("/cw/outbound")
async def receive_xml(request: Request):
    body = await request.body()
    xml_data = body.decode("utf-8")

    # Save XML
    os.makedirs("xml_logs", exist_ok=True)
    xml_filename = f"xml_logs/cw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"

    with open(xml_filename, "w", encoding="utf-8") as f:
        f.write(xml_data)

    print("XML saved:", xml_filename)
    print("RAW XML:", xml_data[:2000])

    # Parse XML
  
    root = ET.fromstring(xml_data)
    ns = {"cw": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    job_number = root.findall(".//cw:Shipment//cw:DataContext/cw:DataSourceCollection/cw:DataSource[cw:Type='ForwardingShipment']/cw:Key", ns)
    company_code =  for ds in root.findall(".//cw:DataSource", ns):
        type_el = ds.find("cw:Type", ns)
        if type_el is not None and type_el.text == "ForwardingShipment":
            key = ds.find("cw:Key", ns)
    email = root.find(".//cw:EventUser/cw:Code", ns)

    job_number = job_number.text if job_number is not None else ""
    company_code = company_code.text if company_code is not None else ""
    email = email.text if email is not None else ""

    print("Job:", job_number)
    print("Company:", company_code)
    print("Email:", email)


    return PlainTextResponse("OK")
