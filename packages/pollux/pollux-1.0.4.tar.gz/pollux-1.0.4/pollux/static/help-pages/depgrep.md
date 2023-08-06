# Querying dependencies

> pollux provides a purpose-built syntax for querying dependencies, called depgrep. It is modern, expressive, powerful and fast. This document describes depgrep's syntax.

## The basics

Like many other linguistic query languages, using depgrep involves specifying *nodes* and *relations*. Nodes match tokens and their various properties. Relations specify how two nodes relate to one another.

    w/fr?iend/ -> p"DT"

The query above specifies two nodes and one relation. In natural language, the query means *Find words matching "friend" or "fiend", which have a dependent determiner*. Very important to remember is that **it is always the leftmost token that will be returned by the query.**

## Nodes

Above, we saw two nodes: `w/fr?iend/` and `p"DT"`. Each is comprised of three meaningful parts: an *attribute* specifier, a set of *boundaries*, and an *expression*.

### Attribute specifier

The attribute specifier tells depgrep which attribute of a token we want to match. It can be:

| Specifier  |  Meaning |
|---|---|
| w  | Word  |
| l  | Lemma  |
| p  | POS tag  |
| x  | XPOS tag |
| f  | Function |
| n  | NER  |
| i  | Index  |
| s  | Sentence index  |

### Boundaries

Node boundaries tell depgrep where a search expression starts and ends, and how it should be interpreted. As in the earlier example, there are two kinds of boundaries. Forward slashes tell depgrep to treat the expression as a [Python regular expression](). Double quotation marks tell depgrep to match contents literally.

### Expressions

Unfortunately, it is beyond the scope of this guide to teach regular expressions. If you need practice, try an [online regular expression engine]().

When using literal expressions, you can use commas to specify a list of possible strings to match. `l"big,bigger,biggest"` will match, well, exactly what you'd expect. The equivalent using a regular expression would be `l/^big($ger|gest)$/`.

## Relations

depgrep can interpret a number of possible relations:

| Relation | Meaning
|-----|------|
| A -> B    | A governs B     |
| A <- B   |  A is a dependent of B   |
|     |      |
|     |      |
|     |      |
|     |      |
|     |      |
|     |      |
|     |      |
|     |      |
|     |      |


## Bracketing

Brackets allow you to group your query into smaller parts, just as you might with an algorithm.

Therefore, a `Dependencies` query like:

    f/nsubj/ -> (f/amod/ & w/^[abc]/) <- f"root"

will match nominal subjects with adjectival modifiers beginning with a, b, or c, when the governor is the root of the parse tree.