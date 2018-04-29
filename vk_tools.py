import requests


def get_vk_username(user_id):
    vk_server = "https://api.vk.com/method/users.get"
    params = {
        "user_ids": str(user_id),
        "v": "5.74"
    }
    try:

        response = requests.get(vk_server, params=params).json()
        if "error" in response:
            return
        user_data = response["response"][0]
        full_name = user_data["first_name"] + " " + user_data["last_name"]
        return full_name

    except Exception as err:
        print(">>> VK error :", err)


def check_vk_user(user_id):
    return bool(get_vk_username(user_id))
