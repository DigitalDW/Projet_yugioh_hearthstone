from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        r = get(url, stream=True)
        if is_good_response(r):
            raw_html = r.content
            html = BeautifulSoup(raw_html, 'html.parser')
            date = None
            if html.find("div", {"data-source": "na_release_date"}) is None:
                date = html.find("div", {"data-source": "en_release_date"})
            else:
                date = html.find("div", {"data-source": "na_release_date"})
            if date is None:
                date = html.find("div", {"data-source": "eu_release_date"})
            
            if date is not None:
                return date.find("div", {"class": "pi-data-value pi-font"}).decode_contents()
            else:
                return "[TBD]"
        else:
            return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
        and content_type is not None 
        and content_type.find('html') > -1)


def log_error(e):
    """
    This function just prints error
    """
    print(e)

def main():
    texte = ""
    try:
        input_test = open("../../data/txt/yugioh_sets.txt","r")
        texte = input_test.read()
        input_test.close()
    except IOError:
        print("Impossible d'ouvrir le fichier!")

    set_dict = {}
    compteur = 1
    for sets in texte.split("\n"):
        date = simple_get("https://yugioh.fandom.com/wiki/" + sets)
        set_dict[sets] = date
        print(compteur)
        compteur+=1

    with open('../../data/json/yugioh_data/yugioh_sets_data.json', 'w', encoding='utf-8') as f:
        json.dump(set_dict, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()