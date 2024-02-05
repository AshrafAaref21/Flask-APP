from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from companyblog import db
from companyblog.models import User, Blog_post
from companyblog.users.forms import RegisterationForm, LoginForm, UpdateUserForm
from companyblog.users.picture_hundler import add_profile_pic


users = Blueprint('users', __name__)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/register', methods=['POST','GET'])
def register():
    form = RegisterationForm()

    if form.validate_on_submit():

        user = User(
            email= form.email.data,
            user_name=form.user_name.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Thanks For Registration')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)



@users.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                flash('Successfully logged in')

                next = request.args.get('next')
                if next == None or not next[0]=='/':
                    next = url_for('core.index')
                print(next)
                return redirect(next)
        
    return render_template('login.html',form=form)




@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.user_name
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User profile updated')
        
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
    
    profile_image = url_for('static', filename= 'profile_pics/'+current_user.profile_image)

    return render_template('account.html', form=form, profile_image=profile_image)



@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(user_name=username).first_or_404()
    blog_posts = Blog_post.query.filter_by(author=user).order_by(Blog_post.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts, user=user)




        


