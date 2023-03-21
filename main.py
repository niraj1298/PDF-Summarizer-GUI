"""
----------------------------------------
[|]=================================[|]
[|]PDF Summarizer GUI IMPLEMENTATION[|]
[|]=================================[|]
----------------------------------------

Developed by: Niraj Nepal
Functionality: This script allows the user to summarize PDF files using OpenAI's GPT-3.

References:
https://pypdf2.readthedocs.io/en/latest/user/extract-text.html ,
https://platform.openai.com/docs/api-reference/models/retrieve?lang=python ,
https://analyzingalpha.com/openai-api-python-tutorial
https://realpython.com/python-gui-tkinter/
https://www.pythontutorial.net/tkinter/

"""

import openai
import PyPDF2
import tkinter as tk
from tkinter import filedialog

openai.api_key = "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"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

# Function to split the text into chunks
def chunk_text(text, chunk_size=2048):
    """
    Splits text into chunks of a specified size.

    Args:
        text (str): The text to be chunked.
        chunk_size (int): Maximum size of a chunk. Default is 2048.

    Returns:
        list: List of chunks.
    """
    tokens = text.split()
    chunks = []
    current_chunk = []

    for token in tokens:
        if len(current_chunk) + len(token) + 1 > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
        current_chunk.append(token)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Function to summarize text using GPT-3
def summarize_text(text, model="text-davinci-002", tokens=300):
    """
    Summarizes text using GPT-3.

    Args:
        text (str): The text to be summarized.
        model (str): GPT-3 model to be used for summarization. Default is "text-davinci-002".
        tokens (int): Maximum number of tokens in the summary. Default is 300.

    Returns:
        str: Generated summary.
    """
    response = openai.Completion.create(
        engine=model,
        prompt=f"Please summarize the following text, give me detailed points and ideas:\n\n{text}\n",
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary

# Modified function to summarize text using GPT-3 in chunks
def summarize_text_chunks(text, model="text-davinci-002", tokens=300):
    """
    Summarizes text using GPT-3 in chunks.

    Args:
        text (str): The text to be summarized.
        model (str): GPT-3 model to be used for summarization. Default is "text-davinci-002".
        tokens (int): Maximum number of tokens in the summary. Default is 300.

    Returns:
        str: Generated summary.
    """
    chunks = chunk_text(text)
    summarized_chunks = []

    for chunk in chunks:
        summary = summarize_text(chunk, model=model, tokens=tokens)
        summarized_chunks.append(summary)

    return ' '.join(summarized_chunks)

# Function to save the summary to a text file
def save_summary_to_file(summary, output_file):
    """
    Saves the summary to a text file.

    Args:
        summary (str): The summary to be saved.
        output_file (str): Path to the output text file.
    """
    with open(output_file, 'w') as file:
        file.write(summary)

# Main function
def main(pdf_path, output_to_file=True):
    """
    Main function to extract text from the input PDF, summarize it, and save the summary
    to a text file or display it in the summary_text widget.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_to_file (bool): Whether to save the summary to a text file or not. Default is True.
    """
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text_chunks(text)
    if output_to_file:
        save_summary_to_file(summary, output_file)
    return summary

# Function to start summarizing and display the summary in the text box
def summarize_pdf():
    """
    Summarizes the input PDF and displays the summary in the summary_text widget.
    """
    summary = main(root.pdf_path, output_to_file=False)
    summary_text.config(state='normal')
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, summary)
    summary_text.config(state='disabled')

####################################
# Create the main window
root = tk.Tk()
root.title("PDF Summarizer")

# Default window size
root.geometry("1000x800")
root.configure(bg='#2f3852')

# Create a text box to display the summary
summary_text = tk.Text(
    root,
    bg='white',
    fg='#2f3852',
    highlightthickness=6,
    highlightbackground='#000000',
    wrap=tk.WORD)
summary_text.pack(expand=True, fill=tk.BOTH)
summary_text.insert(tk.END, "Your summary will load here.")
summary_text.config(state='disabled')

# Function to select the input PDF file
def select_pdf_file():
    """
    Opens a file dialog to select the input PDF file.
    """
    root.pdf_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )

# Create a button to select the input PDF file
select_button = tk.Button(
    root,
    activebackground='#5fb878',
    activeforeground='black',
    borderwidth=3,
    bg='#5fb878',
    fg='#f7efef',
    text="Select PDF File",
    command=select_pdf_file)
select_button.pack(padx=8, pady=8)

# Create a button to start summarizing
summarize_button = tk.Button(
    root,
    activebackground='#5fb878',
    activeforeground='black',
    borderwidth=3,
    bg='#5fb878',
    fg='#f7efef',
    text="Summarize PDF",
    command=summarize_pdf)
summarize_button.pack(padx=8, pady=8)

# Function to clear the summary
def clear_summary():
    """
    Clears the summary displayed in the summary_text widget.
    """
    summary_text.config(state='normal')
    summary_text.delete(1.0, tk.END)
    summary_text.config(state='disabled')

def generate_new_response():
    """
    Generates a new summary response.
    """
    summarize_pdf()

clear_button = tk.Button(
    root,
    activebackground='#5fb878',
    activeforeground='black',
    borderwidth=3,
    bg='#5fb878',
    fg='#f7efef',
    text="Clear Summary",
    command=clear_summary)
clear_button.pack(padx=8, pady=8)

# Create a button for the "Generate New Response" functionality
new_response_button = tk.Button(
    root,
    activebackground='#5fb878',
    activeforeground='black',
    borderwidth=3,
    bg='#5fb878',
    fg='#f7efef',
    text="Generate New Response",
    command=generate_new_response)
new_response_button.pack(padx=8, pady=8)

# Function to save the summary from the text box to a file
def save_summary_from_text_box():
    """
    Saves the summary displayed in the summary_text widget to a text file.
    """
    output_file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if output_file:
        summary = summary_text.get(1.0, tk.END)
        save_summary_to_file(summary, output_file)

# Create a button to save the summary to a file
save_button = tk.Button(
    root,
    activebackground='#5fb878',
    activeforeground='black',
    borderwidth=3,
    bg='#5fb878',
    fg='#f7efef',
    text="Save Summary",
    command=save_summary_from_text_box)
save_button.pack(padx=8, pady=8)

# Start the GUI event loop
root.mainloop()
