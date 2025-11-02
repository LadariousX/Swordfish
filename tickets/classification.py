from http.client import responses

from openai import OpenAI
import base64
from dotenv import load_dotenv



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

def classify_input_data(ticket):
    load_dotenv()
    client = OpenAI()

    image_file = ticket.image
    comment = ticket.comments

    r_model1 = model1_image(client,image_file).output_text

    r_model2 = model2_csv(client, r_model1, comment)
    print("\n\n")
    print(r_model2)
    print("\n\n")

    r_model2_parts = r_model2.split("\n")
    ticket.category = r_model2_parts[0]
    ticket.summary = r_model2_parts[1]

    ticket.save()
    return ticket