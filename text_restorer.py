from trie import match_case_pattern

def restore_all_matches_from_file(trie, filename):
    """
    Reads a file with wildcard words, finds all possible matches in the trie,
    and prints each line with the lists of matches.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().split()
                restored_words = []
                for w in words:
                    if '*' in w:
                        matches = trie.wildcard_search(w.lower())
                        # Format matches while preserving original case
                        matched_words = [match_case_pattern(w, m[0]) for m in matches]
                        restored_words.append(str(matched_words))
                    else:
                        restored_words.append(w)
                print(' '.join(restored_words))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def restore_best_matches_from_file(trie, filename):
    """
    Reads a file with wildcard words, finds the best match for each in the trie,
    and prints each line with the restored words.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().split()
                restored_words = []
                for w in words:
                    if '*' in w:
                        best_match = trie.best_match(w.lower())
                        if best_match:
                            # Format the best match and preserve case
                            restored_word = f"<{match_case_pattern(w, best_match[0])}>"
                            restored_words.append(restored_word)
                        else:
                            restored_words.append(w)  # No match found
                    else:
                        restored_words.append(w)
                print(' '.join(restored_words))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")