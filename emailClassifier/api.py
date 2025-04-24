from flask import Flask, request, jsonify
from models import EmailClassifier
from utils import PIIMasker

def create_app():
    """
    Create and configure the Flask application
    
    Returns:
        Flask application
    """
    app = Flask(__name__)
    
    # Initialize classifier and masker
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
    
    return app

# For direct execution
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=7860)
