import requests
import os

def load_env_variables(env_file=".env"):
    with open(env_file) as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Example usage
load_env_variables()

class ZaraAvailabilityChecker:
    def __init__(self, code, which_size):
        self.code = code
        self.which_size = which_size
        self.base_url = "https://www.zara.com/itxrest/1/catalog/store/11766/product/id/{}/availability" #11766 for TR 
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        self.ntfy_channel = os.getenv('NTFY_CHANNEL')

    def get_sorted_availability(self):
        url = self.base_url.format(self.code)
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            if "skusAvailability" in data:
                sorted_skus_availability = sorted(data["skusAvailability"], key=lambda i: i["sku"])
                return sorted_skus_availability
            else:
                print("skusAvailability not found in the response")
                return []
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def return_availability(self):
        sorted_skus_availability = self.get_sorted_availability()
        if sorted_skus_availability:
            return sorted_skus_availability[(self.which_size) - 1]["availability"]
        else:
            return "unknown"

    def ntfyOnAvailability(self):
        availability = self.return_availability().lower()
        if availability in ["in_stock", "low_on_stock"]:
            print(self.ntfy_channel)
            try:
                requests.post(f"https://ntfy.sh/{self.ntfy_channel}", 
                              data=f"{self.code} AVAILABLE".encode('utf-8'))
            except requests.RequestException as e:
                print(f"Error sending notification: {e}")
        else:
            print("Item not available")

if __name__ == "__main__":
    checker = ZaraAvailabilityChecker("315079187", 2)
    checker.ntfyOnAvailability()
