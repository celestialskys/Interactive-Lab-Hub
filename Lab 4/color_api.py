#Asked ChatGPT to help me query API for color names to hex and rgb values.
import requests
from typing import TypedDict, Optional, List, Dict, Any

BASE_URL = "https://api.color.pizza/v1"

class ColorNameAPIError(Exception):
    """Custom exception for API errors."""
    pass


def rgba_to_hex(rgba):
    r, g, b, _a = rgba
    hex_color = "{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))
    return hex_color


class RGBColor(TypedDict):
    r: int
    g: int
    b: int
    
def get_name_by_rgba(rgb_value: RGBColor):
    """Query Color Pizza API using RGBA values."""
    print(rgb_value)
    if len(rgb_value) < 3:
        raise ValueError("RGBA values must be at least 3 elements")
    else:
        r, g, b, a = rgb_value["r"], rgb_value["g"], rgb_value["b"], rgb_value.get("a", 1.0)
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and 0.0 <= a <= 1.0):
            raise ValueError("RGBA values out of range")
        else:
            hex_val = rgba_to_hex([r, g, b, a])
            print(f"Looking up color for RGBA({r}, {g}, {b}, {a}) -> {hex_val}")
            return pretty_names_by_hex(hex_val)
    

def get_names_by_hex(
    hex_values: List[str],
    name_list: Optional[str] = None,
    noduplicates: bool = False
) -> Dict[str, Any]:
    """
    Query the API with one or more hex color values.
    Returns the JSON response as a dict.
    
    Example:
      get_names_by_hex(["aaffcc", "ff00ff"], name_list="wikipedia", noduplicates=True)
    """
    params: Dict[str, Any] = {
        "values": ",".join(hex_values)
    }
    if name_list is not None:
        params["list"] = name_list
    if noduplicates:
        params["noduplicates"] = "true"
    
    resp = requests.get(BASE_URL + "/", params=params)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        msg = f"HTTP {resp.status_code}: {resp.text}"
        raise ColorNameAPIError(msg) from e
    
    data = resp.json()
    # You could do schema checks here
    return data

def get_hex_by_name(
    name: str,
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Reverse lookup: from a color name, get matching hex(es) and metadata.
    """
    url = BASE_URL + "/names/"
    params = {
        "name": name,
        "maxResults": max_results
    }
    resp = requests.get(url, params=params)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        msg = f"HTTP {resp.status_code}: {resp.text}"
        raise ColorNameAPIError(msg) from e
    return resp.json()

# Optional helper for pretty printing / parsing
def pretty_names_by_hex(*hexes: str, **kwargs) -> None:
    """
    Call get_names_by_hex and pretty print results.
    """
    data = get_names_by_hex(list(hexes), **kwargs)
    import json
    print(json.dumps(data, indent=2))

# def main():
#     # simple demo
#     print("Name(s) for 'r': 255, 'g': 144, 'b': 0:")
#     color = {'r': 255, 'g': 144, 'b': 0, 'a': 1.0}
#     get_name_by_rgba(color)

# if __name__ == "__main__":
#     main()