pollux: help
============

> Here, you can find out how to use pollux, and learn a little more about how its components work under the hood.

<!-- MarkdownTOC -->

- [Getting started](#getting-started)
- [Available datasets](#available-datasets)
- [Uploading and parsing](#uploading-and-parsing)
    - [Multimodal data](#multimodal-data)
    - [Parsing](#parsing)
- [Exploring a corpus](#exploring-a-corpus)
    - [Sentences/concordance view](#sentencesconcordance-view)
    - [Table view](#table-view)
    - [Pivot view](#pivot-view)
- [Searching and filtering](#searching-and-filtering)
    - [Trees](#trees)
    - [Dependencies](#dependencies)
    - [CQL](#cql)
    - [Searching by metadata or feature](#searching-by-metadata-or-feature)
    - [Previous queries](#previous-queries)
- [When things go wrong](#when-things-go-wrong)
- [Anything else?](#anything-else)

<!-- /MarkdownTOC -->

<a name="getting-started"></a>
Getting started
----------------

You can access pollux in two ways. First, you can simply [visit its website]() and login (if necessary). This will give you access to a number of free corpora, and give you the option of uploading your own. Second, pollux can be downloaded and used locally. This might be a better option for those who:

* Do not have university credentials
* Want to be able to work offline
* Have very large amounts of data
* Have very sensitive data
* Want to modify the source code
* Want to run pollux on a server

If this might be you, visit the [installation instructions]() to learn more. Once you've got the tool up and running, the remainder of this guide will help you use it.

<a name="available-datasets"></a>
Available datasets
--------------------

pollux has some ready-made datasets, most of which are completely open source. If you want to see how the tool works, you might like to start by opening one of these. For the remainder of this guide, we will rely on one of these corpora.

<a name="uploading-and-parsing"></a>
Uploading and parsing
------------------------

Many users are interested in uploading their own texts. This is part of what pollux is designed to do. Below the table of available corpora is an `Upload` button, which will ask you to provide some information about a new dataset. Provide a useful project name and summary, and select a language for your project. 

Please note that pollux relies on various other tools for the linguistic annotation of texts. Therefore, support for other languages is dependent on the availability of parsers. If there is a parser or language you need support for, please [file an issue]() about it.

pollux is happy to parse plain text files without any particular pre-processing. Standard language varieties will of course lead to more accurate parsing. Any normalisation you can do to the data before uploading and parsing it could help a lot.

#### Corpus metadata

One key feature of pollux is that it can accept text containing arbitrary metadata. Metadata is ignored during parsing, but reintroduced later, so that it can be searched, filtered, and visualised.

To add metadata to your corpus, there are two possibilities. First, you can select the `Speakers` option, and provide data with speaker names beginning each line:

    MATTHIAS: You'll be the king for a day!
    FRIEND2: I can only hope so.
    NARRATOR: Back then, I was young enough to believe him.

If you have other kinds of metadata, however, you're better off providing it as `XML` tags at the end sentences:

    You'll be the king for a day! <metadata speaker="MATTHIAS" move="flattery">
    I can only hope so. <metadata move="agree" speaker="FRIEND2">
    Back then, I was young enough to believe him <metadata scene="5" speaker="NARRATOR">

If you already have files that are already in [CONLL-U]() format, you can also upload these, forgoing the parsing process. Some other formats are also accepted. TCF files and CoreNLP `json` output will soon be supported.

<a name="multimodal-data"></a>
### Multimodal data

People have often criticised corpus linguistics for removing language from its original context. pollux hopes to address this problem by supporting multimodal data types.

#### YouTube

pollux can work with any YouTube video for which closed captions are available. Simply provide the ID or URL of a YouTube clip, and the tool will:

1. Extract the text and timestamps from the captions
2. Parse the text, and store the timestamps for each sentence
3. Hyperlink search results to their location in the video

This feature is experimental, and is currently bound by the standardness of closed captions. If sentence boundaries are not marked with full-stops, for example, the tool might run into problems.

#### Films and subtitles

pollux also supports analysis of films with SRT-format subtitle files. Here, the workflow is the same as for YouTube videos. This feature can only be used when pollux is run locally, however: pollux's servers can't cope with uploading of films. A workaround would be to upload the video to YouTube, caption it, and provide pollux with its ID.

#### PDFs

> Support for PDFs and images containing text is forthcoming. Watch this space!

<a name="parsing"></a>
### Parsing

Parsing can take a long time. Be patient!

<a name="exploring-a-corpus"></a>
Exploring a corpus
-----------------------

When you select a corpus from the list on the main page, or when you successfully upload a text, you are taken to the `Explore` page. Almost everything interesting takes place here:

* Searching
* Editing results
* Generating statistics
* Visualising statistics
* Viewing parse trees

#### Browsing corpora

Before you search, you are able to browse and manipulate the entire contents of the corpus. You can do this via tabs:

1. `Sentences`, which shows each sentence, alongside its metadata
2. `Table`, which displays frequency counts
3. `Pivot`, which provides an interactive pivot table
4. `Trees`, which visualises the constituency and dependncy parses of each sentence
3. `Chart`, which visualises the frequencies in `Table`

Each is explained below.

<a name="sentencesconcordance-view"></a>
### Sentences/concordance view

The default viewer is `Sentences`, which provides a table of sentences and their metadata. You can click any sentence to view its graphical representations in the `Tree` view. You can also change the token format: if you select `Word`, `Lemma` and `Function`, the sentence will be displayed as a series of slash-separated units:

    the/the/det biggest/big/amod guys/guy/nsubj ...

You can also use the `Highlight` menu to colour the tokens of the sentence according to various properties, such as their POS tags, dependency functions, or named entity information.

If your data is multimodal, you can also view the original text (i.e. the video at the correct timestamp, or the PDF at the correct co-ordinates).

The sentences can be searched via a search bar above the table, though this is much less powerful than the main query engine. 

Buttons are available for paginating and unpaginating, for exporting, and for hiding columns in the view.

<a name="table-view"></a>
### Table view

The second view is a spreadsheet-like display of frequency counts. If you have not yet searched the data, by default, POS tags are displayed, sorted by total frequency. Using the controls above the table, however, you can modify the data below in a number of ways:

1. Choose which metadata values should be used as the index/subcorpora
2. Choose the token format (as in the `Concordance` view, above)
3. Calculate relative frequency or keyness of the selected data, using any search result as the denominator value
4. Sort the results by name, frequency, or by trajectory by subcorpus (using a linear regression algorithm to draw trend lines, and sort by their slopes)

You can also manually select subcorpora via the checkboxes in the table, and merge or delete them. As with the `Concordance` view, you can manually search or sort the columns, or export the result to a number of formats.

<a name="pivot-view"></a>
### Pivot view

The third tab allows you to create *pivot tables* by dragging and dropping token features and metadata values into the rows and columns of the chart. Also embedded within this interface are basic tools for charting, calculating relative frequencies, and so on.

#### Tree view

The `Tree` view presents a graphical representation of a single sentence. Using the navigation bar, you can browse other sentences, switch between constituency and dependency reprsentations, and export the figure. You can also jump back to the `Sentences/Concordance` view, with the current sentence highlighted.

The tree itself is an SVG. It can be dragged and zoomed.

#### Chart view

`Chart` view provides an interface for plotting whatever is currently shown in the `Table` view. You can select kinds of chart, axis labels, and so forth. If your index/subcorpora are numerical, additional options open up.

<a name="searching-and-filtering"></a>
Searching and filtering
-------------------------

Perhaps the most powerful thing about pollux is its ability to quickly search datasets for relevant features. A number of search languages are supported.

<a name="trees"></a>
### Trees

When querying `Trees`, you are searching the constituency parse of the sentence using a Python implementation of Tgrep2. Documentation for this query language is provided [here]().

<a name="dependencies"></a>
### Dependencies

The `Dependencies` option allows you to write queries using a purpose-built query language called `depgrep`. It is similar to Tgrep2, but has a number of important differences. An overview of the syntax is available [here]().

<a name="cql"></a>
### CQL

`CQL` allows the user to search using a subset of the CQL corpus query language.

<a name="searching-by-metadata-or-feature"></a>
### Searching by metadata or feature

The final kinds of search are simpler. The `metadata` search type will prompt the user for a specific metadata field. If your corpus is annotated with speaker names, for example, you can restrict to a given speaker here. The `features` search type allows you to specify a single token attribute to search for.

<a name="previous-queries"></a>
### Previous queries

Whenever you search your data, a few things change on screen:

* The results appear in the viewing space
* `Sentences` view becomes `Concordance` view
* The `Search` button becomes a `Filter` button
* Your query is added to the pane on the left and selected (i.e. highlighted)

Whichever query is highlighted on the left is treated as the dataset for the next search. So, by default, your second search will further refine, or filter, the first. If you want to start from scratch, or view the corpus data unfiltered, click on the `Corpus` button, with the globe icon.

Subsequent searches are indented in the pane on the left, and have a different icon. You can, of course, further filter these results. The only difference is that only your most recent edit is available for refining.

You can clear all previous queries if need be.

<a name="when-things-go-wrong"></a>
When things go wrong
----------------------

pollux provides an interface for a lot of things, including the uploading and searching texts, and editing and visualising search results. To do all this, it pulls together a number of different tools, including parsers, search query languages and data visualisation tools. This means, in short, that things can break. Fortunately, like the majority of the tools it relies upon, pollux is open-source, meaning that you are free to download or modify its source code as you wish. If you know how to code (or want to learn!), it also means that you can contribute to the project by fixing bugs or adding features yourself.

If you find a bug, you can report it [here](). Reporting bugs publicly allows other users to find relevant help when they encounter the same problem. For the developer, issue tracking helps determine which parts of the code need fixing, and how badly. This leads to better software for all.

<a name="anything-else"></a>
Anything else?
----------------

If your question wasn't answered here, please [file an issue]() requesting further documentation.