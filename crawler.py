import requests
from bs4 import BeautifulSoup
import difflib
import re
import pywhatkit

# URL of the page to crawl
url = 'https://vulms.vu.edu.pk/NoticeBoard/NoticeBoard2.aspx'

# Function to get the content of the div with class "m-portlet__body"
def get_div_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    div = soup.find("div", class_="m-portlet__body")
    if div:
        return div.get_text()
    else:
        return ""

# Function to get the text content of a page
def get_page_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.get_text()

# Function to send new content to a WhatsApp group
def send_to_whatsapp_group(message, group_id):
    # Replace with the group ID of the WhatsApp group
    group_id = "Bel2RDaQvfwD2lt2saaZ9t"

    # Send the message to the WhatsApp group
    pywhatkit.sendwhatmsg_to_group_instantly(group_id, message)
    print(f"Message sent to WhatsApp group '{group_id}': {message}")

# Function to check for changes in the div
def check_for_changes(url, previous_content):
    current_content = get_div_content(url)
    if current_content != previous_content:
        diff = difflib.unified_diff(previous_content.splitlines(), current_content.splitlines(), n=0, lineterm='')
        new_content = []
        for line in diff:
            if line.startswith('+'):
                new_content.append(line[1:])
        if new_content:
            print("New content in the 'm-portlet__body' div:")
            message = "\n".join(new_content)
            print(message)
            send_to_whatsapp_group(message, "Your Group ID")  # Send new content to WhatsApp group

            # Check for hyperlinks and print linked page content
            for line in new_content:
                link = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
                if link:
                    link_url = link.group()
                    print(f"Found hyperlink: {link_url}")
                    page_text = get_page_text(link_url)
                    print("Text content of the linked page:")
                    print(page_text)
            return current_content
    else:
        return previous_content

# Initial div content
previous_content = get_div_content(url)

# Send a test message
test_message = "This is an automated test message."
send_to_whatsapp_group(test_message, "Your Group ID")

# Continuous monitoring loop
while True:
    previous_content = check_for_changes(url, previous_content)
    # Add a delay or break condition as needed