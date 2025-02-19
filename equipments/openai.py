import json
from openai import OpenAI
client = OpenAI()


def test():
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        temperature=0.2,
        stop=["\n\n"],
        messages=[
            {"role": "system", "content": "Respond only with JSON format."},
            {
                "role": "user",
                "content": "List the specs of ASUS P3605CVA."
            }
        ]
    )

    response = json.loads(completion.choices[0].message.content)
    print(response)
