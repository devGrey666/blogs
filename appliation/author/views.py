from flask import Blueprint, render_template, flash, jsonify,request
from application.authors.helper import scrap_Dawn
from application.authors.Tribune import scrap_Tribune
from application.authors.model import Blog,Author
from application.authors.Aljazeera import scrap_Aljazeera
authors = Blueprint('authors', __name__)
@authors.route('/news_blogs/<news_channel>', methods=['GET', 'POST'])
def news_blogs(news_channel):
    value = True;
    try:
        if news_channel == 'Dawn':
            value = scrap_Dawn()
        elif news_channel == 'Aljazeera':
            value = scrap_Aljazeera()
        elif news_channel == 'Tribune':
            value = scrap_Tribune()
    except TypeError as e:
        flash("Error occured", e)
    else:
        if value is not True:
            flash("Something Bad happen here !!!",'danger')
            return render_template('dawn_blogs.html', title="Blogs Site")
        else:
            page = request.args.get('page', 1, type=int)
            blogs = Blog.query.filter_by(blog_news_site=news_channel).order_by(Blog.blog_published_time).paginate(page=page,per_page=1)
            return render_template('dawn_blogs.html', title='Blogs Site', blogs=blogs)

    flash("Sorry!!! There is mo content",'warning')
    return render_template('dawn_blogs.html', title="Blogs Site")
        # if news_channel == 'Dawn':
    #         # value = scrap_Dawn()
    #     value = True
    #     if value is True:
    #         blog = Blog.query.filter_by(blog_news_site='Dawn').all()
    #         blog_content = blog[0].blog_content.split('&')
    #         return render_template('dawn_blogs.html', title='Dawn Blogs', list_articles=blog,blog=blog[0],blog_content=blog_content)
    #     else:
    #         flash("There is no content", 'warning')
    #         return render_template('dawn_blogs.html', title='Dawn Blogs')
    #     # else:
        #     blog = Blog.query.filter_by(blog_id=int(blog_title)).first()
        #     print(blog)
        #     if blog is None:
        #         return "Nothing to show"
        #     else:
        #         title = blog.blog_title
        #         heading = blog.blog_heading
        #         content = blog.blog_content
        #         author = blog.author.author_name
        #         blog = {
        #             'blog_title':title,
        #             'blog_heading': heading,
        #             'blog_content':content,
        #             'blog_author':author
        #         }
        #         return jsonify({"data":blog})
        #     # return render_template('dawn_blogs.html', title='Dawn Blogs', list_articles=blog, blog=blog[0])
    # elif news_channel == 'Aljazeera':
    #     print("hi")
    #     # values = scrap_Aljazeera()
    #     values = True
    #     if values is True:
    #         try:
    #             blog = Blog.query.filter_by(blog_news_site=news_channel).order_by('blog_published_time').all()
    #             blog_content = blog[0].blog_content.split('&')
    #             return render_template('dawn_blogs.html', title='Dawn Blogs', list_articles=blog, blog=blog[0],
    #                                        blog_content=blog_content)
    #         except IndexError as e:
    #             print("Error: Index Error")
    #
    #     else:
    #         flash("There is no content", 'warning')
    #         return render_template('dawn_blogs.html', title='Dawn Blogs')
    # elif news_channel == 'Tribune':
    #     print("hi")
    #     # values = scrap_Tribune()
    #     values = True
    #     if values is True:
    #         try:
    #             blog = Blog.query.filter_by(blog_news_site='Tribune').all()
    #             blog_content = blog[0].blog_content.split('&')
    #             return render_template('dawn_blogs.html', title='Dawn Blogs', list_articles=blog, blog=blog[0],blog_content=blog_content)
    #         except IndexError as e:
    #             print("Error: Index Error")
    #
    #     else:
    #         flash("There is no content", 'warning')
    #         return render_template('dawn_blogs.html', title='Dawn Blogs')
    # flash("Error",'danger')
    # return render_template('home.html')
@authors.route("/author")
def author():
    authors = Author.query.order_by(Author.author_name).all()
    author_names = {}
    i = 1
    while i <= len(authors):
        author_names[i] = {'author_name':authors[i-1].author_name.replace('\n',''),
                           'author_id':authors[i-1].author_id}
        i = i + 1
    return jsonify({'data':author_names,'length':len(authors)})

@authors.route('/author/<int:author_id>')
def author_data(author_id):
    try:
        page = request.args.get('page', 1, type=int)
        blogs = Blog.query.filter_by(author_id=author_id).order_by(Blog.blog_published_time.desc()).paginate(page=page,per_page=1)
    except TypeError as e:
        flash("Error ",'danger')
        return render_template('author_content.html', title=None)
    else:
        if blogs:
            return render_template('author_content.html', title=author_id, blogs=blogs)
        else:
            flash("There is something wrong", 'info')
            return render_template('author_content.html',title=author_id)