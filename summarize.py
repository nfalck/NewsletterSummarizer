from langchain_text_splitters import CharacterTextSplitter
from groq import Groq
import os
import time
from dotenv import load_dotenv
load_dotenv()

def split_text():
    """Split the text into chunks that fix the max tokens per minute with langchain and tiktoken"""

    # read the emails that were collected from gmail
    with open('collectedemails.txt', 'r') as file:
        emails = file.read()
        file.close()

    # split the text into chunks of size 2500
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=2500, chunk_overlap=0
    )
    return text_splitter.split_text(emails)

# authenticate Groq with the API key
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Pre-defined prompts
system_prompt = ("You are a skilled newsletter summarizer designed to distill the most "
                 "valuable insights, ideas, and action points from newsletters. Your goal is to save time by extracting only the "
                 "most impactful and relevant information.")

user_prompt = ("Summarize the content from these newsletters. Focus on actionable insights, inspiring ideas, key takeaways, and any "
               "recommended resources or tools. Be concise and engaging.")

def ai_summarize(texts):
    """Iterating through each chunk and using Groq with Mixtral to summarize each chunk
    and appending the summary into summary.txt"""

    # clear the summary.txt to remove old summaries
    open('summary.txt', 'w').close()

    # iteration of every text chunk
    with open('summary.txt', 'a') as file:
        for text in texts:
            print("new text chunk") # for logging/testing purposes
            new_user_prompt = user_prompt + " " + text # include the text in the prompt
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },

                    {
                        "role": "user",
                        "content": new_user_prompt,
                    }
                ],

                model="mixtral-8x7b-32768"
            )
            file.write(chat_completion.choices[0].message.content)
            time.sleep(60) # wait 1 minute in order to use the model again

        file.close()



