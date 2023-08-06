# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Dataset Json Generator. An Json generator that describes EDRN dataset statistics using dataset webservices.
'''

from Acquisition import aq_inner
from five import grok
from interfaces import IJsonGenerator
from edrn.summarizer import _
from summarizergenerator import ISummarizerGenerator
from rdflib.term import URIRef
from rdflib.parser import URLInputSource
from rdflib import ConjunctiveGraph
from utils import validateAccessibleURL
from zope import schema
import jsonlib


_organPredicateURI      = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#organ')

class IDatasetSummarizerGenerator(ISummarizerGenerator):
    '''Dataset JSON Statistics Generator.'''
    rdfDataSource = schema.TextLine(
        title=_(u'Datasets Web Service URL'),
        description=_(u'The Uniform Resource Locator to the DMCC Datasets web service.'),
        required=True,
        constraint=validateAccessibleURL,
    )

class DatasetJsonGenerator(grok.Adapter):
    '''A Json generator that produces statements about EDRN's dataset statistics using the DMCC web service.'''
    def addGraphToStatements(self, graph, statements):
        u'''Add the statements in the RDF ``graph`` to the ``statements`` dict.'''
        for s, p, o in graph:
            if s not in statements:
                statements[s] = {}
            predicates = statements[s]
            if p not in predicates:
                predicates[p] = []
            predicates[p].append(o)

    def getRDFStatements(self):
        u'''Parse the main and additional RDF data sources and return a dict {uri → {predicate → [objects]}}'''
        context = aq_inner(self.context)
        statements = {}
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(context.rdfDataSource))
        self.addGraphToStatements(graph, statements)
        return statements

    grok.provides(IJsonGenerator)
    grok.context(IDatasetSummarizerGenerator)
    def generateJson(self):
        organDatasetCount = {}
        statements = self.getRDFStatements()

        for uri, predicates in statements.items():
            organ = predicates[_organPredicateURI][0].rsplit('/', 1)[-1]

            if organ in organDatasetCount:
                organDatasetCount[organ] += 1
            else:
                organDatasetCount[organ] = 1

        # C'est tout.
        return jsonlib.write(organDatasetCount)
