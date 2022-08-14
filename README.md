# Stateful event processing

## An example 

Imagine we are github, The problem begins where we want move to the event driven world by capturing events and emitting them from the application.now imagine we decide to do a data replication from database to AWS and other shiny cloud solutions.
You know that one way to do this is by capturing CDC events from database operations, you know there are tools built for this purpose so you jump to next problem, which is consuming these CDC events, doing transformations and complex joins on the data to get some meaningful results and create data products. You start by exploring different tools available, while robust tools like Flink or Kafka Streams support joins, they are extremely limited. The typical use case is to enrich a stream of records with another stream that is used as a small lookup table.

Our stream processing tool works as follows:
- consume CDC events from database
- transform data possibly with joins
- create data products from replicated data meaning that data output is consumable through API, streaming and bulk dump.

### Transformation requirements
All transformations are described in SQL language.

The entities application works with are as follows:
### Entities

**User**
- email
- username
- registered_at
- type (org,person)
pk: username

**Repo**
- name
- owner
- description
- star_count
- fork_count
- created_at
- updated_at
pk: (owner,name)

**Pull Request**
- repo
- index
- author
- related_issue
- created_at
- updated_at
pk: (repo,index)

**Issue**
- repo
- index
- author
- content
- status
- created_at
- updated_at
pk (repo,index)

**Comment**
- id
- author
- related_entity_id
- reply_to
- body
pk: (id)

**Star**
- username
- repo_name
- repo_owner
- created_at
pk: (username, repo_name, repo_owner)

## Data Product
Let's say we want our streaming application to consume CDC events from above tables and create following entities from it:

**User Profile**
- email
- username
- stars_received
- total_pull_request_count

Filter user events on type
Left join on PR table and count pull requests by user
left join on start table and count stars received


** Org Profile **
- members
- name
- 10_x_dev (the person who contributed the most to Org Repos)

Filter user events on type
left join on PR table and find the person in the org with max PR count in all org Repos
