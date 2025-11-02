from geopy.geocoders import Nominatim

from openai import OpenAI
import base64
from dotenv import load_dotenv
import requests



def model1_image(client, image_file):
    base64_image=(base64.b64encode(image_file.read()).decode("utf-8"))

    input_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "You are a city issue identification assistant, you will give descriptions of scenes people find problematic,"
                       "don't give extra details and predictions just your own observations."
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                },
            ]
        }
    ]
    response = client.responses.create(
        model="gpt-5-mini",
        input = input_messages
    )
    return response


def model2_csv(client, scene_description, comment):

    input_messages = [
        {
            "role": "system",
            "content": "You are a city issue identification assistant. Read the notes and identify the issue. Choose one issue category from this list: Street Maintenance, Trash Services, Water Utilities, Animal Control, Electrical Utilities. If no category matches give etc. .Return data in format: category\ndescription of problem."
        },
        {
            "role": "user",
            "content": f"{scene_description}\n\nCitizen's testimony: {comment}]"
        }
    ]

    response = client.responses.create(
        model="ft:gpt-4.1-mini-2025-04-14:personal:projectswordfish:CXHijo5R",
        input=input_messages
    )

    return response.output_text
import requests

import requests
from geopy.geocoders import Nominatim

def reverse_geocode(location_str: str) -> str:
    """
    Convert a string like '27.71244, -97.32613' into a simplified address.
    Returns 'Unknown address' if lookup fails.
    """
    try:
        # Parse latitude and longitude
        lat_str, lon_str = location_str.split(',')
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())

        # Try direct Nominatim API request
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": lat, "lon": lon, "format": "jsonv2", "addressdetails": 1}
        headers = {"User-Agent": "CivicLens/1.0 (contact@example.com)"}
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()

        data = r.json()
        addr = data.get("address", {})
        if not addr:
            return "Unknown address"

        # Extract key pieces
        street = addr.get("road", "")
        house_num = addr.get("house_number", "")
        city = addr.get("city") or addr.get("town") or addr.get("village") or ""
        address = f"{house_num} {street}, {city}".strip().strip(",")

        # Fallback: use geopy if API didn’t return properly
        if not address or address == ",":
            geolocator = Nominatim(user_agent="swordfish-app")
            location = geolocator.reverse((lat, lon), language="en")
            if not location or not location.raw.get("address"):
                return "Unknown address"
            addr = location.raw["address"]
            street = addr.get("road", "")
            house_num = addr.get("house_number", "")
            city = addr.get("city") or addr.get("town") or addr.get("village") or ""
            address = f"{house_num} {street}, {city}".strip().strip(",")

        return address or "Unknown address"

    except Exception as e:
        print("Reverse geocode error:", e)
        return "Unknown address"

def classify_input_data(ticket):
    load_dotenv()
    client = OpenAI()

    ticket.address = reverse_geocode(ticket.location)

    image_file = ticket.image
    comment = ticket.comments

    r_model1 = model1_image(client,image_file).output_text

    r_model2 = model2_csv(client, r_model1, comment)
    print("\n\nAI:\n")
    print(r_model2)
    print("\n\n")

    r_model2_parts = r_model2.split("\n")
    ticket.category = r_model2_parts[0]
    ticket.summary = r_model2_parts[1]

    ticket.save()
    return ticket