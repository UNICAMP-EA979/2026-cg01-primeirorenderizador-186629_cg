start = """name: Autograding Tests
on: push
permissions:
  checks: write
  actions: read
  contents: read
jobs:
  run-autograding-tests:
    runs-on: ubuntu-latest
    if: github.actor != 'github-classroom[bot]'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python 3.12
        uses: actions/setup-python@v2
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          python3 -m pip install --upgrade pip
          python3 -m pip install .[tests]
"""

step_template = """      - name: {name}
        id: {id}
        uses: classroom-resources/autograding-command-grader@v1
        with:
            test-name: {name}
            setup-command: ""
            command: pytest {path}
            timeout: 2
            max-score: {score}
"""

result_template = """{name}: "${{{{steps.{id}.outputs.result}}}}""""


reporter_step_template = """      - name: Autograding Reporter
        uses: classroom-resources/autograding-grading-reporter@v1
        env:
          {results}
        with:
            runners: {ids}
      
"""

if __name__ == "__main__":
    rules = []
    with open("grading.txt") as file:
        rules = file.readlines()

    result = ""

    ids = set()
    results = []
    for rule in rules:
        if rule == "" or rule == "\n":
            continue

        rule = rule.split(" ")
        path = rule[0]
        score = int(rule[1])

        test_name = path.split("/")[-1].split("::")[-1].removesuffix(".py")
        test_id = test_name.replace("_", "")

        if test_id in ids:
            raise ValueError("Duplicated test name")
        ids.add(test_id)

        step = step_template.format(
            name=test_name, id=test_id, path=path, score=score)

        result = result + step

        result_name = test_id.upper()+"_RESULTS"
        results.append(result_template.format(name=result_name, id=test_id))

    reporter_results = "\n          ".join(results)
    reporter_ids = ",".join(ids)
    result += reporter_step_template.format(
        results=reporter_results, ids=reporter_ids)

    result = start + result

    with open("classroom.yml", "w") as file:
        file.write(result)
