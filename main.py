import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt import system_prompt
from functions.call_function import available_functions, call_function


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
        
    for _ in range(20):
      response, function_responses = generate_content(client, messages, args.verbose)
      
      if response.candidates:
        for candidate in response.candidates:
          # for part in candidate.content.parts:
            # print(f"DEBUG part: function_call={part.function_call}, thought_signature={getattr(part, 'thought_signature', 'MISSING')}")
          messages.append(candidate.content)
          # messages.append([types.Content(role="model", parts=[types.Part(text=candidate)])])
      
      if not response.function_calls:
        print(f"Final response: {response.text}")
        exit(0)
      
      messages.append(types.Content(role="user", parts=function_responses))
      
    print("Model didn't responde with a final response")
    exit(1)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        # model="gemini-3.1-flash-light",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0, tools=[available_functions])
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    prompt_tokens = response.usage_metadata.prompt_token_count
    candidates_tokens = response.usage_metadata.candidates_token_count
    if verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {candidates_tokens}")
        
    function_calls = response.function_calls
    function_results = []
    
    if function_calls is not None:
      for function_call in function_calls:
        # Start here the real function calling          
        function_call_result = call_function(function_call, verbose=verbose)
        if function_call_result.parts is None:
          raise Exception("Parts list from function_call_result is Empty")
        
        function_response = function_call_result.parts[0].function_response
        if function_response is None:
          raise Exception("Function response is somehow None")
        
        final_response = function_response.response
        if final_response is None:
          raise Exception("Final function response is None")
        
        function_results.append(function_call_result.parts[0])
        # function_responses.append(final_response)
        
        if verbose:
          print(f"-> {function_call_result.parts[0].function_response.response}")
          
      # return response, function_results
    # print(f"Final response: {response.text}")
    return response, function_results


if __name__ == "__main__":
    main()
