Wagtail Atomic Admin
====================
This is an amended version of the Wagtail admin UI that makes it easier for users more easily visualises nested items and corrects a number of minor styling issues. Changes:

 - Much improved UI for nested StreamFields
 - Consistency of UI presentation between inline panels, streamfield panels, multipanels etc.
 - Always visible help text
 - Consistent alignment of titles, fields and help text
 - Consistent alignment of success text, breadcrumb and title
 - Separation of meta data and actions in editor footer
 - Conforms AA to WCAG
 - Styling added to `delete` and `unpublish` actions in dropdown menu

![Screenshot](screenshot.png)

Install
-------

    pip install wagtailatomicadmin

Then add `wagtailatomicadmin` to your installed apps. Make sure to place it *before* `wagtail.wagtailadmin` so Django will give it precedence when searching for files.


