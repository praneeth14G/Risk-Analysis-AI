// static/script.js — Frontend interactivity

async function doSearch() {
  const query = document.getElementById('searchQuery').value.trim();
  const resultDiv = document.getElementById('searchResult');

  if (!query) {
    resultDiv.textContent = 'Please enter a search query.';
    return;
  }

  resultDiv.textContent = 'Searching and generating AI response...';

  try {
    const formData = new FormData();
    formData.append('query', query);

    const response = await fetch('/web-search', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    resultDiv.textContent = data.result || 'No result returned.';
  } catch (err) {
    resultDiv.textContent = 'Search failed: ' + err.message;
  }
}