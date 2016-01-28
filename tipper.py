"""
The KickTippTipper logs into your KickTipp account and automatically
submits his generated bets. The bets get calculated by considering
each teams odds.
"""
import robobrowser
from bs4 import BeautifulSoup
import math


url_tippabgabe = "http://www.kicktipp.de/leon2006/tippabgabe"
url_login = "http://www.kicktipp.de/info/profil/login"
nutzername = "my_username
passwort = "my_password"


def login():
    """Logs into useraccount"""
    browser.open(url_login)
    form = browser.get_form()
    form['kennung'] = nutzername
    form['passwort'] = passwort
    browser.submit_form(form)


def grab_odds():
    """Grabs latest odds for each match"""
    odds = []
    browser.open(url_tippabgabe)
    
    for i in browser.find_all("td", class_="kicktipp-wettquote"):
        quote = float(i.get_text())
        odds.append(quote)
    odds = [odds[i:i+3] for i in range(0, len(odds), 3)]
    return odds


def calc_results(odds):
    """By considering odds, calculates match results"""
    results = []
    deuce = [1,1]
    team1 = [2,1]
    team2 = [1,2]
    team1_high = [3,1]
    team2_high = [1,3]
    
    for i in odds:
        diff = math.fabs(i[0]-i[2])
        if diff < 1.0:
            results.append(deuce)
        elif diff > 8.0:
            if i[0] > i[1]:
                results.append(team2_high)
            else:
                results.append(team1_high)
        else:
            if i[0] > i[1]:
                results.append(team2)
            else:
                results.append(team1)
    return results


def get_keys():
    """Get necessary input keys"""
    formkeys = []
    browser.open(url_tippabgabe)
    
    for i in browser.find_all("input",type="tel"):
        formkeys.append(i.get("name"))
    formkeys = [formkeys[i:i+2] for i in range(0, len(formkeys), 2)]
    return formkeys


def pass_results(results):
    """Submit calculated results and save them"""
    formkeys = get_keys()
    browser.open(url_tippabgabe)
    form = browser.get_form()
    
    for i in range(0,9):
        form[formkeys[i][0]] = results[i][0]
        form[formkeys[i][1]] = results[i][1]        
    browser.submit_form(form)
            
 
if __name__ == '__main__':
        browser = robobrowser.RoboBrowser()
        login()
        my_odds = grab_odds()
        my_results = calc_results(my_odds)
        pass_results(my_results)

