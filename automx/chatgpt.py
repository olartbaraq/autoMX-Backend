from openai import OpenAI
from decouple import config


client = OpenAI(
    organization=config("ORG_ID"),
)


async def promptGPT(
    location: str,
    temperature: str,
    temp_feels_like: str,
    weather: str,
    weather_description: str,
) -> dict:
    my_assistant = client.beta.assistants.create(
        instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
        name="Math Tutor",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4",
    )
    print(my_assistant)
