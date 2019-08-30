item = '''
    "item": {
        "class": "NewsItem",
        "loader": "ChinaLoader",
        "attrs": {
            "title": [
                {
                    "method": "xpath",
                    "args": [
                        "{titleXpath}"
                    ]
                }
            ],
            "url": [
                {
                    "method": "attr",
                    "args": [
                        "url"
                    ]
                }
            ],
            "text": [
                {
                    "method": "xpath",
                    "args": [
                        "{textXpath}"
                    ]
                }
            ],
            "website": [
                {
                    "method": "value",
                    "args": [
                        "定制家电"
                    ]
                }
            ]
        }
    }
'''
print(item)