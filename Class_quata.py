from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_class_quota(course_code):
    url = "https://w5.ab.ust.hk/wcq/cgi-bin/2410/"  # Base URL for class quota
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Could not fetch data from the class quota website.")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the course section based on the course code
    course_section = soup.find('div', class_='courseanchor', id=course_code)
    if not course_section:
        raise Exception("Course not found.")

    # Extract course information
    course_info = {}
    course_info['subject'] = course_section.find('div', class_='subject').get_text(strip=True)

    # Extract the sections table
    sections_table = course_section.find_next('table', class_='sections')
    if sections_table:
        sections = []
        rows = sections_table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 10:  # Ensure there are enough columns
                section_info = {
                    'section': cells[0].get_text(strip=True),
                    'date_time': cells[1].get_text(strip=True),
                    'room': cells[2].get_text(strip=True),
                    'instructor': cells[3].get_text(strip=True),
                    'ta': cells[4].get_text(strip=True),
                    'quota': cells[5].get_text(strip=True),
                    'enrollment': cells[6].get_text(strip=True),
                    'available': cells[7].get_text(strip=True),
                    'wait': cells[8].get_text(strip=True),
                    'remarks': cells[9].get_text(strip=True),
                }
                sections.append(section_info)
        course_info['sections'] = sections

    return course_info

@app.route('/')
def class_quota():
    course_code = request.args.get('course_code')
    if not course_code:
        return jsonify({'error': 'Course code is required'}), 400

    try:
        quota_info = fetch_class_quota(course_code)
        return jsonify(quota_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)