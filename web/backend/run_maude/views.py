from django.shortcuts import render
import os
from django.http import JsonResponse
from rest_framework.decorators import APIView
import traceback

import maude

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


class MaudeView(APIView):
    def get(self, request, format=None):
        maude.init()

        algo_path = request.query_params.get('algo_path', None)
        maude.load(algo_path)

        module_name = request.query_params.get('module', None)
        module = maude.getModule(module_name)
        test_case_path = request.query_params.get('test_case', None)
        try:
            initial_terms, goal_terms, test_titles = read_test_case(test_case_path if test_case_path != None else "./python/dijkstra/test_cases_gpt4o.txt")
            ans = []

            for i in range(len(initial_terms)):
                ans.append({
                    'test_title': test_titles[i],
                    'initial': initial_terms[i],
                    'goal': goal_terms[i],
                })
                initial_term = module.parseTerm(initial_terms[i])
                goal_term = module.parseTerm(goal_terms[i])

                try:
                    search_result = initial_term.search(target=goal_term, type=1)
                    print(search_result)
                    solution = next(search_result)
                    ans[-1]['solution'] = str(solution)
                except Exception as e:
                    ans[-1]['error'] = f"Cannot find solution {e}"

            return JsonResponse({'results': ans})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        finally:
            maude

