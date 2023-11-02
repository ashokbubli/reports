import requests
import csv
import yaml
import base64
import os

# GitHub API base URL
BASE_URL = "https://api.github.com"

# Your GitHub username and personal access token
USERNAME = "ashokbubli"
TOKEN = os.envirn.get("PAT")

# Create a CSV file to store the metadata
with open("repository_metadata.csv", "w", newline="") as csv_file:
    fieldnames = ["Repository", "Application", "IT Owner", "Key Expert", "Hosted Environment", "Accessibility", "Business Service Name"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

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

                if response.status_code == 200:
                    content = response.json()
                    content_data = content.get("content", "")

                    # Decode the content from base64
                    content_text = base64.b64decode(content_data).decode("utf-8")

                    # Extract metadata from the YAML/YML file
                    metadata = yaml.safe_load(content_text)

                    writer.writerow({
                        "Repository": repo_name,
                        "Application": metadata.get("application", ""),
                        "IT Owner": metadata.get("contacts", {}).get("it-owner", ""),
                        "Key Expert": ", ".join(metadata.get("contacts", {}).get("key-expert", [])),
                        "Hosted Environment": metadata.get("contacts", {}).get("hosted-env", ""),
                        "Accessibility": metadata.get("contacts", {}).get("accessibility", ""),
                        "Business Service Name": metadata.get("servicenow", {}).get("business-service-name", ""),
                    })
                else:
                    print(f"No .abd/app.yaml or .abd/app.yml found in repository: {repo_name}")
                    writer.writerow({
                        "Repository": repo_name,
                        "Application": "",
                        "IT Owner": "",
                        "Key Expert": "",
                        "Hosted Environment": "",
                        "Accessibility": "",
                        "Business Service Name": "",
                    })

            page += 1
        else:
            print(f"Error fetching repositories. Check your username and token.")
            break

print("CSV report generated successfully.")
