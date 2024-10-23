from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV file with the appropriate encoding
try:
    common_queries_df = pd.read_csv(r"C:\Users\HP\nlp\Common_Queries.csv", encoding='ISO-8859-1')
    print("CSV file loaded successfully.")
except Exception as e:
    print(f"Error loading CSV: {e}")

# Function to search query in CSV and return the 'Resolution'
def get_response(user_query):
    # Convert query to lowercase for matching
    user_query = user_query.lower().strip()

    # Search in the 'Query' column for a match and return the corresponding 'Resolution'
    response = common_queries_df[common_queries_df['Query_Text'].str.lower().str.contains(user_query, na=False)]

    if not response.empty:
        # Retrieve the first 'Resolution' column value for the matched query
        return response.iloc[0]['Common_Resolution']
    else:
        # If the query doesn't match any known queries, return a casual response
        return "Hi! I'm here to assist you. Could you please clarify what you're looking for?"

# Route for the chatbot UI
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling chatbot queries
@app.route('/get-response', methods=['POST'])
def chatbot_response():
    user_query = request.form['query']
    chatbot_reply = get_response(user_query)
    return jsonify({'response': chatbot_reply})

if __name__ == '__main__':
    app.run(debug=True)
