# wakatime-stats-api

The WakaTime Stats API is a tool
for generating charts based on your last 7 days of coding data from [Wakatime](https://wakatime.com/).
It uses [Matplotlib](https://matplotlib.org/) to make the charts
and connects to the [Wakatime API](https://wakatime.com/developers) to get your data.

Built with Python [FastAPI](https://fastapi.tiangolo.com/), it's quick and easy to use,
perfect for developers who want to visualize their coding activity without much hassle.

You can customize the API to hide certain data, group items, change colors, and adjust the size of your charts.
It even supports wildcards for more flexible data handling
and uses [GitHub language colors](https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml) to color code programming languages.

## Table of Contents

- [Showcase](#showcase)
- [Features](#features)
- [Usage/Examples](#usageexamples)
- [API Reference](#api-reference)
- [Local run](#local-run)
- [Deployment](#deployment)
- [License](#license)

## Showcase

#### API call
```
GET https://{domain}/api/{your_wakatime_username}/pie/languages
  ?hide=http**,**ml,docker**,json
  &width=420
  &height=215
  &vue.js=41b883
  &bash=89e051
```

#### Result

![image](https://github.com/krios2146/wakatime-stats-api/assets/91407999/732ea5be-7bcc-4cb1-8d0c-32ac66171612)

## Features

- API allows hiding any data you don't want to show
- API allows defining groups of data. Useful if you don't want to show names of your work-related / confidential projects
- API allows changing color of any data
- API allows changing the output size of the image
- API allows using wildcard (`**`) when hiding or defining groups
- API uses [GitHub languages colors](https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml) for coloring languages in the `/languages` endpoint 

## Usage/Examples

#### Hiding all languages that start with "docker" and "java" (Dockerfile, Java, JavaScript) [case-insensitive]

```
GET https://{domain}/api/{your_wakatime_username}/pie/languages
  ?hide=docker**,java**
```

#### Hiding all languages that ends with "ml" (YAML, HTML) [case-insensitive]

```
GET https://{domain}/api/{your_wakatime_username}/pie/languages
  ?hide=**ml
```

#### Grouping work-related projects that start with "curo" and "compose-stack" specifically [case-insensitive]

```
GET https://{domain}/api/{your_wakatime_username}/pie/projects
  ?group=work-related
  &work-related=curo**,compose-stack
```

#### Changing colors of a group and projects individually [HEX and color names]

```
GET https://{domain}/api/{your_wakatime_username}/pie/projects
  ?group=work-related
  &work-related=curo**,compose-stack
  &work-related_colors=black
  &wakatime-api-stats=e5e7eb
```

#### Changing size of the output image [pixels]

```
GET https://{domain}/api/{your_wakatime_username}/pie/editors
  ?width=650
  &height=300
```

## API Reference

Swagger UI is available on the `/docs` endpoint, but it doesn't cover all available GET parameters

<details>
<summary> Excalidraw API Spec [under the spoiler]</summary>
<p>

![wakatime-api-spec](https://github.com/krios2146/wakatime-stats-api/assets/91407999/bbec3051-7a1c-4dab-aecf-5f4a18351f67)

</p>
</details>

#### Languages

```http
GET /api/{username}/pie/languages
```

| Parameter         | Type                  | Description                                                                                                                                                                                 |
|:------------------|:----------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`        | `string`              | **Required**. Your WakaTime username                                                                                                                                                        |
| `hide`            | `string`, `string []` | Exact name of the language to hide. <br/> Wildcard `**` name of the language to hide with prefix** or **suffix. <br/> **Case-insensitive** <br/> Multiple value must be comma `,` separated |
| `{language_name}` | `string`              | Key is exact name of the language **case-insensitive**. <br/> Value is color in the HEX format (with or without `#`)                                                                        |
| `width`           | `number`              | Width of the output image in pixels                                                                                                                                                         |
| `height`          | `number`              | Height of the output image in pixels                                                                                                                                                        |

#### Editors

```http
GET /api/{username}/pie/editors
```

| Parameter       | Type                  | Description                                                                                                                                                                             |
|:----------------|:----------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`      | `string`              | **Required**. Your WakaTime username                                                                                                                                                    |
| `hide`          | `string`, `string []` | Exact name of the editor to hide. <br/> Wildcard `**` name of the editor to hide with prefix** or **suffix. <br/> **Case-insensitive** <br/> Multiple value must be comma `,` separated |
| `{editor_name}` | `string`              | Key is exact name of the editor **case-insensitive**. <br/> Value is color in the HEX format (with or without `#`)                                                                      |
| `width`         | `number`              | Width of the output image in pixels                                                                                                                                                     |
| `height`        | `number`              | Height of the output image in pixels                                                                                                                                                    |

#### Projects

```http
GET /api/{username}/pie/projects
```

| Parameter            | Type                  | Description                                                                                                                                                                                                                                              |
|:---------------------|:----------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`           | `string`              | **Required**. Your WakaTime username                                                                                                                                                                                                                     |
| `hide`               | `string`, `string []` | Exact name of the project or group to hide. <br/> Wildcard name of the project (or group) to hide with prefix** or **suffix. <br/> **Case-insensitive** <br/> Multiple value must be comma `,` separated                                                 |
| `{project_name}`     | `string`              | Key is exact name of the project **case-insensitive**. <br/> Value is color in the HEX format (with or without `#`)                                                                                                                                      |
| `width`              | `number`              | Width of the output image in pixels                                                                                                                                                                                                                      |
| `height`             | `number`              | Height of the output image in pixels                                                                                                                                                                                                                     |
| `group`              | `string`              | Name of the group that can be used in other parameters                                                                                                                                                                                                   |
| `{group_name}`       | `string`, `string []` | Key is exact name of the group. <br/> Value is exact name of the project to include in the group. <br/> Wildcard `**` name of the project to hide with prefix** or **suffix. <br/> **Case-insensitive** <br/> Multiple value must be comma `,` separated |
| `{group_name}_color` | `string`              | Key is exact name of the group with following `_color` suffix. <br/> Value is color in the HEX format (with or without `#`)                                                                                                                              |

## Local run

1. Clone project

    ```bash
    git clone git@github.com:krios2146/wakatime-stats-api.git
    ```
2. Go to project directory

    ```bash
    cd wakatime-stats-api
    ```

3. Create `.env` file

    ```bash
    touch .env
    ```

    The content of the `.env` is the following
    ```env
    WAKATIME_BASE_URL=https://wakatime.com/api/v1
    WAKATIME_API_KEY=waka_**
    ```

    - [How to get WAKATIME_API_KEY](https://wakatime.com/faq#api-key)

4. Set up venv

    Assuming that python is installed

    ```bash
    python -m venv
    ```

    ```bash
    source venv/biv/activate
    ```

    ```bash
    pip install -r requirements.txt
    ```

5. Start the API

    In dev mode with debug log configuration
    ```bash
    uvicorn app.main:app --reload --log-config=debug_log_config.yam
    ```

    In production mode with fast api cli
    ```bash
    fastapi run
    ```

6. Alternatively, you can run it inside a Docker container

    Build
    ```bash
    docker build . -t wakatime-stats-api
    ```

    Run
    ```bash
    docker run -d -p 80:8000 --env-file .env wakatime-stats-api
    ```

7. Call the API

    In browser type
    ```
    localhost:8000/api/{your_wakatime_username}/pie/languages
    ```

## Deployment

To deploy this project and use it for your own purposes, you need a VPS

The steps are the same as in [Local run](#local-run) section

The easiest way is to deploy using docker

---

Run locally after cloning the project 

```bash
docker build . -t {docker_username}/wakatime-stats-api
```

```bash
docker push {docker_username}/wakatime-stats-api
```

---

Run on the VPS, assuming you have docker installed

```bash
docker pull {docker_username}/wakatime-stats-api
```

Remember about .env file

 ```bash
 docker run -d -p 80:8000 --env-file .env {docker_username}/wakatime-stats-api
 ```

## License

[MIT](https://choosealicense.com/licenses/mit/)
