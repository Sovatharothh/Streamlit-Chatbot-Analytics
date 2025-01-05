# AUPPSearch

AUPPSearch is an interactive Streamlit-based web application designed to provide intuitive data exploration capabilities. Using OpenAI's Google Gemini model and pandasAI, it enables users to upload datasets and interact with them through natural language queries.

## Features

- Upload and preview datasets in CSV, Excel, or JSON formats.
- Process and analyze datasets using natural language prompts.
- Generate interactive visualizations and insights with ease.
- Fast and efficient file processing with support for large datasets.

## Requirements

- Python 3.8 or higher
- Streamlit
- pandas
- matplotlib
- openai
- pandasAI
- dotenv
- Excel file handling with `openpyxl`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Sovatharothh/Streamlit-Chatbot-Analytics.git
   cd Streamlit-Chatbot-Analytics
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the application:

   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the app in your browser (usually at `http://localhost:8501`).
2. Upload a dataset in CSV, Excel, or JSON format using the file uploader.
3. Preview the dataset and interact with it using the chat input box.
4. Ask questions or request insights about the data, and receive responses powered by Google Gemini and pandasAI.

## File Format Support

- **CSV**: Comma-separated values files (.csv)
- **Excel**: Excel workbooks (.xlsx)
- **JSON**: JavaScript Object Notation files (.json)

## Example Prompts

- "What are the top 5 rows of the dataset?"
- "Show me a plot of top 5 students by courses."
- "What is the average value of the column `GPA`?"

## Known Issues

- Errors may occur if the uploaded dataset contains unsupported formats or corrupted data.
- Long processing times for very large datasets.


## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web application framework.
- [OpenAI](https://ai.google.dev/gemini-api/docs/models/gemini) for the Google Gemini model.
- [pandasAI](https://pandas-ai.com/) for the intelligent dataframe integration.
- [matplotlib](https://matplotlib.org/) for visualizations.

