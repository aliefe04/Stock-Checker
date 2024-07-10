import requests
from utils import getenv


class HmAvailabilityChecker:
    def __init__(self, code, which_size):
        self.code = code
        self.which_size = which_size
        self.base_url = f"https://www2.hm.com/hmwebservices/service/product/tr/availability/{code[:-3]}.json"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
        }

    def get_sorted_availability(self):
        url = self.base_url.format(self.code)
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            if "availability" in data:
                sorted_availability = sorted(data["availability"], key=lambda i: i)
                return sorted_availability
            else:
                print("Availability not found in the response")
                return []
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def return_availability(self):
        sorted_availability = self.get_sorted_availability()
        for i in sorted_availability:
            if str(i) == (self.code + f"00{self.which_size}"):
                return True
        return False


if __name__ == "__main__":
    code = "1210963003"
    getenv("NTFY_CHANNEL")
    checker = HmAvailabilityChecker(code, 3)
    link = f"https://www2.hm.com/tr_tr/productpage.{code}.html"
    if checker.return_availability():
        requests.post(
            f"https://ntfy.sh/{getenv('NTFY_CHANNEL')}",
            data=f"{link} AVAILABLE".encode("utf-8"),
            headers={"Click": link},
        )
        print("Item available")
