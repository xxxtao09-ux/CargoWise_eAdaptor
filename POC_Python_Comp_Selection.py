from POC_Python_eAdaptor import CargoWise_eAdaptor
from POC_Python_eAdaptor_PH_GEN import CargoWise_eAdaptor_PH_GEN
from POC_Python_eAdaptor_SG import CargoWise_eAdaptor_SG_BOL
from POC_Python_eAdaptor_PH_CTN import CargoWise_eAdaptor_PH_CTN
from POC_Python_eAdaptor_IN import CargoWise_eAdaptor_IN_CargoItineraryData
from POC_Python_eAdaptor_IN import CargoWise_eAdaptor_IN_CargoItemsData
from POC_Python_eAdaptor_IN import CargoWise_eAdaptor_IN_ContainerData

class fetch_eAdaptor_data():

    @staticmethod
    def eadaptor_instance():

        eAdaptor = CargoWise_eAdaptor()  

        if eAdaptor.comp_code.endswith("PH"):
            CargoWise_eAdaptor_PH_GEN(eAdaptor).main()
            CargoWise_eAdaptor_PH_CTN(eAdaptor).main()

        elif eAdaptor.comp_code.endswith("SG"):
            CargoWise_eAdaptor_SG_BOL(eAdaptor).main()

        elif eAdaptor.comp_code.endswith("IN"):
            CargoWise_eAdaptor_IN_CargoItineraryData(eAdaptor).main()
            CargoWise_eAdaptor_IN_CargoItemsData(eAdaptor).main()
            CargoWise_eAdaptor_IN_ContainerData(eAdaptor).main()

        else:
            print("Invalid Company Code")


if __name__ == "__main__":
    fetch_eAdaptor_data.eadaptor_instance()