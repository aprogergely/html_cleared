from bs4 import BeautifulSoup

def clean_forum_html(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Remove all script and style tags
    for tag in soup(["script", "noscript", "link", "style"]):
        tag.decompose()

    # Remove anchor tags but keep their text content
    for a in soup.find_all("a"):
        if a.find("img"):
            a.unwrap()  # keeps image
        elif a.text.strip():
            a.replace_with(a.text)
        else:
            a.decompose()

    # Remove elements that are purely decorative or interactive outside posts
    for cls in [
        "message-attribution-opposite",
        "bookmarkLink",
        "message-attribution-gadget",
        "fa-share-alt",
        "fa-eye",
        "fa-eye-slash"
    ]:
        for el in soup.select(f".{cls}"):
            el.decompose()

    # Remove inline mod controls and attributes like data-xf-init, onclick, etc.
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr.startswith("data-") or attr in ["onclick", "role", "id", "itemprop", "itemscope", "itemtype", "aria-hidden", "aria-label", "rel", "tabindex", "title"]:
                del tag.attrs[attr]

    # Remove empty <i> or <time> tags outside messages
    for tag in soup.find_all(["i", "time"]):
        if not tag.text.strip() and not tag.find("img"):
            tag.decompose()

    # Remove empty or non-functional bbImageWrappers
    for wrapper in soup.select(".bbImageWrapper"):
        img = wrapper.find("img")
        if not img or not img.get("src"):
            wrapper.decompose()
        else:
            wrapper.replace_with(img)

    # Output the cleaned HTML
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(str(soup))

# Example usage:
clean_forum_html("cleaned_forum_page_3.html", "forum_page_static_3.html")
