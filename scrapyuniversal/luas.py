
# splash:runjs("document.getElementsByClassName('laypage_next').click()")
# "getElementByXpath("//html[1]/body[1]/div[1]")"
# document.querySelector('.laypage_next').setAttribute('data-page',%d);document.querySelector('.laypage_next').click()

luaScript = '''
    function main(splash)
        splash.images_enabled = splash.args.images
        splash:go(splash.args.url)
        splash:wait(2)
        js = string.format(splash.args.js)
        splash:runjs(js)
        splash:wait(2)
        return splash:html()
    end
'''

luaSimple = '''
    function main(splash)
        splash.images_enabled = splash.args.images
        splash:go(splash.args.url)
        splash:wait(2)
        return splash:html()
    end
'''