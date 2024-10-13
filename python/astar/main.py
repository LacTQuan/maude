import maude
maude.init()

maude.load("../../maude_code/ogata/dijkstra/astar00.maude")

astar_module = maude.getModule("ASTAR")
initial_term = astar_module.parseTerm("init")
search_pattern = astar_module.parseTerm("{(gstat: found) OCs}")
print(type(search_pattern))

try:
    search_result = initial_term.search(target=search_pattern, type=1)

    if search_result:
        solution = next(search_result)
        print("Solution found:")
        print(solution)
    else:
        print("No solutions found.")

except Exception as e:
    print(f"An error occurred: {e}")