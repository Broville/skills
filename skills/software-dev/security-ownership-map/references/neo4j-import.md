# Neo4j Import Guide

This guide explains how to load the ownership map CSV exports into Neo4j for interactive graph exploration and visualization.

## Prerequisites

- Neo4j 4.x+ running locally or accessible remotely
- The ownership map output directory containing CSV files

## Setup Constraints

```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (f:File) REQUIRE f.path IS UNIQUE;
```

## Import Commands

From the Neo4j Browser or `cypher-shell`, run from the output directory:

```cypher
// Load people nodes
LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (p:Person {id: row.person})
SET p.commits = toInteger(row.commits),
    p.sensitive_touches = toInteger(row.sensitive_touches),
    p.primary_tz_offset = row.primary_tz_offset;

// Load file nodes
LOAD CSV WITH HEADERS FROM 'file:///files.csv' AS row
MERGE (f:File {path: row.path})
SET f.bus_factor = toInteger(row.bus_factor),
    f.tags = row.tags;

// Load ownership edges
LOAD CSV WITH HEADERS FROM 'file:///edges.csv' AS row
MATCH (p:Person {id: row.person}), (f:File {path: row.path})
MERGE (p)-[:TOUCHES {commits: toInteger(row.commits)}]->(f);

// Load co-change edges (optional)
LOAD CSV WITH HEADERS FROM 'file:///cochange_edges.csv' AS row
MATCH (f1:File {path: row.file_a}), (f2:File {path: row.file_b})
MERGE (f1)-[:CO_CHANGES_WITH {jaccard: toFloat(row.jaccard)}]->(f2);
```

## Visualization Tips

- Use Neo4j Bloom or the Browser visualization to explore the ownership graph
- Color nodes by `sensitive_touches` (people) or `bus_factor` (files)
- Filter edges by `jaccard` weight to find strong co-change clusters
- Use the GDS library for betweenness centrality to find hidden owners

## Example Queries

```cypher
// Find files with bus factor 1 that are security-sensitive
MATCH (f:File)
WHERE f.bus_factor = 1 AND f.tags CONTAINS 'auth'
RETURN f.path, f.tags;

// Find people who touch the most sensitive code
MATCH (p:Person)-[t:TOUCHES]->(f:File)
WHERE f.tags IS NOT NULL
RETURN p.id, sum(t.commits) AS sensitive_commits
ORDER BY sensitive_commits DESC LIMIT 10;

// Find co-change clusters
MATCH (f1:File)-[c:CO_CHANGES_WITH]->(f2:File)
WHERE c.jaccard > 0.1
RETURN f1.path, f2.path, c.jaccard
ORDER BY c.jaccard DESC LIMIT 20;
```