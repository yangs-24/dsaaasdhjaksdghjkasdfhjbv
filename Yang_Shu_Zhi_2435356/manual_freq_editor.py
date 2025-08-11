# manual_freq_editor.py
# Custom Feature: Manual Frequency Editor
# Contributor: Shu Zhi Yang
# DAAA/2A/03

from trie import Trie

class ManualFrequencyEditor:
    def __init__(self):
        self.trie = Trie()

    def edit_frequency(self, word, new_freq):
        """
        Edits the frequency of a word in the trie if it exists.
        """
        if not word:
            print("Word cannot be empty.")
            return False

        word = word.lower().strip()
        node = self.trie.root

        for char in word:
            if char not in node.children:
                print(f"'{word}' not found in trie.")
                return False
            node = node.children[char]

        if node.is_terminal:
            old_freq = node.frequency
            node.frequency = new_freq
            print(f"Frequency for '{word}' updated from {old_freq} to {new_freq}.")
            return True
        else:
            print(f"'{word}' is a prefix, not a complete word.")
            return False

    def manual_freq_menu(self):
        """
        Display the menu for manual frequency editing.
        """
        print("\nManual Frequency Editor Menu:")
        print("1. Edit Word Frequency")
        print("2. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            word = input("Enter the word to edit frequency: ")
            new_freq = input("Enter the new frequency: ")
            try:
                new_freq = int(new_freq)
                if self.edit_frequency(word, new_freq):
                    print(f"Frequency for '{word}' successfully updated.")
            except ValueError:
                print("Invalid frequency value. Please enter a number.")
        elif choice == '2':
            return
        else:
            print("Invalid choice. Please try again.")


    def manual_freq_menu(self):
        """
        Display the menu for manual frequency editing.
        """
        while True:
            try:
                print("\n" + "-"*50)
                print("Manual Frequency Editor Menu:")
                print("-"*50)
                print("1. Edit Word Frequency")
                print("2. Display All Word Frequencies")
                print("3. Exit to Main Menu")
                print("-"*50)

                choice = input("Enter your choice (1-3): ").strip()

                if choice == '1':
                    word = input("Enter the word to edit frequency: ").strip()
                    if not word:
                        print("Invalid word. Please enter a valid word.")
                        continue
                        
                    freq_input = input("Enter the new frequency: ").strip()
                    try:
                        new_freq = int(freq_input)
                        if new_freq < 0:
                            print("Frequency must be non-negative.")
                            continue
                        self.edit_frequency(word, new_freq)
                    except ValueError:
                        print("Invalid frequency value. Please enter a number.")
                        
                elif choice == '2':
                    self.display_word_frequencies()
                    
                elif choice == '3':
                    print("Returning to Main Menu...")
                    break
                    
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")
                    
            except KeyboardInterrupt:
                print("\nReturning to Main Menu...")
                break
            except Exception as e:
                print(f"Error: {e}")
