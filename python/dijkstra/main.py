import maude
import sys

def read_test_case(file_path):
    initial_terms = []
    goal_terms = []
    test_titles = []

    with open(file_path, "r") as file:
        lines = file.readlines()

        for i in range(len(lines)):
            if lines[i].strip() == "Init state:" or lines[i].strip() == "Goal state:":
                j = i + 1
                term = lines[j].strip()
                j += 1
                while j < len(lines) and lines[j].strip() != "":
                    term += " " + lines[j].strip()
                    j += 1
                
                if lines[i].strip() == "Init state:":
                    initial_terms.append(term)
                elif lines[i].strip() == "Goal state:":
                    goal_terms.append(term)
                
                i = j
            elif lines[i].strip().startswith("Test"):
                test_titles.append(lines[i].strip())

    return initial_terms, goal_terms, test_titles

if __name__ == "__main__":

    maude.init()
    maude.load(sys.argv[1] if len(sys.argv) > 1 else "./maude_code/ogata/dijkstra/dijkstra00.maude")

    dijkstra_module = maude.getModule("DIJKSTRA")
    try:
        initial_terms, goal_terms, test_titles = read_test_case(sys.argv[2] if len(sys.argv) > 2 else "./python/dijkstra/test_cases/qwen2.txt")

        for i in range(len(initial_terms)):
            print(test_titles[i])
            initial_term = dijkstra_module.parseTerm(initial_terms[i])
            goal_term = dijkstra_module.parseTerm(goal_terms[i])

            try:
                search_result = initial_term.search(target=goal_term, type=1)
                solution = next(search_result)
                print("Solution found:")
                print(solution)
            except Exception as e:
                print(f"Cannot find solution {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

# ../../maude_code/ogata/dijkstra/dijkstra00.maude
# ./test_cases.txt
        