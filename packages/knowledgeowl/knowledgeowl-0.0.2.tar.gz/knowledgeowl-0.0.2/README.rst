===============
knowledgeowl
===============
Python implementation of knowledgeowl API

Examples
-----------------

Create connection to knowledge owl::

  import knowledgeowl
  ko = knowledgeowl.KnowledgeOwl('api_key', 'project_id')

List all articles and print their ID and Name::

  resp = ko.list_articles()
  for i in resp['data']:
      print('{name}: {id}'.format(**i))

Get article by article id::

  >>> ko.get_article('58cbd78a32131c852498774d')
  2017-03-20 08:04:57 INFO connectionpool._get_conn Resetting dropped connection: app.knowledgeowl.com
  {u'valid': True, u'data': {u'inherited_roles': None, u'search_phrases': u'', u'internal_title': u'', u'current_version_id': u'xxxxxxxxxxxxxxxxxxxxxxxx', u'application_screens': [u''], u'content_article': None, u'meta_page_title': u'', u'current_version': {u'text': u'updated by ko admin', u'en': {u'text': u'', u'title': u'Test'}, u'title': u'test'}, u'id': u'58cbd78a32131c852498774d', u'auto_save': u'', u'category': u'xxxxxxxxxxxxxxxxxxxxxxxx', u'view_count': None, u'url_hash': u'testapi', u'author': u'xxxxxxxxxxxxxxxxxxxxxxxx', u'ready_versions': None, u'callout': u'none', u'remove_pdf': u'', u'languages': None, u'meta_description': u'', u'current_version_number': 1, u'searchTitle': {u'en': u'Test'}, u'parents': [u'xxxxxxxxxxxxxxxxxxxxxxxx'], u'project_id': u'xxxxxxxxxxxxxxxxxxxxxxxx', u'type': u'article', u'callout_video': u'', u'status': u'published', u'redirect_link': None, u'index': 6, u'toc_title': u'', u'visibility': u'public', u'date_published': {u'usec': 0, u'sec': -68400}, u'reader_roles': u'', u'related_articles': [u''], u'pdf': u'/help/pdfexport/id/58cbd78a32131c852498774d', u'template_article': u'', u'remove_feedback': u'', u'article_link': None, u'tags': u'', u'hide_from_toc': u'', u'callout_expire': 1490619453, u'name': u'Test', u'date_modified': u'03/20/2017 8:57 am EDT', u'prevent_searching': u'', u'date_deleted': None, u'summary': False, u'remove_comments': u'', u'meta_data': None, u'category_view': u'', u'date_created': u'03/17/2017 8:33 am EDT', u'user_teams': u'', u'modified_author': u'xxxxxxxxxxxxxxxxxxxxxxxx'}}

Update article::

  r = ko.update_article('58cbd78a32131c852498774d', index=6).json()



Notes:
-----------------

There are certain fields you shouldn't try to update. Here is the list of fields you can update.::

  >>> knowledgeowl.ARTICLE_KEYS
  ['name', 'visibility', 'status', 'url_hash', 'toc_title', 'category', 'application_screens', 'index', 'category_view', 'prevent_searching', 'hide_from_toc', 'remove_pdf', 'callout', 'callout_expire', 'callout_video', 'reader_roles', 'current_version']
  >>> knowledgeowl.CATEGORY_KEYS
  ['name', 'visibility', 'status', 'url_hash', 'type', 'parent_id', 'toc_title', 'faq_display', 'toc_hide_children', 'description', 'index', 'cat_toggle_override', 'reader_roles', 'hide_from_toc']

