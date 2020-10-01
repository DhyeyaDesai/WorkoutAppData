import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

bodyparts = ["Traps", "Shoulders", "Chest", "Biceps", "Forearms", "Abdominals", "Quads", "Calves", "Triceps", "Traps_middle", "Lats", "Lowerback", "Glutes", "Hamstrings"]

all_exercises = []

for bodypart in bodyparts:
    gender = "Male"
    urls = [f"https://musclewiki.com/Exercises/{gender}/", f"https://musclewiki.com/Stretches/{gender}/", f"https://musclewiki.com/Bodyweight/{gender}/", f"https://musclewiki.com/Kettlebells/{gender}/"]
    for url in urls:
        r = requests.get(url+bodypart)
        soup = BeautifulSoup(r.content, "html.parser")
        section = soup.find("div", class_="body")
        exercises = section.find_all("h3")
        links = section.find_all("p")
        steps = section.find_all("ol")

        for n, exercise in enumerate(exercises):
            one = {"Gender":gender, "Bodypart":bodypart, "Exercise":exercise.text.replace("\n", ""), "Type":url.split("/")[3], "Video Links":str(["https://musclewiki.com" + (img.get("src")) for img in links[n+1].find_all("img")]).replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace(" ", ","), "Steps":steps[n].text.replace("\n", " ")}
            all_exercises.append(one)

for bodypart in bodyparts:
    gender = "Female"
    urls = [f"https://musclewiki.com/Exercises/{gender}/", f"https://musclewiki.com/Stretches/{gender}/", f"https://musclewiki.com/Bodyweight/{gender}/", f"https://musclewiki.com/Kettlebells/{gender}/"]
    for url in urls:
        r = requests.get(url+bodypart)
        soup = BeautifulSoup(r.content, "html.parser")
        section = soup.find("div", class_="body")
        exercises = section.find_all("h3")
        links = section.find_all("p")
        steps = section.find_all("ol")

        for n, exercise in enumerate(exercises):
            one = {"Gender":gender, "Bodypart":bodypart, "Exercise":exercise.text.replace("\n", ""), "Type":url.split("/")[3], "Video Links":str(["https://musclewiki.com" + (img.get("src")) for img in links[n+1].find_all("img")]).replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace(" ", ","), "Steps":steps[n].text.replace("\n", " ")}
            all_exercises.append(one)

df = pd.DataFrame(all_exercises)

#To save the URLS in json but without the messy slashes

result = df.to_json("x.json", orient="records")
parsed = json.loads(result)
f = json.dumps(parsed, indent=4)

with open("Final.json", "w") as f1:
    f1.write(f)