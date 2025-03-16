import requests

DOMAIN = "https://wewo-website.vercel.app/api/"

def send_water_lvl(res_value):

    url = DOMAIN + "get-water-status"
    headers = {"Content-Type": "application/json"}

    # res_value = 0 means not empty
    # res_value = 1 means empty
    # in api, it's the opposite (TRUE means not empty, FALSE means empty)
    
    data = {"status": "TRUE"} if int(res_value) == 0 else {"status": "FALSE"}
    res = requests.post(url, json=data, headers=headers)
    print(res)