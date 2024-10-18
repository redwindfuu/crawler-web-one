import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import re

url = "https://www.businesstimes.com.sg/singapore/car-expo-sales-rev-bigger-coe-supply-demand-china-evs"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

print("HTML content has been written to output.txt")

script_tag = soup.find("script", string=lambda s: s and "window.__staticRouterHydrationData" in s)

if script_tag:
    script_content = script_tag.string

    match = re.search(r'JSON\.parse\("(.+?)"\)', script_content)
    if match:

        encoded_json_string = match.group(1)
        cleaned_json_string = encoded_json_string.replace('\\"', '"')
        data_dict = json.loads(cleaned_json_string)
        print(data_dict)

        # with open('output1.txt', 'w', encoding='utf-8') as file:
        #     file.write(data_dict.)

        dataRaw = data_dict["loaderData"]["1"]

        print(dataRaw)

        with open('output.txt', 'w', encoding='utf-8') as file:
            file.write(dataRaw)

        decoded_json_string = urllib.parse.unquote(dataRaw)

        dataJson = json.loads(decoded_json_string)

        with open('output.json', 'w', encoding='utf-8') as json_file:
            json.dump(dataJson, json_file, indent=4, ensure_ascii=False)

        print("Data has been written to output.json")
    else:
        print("No JSON data found in the script.")
else:
    print("No matching <script> tag found.")