# context_analyzer.py
# ST1507 CA2 - Context Analyzer Feature
# Additional Feature for Newspaper Restoration App
# Ashley Yong Lok Xi
# DAAA/2A/03

import re
from collections import Counter, defaultdict
from datetime import datetime
import string

class ContextAnalyzer:
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'under', 'over',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
            'her', 'its', 'our', 'their'
        }
        
        # Common newspaper section keywords
        self.section_keywords = {
            'news': ['breaking', 'report', 'incident', 'announce', 'government', 'official'],
            'sports': ['game', 'match', 'team', 'player', 'score', 'championship', 'league'],
            'business': ['company', 'market', 'stock', 'economy', 'profit', 'revenue', 'trade'],
            'entertainment': ['movie', 'film', 'actor', 'actress', 'music', 'concert', 'show'],
            'weather': ['temperature', 'rain', 'sunny', 'cloudy', 'storm', 'forecast'],
            'obituary': ['died', 'passed', 'funeral', 'survived', 'memorial', 'beloved']
        }
        
        # Time-related patterns
        self.time_patterns = {
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'time': r'\b\d{1,2}:\d{2}(?:\s*[APap][Mm])?\b',
            'year': r'\b\d{4}\b',
            'month': r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
        }

    def analyze_text(self, text):
        """
        Main analysis function that returns comprehensive context analysis
        """
        if not text or not text.strip():
            return {"error": "No text provided for analysis"}
        
        # Clean and prepare text
        cleaned_text = self._clean_text(text)
        words = self._extract_words(cleaned_text)
        
        analysis = {
            'basic_stats': self._get_basic_stats(text, words),
            'content_analysis': self._analyze_content(words),
            'section_classification': self._classify_section(words),
            'temporal_analysis': self._analyze_temporal_elements(text),
            'readability': self._analyze_readability(text, words),
            'keywords': self._extract_keywords(words),
            'sentiment_indicators': self._basic_sentiment_analysis(words)
        }
        
        return analysis

    def _clean_text(self, text):
        """Clean text for analysis"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        return text

    def _extract_words(self, text):
        """Extract words from text"""
        # Convert to lowercase and remove punctuation
        text = text.lower()
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        return words

    def _get_basic_stats(self, original_text, words):
        """Get basic text statistics"""
        sentences = re.split(r'[.!?]+', original_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        paragraphs = original_text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        return {
            'character_count': len(original_text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
            'avg_sentences_per_paragraph': len(sentences) / len(paragraphs) if paragraphs else 0
        }

    def _analyze_content(self, words):
        """Analyze content characteristics"""
        if not words:
            return {}
        
        # Filter out stop words
        content_words = [word for word in words if word not in self.stop_words]
        
        # Most common words
        word_freq = Counter(content_words)
        most_common = word_freq.most_common(10)
        
        # Unique words ratio
        unique_ratio = len(set(words)) / len(words) if words else 0
        
        return {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'content_words': len(content_words),
            'unique_word_ratio': round(unique_ratio, 3),
            'most_common_words': most_common,
            'vocabulary_richness': len(content_words) / len(words) if words else 0
        }

    def _classify_section(self, words):
        """Classify text into newspaper sections"""
        section_scores = defaultdict(int)
        
        for word in words:
            for section, keywords in self.section_keywords.items():
                if word in keywords:
                    section_scores[section] += 1
        
        # Calculate confidence scores
        total_matches = sum(section_scores.values())
        section_confidence = {}
        
        if total_matches > 0:
            for section, score in section_scores.items():
                section_confidence[section] = round(score / total_matches, 3)
        
        predicted_section = max(section_scores, key=section_scores.get) if section_scores else "unknown"
        
        return {
            'predicted_section': predicted_section,
            'confidence_scores': dict(section_confidence),
            'keyword_matches': dict(section_scores)
        }

    def _analyze_temporal_elements(self, text):
        """Analyze temporal elements in text"""
        temporal_elements = {}
        
        for element_type, pattern in self.time_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            temporal_elements[element_type] = matches
        
        return temporal_elements

    def _analyze_readability(self, text, words):
        """Basic readability analysis"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences or not words:
            return {}
        
        # Calculate basic readability metrics
        avg_sentence_length = len(words) / len(sentences)
        
        # Count syllables (rough approximation)
        syllable_count = 0
        for word in words:
            syllable_count += max(1, len(re.findall(r'[aeiouAEIOU]', word)))
        
        avg_syllables_per_word = syllable_count / len(words) if words else 0
        
        # Simple readability score (based on sentence length and syllables)
        readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Classify reading level
        if readability_score >= 90:
            level = "Very Easy"
        elif readability_score >= 80:
            level = "Easy"
        elif readability_score >= 70:
            level = "Fairly Easy"
        elif readability_score >= 60:
            level = "Standard"
        elif readability_score >= 50:
            level = "Fairly Difficult"
        elif readability_score >= 30:
            level = "Difficult"
        else:
            level = "Very Difficult"
        
        return {
            'avg_sentence_length': round(avg_sentence_length, 2),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2),
            'readability_score': round(readability_score, 2),
            'reading_level': level
        }

    def _extract_keywords(self, words):
        """Extract potential keywords"""
        # Filter out stop words and short words
        keywords = [word for word in words if word not in self.stop_words and len(word) > 3]
        
        # Count frequency
        keyword_freq = Counter(keywords)
        
        # Get top keywords
        top_keywords = keyword_freq.most_common(15)
        
        return {
            'top_keywords': top_keywords,
            'keyword_count': len(set(keywords))
        }

    def _basic_sentiment_analysis(self, words):
        """Basic sentiment analysis using word lists"""
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'positive',
            'success', 'achievement', 'victory', 'win', 'celebrate', 'happy', 'joy',
            'love', 'like', 'enjoy', 'pleased', 'satisfied', 'delighted', 'thrilled'
        }
        
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'negative', 'problem', 'issue',
            'failure', 'defeat', 'loss', 'sad', 'angry', 'disappointed', 'frustrated',
            'hate', 'dislike', 'worried', 'concerned', 'crisis', 'disaster', 'tragedy'
        }
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            sentiment = "neutral"
            confidence = 0
        else:
            if positive_count > negative_count:
                sentiment = "positive"
                confidence = positive_count / total_sentiment_words
            elif negative_count > positive_count:
                sentiment = "negative"
                confidence = negative_count / total_sentiment_words
            else:
                sentiment = "neutral"
                confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'positive_indicators': positive_count,
            'negative_indicators': negative_count
        }

    def display_analysis(self, analysis):
        """Display analysis results in a formatted way"""
        if 'error' in analysis:
            print(f"Error: {analysis['error']}")
            return
        
        print("\n" + "="*60)
        print("CONTEXT ANALYSIS REPORT")
        print("="*60)
        
        # Basic Statistics
        print("\nBASIC STATISTICS")
        print("-" * 30)
        stats = analysis['basic_stats']
        print(f"Characters: {stats['character_count']:,}")
        print(f"Words: {stats['word_count']:,}")
        print(f"Sentences: {stats['sentence_count']:,}")
        print(f"Paragraphs: {stats['paragraph_count']:,}")
        print(f"Avg words per sentence: {stats['avg_words_per_sentence']:.1f}")
        
        # Content Analysis
        print("\nCONTENT ANALYSIS")
        print("-" * 30)
        content = analysis['content_analysis']
        if content:
            print(f"Unique words: {content['unique_words']:,}")
            print(f"Vocabulary richness: {content['vocabulary_richness']:.3f}")
            print(f"Most common words: {', '.join([f'{word}({count})' for word, count in content['most_common_words'][:5]])}")
        
        # Section Classification
        print("\nSECTION CLASSIFICATION")
        print("-" * 30)
        section = analysis['section_classification']
        print(f"Predicted section: {section['predicted_section'].upper()}")
        if section['confidence_scores']:
            print("Confidence scores:")
            for sec, score in sorted(section['confidence_scores'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {sec}: {score:.3f}")
        
        # Temporal Analysis
        print("\nTEMPORAL ELEMENTS")
        print("-" * 30)
        temporal = analysis['temporal_analysis']
        for element_type, matches in temporal.items():
            if matches:
                print(f"{element_type.capitalize()}: {', '.join(matches[:3])}")
        
        # Readability
        print("\nREADABILITY")
        print("-" * 30)
        readability = analysis['readability']
        if readability:
            print(f"Reading level: {readability['reading_level']}")
            print(f"Readability score: {readability['readability_score']:.1f}")
            print(f"Avg sentence length: {readability['avg_sentence_length']:.1f} words")
        
        # Keywords
        print("\nTOP KEYWORDS")
        print("-" * 30)
        keywords = analysis['keywords']
        if keywords['top_keywords']:
            keyword_list = [f"{word}({count})" for word, count in keywords['top_keywords'][:10]]
            print(", ".join(keyword_list))
        
        # Sentiment
        print("\nSENTIMENT INDICATORS")
        print("-" * 30)
        sentiment = analysis['sentiment_indicators']
        print(f"Overall sentiment: {sentiment['sentiment'].upper()}")
        print(f"Confidence: {sentiment['confidence']:.3f}")
        print(f"Positive indicators: {sentiment['positive_indicators']}")
        print(f"Negative indicators: {sentiment['negative_indicators']}")
        
        print("\n" + "="*60)

def context_analyzer_menu():
    """Menu function for context analyzer"""
    analyzer = ContextAnalyzer()
    
    while True:
        print("\n" + "="*50)
        print("CONTEXT ANALYZER")
        print("="*50)
        print("1. Analyze text from input")
        print("2. Analyze text from file")
        print("3. Back to main menu")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nEnter text to analyze (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            
            text = "\n".join(lines[:-1])  # Remove the last empty line
            
            if text.strip():
                analysis = analyzer.analyze_text(text)
                analyzer.display_analysis(analysis)
            else:
                print("No text provided for analysis.")
        
        elif choice == '2':
            filename = input("Enter filename: ").strip()
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                if text.strip():
                    analysis = analyzer.analyze_text(text)
                    analyzer.display_analysis(analysis)
                else:
                    print("File is empty or contains no readable text.")
            
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found.")
            except Exception as e:
                print(f"Error reading file: {e}")
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Integration for the main application
def integrate_context_analyzer():
    """
    Function to integrate context analyzer into the main newspaper restoration app
    This should be called from one of the additional feature menu options
    """
    try:
        context_analyzer_menu()
    except Exception as e:
        print(f"Error in context analyzer: {e}")

if __name__ == "__main__":
    # Test the context analyzer
    context_analyzer_menu()