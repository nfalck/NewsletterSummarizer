# importing the modules I made
import gmail
import summarize

# write your newsletters in the list
emails = ["klementoninvesting@substack.com", "community@amplifyme.com", "dan@tldrnewsletter.com"]

# fetch the emails and put their content into collectedemails.txt
gmail.get_emails(gmail.query_setter(emails=emails))

# splitting and AI summarization of collectedemails.txt with output in summary.txt
summarize.ai_summarize(summarize.split_text())

# printing that it is complete
print("complete!")