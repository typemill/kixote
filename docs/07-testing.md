# Testing

You can auto-test the application when running it either with **Python** or **Docker**.

## Running with Python

Create a virtual environment, install dependencies, and run the application with:

```bash
python3 run.py
```

You should add all required parameters manually in `/common/config.py`.

## Running with Docker

Run the application with Docker, including test data.  
Example:

```bash
docker run -d \
  -p 5000:5000 \
  -v /path/on/host/data:/data \
  -e KIXOTE_DB_PATH=/data/clients.db \
  -e LOGIN_REQUIRED=true \
  -e ADMIN_KEY=admin123 \
  -e SECRET_KEY=secret123 \
  -e JWT_SECRET_KEY=jwt123 \
  -e CLIENT_LIMIT_MAKER=220 \
  -e CLIENT_LIMIT_BUSINESS=1220 \
  --name kixote-app \
  kixote-app
```

## Parameters

You should test both cases with:

- `LOGIN_REQUIRED=true`
- `LOGIN_REQUIRED=false`

## Run `tests.sh`

The bash script **`tests.sh`** will run the autotests, call all endpoints, and print the responses in the console.  

Run it from the console with:

```bash
./tests.sh local|prod ADMIN_KEY
```

Where:
- `local` → tests against `http://localhost:5000`
- `prod` → tests against `https://kixote.typemill.net`
