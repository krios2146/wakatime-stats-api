# wakatime-stats-aggregator

Telegram bot for fetching personal stats from the Wakatime using their API and creating charts based on the data

## Showcase

![image](https://github.com/krios2146/wakatime-stats-aggregator/assets/91407999/de7c92cc-9a92-40f2-900d-22ce7ed8c013)

## Features

Pie chart generation for the projects, languages and editors data obtained form the Wakatime API

Telegram bot serves as an interface for triggering the process of chart creation

Chart for languages uses [GitHub languages colors](https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml) for generation. 
If color isn't present in the github-linguist then the default matplotlib color will be used

All charts are saved under the plots directory (should be created manually)

## Modules

##### `api_client.py`

Used for API calls

Wakatime API URL is build like this `${WAKATIME_BASE_URL}/users/${WAKATIME_USER}/last_7_days`. 
Will be called every time any bot command is called

If /languages bot command is called then `https://raw.githubusercontent.com/github-linguist/linguist/master/lib/linguist/languages.yml` will be fetched

##### `telegram_bot.py`

Uses `api_client` to get data, pass it to the `data_processor` and show the chart obtained by `image_manager`

Have 4 commands:
- /start
- /languages
- /editors
- /projects

For the /languages command [github-linguist](https://github.com/github-linguist/linguist) `languages.yml` file is fetched via `api_client`

##### `data_processor.py`

Uses [matplotlib](https://matplotlib.org/stable/) to build charts for every bot command.
Charts are saved under `plots` directory. 
Chart names follow the pattern - `${UUID}_${date}.png`, 
where `UUID` is the UUID of a request, and `date` is a date in the YY-MM-DD format

##### `image_manager.py`

Used by `data_processor` to save charts to the charts and by `telegram_bot` to retrieve the chart by its UUID

## Local run

1. Clone project

```bash
git clone git@github.com:krios2146/wakatime-stats-aggregator.git
```
2. Go to project directory

```bash
cd wakatime-stats-aggregator
```

3. Create `.env` file

```bash
touck .env
```

The content of the `.env` is the following
```env
WAKATIME_API_KEY=''
WAKATIME_BASE_URL='https://wakatime.com/api/v1'
WAKATIME_USER='krios2146'
TELEGRAM_API_TOKEN=''
```

[How to get WAKATIME_API_KEY](https://wakatime.com/faq#api-key) 
[How to get TELEGRAM_API_TOKEN](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) 

4. Create `plots` directory

```bash
mkdir plots 
```

5. Set up venv

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

6. Start the bot

```bash
python src/telegram_bot.py
```

7. In your bot first type /start and then one of the following commands:

- /languages
- /editors
- /projects
