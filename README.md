# PDF Manipulation and Similarity Script

## Description
This project provides a command-line interface (CLI) for manipulating PDF files and analyzing document similarity. It includes functionalities such as merging, splitting, extracting text, encrypting, decrypting, rotating, adding watermarks, compressing, and managing metadata of PDF files. Additionally, it supports text similarity analysis between documents using various metrics.

## Features
- **PDF Manipulation**:
  - Merge multiple PDF files into one.
  - Split a PDF file into individual pages.
  - Extract text from a PDF file.
  - Encrypt and decrypt PDF files with a password.
  - Rotate pages in a PDF file.
  - Add watermarks to PDF files.
  - Compress PDF files to reduce file size.
  - Add, view, and remove metadata from PDF files.

- **Document Similarity Analysis**:
  - Compute cosine similarity, Jaccard similarity, Levenshtein similarity, and Jaro-Winkler similarity.
  - Visualize similarity scores using bar charts.
  - Load and compare documents from a specified directory.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdf-manipulation-similarity.git
   ```
2. Navigate to the project directory:
   ```bash
   cd pdf-manipulation-similarity
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### PDF Manipulation
Run the main script to access the PDF manipulation functionalities:
```bash
python main.py
```
Follow the on-screen instructions to select the desired operation.

### Document Similarity Analysis
Run the similarity analysis script to compare documents:
```bash
python similarity_project/app.py
```
The script will load documents from the specified directory and compare them against a test document, displaying the similarity scores and visualizations.

## Languages Supported
The application supports the following languages for user interaction:
- English (en)
- French (fr)
- Arabic (ar)

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
