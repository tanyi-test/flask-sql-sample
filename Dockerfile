from python
workdir /app
copy . .

run pip install --no-cache-dir -r requirements.txt
cmd ["python", "app.py"]
