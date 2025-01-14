# Document Similarity Analysis

## Description
This module provides functionality for analyzing the similarity between documents using various text similarity metrics. It includes preprocessing of text, extraction of text from PDFs, and computation of similarity scores such as cosine similarity, Jaccard similarity, Levenshtein similarity, and Jaro-Winkler similarity. The results are visualized using bar charts for easy interpretation.

## Features
- **Text Preprocessing**: Clean and preprocess text by removing HTML tags, special characters, and stop words, and by lemmatizing words.
- **Text Extraction**: Extract text from PDF files for analysis.
- **Similarity Metrics**:
  - **Cosine Similarity**: Measures the angle between two vectors, with 1 being identical.
  - **Jaccard Similarity**: Focuses on the intersection of unique terms.
  - **Levenshtein Similarity**: Measures the edit distance between two documents.
  - **Jaro-Winkler Similarity**: A variant of Levenshtein similarity that gives more weight to matching characters at the beginning of the strings.
- **Visualization**: Generate bar charts to visualize similarity scores between documents.

## Installation
1. Ensure you have the required dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
2. The module is part of the main project and can be accessed by running the `app.py` script.

## Usage
To run the document similarity analysis, execute the following command:
```bash
python similarity_project/app.py
```
The script will load documents from the specified directory and compare them against a test document, displaying the similarity scores and visualizations.

## Example
```bash
python similarity_project/app.py
```
This will load documents from the `pdf_directory` and compare them against the test document `a.pdf`, displaying the similarity scores and generating a bar chart.

## Visualizations
The application generates bar charts to visualize the similarity scores between documents. The charts include the following metrics:
- Content Vector Similarity (Cosine)
- Overlap-Based Similarity (Jaccard)
- Text Edit Similarity (Levenshtein)
- String Proximity Similarity (Jaro-Winkler)
- Overall Similarity Score (Combined)

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
