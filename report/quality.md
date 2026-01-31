## Accuracy
High syntactic accuracy through parse scripts.
Data is discarded before being incorrectly ingested.
Might change with inclusion of extracted triples from less well formatted sources.
Right now invalid syntax would crash graph builder.
Semantic accuracy (whether data represents correct state of object) is more difficult. Less meaningful for snapshots / observations.

## Completeness
Horrendous, but quantifiable.
Check how many categories have entries for a company.

## Consistency
Compare entries in same category to each other.
Requires precise taxonomy.

## Timeliness
Describes average age of data.
Not easily accessable, inferrable with lots of effort.
Not that relevant, since each observations has a date its information is relevant for. Timeliness of observation is irrelevant (except for resolving conflicts.)

## Trustworthiness
High but partially crowdsourced and therefore open to adversarial injection.
Also susceptible to misreporting by companies.

## Availability
Availability is perfect. No remote resources are used.
Might change with inclusion of APIs or language models for query translation.
