from trie import Trie
from text_restorer import restore_all_matches_from_file, restore_best_matches_from_file

import os

from Ashley_Yong_Lok_Xi_2435781.context_analyzer import integrate_context_analyzer
from Ashley_Yong_Lok_Xi_2435781.trie_visualizer import integrate_trie_visualizer

from Yang_Shu_Zhi_2435356.confidence_restorer import ConfidenceRestorer
from Yang_Shu_Zhi_2435356.manual_freq_editor import ManualFrequencyEditor

class NewspaperRestorationApp:
    def __init__(self):
        self.__trie = Trie()
        self.running = True
        self.conf_restorer = ConfidenceRestorer()
        self.freq_editor = ManualFrequencyEditor()

    def display_main_menu(self):
        print("\n" + "*"*65)
        print("* ST1507 DSAA: Predictive Text Editor (using tries)             *")
        print("*"+"-"*63 + "*")
        print("*" + " "*63 + "*")
        print("*  - Done by: Yang Shu Zhi (2435356) & Ashley Yong (2435781)    *")
        print("*  - Class: DAAA/2A/03                                          *")
        print("*" + " "*63 + "*")
        print("*"*65)
        print("\n\n")
        print("Please select your choice ('1','2','3','4','5','6','7'):")
        print("    1. Construct/Edit Trie")
        print("    2. Predict/Restore Text")
        print("    "+"-"*52)
        print("    3. Restore Word with Confidence (Yang Shu Zhi)")
        print("    4. Manual Frequency Editor (Yang Shu Zhi)")
        print("    "+"-"*52)
        print("    5. Context Analyzer (Ashley Yong Lok Xi)")
        print("    6. Parse Tree Grammar Validation (Ashley Yong Lok Xi)")
        print("    "+"-"*52)
        print("    7. Exit")
        
    def construct_edit_trie_menu(self):
        print("\n" + "-"*60)
        print("Construct/Edit Trie Commands:")
        print("    '+','-','?','#','@','~','=','!','\\'")
        print("-"*60)
        print("    +sunshine       (add a keyword)")
        print("    -moonlight      (delete a keyword)")
        print("    ?rainbow        (find a keyword)")
        print("    #               (display Trie)")
        print("    @               (write Trie to file)")
        print("    ~               (read keywords from file to make Trie)")
        print("    =               (write keywords from Trie to file)")
        print("    !               (print instructions)")
        print("    \\               (exit)")
        print("-"*60+"\n")

        while True:
            try:
                command = input(">").strip()
                if not command: continue

                if command == '\\':
                    print("Exiting Construct/Edit Trie Command Prompt.")
                    break

                elif command.startswith('+'):
                    word = command[1:].lower()
                    if word: 
                        self.__trie.add(word)
                        print(f"Added '{word}' to Trie.")
                    else:
                        print("Invalid keyword")

                elif command.startswith('-'):
                    word = command[1:].lower()
                    if word: 
                        if self.__trie.delete(word):
                            print(f"Deleted '{word}' from Trie.")
                        else:
                            print(f"'{word}' not found in Trie.")
                    else:
                        print("Invalid keyword")

                elif command.startswith('?'):
                    word = command[1:].lower()
                    if word:
                        if self.__trie.search(word):
                            print(f"'{word}' found in Trie")
                        else:
                            print(f"'{word}' not found in Trie")
                    else:
                        print("Invalid keyword")

                elif command == '#':
                    print("\nCurrent Trie")
                    self.__trie.display()

                elif command == '@':
                    filename = input("Enter filename to write trie: ").strip()
                    if filename:
                        self.__trie.write_to_file(filename)
                        print(f"Trie written to file '{filename}'.")
                    else:
                        print("Invalid filename")

                elif command == '~':
                    filename = input("Enter filename to read keywords: ").strip()
                    if filename:
                        try:
                            self.__trie.read_file_keywords(filename)
                            print(f"Keywords loaded from file '{filename}'.")
                        except FileNotFoundError:
                            print(f"Error: File '{filename}' not found.")
                    else:
                        print("Error: No filename entered.")

                elif command == '=':
                    filename = input("Enter filename to write keywords to: ").strip()
                    if filename:
                        try:
                            self.trie.write_keywords_to_file(filename) 
                            print(f"Keywords successfully written to '{filename}'.")
                        except IOError as e:
                            print(f"Error: Could not write to file '{filename}'.")
                            print(f"Reason: {e}")
                    else:
                        print("Error: Invalid filename.")
                
                elif command == "!":
                    self.construct_edit_trie_menu()

                else:
                    print("Invalid command. Use '!' to see available commands.")

            except KeyboardInterrupt:
                print("\nExiting Construct/Edit Trie Command Prompt.")
                break
            except Exception as e:
                print(f"Error: {e}")


    def predict_restore_text_menu(self):
        print("-" * 63)
        print("\nPredict/Restore Text Commands:")
        print("'~', '#', '$', '&', '@', '!', '\'")
        print("-" * 63)
        print("~ : Read keywords from a file to make a new prefix trie")
        print("# : Display the current prefix trie on the screen")
        print("$ : List all possible matching keywords")
        print("? : Restore a word using the best keyword match")
        print("& : Restore a text using all matching keywords")
        print("@ : Restore a text using the best keyword matches")
        print("! : Print instructions for various commands")
        print("\\ : Exit and return to main menu")

        while True:
            try:
                command = input("\nEnter command: ").strip()
                if not command: continue
                
                if command == '\\':
                    break

                elif command == '~':
                    filename = input("Enter filename to read keywords: ").strip()
                    if filename:
                        try:
                            self.__trie.read_file_keywords(filename)
                            print(f"Keywords loaded from file '{filename}'.")
                        except FileNotFoundError:
                            print(f"Error: File '{filename}' not found.")
                    else:
                        print("Error: No filename entered.")

                elif command == '#':
                    print("\nCurrent Trie")
                    self.__trie.display()
                
                elif command.startswith('$'):
                    pattern = command[1:].lower()
                    if pattern:
                        matches = self.__trie.wildcard_search(pattern)
                        print(f"Matches found: {[word for word, freq in matches]}")
                
                elif command.startswith('?'):
                    pattern = command[1:].lower()
                    if pattern:
                        best = self.__trie.best_match(pattern)
                        print(f"Best match: <{best[0]}>" if best else "No match found.")
            
                elif command == '&':
                    filename = input("Enter defect text file: ")
                    restore_all_matches_from_file(self.__trie, filename)

                elif command == '@':
                    filename = input("Enter defect text file: ")
                    restore_best_matches_from_file(self.__trie, filename)

                elif command == '#':
                    for line in self.__trie.display():
                        print(line)
                
                elif command == '!':
                    self.predict_restore_text_menu()

                else:
                    print("Invalid command. Use '!' to see available commands.")

            except KeyboardInterrupt:
                print("\nExiting Predict/Restore Text Command Prompt.")
                break
            except Exception as e:
                print(f"Error: {e}")


    def run(self):
        while True:
            try:
                self.display_main_menu()
                choice = input("Enter choice: ").strip()
                
                if choice == '1':
                    self.construct_edit_trie_menu()
                elif choice == '2':
                    self.predict_restore_text_menu()
                elif choice == '3':
                    self.conf_restorer.trie = self.trie
                    self.conf_restorer.restore_confidence_menu()
                elif choice == '4':
                    self.conf_restorer.trie = self.trie
                    self.freq_editor.manual_freq_menu()
                elif choice == '5':
                    print("Additional Feature 3 - Context Analyzer")
                    integrate_context_analyzer()
                elif choice == '6':
                    print("Additional Feature 4 - Parse Tree Grammar Validation")
                    integrate_trie_visualizer()
                elif choice == '7':
                    print("Thank you for using the Newspaper Restoration Application!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")
                    
            except KeyboardInterrupt:
                print("\nThank you for using the Newspaper Restoration Application!")
                break
            except Exception as e:
                print(f"Error: {e}")