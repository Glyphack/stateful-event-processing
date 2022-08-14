t # Stateful event processing

Go multiple levels deep
Join on primary and non-primary keys depending on the particular relation
Preferably perform multiple joins without writing intermediate results out to different topics or adding operational complexity
Not be windowed joins on time series data
All input topics are treated as if they were ‘tables’
Support 1 to 1, 1 to many, and many to 1 relations
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

Pk: username

**Repo**
- name
- owner
- description
- star_count
- fork_count
- created_at
- updated_at

Pk: (owner,name)

**Pull Request**
- repo
- repo_owner
- index
- author
- created_at

Pk: (repo, repo_owner,index)

**Star**
- username
- repo_name
- repo_owner
- created_at

Pk: (username, repo_name, repo_owner)

**Issue**
- repo
- index
- author
- content
- status
- created_at
- updated_at
    
Pk (repo,index)

**Comment**
- id
- author
- related_entity_id
- reply_to
- body

Pk: (id)


## Data Product
Let's say we want our streaming application to consume CDC events from above tables and create following entities from it:

**User Profile**
- email
- username
- starred_repos (many to many rel)
    - repo = repo_name/repo_owner
    - description
- opened_pull_requests (one to many rel)
    - repo = repo_name/repo_owner
    - index
    - title
    - created_at
    - status

Filter user events on type

Left join on PR table and add all user PR to record
Left join on star table and add all repo names that user starred

**Org Profile**
- members
- name
- 10_x_dev (the person who contributed the most to Org Repos)

Filter user events on type

Left join on PR table

Find the person in the org with max PR count in all org Repos

