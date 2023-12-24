from asyncio.log import logger
from typing import Dict, List, Optional
import aiohttp

from site_ip.request_utils import handle_request_errors

TIMEOUT = 10
BASE_API_URL = "http://makeup-api.herokuapp.com/api/v1/products.json"
DEFAULT_SUCCESS_CODE = 200

BASE_PARAMS = {
    "name": "",
    "product_type": "",
    "product_category": "",
    "product_tags": "",
    "brand": "",
    "price_greater_than": "",
    "price_less_than": "",
    "rating_greater_than": "",
    "rating_less_than": ""
}


@handle_request_errors
async def make_response(params: Dict[str, Optional[str]], success_code: int = DEFAULT_SUCCESS_CODE) -> Optional[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_API_URL, params=params, timeout=TIMEOUT) as response:
            response.raise_for_status()
            if response.status == success_code:
                return await response.json()

    return None


def extract_unique_elements(data, key):
    return sorted({item[key] for item in data if item[key] is not None})


async def get_conditions_list(params: dict, selected_condition: str) -> List:
    data = await make_response(params)

    if not data:
        logger.warning("API response is empty.")
        return []

    if selected_condition == "brand":
        return extract_unique_elements(data, 'brand')

    elif selected_condition == "product_tag":
        return sorted({element for item in data for element in item.get('tag_list', [])})

    elif selected_condition == "product_type":
        return extract_unique_elements(data, 'product_type')

    elif selected_condition == "list_name_product":
        return extract_unique_elements(data, 'name')

    elif selected_condition == "all_condition":
        brands = extract_unique_elements(data, 'brand')
        tags = sorted({element for item in data for element in item.get('tag_list', [])})
        product_types = extract_unique_elements(data, 'product_type')
        return sorted(brands + tags + product_types)
