# services/websearch_service.py
# Fetches live web content using Firecrawl API

import requests
from utils.config import FIRECRAWL_API_KEY

def search_web(query):
    """
    Use Firecrawl to search the web and return scraped content.
    Returns the text content as a string.
    """
    try:
        url = "https://api.firecrawl.dev/v0/search"
        headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": query,
            "pageOptions": {"onlyMainContent": True},
            "searchOptions": {"limit": 3}
        }
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
        
        # Combine content from top results
        content = ""
        for result in data.get("data", []):
            content += result.get("content", "") + "\n\n"
        
        return content if content else "No content found."
    
    except Exception as e:
        return f"Search unavailable: {str(e)}"