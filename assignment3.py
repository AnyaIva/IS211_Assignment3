import datetime
import argparse
import urllib.request
import csv
import io
import re


def downloadData(url):                                    ## Downloads the data returns the data as a string
                                                           
    
    with urllib.request.urlopen(url) as response:
        file_data = response.read().decode('utf-8')
    return file_data


def process_url(file_data):
    image_hits = 0

                                                           
    browser_dict = {
        'IE': 0,
        'Safari': 0,
        'Chrome': 0,
        'Firefox': 0
    }                                                      ## dict to store browser hits

   
    csv_reader = csv.reader(io.StringIO(file))
    for i, row in enumerate(csv_reader):
        path_to_file = row[0]
        datetime_accessed = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') 
        browser = row[2]
        status = row[3]
        request_size = row[4]
        print(row)

        if re.search(r"\.gif|\.jpe?g|\.png", path_to_file.lower()): 
            image_hits += 1
                                                           ## checks browser and update dict
        if browser.upper().find("IE") != -1:
            browser_dict['IE'] += 1
        elif browser.upper().find("Firefox") != -1:
            browser_dict['Firefox'] += 1
        elif browser.upper().find("Chrome") != -1:
            browser_dict['Chrome'] += 1
        elif browser.upper().find("Safari") != -1:
            browser_dict["Safari"] += 1
     
    avg_hits = image_hits/(i + 1) * 100
    print(f'Image requests account for {avg_hits}% of all requests.')
    most_popular = max(browser_dict)                                            ## Finds most popular browser
    print('The most popular browser is', most_popular )

def main(url):
    print(f"Running main with URL = {url}...")
    data = downloadData(url)
    process_url(data)   

if __name__ == "__main__":
    """Main entry point"""
   ## http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
