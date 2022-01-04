from datetime import date
import requests
import json
from time import sleep

user = input("Enter the reddit username: ")
url = f"https://api.pushshift.io/reddit/search/comment/?author={user}&size=100"
date_modifier = ""

count = 0
comments_list = []
while True: 
    sleep(0.5)
    comments_json = requests.get(url + date_modifier).json()["data"]
    if  comments_json:
        comments_list += comments_json
        date_modifier = "&before=" + str(comments_json[-1]["created_utc"])
        
        count += 1
        print(f" {count} requests made", end="\r")
    else:
        break

print(f"{count} requests made ")
print(f"{len(comments_list)} comments loaded")

with open("Data/comments.json", "w") as file:
    print("Writing to file...")
    json.dump(comments_list, file, indent=4)

print("Done.")
