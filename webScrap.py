import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv

# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}
# req = requests.get(url, headers=headers)
# src = req.text

# Save page on desktop
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)


# with open("index.html", encoding="utf-8") as file:
#     src = file.read()

# soup = BeautifulSoup(src, "lxml")

# all_ctegories_dict = {}

# all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#     all_ctegories_dict[item_text] = item_href

# with open("all_categories_dict.json", "w") as file:
#     json.dump(all_ctegories_dict, file, indent=4, ensure_ascii=False)


with open("all_categories_dict.json") as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Iteration : {iteration_count}")

for category_name, category_href in all_categories.items():

    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")
    
    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/html/{category_name}_{count}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"data/html/{category_name}_{count}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    table_heads = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")    
    product = table_heads[0].text
    calories = table_heads[1].text
    proteins = table_heads[2].text
    fats = table_heads[3].text
    carbohydrates = table_heads[4].text
    
    with open(f"data/csv/{category_name}_{count}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates,
            )
        )
    
    products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    product_info = []
    for item in products_data:
        product_tbs = item.find_all("td")

        title = product_tbs[0].find("a").text
        calories = product_tbs[1].text
        proteins = product_tbs[2].text
        fats = product_tbs[3].text
        carbohydrates = product_tbs[4].text

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates,

            }
        )

        with open(f"data/json/{category_name}_{count}.json", "a", encoding="utf-8") as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)
        
        with open(f"data/csv/{category_name}_{count}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates,
                )
            )
        
    count += 1
    print(f"# Iteration is: {count}. {category_name} is append!")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Job is finished!!!")
        break

    print(f"Iteration is left: {iteration_count}")
    sleep(random.randrange(2, 4))