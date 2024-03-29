from flask import render_template, request, Blueprint
from companyblog.models import Blog_post

core = Blueprint('core',
                 __name__,
                 )


@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = Blog_post.query.order_by(Blog_post.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', blog_posts=blog_posts)



@core.route('/info')
def info():
    return render_template('info.html')
