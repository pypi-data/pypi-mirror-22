.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.behavior.internalnumber
==============================================================================

This product adds a plone behavior for dexterity content.
The behavior adds a text field containing an internal number.

Features
--------

- Optional uniqueness validation
- Optional default value
- Inclusion in searchable text
- Global or type by type configuration
- A configuration page can manage globally or type by type:

  * a uniqueness option
  * an incremented number
  * a default value tal expression

Usage
-----

In the configuration panel, go to dexterity types.
Click on the type you want extend with the internal number field.
Go to the behavior tab.
Select "Internal number field" behavior.

If you want the internal number be searched in searchable text, you can also select
the "Dynamic SearchableText indexer behavior"

Translations
------------

This product has been translated into

- French (thanks the author)


Installation
------------

Install collective.behavior.internalnumber by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.behavior.internalnumber


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.behavior.internalnumber/issues
- Source Code: https://github.com/collective/collective.behavior.internalnumber
- Documentation: https://docs.plone.org/foo/bar


License
-------

The project is licensed under the GPLv2.
