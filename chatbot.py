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

    results = search_rules("CR7", rules_list)
    display_results(results)


if __name__ == "__main__":
    main()
