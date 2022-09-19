import wikipedia as wiki

user_input = str(input("Enter Your Query: "))

results = wiki.search(user_input)

if len(results) == 0:
    print("\n\nPlease Enter a Valid Search Query! \nError Code: 404 --- NO RESULTS OBTAINED!\nChecking Suggestions...")
    results = wiki.suggest(user_input)
    if len(results) == 0:
        print("Zero Suggestions Found!")
        quit(0)

for r in results:
    try:
        p = wiki.summary(r)
        print(r, ":\n", p, "\n\n")
    except wiki.DisambiguationError as e:
        print(e.options)
    except wiki.PageError as pe:
        print("Page Error Title:", pe.error)