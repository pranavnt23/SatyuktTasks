from db_fms import fetch
import json

from db_fms import fetch

def get_user_category(user_id: int):
    user_cred = fetch(
        "user_credentials",
        columns=["user_name"],
        user_id=user_id
    )
    if not user_cred or not user_cred[0]:
        return None

    user_name = user_cred[0][0]

    user_reg = fetch(
        "user_registration",
        columns=["category"],
        mobile_no=user_name
    )
    if user_reg and user_reg[0]:
        return user_reg[0][0]
    return None

def get_tasks_for_field_operator(user_id: int):
    tasks = fetch(
        "fo_task_details",
        columns=["task_name", "task_description", "assigned_date", "due_date", "status"],
        fo_id=user_id
    )
    return tasks

def get_tasks_for_assignee(user_id: int):
    tasks = fetch(
        "fo_task_details",
        columns=["task_name", "task_description", "assigned_date", "due_date", "status"],
        assignee_id=user_id
    )
    return tasks

def view_tasks(user_id: int):
    category = get_user_category(user_id)
    if category == "Field Operator":
        tasks = get_tasks_for_field_operator(user_id)
    else:
        tasks = get_tasks_for_assignee(user_id)

    if not tasks:
        return {"status": "success", "message": "No tasks found for this user.", "tasks": []}

    task_list = []
    for task in tasks:
        task_list.append({
            "task_name": task[0],
            "task_description": task[1],
            "assigned_date": str(task[2]),
            "due_date": str(task[3]),
            "status": task[4]
        })

    return {"status": "success", "tasks": task_list}


if __name__ == "__main__":
    result = view_tasks(6)
    print(json.dumps(result, indent=4))
