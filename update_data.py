import requests, json

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

keywords = [
    "ai tool",
    "ai assistant",
    "text-to-image",
    "llm",
    "ai generator",
    "chatbot",
    "voice ai",
    "audio ai",
    "video ai"
]

def get_category(keyword):
    keyword = keyword.lower()
    if "text-to-image" in keyword or "image" in keyword:
        return "Imagen"
    if "chatbot" in keyword or "assistant" in keyword:
        return "Chatbot"
    if "voice" in keyword or "audio" in keyword:
        return "Audio"
    if "video" in keyword:
        return "Video"
    if "text" in keyword or "nlp" in keyword:
        return "Texto"
    return "General"

def search_github(query):
    params = {
        "q": query + " in:name,description",
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }
    response = requests.get(GITHUB_SEARCH_URL, params=params)
    return response.json()

def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def exists(data, repo_url):
    return any(item.get("link") == repo_url for item in data)

def main():
    data = load_data()

    for kw in keywords:
        result = search_github(kw)
        items = result.get("items", [])

        for item in items:
            repo_url = item["html_url"]
            name = item["name"]
            desc = item.get("description") or "Sin descripción"
            category = get_category(kw)

            if not exists(data, repo_url):
                data.append({
                    "name": name,
                    "category": category,
                    "keywords": [kw],
                    "link": repo_url,
                    "description": desc
                })

    save_data(data)
    print("data.json actualizado con GitHub API")

if __name__ == "__main__":
    main()
