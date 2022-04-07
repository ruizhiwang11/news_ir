import enum
import json

with open("data.json", "r") as f:
    d = f.read()

data = json.loads(d)


for i, element in enumerate(data.copy()):
    for k, v in element.items():
        element[k] = v.strip()
    if element["location"] == "":
        element["location"] = "singapore"
    if element["author"] == "":
        element["author"] = "anonymous"
    data[i] = element

[dict(t) for t in {tuple(d.items()) for d in data}]


with open("clean.json", "w") as f1:
    f1.write(json.dumps(data,indent=4))


# with open("total_10_pages.json", "r") as f:
#     d = f.read()

# data = json.loads(d)

# for i, element in enumerate(data.copy()):
#     tmp = data[i]["category"]
#     tmp = "singapore " + tmp
#     data[i]["category"] = tmp

# with open("a.json", "w") as f:
#     f.write(json.dumps(data,indent=4))