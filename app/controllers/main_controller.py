from models.user import User
from models.post import Post

class MainController:
    def get_posts(self):
        posts = []
        for i in range(1, 4):
            post = Post(i, f"Title {i}", f"Content {i}")
            posts.append(post)
        return posts

    def get_user(self, user_id):
        user = User(user_id, f"User {user_id}")
        return user

    def get_post(self, post_id):
        post = Post(post_id, f"Title {post_id}", f"Content {post_id}")
        return post