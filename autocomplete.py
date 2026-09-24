import csv
import re

def main():
    # 1. Load the data
    print("Loading dataset...")
    sentences = load_data('sentences.csv')
    print(f"Successfully loaded {len(sentences)} sentences.\n")
    
    # 2. Train the model
    print("Training N-gram model with Backoff smoothing...\n")
    model, fallback_words = build_model(sentences)
    
    # 3. Interactive prediction engine
    print("--- Darija Autocomplete Engine ---")
    print("Type 'quit' to exit.")
    
    while True:
        test_word = input("\nType a word: ").strip()
        
        if test_word.lower() == 'quit':
            print("Exiting...")
            break
            
        predict_next_word(model, fallback_words, test_word)

def load_data(filename):
    sentences = []
    # Using utf-8 prevents the mojibake error in Excel
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None) # Skips the header row just in case
        for row in reader:
            if row: # Ensures the row isn't completely empty
                # Grab Column A (index 0) which contains the Arabizi text
                sentences.append(row[0])
    return sentences

def tokenize(text):
    #lowercase and extract only valid words
    return re.findall(r'\b\w+\b', text.lower())

# (Keep load_data and tokenize exactly as they are)

def build_model(sentences):
    model = {}
    unigram_counts = {} # NEW: Dictionary to track every single word's overall frequency
    
    for sentence in sentences:
        tokens = tokenize(sentence)
        
        for i in range(len(tokens) - 1):
            current_word = tokens[i]
            next_word = tokens[i+1]
            
            # Count individual words for our fallback mechanism
            unigram_counts[current_word] = unigram_counts.get(current_word, 0) + 1
            
            # Build the Bigram model (your existing logic)
            if current_word not in model:
                model[current_word] = {}
            model[current_word][next_word] = model[current_word].get(next_word, 0) + 1
            
    # Mathematically find the top 3 most common words in the entire dataset
    sorted_unigrams = sorted(unigram_counts.items(), key=lambda item: item[1], reverse=True)
    fallback_words = [word for word, count in sorted_unigrams[:3]]
    
    return model, fallback_words

def predict_next_word(model, fallback_words, word):
    word = word.lower()
    
    if word in model:
        # Known word: Calculate bigram probabilities
        predictions = model[word]
        sorted_predictions = sorted(predictions.items(), key=lambda item: item[1], reverse=True)
        top_3 = sorted_predictions[:3]
        
        print(f"Top suggestions for '{word}':")
        for predicted_word, count in top_3:
            print(f" -> {predicted_word} (seen {count} times)")
    else:
        # Unknown word: Backoff to unigrams
        print(f"Word '{word}' not recognized. Backing off to overall most common words:")
        for fallback in fallback_words:
            print(f" -> {fallback} (fallback suggestion)")

if __name__ == "__main__":
    main()