import json

json_file_path = 'markers.json'
specific_key = 'evaluations'
other_keys = ["evaluation_invites", "goals", "handins", "question_responses", "questions", "reports", "users"]

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

def filter(text):
    return text.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("<ul>", "").replace("</ul>", "").replace("<ol>", "").replace("</ol>", "").replace("<li>", "").replace("</li>", "").replace("<strong>", "").replace("</strong>", "").replace("<em>", "").replace("</em>", "").replace("<u>", "").replace("</u>", "").replace("<s>", "").replace("</s>", "")

if specific_key in data:
    elements = data[specific_key]

    if isinstance(elements, list):
        import os
        import re

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        for idx, element in enumerate(elements):
            created_by_user_id = element["created_by_user_id"]
            created_time = element["created_time"]
            display_label = element["display_label"]
            users_send_to_ids = element["evaluation_invite_ids"]
            evaluation_type = element["evaluation_type"]
            feedback_moment_id = element["feedback_moment_id"]
            feedback_provider_type_id = element["feedback_provider_type_id"]
            goal_ids = element["goal_ids"]
            element_id = element["id"]
            is_sent = element["is_sent"]
            is_sent_time = element["is_sent_time"]
            label = element["label"]
            last_reminder_sent_time = element["last_reminder_sent_time"]
            linked_handin_ids = element["linked_handin_ids"]
            linked_report_ids = element["linked_report_ids"]
            load_time = element["load_time"]
            message = element["message"]
            project_id = element["project_id"]
            rubric = element["rubric_id"]
            self_evaluation_report_id = element["self_evaluation_report_id"]

            users_send_to_id = set()
            users_send_to = {}
            responses = {}
            file_urls = set()

            typed_texts = set()

            for key in other_keys:
                if key not in data:
                    continue
                other_elements = data[key]

                if not isinstance(other_elements, list):
                    continue
                
                for other_element in other_elements:
                    try:
                        if key == "evaluation_invites":
                            if other_element["id"] in users_send_to_ids:
                                users_send_to_id.add(other_element["user_id"])

                        elif key == "question_responses":
                            if other_element.get("evaluation_id") == element_id:
                                typed_texts.add(filter(other_element["comment"]))

                            if other_element.get("feedback_provider_id") in users_send_to_id and \
                               other_element.get("evaluation_id") == element_id:
                                uid = other_element["feedback_provider_id"]
                                if uid not in responses:
                                    responses[uid] = []
                                responses[uid].append(filter(other_element["comment"]))

                        elif key == "handins":
                            if other_element.get("evaluation_id") == element_id:
                                print(other_element["file_download_url"])
                                file_urls.add(other_element["file_download_url"])

                        elif key == "users":
                            uid = other_element["id"]
                            if uid in users_send_to_id and uid not in users_send_to:
                                full_name = f"{other_element['first_names']} {other_element['last_name']}"
                                users_send_to[uid] = full_name

                    except Exception:
                        continue
            if feedback_moment_id == 10074:
                type_file = "evaluation"
            elif feedback_moment_id == 10076:
                type_file = "reflection"
            elif feedback_moment_id == 10075:
                type_file = "feedback"
            elif feedback_moment_id == 10077:
                type_file = "checkin"
            elif feedback_moment_id == 10120:
                type_file = "file"
            else:
                type_file = "something else"        
            markdown_lines = [
                f"# {display_label}\n",
                f"**ID:** {element_id}",
                f"\n**Message:** {message}\n",
                f"\n**type of file:** {type_file}\n",
                f"\n**download url of file:** {file_urls}\n",
            ]

            if typed_texts:
                markdown_lines.append(f"\n**Typed Texts:**")
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

            safe_filename = re.sub(r'[^\w\-_\. ]', '_', display_label)[:100]
            file_path = os.path.join(output_dir, f"{safe_filename}.md")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(markdown_lines))

            print(f"Markdown saved to {file_path}")


    elif isinstance(elements, dict):
        for key, value in elements.items():
            print(f"Key: {key}, Value: {value}")
    else:
        print(f"The value under '{specific_key}' is neither a list nor a dictionary.")
else:
    print(f"Key '{specific_key}' not found in the JSON file.")
