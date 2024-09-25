import requests

API_URL = 'http://localhost:5000/submit_answer'

quiz_data = [
  {
    "question_id": 1,
    "question": "What is the capital of France?",
    "options": ["Paris", "Rome", "Berlin", "Madrid"],

  },
  {
    "question_id": 2,
    "question": "Which planet is known as the Red Planet?",
    "options": ["Earth", "Mars", "Jupiter", "Saturn"],
    
  },
  {
    "question_id": 3,
    "question": "Who wrote 'Hamlet'?",
    "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"],
    
  },
  {
    "question_id": 4,
    "question": "What is the largest ocean on Earth?",
    "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
    
  },
  {
    "question_id": 5,
    "question": "Which element has the chemical symbol 'O'?",
    "options": ["Gold", "Oxygen", "Silver", "Iron"],
    
  }
]


def send_answer(student_name, question_id, answer):
    try:
        response = requests.post(API_URL, json={
            "student_name": student_name,
            "question_id": question_id,
            "answer": answer
        })
        
        # Check if the server returned a successful status code
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from the server.")
            print(f"Response content: {response.text}")
            return

        # Try to parse the response as JSON
        result = response.json().get('result', 'unknown')
        print(f"Your answer is {result}!")

    except requests.exceptions.RequestException as e:
        print(f"Error while sending request: {e}")

if __name__ == "__main__":
    student_name = input("Enter your name: ")
    
    for question in quiz_data:
        print(question['question'])
        for idx, option in enumerate(question['options'], 1):
            print(f"{idx}. {option}")
        answer_idx = int(input("Enter your answer (1-4): ")) - 1
        send_answer(student_name, question['question_id'], question['options'][answer_idx])


