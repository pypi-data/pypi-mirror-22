
==========
Markdownme
==========

Markdownme is a text editor component with Markdown syntax support,
simplified file upload and deletion and a history of text changes.
Its file-uploading history-containing nature makes it a better choice
for more complex text entries which are edited by trusted users such
as blog posts, as opposed to short text comments which anyone can post.

Detailed documentation is in the github project repository.

Quick start
-----------

1. Add "markdownme" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'markdownme',
    ]

2. Include the markdownme URLconf in your project urls.py like this::

    url(r'^markdownme/', include('markdownme.urls')),

3. Run `python manage.py migrate` to create the markdownme models.

4. Run `python manage.py collectstatic` to collect markdownme static files.

5. Create your desired model and derive it from 'MarkdownmeEntry' like this::

    class Article(MarkdownmeEntry):

6. Your model now has access to 3 new fields called::

    markdown_text
    parsed_text
    markdown_identifier

7. Include these in your Article admin fields like this::

    fields = ('title', 'date', 'markdown_text', 'markdown_identifier')
    
8. Start the development server and visit http://127.0.0.1:8000/admin/
   to create an article (you'll need the Admin app enabled).

9. Your article text now has a fancy editor and you can also use 'parsed_text'
   to access the HTML resulting from your parsed Markdown text.