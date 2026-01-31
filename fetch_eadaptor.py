import http.client
import base64
import csv
import xml.etree.ElementTree as ET
from io import StringIO


def fetch_eadaptor_csv(job_number: str, company_code: str) -> StringIO:
    auth = base64.b64encode(
        "HONEASHKG:h184livEtkJ/IxYOanBQmqjs".encode()
    ).decode()

    data_context = (
        "CustomsDeclaration"
        if job_number.startswith("B")
        else "ForwardingShipment"
    )

    conn = http.client.HTTPSConnection("H56PRDservices.wisegrid.net")
    conn.request(
        "POST",
        "/eAdaptor",
        body=f"""
        <UniversalShipmentRequest xmlns="http://www.cargowise.com/Schemas/Universal/2011/11" version="1.1">
            <ShipmentRequest>
                <DataContext>
                    <DataTargetCollection>
                        <DataTarget>
                            <Type>{data_context}</Type>
                            <Key>{job_number}</Key>
                        </DataTarget>
                    </DataTargetCollection>
                    <Company>
                        <Code>{company_code}</Code>
                    </Company>
                    <EnterpriseID>H56</EnterpriseID>
                    <ServerID>PRD</ServerID>
                </DataContext>
            </ShipmentRequest>
        </UniversalShipmentRequest>
        """,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "text/xml"
        }
    )

    response = conn.getresponse()
    xml_response = response.read().decode()

    root = ET.fromstring(xml_response)

    ns = {"cw": "http://www.cargowise.com/Schemas/Universal/2011/11"}

    company_name = root.find(
        ".//cw:Shipment/cw:DataContext/cw:Company/cw:Name",
        ns
    )

    server_id = root.find(
        ".//cw:Shipment/cw:DataContext/cw:ServerID",
        ns
    )

    # Write CSV to memory (not disk)
    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["Server ID", "Company Name"]
    )
    writer.writeheader()
    writer.writerow({
        "Server ID": server_id.text if server_id is not None else "",
        "Company Name": company_name.text if company_name is not None else ""
    })

    output.seek(0)
    return output
