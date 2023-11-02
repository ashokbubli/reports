import requests
import yaml
import base64
import os

# GitHub API base URL
BASE_URL = "https://api.github.com"

# Your GitHub username and personal access token
USERNAME = "ashokbubli"
TOKEN = "os.environ.get("PAT")"

# Create a Markdown file to store the metadata
with open("repository_metadata.md", "w") as md_file:
    md_file.write("# Repository Metadata\n\n")

    # Get a list of all repositories for your GitHub account (including private repositories)
    page = 1
    while True:
        response = requests.get(
            f"{BASE_URL}/user/repos?page={page}&per_page=100",  # Increase per_page if you have more repositories
            headers={"Authorization": f"token {TOKEN}"}
        )

        if response.status_code == 200:
            repositories = response.json()
            if not repositories:
                break

            for repo in repositories:
                repo_name = repo['name']
                repo_url = repo['html_url']

                # Fetch the contents of app.yaml/app.yml from the repository
                response_yaml = requests.get(f"{BASE_URL}/repos/{USERNAME}/{repo_name}/contents/.abd/app.yaml", headers={"Authorization": f"token {TOKEN}"})
                response_yml = requests.get(f"{BASE_URL}/repos/{USERNAME}/{repo_name}/contents/.abd/app.yml", headers={"Authorization": f"token {TOKEN}"})

                response = response_yaml if response_yaml.status_code == 200 else response_yml

                md_file.write(f"## Repository: [{repo_name}]({repo_url})\n\n")

                if response.status_code == 200:
                    content = response.json()
                    content_data = content.get("content", "")

                    # Decode the content from base64
                    content_text = base64.b64decode(content_data).decode("utf-8")

                    # Extract metadata from the YAML/YML file
                    metadata = yaml.safe_load(content_text)

                    md_file.write("### Metadata\n\n")
                    md_file.write(f"- **Application:** {metadata.get('application', '')}\n")
                    md_file.write(f"- **IT Owner:** {metadata.get('contacts', {}).get('it-owner', '')}\n")
                    md_file.write(f"- **Key Expert:** {', '.join(metadata.get('contacts', {}).get('key-expert', []))}\n")
                    md_file.write(f"- **Hosted Environment:** {metadata.get('contacts', {}).get('hosted-env', '')}\n")
                    md_file.write(f"- **Accessibility:** {metadata.get('contacts', {}).get('accessibility', '')}\n")
                    md_file.write(f"- **Business Service Name:** {metadata.get('servicenow', {}).get('business-service-name', '')}\n\n")
                else:
                    print(f"No .abd/app.yaml or .abd/app.yml found in repository: {repo_name}")

            page += 1
        else:
            print(f"Error fetching repositories. Check your username and token.")
            break

print("Markdown report generated successfully.")
