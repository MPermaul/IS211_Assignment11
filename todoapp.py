from flask import Flask, render_template, redirect, request
import pickle
import re
app = Flask(__name__)


class Task():
    """A class represnting a task on a to do list."""

    # constructor for Task
    def __init__ (self, task, email, priority):
        self.task = task
        self.email = email
        self.priority = priority


# route for the index page
@app.route('/')
def index():

    # use index.html in templates directory, passing in the task list and message
    return render_template('index.html', todo_list = todo_list, message = message)

# route for submit button
@app.route('/submit', methods = ['POST'])
def submit():
    
    global message
    global todo_list
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    # check to verify if task field is empty
    if task == '':
        message = 'Unable to Add Task - Task Field is Blank'
        return redirect("/")

    # regex pattern for verifying the email address
    email_reg = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

    # check to verify if email field is empty
    if email == '':
        message = 'Unable to Add Task - Email Field is Blank'
        return redirect("/")
    
    # check to verify if email entered is valid
    elif not re.search(email_reg, email):
        message = 'Unable to Add Task - Email Format is Not Valid'
        return redirect("/")
    
    # check to verify if priority was set
    if priority == 'Blank':
        message = 'Unable to Add Task - Priority Was Not Set'
        return redirect("/")
      
    # create Task class object and pass in form data once checks have passed
    new_task = Task(task, email, priority)
    
    # add task to list and set message varialbe back to blank
    todo_list.append(new_task)
    message = ''

    # redirect to index page
    return redirect("/")

# route for clear all tasks button
@app.route('/clear', methods = ['POST'])
def clear():

    global todo_list
    global message

    # set todo list to empty list
    todo_list = []
    message = ''
    
    # redirect to index page
    return redirect("/")


# route to delete individual task
@app.route('/delete', methods=['POST'])
def delete():

    global todo_list
    
    # get index value for row to delete
    index = int(request.form['index'])

    # delete object in list at that index
    del todo_list[index]
    
    # redirect to index page
    return redirect("/")


# route to save tasks to file
@app.route('/save', methods=['POST'])
def save():

    global todo_list
    global message

    # dump list to file using pickle    
    pickle.dump(todo_list, open('todo.p', 'wb'))

    # display message that file was saved
    message = 'To Do List Saved'

    # redirect to index page
    return redirect("/")


if __name__ == '__main__':


    # Global Variables for use within the app
    message = ''

    # check if file exists with saved task data and set it to todo list
    try:
        todo_list = pickle.load(open('todo.p', 'rb'))

    # if any exception, set todo
    except:
        todo_list = []

    # run the app
    app.run()
