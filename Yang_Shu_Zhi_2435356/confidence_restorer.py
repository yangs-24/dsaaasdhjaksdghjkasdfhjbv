# confidence_restorer.py
# Custom Feature: Restore Word with Confidence Score
# Contributor: Shu Zhi Yang
# DAAA/2A/03

from trie import Trie

class ConfidenceRestorer:
    def __init__(self):
        self.trie = Trie()
    
    def restore_with_confidence(self, word_with_wildcards):
        """
        Restore a wildcard word using matches from the trie and show confidence scores.
        """
        matches = self.trie.find_all_matches(word_with_wildcards)
        if not matches:
            print(f"No matches found for '{word_with_wildcards}'.")
            return

        # Get word frequencies from the trie
        total_frequency = 0
        word_frequencies = []

        for word in matches:
            node = self.trie.root
            for char in word:
                node = node.children[char]

            if node and node.is_terminal:
                word_frequencies.append((word, node.frequency))
                total_frequency += node.frequency

        # Display the results
        print(f"Restoring: {word_with_wildcards}")
        print("Possible Matches with Confidence Scores:")
        for word, freq in word_frequencies:
            confidence = (freq / total_frequency) * 100
            print(f" - {word} ({confidence:.2f}%)")


    def restore_confidence_menu(self):
        """
        Display the menu for restoring words with confidence scores.
        """
        while True:
            try:
                print("\n" + "-"*50)
                print("Confidence Restorer Menu:")
                print("-"*50)
                print("1. Restore Word with Wildcards")
                print("2. Exit to Main Menu")
                print("-"*50)
                choice = input("Enter your choice (1-2): ").strip()
                
                if choice == '1':
                    word_with_wildcards = input("Enter the word with wildcards (e.g., 'c*t'): ").strip()
                    if word_with_wildcards:
                        self.restore_with_confidence(word_with_wildcards)
                    else:
                        print("Invalid input. Please enter a word with wildcards.")
                        
                elif choice == '2':
                    print("Returning to Main Menu...")
                    break
                    
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
                    
            except KeyboardInterrupt:
                print("\nReturning to Main Menu...")
                break
            except Exception as e:
                print(f"Error: {e}")