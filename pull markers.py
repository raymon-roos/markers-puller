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
        for idx, element in enumerate(elements):
            print(f"Element {idx}: {element}")
            print(f"Element {idx} has name: \n{element["display_label"]} \nwith message: \n{element["message"]} \nand its id is: \n{element["id"]}")
            users_send_to_ids = element["evaluation_invite_ids"]
            element_id = element["id"]
            users_send_to_id = []
            users_send_to = []
            responses = []
            for key in other_keys:
                if key in data:
                    other_elements = data[key]
                    if key == "question_responses":
                        if isinstance(other_elements, list):
                            for idy, other_element in enumerate(other_elements):
                                try:
                                    if other_element["evaluation_id"] == element["id"]:
                                        print(f"you typed: \n{other_element["comment"]}\n")
                                except:
                                    continue
                    if key == "evaluation_invites":
                        if isinstance(other_elements, list):
                            for idy, other_element in enumerate(other_elements):
                                try:
                                    for user in users_send_to_ids:
                                        if other_element["id"] == user:
                                            users_send_to_id.append(other_element["user_id"])
                                except:
                                    continue
                    if key == "question_responses":
                        if isinstance(other_elements, list):
                            for idy, other_element in enumerate(other_elements):
                                try:
                                    for user in users_send_to_id:
                                        if other_element["feedback_provider_id"] == user:
                                            responses.append([user, other_element['evaluation_id'], other_element["comment"]])
                                except:
                                    continue
                    if key == "users":
                        if isinstance(other_elements, list):
                            for idy, other_element in enumerate(other_elements):
                                try:
                                    for user in users_send_to_id:
                                        if other_element["id"] == user:
                                            users_send_to.append([user, other_element["first_names"] + " " + other_element["last_name"]])
                                except:
                                    continue
                            print("you send this to: ")
                            for i in users_send_to:
                                print(f"{i[1]}")
                            for i in users_send_to:
                                for j in responses:
                                    if j[0] == i[0] and j[1] == element_id:
                                        print(f"\n{i[1]} has answered with: \n{j[2]}")

                        # print(f"you send this to: \n{users_send_to}\n")
                    # else:
                    #     if isinstance(other_elements, list):
                    #         for idy, other_element in enumerate(other_elements):
                    #             try:
                    #                 if other_element["evaluation_id"] == element["id"]:
                    #                     print(other_element)
                    #             except:
                    #                 continue
            # If element is a dict, you can access its keys here, e.g.
            # print(element.get('sub_key', 'N/A'))

    elif isinstance(elements, dict):
        for key, value in elements.items():
            print(f"Key: {key}, Value: {value}")
    else:
        print(f"The value under '{specific_key}' is neither a list nor a dictionary.")
else:
    print(f"Key '{specific_key}' not found in the JSON file.")
