import json

json_file_path = 'markers.json'
specific_key = 'evaluations'  # The key where the list/dict is located
other_keys = ["evaluation_invites", "goals", "handins", "question_responses", "questions", "reports", "users"]

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

if specific_key in data:
    elements = data[specific_key]

    # Check if it's a list or dictionary
    if isinstance(elements, list):
        import os
        import re

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        for idx, element in enumerate(elements):
            display_label = element["display_label"]
            message = element["message"]
            element_id = element["id"]
            users_send_to_ids = set(element["evaluation_invite_ids"])
            users_send_to_id = set()
            users_send_to = {}
            responses = {}

            typed_texts = set()

            # Process all relevant keys once
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
                            # Typed text
                            if other_element.get("evaluation_id") == element_id:
                                typed_texts.add(other_element["comment"])

                            # Responses
                            if other_element.get("feedback_provider_id") in users_send_to_id and \
                               other_element.get("evaluation_id") == element_id:
                                uid = other_element["feedback_provider_id"]
                                if uid not in responses:
                                    responses[uid] = []
                                responses[uid].append(other_element["comment"])

                        elif key == "users":
                            uid = other_element["id"]
                            if uid in users_send_to_id and uid not in users_send_to:
                                full_name = f"{other_element['first_names']} {other_element['last_name']}"
                                users_send_to[uid] = full_name

                    except Exception:
                        continue
                    
            # Create Markdown content
            markdown_lines = [
                f"# {display_label}\n",
                f"**ID:** {element_id}",
                f"\n**Message:** {message}\n",
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

            # Sanitize filename
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
