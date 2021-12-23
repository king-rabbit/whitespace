import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))

    app.db = client.whitespace

    entries = []


    @app.route("/", methods=["GET", "POST"])
    def home():

        entries_with_date = [
                ( entry['title'], entry['content'], datetime.datetime.strptime(entry['date'], "%Y-%m-%d").strftime("%b %d") )
                for entry in app.db.posts.find({},)
                ]

        return render_template("index.html", entries=entries_with_date)



    @app.route("/write_post", methods=['GET', 'POST'])
    def write_post():

        if request.method == "POST":
            entry_title = request.form.get("title")
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")

            print(entry_title)

            app.db.posts.insert_one({"title":entry_title, "content":entry_content, "date":formatted_date})
            

        return render_template("write_post.html") #html파일을 jinja 템플릿으로 넘긴다


    @app.route("/post/<string:post_title>")
    def individual_post(post_title):
        print(post_title)
        result = app.db.posts.find( {"title":post_title } )
        for r in result:
            print(r)

        indv_post = [ 
            (post['title'] , post['content'], datetime.datetime.strptime(post['date'], "%Y-%m-%d") ) 
             for post in app.db.posts.find( {"title":post_title } )
        ]
        print(indv_post)
       
        return render_template("post.html", post_data=indv_post)

    
    return app

'''
if __name__ == '__main__':
    app.run(host="127.0.0.1", port='8000')
''' 