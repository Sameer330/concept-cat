import wikipediaapi
import wikipedia

wiki = wikipediaapi.Wikipedia('en')
# Wikipedia language set to English

input_text = str(input("Enter Input: "))
# User Input
# Accepts valid English words/phrases/sentences
# Does not accept "Gibberish"

results = wikipedia.search(input_text)
# Returns a list of search results for the input query
# returns valid topics relating to your input

if len(results) == 0:
    # If no topics are found
    # either the query is not in English
    # or some unintelligible word was entered
    print("Could not fetch enough results!")
    print("Please check your query and try again!")
    quit(0)
    # Quits with ERRORCODE - 0
    # 0 - signifies 'zero' results returned during search

for i in range(len(results)):
    page = wiki.page(results[i], unquote=False)
    # Scrapes the Wikipedia site for the subject containes in 'results[i]'

    if page.exists():
        # Executes only if webpage is not broken 
        print(i + 1, ".", page.title, ":", page.fullurl, "\n\t", page.summary, "\n")
    else:
        print("Could not find Page: Exists?", page.exists())