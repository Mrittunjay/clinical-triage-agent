import os
from openai import AzureOpenAI, BadRequestError
from dotenv import load_dotenv

# Load env vars once, at import time
load_dotenv()

client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_KEY"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def planner_llm(prompt: str) -> str:
    """
    Calls Azure OpenAI to perform clinical triage planning.
    Returns plain text resoning (no diagnosis)
    """
    # print("client: ", client)
    # print("The deployment name: ", DEPLOYMENT_NAME)

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a clinical triage planner assigning medical professional. "
                        "Do not make diagnosis. "
                        "Classify urgency only (RED, YELLOW, GREEN) and explain reasoning."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content or ""

        # # Access the content from the first choice
        # ai_reasoning = response.choices[0].message.content
    
    except BadRequestError:
        print("Open AI content filter triggered")
        return "__CONTENT_BLOCKED__"
    
    except Exception as e:
        print("Unexpected openAI error")
        return ""   # Returning None creates issues