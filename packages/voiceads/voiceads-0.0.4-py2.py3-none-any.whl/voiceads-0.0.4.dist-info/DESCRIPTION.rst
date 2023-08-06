voiceads
---------

# Install the package

you can install the package locally in the current folder by using the following command: 

#from main public PIP repo

pip install -t ./ voiceads

----------

## SDK usage: 

from voiceads import VoiceAdsAI

appToken = '<YOUR APP TOKEN>'

appType = '<YOUR APP TYPE>'

va = VoiceAdsAI()

params = {
    'appName' : '<YOUR APP NAME>',

    'appId': '<YOUR APP ID>',

    'appType': '<YOUR APP TYPE>',

    'appCategory' : '<YOUR APP CATEGORY>'
}

va.initialize(appToken, appType, params)

resp = va.getAd()


