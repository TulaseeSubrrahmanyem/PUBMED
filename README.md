 
# PubMed Research Paper Fetcher
 
## Overview
 
This project allows users to fetch research papers from PubMed based on a search query, extract relevant details like authors, publication date, affiliations, and corresponding author emails, and save the results in a CSV file. It provides a command-line interface for executing searches with flexibility and support for PubMed's full query syntax.
 
## Installation Instructions
 
### 1. Install Poetry
 
To manage dependencies, this project uses [Poetry](https://python-poetry.org/). If you don’t have it installed, run the following command:
 
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
 
Alternatively, you can install it using `pip`:
 
```bash
pip install poetry
```
 
### 2. Clone the Repository
 
Clone this repository to your local machine:
 
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
 
### 3. Install Dependencies
 
Run the following command to install all dependencies defined in `pyproject.toml`:
 
```bash
poetry install
```
 
This will create a virtual environment and install all the required dependencies.
 
### 4. Running the Program
 
Once the dependencies are installed, you can run the program using the following command:
 
```bash
poetry run get-papers-list "your_search_query"
```
 
- Replace `"your_search_query"` with your desired PubMed search query.
- You can also provide options:
  - `-d` or `--debug`: Print debug information during execution.
  - `-f` or `--file`: Specify the filename to save the results in CSV format (e.g., `results.csv`).
 
For example, to search for "cancer research" and save the results to a file:
 
```bash
poetry run get-papers-list "cancer research" -f "cancer_research_results.csv"
```
 
## Command-Line Arguments
 
- `-h` or `--help`: Display usage instructions.
- `-d` or `--debug`: Print debug information during execution.
- `-f` or `--file`: Specify the filename to save the results (CSV). If not provided, the output will be printed to the console.
 
## Output Format
 
The program returns a CSV file with the following columns:
- **PubmedID**: Unique identifier for the paper.
- **Title**: Title of the paper.
- **Publication Date**: Date the paper was published.
- **Non-academic Author(s)**: Names of authors affiliated with non-academic institutions.
- **Company Affiliation(s)**: Names of pharmaceutical/biotech companies.
- **Corresponding Author Email**: Email address of the corresponding author.
 
## Contributing
 
Feel free to fork the repository, make changes, and submit pull requests. Please ensure that the code follows the existing style and includes appropriate comments and documentation.
 
## License
 
This project is licensed under the MIT License - see the LICENSE file for details.
 
---
 
### Key Details Covered:
1. **How the code is organized**: Explains the file structure, including the role of each file (`main.py`, `pyproject.toml`).
2. **Installation Instructions**: Steps for installing Poetry and setting up the project using `poetry install`.
3. **Running the Program**: Instructions on how to run the program and the available command-line arguments.
4. **Output Format**: Describes the CSV file format that the program generates.
5. **Command-Line Arguments**: Explains the options available for users (`-h`, `-d`, `-f`).
6. **Tools and Libraries**: Lists the tools and libraries used with relevant links to their documentation.
7. **Contributing**: Encourages collaboration by forking and submitting pull requests.
8. **License**: Specifies that the project uses the MIT License.
 
 