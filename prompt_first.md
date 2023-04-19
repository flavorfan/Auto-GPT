# 1 prompt

``` md
You are writer_2, an AI design to write articles
Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications.

GOALS:

1. Search 10 news items about AutoGPT on the Internet
2. Summarize the news into a 1000-word "news.txt".
3. None
4. None
5. None


Constraints:
1. ~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.
2. If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.
3. No user assistance
4. Exclusively use the commands listed in double quotes e.g. "command name"

Commands:
1. Google Search: "google", args: "input": "<search>"
2. Browse Website: "browse_website", args: "url": "<url>", "question": "<what_you_want_to_find_on_website>"
3. Start GPT Agent: "start_agent", args: "name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"
4. Message GPT Agent: "message_agent", args: "key": "<key>", "message": "<message>"
5. List GPT Agents: "list_agents", args: 
6. Delete GPT Agent: "delete_agent", args: "key": "<key>"
7. Write to file: "write_to_file", args: "file": "<file>", "text": "<text>"
8. Read file: "read_file", args: "file": "<file>"
9. Append to file: "append_to_file", args: "file": "<file>", "text": "<text>"
10. Delete file: "delete_file", args: "file": "<file>"
11. Search Files: "search_files", args: "directory": "<directory>"
12. Evaluate Code: "evaluate_code", args: "code": "<full_code_string>"
13. Get Improved Code: "improve_code", args: "suggestions": "<list_of_suggestions>", "code": "<full_code_string>"
14. Write Tests: "write_tests", args: "code": "<full_code_string>", "focus": "<list_of_focus_areas>"
15. Execute Python File: "execute_python_file", args: "file": "<file>"
16. Execute Shell Command, non-interactive commands only: "execute_shell", args: "command_line": "<command_line>"
17. Task Complete (Shutdown): "task_complete", args: "reason": "<reason>"
18. Generate Image: "generate_image", args: "prompt": "<prompt>"
19. Do Nothing: "do_nothing", args: 

Resources:
1. Internet access for searches and information gathering.
2. Long Term memory management.
3. GPT-3.5 powered Agents for delegation of simple tasks.
4. File output.

Performance Evaluation:
1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities.
2. Constructively self-criticize your big-picture behavior constantly.
3. Reflect on past decisions and strategies to refine your approach.
4. Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.

You should only respond in JSON format as described below 
Response Format: 
{
    "thoughts": {
        "text": "thought",
        "reasoning": "reasoning",
        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    },
    "command": {
        "name": "command name",
        "args": {
            "arg name": "value"
        }
    }
} 
Ensure the response can be parsed by Python json.loads

```

# 2 assistant_reply
```json
{
    "thoughts": {
        "text": "I will begin by searching the internet for recent news about AutoGPT.",
        "reasoning": "I need up-to-date information to write my article on AutoGPT.",
        "plan": "- Search the internet using Google search for recent news about Autogpt\n- Read through them, and select the top 10 relevant news articles\n- Summarize the news articles into a 1000-word news.txt file.",
        "criticism": "I should be mindful not to spend too much time on this task as I have other tasks that need to be done later.",
        "speak": "I will perform a Google search to find recent news about AutoGPT."
    },
    "command": {
        "name": "google",
        "args": {
            "input": "recent news about AutoGPT"
        }
    }
}
```

``` format
WRITER_2 THOUGHTS:  I will begin by searching the internet for recent news about AutoGPT.
REASONING:  I need up-to-date information to write my article on AutoGPT.
PLAN: 
-  Search the internet using Google search for recent news about Autogpt
-  Read through them, and select the top 10 relevant news articles
-  Summarize the news articles into a 1000-word news.txt file.
CRITICISM:  I should be mindful not to spend too much time on this task as I have other tasks that need to be done later.
```

# 3 memory_to_add: assistant reply, result, human feedback
```txt
Assistant Reply: {
    "thoughts": {
        "text": "I will begin by searching the internet for recent news about AutoGPT.",
        "reasoning": "I need up-to-date information to write my article on AutoGPT.",
        "plan": "- Search the internet using Google search for recent news about Autogpt\n- Read through them, and select the top 10 relevant news articles\n- Summarize the news articles into a 1000-word news.txt file.",
        "criticism": "I should be mindful not to spend too much time on this task as I have other tasks that need to be done later.",
        "speak": "I will perform a Google search to find recent news about AutoGPT."
    },
    "command": {
        "name": "google",
        "args": {
            "input": "recent news about AutoGPT"
        }
    }
} 
Result: Command google returned: ['https://www.marktechpost.com/2023/04/16/breaking-down-autogpt-what-it-is-its-features-limitations-artificial-general-intelligence-agi-and-impact-of-autonomous-agents-on-generative-ai/', 'https://interestingengineering.com/innovation/meet-autogpt-internet-is-crazy-about', 'https://levelup.gitconnected.com/autogpt-the-new-kid-on-the-ai-block-thats-changing-everything-6d6ee8cf169f', 'https://www.euronews.com/next/2023/04/14/make-some-room-chatgpt-rival-ai-chatbot-autogpt-has-landed-this-is-what-we-know-about-it-s', 'https://fortune.com/2023/04/15/babyagi-autogpt-openai-gpt-4-autonomous-assistant-agi/', 'https://pub.towardsai.net/the-ai-revolution-how-auto-gpt-unleashes-a-new-era-of-automation-and-creativity-2008aa2ca6ae', 'https://www.tomsguide.com/news/auto-gpt', 'https://autogpt.net/amazing-use-cases-for-auto-gpt-on-twitter/'] 
Human Feedback: Determine which next command to use, and respond using the format specified above: 
```

