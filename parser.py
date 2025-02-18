import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# __define_ocg__

# Constants for validation
VALID_LANGUAGES = {"en", "fr", "de", "es"}
VALID_CURRENCIES = {"EUR", "USD", "GBP"}
VALID_NATIONALITIES = {"US", "GB", "CA"}
VALID_MARKETS = {"US", "GB", "CA", "ES"}
DEFAULT_LANGUAGE = "en"
DEFAULT_CURRENCY = "EUR"
DEFAULT_NATIONALITY = "US"
DEFAULT_MARKET = "ES"
DEFAULT_OPTIONS_QUOTA = 20
MAX_OPTIONS_QUOTA = 50
ALLOWED_ROOM_COUNT = 5
ALLOWED_ROOM_GUEST_COUNT = 4
ALLOWED_CHILD_COUNT_PER_ROOM = 2

# Sample Exchange Rates for currency conversion
EXCHANGE_RATES = {
    ("USD", "EUR"): 0.85,
    ("EUR", "USD"): 1.18,
    ("USD", "GBP"): 0.75,
    ("GBP", "USD"): 1.33
}

var_ocg: str = "special_flag"


class XMLParsingError(Exception):
    """Custom exception for XML parsing errors."""
    pass


# Function to parse XML input
def parse_xml(xml_string: str) -> Dict[str, Any]:
    """
    Parses XML input and extracts necessary fields.

    :param xml_string: XML input as a string
    :return: Dictionary containing extracted and validated data
    """
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        raise XMLParsingError(f"Invalid XML format: {e}")

    language_code: str = root.findtext(".//source/languageCode", DEFAULT_LANGUAGE)
    options_quota: int = int(root.findtext(".//optionsQuota", DEFAULT_OPTIONS_QUOTA))
    options_quota = min(options_quota, MAX_OPTIONS_QUOTA)

    config_params: Optional[ET.Element] = root.find(".//Configuration/Parameters/Parameter")
    if config_params is None or not all(config_params.get(attr) for attr in ["password", "username", "CompanyID"]):
        raise XMLParsingError("Missing required Configuration parameters")

    start_date_str: Optional[str] = root.findtext(".//StartDate")
    end_date_str: Optional[str] = root.findtext(".//EndDate")

    try:
        start_date: datetime = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date: datetime = datetime.strptime(end_date_str, "%d/%m/%Y")
    except ValueError:
        raise XMLParsingError("Invalid date format. Expected DD/MM/YYYY.")

    if start_date < datetime.today() + timedelta(days=2):
        raise XMLParsingError("StartDate must be at least 2 days from today.")
    if (end_date - start_date).days < 3:
        raise XMLParsingError("Stay duration must be at least 3 nights.")

    currency: str = root.findtext(".//Currency", DEFAULT_CURRENCY)
    if currency not in VALID_CURRENCIES:
        raise XMLParsingError("Invalid currency provided.")

    return {
        "language_code": language_code,
        "options_quota": options_quota,
        "currency": currency,
        "start_date": start_date,
        "end_date": end_date,
        "var_ocg": var_ocg
    }


# Function to generate JSON response
def generate_json_response(parsed_data: Dict[str, Any]) -> str:
    """
    Generates a JSON response based on parsed XML data.

    :param parsed_data: Dictionary containing validated input data
    :return: JSON-formatted response string
    """
    net_price: float = 132.42
    markup_percentage: float = 3.2
    selling_price: float = net_price * (1 + markup_percentage / 100)
    exchange_rate: float = EXCHANGE_RATES.get((parsed_data["currency"], "USD"), 1.0)

    response_data = [
        {
            "id": "A#1",
            "hotelCodeSupplier": "39971881",
            "market": DEFAULT_MARKET,
            "price": {
                "minimumSellingPrice": None,
                "currency": parsed_data["currency"],
                "net": net_price,
                "selling_price": round(selling_price, 2),
                "selling_currency": parsed_data["currency"],
                "markup": markup_percentage,
                "exchange_rate": exchange_rate
            },
            "var_ocg": parsed_data["var_ocg"]
        }
    ]

    return json.dumps(response_data, indent=2)


# Function to test the parser
def parser(xml_input_str: str) -> Optional[str]:
    """
    Parses XML and generates JSON response.

    :param xml_input_str: XML input as a string
    :return: JSON response or None if an error occurs
    """
    try:
        parsed_data = parse_xml(xml_input_str)
        response = generate_json_response(parsed_data)
        return response
    except XMLParsingError as e:
        print(f"Parser Failed: {e}")
        return None


if __name__ == "__main__":
    xml_input_str = """
    <AvailRQ xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema">
 <timeoutMilliseconds>25000</timeoutMilliseconds>
 <source>
 <languageCode>en</languageCode>
 </source>
 <optionsQuota>20</optionsQuota>
 <Configuration>
 <Parameters>
 <Parameter password="XXXXXXXXXX" username="YYYYYYYYY"
CompanyID="123456"/>
 </Parameters>
 </Configuration>
 <SearchType>Multiple</SearchType>
 <StartDate>21/02/2025</StartDate>
 <EndDate>25/10/2025</EndDate>
 <Currency>USD</Currency>
 <Nationality>US</Nationality>
</AvailRQ>
    """
    print(parser(xml_input_str=xml_input_str))
