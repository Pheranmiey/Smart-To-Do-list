from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Task lists
tasks = []
done_tasks = []

# Function to calculate priority score
def calculate_priority(due_date, estimated_time, complexity, urgency):
    days_until_due = (due_date - datetime.date.today()).days
    urgency_weight = 0.4
    complexity_weight = 0.2
    time_weight = 0.1
    due_date_weight = 0.3
    priority_score = (urgency * urgency_weight) + (10 - complexity) * complexity_weight + \
                     (10 - estimated_time) * time_weight + (10 - min(days_until_due, 10)) * due_date_weight
    return priority_score

@app.route('/')
def index():
    # Sort tasks by priority
    sorted_tasks = sorted(tasks, key=lambda x: calculate_priority(
        x['due_date'], x['estimated_time'], x['complexity'], x['urgency']), reverse=True)

    # Adding calculated priority score to tasks
    for task in sorted_tasks:
        task['priority_score'] = calculate_priority(
            task['due_date'], task['estimated_time'], task['complexity'], task['urgency']
        )

    return render_template('index.html', tasks=sorted_tasks, done_tasks=done_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    due_date = datetime.datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
    estimated_time = int(request.form['estimated_time'])
    complexity = int(request.form['complexity'])
    urgency = int(request.form['urgency'])

    task = {
        'task_name': task_name,
        'due_date': due_date,
        'estimated_time': estimated_time,
        'complexity': complexity,
        'urgency': urgency,
    }

    tasks.append(task)
    return redirect(url_for('index'))

@app.route('/mark_done/<int:task_id>', methods=['POST'])
def mark_done(task_id):
    task = tasks.pop(task_id)
    done_tasks.append(task)
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    tasks.pop(task_id)
    return redirect(url_for('index'))

@app.route('/undo/<int:task_id>', methods=['POST'])
def undo(task_id):
    task = done_tasks.pop(task_id)  # Remove from done tasks
    tasks.append(task)  # Add back to active tasks
    return redirect(url_for('index'))

@app.route('/delete_last_done', methods=['POST'])
def delete_last_done():
    if done_tasks:
        done_tasks.pop()  # Remove the last completed task
    return redirect(url_for('index'))

@app.route('/delete_completed_task/<int:task_id>', methods=['POST'])
def delete_completed_task(task_id):
    done_tasks.pop(task_id)  # Remove the specified completed task
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
