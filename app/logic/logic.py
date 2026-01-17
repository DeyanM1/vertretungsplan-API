import json
from dataclasses import dataclass
from typing import Any
import datetime

import regex as re
import requests
from bs4 import BeautifulSoup


class DomainError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

@dataclass
class Entry:
    klasse: str
    hour: str
    vertreter: str
    fach: str
    fachNeu: str
    raum: str
    art: str
    text: str

    def ret(self):
        return self.klasse, self.hour, self.vertreter, self.fach, self.fachNeu, self.raum, self.art, self.text

def getCurrentWeekNumber() -> str:
    today = datetime.datetime.today()
    weekNum = today.isocalendar().week

    return str(weekNum)

def translateClassIndex(className: str, availableClasses: dict[str, int]) -> str:
    """
    Translates a className to their urlClassIndex ex.: 09F -> 000034
    """
    
    classIndex = availableClasses.get(className)
    
    return f"0000{classIndex}" if len(str(classIndex)) < 2 else f"000{classIndex}"

def getAvailableClasses() -> dict[str, int]:
    """
    returns: dict[className, classIndex]
    """
    url = "https://arg-heusenstamm.de/vertretungsplan/allgemein/frames/navbar.htm" 
    try:
        page = requests.get(url)
    except Exception:
        raise DomainError("Error at fetching availableClasses", 500)
    
    if not page:
        raise DomainError("Error at fetching availableClasses", 500)
    
    soup = BeautifulSoup(page.text, "html.parser")
    scriptTag = soup.find_all("script")[1]
    
    classes: list[str] = []

    scriptText: str = str(scriptTag.string)
    if not scriptTag.string:
        #print("ERROR | Failed getting Classes List")
        raise DomainError("Error at fetching availableClasses", 500)

    match = re.search(pattern=r'var classes\s*=\s*(\[[^\]]*\])', string=scriptText)

    if not match:
        #print("ERROR | Couldnt match class")
        raise DomainError("Error at fetching availableClasses", 500)

    classes = json.loads(match.group(1))


    availableClasses: dict[str, int] = {cls: i+1 for i, cls in enumerate(classes)}
    
    return availableClasses


def makeRequest(className: str, weekNumRaw: str) -> list[dict[str, dict[int, Entry]]]|str:
    """
    Return is dict[weekNum, dict[dayOfWeekNum, Entry]]
    """


    urlClassIndex = translateClassIndex(className, getAvailableClasses())
    

    listEntries: list[dict[str, dict[int, Entry]]] = []

    match weekNumRaw:
        case "-1":
            weekList = [getCurrentWeekNumber()]
        case "-2":
            weekList = list(range(1, 53))
        case "-3":
            weekList = [getCurrentWeekNumber(), str(int(getCurrentWeekNumber())+1)]
        case _:
            weekList = [weekNumRaw]


    for week in weekList:
        weekNum = f"0{week}" if len(str(week)) == 1 else str(week)

        url = f"https://arg-heusenstamm.de/vertretungsplan/allgemein/{weekNum}/w/w{urlClassIndex}.htm"

        try:
            page = requests.get(url)
        except Exception:
            raise DomainError("Error at fetching plan for given class", 500)

        if not page.text:
            raise DomainError("Error at fetching plan for given class", 500)


        soup = BeautifulSoup(page.text, "html.parser")
        
        days: dict[str, dict[int, Entry]] = {
            "Montag": {},
            "Dienstag": {},
            "Mittwoch": {},
            "Donnerstag": {},
            "Freitag": {}
        }
        
        dayAnchors: dict[str, str] = {
                "Montag": "1",
                "Dienstag": "2",
                "Mittwoch": "3",
                "Donnerstag": "4",
                "Freitag": "5"
            }


        for dayName, anchorName in dayAnchors.items():
            anchor = soup.find('a', attrs={'name': anchorName})
            
            if anchor:
                table = anchor.find_next('table', class_='subst')
                
                if table:
                    rows = table.find_all('tr', class_='list')
                    
                    
                    row_index = 0
                    for row in rows:
                        cols = row.find_all('td')
                        if not cols: 
                            continue 

                        def get_text(col: Any) -> str:
                            return col.get_text(strip=True)

                        # 0: Klasse (09F)
                        # 1: Stunde (5 - 6)
                        # 2: Vertreter (Fr. Brandis)
                        # 3: Fach (M) - The original subject
                        # 4: (Fach) - The new subject
                        # 5: Raum (---)
                        # 6: Art (Entfall)>
                        # 7: Text

                        entry = Entry(get_text(cols[0]), get_text(cols[1]), get_text(cols[2]), get_text(cols[3]), get_text(cols[4]), get_text(cols[5]), get_text(cols[6]), get_text(cols[7]))


                        # Add to dictionary
                        days[dayName][row_index] = entry
                        row_index += 1
            

        listEntries.append(days)

    return listEntries