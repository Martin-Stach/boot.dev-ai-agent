import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt import system_prompt


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0)
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    prompt_tokens = response.usage_metadata.prompt_token_count
    candidates_tokens = response.usage_metadata.candidates_token_count
    if verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {candidates_tokens}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
