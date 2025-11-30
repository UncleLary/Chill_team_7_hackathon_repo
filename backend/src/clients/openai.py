import os
from openai import AsyncOpenAI

async def run_llm_prompt(prompt : str) -> str:
    model_name = os.environ["OPENAI_MODEL_NAME"]
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_KEY"),)
    print(f"OpenAI prompt [{model_name}]: {prompt}")
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_name,
    )
    print(f"OpenAI returned {chat_completion}")
    return chat_completion.choices[0].message.content
