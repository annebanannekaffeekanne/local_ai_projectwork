# import necessary libraries and methods form files
import os
import fitz
from preprocessing import preprocess_texts, chunk_texts
import logging

## _____________________________________________________________________________________________________________
# extract text from pdf files
def extract_text_from_pdf(path):
    try:
        # open file
        with fitz.open(path) as doc:
            # extract text from each page and connect it to one big textblock
            return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        # when there's an error reading/opening the file return None and print error
        print(f"PDF error {path}: {e}")
        return None

# ------------------------------------------------------------------------
# read the text of a markdown file
def extract_text_from_md(path):
    try:
        # opens file with reading mode and UTF-8-Encoding
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        # return error if there's one
        print(f"MD error {path}: {e}")
        return None

## _____________________________________________________________________________________________________________
# scan directory for pdf and md files
def scan_directory(base_path):
    supported = [".pdf", ".md"]
    # save list of documents found
    docs = []
    # recursive iteration over all directories and files below the base directory
    for root, _, files in os.walk(base_path):
        logging.info(f"Scanning directory: {root}")
        logging.info(f"Found files: {files}")
        for file in files:
            # extract file ending (.pdf,..)
            ext = os.path.splitext(file)[1].lower()
            if ext in supported:
                # build absolute path to the file
                full_path = os.path.join(root, file)
                # depending on file type extract text with the fitting function
                content = extract_text_from_pdf(full_path) if ext == ".pdf" else extract_text_from_md(full_path)
                if content:
                    preprocessed_content = preprocess_texts(content)
                    chunks = chunk_texts(preprocessed_content)

                    last_modified = os.path.getmtime(full_path)
                    # if text's been extracted
                    docs.append({
                        # save path to file
                        "path": full_path,
                        # save extracted text
                        "content": " ".join(chunks),
                        "last_modified": last_modified
                    })
    # return list of all docs that've been found and read
    return docs

## _____________________________________________________________________________________________________________
# check if working
if __name__ == '__main__':
    BASE_PATH = os.environ.get("DOC_BASE_PATH", "/Users/anne/Documents")
    docs = scan_directory(BASE_PATH)
    print(len(docs))
