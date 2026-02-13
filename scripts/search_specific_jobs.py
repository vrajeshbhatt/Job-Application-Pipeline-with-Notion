import urllib.request
import json
import ssl

headers = {
    'X-Subscription-Token': 'BSAY8R4E_8hBk4sbvnojJC8YE-vHfxZ',
    'Accept': 'application/json'
}

searches = [
    ("Altus Group Data Analyst Halifax", "Altus Group"),
    ("entry level data analyst CGI IBM Accenture Canada 2025", "Consulting"),
    ("government data analyst Nova Scotia New Brunswick 2025", "Government"),
    ("RBC TD Scotiabank data analyst entry level 2025", "Banking"),
    ("fintech data analyst Toronto entry level 2025", "FinTech")
]

ctx = ssl.create_default_context()
all_results = []

for query, category in searches:
    print(f"\n=== {category}: {query} ===")
    url = f'https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}&count=5&country=ca'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            data = json.loads(response.read().decode())
            for result in data['web']['results'][:5]:
                print(f"- {result['title']}")
                print(f"  {result['url']}")
                all_results.append({
                    'category': category,
                    'title': result['title'],
                    'url': result['url'],
                    'description': result['description']
                })
    except Exception as e:
        print(f"Error: {e}")

# Save all results
with open('job_search_detailed.json', 'w') as f:
    json.dump(all_results, f, indent=2)

print(f"\nTotal results collected: {len(all_results)}")
