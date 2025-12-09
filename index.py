import requests
import logging

logging.basicConfig(
    filename="currency_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class CurrencyConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"

    def get_rate(self, from_currency, to_currency):
        url = f"{self.base_url}/{self.api_key}/pair/{from_currency}/{to_currency}"
        try:
            r = requests.get(url)
            data = r.json()
            if data.get("result") != "success":
                raise Exception(f"API error: {data.get('error-type', 'unknown')}")
            return data["conversion_rate"]
        except Exception as e:
            logging.error(f"Rate fetch failed: {e}")
            raise

    def convert(self, amount, from_currency, to_currency, decimals=2):
        rate = self.get_rate(from_currency, to_currency)
        result = round(amount * rate, decimals)
        logging.info(f"Converted {amount} {from_currency} to {result} {to_currency}")
        return result


if __name__ == "__main__":
    API_KEY = "9e899f0b5f7544ef9e56dc10"
    converter = CurrencyConverter(API_KEY)

    # Test run
    try:
        print(converter.convert(100, "USD", "INR"))
    except Exception as e:
        print("Conversion failed:", e)

    # Interactive loop
    while True:
        x = input("Enter in format: amount from_currency to_currency (or 'exit'): ")
        if x.lower().strip() == "exit":
            break

        parts = x.split()
        if len(parts) != 3:
            print(" Invalid format. Example: 100 USD INR")
            continue

        amount_str, f, t = parts
        try:
            amount = float(amount_str)
            result = converter.convert(amount, f.upper(), t.upper())
            print(f"{amount} {f.upper()} = {result} {t.upper()}")
        except ValueError:
            print("Amount must be a number. Example: 100 USD INR")
        except Exception as e:
            print("Error:", e)