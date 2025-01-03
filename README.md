# Newsletter Summarizer
Python script that fetches newsletter emails through Gmail API 
and summarizes them weekly through Groq, Langchain and Mixtral AI. 

This idea came after thinking of an aspect to automate in my life, and thus I 
came up with this program using AI to summarize the many newsletters that I receive.

## Features

- Fetch Newsletters Sent to Your Gmail
- AI Summarization of Newsletters

## Getting Started
To get a local copy up and running for development or testing, follow the steps below.

### Prerequisites
To run this application, you need to have at least Python 3.12 installed on your computer. You can download Python from [python.org](https://www.python.org/downloads/).

You also need to install the required packages. You can do this by:
```shell
pip install -r requirements.txt
```

### Installation
1. **Clone the repository:**
```shell
git clone https://github.com/nfalck/NewsletterSummarizer.git
cd NewsletterSummarizer
```

2. **Create and activate virtual environment:**
```shell
python3 -m venv venv
source venv/bin/activate
```
3. **Set up environment variables:**

    Create a .env file and add your Groq API key (create an account at Groq and create an API key)

```
GROQ_API_KEY=your_api_key
```

4. **Create Gmail API Credentials:**

    Follow this [Quickstart by Google](https://developers.google.com/gmail/api/quickstart/python) to:
    - create a Google Cloud project
    - enable Gmail API on the project
    - configure OAuth consent screen and add yourself as a testing user
    - create OAuth client ID to save as **credentials.json**


5. **Set up the newsletter emails:**
   - Go to main.py and fill in the emails list with strings of the email addresses you wish to fetch messages from


6. **Run the code:**
   ```shell
   python3 main.py
   ```
   Keep in mind that the files token.json, collectedemails.txt and summary.txt will be created.
   
**Additional important information:**

At first run, the program with your Gmail API will ask you to grant access to your Gmail account. 
Through this you will get a token.json which expires in 7 days if your Google Cloud project is under "testing" status.
After 7 days, it will ask for access again. 
The duration of the token can apparently be increased by publishing your project to be in "in production" 
status, however keep in mind, that others could have access to the project, so be careful to keep your OAuth credentials safe. 

7. **Schedule the main.py script:**

   Schedule the main.py script through crontab or a task scheduler.

## Future Improvements

- Instead of clustered summaries added together, use Map-Reduce method instead to make a final summary of all the summaries
- Make a nicely formatted PDF of the summary or email the text content

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
