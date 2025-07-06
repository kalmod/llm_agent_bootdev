import os
import sys
import argparse
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

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    fabulous_print(Color.BLUE, response.text)

    if response.usage_metadata is not None and args.verbose:
        v_output = (
            f"User prompt: {args.user_prompt}\n"
            f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
            f"Response tokens: {response.usage_metadata.candidates_token_count}"
        )
        fabulous_print(Color.ORANGE, v_output)

    sys.exit(0)


if __name__ == "__main__":
    main()
