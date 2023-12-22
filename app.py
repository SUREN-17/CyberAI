from flask import Flask, render_template, jsonify, request
import openpyxl

app = Flask(__name__)

# Load FAQ data from Excel
def load_faqs_from_excel(file_name):
    faq_data = {}
    try:
        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            question, answer = row
            faq_data[question] = answer
        return faq_data
    except FileNotFoundError:
        return None

faq_data = load_faqs_from_excel('chat_bot.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_query = request.json['query']
    bot_response = faq_data.get(user_query, "Sorry, I don't have an answer for that.")
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
