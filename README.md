# Stateful event processing

## Problem Statement

Imagine we are github, The problem begins where we want move to the event driven world by capturing events and emitting them from the application.now imagine we decide to do a data replication from database to AWS and other shiny cloud solutions.
You know that one way to do this is by capturing CDC events from database operations, you know there are tools built for this purpose so you jump to next problem, which is consuming these CDC events, doing transformations and complex joins on the data to get some meaningful results and create data products. You start by exploring different tools available but they all are costly to develop maintain, that where you find this amazing solution to build your own stream processing tool.

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
