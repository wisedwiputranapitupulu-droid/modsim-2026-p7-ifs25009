import requests
from app.config import Config


def generate_from_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {Config.LLM_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    url = f"{Config.BASE_URL}/chat/completions"
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=20,
        )
    except requests.RequestException as e:
        raise Exception(f"LLM request failed: {str(e)}") from e

    if response.status_code != 200:
        raise Exception(
            f"LLM request failed with status {response.status_code}: {response.text}"
        )

    try:
        result = response.json()
    except ValueError as e:
        raise Exception(
            f"LLM response could not be parsed as JSON: {response.text}"
        ) from e
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception("Invalid LLM response format")
