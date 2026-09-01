---
name: helloao-bible-api
description: Retrieve licensed Bible resources from the Free Use Bible API.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Bible, API, translations, commentaries, cross-references]
    related_skills: [scripture-study-method, bible-study-facilitation, bible-study-app-development]
trigger:
  - When an agent needs Bible text, public-domain commentary, or cross-reference data from bible.helloao.org.
  - When a Bible-study workflow needs to verify a translation ID or retrieve a complete chapter.
inputs:
  - name: request
    description: Resource type and identifiers such as translation, commentary, dataset, book, and chapter.
    required: true
outputs:
  - name: cited-json-resource
    description: Validated JSON data with source and license metadata retained.
---

# HelloAO Bible API

## Description

Use this skill to retrieve Bible translations, public-domain commentaries, and datasets from the Free Use Bible API at `https://bible.helloao.org`. The service is public and needs no authentication, but users must still verify each resource's license and attribution before redistributing or storing it in a shared product.

The API supplies text, commentary, and datasets; it does not supply original-language morphology, lemmas, or full-text search. Use a separate licensed corpus for those needs.

## Prerequisites

- An HTTP client available to the agent, such as an HTTP tool, `curl`, or a standard-library client.
- Permission to access the public endpoint from the current network.
- A chosen translation or a discovery step before requesting a chapter.

Base URL: `https://bible.helloao.org/api/`

## Endpoints

| Resource | Endpoint |
|---|---|
| Available translations | `available_translations.json` |
| Books in a translation | `{translation}/books.json` |
| Translation chapter | `{translation}/{BOOK}/{chapter}.json` |
| Complete translation | `{translation}/complete.json` |
| Available commentaries | `available_commentaries.json` |
| Commentary books | `c/{commentary}/books.json` |
| Commentary chapter | `c/{commentary}/{BOOK}/{chapter}.json` |
| Commentary profiles | `c/{commentary}/profiles.json` |
| Available datasets | `available_datasets.json` |
| Dataset books | `d/{dataset}/books.json` |
| Dataset chapter | `d/{dataset}/{BOOK}/{chapter}.json` |

## Steps

1. **Discover resources first.** Request `https://bible.helloao.org/api/available_translations.json`, `available_commentaries.json`, or `available_datasets.json` as appropriate. Use the returned `id`, endpoint links, `licenseUrl`, and format metadata instead of guessing identifiers. Completion: the requested resource ID appears in the relevant discovery response.
2. **Verify identifiers.** Translation and source IDs are case-sensitive. Use uppercase USFM book codes such as `GEN`, `PSA`, `MAT`, `JHN`, and `REV`; chapters are positive integers. Completion: the constructed endpoint returns JSON, not an HTML documentation page.
3. **Fetch the smallest suitable resource.** Use a chapter endpoint for reading, citation, or passage study. Use `complete.json` only for an offline pack, indexing job, or bulk analysis; it can be several megabytes. Completion: the response parses as JSON and its returned metadata matches the selected resource.
4. **Preserve structure.** Chapter `content` may contain headings, line breaks, subtitles, and verses. Verse content can contain strings, formatted-text objects, inline headings, line-break markers, and footnote references. Preserve semantic items and record any rendering simplifications. Completion: a rendered extract does not silently drop verse boundaries or attribute text to the wrong verse.
5. **Check rights and attribution.** Read `licenseUrl` and source metadata from the discovered resource before copying text into a product, cache, or public repository. Public endpoint access does not itself grant redistribution rights. Completion: the project source registry records the license, attribution requirement, and allowed use.
6. **Cite the retrieval.** Keep the API URL, resource name and ID, access date, and applicable license link with each excerpt or imported dataset. Completion: another agent can reproduce the request and inspect the source terms.

## Request Examples

List translations:

```text
GET https://bible.helloao.org/api/available_translations.json
```

Fetch a verified translation chapter:

```text
GET https://bible.helloao.org/api/[translation-id]/GEN/1.json
```

Fetch a public commentary chapter after discovery:

```text
GET https://bible.helloao.org/api/c/[commentary-id]/GEN/1.json
```

Fetch cross references after dataset discovery:

```text
GET https://bible.helloao.org/api/d/[dataset-id]/GEN/1.json
```

A portable command-line JSON check:

```bash
curl -fsSL 'https://bible.helloao.org/api/available_translations.json' \
  | python3 -c 'import json, sys; print(len(json.load(sys.stdin)["translations"]))'
```

Expected result: a positive integer and exit status `0`.

## Limits

- No authentication is required; no published rate limit was identified. Use polite request rates and cache only where the source terms allow it.
- The root site and invalid paths can return documentation HTML. Always use the `/api/` prefix and validate JSON.
- There is no server-side full-text search. Downloaded, permitted data must be indexed by the consuming application if search is needed.
- The service does not provide parsed Hebrew, Aramaic, or Greek data such as morphology, lemmas, or Strong's identifiers.
- Commentary coverage and granularity vary. Verify available books and inspect returned chapter content rather than assuming one entry per verse.

## Pitfalls

- Guessing translation IDs; always discover them from the available-translations response.
- Using lowercase book codes or requesting the documentation root, which may return HTML instead of API data.
- Treating a successful HTTP response as evidence that the requested translation exists; validate JSON and response metadata.
- Redistributing text, commentary, audio links, or a complete download without checking the resource's own license and attribution requirements.
- Flattening formatted content and losing headings, poetry markers, footnotes, or verse boundaries.
- Assuming this API provides original-language analysis or a search endpoint.

## Verification

- Discovery, translation-book, chapter, commentary, and dataset endpoints return HTTP `200` and valid JSON from the current environment.
- A valid chapter response identifies the chosen translation, book, and chapter.
- Resource ID, source URL, access date, license URL, and any required attribution are retained with imported material.
- The consumer handles non-verse content and footnotes deliberately.
- No request contains secrets, credentials, machine-local paths, or assumptions about a particular agent framework.

## Reference

- API documentation: `https://bible.helloao.org/docs/reference/`
- Source repository: `https://github.com/HelloAOLab/bible-api`
