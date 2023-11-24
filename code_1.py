class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.word_list = []  # Storing all words for simplicity

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        self.word_list.append(word)  # Add word to the list

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition

    return d[lenstr1 - 1, lenstr2 - 1]

def load_dictionary(file_path, trie):
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            trie.insert(word)

def suggest_corrections(word, trie, max_distance=2):
    suggestions = []
    for dict_word in trie.word_list:
        if damerau_levenshtein_distance(word, dict_word) <= max_distance:
            suggestions.append(dict_word)
    return suggestions

# Main execution
def main():
    trie = Trie()
    load_dictionary("dictionary.txt", trie)
    
    # Test words
    test_words = ["hellp", "swpa", "coffet"]
    for word in test_words:
        print(f"Suggestions for '{word}': {suggest_corrections(word, trie)}")

if __name__ == "__main__":
    main()
