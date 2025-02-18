# XML to JSON Parser

## Overview
This project is a Python-based XML to JSON parser that processes XML input, applies business rules, and generates structured JSON output. The parser ensures validation, error handling, and transformation of XML data into JSON format while adhering to predefined rules.

## Features
- Parses XML input and extracts relevant fields
- Validates essential parameters such as authentication credentials, dates, currency, and quotas
- Implements business logic, including:
  - Start date validation (must be at least 2 days ahead)
  - Minimum stay duration (at least 3 nights)
  - Language, currency, and market validation
  - Room and passenger validation (adults and children per room)
- Computes pricing with markup and currency conversion
- Returns a well-structured JSON response
- Implements exception handling with a custom `XMLParsingError` class
- Includes `__define_ocg__` as a comment and utilizes `var_ocg` as part of the response

## Dependencies
- Python 3.6+
- Standard Python Libraries:
  - `xml.etree.ElementTree`
  - `json`
  - `datetime`
  - `typing`

## Installation
No additional packages are required. Ensure you have Python installed, then clone the repository and run the script.

```bash
git clone https://github.com/codeprofile/xml-json-parser..git
cd xml-json-parser.
python parser.py
```

## Constants and Validation Rules
The script defines constants for validation to ensure correctness and compliance with business rules:

- **Languages:** `en`, `fr`, `de`, `es`
- **Currencies:** `EUR`, `USD`, `GBP`
- **Nationalities:** `US`, `GB`, `CA`
- **Markets:** `US`, `GB`, `CA`, `ES`
- **Default Values:**
  - Language: `en`
  - Currency: `EUR`
  - Nationality: `US`
  - Market: `ES`
  - Options Quota: `20`
  - Maximum Options Quota: `50`
- **Room and Passenger Rules:**
  - Maximum rooms: `5`
  - Maximum guests per room: `4`
  - Maximum children per room: `2`
  - A child (age ≤ 5) must have an accompanying adult in the same room

## Functions

### `parse_xml(xml_string: str) -> Dict[str, Any]`
Parses the XML input, extracts relevant fields, and validates them based on business rules.

#### Parameters:
- `xml_string`: The XML input as a string.

#### Returns:
- A dictionary containing extracted and validated data.

#### Raises:
- `XMLParsingError`: If the XML is malformed or mandatory fields are missing.

### `generate_json_response(parsed_data: Dict[str, Any]) -> str`
Generates a structured JSON response based on parsed and validated XML data.

#### Parameters:
- `parsed_data`: Dictionary containing extracted XML data.

#### Returns:
- A JSON-formatted string.

## Example XML Input
```xml
<AvailRQ>
    <source>
        <languageCode>en</languageCode>
    </source>
    <optionsQuota>20</optionsQuota>
    <Configuration>
        <Parameters>
            <Parameter password="XXXXXXXXXX" username="YYYYYYYYY" CompanyID="123456"/>
        </Parameters>
    </Configuration>
    <SearchType>Multiple</SearchType>
    <StartDate>21/02/2025</StartDate>
    <EndDate>25/10/2025</EndDate>
    <Currency>USD</Currency>
    <Nationality>US</Nationality>
</AvailRQ>
```

## Example JSON Output
```json
[
    {
        "id": "A#1",
        "hotelCodeSupplier": "39971881",
        "market": "ES",
        "price": {
            "minimumSellingPrice": null,
            "currency": "USD",
            "net": 132.42,
            "selling_price": 136.66,
            "selling_currency": "USD",
            "markup": 3.2,
            "exchange_rate": 1.0
        },
        "var_ocg": "special_flag"
    }
]
```

## Running Tests
Run the script to see the parser in action. It includes sample test cases that validate different scenarios.

```bash
python parser.py
```

## Error Handling
The script includes a custom exception class `XMLParsingError` to handle invalid XML structure and missing required fields. Errors are logged and displayed for debugging purposes.

## Best Practices Followed
- **Code Readability:** Well-commented functions and meaningful variable names.
- **Error Handling:** Uses a custom exception for better debugging.
- **Validation & Business Logic:** Ensures input constraints such as date validity, required parameters, and currency validation.
- **Scalability:** The structured approach allows easy modifications for additional business rules.

## Conclusion
This script provides a robust solution for XML to JSON transformation while enforcing business logic and validation. It demonstrates clean coding practices and problem-solving skills required for production-level applications.

