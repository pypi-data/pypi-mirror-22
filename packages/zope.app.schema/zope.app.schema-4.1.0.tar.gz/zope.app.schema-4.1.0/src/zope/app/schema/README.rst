=====================================
 Component-based Vocabulary Registry
=====================================

This package provides a vocabulary registry for zope.schema,
based on the component architecture.

**NOTE:** This functionality has been replaced with
``zope.vocabularyregistry``. These imports continue to work
for backwards compatibility.

It replaces the zope.schema's simple vocabulary registry
when ``zope.app.schema`` package is imported, so it's done
automatically. All we need is provide vocabulary factory
utilities:

  >>> import zope.app.schema
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

Configuration
=============

This package provides configuration that sets security permissions and
factories for the objects provided in ``zope.schema``. The
``zope.security`` package must be installed to use it.

  >>> from zope.configuration import xmlconfig
  >>> _ = xmlconfig.string(r"""
  ... <configure xmlns="http://namespaces.zope.org/zope" i18n_domain="zope">
  ...   <include package="zope.app.schema" />
  ... </configure>
  ... """)
