import json
from datetime import datetime

RULE_PATH = "data/rules.json"
LOG_PATH = "logs/session.log"


# Loads rules from JSON. Returns None if file is missing.
def load_rules(file):
    try:
        with open(file, "r") as data:
            return json.load(data)
    except FileNotFoundError:
        print("Rules file not found")
        return None


# Checks all rules have required fields. Logs all problems at once.
def validate_rules(rules_list):
    if not rules_list:
        return False

    req_fields = ["id", "category", "keywords", "rule", "severity", "action_required"]
    is_valid = True

    for rule in rules_list:
        for field in req_fields:
            if field not in rule:
                print(f"WARNING: {rule.get('id')} is missing field: {field}")
                is_valid = False

    return is_valid


# Matches rules by keywords. Lowercased for case-insensitive search.
def search_rules(query, rules_list):
    result_list = []
    query_txt = query.lower()
    for rule in rules_list:
        keywords = rule.get("keywords")
        for key in keywords:
            if key in query_txt and rule not in result_list:
                result_list.append(rule)
    return result_list


# Wrapper around search_rules for scenario mode.
def check_scenario(scenario, rules_list):
    violations = search_rules(scenario, rules_list)
    return violations


# Prints a warning header if violations found, clean message if not.
def display_violations(violations):
    if not violations:
        print("No compliance violations detected")
        return
    print("⚠️  VIOLATION DETECTED")
    display_results(violations)


# Prints matched rules in formatted blocks.
def display_results(results):
    if not results:
        print("No matching rules found")
        return
    for result in results:
        print("─────────────────────────────")
        print(f'ID      : {result.get("id")}')
        print(f'Category: {result.get("category")}')
        print(f'Severity: {result.get("severity")}')
        print(f'Rule    : {result.get("rule")}')
        print(f'Action  : {result.get("action_required")}')
        print("─────────────────────────────\n")


# logs records of what is asked and what is returned
def log_session(query, results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    matches_num = len(results)
    log = f"[{timestamp}] QUERY: {query} | MATCHES: {matches_num}"
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"{log}\n")


# Main function that keeps the chatbot running in a loop.
def main():
    rules_list = load_rules(RULE_PATH)

    if validate_rules(rules_list):
        print(f"{len(rules_list)} rules loaded successfully")
    else:
        print("Rule validation failed.")

    print("ComplianceCLI — AML/KYC Assistant")
    print("Type your question, or start with 'scenario:' to check a transaction.")
    while True:
        usr_input = input("You: ")
        if usr_input.lower() in ["quit", "exit"]:
            print("Goodbye.")
            break
        if "scenario" in usr_input:
            sc = usr_input.removeprefix("scenario:")
            result = check_scenario(sc, rules_list)
            display_violations(result)
            log_session(sc, result)
        else:
            result = search_rules(usr_input, rules_list)
            display_results(result)
            log_session(usr_input, result)


if __name__ == "__main__":
    main()
