from pandas import DataFrame
from requests import request

# query = https://www.aena.es/sites/Satellite?pagename=AENA_ConsultarVuelos&airport=PMI&flightType=S


class AenaFlightsRepository:

    base_url = "https://www.aena.es/sites/Satellite"
    
    def get_departing_flights(self, iata_code: str) -> DataFrame:
        # Define all parameters in the params dictionary
        params = {
            "pagename": "AENA_ConsultarVuelos",
            "airport": iata_code,
            "flightType": "S"  # S for departing flights (Salidas)
        }
        
        # Make the request with the base URL and params
        response = request("GET", self.base_url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching data from Aena: {response.status_code}")
        data = response.json()

        data = DataFrame.from_records(data)
        if data.empty:
            raise Exception("No departing flights found for the given IATA code")

        
        return data
    

        