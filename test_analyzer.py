import unittest
import spacy
from app import NaturalLanguagePipeline, SyntaxTreeAnalyzer

class TestSyntaxTreeAnalyzer(unittest.TestCase):
    """
    Automated Unit Testing suite utilizing standard AAA (Arrange, Act, Assert) patterns.
    Validates structural graph traversal and edge-case syntax topology.
    """
    @classmethod
    def setUpClass(cls):
        """Executed once before the suite runs to load infrastructure into memory."""
        # Initialize the pipeline via the same architecture used in production
        cls.pipeline = NaturalLanguagePipeline()

    def test_standard_svo_extraction(self):
        """Validates that a straightforward declarative sentence extracts correctly."""
        # Arrange
        sentence = "猫抓了一个老鼠。"
        doc = self.pipeline.process_text(sentence)
        analyzer = SyntaxTreeAnalyzer(doc)

        # Act
        result = analyzer.extract_svo_schema()

        # Assert
        self.assertEqual(result["subject"], "猫")
        self.assertEqual(result["verb"], "抓")
        self.assertEqual(result["object"], "一个老鼠")

    def test_missing_object_sentence(self):
        """Ensures the graph fallback yields 'Unknown' safely when an object is absent."""
        # Arrange
        sentence = "我今天在学校吃。"
        doc = self.pipeline.process_text(sentence)
        analyzer = SyntaxTreeAnalyzer(doc)

        # Act
        result = analyzer.extract_svo_schema()

        # Assert
        self.assertEqual(result["subject"], "我")
        self.assertEqual(result["verb"], "吃")
        self.assertEqual(result["object"], "Unknown")

    def test_empty_string_graceful_failure(self):
        """Guarantees robustness when processing an anomalous empty string vector."""
        # Arrange
        sentence = ""
        doc = self.pipeline.process_text(sentence)
        analyzer = SyntaxTreeAnalyzer(doc)

        # Act
        result = analyzer.extract_svo_schema()

        # Assert
        self.assertEqual(result["subject"], "Unknown")
        self.assertEqual(result["verb"], "Unknown")
        self.assertEqual(result["object"], "Unknown")

if __name__ == "__main__":
    unittest.main()


