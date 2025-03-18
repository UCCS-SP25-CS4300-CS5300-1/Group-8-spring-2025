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
        {"role": "system","content": "You are a software engineer performing a code review on a Django project. Provide concise, actionable feedback, paying special attention to Django convention, security, and code efficiency."},
        {"role": "user", "content": f"The following is a git diff for a current pull request, provide feedback in MarkDown format:\n{diff}"}
    ],
    model="o3-mini"
)

feedback = chat_completion.choices[0].message.content
print(feedback)

with open("feedback.md", "w") as file:
    file.write(f"## AI Code Review Feedback\n{feedback}")


