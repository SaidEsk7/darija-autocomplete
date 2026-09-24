# Darija Autocomplete - Bigram Language Model
 
A word-prediction tool for Moroccan Darija, built  in Python. Given a word, it predicts the most likely next word using a bigram statistical language model I didn't use any NLP libraries, just the standard library.
 
## Background
 
This started as a follow-up to my CS50P final project, a lexical analyzer that tokenized text and counted word frequencies. This project takes that same idea further: instead of just counting words, it models which words tend to follow which, and uses that to predict what comes next.
 
Darija (Moroccan dialect which is a mixture of languages that includes Arabic, Amazigh , French , Spanish and Portuguese)  is a good test case for this kind of project because it doesn't have standardized spelling and is usually written in a mix of Latin script and numerals (Arabizi) rather than Arabic script. That makes it messier to work with than English, but also more realistic as an NLP problem.
 
## How it works
 
- **Data**: Sentences come from [DODa]([https://github.com](https://github.com/darija-open-dataset/dataset)) (Darija Open Dataset), using the Arabizi (Latin-script) column.
- **Tokenization**: Text is lowercased and split into words using regex, stripping punctuation.
- **Model**: The script counts how often each word follows each other word (bigrams) and how often each word appears overall (unigrams). Predicting the next word means looking up which words followed the input word most often in the data, and returning the top 3.
- **Fallback**: If the input word never appeared in the training data, the model falls back to the most common words overall, so it always returns something instead of failing.
This is a Maximum Likelihood Estimation (MLE) bigram model  the standard first approach to statistical language modeling, predating and much simpler than neural approaches. It has real limitations: it only looks one word back, and it can't handle input it's never seen.

## Limitations
 
- Only considers the immediately preceding word (no longer context)
- Prediction quality depends entirely on how much relevant data is in `sentences.csv`
 
## Usage
 
```bash
python autocomplete.py
```
 
Enter a Darija word (e.g. `wach`, `salam`, `khouya`) and the script prints the three most likely next words based on the training data.
 

## Sample Output

```text
Loading dataset...
Successfully loaded 48839 sentences.

Training N-gram model with Backoff smoothing...

--- Darija Autocomplete Engine ---
Type a word: khouya
Top suggestions for 'khouya':
 -> sghir (seen 2 times)
 -> labas (seen 1 times)

Type a word: wach
Top suggestions for 'wach':
 -> nta (seen 14 times)
 -> mcha (seen 8 times)
 -> kayna (seen 5 times)
 
