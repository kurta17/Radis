from flask import Flask, request, jsonify
import redis


app = Flask(__name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0)


quiz_data = [
  {
    "question_id": 1,
    "question": "What is the capital of France?",
    "options": ["Paris", "Rome", "Berlin", "Madrid"],
    "correct_answer": "Paris"
  },
  {
    "question_id": 2,
    "question": "Which planet is known as the Red Planet?",
    "options": ["Earth", "Mars", "Jupiter", "Saturn"],
    "correct_answer": "Mars"
  },
  {
    "question_id": 3,
    "question": "Who wrote 'Hamlet'?",
    "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"],
    "correct_answer": "William Shakespeare"
  },
  {
    "question_id": 4,
    "question": "What is the largest ocean on Earth?",
    "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
    "correct_answer": "Pacific Ocean"
  },
  {
    "question_id": 5,
    "question": "Which element has the chemical symbol 'O'?",
    "options": ["Gold", "Oxygen", "Silver", "Iron"],
    "correct_answer": "Oxygen"
  }
]



@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    student_name = data['student_name']
    question_id = data['question_id']
    answer = data['answer']
    
    question = next(q for q in quiz_data if q['question_id'] == question_id)
    correct_answer = question['correct_answer']
    
    if answer == correct_answer:
        redis_client.zincrby('leaderboard', 1, student_name)
        return jsonify({"result": "correct"}), 200
    else:
        return jsonify({"result": "incorrect"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

