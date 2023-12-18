import json
from typing import Dict, List, Optional

import requests

from handlers.default_handlers.exception_handler import handle_request_errors

TIMEOUT = 10

BASE_URL = "http://makeup-api.herokuapp.com/api/v1/products.json"
DEFAULT_SUCCESS_CODE = requests.codes.ok

BASE_PARAMS = {
    "name": None,
    "product_type": None,
    "product_category": None,
    "product_tags": None,
    "brand": None,
    "price_greater_than": None,
    "price_less_than": None,
    "rating_greater_than": None,
    "rating_less_than": None
}

@handle_request_errors
def make_response(params: Dict[str, Optional[str]], success_code: int = DEFAULT_SUCCESS_CODE) -> Optional[Dict]:
    response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
    response.raise_for_status()

    if response.status_code == success_code:
        return json.loads(response.text)

    return None

@handle_request_errors
def get_conditions_list(params: dict, selected_condition: str) -> List:
    data = make_response(params)

    if not data:
        # Handle the case when the API request fails
        return []

    if selected_condition == "brand":
        return sorted(list(set([item['brand'] for item in data if item['brand'] is not None])))

    elif selected_condition == "product_tag":
        return sorted(list(set([tag for item in data for tag in item['tag_list'] if item['tag_list']])))

    elif selected_condition == "product_type":
        return sorted(list(set([item['product_type'] for item in data if item['product_type'] is not None])))

    elif selected_condition == "list_name_product":
        return sorted(list(set([item['name'] for item in data if item['name'] is not None])))

    elif selected_condition == "all_condition":
        brands = sorted(list(set([item['brand'] for item in data if item['brand'] is not None])))
        tags = sorted(list(set([tag for item in data for tag in item['tag_list'] if item['tag_list']])))
        product_types = sorted(list(set([item['product_type'] for item in data if item['product_type'] is not None])))
        return brands + tags + product_types

