from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clipboard.db'
db = SQLAlchemy(app)

class UserClipboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    copied_text = db.Column(db.String(255), nullable=True)

@app.route('/get_clipboard/<string:user_id>', methods=['GET'])
def get_clipboard(user_id):
    with app.app_context():
        user_clipboard = UserClipboard.query.filter_by(user_id=user_id).first()
        if user_clipboard:
            return jsonify({'copied_text': user_clipboard.copied_text})
        return jsonify({'copied_text': ''})

@app.route('/set_clipboard/<string:user_id>', methods=['POST'])
def set_clipboard(user_id):
    data = request.get_json()
    copied_text = data.get('copied_text', '')

    with app.app_context():
        user_clipboard = UserClipboard.query.filter_by(user_id=user_id).first()
        if user_clipboard:
            user_clipboard.copied_text = copied_text
        else:
            user_clipboard = UserClipboard(user_id=user_id, copied_text=copied_text)

        db.session.add(user_clipboard)
        db.session.commit()
    return jsonify({'message': 'Clipboard updated successfully'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
