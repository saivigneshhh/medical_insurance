# ai_client.py
import asyncio
import json
import requests
from typing import Dict, Any, List, Optional

class LLMClient:
    """
    A client to interact with the Gemini LLM API for text generation and structured JSON output.
    """
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model_name = model_name
        # API key is intentionally left empty as per instructions; Canvas will provide it at runtime.
        self.api_key = ""
        self.api_url_base = "https://generativelanguage.googleapis.com/v1beta/models"

    async def _call_llm(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal helper to make the API call to the LLM.
        """
        url = f"{self.api_url_base}/{self.model_name}:generateContent?key={self.api_key}"
        try:
            # Using requests.post directly within asyncio.to_thread
            response = await asyncio.to_thread(
                requests.post, url, headers={'Content-Type': 'application/json'}, json=payload
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            raise

    async def generate_text(self, prompt: str) -> str:
        """
        Generates text using the LLM based on a given prompt.
        """
        chat_history = []
        chat_history.append({ "role": "user", "parts": [{ "text": prompt }] })
        payload = { "contents": chat_history }

        result = await self._call_llm(payload)

        if result.get("candidates") and result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and \
           result["candidates"][0]["content"]["parts"][0].get("text"):
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Unexpected LLM response structure for text generation: {result}")
            raise ValueError("Failed to generate text from LLM.")

    async def generate_structured_json(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates structured JSON output using the LLM based on a given prompt and JSON schema.
        """
        chat_history = []
        chat_history.append({ "role": "user", "parts": [{ "text": prompt }] })
        payload = {
            "contents": chat_history,
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": schema
            }
        }

        result = await self._call_llm(payload)

        if result.get("candidates") and result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and \
           result["candidates"][0]["content"]["parts"][0].get("text"):
            try:
                # The response is a stringified JSON, so parse it
                return json.loads(result["candidates"][0]["content"]["parts"][0].get("text", "{}"))
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON from LLM response: {e}. Response: {result['candidates'][0]['content']['parts'][0].get('text', '')}")
                raise ValueError("LLM returned malformed JSON.")
        else:
            print(f"Unexpected LLM response structure for structured JSON generation: {result}")
            raise ValueError("Failed to generate structured JSON from LLM.")