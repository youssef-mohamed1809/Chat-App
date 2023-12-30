import re
import simpleaudio as sa
from colorama import init, Fore, Style

init(autoreset=True)

def print_colorized_text(text,color,end = '\n'):
    if color == 'RED':
        print(Fore.RED + text,end = end)
    elif color == 'GREEN':
        print(Fore.GREEN + text,end = end)
    elif color == 'BLUE':
        print(Fore.BLUE + text,end = end)
    elif color == 'YELLOW':
        print(Fore.YELLOW + text,end = end)
    else:
        print(text,end)
    


def play_sound(file_path):
    try:
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()  
    except Exception as e:
        print(f"An error occurred: {e}")

emojis = {
    ":)": "😀",
    ";)": "😂",
    ":(": "😢",
    "fire": "🔥",
}

def format_emoji(input_string):
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def replace_with_emoji(match):
        emoji_name = match.group(1)
        emoji = emojis.get(emoji_name, None)
        if emoji:
            return f"{BOLD}{emoji}{RESET}"
        else:
            return f"[{emoji_name} not found]"

    formatted_string = re.sub(r'\&(.*?)\&', replace_with_emoji, input_string)
    return formatted_string


def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''
    blue_text = '\033[34m' 
    reset_color = '\033[0m'
    escape_mask = '\033]8;{};{}\033\\' + blue_text + '{}'+ reset_color + '\033]8;;\033\\'
    return escape_mask.format(parameters, uri, label)

def convert_urls_to_hyperlinks(text):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def replace_with_hyperlink(match):
        url = match.group(0)
        return link(url)

    return re.sub(url_pattern, replace_with_hyperlink, text)

def format_user_input(input_text):

    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

    formatted_text = input_text
    formatted_text = re.sub(r'\*(.*?)\*', lambda m: f"{BOLD}{m.group(1)}{RESET}", formatted_text)
    formatted_text = re.sub(r'_(.*?)_', lambda m: f"{ITALIC}{m.group(1)}{RESET}", formatted_text)
    formatted_text = re.sub(r'~(.*?)~', lambda m: f"{UNDERLINE}{m.group(1)}{RESET}", formatted_text)

    return formatted_text


def format_messages(msg):
    formatted_output = format_user_input(msg)
    formatted_output = convert_urls_to_hyperlinks(formatted_output)
    formatted_output = format_emoji(formatted_output)
    return formatted_output
