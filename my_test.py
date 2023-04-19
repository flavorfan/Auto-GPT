# %%
# import packages
import sys 
sys.path.append('scripts/')
import json
import random
import commands as cmd
import utils
from memory import get_memory, get_supported_memory_backends
import chat
from colorama import Fore, Style
from spinner import Spinner
import time
import speak
from config import Config
from json_parser import fix_and_parse_json
from ai_config import AIConfig
import traceback
import yaml
import argparse
from logger import logger
import logging
from prompt import get_prompt


# %%
# set config
cfg = Config()
cfg.set_debug_mode(True)
cfg.set_smart_llm_model(cfg.fast_llm_model)
# get_supported_memory_backends()
cfg.memory_backend = 'local'
# %%
logger.set_level(logging.DEBUG if cfg.debug_mode else logging.INFO)
# %%
ai_name = ""
# %%
# make first prompt
def construct_prompt():
    """Construct the prompt for the AI to respond to"""
    config = AIConfig.load()
    if config.ai_name:
        logger.typewriter_log(
            f"Welcome back! ",
            Fore.GREEN,
            f"Would you like me to return to being {config.ai_name}?",
            speak_text=True)
        should_continue = utils.clean_input(f"""Continue with the last settings?
Name:  {config.ai_name}
Role:  {config.ai_role}
Goals: {config.ai_goals}
Continue (y/n): """)
        if should_continue.lower() == "n":
            config = AIConfig()

    if not config.ai_name:
        config = prompt_user()
        config.save()

    # Get rid of this global:
    global ai_name
    ai_name = config.ai_name

    full_prompt = config.construct_full_prompt()
    return full_prompt
prompt = construct_prompt()
print(prompt)
# %%
full_message_history = []
result = None
next_action_count = 0
# Make a constant:
user_input = "Determine which next command to use, and respond using the format specified above:"
# Initialize memory and make sure it is empty.
# this is particularly important for indexing and referencing pinecone memory
# %%
# memory init
memory = get_memory(cfg, init=True)
# memory
print('Using memory of type: ' + memory.__class__.__name__)
# %%
loop_count = 0
# %%
assistant_reply = chat.chat_with_ai(
    prompt,
    user_input,
    full_message_history,
    memory,
    cfg.fast_token_limit) 

print(assistant_reply)
# %%
def print_assistant_thoughts(assistant_reply):
    """Prints the assistant's thoughts to the console"""
    global ai_name
    global cfg
    try:
        try:
            # Parse and print Assistant response
            assistant_reply_json = fix_and_parse_json(assistant_reply)
        except json.JSONDecodeError as e:
            logger.error("Error: Invalid JSON in assistant thoughts\n", assistant_reply)
            assistant_reply_json = attempt_to_fix_json_by_finding_outermost_brackets(assistant_reply)
            assistant_reply_json = fix_and_parse_json(assistant_reply_json)

        # Check if assistant_reply_json is a string and attempt to parse it into a JSON object
        if isinstance(assistant_reply_json, str):
            try:
                assistant_reply_json = json.loads(assistant_reply_json)
            except json.JSONDecodeError as e:
                logger.error("Error: Invalid JSON\n", assistant_reply)
                assistant_reply_json = attempt_to_fix_json_by_finding_outermost_brackets(assistant_reply_json)

        assistant_thoughts_reasoning = None
        assistant_thoughts_plan = None
        assistant_thoughts_speak = None
        assistant_thoughts_criticism = None
        assistant_thoughts = assistant_reply_json.get("thoughts", {})
        assistant_thoughts_text = assistant_thoughts.get("text")

        if assistant_thoughts:
            assistant_thoughts_reasoning = assistant_thoughts.get("reasoning")
            assistant_thoughts_plan = assistant_thoughts.get("plan")
            assistant_thoughts_criticism = assistant_thoughts.get("criticism")
            assistant_thoughts_speak = assistant_thoughts.get("speak")

        logger.typewriter_log(f"{ai_name.upper()} THOUGHTS:", Fore.YELLOW, assistant_thoughts_text)
        logger.typewriter_log("REASONING:", Fore.YELLOW, assistant_thoughts_reasoning)

        if assistant_thoughts_plan:
            logger.typewriter_log("PLAN:", Fore.YELLOW, "")
            # If it's a list, join it into a string
            if isinstance(assistant_thoughts_plan, list):
                assistant_thoughts_plan = "\n".join(assistant_thoughts_plan)
            elif isinstance(assistant_thoughts_plan, dict):
                assistant_thoughts_plan = str(assistant_thoughts_plan)

            # Split the input_string using the newline character and dashes
            lines = assistant_thoughts_plan.split('\n')
            for line in lines:
                line = line.lstrip("- ")
                logger.typewriter_log("- ", Fore.GREEN, line.strip())

        logger.typewriter_log("CRITICISM:", Fore.YELLOW, assistant_thoughts_criticism)
        # Speak the assistant's thoughts
        if cfg.speak_mode and assistant_thoughts_speak:
            speak.say_text(assistant_thoughts_speak)

        return assistant_reply_json
    except json.decoder.JSONDecodeError as e:
        logger.error("Error: Invalid JSON\n", assistant_reply)
        if cfg.speak_mode:
            speak.say_text("I have received an invalid JSON response from the OpenAI API. I cannot ignore this response.")

    # All other errors, return "Error: + error message"
    except Exception as e:
        call_stack = traceback.format_exc()
        logger.error("Error: \n", call_stack)
print_assistant_thoughts(assistant_reply)
# %%
# parse assistant reply to get command name and arguments
# command_name, arguments = cmd.get_command(
                # attempt_to_fix_json_by_finding_outermost_brackets(assistant_reply))

def attempt_to_fix_json_by_finding_outermost_brackets(json_string):
    if cfg.speak_mode and cfg.debug_mode:
      speak.say_text("I have received an invalid JSON response from the OpenAI API. Trying to fix it now.")
    logger.typewriter_log("Attempting to fix JSON by finding outermost brackets\n")

    try:
        # Use regex to search for JSON objects
        import regex
        json_pattern = regex.compile(r"\{(?:[^{}]|(?R))*\}")
        json_match = json_pattern.search(json_string)

        if json_match:
            # Extract the valid JSON object from the string
            json_string = json_match.group(0)
            logger.typewriter_log(title="Apparently json was fixed.", title_color=Fore.GREEN)
            if cfg.speak_mode and cfg.debug_mode:
               speak.say_text("Apparently json was fixed.")
        else:
            raise ValueError("No valid JSON object found")

    except (json.JSONDecodeError, ValueError) as e:
        if cfg.speak_mode:
            speak.say_text("Didn't work. I will have to ignore this response then.")
        logger.error("Error: Invalid JSON, setting it to empty JSON now.\n")
        json_string = {}

    return json_string

attempt_to_fix_json_by_finding_outermost_brackets(assistant_reply)
#  %%
print(assistant_reply)
# %%
command_name, arguments = cmd.get_command(
                attempt_to_fix_json_by_finding_outermost_brackets(assistant_reply))

command_name, arguments
# %%
# run command
rlt = cmd.execute_command(command_name, arguments)
# %%
rlt
# %%
result = f"Command {command_name} returned: {rlt}"
result
# %%
user_input == "GENERATE NEXT COMMAND JSON"
memory_to_add = f"Assistant Reply: {assistant_reply} " \
                f"\nResult: {result} " \
                f"\nHuman Feedback: {user_input} "
print(memory_to_add)
# %%
# ?how to use the memory data
memory.add(memory_to_add)
memory
# %%
# ?add log out put file
full_message_history.append(chat.create_chat_message("system", result))
logger.typewriter_log("SYSTEM: ", Fore.YELLOW, result)
# %%
full_message_history[0]
# %%
