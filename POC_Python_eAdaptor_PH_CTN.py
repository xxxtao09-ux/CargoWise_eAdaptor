import csv
from POC_Python_eAdaptor import CargoWise_eAdaptor

class CargoWise_eAdaptor_PH_CTN():  
    
    def __init__(self, eAdaptor):
        self.eAdaptor = eAdaptor
        
    def main(self):
        PH_eAdaptor = self.eAdaptor
        filename = f"edi_output/{self.eAdaptor.comp_code}_{self.eAdaptor.key}.CTN"
                   
        with open(f"{filename}", "w", newline='') as file:
            writer = csv.DictWriter(file, 
                                    quotechar='"',
                                    quoting=csv.QUOTE_ALL,
                                    
                                    
                                    fieldnames=[
                                        "Customs Office Code", 
                                        "Master Bill Number", 
                                        "House Bill Number", 
                                        "Container Number", 
                                        "Container Size", 
                                        "Container Mode", 
                                        "Seal 1", 
                                        "Seal 2", 
                                        "Seal 3", 
                                        "Sealing Party"
                                        ]) 
            writer.writeheader()
            writer.writerow({
                "Customs Office Code": "P02B", 
                "Master Bill Number": PH_eAdaptor.get_text(".//cw:Shipment//cw:WayBillNumber"),
                "House Bill Number": PH_eAdaptor.get_text(".//cw:Shipment//cw:SubShipmentCollection/cw:SubShipment/cw:WayBillNumber"),
                "Container Number": ", ".join([c.text for c in PH_eAdaptor.root.findall(".//cw:Shipment/cw:ContainerCollection/cw:Container/cw:ContainerNumber", PH_eAdaptor.ns) if c.text]),
                "Container Size": ", ".join([ct.text for ct in PH_eAdaptor.root.findall(".//cw:Shipment/cw:ContainerCollection/cw:Container/cw:ContainerType/cw:Code", PH_eAdaptor.ns) if ct.text]),    
                "Container Mode": ", ".join([ct.text for ct in PH_eAdaptor.root.findall(".//cw:Shipment/cw:ContainerCollection/cw:Container/cw:FCL_LCL_AIR/cw:Code", PH_eAdaptor.ns) if ct.text]),
                "Seal 1": ", ".join([s1.text for s1 in PH_eAdaptor.root.findall(".//cw:Shipment/cw:ContainerCollection/cw:Container/cw:Seal1", PH_eAdaptor.ns) if s1.text]),
                "Seal 2": ", ".join([s2.text for s2 in PH_eAdaptor.root.findall(".//cw:Shipment/cw:ContainerCollection/cw:Container/cw:Seal2", PH_eAdaptor.ns) if s2.text]),
                "Seal 3": ", ".join([s3.text for s3 in PH_eAdaptor.root.findall(".//cw:Shipment/cw:ContainerCollection/cw:Container/cw:Seal3", PH_eAdaptor.ns) if s3.text]),
                "Sealing Party": ", ".join([ct.text for ct in PH_eAdaptor.root.findall(".//cw:Shipment/cw:ContainerCollection/cw:Container/cw:SealPartyType/cw:Code", PH_eAdaptor.ns) if ct.text]),
            })
