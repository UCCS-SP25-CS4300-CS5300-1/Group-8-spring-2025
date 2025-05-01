from openai import OpenAI
import os

# Read diff
with open("diff.txt", "r") as file:
    diff = file.read()

# Query ChatGPT
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are an expert software engineer performing a code review on a Django project. Provide concise, actionable feedback."},
        {"role": "user", "content": f"Provide concise, actionable feedback in Markdown format, paying special attention to Django convention, security, and code efficiency, and in each case mentioning the file name and line number for the suggestion. Here's the pull request diff:\n{diff}"}
    ],
    model="gpt-4o"
)

feedback = chat_completion.choices[0].message.content
print(feedback)

with open("feedback.md", "w") as file:
    file.write(f"## AI Code Review Feedback\n{feedback}")


