import csv, requests, json

url = 'https://api.newjunes.skybro2004.com/lecture'
headers = {
    "X-CSRFToken": "iDUjpukzVxXyCJZtXtdpvhMmAXw7xwx4",
    "Cookie": "csrftoken=iDUjpukzVxXyCJZtXtdpvhMmAXw7xwx4"
}

with open("C:/Users/skybr/OneDrive/Desktop/temp/asdf.csv", 'r', encoding="UTF-8-sig") as f:
    reader = csv.reader(f)
    for data in reader:
        if data[7]!="":
            continue
        print(data)
        form = {
            "course_number": str(data[2].split('-')[0]),
            "grade": int(data[0]),
            "classification": data[1],
            "name": data[3],
            "credit": int(data[5]),
            "department": data[11],
            "division": str(data[2].split('-')[1]),
            "professor": data[4],
            "period": data[6],
            "lecture_room": data[7],
            "rating": float(data[8]),
            "applicant": int(data[9]),
            "capacity": int(data[10]),
            "annotation": data[12]
        }
        
        res = requests.post(url, data=json.dumps(form), headers=headers)
        with open("C:/Users/skybr/OneDrive/Desktop/temp/asdff.html", 'w', encoding="UTF-8") as f:
            f.write(res.text)
        if (res.text.startswith('<')):
            input()
        # input()