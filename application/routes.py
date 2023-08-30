from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl

from application import app
from flask import render_template, request, flash, redirect, url_for
from application import db
from .forms import TodoForm
from datetime import datetime
from bson import ObjectId
from werkzeug.utils import secure_filename
# from werkzeug.utils import send_from_directory

import os





@app.route("/")
def get_info():
    todos = db.colection_DB.find().sort("created_data", -1)
    return render_template("view_todos.html", title = "LayOut Page", todos = todos)


#save function

def save_image(image):
    if image:
        image_filename = secure_filename(image.filename)
        image_dir =  os.path.join("static","asset","images")
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, image_filename)
        image.save(image_path)
        return image_filename
    return None
    


@app.route("/add_todo" ,methods = ["POST", "GET"])
def add_todo():
    # app.config['UPLOAD_FOLDER'] = '../static/assets/image'
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name =  form.name.data
        todo_description = form.description.data
        completed = form.completed.data
        image = request.files.get("image")

        print(f"Todo Name: {todo_name}")
        print(f"Todo Description: {todo_description}")
        print(f"Completed: {completed}")
        print(f"image: {image}")


        final_image = None
        if image:
            final_image=save_image(image)
        print(f"Final Image: {final_image}")

        db.colection_DB.insert_one({ 
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "image": final_image,
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
    data_DB = db.colection_DB.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        form = TodoForm(request.form) 
        todo_name =  form.name.data
        todo_description = form.description.data
        completed = form.completed.data
        image = request.files.get("image")


        if image:
            # Delete the existing image file
            delete_image(data_DB["image"])

            # Save the new image and get its filename
            image_filename = save_image(image)


        db.colection_DB.find_one_and_update({"_id": ObjectId(id)}, {"$set":{
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "image": image_filename,
            "created_data": datetime.utcnow(), 

        }})


        flash("Todo Updated successfully!!", "succsss")
        return redirect("/") 
    else:
        form = TodoForm()
        x= db.colection_DB.find_one({"_id": ObjectId(id)})

        todo = db.colection_DB.find_one_or_404({"_id": ObjectId(id)})
        print(todo)
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completed", None)
        x['image'] = todo.get("image", None)

    return render_template("add_todo.html", form = form)



def delete_image(image_filename):
    if image_filename:
        image_path = os.path.join("static", "asset", "images", image_filename)
        print(image_path)
        if os.path.exists(image_path):
            os.remove(image_path)




# For deleting the record
@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.colection_DB.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo deleted", "success")
    return redirect("/")