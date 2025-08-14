# Kixote PDF Service – WeasyPrint Endpoint

## Generate PDF

Generate a PDF from HTML using the WeasyPrint service.

### Request

**POST** `/weasyprint/pdf`

**Headers:**
- `Authorization: Bearer YOUR_JWT_TOKEN`
- `Content-Type: application/json`

**Body:**  
You can provide the following fields (all except `html` are optional):

```json
{
  "html": "<h1>Hello, PDF!</h1><p>This is a test document.</p>",
  "css": "h1 { color: red; }",                // string or list of strings
  "metadata": {"title": "My PDF"},            // dictionary
  "zoom": 1.0,                                // number
  "base_url": "https://example.com",          // string
  "presentational_hints": true,               // boolean
  "optimize_size": ["images", "fonts"],       // list
  "filename": "custom.pdf"                    // string
}
```

---

### Example cURL

```sh
curl -X POST http://localhost:5000/book/pdf \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d @payload.json \
  --output output.pdf
```

---

### Example Python (requests)

```python
import requests

headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "html": "<h1>Hello, PDF!</h1><p>This is a test document.</p>",
    "filename": "custom.pdf"
}
response = requests.post("http://localhost:5000/book/pdf", json=data, headers=headers)
with open("output.pdf", "wb") as f:
    f.write(response.content)
```

---

### Example PHP (using cURL)

```php
<?php
$token = 'YOUR_JWT_TOKEN';
$data = [
    "html" => "<h1>Hello, PDF!</h1><p>This is a test document.</p>",
    "filename" => "custom.pdf"
];
$ch = curl_init('http://localhost:5000/book/pdf');
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer $token",
    "Content-Type: application/json"
]);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
file_put_contents('output.pdf', $response);
curl_close($ch);
?>
```

---

### Example JavaScript (fetch, Node.js or browser)

```javascript
fetch("http://localhost:5000/book/pdf", {
  method: "POST",
  headers: {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    html: "<h1>Hello, PDF!</h1><p>This is a test document.</p>",
    filename: "custom.pdf"
  })
})
.then(response => response.blob())
.then(blob => {
  // For browser: download the PDF
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = "output.pdf";
  document.body.appendChild(a);
  a.click();
  a.remove();
  // For Node.js: use fs to write blob to file
});
```

---

### Response

- Returns a PDF file as a download (`output.pdf` or your chosen filename).
- If the request is invalid, returns a JSON error message.

**Example error response:**
```json
{
  "error": "Missing 'html' in request body"
}
```