import requests


class LookupClient:
    __API_KEYS = {
        # Returns: object: https://docs.virustotal.com/reference/files
        "virustotal": "e3848f6c5ae68135e320ec90a73ebf74986c8bb5c3e7afac7fbccc16507ff337",
    }

    def __init__(self, website):
        self.lookupWebsite = website

    def lookup(self, hash):
        """
        Performs a lookup for a given hash using a specific website API.

        Args:
            hash (str): The hash value to lookup.

        Returns:
            dict or None: The response from the API in JSON format if the request is successful, 
                          otherwise None.
        """
        link = self.lookupWebsite + hash
        
        headers = {}
        if ("viriustotal.com" in link):
            header = {
                "x-apikey": self.__API_KEYS["virustotal"]
            }

        response = requests.get(
            link, 
            headers=header
        )

        # Check the response we get from the service
        if (response.status_code == 200):
            return response.json()
        
        else:
            return None
        

