from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl

from application import app
from flask import render_template, request, flash, redirect, url_for
from application import db
from .forms import TodoForm
from datetime import datetime
from bson import ObjectId

import os

# @app.route("/")
# def get_info():
#     todos = []
#     for info in db.collection_DB.find().sort("_id", -1):
#         info["_id"] = str(info["_id"])
#         # info["created_data"] = info["created_data"].strftime("%b %d %Y %H: %M%S")
#         todos.append(info)
        
#     return render_template("view_todos.html", title = "LayOut Page", todos = todos)




@app.route("/")
def get_info():
    todos = db.colection_DB.find().sort("created_data", -1)
    return render_template("view_todos.html", title = "LayOut Page", todos = todos)


# @app.route("/")
# def get_todos():
#     todos = []
#     for todo in db.colection_DB.find().sort("created_data", -1):
#         todo["_id"] = str(todo["_id"])
#         todo["created_data"] = todo["created_data"].strftime("%b %d %Y %H:%M:%S")
#         todos.append(todo)

#     return render_template("view_todos.html", todos = todos)



@app.route("/add_todo" ,methods = ["POST", "GET"])
def add_todo():
    app.config['UPLOAD_FOLDER'] = '../static/assets/image'
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name =  form.name.data
        todo_description = form.description.data
        completed = form.completed.data
        # image = form.image.data


        db.colection_DB.insert_one({ 
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            # "image": image,
            "created_data": datetime.utcnow(), 
        })

        flash("Todo Successfully added the data", "success")
        return redirect("/")
    else:
        form = TodoForm() #todoForm Class k import kore form a insert kora
    
    return render_template("add_todo.html", form = form)




# For Update the Information
@app.route("/update_todo/<id>", methods = ['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form) 
        todo_name =  form.name.data
        todo_description = form.description.data
        completed = form.completed.data
        # image = form.image.data

        db.colection_DB.find_one_and_update({"_id": ObjectId(id)}, {"$set":{
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            # "image": image,
            "created_data": datetime.utcnow(), 

        }})

        flash("Todo Updated successfully!!", "succsss")
        return redirect("/") 
    else:
        form = TodoForm()

        todo = db.colection_DB.find_one_or_404({"_id": ObjectId(id)})
        print(todo)
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completed", None)
        # form.image.data = todo.get("image", None)

    return render_template("add_todo.html", form = form)


# For deleting the record
@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.colection_DB.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo deleted", "success")
    return redirect("/")