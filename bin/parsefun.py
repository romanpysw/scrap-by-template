import requests
import time
import datetime
import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS

async def scrap_chapter(session, url_list, names_csv, web_list_name, web_selectors, web_types, templ_name, pg_iter):
    if not (len(names_csv) == len(web_selectors)):
        return False
    
    iter = 0
    templ_name = templ_name.replace(".xml", "")

    wFile = open("parsing results/" + templ_name + '-' + str(datetime.date.today()) + ".csv", mode = "a", encoding = 'utf-8')
    file_writer = csv.DictWriter(wFile, delimiter = ';', lineterminator = '\n', fieldnames = names_csv)
    meta_field = dict.fromkeys(names_csv)
    count_page = 0

    while(1):
        count_page = page_iter(iter, pg_iter)
        async with session.get((url_list + str(count_page))) as response:
            print(url_list + str(count_page))
            response_text = await response.text()
            html = BS(response_text, 'html.parser')
            item_list = html.select(web_list_name)

        if len(item_list):
            for item in item_list:
                for i in range(len(web_selectors)):
                    if web_types[i] == "URL":
                        meta_data = item.find('a', href = True)
                        meta_field[names_csv[i]] = meta_data.get('href')
                        continue

                    meta_data = item.select(web_selectors[i])
                    if not meta_data:
                        meta_field[names_csv[i]] = "NoData"
                    elif web_types[i] == "Number":
                        meta_field[names_csv[i]] = meta_data[0].text
                    elif web_types[i] == "Text":
                        meta_field[names_csv[i]] = meta_data[0].text
                file_writer.writerow(meta_field)
                meta_field.clear()
                meta_field = dict.fromkeys(names_csv)
        else:
            return True
        iter += 1
    return True

async def gather_data(urls, names, list_name, selectors, types, tmp_name, pg_iter):
    async with aiohttp.ClientSession() as session:
        tasks = [ asyncio.create_task(scrap_chapter(session, urls[i-1], names, list_name, selectors, types, tmp_name, pg_iter)) for i in range( 1, len(urls) + 1 )  ]
        await asyncio.gather(*tasks)
    return True


def parse(urls, names, list_name, selectors, types, tm_name, pg_iter):
    tm_name = tm_name.replace(".xml", "")
    wFile = open("parsing results/" + tm_name + '-' + str(datetime.date.today()) + ".csv", mode = "w", encoding = 'utf-8')
    file_writer = csv.DictWriter(wFile, delimiter = ';', lineterminator = '\n', fieldnames = names)
    meta_field = dict.fromkeys(names)
    for name in names:
        meta_field[name] = name

    file_writer.writerow(meta_field)
    print("[INFO] Header writed!")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(gather_data(urls, names, list_name, selectors, types, tm_name, pg_iter))

    return True

def session(queue = list()):
    for template in queue:
        if not template.is_ok():
            return False
    for template in queue:
        parse(template.urls, template.names, template.list_name, template.selectors, template.types, template.name)
    return True

def page_iter(i, template_str):
    return eval(template_str)


#    semaphore = asyncio.Semaphore(200)
#    async with semaphore: