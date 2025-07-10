import os
import sys
import argparse
from functions.config import SYSTEM_PROMPT, MAX_ITERS
from call_function import call_function, available_functions
from dotenv import load_dotenv
from google import genai
from google.genai import types

from format_colors import fabulous_print, Color


def main():
    parser = argparse.ArgumentParser(
        prog="llm_agent", description="A cli-tool to prompt google's gemeni ai."
    )

    parser.add_argument(
        "user_prompt",
        type=str,
        help="Prompt entered by the user.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enables verbose output.",
        required=False,
    )

    args = parser.parse_args()

    # LOAD ENV VARIABLES
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    # types.Content list to store our users prompts
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            fabulous_print(Color.GREEN, f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                fabulous_print(Color.GREEN, "Final Response:")
                fabulous_print(Color.ORANGE, final_response)
                break
        except Exception as e:
            fabulous_print(Color.RED, f"Error in generate_content: {e}")
            # fabulous_print(Color.RED, f"error: Error generating content - {e}")

    sys.exit(0)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )

    # Adding candidates from our generate_content.response
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if verbose:
        v_output = (
            # f"User prompt: {args.user_prompt}\n"
            f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
            f"Response tokens: {response.usage_metadata.candidates_token_count}"
        )
        fabulous_print(Color.ORANGE, v_output)

    if not response.function_calls:
        return fabulous_print(Color.BLUE, response.text)

    function_responses = []
    for fcPart in response.function_calls:
        function_call_result = call_function(fcPart, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
