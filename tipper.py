"""
The KickTippTipper logs into your KickTipp account and automatically
submits its generated bets. The bets get calculated by considering
each teams odds.
"""
import robobrowser
from bs4 import BeautifulSoup
import math

url_login = "http://www.kicktipp.de/info/profil/login"

#Possible Results, modify at will
deuce = [1,1]
team1_win = [2,1]
team2_win = [1,2]
team1_greatwin = [3,1]
team2_greatwin = [1,3]


def login():
    """Logs into useraccount"""
    while True:
        username = input("Username: ")
        password = input("Password: ")
        browser.open(url_login)
        form = browser.get_form()
        form['kennung'] = username
        form['passwort'] = password
        browser.submit_form(form)

        if not did_login_work():
            print("Your email or password was incorrect. Please try again.")
            print("")
        else:
            break
        
                
def did_login_work():
    """Returns true if function does not find any input possibility"""
    for i in browser.find_all("input",type="text"):
        if i.get("name") == "kennung":
            return False
    return True
        
def grab_odds():
    """Grabs latest odds for each match"""
    odds = []
    browser.open(url_betting)
    
    for i in browser.find_all("td", class_="kicktipp-wettquote"):
        quote = float(i.get_text())
        odds.append(quote)
    odds = [odds[i:i+3] for i in range(0, len(odds), 3)]
    return odds


def calc_results(odds):
    """By considering odds, calculates match results"""
    results = []
    
    for i in odds:
        diff = math.fabs(i[0]-i[2])
        if diff < 1.0:
            results.append(deuce)
        elif diff > 8.0:
            if i[0] > i[1]:
                results.append(team2_greatwin)
            else:
                results.append(team1_greatwin)
        else:
            if i[0] > i[1]:
                results.append(team2_win)
            else:
                results.append(team1_win)
    return results


def get_keys():
    """Get necessary input keys"""
    formkeys = []
    browser.open(url_betting)
    
    for i in browser.find_all("input",type="text"):
        formkeys.append(i.get("name"))
    formkeys = [formkeys[i:i+2] for i in range(0, len(formkeys), 2)] 
    return formkeys


def pass_results(results):
    """Submit calculated results and save them"""
    formkeys = get_keys()
    browser.open(url_betting_mobile)
    form = browser.get_form()
    
    #If some matches already have been played the results list needs to be adjusted
    if len(formkeys) != len(results):
        to_delete = len(results)-len(formkeys)
        results = results[to_delete:]

    for i in range(0,len(formkeys)):
        form[formkeys[i][0]] = results[i][0]
        form[formkeys[i][1]] = results[i][1]
    browser.submit_form(form)


def grab_beturl():
    """Searches for the bet-url"""
    for i in browser.find_all("a"):
        link = i.get("href")
        name = i.contents[0]
        link = link.replace("/","")
        if link == name:
            return link
            break

def set_bet_urls(attachment):
    """Sets bet-urls"""
    global url_betting
    global url_betting_mobile
    url_betting = "http://www.kicktipp.de/" + attachment + "/tippabgabe"
    url_betting_mobile = "http://m.kicktipp.de/" + attachment + "/tippabgabe"
    
    
if __name__ == '__main__':
    browser = robobrowser.RoboBrowser(parser="html.parser")
    login()
    set_bet_urls(grab_beturl())
    my_odds = grab_odds()
    my_results = calc_results(my_odds)
    pass_results(my_results)
    print("Done!")
