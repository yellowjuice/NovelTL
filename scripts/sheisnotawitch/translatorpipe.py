import json
import glob
import os
from openai import OpenAI

client = OpenAI(base_url = "https://api.deepseek.com")

glossaryfile = 'glossary_translated.csv'
rawdir = '../../../Database/sheisnotawitch/raw/'
outdir = '../../../Database/sheisnotawitch/en/'

userprompt = "Translate the following chapter from Chinese to English:\n"
sysprompt = "You are a translator translating the Chinese webnovel \"才不是魔女\" to English. You have a glossary as reference of names below. There may be mistakes, so use your own judgement when translating.\n"

with open(glossaryfile, 'r') as f:
    glossary = f.read()

out = {}
MAX_FAIL = 40
fails = 0

for cnum in range(276 ,277):
    file = rawdir + "chapter_" + str(cnum) + ".txt"
    with open(file, 'r') as f:
        chap = f.read()
    while fails < MAX_FAIL:
        try:
            response = client.chat.completions.create(
                model = "deepseek-chat",
                messages = [{"role": "system", "content": sysprompt + glossary}, {"role": "user", "content": userprompt + chap}],
                temperature = 1.3
            )
            print("Translated " + file)
            break
        except Exception as e:
            print("An error occured")
            print(e.message, e.args)
    if fails >= MAX_FAIL:
        print("Too many fails, breaking at " + file)
        break
    with open(outdir + os.path.basename(file), 'w') as g:
        g.write(response.choices[0].message.content)
