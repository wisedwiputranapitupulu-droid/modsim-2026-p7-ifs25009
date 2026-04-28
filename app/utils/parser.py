import json
import re


def parse_llm_response(result: str) -> list:
    """Parse JSON response dari LLM, hapus markdown code fence jika ada."""
    try:
        content = result.strip()

        # Hapus markdown code fence: ```json ... ``` atau ``` ... ```
        content = re.sub(r"```json\s*|\s*```", "", content).strip()

        parsed = json.loads(content)
        return parsed.get("slogans", [])

    except Exception as e:
        raise Exception(f"Invalid JSON from LLM: {str(e)}")
