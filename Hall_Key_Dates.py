from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_important_dates():
    url = "https://shrl.hkust.edu.hk/apply-for-housing/ug/new-local-ugs" #The url that is going to be fetched
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing key dates
    dates_table = soup.find('table', class_='calendar-details') # Get the Key dates in the website

    important_dates = []

    if dates_table:
        rows = dates_table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                date_info = {
                    'date': cells[0].get_text(strip=True),
                    'event': cells[1].get_text(strip=True)
                }
                important_dates.append(date_info) #Store the important dates and event

    return important_dates

@app.route('/')
def important_dates():
    try:
        dates = fetch_important_dates()
        return jsonify(dates) #change dates into a json file
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)