# Email Classification and PII Masking API

This project is a Flask-based API for classifying emails and masking Personally Identifiable Information (PII). It uses machine learning models to classify emails into categories and employs natural language processing (NLP) techniques to detect and mask PII such as names, email addresses, phone numbers, and more.

## Features

- **Email Classification**: Classifies emails into predefined categories.
- **PII Masking**: Detects and masks PII entities like full names, email addresses, phone numbers, credit card numbers, etc.
- **API Endpoint**: Provides a RESTful API endpoint for easy integration.

## Setup Instructions

### Prerequisites

- Python 3.12 or later
- Virtual environment (recommended)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <https://github.com/Shrya1712/EmailClassifier>
   cd <emailCLassifier>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements_compatible.txt
   ```

4. **Download SpaCy Language Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application

1. **Start the Flask Server**:
   ```bash
   python app.py
   ```

   The server will start on `http://127.0.0.1:7860`.

## Using the API

### Endpoint

- **POST** `/classify_email`

### Request Body

Send a JSON object with the `email_body` field containing the email text:

```json
{
  "email_body": "Your email text here"
}
```

### Response

The API returns a JSON response with the following fields:

- `input_email_body`: The original email text.
- `list_of_masked_entities`: A list of detected PII entities with their classifications and positions.
- `masked_email`: The email text with PII entities masked.
- `category_of_the_email`: The classification category of the email.

### Testing with Postman

1. Open Postman and create a new `POST` request.
2. Set the URL to `http://localhost:7860/classify_email`.
3. Add a header: `Content-Type: application/json`.
4. In the body, select `raw` and `JSON`, then paste your email text.
5. Send the request and observe the response.

## Sample Email for Testing

```json
{
  "email_body": "Dear Mr. John Doe, I hope this message finds you well. We wanted to inform you that your account with the email john.doe@example.com has been updated. Please verify your phone number +1-800-555-0199 and your credit card number 1234-5678-9012-3456. Your next billing date is 12/25/2023. If you have any questions, feel free to contact our support team. Thank you for choosing our services. Sincerely, Dr. Jane Smith Customer Support Your Company"
}
```
