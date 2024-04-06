
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process_item', methods=['POST'])
def process_item():
    selected_item = request.form.get('selected_item')
    # Process the selected item (e.g., perform some action or return a response)
    # You can replace this with your actual backend logic
    return jsonify({'message': f'Selected item: {selected_item}'})

if __name__ == '__main__':
    app.run(debug=True)

