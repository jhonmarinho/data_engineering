import requests
import json
from datetime import datetime 

DATE = str(datetime.today())

def get_most_relevant_items_for_category(category):
    url=f"https://api.mercadolibre.com/sites/MLA/search?category={category}#json"
    response = requests.get(url).text
    response = json.loads(response)
    data = response["results"]
    print(data)
    
    with open('/opt/airflow/dags/tmp/file.tsv','w') as file:
        for item in data:
                id = getKeyFromItem(item,"id")
                site_id = getKeyFromItem(item,"site_id")
                title = getKeyFromItem(item,"title")
                price = getKeyFromItem(item,"price")
                available_quantity = getKeyFromItem(item,"available_quantity")
                thumbnail = getKeyFromItem(item,"thumbnail")

                file.write(f"{id}\t{site_id}\t{title}\t{price}\t{available_quantity}\t{thumbnail}\t{DATE}\n")

                
            
def getKeyFromItem(item, key):
    return str(item[key]).replace(' ','').strip() if item.get(key) else "null"     
    
def main():
    CATEGORY = "MLA1577"
    get_most_relevant_items_for_category(CATEGORY)
    
main()