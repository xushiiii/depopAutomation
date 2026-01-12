import base64
import requests

CLIENT_ID = "TaylorXu-resellin-PRD-8e8d9c741-c2ba1544"
CLIENT_SECRET = "PRD-e8d9c741f912-2366-4c12-abf6-c796"

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
SCOPE = "https://api.ebay.com/oauth/api_scope"

def get_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError("Missing EBAY_CLIENT_ID / EBAY_CLIENT_SECRET env vars.")

    basic = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {basic}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials",
        "scope": SCOPE,
    }
    r = requests.post(TOKEN_URL, headers=headers, data=data, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

def get_tree_id(token):
    r = requests.get(
        "https://api.ebay.com/commerce/taxonomy/v1/get_default_category_tree_id",
        headers={"Authorization": f"Bearer {token}"},
        params={"marketplace_id": "EBAY_US"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["categoryTreeId"]

def suggest_categories(token, tree_id, query):
    r = requests.get(
        f"https://api.ebay.com/commerce/taxonomy/v1/category_tree/{tree_id}/get_category_suggestions",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": query},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("categorySuggestions", [])

def format_full_path(suggestion):
    cat = suggestion.get("category", {}) or {}
    cat_id = str(cat.get("categoryId", ""))
    cat_name = str(cat.get("categoryName", ""))

    ancestors = suggestion.get("categoryTreeNodeAncestors", []) or []
    # ancestors often come leaf->root, so reverse for root->leaf display
    path_names = [a.get("categoryName", "") for a in reversed(ancestors) if a.get("categoryName")]
    full_path = " > ".join(path_names + ([cat_name] if cat_name else []))

    return cat_id, cat_name, full_path

def main():
    token = get_token()
    tree_id = get_tree_id(token)

    while True:
        q = input("Search (blank to quit): ").strip()
        if not q:
            break

        suggestions = suggest_categories(token, tree_id, q)
        if not suggestions:
            print("No results.\n")
            continue

        for s in suggestions[:10]:
            cat_id, cat_name, full_path = format_full_path(s)
            # Print full path so you can see Men's vs Women's branches
            print(f"{cat_id}  {full_path or cat_name}")
        print()

if __name__ == "__main__":
    main()