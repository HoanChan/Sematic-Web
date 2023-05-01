from flask import Flask, render_template
from controllers.main_controller import MainController

app = Flask(__name__, template_folder="views", static_folder="public")

# Khởi tạo controller
main_controller = MainController()

# Route mặc định
@app.route("/")
def index():
    posts = main_controller.get_posts()
    return render_template("index.html")#, posts=posts)

# Route hiển thị thông tin user
@app.route("/users/<int:user_id>")
def user(user_id):
    user = main_controller.get_user(user_id)
    return render_template("user.html", user=user)

# Route hiển thị thông tin post
@app.route("/posts/<int:post_id>")
def post(post_id):
    post = main_controller.get_post(post_id)
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)