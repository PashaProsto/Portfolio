#Импорт
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

SOCIAL_LINKS = {
    "email": "pavelzubashich@gmail.com",
    "GitHub": "https://github.com/PashaProsto",
    "telegram": "https://t.me/alembic1"
}

# Обработка главной страницы
@app.route('/', methods=['GET', 'POST'])
def home():
    # Обработка кнопок проектов
    button_python = request.form.get('button_python')
    button_html = request.form.get('button_html')
    button_db = request.form.get('button_db')
    button_TG = request.form.get('button_TG')
    
    feedback_sent = False
    
    # Обработка формы обратной связи
    if request.method == 'POST' and 'email' in request.form and 'text' in request.form:
        email = request.form['email']
        message = request.form['text']
        
        # Сохраняем в базу данных
        new_feedback = Feedback(email=email, message=message)
        db.session.add(new_feedback)
        db.session.commit()
        feedback_sent = True
    
    return render_template(
        'index.html', 
        social_links=SOCIAL_LINKS,
        button_python=button_python,
        button_html=button_html,
        button_TG=button_TG,
        button_db=button_db,
        feedback_sent=feedback_sent
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
