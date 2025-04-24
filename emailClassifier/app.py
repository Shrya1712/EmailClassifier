import os
import json
from flask import Flask, request, jsonify
from models import EmailClassifier
from utils import PIIMasker

# Initialize Flask app
app = Flask(__name__)

# Load the classifier and masker
classifier = EmailClassifier()
masker = PIIMasker()

@app.route('/classify_email', methods=['POST'])
def classify_email():
    """
    API endpoint to classify an email and mask PII
    
    Request body:
        JSON with 'email_body' field containing the email text
        
    Returns:
        JSON response with classification results and masked entities
    """
    try:
        # Get email body from request
        data = request.json
        
        if not data or 'email_body' not in data:
            return jsonify({"error": "Missing email_body in request"}), 400
        
        email_body = data['email_body']
        
        # Mask PII entities
        masked_email, entities = masker.mask_text(email_body)
        
        # Classify the masked email
        category = classifier.predict(masked_email)
        
        # Format response
        response = {
            "input_email_body": email_body,
            "list_of_masked_entities": entities,
            "masked_email": masked_email,
            "category_of_the_email": category
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
