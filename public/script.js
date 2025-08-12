document.getElementById('send').addEventListener('click', async () => {
  const phrases = document.getElementById('phrases').value
    .split('\n')
    .map(p => p.trim())
    .filter(Boolean);

  const response = await fetch('/api/minus', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phrases })
  });

  const data = await response.json();
  document.getElementById('result').textContent = data.minusWords || 'Ошибка при запросе';
});
