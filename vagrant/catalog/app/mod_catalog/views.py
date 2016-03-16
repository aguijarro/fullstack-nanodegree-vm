"""
Contains functions used for the catalog process
"""
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, jsonify
#call Blueprint
from . import mod_catalog
from .forms import TaskForm, TypeTaskForm
from .models import Task, TypeTask
from flask import session as login_session
from .. import db
from werkzeug import secure_filename
import os
import json
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
import datetime


def allowed_file(filename):
    app = current_app._get_current_object()
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Show Index site
@mod_catalog.route('/tasks', methods=['GET'])
@mod_catalog.route('/<int:type_task_id>/tasks', methods=['GET'])
def tasks(type_task_id=None):
    """Return a list of tasks recorded in the database related to a Type of Task.
       Args:
         type_task_id: Parameter use to filter tasks.
    """
    page = request.args.get('page', 1, type=int)
    if type_task_id == None:
        paginationTasks = Task.query.paginate(page, per_page=current_app.config['TASK_PER_PAGE'],error_out=False)
    else:
        paginationTasks = Task.query.filter_by(type_task_id=type_task_id).paginate(page, per_page=current_app.config['TASK_PER_PAGE'],error_out=False)

    tasks = paginationTasks.items
    typeTasks = TypeTask.query.filter_by(user_id=login_session['user_id'])
    return render_template('catalog/tasks.html', tasks = tasks, paginationTasks = paginationTasks, typeTasks=typeTasks, type_task_id = type_task_id)

@mod_catalog.route('/<int:task_id>/showTask', methods=['GET'])
def showTask(task_id):
    """Return a specific task recorded in the database.
       Args:
            task_id: Parameter use to query tasks table.
    """
    task = Task.query.filter_by(id=task_id).one()
    typeTasks = TypeTask.query.filter_by(user_id=login_session['user_id'])
    return render_template('catalog/showTask.html', task = task, typeTasks=typeTasks)

# JSON APIs to view Restaurant Information
@mod_catalog.route('/<int:task_id>/showTask/JSON')
def showTaskJSON(task_id):
    """Return a specific task recorded in the database in JSON format.
       Args:
            task_id: Parameter use to query tasks table.
    """
    task = Task.query.filter_by(id=task_id).one()
    return jsonify(Task=task.serialize)

# XML APIs to view Restaurant Information
@mod_catalog.route('/<int:task_id>/showTask/ATOM')
def showTaskATOM(task_id):
    """Return a specific task recorded in the database in ATOM format.
       Args:
            task_id: Parameter use to query tasks table.
    """
    task = Task.query.filter_by(id=task_id).one()
    now = datetime.datetime.now()
    feed = AtomFeed('Recent Task', feed_url=request.url, url=request.url_root)
    feed.add(task.name, content_type='html', id=task_id, author=login_session['username'], updated=now)
    return feed.get_response()


# Show Index site
@mod_catalog.route('/newTask', methods=['GET','POST'])
@mod_catalog.route('/<int:type_task_id>/newTask', methods=['GET','POST'])
def newTask(type_task_id=None):
    """Records a specific task in the database.
       Args:
            type_task_id: Parameter use to save task related to a type_of_task.
    """
    app = current_app._get_current_object()
    form = TaskForm()
    if type_task_id==None:
        typeTaskQuery = TypeTask.query.filter_by(user_id=login_session['user_id'])
    else:
        typeTaskQuery = TypeTask.query.filter_by(user_id=login_session['user_id'],id=type_task_id)
    form.typeTask.query = typeTaskQuery

    if form.validate_on_submit():
        typeTasksId = TypeTask.query.filter_by(name=str(form.typeTask.data)).one()

        fileTask = request.files['fileTask']
        fileTaskName = ''
        if fileTask and allowed_file(fileTask.filename):
            fileTaskName = secure_filename(fileTask.filename)
            fileTask.save(os.path.join(app.config['UPLOAD_FOLDER'], fileTaskName))

        task = Task(name = form.name.data,
                    description = form.description.data,
                    startDate = form.startDate.data,
                    endDate = form.endDate.data,
                    type_task_id = typeTasksId.id,
                    task_path = fileTaskName,
                    user_id = login_session['user_id'])

        db.session.add(task)
        db.session.commit()

        #Redirect to list of tasks. Consider the location of file
        return redirect(url_for('.tasks', type_task_id = type_task_id))

    typeTasks = TypeTask.query.filter_by(user_id=login_session['user_id'])
    return render_template('catalog/newTask.html',form=form,typeTasks=typeTasks, type_task_id = type_task_id)

# Show Index site
@mod_catalog.route('/<int:task_id>/editTask', methods=['GET','POST'])
def editTask(task_id):
    """Modify a specific task recorded in the database.
       Args:
            task_id: Parameter use to query tasks table.
    """
    app = current_app._get_current_object()
    form = TaskForm()
    task = Task.query.get_or_404(task_id)
    typeTaskQuery = TypeTask.query.filter_by(user_id=login_session['user_id'])
    form.typeTask.query = typeTaskQuery

    if form.validate_on_submit():
        typeTasksId = TypeTask.query.filter_by(name=str(form.typeTask.data)).one()

        fileTask = request.files['fileTask']
        fileTaskName = ''
        if fileTask and allowed_file(fileTask.filename):
            fileTaskName = secure_filename(fileTask.filename)
            fileTask.save(os.path.join(app.config['UPLOAD_FOLDER'], fileTaskName))

        task.name = form.name.data
        task.type_task_id = typeTasksId.id
        task.task_path = fileTaskName

        db.session.add(task)
        db.session.commit()
        flash('The task has been updated.')
        return redirect(url_for('.tasks'))


    form.name.data = task.name
    form.description.data = task.description
    form.startDate.data = task.startDate
    form.endDate.data = task.endDate

    '''uses to built menu'''
    typeTasks = TypeTask.query.filter_by(user_id=login_session['user_id'])
    return render_template('catalog/editTask.html',form=form,typeTasks=typeTasks, task = task)

# Show Index site
@mod_catalog.route('/<int:task_id>/deleteTask', methods=['GET','POST'])
def deleteTask(task_id):
    """Delete to a specific task recorded in the database.
       Args:
            task_id: Parameter use to query tasks table.
    """
    task = Task.query.filter_by(id=task_id).first_or_404()
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        flash('The task has been deleted.')
        return redirect(url_for('.tasks'))
    else:
        typeTasks = TypeTask.query.filter_by(user_id=login_session['user_id'])
        return render_template('catalog/deleteTask.html', task = task,typeTasks=typeTasks)


# Show Index site
@mod_catalog.route('/newTypeTask', methods=['GET','POST'])
def newTypeTask():
    """Records a specific Type of task in the database.
    """
    form = TypeTaskForm()
    if form.validate_on_submit():

        typeTask = TypeTask(name = form.name.data,
                            user_id = login_session['user_id'])
        db.session.add(typeTask)
        db.session.commit()

        #Redirect to list of tasks. Consider the location of file
        return redirect(url_for('.tasks'))
    return render_template('catalog/newTypeTask.html',form=form)
