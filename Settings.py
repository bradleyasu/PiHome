import json

ifttt_settings = json.dumps([
    {'type': 'title',
     'title': 'IFTTT & Adafruit.io integration'
    },
    {
        'type': 'string',
        'title': "AdaFruit IO API Key",
        'desc': "API Key to retrieve alerts",
        'section': "IFTTT",
        'key': 'aioKey'
    },
    {
        'type': 'string',
        'title': "AdaFruit IO Username",
        'desc': "What's your AdaFruit IO username?",
        'section': "IFTTT",
        'key': 'aioUsername'
    },
    {
        'type': 'string',
        'title': "AdaFruit IO Feed Key",
        'desc': "Which feed would you like to monitor?",
        'section': "IFTTT",
        'key': 'aioFeedKey'
    },
    {
        'type': 'bool',
        'title': 'AdaFruit IO Integration',
        'desc': 'Would you like to check for alerts?',
        'section': "IFTTT",
        'key': 'aioEnabled'
    },
])
weather_settings = json.dumps([
    {'type': 'title',
     'title': 'Weather Screen'
    },
    {
        'type': 'string',
        'title': "Open Weather Map API Key",
        'desc': "Open weather map API key is required for gathering weather information",
        'section': "Weather",
        'key': 'owmKey'
    },
    {
        'type': 'string',
        'title': "Weather Underground API Key",
        'desc': "Weather Underground API key is required for gathering weather information",
        'section': "Weather",
        'key': 'wuKey'
    },
    {
        'type': 'string',
        'title': "Zip Code",
        'desc': "Enter your zip code for local weather information",
        'section': "Weather",
        'key': 'zip'
    }
])
general_settings = json.dumps([
    {'type': 'title',
     'title': 'Home Screen Wallpapers'
    },
    {
        'type': 'bool',
        'title': 'Wallpapers',
        'desc': 'Automatically Refresh Background Image',
        'section': "General",
        'key': 'wallpaperRefresh'
    },
    {
        'type': 'string',
        'title': 'Wallpaper Sources One',
        'desc': 'Enter Subreddit Sources For Wallpaper (multi-subreddit format)',
        'section': "General",
        'key': 'wallpaperSourceOne'
    },
    {
        'type': 'string',
        'title': 'Wallpaper Sources Two',
        'desc': 'Enter Tumblr Sources For Wallpaper (comma separated format)',
        'section': "General",
        'key': 'wallpaperSourceTwo'
    },
    {
        'type': 'options',
        'title': 'Active Wallpaper Source',
        'desc': 'Which of the above sources would you like to use?',
        'section': "General",
        'key': 'wallpaperActiveSource',
        'options': ['Source One', 'Source Two']
    },
    {'type': 'title',
     'title': 'Reddit Rising Notifications'
    },
    {
        'type': 'string',
        'title': 'News Subreddit Source',
        'desc': 'Which subreddit(s) would you like to monitor?',
        'section': "RedditRising",
        'key': 'rrsource',
    },
    {
        'type': 'numeric',
        'title': 'Upvotes Required',
        'desc': 'What is the minimum upvotes required to display?',
        'section': "RedditRising",
        'key': 'rrups',
    },
    {
        'type': 'bool',
        'title': 'Enable Rising News?',
        'desc': 'If disabled, no news will be on the home screen',
        'section': "RedditRising",
        'key': 'rrenabled',
    }
])