import json
import os
import re
import requests
import urllib.parse

# Utility to sanitize and filter HTML tags
def filter(text):
    return text.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("<ul>", "").replace("</ul>", "")\
        .replace("<ol>", "").replace("</ol>", "").replace("<li>", "").replace("</li>", "")\
        .replace("<strong>", "").replace("</strong>", "").replace("<em>", "").replace("</em>", "")\
        .replace("<u>", "").replace("</u>", "").replace("<s>", "").replace("</s>", "")\
        .replace("<span>", "").replace("</span>", "")

# Utility to download a file from a URL into the given folder
def download_file(url, save_dir):
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(urllib.parse.unquote(parsed_url.path))
    save_path = os.path.join(save_dir, filename)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Downloaded file to: {save_path}")

# Load the JSON file
json_file_path = 'markers.json'
specific_key = 'evaluations'
other_keys = ["evaluation_invites", "goals", "handins", "question_responses", "questions", "reports", "users"]

def answer_check(check):
    if check != "yes" and check != "no":
        print("impossible answer")
        check = str(input("yes or no\n"))
        answer_check(check)
    else:
        json_name(check)

def json_name(check):
    global data
    if check == "yes":
        print("weird, please contact the developer for help")
        exit()
    if check == "no":
        json_file_path = str(input("please type the corect name of the json file including .json\n"))
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except:
            print(f"couldn't find {json_file_path}")
            print(f"are you sure {json_file_path} is corect?")
            check = str(input("yes or no\n"))
            answer_check(check)

try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except:
    print(f"couldn't find {json_file_path}")
    print(f"are you sure {json_file_path} is corect?")
    check = str(input("yes or no\n"))
    answer_check(check)

# Main processing
if specific_key in data:
    elements = data[specific_key]

    if isinstance(elements, list):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        for idx, element in enumerate(elements):
            display_label = element["display_label"]
            element_id = element["id"]
            message = element["message"]
            feedback_moment_id = element["feedback_moment_id"]
            users_send_to_ids = element["evaluation_invite_ids"]

            users_send_to = {}
            responses = {}
            file_urls = set()
            typed_texts = set()
            users_send_to_id = set()

            # Determine type_file
            type_file = {
                10074: "evaluation",
                10076: "reflection",
                10075: "feedback",
                10077: "checkin",
                10120: "file"
            }.get(feedback_moment_id, "something else")

            # Collect related data
            for key in other_keys:
                if key not in data or not isinstance(data[key], list):
                    continue
                for other_element in data[key]:
                    try:
                        if key == "evaluation_invites" and other_element["id"] in users_send_to_ids:
                            users_send_to_id.add(other_element["user_id"])
                        elif key == "question_responses":
                            if other_element.get("evaluation_id") == element_id:
                                typed_texts.add(filter(other_element["comment"]))
                            if other_element.get("feedback_provider_id") in users_send_to_id and \
                               other_element.get("evaluation_id") == element_id:
                                uid = other_element["feedback_provider_id"]
                                responses.setdefault(uid, []).append(filter(other_element["comment"]))
                        elif key == "handins" and other_element.get("evaluation_id") == element_id:
                            for k in ["file_download_url", "external_url"]:
                                url = other_element.get(k)
                                if url:
                                    file_urls.add(url)
                        elif key == "users":
                            uid = other_element["id"]
                            if uid in users_send_to_id:
                                users_send_to[uid] = f"{other_element['first_names']} {other_element['last_name']}"
                    except Exception:
                        continue

            # Safe directory and file naming
            entry_dir = os.path.join(output_dir, type_file)
            os.makedirs(entry_dir, exist_ok=True)

            # Try using the full display label for the filename first
            safe_filename = re.sub(r'[^\w\-_\. ]', '_', display_label).strip()[:100]
            md_filename = f"{safe_filename}.md"
            md_path = os.path.join(entry_dir, md_filename)

            # Get the absolute path to check its total length
            abs_md_path = os.path.abspath(md_path)

            # Download files if applicable
            if type_file == "file":
                for url in file_urls:
                    try:
                        download_file(url, entry_dir)
                    except Exception as e:
                        print(f"Failed to download {url}: {e}")

            # Generate Markdown content
            markdown_lines = [
                f"# {display_label}\n",
                f"**ID:** {element_id}",
                f"\n**type of file:** {type_file}\n"
            ]

            if message:
                markdown_lines.append(f"\n**Message:** {message}\n")
            if file_urls:
                markdown_lines.append("\n**Download URLs:**")
                for url in file_urls:
                    markdown_lines.append(f"- {url}")
            if typed_texts:
                markdown_lines.append("\n**Typed Texts:**")
                for txt in typed_texts:
                    markdown_lines.append(f"\n```html\n{txt}\n```\n")
            if users_send_to:
                markdown_lines.append("\n**You sent this to:**")
                for name in users_send_to.values():
                    markdown_lines.append(f"\n- {name}")
            if responses:
                markdown_lines.append("\n\n**Responses:**")
                for uid, comments in responses.items():
                    name = users_send_to.get(uid, f"User {uid}")
                    for comment in comments:
                        markdown_lines.append(f"\n- {name} responded:\n```html\n{comment}\n```\n")

            # Write Markdown file
            # If the full absolute path is too long, shorten the filename portion
            if len(abs_md_path) > 260:
                short_filename = re.sub(r'[^\w\-_\. ]', '_', display_label).strip()[:30]
                md_filename = f"{short_filename}.md"
                md_path = os.path.join(entry_dir, md_filename)
                abs_md_path = os.path.abspath(md_path)
            
                # Fallback: truncate further if needed
                if len(abs_md_path) > 260:
                    md_filename = f"{element_id}.md"
                    md_path = os.path.join(entry_dir, md_filename)
                    abs_md_path = os.path.abspath(md_path)

            with open(md_path, "w", encoding="utf-8") as f:
                f.write("\n".join(markdown_lines))

            print(f"Markdown saved to {md_path}")
