import re

class DomainClassifier:
    def classify(self, issue, subject="", company=""):
        text = f"{issue} {subject} {company}".lower()
        
        # Priority mapping with broader keywords
        if any(kw in text for kw in ['hackerrank', 'hacker rank', 'hiring account', 'assessment', 'coding test']):
            return 'hackerrank', 1.0
        if any(kw in text for kw in ['claude', 'anthropic', 'bedrock', 'model access', 'workspace']):
            return 'claude', 1.0
        if any(kw in text for kw in ['visa', 'card', 'transaction', 'payment', 'travel', 'merchant', 'spent', 'spending']):
            return 'visa', 1.0
            
        return 'unknown', 0.0

class RiskScanner:
    def scan(self, text):
        text = text.lower()
        critical_patterns = [r'stolen', r'compromised', r'breach', r'fraud', r'unauthorized', r'security vulnerability']
        high_patterns = [r'refund', r'billing error', r'cannot login', r'hacked']
        
        flags = []
        for p in critical_patterns:
            if re.search(p, text):
                flags.append(p)
        if flags:
            return 'critical', flags
            
        for p in high_patterns:
            if re.search(p, text):
                flags.append(p)
        if flags:
            return 'high', flags
            
        return 'low', []

class IntentClassifier:
    def __init__(self):
        self.keywords = {
            'how_to': ['how', 'guide', 'steps', 'procedure', 'help'],
            'billing': ['cost', 'price', 'subscription', 'pay', 'invoice'],
            'bug_report': ['error', 'fail', 'broken', 'not working'],
            'feature_request': ['want', 'need', 'add', 'suggest']
        }

    def classify(self, text):
        text = text.lower()
        for intent, kws in self.keywords.items():
            if any(kw in text for kw in kws):
                return intent
        return 'unknown'

class ProductAreaClassifier:
    def classify(self, text, domain):
        text = text.lower()
        
        # Enhanced keyword-based classification
        if domain == 'hackerrank':
            if any(kw in text for kw in ['assessment', 'test', 'exam', 'certificate', 'score', 'challenge', 'submission']):
                return 'assessment_platform'
            elif any(kw in text for kw in ['interview', 'candidate', 'interviewer', 'mock', 'screen share']):
                return 'interview_tool'
            elif any(kw in text for kw in ['subscription', 'billing', 'payment', 'invoice', 'refund', 'pause', 'cancel']):
                return 'billing'
            elif any(kw in text for kw in ['account', 'login', 'password', 'user', 'member', 'employee', 'remove', 'delete']):
                return 'account_settings'
            elif any(kw in text for kw in ['resume', 'profile', 'job', 'apply']):
                return 'candidate_management'
            else:
                return 'candidate_management'
                
        elif domain == 'claude':
            if any(kw in text for kw in ['api', 'bedrock', 'aws', 'request', 'failing', 'error', 'integration']):
                return 'api_usage'
            elif any(kw in text for kw in ['subscription', 'billing', 'payment', 'invoice', 'cost', 'price']):
                return 'billing'
            elif any(kw in text for kw in ['security', 'vulnerability', 'data', 'privacy', 'crawl', 'training']):
                return 'compliance'
            elif any(kw in text for kw in ['workspace', 'team', 'access', 'seat', 'member', 'organization']):
                return 'account_management'
            elif any(kw in text for kw in ['lti', 'student', 'professor', 'education']):
                return 'integrations'
            else:
                return 'web_interface'
                
        elif domain == 'visa':
            if any(kw in text for kw in ['stolen', 'lost', 'fraud', 'identity', 'blocked', 'compromised']):
                return 'card_security'
            elif any(kw in text for kw in ['transaction', 'payment', 'charge', 'dispute', 'refund', 'merchant', 'spend']):
                return 'transactions'
            elif any(kw in text for kw in ['travel', 'abroad', 'international', 'paris', 'trip']):
                return 'travel_support'
            elif any(kw in text for kw in ['cash', 'atm', 'withdraw']):
                return 'transactions'
            else:
                return 'transactions'
                
        return 'unknown'
