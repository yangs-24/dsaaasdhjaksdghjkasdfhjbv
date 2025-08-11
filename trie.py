class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_terminal = False
        self.frequency = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add(self, word, freq=1):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_terminal = True
        node.frequency += freq

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_terminal

    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if node.is_terminal:
                    node.is_terminal = False
                    node.frequency = 0
                    return len(node.children) == 0
                else:
                    return False
            char = word[depth]
            if char in node.children:
                can_delete = _delete(node.children[char], word, depth + 1)
                if can_delete:
                    del node.children[char]
                    return not node.is_terminal and len(node.children) == 0
            return False
        return _delete(self.root, word, 0)

    def display(self):
        """
        Display the trie structure in a readable format.
        Shows the hierarchical structure with terminal nodes marked.
        """
        if not self.root.children:
            print("[]")
            return

        def _display_node(node, prefix, is_last):
            """
            Recursively displays the trie nodes.
            """
            word_display = ""
            if node.is_terminal:
                word_display = f"* (Frequency: {node.frequency})"

            # Determine the correct prefix for the current node
            connector = "└── " if is_last else "├── "
            if prefix:
                # For nodes other than the root's direct children
                print(prefix + connector + word_display)
            else:
                # For the root's direct children
                print(connector + word_display)

            children = list(node.children.items())
            for i, (char, child_node) in enumerate(children):
                new_prefix = prefix + ("    " if is_last else "│   ")
                # Create a more descriptive display for the children
                child_display_prefix = new_prefix + ("└── " if i == len(children) - 1 else "├── ")
                
                if child_node.is_terminal:
                    print(f"{child_display_prefix}{char}* (Frequency: {child_node.frequency})")
                else:
                    print(f"{child_display_prefix}{char}")
                
                # Recurse to the children of the current child node
                if child_node.children:
                    _display_node(child_node, new_prefix + ("    " if i == len(children) - 1 else "│   "), i == len(children)-1)


        print("Trie Structure:")
        # Start the display from the children of the root
        children = list(self.root.children.items())
        for i, (char, child_node) in enumerate(children):
            is_last_child = i == len(children) - 1
            
            # Display the first level of characters
            connector = "└── " if is_last_child else "├── "
            if child_node.is_terminal:
                print(f"{connector}{char}* (Frequency: {child_node.frequency})")
            else:
                print(f"{connector}{char}")
            
            # Now, display the rest of the trie from this node
            _display_node(child_node, "    " if is_last_child else "│   ", is_last_child)

    def to_list(self):
        def _collect(node, prefix):
            words = []
            if node.is_terminal:
                words.append((prefix, node.frequency))
            for char, child in node.children.items():
                words.extend(_collect(child, prefix + char))
            return words
        return _collect(self.root, '')

    def from_list(self, word_list):
        self.root = TrieNode()
        for word, freq in word_list:
            self.add(word, freq)

    def wildcard_search(self, pattern):
        results = []

        def dfs(node, i, path):
            if i == len(pattern):
                if node.is_terminal:
                    results.append((path, node.frequency))
                return
            if pattern[i] == '*':
                for char, child in node.children.items():
                    dfs(child, i + 1, path + char)
            elif pattern[i] in node.children:
                dfs(node.children[pattern[i]], i + 1, path + pattern[i])
        dfs(self.root, 0, '')
        results.sort(key=lambda x: -x[1])  # sort by frequency descending
        return results

    def best_match(self, pattern):
        matches = self.wildcard_search(pattern)
        return matches[0] if matches else None
    
    def read_file_keywords(self, filename):
        """
        Read keywords from a file and build the trie.
        File format: word,frequency (one per line)
        Clears existing trie before loading new data.
        """
        try:
            self.root = TrieNode()
            self.size = 0
            
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        if ',' in line:
                            parts = line.split(',')
                            word = parts[0].strip()
                            frequency = int(parts[1].strip()) if len(parts) > 1 else 1
                        else:
                            word = line
                            frequency = 1
                            
                        if word:
                            self.add(word, frequency)
                            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error reading file: {e}")
            
    def write_keywords_to_file(self, filename):
        """
        Write all keywords and their frequencies to a file.
        File format: word,frequency (one per line)
        """
        try:
            words = self.get_all_words()
            with open(filename, 'w', encoding='utf-8') as file:
                for word, frequency in words:
                    file.write(f"{word},{frequency}\n")
                    
        except Exception as e:
            print(f"Error writing file: {e}")
            
    def write_trie_to_file(self, filename):
        """
        Write the trie structure to a file in a readable format.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                if self.size == 0:
                    file.write("[]\n")
                    return
                    
                def _write_node(node, prefix="", is_last=True):
                    if node.is_terminal:
                        file.write(f"{prefix}{'└── ' if is_last else '├── '}{node.word}* ({node.frequency})\n")
                    
                    children = list(node.children.items())
                    for i, (char, child_node) in enumerate(children):
                        is_last_child = i == len(children) - 1
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        
                        if child_node.is_terminal:
                            _write_node(child_node, next_prefix, is_last_child)
                        else:
                            file.write(f"{next_prefix}{'└── ' if is_last_child else '├── '}{char}\n")
                            _write_node(child_node, next_prefix + ("    " if is_last_child else "│   "), True)
                            
                file.write("Trie Structure:\n")
                _write_node(self.root)
                file.write(f"\nTotal words: {self.size}\n")
        except Exception as e:
            print(f"Error writing trie to file: {e}")


def match_case_pattern(original, matched):
    # Applies the capitalization pattern of `original` to `matched`
    result = []
    for o_char, m_char in zip(original, matched):
        if o_char.isupper():
            result.append(m_char.upper())
        else:
            result.append(m_char.lower())
    # Append any remaining characters in matched (lowercase)
    result.extend(matched[len(original):])
    return ''.join(result)
