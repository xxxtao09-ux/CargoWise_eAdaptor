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
    company_code =  root.find(".//cw:Shipment//cw:DataContext/cw:Company/cw:Code", ns)
    email = root.find(".//cw:EventUser/cw:Code", ns)

    job_number = job_number.text if job_number is not None else ""
    company_code = company_code.text if company_code is not None else ""
    email = email.text if email is not None else ""

    print("Job:", job_number)
    print("Company:", company_code)
    print("Email:", email)

    # Bridge: pass parsed values directly into your eAdaptor class
    eAdaptor = CargoWise_eAdaptor(
        key=job_number,
        comp_code=company_code
    )

    # Route to correct transformer (same logic as fetch_eAdaptor_data)
    if company_code.endswith("PH"):
        CargoWise_eAdaptor_PH_GEN(eAdaptor).main()
        CargoWise_eAdaptor_PH_CTN(eAdaptor).main()
    elif company_code.endswith("SG"):
        CargoWise_eAdaptor_SG_BOL(eAdaptor).main()
    elif company_code.endswith("IN"):
        CargoWise_eAdaptor_IN_CargoItineraryData(eAdaptor).main()
        CargoWise_eAdaptor_IN_CargoItemsData(eAdaptor).main()
        CargoWise_eAdaptor_IN_ContainerData(eAdaptor).main()
    else:
        print(f"Invalid Company Code: {company_code}")
        return PlainTextResponse("Invalid company code", status_code=400)

    return PlainTextResponse("OK")
    return PlainTextResponse("OK")
