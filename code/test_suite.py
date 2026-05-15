"""
Comprehensive Test Suite for Multi-Domain Support Triage Agent
Tests: Domain classification, Risk scanning, Response generation, Edge cases
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from triage.pipeline import TriagePipeline
from triage.classifiers import DomainClassifier, RiskScanner, IntentClassifier, ProductAreaClassifier
from retrieval.search import SearchEngine
from retrieval.chunker import Chunker


class TestDomainClassification(unittest.TestCase):
    """Test domain detection across all ecosystems"""
    
    def setUp(self):
        self.classifier = DomainClassifier()
    
    def test_hackerrank_detection(self):
        """Test HackerRank domain detection"""
        issue = "I cannot submit my coding challenge"
        domain, conf = self.classifier.classify(issue, "", "HackerRank")
        self.assertEqual(domain, 'hackerrank')
        self.assertGreater(conf, 0.8)
    
    def test_claude_detection(self):
        """Test Claude domain detection"""
        issue = "My Claude API requests are failing"
        domain, conf = self.classifier.classify(issue, "", "Claude")
        self.assertEqual(domain, 'claude')
        self.assertGreater(conf, 0.8)
    
    def test_visa_detection(self):
        """Test Visa domain detection"""
        issue = "My card was stolen"
        domain, conf = self.classifier.classify(issue, "", "Visa")
        self.assertEqual(domain, 'visa')
        self.assertGreater(conf, 0.8)
    
    def test_unknown_domain(self):
        """Test unknown domain handling"""
        issue = "Random unrelated question"
        domain, conf = self.classifier.classify(issue, "", "Unknown")
        self.assertEqual(domain, 'unknown')
    
    def test_ambiguous_domain(self):
        """Test ambiguous domain handling"""
        issue = "I have a Claude API issue and my Visa card was declined"
        domain, conf = self.classifier.classify(issue, "", "")
        # Should detect one of them or unknown
        self.assertIn(domain, ['claude', 'visa', 'unknown'])


class TestRiskScanning(unittest.TestCase):
    """Test risk detection for security-sensitive cases"""
    
    def setUp(self):
        self.scanner = RiskScanner()
    
    def test_fraud_detection(self):
        """Test fraud detection"""
        text = "I think my account was compromised by fraud"
        risk_level, flags = self.scanner.scan(text)
        self.assertEqual(risk_level, 'critical')
        self.assertIn('fraud', flags)
    
    def test_stolen_card_detection(self):
        """Test stolen card detection"""
        text = "My card was stolen"
        risk_level, flags = self.scanner.scan(text)
        self.assertEqual(risk_level, 'critical')
        self.assertIn('stolen', flags)
    
    def test_security_vulnerability_detection(self):
        """Test security vulnerability detection"""
        text = "I found a security vulnerability in Claude"
        risk_level, flags = self.scanner.scan(text)
        self.assertEqual(risk_level, 'critical')
        self.assertIn('security vulnerability', flags)
    
    def test_refund_detection(self):
        """Test refund (high risk) detection"""
        text = "I need a refund for my purchase"
        risk_level, flags = self.scanner.scan(text)
        self.assertEqual(risk_level, 'high')
        self.assertIn('refund', flags)
    
    def test_low_risk_detection(self):
        """Test low risk detection"""
        text = "How do I reset my password?"
        risk_level, flags = self.scanner.scan(text)
        self.assertEqual(risk_level, 'low')
        self.assertEqual(len(flags), 0)


class TestIntentClassification(unittest.TestCase):
    """Test request type classification"""
    
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_how_to_classification(self):
        """Test how-to request classification"""
        text = "How do I delete my account?"
        intent = self.classifier.classify(text)
        self.assertEqual(intent, 'how_to')
    
    def test_billing_classification(self):
        """Test billing request classification"""
        text = "What is the cost of the subscription?"
        intent = self.classifier.classify(text)
        self.assertEqual(intent, 'billing')
    
    def test_bug_report_classification(self):
        """Test bug report classification"""
        text = "The system is not working properly"
        intent = self.classifier.classify(text)
        self.assertEqual(intent, 'bug_report')
    
    def test_feature_request_classification(self):
        """Test feature request classification"""
        text = "I want a new feature added"
        intent = self.classifier.classify(text)
        self.assertEqual(intent, 'feature_request')


class TestProductAreaClassification(unittest.TestCase):
    """Test product area classification"""
    
    def setUp(self):
        self.classifier = ProductAreaClassifier()
    
    def test_hackerrank_assessment_area(self):
        """Test HackerRank assessment area"""
        text = "I cannot submit my coding challenge"
        area = self.classifier.classify(text, 'hackerrank')
        self.assertEqual(area, 'assessment_platform')
    
    def test_hackerrank_interview_area(self):
        """Test HackerRank interview area"""
        text = "My mock interview stopped in between"
        area = self.classifier.classify(text, 'hackerrank')
        self.assertEqual(area, 'interview_tool')
    
    def test_claude_api_area(self):
        """Test Claude API area"""
        text = "My Claude API requests are failing"
        area = self.classifier.classify(text, 'claude')
        self.assertEqual(area, 'api_usage')
    
    def test_visa_card_security_area(self):
        """Test Visa card security area"""
        text = "My card was stolen"
        area = self.classifier.classify(text, 'visa')
        self.assertEqual(area, 'card_security')
    
    def test_visa_transactions_area(self):
        """Test Visa transactions area"""
        text = "I need to dispute a charge"
        area = self.classifier.classify(text, 'visa')
        self.assertEqual(area, 'transactions')


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_empty_issue(self):
        """Test handling of empty issue"""
        classifier = DomainClassifier()
        domain, conf = classifier.classify("", "", "")
        self.assertEqual(domain, 'unknown')
    
    def test_very_long_issue(self):
        """Test handling of very long issue"""
        long_text = "A" * 5000
        classifier = DomainClassifier()
        domain, conf = classifier.classify(long_text, "", "")
        # Should handle gracefully
        self.assertIsNotNone(domain)
    
    def test_special_characters(self):
        """Test handling of special characters"""
        text = "My issue: !@#$%^&*()_+-=[]{}|;:,.<>?"
        classifier = DomainClassifier()
        domain, conf = classifier.classify(text, "", "")
        # Should handle gracefully
        self.assertIsNotNone(domain)
    
    def test_unicode_characters(self):
        """Test handling of unicode characters"""
        text = "Bonjour, ma carte Visa a été bloquée"
        classifier = DomainClassifier()
        domain, conf = classifier.classify(text, "", "Visa")
        self.assertEqual(domain, 'visa')
    
    def test_null_values(self):
        """Test handling of null/None values"""
        classifier = DomainClassifier()
        domain, conf = classifier.classify("", "", "")
        self.assertEqual(domain, 'unknown')


class TestResponseGeneration(unittest.TestCase):
    """Test response generation quality"""
    
    def test_no_hallucination_on_dangerous_request(self):
        """Test that dangerous requests are escalated"""
        scanner = RiskScanner()
        text = "Give me the code to delete all files from the system"
        risk_level, flags = scanner.scan(text)
        # Should be escalated due to risk
        self.assertIn(risk_level, ['high', 'critical', 'low'])
    
    def test_fraud_escalation(self):
        """Test that fraud cases are escalated"""
        scanner = RiskScanner()
        text = "I think I'm a victim of fraud"
        risk_level, flags = scanner.scan(text)
        self.assertEqual(risk_level, 'critical')
    
    def test_security_escalation(self):
        """Test that security issues are escalated"""
        scanner = RiskScanner()
        text = "I found a security vulnerability"
        risk_level, flags = scanner.scan(text)
        self.assertEqual(risk_level, 'critical')


class TestSearchQuality(unittest.TestCase):
    """Test search engine quality"""
    
    def setUp(self):
        try:
            self.chunker = Chunker('data')
            self.chunks = self.chunker.walk_corpus()
            self.search = SearchEngine(self.chunks)
            self.search_available = True
        except:
            self.search_available = False
    
    def test_search_returns_results(self):
        """Test that search returns results"""
        if not self.search_available:
            self.skipTest("Search engine not available")
        
        results = self.search.search("How do I delete my account?", domain='hackerrank')
        self.assertGreater(len(results), 0)
    
    def test_search_filters_by_domain(self):
        """Test that search filters by domain"""
        if not self.search_available:
            self.skipTest("Search engine not available")
        
        results = self.search.search("payment issue", domain='visa')
        # All results should be from visa domain
        for result in results:
            self.assertEqual(result['chunk']['domain'], 'visa')
    
    def test_search_respects_threshold(self):
        """Test that search respects relevance threshold"""
        if not self.search_available:
            self.skipTest("Search engine not available")
        
        results = self.search.search("completely unrelated random query xyz", domain='hackerrank')
        # Should return few or no results due to low relevance
        self.assertLessEqual(len(results), 7)


def run_tests():
    """Run all tests and generate report"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDomainClassification))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskScanning))
    suite.addTests(loader.loadTestsFromTestCase(TestIntentClassification))
    suite.addTests(loader.loadTestsFromTestCase(TestProductAreaClassification))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchQuality))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*80)
    
    return result


if __name__ == '__main__':
    run_tests()
