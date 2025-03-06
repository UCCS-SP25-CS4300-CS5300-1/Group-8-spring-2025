from openai import OpenAI
from github import Github
import os

# Load secrets
github_token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPO")
pr_number = os.getenv("GITHUB_PR_NUMBER")

# Read diff
with open("diff.txt", "r") as file:
    diff = file.read()

# Query ChatGPT
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system","content": "You are an expert software engineer performing a code review on a Django project. Provide concise, actionable feedback."},
        {"role": "user", "content": f"Please review the following code changes and provide feedback:\n{diff}"}
    ],
    model="gpt-4"
)
print(type(chat_completion))
feedback = chat_completion.choices[0].message.content
print(feedback)

# Post review as comment
g = Github(github_token)
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)
pr.create_issue_comment(f"### AI Code Review Feedback\n{feedback}")
