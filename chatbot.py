import json

RULE_PATH = "data/rules.json"


def load_rules(file):
    try:
        with open(file, "r") as data:
            return json.load(data)
    except FileNotFoundError:
        print("Rules file not found")
        return None


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


def search_rules(query, rules_list):
    result_list = []
    query_txt = query.lower()
    for rule in rules_list:
        keywords = rule.get("keywords")
        for key in keywords:
            if key in query_txt and rule not in result_list:
                result_list.append(rule)
    return result_list


def check_scenario(scenario, rules_list):
    violations = search_rules(scenario, rules_list)
    return violations


def display_violations(violations):
    if not violations:
        print("No compliance violations detected")
        return
    print("⚠️  VIOLATION DETECTED")
    display_results(violations)


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
        else:
            result = search_rules(usr_input, rules_list)
            display_results(result)


if __name__ == "__main__":
    main()
