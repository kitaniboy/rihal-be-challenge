# Rihal BE Challenge

## How to run

```shell
docker-compose up --build
```

## Approach Description

As mentioned in the challenge specification, the main aim of this application is to **search** through files and **extract valuable insights** and this aim have been the central part when designing this solution. Python was chosen for it's well known capabiliteis and huge community in data mining and backend development; for example, when it comes to sentence and word tokenization, and filtering stop words, these functionalities have been previously with the aid of trained machine learning models, and made publicly available via the nltk python package. Hence, reinventing the wheel is strictly unnecessary. In addition, a simple document summarizer feature has been added to provide a summary of a given text.

&nbsp;&nbsp;&nbsp;&nbsp;Moreover, other decisions have been made when designing this solution. The integration of cloud-based object storage and a locally hosted database has been chosen to achive optimal balance between performance and scalability. Firebase was used for the long term storage of PDF documents for it's ease of use and quality service. On the other hand, PostgreSQL was used for fast retrival of data used in analysis, a consept similar to caching.

## Endpoints

The following table shows which RESTful HTTP methods are supported for each endpoint:

| Endpoint | GET | POST | PUT | DELETE |
| --- | --- | --- | --- | --- |
| `document/` | | ### |
| `documents/` | ### |
| `search/` | ### |
| `document/<int:id>` | ### | | | ### |
| `document/<int:id>/page/<int:num>` | ### |
| `document/<int:id>/sentences` | ### |
| `document/<int:id>/summary` | ### |
| `document/<int:id>/search` | ### |
| `document/<int:id>/top` | ### |
| `register/` | | ### |
| `token/` | | ### |
| `token/refresh/` | ### |
| `token/verify/` | ### |

The following table describes each endpoint:

| Endpoint | Request body | Description |
| --- | --- | --- |
| `document/` | **Content-Type:** multipart/form-data <br/> **file:** PDF file | Send and save a PDF file under the user |
| `documents/` | | Get all PDF files details saved under the user |
| `search/` | **keyword:** string | Search for a keyword in all PDF documents |
| `document/<int:id>` | | Get a specific PDF document details |
| `document/<int:id>/page/<int:num>` | | Get a specific page from a specific document as an image (`num` is zero indexed)|
| `document/<int:id>/sentences` | | Get the parsed sentences from a specific document |
| `document/<int:id>/summary` | **count:** int? | Get a summary limited by **count** (20% of the document default) |
| `document/<int:id>/search` | **keyword:** string | Search for a keyword in a specific PDF document |
| `document/<int:id>/top` | **count:** int? | Get most common words (5 words by default) |
| `register/` | **username:** string <br/> **password:** string | Create a new user |
| `token/` | **username:** string <br/> **password:** string | Create a new token for the user |
| `token/refresh/` | **refresh:**: string  | Refresh an access token by supplying refresh token |
| `token/verify/` | **token:** string | Verify the authenticity of a token |

### Important note

In some cases adding a backslash '/' to an endpiont may **stop it from working**, e.g., `document/1/page/0` will work but `document/1/page/0/` will **not!** This also works the other way around, `document/` will work but `document` will **not!**

## Tokens Usage

After creating a new user from the `register/` endpoint, the user can request a new token from `token/` which will return a **refresh** token valid for 1 day and an **access** token valid to for 40 minutes to be added to each request in the Header under Authorization as 'Bearer {access_token}'. After 40 minutes, the **access** token will be expired and the `token/refresh/` can be used supplied with **refresh** token to refresh the **access** token.

## Legal Notice

The authour of this project have tried to make sure that all the packages, libraries, and any material is permissible to be used in the context of this challenge.
