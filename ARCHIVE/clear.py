from bs4 import BeautifulSoup

def clean_forum_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove page header
    header = soup.find('header', class_='p-header')
    if header:
        header.decompose()
    
    # Remove navigation
    nav = soup.find('nav', class_='p-nav')
    if nav:
        nav.decompose()
    
    # Remove footer
    footer = soup.find('footer', class_='p-footer')
    if footer:
        footer.decompose()
    
    # Remove breadcrumbs
    for breadcrumbs in soup.find_all('ul', class_='p-breadcrumbs'):
        breadcrumbs.decompose()
    
    # Process each message/post
    for message in soup.find_all('article', class_='message'):
        # Remove action buttons (reply, edit, etc.)
        for action_bar in message.find_all('div', class_='actionBar'):
            action_bar.decompose()
        
        # Remove footer with buttons
        for footer in message.find_all('footer', class_='message-footer'):
            footer.decompose()
        
        # Remove user stats and extras (keep only username and avatar)
        message_user = message.find('section', class_='message-user')
        if message_user:
            # Keep only the avatar and username elements
            for elem in message_user.find_all(True):
                if elem is None:
                    continue

                # Get class safely
                try:
                    elem_classes = elem.get('class', []) if elem else []
                    if not isinstance(elem_classes, list):
                        elem_classes = []
                except:
                    continue
                # Keep only avatar and username elements
                if 'message-userExtra' in elem_classes or 'message-userExtras' in elem_classes or 'message-userStats' in elem_classes:
                    elem.decompose()
        
        # Remove signature
        for signature in message.find_all('aside', class_='message-signature'):
            signature.decompose()
    
    # Remove quick reply section
    quick_reply = soup.find('form', class_='js-quickReply')
    if quick_reply:
        quick_reply.decompose()
    
    # Remove "Users viewing this thread" section
    user_activity = soup.find('div', class_='block-userActivity')
    if user_activity:
        user_activity.decompose()
    
    # Remove share buttons
    share_buttons = soup.find('div', class_='shareButtons')
    if share_buttons:
        share_buttons.decompose()
    
    # Remove pagination
    for pagination in soup.find_all('nav', class_='pageNavWrapper'):
        pagination.decompose()
    
    return str(soup)

# Example usage:
with open('Finished - Daily Puzzles - Page 3 - The PokéCommunity Forums.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

cleaned_html = clean_forum_html(html_content)

with open('cleaned_forum_page_3.html', 'w', encoding='utf-8') as f:
    f.write(cleaned_html)