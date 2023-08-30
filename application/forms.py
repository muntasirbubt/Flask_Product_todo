from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
photos = UploadSet('photos', IMAGES)



class TodoForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    completed = SelectField("Completed", choices=[("False", "false"), ("True", "true")], validators=[DataRequired()])
    image = FileField("Image", validators=[FileAllowed(photos, 'Images only!')])
    submit = SubmitField("Add Todo")

    