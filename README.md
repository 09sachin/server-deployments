# 🔧 Bash Script Trigger HTTP Server

This is a lightweight Python-based HTTP server that listens for incoming HTTP requests and executes predefined bash scripts based on the request URL and authenticated headers.

---

## 📌 Features

* Simple HTTP server using Python's built-in `socket` module
* Executes bash scripts mapped to URL endpoints
* Authenticates requests using `Client-ID` and `Client-Secret` headers
* Uses a `.env` file to configure allowed endpoints and secrets

---

## 🚀 How It Works

1. **Client sends HTTP request** with a `Client-ID` and `Client-Secret` in the headers
2. **URL is matched** with a bash script path defined in `.env`
3. **If authenticated**, the server executes the bash script using `subprocess`
4. **Returns HTTP response** confirming script execution

---

## 📁 .env Configuration

Create a `.env` file in the same directory with the following format:

```env
ClientId=your_client_id
ClientSecret=your_client_secret

# Script URLs and paths (use index numbers consistently)
ScriptUrl1=/deploy-service-a
ScriptPath1=/path/to/deploy-service-a.sh

ScriptUrl2=/restart-db
ScriptPath2=/path/to/restart-db.sh

# Add more as needed
```

> 🔐 The index numbers must match (e.g., `ScriptUrl3` corresponds to `ScriptPath3`)

---

## 🧑‍💻 Running the Server

```bash
python3 server.py
```

The server will start on `127.0.0.1:8080`.

---

## 📬 Example Request

```http
POST /deploy-service-a HTTP/1.1
Host: localhost:8080
Client-ID: your_client_id
Client-Secret: your_client_secret
```

### ✅ Successful Response

```http
HTTP/1.1 200 OK
Content-Type: text/html

Deployment done!
```

### ❌ Invalid Client ID/Secret

```http
HTTP/1.1 400 Bad Request
Content-Type: text/html

Client ID or Client Secret missing
```

### ❌ Unknown URL

```http
HTTP/1.1 400 Bad Request
Content-Type: text/html

Page missing
```

---

## 🔐 Security Notes

* This server does **not** use HTTPS. Use only on **trusted networks**.
* Keep `.env` safe and secure with strong credentials.
* For production:

  * Place the server behind an HTTPS reverse proxy like Nginx
  * Use firewall/IP whitelisting
  * Consider adding token-based or OAuth authentication

---

## 🐳 Docker Support (Optional)

To run this with Docker:

**Dockerfile**

```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY server.py ./
COPY .env ./
CMD ["python", "server.py"]
```

**Build and run**

```bash
docker build -t bash-trigger-server .
docker run -p 8080:8080 bash-trigger-server
```

---

## 📜 License

MIT License
