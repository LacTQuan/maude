# How to run?
1. Clone this repo to the local machine
2. Clone the mcover-agent lib through this [link](https://github.com/LacTQuan/cover-agent.git)
3. Install it by using `pip install 'path_to_the_cover_agent_repo'`
4. Navigate into a specific folder: astar/dijkstra/lpastar. Example:
```
cd cover-agent/astar & 
cover-agent \
  --source-file-path "app.py" \
  --test-file-path "test_app.py" \
  --project-root "." \
  --code-coverage-report-path "coverage.xml" \
  --test-command "pytest --cov=. --cov-report=xml --cov-report=term" \
  --test-command-dir "." \
  --coverage-type "cobertura" \
  --desired-coverage 99 \
  --max-iterations 10 \
  --prompt-path "prompt.json" \
  --additional-instructions "However, do not assert exception messages or any string-based messages in assertions, as these may lead to test failures due to minor variations." \
  --model "gpt-4o-mini"
```
