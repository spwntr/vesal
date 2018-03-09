# Vesal

## Introduction

Vesal is an experiment in turning a curriculum into a graph database. Theoretically, a curriculum as a graph can be mapped to any study material or new graph. There also would be benefits to generating tools that crawl across the graph and generate educational content or, if the graph is big enough, new hypotheses and knowledge.

### Design Requirements

1. The project should be browsable and internally linked as flat files and eligible for free web-hosting, similar to a wiki.
1. The browsable files should be hosted in a place where it will remain easy for anyone browsing to identify mistakes and submit corrections or clarifications.
1. The project's flat files should be version-controlled.
1. The database should be able to be constructed from the browsable flat files by a database generating engine (DGE).
  * It would be very nice to be able to host the database on free hosting, but individuals must be able to create it themselves (even if that process takes a very long time).
1. The database should maintain versioning so that when the DGE attempts to update the database, only diffs will be applied to existing databases.
1. It should be clear to the user the exact changes made with each DGE update to the database.
1. All datatypes represented in the database should be easily extended to allow mapping of new content to all individual data elements.
1. The database should be able to easily pull large clusters of dissimilar but related datatypes during queries to facilitate the generation of discrete educational content.
1. The database should be auditable such that flat files with broken internal links are identified by the DGE.
1. The database should be able to import or inherit data elements and connectivity from web ontology language datasets (OWL files).

### Examples of Intended Usage

1. Open access, data management
  * Individuals will browse any version of the flat files as a digital textbook.
  * Individuals will build any study tools on top of the flat files or database they see fit.
2. Open source, data integrity
  * Any individual should be able to contribute data to the flat files.
  * Individuals will identify gaps in the content and fill them through pull requests.
  * Pull requests will be merged by domain experts to maintain the validity of the content.
3. Internal audits, data integrity
  * When generating the flat files that will be turned into the database, a user should be able to get instant feedback about the content and format of their contribution such that all relationships are defined appropriately.
  * The user should be notified if their contribution introduces a broken or improperly defined link or relationship.
4. Question generation engine, study material
  * The database should be structured in a way that allows for question generation engine (QGE) to use templated queries to create a nearly infinite number of questions that can be used to learn the content of and relationships between data elements.
  * This may require additional engines as the database gets larger to allow for the synthesis of many relationships and content to contextualize a question.
  * For instance, a "boards style" question stem should generate:
    * A prototypical patient with risk factors
    * Prototypical laboratory values
    * Prototypical exam findings
    * Prototypical imaging and study findings
  * And a "boards style" set of answers should generate:
    * The correct answer and explanation for why it is correct.
    * A series of close but not correct answers
    * Explanations for why each incorrect answer is incorrect, or how to modify the question to make an incorrect answer the correct answer
5. Build upon established projects, data management
  * Use the [Foundational Model of Anatomy (FMA)](http://si.washington.edu/projects/fma) to establish data elements, data types, and structural relationships before adding functional and pathological information.

## Goals (January - March 2018)

#### Major

Develop a proof-of-concept for a structural anatomy dataset as a graph curriculum and build a simple question generating bot for it.

#### Minor

Generate the graph from a series of flat files that can be browsed through GitHub similar to an online textbook.

## Why?

The Internet and open-access sources like [Wikipedia](www.wikipedia.com) have increased access to knowledge and attempted to organize it. However, for more highly specialized training, details are often less organized and digestible. We see this as a supplement to educational resources that already exist, but the use of a graph curriculum as part of a massive open online course (MOOC) is only limited by the size of the graph.

## Stack (tentative)

* python
* neo4j

## Can I help?

Yes! We intend for Vesal to be an open-access, open-sourced structural anatomy curriculum for anyone and everyone. The minor goal listed above is for the explicit purpose of making it easy to navigate and contribute to by managing the graph through GitHub (fork, modify, submit pull request, merge, profit).

#### How can I help?

At the beginning, it might be hard to help as we stumble to find the best way to build the graph from flat json's. We will try to develop a 'Getting Started' guide here as we start to get things coherent.

## Getting Started

1. Will update as we go
