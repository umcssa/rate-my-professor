"""Insta485 model (database) API."""
import os
import hashlib
import uuid
import shutil
import tempfile
import sqlite3
import flask
import arrow
import insta485


def dict_factory(cursor, row):
    """
    Convert database row objects to a dictionary.

    This is useful for building dictionaries which
    are then used to render a template. Note that
    this would be inefficient for large queries.
    """
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output


def get_db():
    """Open a new database connection."""
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(
            insta485.app.config['DATABASE_FILENAME'])
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@insta485.app.teardown_appcontext
def close_db(error):
    # pylint: disable=unused-argument
    """Close the database at the end of a request."""
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()


def get_password_db_string(password):
    """Covert password to database string."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def get_password_with_salt(password, salt):
    """Covert password to database string with salt."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def get_password_salt(password):
    """Get the salt of password."""
    password = str(password)
    salt = password[password.find('$') + 1:]
    salt = salt[:salt.find('$')]
    return salt


def check_password(username, password):
    """Check username and password match."""
    cur = get_db().execute(
        "SELECT password FROM users WHERE username = '{}'".format(
            username))
    result = cur.fetchone()
    cur.close()
    db_password = str(result['password'])
    salt = get_password_salt(db_password)
    password_db_string = get_password_with_salt(password, salt)
    if not result:
        return 0
    return db_password == password_db_string


def get_user_info(username, logname):
    """Get info of username."""
    user_info = {}
    user_info['username'] = username
    user_info['user_img_url'] = '/uploads/' + get_user_filename(
        username)
    user_info['logname_follows_username'] = is_following(logname,
                                                         username)
    return user_info


def get_user_info_verbose(username, logname):
    """Get verbose info of username."""
    cur = get_db().execute(
        "SELECT username, fullname FROM users WHERE username = '{}'".format(
            username))
    user_info_verbose = cur.fetchone()
    cur = get_db().execute(
        "SELECT COUNT(*) FROM following WHERE username2 = '{}'".format(
            username))
    user_info_verbose['followers'] = cur.fetchone()['COUNT(*)']
    cur = get_db().execute(
        "SELECT COUNT(*) FROM following WHERE username1 = '{}'".format(
            username))
    user_info_verbose['following'] = cur.fetchone()['COUNT(*)']
    cur.close()
    user_info_verbose['logname_follows_username'] = is_following(
        logname, username)
    user_info_verbose['posts'] = get_user_posts(username, logname)
    user_info_verbose['total_posts'] = len(user_info_verbose['posts'])
    return user_info_verbose


def is_following(username1, username2):
    """Check if username1 is following username2."""
    cur = get_db().execute(
        "SELECT COUNT(*) FROM following WHERE username1 = '{}' "
        "AND username2 = '{}'".format(
            username1, username2))
    count = cur.fetchone()['COUNT(*)']
    cur.close()
    return int(count) > 0


def get_followers(username, logname):
    """Get the followers of username."""
    cur = get_db().execute(
        "SELECT username1 FROM following WHERE username2 = '{}'".format(
            username))
    followers = cur.fetchall()
    followers_info = []
    for follower in followers:
        followers_info.append(
            get_user_info(follower['username1'], logname))
    return followers_info


def get_following(username, logname):
    """Get the users username is following."""
    cur = get_db().execute("SELECT username AS username2 FROM users "
                           "WHERE username = '{}' UNION "
                           "SELECT username2 FROM following "
                           "WHERE username1 = '{}' INTERSECT "
                           "SELECT username2 FROM following "
                           "WHERE username1 = '{}'".format(logname,
                                                           logname,
                                                           username))
    following = cur.fetchall()
    following_info = []
    for follow in following:
        following_info.append(
            get_user_info(follow['username2'], logname))
    return following_info


def get_posts(logname):
    """Get all the posts that can be viewed by logname in index."""
    cur = get_db().execute(
        "SELECT posts.postid, posts.created FROM posts "
        "WHERE owner = '{}' UNION SELECT posts.postid, posts.created "
        "FROM posts INNER JOIN following ON "
        "following.username2 = posts.owner WHERE username1 = '{}' "
        "ORDER BY created DESC, posts.postid DESC".format(
            logname, logname))
    postids = cur.fetchall()
    cur.close()
    posts = []
    for postid in postids:
        posts.append(get_post(postid['postid'], logname))
    return posts


def get_user_posts(username, logname):
    """Get the posts of username."""
    cur = get_db().execute(
        "SELECT postid, created FROM posts WHERE owner = '{}' "
        "ORDER BY created DESC, postid DESC".format(
            username))
    postids = cur.fetchall()
    cur.close()
    posts = []
    for postid in postids:
        posts.append(get_post(postid['postid'], logname))
    return posts


def get_post(postid, logname):
    """Get info of post with postid."""
    cur = get_db().execute(
        "SELECT * FROM posts WHERE postid = {}".format(postid))
    post = cur.fetchone()
    post['owner_img_url'] = '/uploads/' + get_user_filename(
        post['owner'])
    post['img_url'] = '/uploads/' + post.pop('filename')
    post['timestamp'] = arrow.get(post['created']).humanize()
    post['likes'] = get_post_like(post['postid'])
    post['comments'] = get_comments(post['postid'])
    cur = get_db().execute(
        "SELECT COUNT(*) FROM likes WHERE owner = '{}' "
        "AND postid = {}".format(
            logname, post['postid']))
    post['liked'] = cur.fetchone()['COUNT(*)'] > 0
    cur.close()
    return post


def get_post_like(postid):
    """Get the number of likes of post."""
    cur = get_db().execute(
        "SELECT COUNT(*) FROM likes WHERE postid = {}".format(postid))
    count = cur.fetchone()['COUNT(*)']
    cur.close()
    return count


def get_user_filename(username):
    """Get the filename of usernmae."""
    cur = get_db().execute(
        "SELECT filename FROM users WHERE username = '{}'".format(
            username))
    filename = cur.fetchone()['filename']
    cur.close()
    return filename


def get_comments(postid):
    """Get the comments of a post."""
    cur = get_db().execute(
        "SELECT commentid, owner, text, created FROM comments "
        "WHERE postid = {} ORDER BY created ASC".format(
            postid))
    comments = cur.fetchall()
    cur.close()
    return comments


def get_not_following(logname):
    """Get the users logname is not following."""
    cur = get_db().execute(
        "SELECT username, filename FROM users "
        "WHERE username != '{}' AND NOT EXISTS "
        "(SELECT * FROM following WHERE username1 = '{}' "
        "AND username2 = username)".format(
            logname, logname))
    not_followings = cur.fetchall()
    cur.close()
    for not_following in not_followings:
        not_following[
            'user_img_url'] = '/uploads/' + \
                              not_following.pop('filename')
    return not_followings


def delete_user(username):
    """Delete username from database."""
    posts = get_user_posts(username, username)
    for post in posts:
        delete_post(post['postid'])
    user_img = get_user_filename(username)
    os.remove(os.path.join(
        insta485.app.config["UPLOAD_FOLDER"], user_img))
    cur = get_db().execute(
        "DELETE FROM users WHERE username = '{}'".format(username))
    cur.close()


def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


def save_file():
    """Save a file to database."""
    # Save POST request's file object to a temp file
    dummy, temp_filename = tempfile.mkstemp()
    file = flask.request.files["file"]
    file.save(temp_filename)

    # Compute filename
    hash_txt = sha256sum(temp_filename)
    dummy, suffix = os.path.splitext(file.filename)
    hash_filename_basename = hash_txt + suffix
    hash_filename = os.path.join(
        insta485.app.config["UPLOAD_FOLDER"],
        hash_filename_basename
    )

    # Move temp file to permanent location
    shutil.move(temp_filename, hash_filename)
    insta485.app.logger.debug("Saved %s", hash_filename_basename)
    return hash_filename_basename


def create_user(user):
    """Create a user."""
    cur = get_db().execute(
        "INSERT INTO users (username, fullname, email, "
        "filename, password) "
        "VALUES ('{}','{}','{}','{}','{}')".format(
            user['username'], user['fullname'], user['email'],
            user['filename'], user['password']))
    cur.close()


def get_user_info_edit(username):
    """Get info of user for edit."""
    cur = get_db().execute(
        "SELECT * FROM users WHERE username = '{}'".format(
            username))
    user_info_edit = cur.fetchone()
    cur.close()
    user_info_edit['filename'] = '/uploads/' + user_info_edit[
        'filename']
    return user_info_edit


def update_user(user):
    """Update user info."""
    if 'filename' in user:
        cur = get_db().execute(
            "SELECT filename FROM users "
            "WHERE username = '{}'".format(
                user['username']))
        old_filename = cur.fetchone()['filename']
        cur = get_db().execute(
            "UPDATE users SET fullname = '{}', email = '{}', "
            "filename = '{}' WHERE username = '{}'".format(
                user['fullname'], user['email'], user['filename'],
                user['username']))
        os.remove(os.path.join(
            insta485.app.config["UPLOAD_FOLDER"], old_filename
        ))
    else:
        cur = get_db().execute(
            "UPDATE users SET fullname = '{}', email = '{}' "
            "WHERE username = '{}'".format(
                user['fullname'], user['email'],
                user['username']))
    cur.close()


def change_password(user):
    """Change the password of user."""
    if user['new_password1'] != user['new_password2']:
        return 401
    cur = get_db().execute(
        "SELECT password FROM users WHERE username = '{}'".format(
            user['username']))
    db_password = cur.fetchone()['password']
    if get_password_with_salt(
            user['password'],
            get_password_salt(db_password)) != db_password:
        cur.close()
        return 403
    new_password = get_password_db_string(user['new_password1'])
    cur = get_db().execute(
        "UPDATE users SET password = '{}' "
        "WHERE username = '{}'".format(
            new_password, user['username']))
    cur.close()
    return 1


def like_post(logname, postid):
    """Logname likes a post."""
    cur = get_db().execute(
        "INSERT INTO likes (owner, postid) "
        "VALUES ('{}',{})".format(
            logname, postid))
    cur.close()


def unlike_post(logname, postid):
    """Logname unlikes a post."""
    cur = get_db().execute(
        "DELETE FROM likes WHERE owner = '{}' "
        "AND postid = {}".format(
            logname, postid))
    cur.close()


def add_comment(logname, postid, text):
    """Logname adds a comment."""
    cur = get_db().execute(
        "INSERT INTO comments (owner, postid, text) "
        "VALUES ('{}',{},'{}')".format(
            logname, postid, text))
    cur.close()


def follow_user(logname, username):
    """Logname follows username."""
    cur = get_db().execute(
        "INSERT INTO following (username1, username2) "
        "VALUES ('{}','{}')".format(
            logname, username))
    cur.close()


def unfollow_user(logname, username):
    """Logname unfollows username."""
    cur = get_db().execute(
        "DELETE FROM following WHERE username1 = '{}' "
        "AND username2 = '{}'".format(
            logname, username))
    cur.close()


def create_post(logname, filename):
    """Create a post."""
    cur = get_db().execute(
        "INSERT INTO posts (filename, owner) "
        "VALUES ('{}','{}')".format(
            filename, logname))
    cur.close()


def delete_comment(commentid):
    """Delete a comment."""
    cur = get_db().execute(
        "DELETE FROM comments WHERE commentid = {}".format(commentid))
    cur.close()


def delete_post(postid):
    """Delete a post."""
    cur = get_db().execute(
        "SELECT filename FROM posts WHERE postid = {}".format(postid))
    filenames = cur.fetchall()
    for filename in filenames:
        os.remove(os.path.join(
            insta485.app.config["UPLOAD_FOLDER"], filename['filename']
        ))
    cur = get_db().execute(
        "DELETE FROM posts WHERE postid = {}".format(postid))
    cur.close()


def check_login():
    """Check user login."""
    if insta485.app.config['SESSION_COOKIE_NAME'] \
            not in flask.session:
        if flask.request.method == 'POST':
            return flask.abort(403)
        return flask.redirect(flask.url_for('login'))
    return 'login'
