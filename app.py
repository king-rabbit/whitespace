import os
import uuid
import datetime
from flask import Flask, render_template, request, send_from_directory, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_ckeditor import CKEditor, CKEditorField, upload_success, upload_fail
from flask_wtf import CSRFProtect  

load_dotenv()
ckeditor = CKEditor()
basedir = os.path.abspath(os.path.dirname(__file__))



def create_app():
    app = Flask(__name__) 
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.whitespace
    entries = []

    app.config['CKEDITOR_SERVE_LOCAL'] = True
    app.config['CKEDITOR_HEIGHT'] = 400
    app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'  # this value can be endpoint or url
    app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')
    app.config['CKEDITOR_ENABLE_CSRF'] = True

    app.secret_key = 'secret string'

    ckeditor.init_app(app)
    csrf = CSRFProtect(app) 


    class PostForm(FlaskForm):
        title = StringField('Title')
        body = CKEditorField('Body', validators=[DataRequired()])
        submit = SubmitField()


    @app.route("/", methods=["GET", "POST"])
    def home():
        
        entries_with_date = [
                ( entry['title'], entry['content'], datetime.datetime.strptime(entry['date'], "%Y-%m-%d").strftime("%b %d") )
                for entry in app.db.posts.find({},)
                ]

        return render_template("index.html", entries=entries_with_date)


    @app.route("/admin/write_post", methods=['GET', 'POST'])
    def write_post():
        form = PostForm()
        if form.validate_on_submit():
             entry_title = form.title.data
             entry_content = form.body.data
            #entry_title = request.form.get("title")
            #entry_content = request.form.get("content")
            #entry_content = request.form.get('ckeditor')
            #entry_content = entry_content.replace('\r\n' , "<br>")
             formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")

             app.db.posts.insert_one({"title":entry_title, "content":entry_content, "date":formatted_date})
             

        return render_template("write_post.html", form=form) 

    
    
    @app.route('/files/<path:filename>')
    def uploaded_files(filename):
        path = app.config['UPLOADED_PATH']
        return send_from_directory(path, filename)

    @app.route('/upload', methods=['POST'])
    def upload():
        f = request.files.get('upload')
        extension = f.filename.split('.')[-1].lower()
        if extension not in ['jpg', 'gif', 'png', 'jpeg']:
            return upload_fail(message='Image only!')
        unique_filename = str(uuid.uuid4())
        f.filename = unique_filename + '.' + extension
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        url = url_for('uploaded_files', filename=f.filename)
        return upload_success(url, filename=f.filename)  # return upload_success call


    @app.route("/post/<string:post_title>",  methods=['GET', 'POST'])
    def individual_post(post_title):

        result = app.db.posts.find( {"title":post_title } )

        for post in app.db.posts.find( {"title":post_title }):
             post_content = post['content'].split('\r\n')

        post_meta = [ 
            (post['title'], datetime.datetime.strptime(post['date'], "%Y-%m-%d").strftime("%Y %b %d") ) 
             for post in app.db.posts.find( {"title":post_title } )
        ]
       
        return render_template("post.html", post_data=post_meta, post_content=post_content)

        
    @app.route("/admin/posts_list", methods = ['GET', 'POST'])
    def admin_posts_list():

        posts = [
                ( post['title'], datetime.datetime.strptime(post['date'], "%Y-%m-%d").strftime("%b %d") )
                for post in app.db.posts.find({},)
                ]

        return render_template("posts_list.html", posts=posts)

    @app.route("/admin/post/<string:post_title>",  methods=['GET', 'POST'])
    def admin_post_edit(post_title):

        result = app.db.posts.find( {"title":post_title } )

        for post in app.db.posts.find( {"title":post_title }):
             post_content = post['content'].split('\r\n')

        post_meta = [ 
            (post['title'], datetime.datetime.strptime(post['date'], "%Y-%m-%d").strftime("%Y %b %d") ) 
             for post in app.db.posts.find( {"title":post_title } )
        ]
       
        return render_template("post_edit.html", post_data=post_meta, post_content=post_content)


    
    return app

'''
if __name__ == '__main__':
    app = create_app()
    app.run(host="127.0.0.1", port='8000')
'''