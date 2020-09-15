import requests
from bs4 import BeautifulSoup
fomr dotenv import load_dotenv
load_dotenv()
URL = "http://uiowa.instructure.com/courses"
COURSES = [142501, 146639]
USERNAME = "<your username>"
PASSWORD = "<your password>*"

# Use https://curl.trillworks.com/ to get the required cookies, headers, and data

cookies = {
    "JSESSIONID": "AC50C5DB5D3333970158102E687ED863",
    "UIP_BROWSER_ID": "5f003408-3e7b-4693-bb6b-916deedf300a",
    "_ga": "GA1.2.781260823.1594833980",
    "_scid": "dbcc25c8-0efa-48fb-8f39-e6ac9b3ad81a",
    "sp": "4a27302b-9715-4913-b6b4-79e2cf95bb55",
    "nmstat": "1596413440621",
    "_sctr": "1|1598331600000",
    "__utmz": "176458936.1599681302.44.36.utmcsr=myui.uiowa.edu|utmccn=(referral)|utmcmd=referral|utmcct=/my-ui/courses/dashboard.page",
    "_sp_id.12a6": "84b98347-8bd2-4ef5-b013-cddcc98a0005.1594359361.25.1599776061.1599344436.44639adb-1059-47d0-911c-0984249fa11c",
    "__utma": "176458936.1677186260.1594359372.1599832853.1599964024.47",
    "__utmc": "176458936",
    "_gid": "GA1.2.837236688.1599964028",
    "__utmt": "1",
    "__utmb": "176458936.25.10.1599964024",
}

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://login.uiowa.edu",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://login.uiowa.edu/uip/login?service=https%3A%2F%2Fuiowa.instructure.com%2Flogin%2Fcas%2F1",
    "Accept-Language": "en-US,en;q=0.9",
}

data = {
  "uip_hawkid": USERNAME,
  "uip_password": PASSWORD,
  "service": "https://uiowa.instructure.com/login/cas/1",
  "uip_nonPassportRequestParameters": "",
  "uip_action": " Log In "
}

s = requests.Session()
s.post("https://login.uiowa.edu/uip/login.page", headers=headers, cookies=cookies, data=data)


for course in COURSES:
    scores = []
    possibles = []
    final_scores = []
    final_possibles = []

    response = s.get(f"{URL}/{course}/grades")
    content = response.content
    soup = BeautifulSoup(content, features='lxml')
    # print(soup.prettify())
    score = soup.find_all("span", class_="grade")
    possible = soup.find_all("td", class_="possible points_possible")
    # print(possible)
    # print(score)
    for item in possible:
        possibles.append(item.get_text())

    for item in score:
        scores.append(item.get_text())

    for i in range(len(possibles)):
        numeric_filter = filter(str.isdigit, possibles[i])
        numeric_string = "".join(numeric_filter)
        if len(numeric_string) != 0: possibles[i] = int(numeric_string)

    for i in range(len(scores)):
        numeric_filter = filter(str.isdigit, scores[i])
        numeric_string = "".join(numeric_filter)
        if len(numeric_string) != 0: scores[i] = int(numeric_string)

    for i in range(len(scores)):
        if isinstance(scores[i], int): 
            final_possibles.append(possibles[i])
            final_scores.append(scores[i])

    print(f" Your grade in {course} is: {sum(final_scores) / sum(final_possibles) * 100}%")
    
    



