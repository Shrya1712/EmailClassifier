import re
import spacy
from typing import List, Dict, Tuple, Any

class PIIMasker:
    def __init__(self):
        """
        Initialize the PII masker
        """
        # Load SpaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If model not found, download it
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Define regex patterns for different PII entities
        self.patterns = {
            "full_name": r'\b(?:Mr|Mrs|Ms|Dr|Prof)\. [A-Z][a-z]+(?: [A-Z][a-z]+)?\b',  # Matches titles followed by names
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone_number": r'(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b',
            "dob": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            "aadhar_num": r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b',
            "credit_debit_no": r'\b(?:\d{4}[ -]?){4}\b',
            "cvv_no": r'\bCVV:? \d{3,4}\b|\bCVV \d{3,4}\b|\b\d{3,4} CVV\b',
            "expiry_no": r'\b(?:0[1-9]|1[0-2])[/-]\d{2,4}\b|\bExp:? \d{2}[/-]\d{2,4}\b'
        }
        
        # Additional patterns for international phone numbers
        self.phone_patterns = [
            r'\+\d{1,3}[-\s]?\d{1,3}[-\s]?\d{3,4}[-\s]?\d{3,4}\b',  # International format
            r'\+\d{1,3}[-\s]?\d{2}[-\s]?\d{4}[-\s]?\d{4}\b',        # Asian format
            r'\+\d{1,3}[-\s]?\d{2}[-\s]?\d{3,4}[-\s]?\d{4}\b'       # European format
        ]
    
    def detect_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect PII entities in the given text
        
        Args:
            text: Input text to scan for PII
            
        Returns:
            List of dictionaries containing detected entities with their positions and types
        """
        entities = []
        
        # Process with SpaCy for named entities
        doc = self.nlp(text)
        
        # Extract named entities from SpaCy
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities.append({
                    "position": [ent.start_char, ent.end_char],
                    "classification": "full_name",
                    "entity": ent.text
                })
        
        # Add logging to see which parts of the text are being matched
        print("SpaCy detected entities:", entities)
        
        # Apply regex patterns for other PII types
        for entity_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Check if this entity overlaps with any existing one
                overlap = False
                for existing_entity in entities:
                    if (match.start() >= existing_entity["position"][0] and 
                        match.start() <= existing_entity["position"][1]) or \
                       (match.end() >= existing_entity["position"][0] and 
                        match.end() <= existing_entity["position"][1]):
                        overlap = True
                        break
                
                if not overlap:
                    entities.append({
                        "position": [match.start(), match.end()],
                        "classification": entity_type,
                        "entity": match.group()
                    })
                
                # Log each regex match
                print(f"Regex detected {entity_type}: {match.group()} at position {match.start()}-{match.end()}")
        
        # Check additional phone patterns
        for pattern in self.phone_patterns:
            for match in re.finditer(pattern, text):
                # Check for overlap
                overlap = False
                for existing_entity in entities:
                    if (match.start() >= existing_entity["position"][0] and 
                        match.start() <= existing_entity["position"][1]) or \
                       (match.end() >= existing_entity["position"][0] and 
                        match.end() <= existing_entity["position"][1]):
                        overlap = True
                        break
                
                if not overlap:
                    entities.append({
                        "position": [match.start(), match.end()],
                        "classification": "phone_number",
                        "entity": match.group()
                    })
                
                # Log each phone number match
                print(f"Regex detected phone_number: {match.group()} at position {match.start()}-{match.end()}")
        
        # Sort entities by position
        entities.sort(key=lambda x: x["position"][0])
        
        return entities
    
    def mask_text(self, text: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Mask PII entities in the given text
        
        Args:
            text: Input text to mask
            
        Returns:
            Tuple containing masked text and list of detected entities
        """
        entities = self.detect_entities(text)
        masked_text = text
        
        # Apply masking from end to beginning to maintain correct positions
        for entity in reversed(entities):
            start, end = entity["position"]
            entity_type = entity["classification"]
            masked_text = masked_text[:start] + f"[{entity_type}]" + masked_text[end:]
        
        # Format entities for API response
        formatted_entities = []
        for entity in entities:
            formatted_entities.append({
                "position": entity["position"],
                "classification": entity["classification"],
                "entity": entity["entity"]
            })
        
        return masked_text, formatted_entities
