import json

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
        'title': "Zip Code",
        'desc': "Enter your zip code for local weather information",
        'section': "Weather",
        'key': 'zip'
    }
])
general_settings = json.dumps([
    {'type': 'title',
     'title': 'Home Screen'
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
    }
])