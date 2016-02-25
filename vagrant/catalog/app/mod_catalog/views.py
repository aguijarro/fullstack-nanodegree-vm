from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
#call Blueprint
from . import mod_catalog
from .forms import TaskForm
from .models import Task
from .. import db

# Show Index site
@mod_catalog.route('/task/', methods=['GET'])
def tasks():
    tasks = Task.query.all()
    print tasks
    return render_template('catalog/tasks.html', tasks = tasks)

# Show Index site
@mod_catalog.route('/task/newTask', methods=['GET','POST'])
def newTask():
    form = TaskForm()
    if form.validate_on_submit():

        task = Task(name = form.name.data)
        db.session.add(task)
        db.session.commit()

        #Redirect to list of tasks. Consider the location of file
        return redirect(url_for('.tasks'))
    return render_template('catalog/newTask.html',form=form)

# Show Index site
@mod_catalog.route('/task/<int:task_id>/editTask', methods=['GET','POST'])
def editTask(task_id):
    form = TaskForm()
    task = Task.query.get_or_404(task_id)

    if form.validate_on_submit():
        task.name = form.name.data
        db.session.add(task)
        db.session.commit()
        flash('The task has been updated.')
        return redirect(url_for('.tasks'))
    form.name.data = task.name
    return render_template('catalog/editTask.html',form=form)

# Show Index site
@mod_catalog.route('/task/<int:task_id>/deleteTask', methods=['GET','POST'])
def deleteTask(task_id):
    task = Task.query.filter_by(id=task_id).first_or_404()
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        flash('The task has been deleted.')
        return redirect(url_for('.tasks'))
    else:
        return render_template('catalog/deleteTask.html', task = task)
