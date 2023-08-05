This package provides a component architecture based vocabulary registry.


Component-based Vocabulary Registry
===================================

This package provides a vocabulary registry for zope.schema,
based on the component architecture.

It replaces the zope.schema's simple vocabulary registry
when ``zope.app.schema`` package is imported, so it's done
automatically. All we need is provide vocabulary factory
utilities:

  >>> from zope.component import provideUtility
  >>> from zope.schema.interfaces import IVocabularyFactory
  >>> from zope.schema.vocabulary import SimpleTerm
  >>> from zope.schema.vocabulary import SimpleVocabulary

  >>> def SomeVocabulary(context=None):
  ...     terms = [SimpleTerm(1), SimpleTerm(2)]
  ...     return SimpleVocabulary(terms)

  >>> provideUtility(SomeVocabulary, IVocabularyFactory,
  ...                name='SomeVocabulary')

Now we can get the vocabulary using standard zope.schema
way:

  >>> from zope.schema.vocabulary import getVocabularyRegistry
  >>> vr = getVocabularyRegistry()
  >>> voc = vr.get(None, 'SomeVocabulary')
  >>> [term.value for term in voc]
  [1, 2]

=======
CHANGES
=======

4.0.1 (2017-05-10)
------------------

- Packaging: Add the Python version and implementation classifiers.


4.0.0 (2017-04-17)
------------------

- Support for Python 3.5, 3.6 and PyPy has been added.

- Added support for tox.

- Drop dependency on ``zope.app.testing``, since it was not needed.


3.6.0 (2017-04-17)
------------------

- Package modernization including manifest.


3.5.0 (2008-12-16)
------------------

- Remove deprecated ``vocabulary`` directive.
- Add test for component-based vocabulary registry.


3.4.0 (2007-10-27)
------------------

- Initial release independent of the main Zope tree.


