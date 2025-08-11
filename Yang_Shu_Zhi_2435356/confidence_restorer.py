# confidence_restorer.py
# Custom Feature: Restore Word with Confidence Score
# Contributor: Shu Zhi Yang
# DAAA/2A/03

from trie import Trie

class ConfidenceRestorer:
    def __init__(self, trie: Trie):
        """
        Initializes the ConfidenceRestorer with a shared Trie instance.
        """
        self.trie = trie
    
    def restore_with_confidence(self, word_with_wildcards):
        """
        Restores a wildcard word using matches from the trie and shows confidence scores.
        """
        # Use the wildcard_search method which returns (word, frequency) tuples
        matches = self.trie.wildcard_search(word_with_wildcards.lower())
        
        if not matches:
            print(f"No matches found for '{word_with_wildcards}'.")
            return

        # Calculate the total frequency from all matches found
        total_frequency = sum(freq for word, freq in matches)

        if total_frequency == 0:
            print(f"Matches found for '{word_with_wildcards}', but they have no frequency data.")
            print("Possible Matches:", [word for word, freq in matches])
            return

        # Display the results with confidence scores
        print(f"\nRestoring: {word_with_wildcards}")
        print("Possible Matches with Confidence Scores:")
        for word, freq in matches:
            confidence = (freq / total_frequency) * 100
            print(f" - {word} ({confidence:.2f}%)")


    def restore_confidence_menu(self):
        """
        Displays the menu for restoring words with confidence scores.
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
                    print("Invalid choice. Please enter either 1 or 2.")
                    
            except KeyboardInterrupt:
                print("\nReturning to Main Menu...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")