from .classifiers import DomainClassifier, RiskScanner, IntentClassifier, ProductAreaClassifier
from .generator import OllamaGenerator
from retrieval.search import SearchEngine
import logging

class TriagePipeline:
    def __init__(self, search_engine):
        self.domain_classifier = DomainClassifier()
        self.risk_scanner = RiskScanner()
        self.intent_classifier = IntentClassifier()
        self.product_area_classifier = ProductAreaClassifier()
        self.generator = OllamaGenerator(model="llama3")
        self.search_engine = search_engine
        self.logger = logging.getLogger('triage')

    def process_ticket(self, ticket):
        ticket_id = ticket.get('ticket_id', 'unknown')
        issue = ticket.get('Issue', '')
        subject = ticket.get('Subject', '')
        company = ticket.get('Company', '')

        # 1. Domain Detection
        domain, domain_conf = self.domain_classifier.classify(issue, subject, company)
        
        # 2. Risk Screening
        risk_level, risk_flags = self.risk_scanner.scan(issue)
        
        # 3. Intent & Product Area Classification
        request_type = self.intent_classifier.classify(issue)
        if request_type == 'unknown':
            categories = ['how_to', 'billing', 'bug_report', 'feature_request', 'account_access', 'feedback']
            request_type = self.generator.classify(issue, categories)

        product_area = self.product_area_classifier.classify(issue, domain)
        if product_area == 'unknown' and domain != 'unknown':
            areas = {
                'hackerrank': ['assessment_platform', 'interview_tool', 'candidate_management', 'account_settings', 'integrations'],
                'claude': ['api_usage', 'web_interface', 'billing', 'model_performance', 'compliance'],
                'visa': ['card_security', 'transactions', 'travel_support', 'digital_wallets', 'benefits']
            }
            if domain in areas:
                product_area = self.generator.classify(issue, areas[domain])
        
        # 4. Retrieval - Search for Top-7 for balance
        search_results = self.search_engine.search(issue, domain=domain, top_k=7)
        
        # NEW: Check for contradictions in retrieved docs
        if search_results and self.search_engine.detect_contradictions(search_results):
            decision = 'escalate'
            justification = "Conflicting information found in documentation. Requires human review."
        
        decision = 'reply'
        justification = "Direct documentation found."
        
        if risk_level in ['critical', 'high']:
            decision = 'escalate'
            justification = f"High risk detected: {', '.join(risk_flags)}"
        elif not search_results:
            decision = 'escalate'
            justification = "No relevant documentation found in corpus."
        elif domain == 'unknown':
            decision = 'escalate'
            justification = "Could not determine the relevant ecosystem."
            
        # 5. Response Generation
        if decision == 'reply':
            top_result = search_results[0]['chunk']
            title = top_result.get('title', 'Support Documentation')
            path = top_result.get('path', '')
            
            # DYNAMIC CONTEXT: Use Top-5 for LLM (Speed)
            llm_context = "\n\n---\n\n".join([r['chunk']['text'] for r in search_results[:5]])
            llm_response = self.generator.generate_response(issue, llm_context, domain)
            
            # Check if LLM says it doesn't have information - if so, escalate
            if llm_response and ("don't have enough information" in llm_response.lower() or 
                                 "i don't have" in llm_response.lower() or
                                 "not have enough information" in llm_response.lower()):
                decision = 'escalate'
                justification = "Documentation found but does not contain sufficient information to answer the query."
                response = "I am escalating your request to a human agent for further assistance. Our documentation does not have a direct answer for this specific case."
            elif llm_response and not llm_response.startswith("Error"):
                response = f"{llm_response}\n\nReference: {title} ({path})"
            else:
                # FALLBACK: If LLM fails, escalate
                decision = 'escalate'
                justification = "LLM generation failed or timed out."
                response = "I am escalating your request to a human agent for further assistance. Our documentation does not have a direct answer for this specific case."
        else:
            response = "I am escalating your request to a human agent for further assistance. "
            if risk_level == 'critical':
                response += "This involves a sensitive security or fraud matter that requires manual review."
            else:
                response += "Our documentation does not have a direct answer for this specific case."
        
        return {
            "ticket_id": ticket_id,
            "domain": domain,
            "risk_level": risk_level,
            "request_type": request_type,
            "product_area": product_area,
            "decision": decision,
            "response": response,
            "justification": justification,
            "top_docs": [r['chunk']['chunk_id'] for r in search_results]
        }
