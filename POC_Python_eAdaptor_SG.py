import csv
from POC_Python_eAdaptor import CargoWise_eAdaptor

class CargoWise_eAdaptor_SG_BOL():

    def __init__(self, eAdaptor):
        self.eAdaptor = eAdaptor

    def main(self):
        SG_eAdaptor = self.eAdaptor
        filename = f"edi_output/{self.eAdaptor.comp_code}_{self.eAdaptor.key}.csv"
                   
        with open(f"{filename}", "a", newline='') as file:
            writer = csv.DictWriter(file, 
                                    fieldnames=[
                                                "Function",
                                                "Vessel Name",
                                                "Vessel Voyage",
                                                "Vessel Port of Discharge",
                                                "Bill of Lading",
                                                "Master Bill of Lading",
                                                "Bill of Lading Remarks",
                                                "Instruction Type",
                                                "Original Port of Load",
                                                "Port of Load",
                                                "Port of Discharge",
                                                "Destination",
                                                "Place of Receipt",
                                                "Place of Delivery",
                                                "Consignee",
                                                "Consignee UEN",
                                                "Consignee Address",
                                                "Shipper",
                                                "Shipper UEN",
                                                "Shipper Address",
                                                "Notify Party Name",
                                                "Notify Party UEN",
                                                "Notify Party Contact Number",
                                                "Notify Party Email",
                                                "Notify Party Address",
                                                "Freight Forwarder Name",
                                                "Freight Forwarder UEN",
                                                "Freight Forwarder Contact Number",
                                                "Freight Forwarder Email",
                                                "Freight Forwarder Address",
                                                "Stevedore Name",
                                                "Stevedore UEN",
                                                "Stevedore Contact Number",
                                                "Stevedore Email",
                                                "Stevedore Address",
                                                "Cargo Agent Name",
                                                "Cargo Agent UEN",
                                                "Cargo Agent Contact Number",
                                                "Cargo Agent Email",
                                                "Cargo Agent Address",
                                                "Item No",
                                                "Package Type",
                                                "HS Code",
                                                "Package Quantity",
                                                "Weight",
                                                "Measurement",
                                                "Handling Instruction",
                                                "Cargo Description",
                                                "Mark and No",
                                                "Dangerous Goods Indicator",
                                                "IMO Class",
                                                "UNDG Number",
                                                "Flashpoint (Celsius)",
                                                "Packing Group",
                                                "Container Number",
                                                "Container Status",
                                                "ISO Code",
                                                "Gross Weight",
                                                "Seal Number Carrier"                                               

                                    ]) 
            writer.writeheader()
            writer.writerow({
                "Function": "",
                "Vessel Name": SG_eAdaptor.get_text(".//cw:Shipment/cw:VesselName"),
                "Vessel Voyage": SG_eAdaptor.get_text(".//cw:Shipment/cw:VoyageFlightNo"),
                "Vessel Port of Discharge": SG_eAdaptor.get_text(".//cw:Shipment/cw:PortOfDischarge/cw:Code"),
                "Bill of Lading": SG_eAdaptor.get_text(".//cw:Shipment/cw:WayBillNumber"),
                "Master Bill of Lading": SG_eAdaptor.get_text(".//cw:Shipment/cw:MasterWayBillNumber"),
                "Bill of Lading Remarks": "",
                "Instruction Type": "",
                "Original Port of Load": SG_eAdaptor.get_text(".//cw:Shipment/cw:OriginalPortOfLoad/cw:Code"),
                "Port of Load": SG_eAdaptor.get_text(".//cw:Shipment/cw:PortOfLoading/cw:Code"),
                "Port of Discharge": SG_eAdaptor.get_text(".//cw:Shipment/cw:PortOfDischarge/cw:Code"),
                "Destination": SG_eAdaptor.get_text(".//cw:Shipment/cw:Destination/cw:Code"),
                "Place of Receipt": SG_eAdaptor.get_text(".//cw:Shipment/cw:PlaceOfReceipt/cw:Code"),
                "Place of Delivery": SG_eAdaptor.get_text(".//cw:Shipment/cw:PlaceOfDelivery/cw:Code"),
                "Consignee": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ConsigneeDocumentaryAddress']/cw:CompanyName"),
                "Consignee UEN": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ConsigneeDocumentaryAddress']/cw:SetUEN"),
                "Consignee Address": ", ".join(filter(None, [
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ConsigneeDocumentaryAddress']/cw:Address1"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ConsigneeDocumentaryAddress']/cw:Address2"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ConsigneeDocumentaryAddress']/cw:City"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ConsigneeDocumentaryAddress']/cw:SetState"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ConsigneeDocumentaryAddress']/cw:PostalCode"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ConsigneeDocumentaryAddress']/cw:Country/cw:Code")
                ])),
                "Shipper": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ShipperDocumentaryAddress']/cw:CompanyName"),
                "Shipper UEN": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ShipperDocumentaryAddress']/cw:SetUEN"),
                "Shipper Address": ", ".join(filter(None, [
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ShipperDocumentaryAddress']/cw:Address1"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ShipperDocumentaryAddress']/cw:Address2"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ShipperDocumentaryAddress']/cw:City"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ShipperDocumentaryAddress']/cw:SetState"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ShipperDocumentaryAddress']/cw:PostalCode"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='ShipperDocumentaryAddress']/cw:Country/cw:Code")
                ])),
                "Notify Party Name": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:CompanyName"),
                "Notify Party UEN": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:SetUEN"),
                "Notify Party Contact Number": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:ContactNumber"),
                "Notify Party Email": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:Email"),
                "Notify Party Address": ", ".join(filter(None, [
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:Address1"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:Address2"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:City"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:SetState"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:PostalCode"),
                    SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/cw:OrganizationAddress[cw:AddressType='NotifyPartyDocumentaryAddress']/cw:Country/cw:Code")
                ])),
                "Stevedore Name": "",
                "Stevedore UEN": "",
                "Stevedore Contact Number": "",
                "Stevedore Email": "",
                "Stevedore Address": "",
                "Cargo Agent Name":
                    SG_eAdaptor.get_text(
                        ".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/"
                        "cw:OrganizationAddress[cw:AddressType='SendingForwarderAddress']/cw:CompanyName"
                    ) if SG_eAdaptor.get_text(".//cw:Shipment//PortOfLoading//cw:Code").startswith("SG")
                    and not SG_eAdaptor.get_text(".//cw:Shipment//PortOfDischarge//cw:Code").startswith("SG")
                    else SG_eAdaptor.get_text(
                        ".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OrganizationAddressCollection/"
                        "cw:OrganizationAddress[cw:AddressType='ReceivingForwarderAddress']/cw:CompanyName"
                    ) if not SG_eAdaptor.get_text(".//cw:Shipment//PortOfLoading//cw:Code").startswith("SG")
                    and SG_eAdaptor.get_text(".//cw:Shipment//PortOfDischarge//cw:Code").startswith("SG")
                    else "",

                "Cargo Agent UEN": "",
                "Cargo Agent Contact Number": "",
                "Cargo Agent Email": "",
                "Cargo Agent Address": "",
                "Item No": "",
                "Package Type":SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:OuterPacksPackageType/cw:Code"),
                "HS Code": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:PackingLineCollection/cw:PackingLine/cw:HarmonisedCode"),
                "Package Quantity": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:PackingLineCollection/cw:PackingLine/cw:PackQty"),
                "Weight": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:PackingLineCollection/cw:PackingLine/cw:Weight"),
                "Measurement": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:PackingLineCollection/cw:PackingLine/cw:Volume"),
                "Handling Instruction": "",
                "Cargo Description": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:PackingLineCollection/cw:PackingLine/cw:DetailedDescription"),
                "Mark and No": SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:PackingLineCollection/cw:PackingLine/cw:MarksAndNos"),
                "Dangerous Goods Indicator": "",
                "IMO Class": "",                                
                "UNDG Number": "",
                "Flashpoint (Celsius)": "",
                "Packing Group": "",
                "Container Number":  SG_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:PackingLineCollection/cw:PackingLine/cw:ContainerNumber"),
                "Container Status": "",
                "ISO Code": "",
                "Gross Weight": "",
                "Seal Number Carrier":""  

            })
