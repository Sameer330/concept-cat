import wikipediaapi
import requests
from bs4 import BeautifulSoup
import re
import os
import sys
import time

if not os.path.exists('pages'):
    os.mkdir('pages')
    # Create 'pages' directory in current directory - if not found.
    # Stores all 'crawled' text files

index_dictionary = {}
# {'url': 0 or 1} --- 
#                   1 - First Entry to queue
#                   0 - Already exists in the index_dictionary

links_list = []
# Queue for processing URLs through crawler

def stripLinks(soup):
    links = soup.findAll('a')
    # Extract all links from the seed
    for link in links:
        if 'href' in link.attrs and 'wiki' in link.attrs['href'] and 'http' in link.attrs['href'] and '#' not in link.attrs['href']:
            # --- "#" links generally point to a sub-section
            # of the current page. Hence ignore them.

            if link not in index_dictionary:
                links_list.append(link['href'])
                # Append only if link was not previously crawled

                index_dictionary[link['href']] = 1;
                # Assign 1 to indicate 'first-time' entry to crawler

            elif link in index_dictionary:
                index_dictionary[link['href']] = 0;
                # Link tried to re-enter crawler


wiki = wikipediaapi.Wikipedia('en')
# Set WIKI Language - ENGLISH

url = requests.get("https://en.wikipedia.org/wiki/Special:Random") 
# Seed URL - DO NOT DELETE

if url.status_code != 200:
    print("STATUS_CODE ERROR!\n")
    quit(url.status_code)
    # Quit the program with whatever 'status_code' returns
    # 200 - Request Successfull ---> Does not quit
    # 404 - Page not found
    # Quits even if link is broken


while os.stat(os.path.join(sys.path[0], "pages")).st_size <= 10485760:
    # Loop until the 'pages' directory crosses the 10MB size mark.

    soup = BeautifulSoup(url.content, "html.parser")

    stripLinks(soup)
    # Extract Links

    title = soup.find('title').get_text()
    # Extract page title

    text = str(soup.get_text())
    # Extract all text data from URL

    links_list.append(str(url))
    # Start Queue Here

    index_dictionary[url.url] = 1
    # Index the Seed URL - Marks first entry

    
    url = requests.get(str(links_list[0]))
    # Update Seed URL

    links_list.pop(0)
    # Pop the updated URL
    text = re.sub(r'(\n\s*\n)', '\n\n', text)
    # Replaces unwanted 'new line' characters with '\n\n' - Saves file storage space

    with open(os.path.join(sys.path[0] + "\\pages\\", title + ".txt"), "w", encoding="utf-8") as file:
        # Creates/Opens the 'crawled' files in 'pages' directory
        # contained in the current directory

        file.write(text)
        # Writes altered text to a .txt file

        time.sleep(0.05) # TESTING
        # Usually file operations are slower than scraping
        # Due to speed differences this might cause a program crash
        # Hence the sleep() function. But Program still crashed!

    file.close()


# 10MB === 10485760 B

# BASIC ALGORITHM

# Run a loop until 'pages' directory size >= 10MB
#   Feed initial Seed URL
#   Strip Link from the page - Store it in 'links_list' --- √
#   Append all links to a 'queue' --- √
#   Load all link to 'index_dictionary'. --- √
#       Assign 1 if link is new else assign 0 if already exists --- √
#   extract title --> (title + '.txt') --- File Name --- √
#   extarct text --> File Content --- √
#   Write to File --- √
#   Update Seed URL from queue --- √
#   POP queue at (0) --- √
# Return to Loop