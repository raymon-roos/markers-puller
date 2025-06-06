import json

json_file_path = 'markers_s1.json'
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

        output_dir = "output_s1"
        os.makedirs(output_dir, exist_ok=True)

        for idx, element in enumerate(elements):
            display_label = element["display_label"]
            message = element["message"]
            element_id = element["id"]
            users_send_to_ids = element["evaluation_invite_ids"]
            users_send_to_id = []
            users_send_to = []
            responses = []

            print(f"Element {idx}: {element}")
            print(f"Element {idx} has name: \n{display_label} \nwith message: \n{message} \nand its id is: \n{element_id}")

            for key in other_keys:
                if key in data:
                    other_elements = data[key]
                    if key == "question_responses":
                        if isinstance(other_elements, list):
                            for other_element in other_elements:
                                try:
                                    if other_element["evaluation_id"] == element_id:
                                        print(f"you typed: \n{other_element['comment']}\n")
                                except:
                                    continue
                                
                    if key == "evaluation_invites":
                        if isinstance(other_elements, list):
                            for other_element in other_elements:
                                try:
                                    for user in users_send_to_ids:
                                        if other_element["id"] == user:
                                            users_send_to_id.append(other_element["user_id"])
                                except:
                                    continue
                                
                    if key == "question_responses":
                        if isinstance(other_elements, list):
                            for other_element in other_elements:
                                try:
                                    for user in users_send_to_id:
                                        if other_element["feedback_provider_id"] == user:
                                            responses.append([user, other_element['evaluation_id'], other_element["comment"]])
                                except:
                                    continue
                                
                    if key == "users":
                        if isinstance(other_elements, list):
                            for other_element in other_elements:
                                try:
                                    for user in users_send_to_id:
                                        if other_element["id"] == user:
                                            full_name = f"{other_element['first_names']} {other_element['last_name']}"
                                            users_send_to.append([user, full_name])
                                except:
                                    continue
                                
            # Create Markdown content
            markdown_lines = [
                f"# {display_label}\n",
                f"**ID:** {element_id}",
                f"\n**Message:** {message}\n",
            ]

            for key in data:
                if key == "question_responses":
                    markdown_lines.append(f"**Typed Texts:**")
                    for other_element in data[key]:
                        try:
                            if other_element["evaluation_id"] == element_id:
                                markdown_lines.append(f"\n```html\n{other_element['comment']}\n```\n")
                        except:
                            continue
                        
            markdown_lines.append("\n**You sent this to:**")
            for user in users_send_to:
                markdown_lines.append(f"\n- {user[1]}")

            markdown_lines.append("\n\n**Responses:**")
            for user in users_send_to:
                for response in responses:
                    if response[0] == user[0] and response[1] == element_id:
                        markdown_lines.append(f"\n- {user[1]} responded:\n```html\n{response[2]}\n```\n")

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
