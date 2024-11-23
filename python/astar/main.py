import maude
maude.init()

maude.load("./python/astar/race_condition.maude")

astar_module = maude.getModule("BANK-ACCOUNTS")
initial_term = astar_module.parseTerm("init")
search_pattern = astar_module.parseTerm("testTransferSuccess")
print(type(search_pattern))

try:
    # search_result = initial_term.search(target=search_pattern, type=1)
    search_result = search_pattern.reduce()

    if search_result:
        solution = next(search_result)
        print("Solution found:")
        print(solution)
    else:
        print("No solutions found.")

except Exception as e:
    print(f"An error occurred: {e}")