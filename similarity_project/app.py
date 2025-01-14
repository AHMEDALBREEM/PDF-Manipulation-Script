import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import LinAlgError
import PyPDF2  # type: ignore
from scipy.stats import spearmanr, kendalltau
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
wordnet.ensure_loaded()  # Ensure wordnet is loaded properly
from difflib import SequenceMatcher
from pyjarowinkler import distance as jaro_winkler_distance
from scipy.spatial.distance import hamming, jaccard, cosine, euclidean, cityblock, chebyshev, canberra, braycurtis, minkowski, correlation, mahalanobis

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize stop words and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Function to clean and preprocess text
def preprocess_text(text):
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove stop words and lemmatize
    text = ' '.join(lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words)
    return text

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        with open(pdf_file, 'rb') as pdf:
            reader = PyPDF2.PdfReader(pdf)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return preprocess_text(text)
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
        return ""

# Load documents from a directory with parallel processing
def load_documents_from_directory(directory):
    documents = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_text_from_pdf, os.path.join(directory, filename))
                   for filename in os.listdir(directory) if filename.endswith(".pdf")]
        for future in futures:
            result = future.result()
            if result.strip():
                documents.append(result)
    return list(set(documents))  # Removes duplicates

# Load the test document
def load_test_document(filepath):
    return extract_text_from_pdf(filepath)

# Compute various similarities and distances
def compute_similarities_and_distances(documents, user_input, vectorizer):
    # Calculate TF-IDF matrix for documents
    tfidf_matrix = vectorizer.fit_transform(documents)
    input_vector = vectorizer.transform([user_input])

    similarities = []
    distances = {
        "Euclidean": [],
        "Manhattan": [],
        "Minkowski": [],
        "Hamming": [],
        "Bray-Curtis": [],
        "Canberra": [],
        "Chebyshev": [],
        "Correlation": [],
        "Spearman": [],
        "Kendall Tau": [],
        "Mahalanobis": []
    }

    distance_funcs = {
        "Euclidean": lambda u, v: np.linalg.norm(u - v),
        "Manhattan": lambda u, v: np.sum(np.abs(u - v)),
        "Minkowski": lambda u, v: np.sum(np.abs(u - v) ** 3) ** (1 / 3),
        "Hamming": lambda u, v: np.mean(u != v),
        "Bray-Curtis": lambda u, v: np.sum(np.abs(u - v)) / np.sum(np.abs(u + v)),
        "Canberra": lambda u, v: np.sum(np.abs(u - v) / (np.abs(u) + np.abs(v) + 1e-10)),
        "Chebyshev": lambda u, v: np.max(np.abs(u - v)),
        "Correlation": lambda u, v: np.corrcoef(u, v)[0, 1],
        "Spearman": lambda u, v: spearmanr(u, v)[0],
        "Kendall Tau": lambda u, v: kendalltau(u, v)[0],
    }

    for doc in documents:
        if doc == user_input:
            continue  # Ensure we don't compare the document with itself

        # Calculate similarities
        cosine_sim = cosine_similarity(input_vector, vectorizer.transform([doc]))[0][0]
        jaccard_sim = jaccard_similarity(user_input, doc)
        levenshtein_sim = levenshtein_similarity(user_input, doc)
        jaro_winkler_sim = jaro_winkler_similarity(user_input, doc)

        # Combine similarities into a score
        combined_score = 0.3 * cosine_sim + 0.2 * jaccard_sim + 0.2 * levenshtein_sim + 0.3 * jaro_winkler_sim

        # Store results
        similarities.append({
            "document": doc,
            "cosine_similarity": round(cosine_sim, 4),
            "jaccard_similarity": round(jaccard_sim, 4),
            "levenshtein_similarity": round(levenshtein_sim, 4),
            "jaro_winkler_similarity": round(jaro_winkler_sim, 4),
            "combined_score": round(combined_score, 4)
        })

        # Calculate distances
        doc_vector = vectorizer.transform([doc]).toarray().flatten()
        for name, func in distance_funcs.items():
            distances[name].append(func(input_vector.toarray().flatten(), doc_vector))
        if "Mahalanobis" in distances:
            try:
                if tfidf_matrix.shape[0] > 1:
                    cov_matrix = np.cov(tfidf_matrix.toarray(), rowvar=False)
                    if np.linalg.matrix_rank(cov_matrix) == cov_matrix.shape[0]:
                        inv_cov_matrix = np.linalg.inv(cov_matrix)
                        mahalanobis_dist = mahalanobis(input_vector.toarray().flatten(), doc_vector, inv_cov_matrix)
                        distances["Mahalanobis"].append(mahalanobis_dist)
                    else:
                        distances["Mahalanobis"].append(None)
                else:
                    distances["Mahalanobis"].append(None)
            except LinAlgError:
                distances["Mahalanobis"].append(None)

    return similarities, distances

# Jaccard Similarity
def jaccard_similarity(doc1, doc2):
    set1, set2 = set(doc1.split()), set(doc2.split())
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

# Levenshtein Similarity
def levenshtein_similarity(doc1, doc2):
    seq_match = SequenceMatcher(None, doc1, doc2)
    return seq_match.ratio()

# Jaro-Winkler Similarity
def jaro_winkler_similarity(doc1, doc2):
    return jaro_winkler_distance.get_jaro_distance(doc1, doc2, winkler=True)

# Mahalanobis Distance function
def mahalanobis(u, v, inv_cov_matrix):
    diff = u - v
    return np.sqrt(np.dot(np.dot(diff.T, inv_cov_matrix), diff))

def extract_title(text):
    # Extract the first line as the title
    return text.split('\n')[0] if text else "Untitled Document"

def get_preview(doc, max_length=100):
    # Display the first 100 characters of the document
    return doc[:max_length] + ("..." if len(doc) > max_length else "")

def interpret_similarity(score):
    if score > 0.8:
        return "High"
    elif score > 0.5:
        return "Moderate"
    else:
        return "Low"

def print_results():
    documents = load_documents_from_directory(comparison_directory)
    user_input = load_test_document(test_document_path)

    if not documents:
        raise ValueError("No documents found in the specified directory.")

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    similarities, distances = compute_similarities_and_distances(documents, user_input, vectorizer)

    if not similarities:
        print("No similarities found.")
        return
    print("-" * 40)
    total_words = sum([len(result['document'].split()) for result in similarities])
    similarities = sorted(similarities, key=lambda x: x["combined_score"], reverse=True)

    total_combined_score = 0
    total_words = sum([len(result['document'].split()) for result in similarities])
    cosine_similarities = []

    for rank, result in enumerate(similarities, start=1):
        document_words = len(result['document'].split())
        cosine_similarities.append(result['cosine_similarity'])

        title = extract_title(result['document'])
        preview = get_preview(result['document'])

        print(f"Rank {rank}:")
        print(f"Title: {title}")
        print(f"Preview: {preview}")
        print(f"Words: {document_words}")
        print(f"Cosine Similarity: {result['cosine_similarity']} ({interpret_similarity(result['cosine_similarity'])})")
        print(f"Jaccard Similarity: {result['jaccard_similarity']} ({interpret_similarity(result['jaccard_similarity'])})")
        print(f"Levenshtein Similarity: {result['levenshtein_similarity']} ({interpret_similarity(result['levenshtein_similarity'])})")
        print(f"Jaro-Winkler Similarity: {result['jaro_winkler_similarity']} ({interpret_similarity(result['jaro_winkler_similarity'])})")
        print(f"Combined Score: {result['combined_score']} ({interpret_similarity(result['combined_score'])})")

        total_combined_score += result['combined_score']

        for name, values in distances.items():
            if values[rank - 1] is not None:
                print(f"{name} Distance: {round(values[rank - 1], 4)}")
            else:
                print(f"{name} Distance: Not calculated")

        print("-" * 40)

    average_combined_score = total_combined_score / len(similarities) if similarities else 0
    average_cosine_similarity = np.mean(cosine_similarities) if cosine_similarities else 0

    # Feedback
    print("\n--- Feedback ---")
    print("The similarity and distance calculations are complete. Please review the results above.")
    print(f"Average Combined Score: {round(average_combined_score, 4)} ({interpret_similarity(average_combined_score)})")
    print(f"Average Cosine Similarity: {round(average_cosine_similarity, 4)} ({interpret_similarity(average_cosine_similarity)})")
    print(f"Total Words in All Documents: {total_words}")
    print(f"Total Comparisons Made: {len(similarities)}")
    if similarities:
        print(f"Most Similar Document: {extract_title(similarities[0]['document'])}")
        print(f"Least Similar Document: {extract_title(similarities[-1]['document'])}")

    # Explanation of metrics
    print("\n--- Explanation of Metrics ---")
    print("Cosine similarity measures the angle between two vectors, with 1 being identical. A lower value suggests that the documents are less similar in terms of content structure and terminology.")
    print("Jaccard similarity focuses on the intersection of unique terms, and a low value indicates little overlap.")
    print("Levenshtein similarity measures the edit distance between two documents, with a higher value indicating more similarity.")
    print("Jaro-Winkler similarity is a variant of Levenshtein similarity that gives more weight to matching characters at the beginning of the strings.")
    print("Topic modeling identifies themes within documents, which could help align documents with different structures but similar topics. Word embeddings map words into a vector space, allowing similar meanings to be recognized even if the exact words don't match.")

    # Visual Representation
    documents = [extract_title(result['document']) for result in similarities]
    cosine = [result['cosine_similarity'] for result in similarities]
    jaccard = [result['jaccard_similarity'] for result in similarities]
    levenshtein = [result['levenshtein_similarity'] for result in similarities]
    jaro_winkler = [result['jaro_winkler_similarity'] for result in similarities]
    combined = [result['combined_score'] for result in similarities]

    plt.figure(figsize=(14, 10))
    bar_width = 0.15
    index = np.arange(len(documents))

    sns.set_palette("colorblind")
    plt.bar(index, cosine, bar_width, label="Cosine Similarity", alpha=0.7)
    plt.bar(index + bar_width, jaccard, bar_width, label="Jaccard Similarity", alpha=0.5)
    plt.bar(index + 2 * bar_width, levenshtein, bar_width, label="Levenshtein Similarity", alpha=0.3)
    plt.bar(index + 3 * bar_width, jaro_winkler, bar_width, label="Jaro-Winkler Similarity", alpha=0.3)
    plt.bar(index + 4 * bar_width, combined, bar_width, label="Combined Score", alpha=0.3)

    plt.xlabel('Compared Documents')
    plt.ylabel('Similarity Score (0-1)')
    plt.title('Similarity Comparison between Documents')
    plt.xticks(index + 2 * bar_width, documents, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    # Add exact score labels on top of each bar
    for i in range(len(documents)):
        plt.text(i, cosine[i] + 0.01, f'{cosine[i]:.2f}', ha='center', va='bottom')
        plt.text(i + bar_width, jaccard[i] + 0.01, f'{jaccard[i]:.2f}', ha='center', va='bottom')
        plt.text(i + 2 * bar_width, levenshtein[i] + 0.01, f'{levenshtein[i]:.2f}', ha='center', va='bottom')
        plt.text(i + 3 * bar_width, jaro_winkler[i] + 0.01, f'{jaro_winkler[i]:.2f}', ha='center', va='bottom')
        plt.text(i + 4 * bar_width, combined[i] + 0.01, f'{combined[i]:.2f}', ha='center', va='bottom')

    plt.show()

test_document_path = "C:/Users/asdal/Downloads/pdf/similarity_project/a.pdf"
comparison_directory = "C:/Users/asdal/Downloads/pdf/similarity_project/pdf_directory"


# Display the results
print_results()
