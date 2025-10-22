#Negi Chen
# crawler/fetch_fei.py

from bs4 import BeautifulSoup;
import pandas as pd;
import requests;
import time;

# if http respond 200 means ok to get this web page
URL = "https://racing.hkjc.com/racing/english/international-racing/world-rankings/world50-ranking.aspx";

def fetch_hkjc_world50_ranking(url: str = URL) -> pd.DataFrame:
    #1 load page
    readHtml = requests.get(url, timeout=15);
    # to print to check the page is possible to print
    print("Status code:", readHtml.status_code);
    # print(html.content);
    # print(soup.p);
    readHtml.raise_for_status(); #if there is error(404, 500)

    #2 parser HTML
    # store the content of the web accessed
    src = readHtml.content;
    soup = BeautifulSoup(src, 'lxml');

    # 3) check if we can see HTML content
    print("\n=== print partial HTML ===")
    print(soup.prettify()[:500]);   

    #4 find the table
    table = soup.find("table");
    if table is None:
        raise RuntimeError("No <table> found.");

    # get the table header 
    # 1.1
    thead_th = [th.get_text(strip = True) for th in table.select("th")];
    print("\n=== table headers ===");
    print(thead_th);
    
    # print first few rows
    # 1.2
    rows = [];
    for tr in table.find_all("tr")[1:5]: #only take front five rows
        tds = [td.get_text(strip=True) for td in tr.find_all("td")];
        print("\n=== table dash===");
        print(tds);
        rows.append(tds);

    # create DataFrame just to preview
    # 1.1 + 1.2
    if thead_th and rows:
        df = pd.DataFrame(rows, columns=thead_th[:len(rows[0])]);
        return df;
        print(df);
    else:
        print("Could not extract table properly.")
        return pd.DataFrame();


# run the function
fetch_hkjc_world50_ranking();



