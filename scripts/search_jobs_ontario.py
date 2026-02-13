import urllib.request
import json
import ssl

headers = {
    'X-Subscription-Token': 'BSAY8R4E_8hBk4sbvnojJC8YE-vHfxZ',
    'Accept': 'application/json'
}

# Search 2: Ontario
url2 = 'https://api.search.brave.com/res/v1/web/search?q=entry+level+Data+Analyst+jobs+Toronto+Ontario+2025+site%3Aindeed.com+OR+site%3Alinkedin.com&count=10&country=ca'

ctx = ssl.create_default_context()

print("=== ONTARIO DATA ANALYST JOBS ===")
req2 = urllib.request.Request(url2, headers=headers)
with urllib.request.urlopen(req2, context=ctx) as response:
    data = json.loads(response.read().decode())
    for i, result in enumerate(data['web']['results'][:10], 1):
        print(f"{i}. Title: {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Description: {result['description'][:200]}...")
        print('---')

# Save results to file
with open('search_results_ontario.json', 'w') as f:
    json.dump(data['web']['results'][:10], f, indent=2)
