#Negi Chen
# crawler/fetch_fei.py
# this file is to extract data from web, and then return clean pandas DataFrame
# DataFrame (raw)  (BeautifulSoup + pandas)

from bs4 import BeautifulSoup;  #html parser machine
import pandas as pd;  #deal with data
import requests;  #http request
# import time;

# if http respond 200 means ok to get this web page
URL = "https://racing.hkjc.com/racing/english/international-racing/world-rankings/world50-ranking.aspx";

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_hkjc_world50_ranking(url: str = URL) -> pd.DataFrame:
    #1 load page
    readHtml = requests.get(url, headers=HEADERS, timeout=15);
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

    # get the table header (if there is not thead then use tr)
    # 1.1
    thead_th = [th.get_text(strip = True) for th in table.select("th")];
    if not thead_th:
        first_tr = table.find("tr");
        if first_tr:
            thead_th =[td.get_text(strip=True) for td in first_tr.find_all("td")]
    
    print("\n=== table headers ===");
    print(thead_th);
    
    # print first few rows
    # 1.2
    rows = [];
    for tr in table.find_all("tr")[1:]: #if u only take front five rows should use like [1:5]:
        tds = [td.get_text(strip=True) for td in tr.find_all("td")];
        # print("\n=== table dash===");
        # print(tds);
        rows.append(tds);

    # this is for basic check
    if not thead_th or not rows:
        raise RuntimeError("Failed to extract headers or rows.")

    # ---incase colume different
    col_n = len(max(rows, key = len));
    # let head the same as well
    thead_th = thead_th[:col_n];
    # every different rows add err string
    rows = [r[:col_n] + [""] * (col_n - len(r)) for r in rows];
    
    # create DataFrame just to preview
    # 1.1 + 1.2
    if thead_th and rows:
        df = pd.DataFrame(rows, columns=thead_th);
        print("\n=== check the extract datas ===");
        print(df.head());
        return df;
    else:
        print("Could not extract table properly.")
        return pd.DataFrame(); 


# run the function
fetch_hkjc_world50_ranking();



# This script fetches the HKJC World 50 horse ranking table from the official website.
# It sends an HTTP request, parses the HTML using BeautifulSoup, and extracts table headers and rows into a DataFrame.