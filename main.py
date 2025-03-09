import pandas as pd #for dataset manupulation
from Bio import Entrez #for pubmed
import requests #for get, post etc requests
import xml.etree.ElementTree as ET  #for parsing and displaying the response in XML format
import argparse # to make the cmd line arguments
from typing import List, Dict # for type hints
import re # regular expressions to extract the text patterns

# Function to fetch research papers from PubMed using the Entrez API (using efetch for more details)
def fetch_papers(query: str, max_results: int = 100) -> List[Dict]:
    Entrez.email ='saiindupuri.25@gmail.com'  # Always use a valid email address
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    ids = record["IdList"]
    
    # Fetch detailed records using the PubMed IDs (using efetch for more details)
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    url = f'{base_url}?db=pubmed&id={",".join(ids)}&rettype=xml&retmode=text'
    
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse the XML response
    records = ET.fromstring(response.text)
    papers = []
    
    for record in records.findall('.//PubmedArticle'):
        # Safely extract publication date
        pub_date_elem = record.find('.//PubDate')
        if pub_date_elem is not None:
            year = pub_date_elem.find('Year')
            month = pub_date_elem.find('Month')
            day = pub_date_elem.find('Day')
            publication_date = f"{year.text}-{month.text}-{day.text}" if year is not None and month is not None and day is not None else year.text
        else:
            publication_date = "Unknown"
        
        # Safely extract authors
        authors = []
        for author in record.findall('.//Author'):
            last_name = author.find('LastName')
            first_name = author.find('ForeName')
            if last_name is not None and first_name is not None:
                authors.append(f"{last_name.text}, {first_name.text}")
            else:
                authors.append("Unknown Author")
        
        # Initialize corresponding_email as 'N/A'
        corresponding_email = "N/A"
        
        # Extract emails from the corresponding author or via regex
        email_elem = record.find('.//CorrespondingAuthor/Email')
        if email_elem is not None:
            corresponding_email = email_elem.text
        else:
            # If no email is found, attempt regex on the affiliation field
            affiliation_text = " ".join([affiliation.text for affiliation in record.findall('.//Affiliation')])
            
            # Debugging output to check affiliation texts
            print("Affiliation Text:", affiliation_text)
            
            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            corresponding_email_matches = re.findall(email_pattern, affiliation_text)
            if corresponding_email_matches:
                corresponding_email = corresponding_email_matches[0]  # Take the first email found
        
        paper = {
            "PubmedID": record.find('.//PMID').text,
            "Title": record.find('.//ArticleTitle').text,
            "Publication Date": publication_date,
            "Authors": authors,
            "Affiliations": [affiliation.text for affiliation in record.findall('.//Affiliation')],
            "Corresponding Author Email": corresponding_email  # This key is guaranteed to exist now
        }
        
        papers.append(paper)
    
    return papers

# Function to filter non-academic authors and pharma/biotech affiliations
def filter_papers(papers: List[Dict]) -> List[Dict]:
    filtered_papers = []
    
    # Pharmaceutical or Biotech company keywords (this can be expanded)
    company_keywords = ["pharma", "biotech", "biotechnology", "corporation", "biopharma", "drug"]
    
    for paper in papers:
        non_academic_authors = []
        company_affiliations = []
        
        # Check authors' affiliations
        for affiliation in paper["Affiliations"]:
            for keyword in company_keywords:
                if keyword.lower() in affiliation.lower():
                    company_affiliations.append(affiliation)
        
        # Check if there are authors affiliated with non-academic institutions
        if company_affiliations:
            for author in paper["Authors"]:
                non_academic_authors.append(author)
            
            filtered_papers.append({
                "PubmedID": paper["PubmedID"],
                "Title": paper["Title"],
                "Publication Date": paper["Publication Date"],
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": paper["Corresponding Author Email"]
            })
    
    return filtered_papers

# Function to save results as CSV
def save_to_csv(papers: List[Dict], filename: str):
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

# Command-line argument parsing
def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information.")
    parser.add_argument("-f", "--file", help="Filename to save results (CSV).")
    
    args = parser.parse_args()
    
    # Fetch papers
    if args.debug:
        print("Fetching papers from PubMed...")
    
    papers = fetch_papers(args.query)
    
    if args.debug:
        print(f"Fetched {len(papers)} papers.")
    
    # Filter papers based on affiliations
    filtered_papers = filter_papers(papers)
    
    if args.debug:
        print(f"Filtered {len(filtered_papers)} papers.")
    
    # Save results
    if args.file:
        save_to_csv(filtered_papers, args.file)
    else:
        for paper in filtered_papers:
            print(paper)

if __name__ == "__main__":
    main()
