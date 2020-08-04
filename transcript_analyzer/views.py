from django.shortcuts import render
from transcript_analyzer.models import Actor
from transcript_analyzer.models import Character
from transcript_analyzer.models import Episode
from . import forms
from django import forms as f
# Create your views here.
def display(request):
    vars = {}
    characters = runit(request)
    print(characters)
    actorsDict = get_actors(request)
    formDict = get_url(request)
    checkboxes = words_per_actor(request, characters, actorsDict)
    vars.update(characters)
    vars.update(formDict)
    vars.update(actorsDict)
    vars.update(checkboxes)
    return render(request,'transcript_analyzer/rewrite.html',vars)
def get_actors(request):
    actors = Actor.objects.all()
    #print (actors)
    actorsDict = {'actors':actors}
    return actorsDict
def get_url(request):
    form = forms.Transcript_url
    return {'form':form}
def save_to_char_db(request, entry):
    character = Character.objects.create(name=entry[0], picture=entry[1])
def words_per_actor(request, characters, actorsDict):
    actor_list = []
    characters_list = []
    checkboxes = {}
    char_check = []
    for i in characters['names']:
        characters_list.append(i)
    for i in actorsDict['actors']:
        actor = forms.actor_obj()
        actor.name = i.first_name
        actor.picture = i.picture
        actor.characters = characters_list
        actor_list.append(actor)
    actor.reload()
    checkboxes['checkboxes'] = actor_list
    return checkboxes
def percentage(request):
    pass
def runit(request):
    if request.method == 'POST':
        print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        form = forms.Transcript_url(request.POST)
        if form.is_valid():
            print(form.cleaned_data['url'])
            import requests
            from bs4 import BeautifulSoup
            import sys
            import re
        #    try:
            if 'NextGen' in form.cleaned_data['url']:
                series = 'Next Gen'
            elif 'DS9' in form.cleaned_data['url']:
                series = 'ds9'
            elif 'Voyager' in form.cleaned_data['url']:
                series = 'voyager'
            elif 'Enterprise' in form.cleaned_data['url']:
                series = 'enterprise'
            elif 'movies' in form.cleaned_data['url']:
                series = 'movies'
            else:
                series = 'tos'
            print (series)
            page = requests.get(form.cleaned_data['url'])
            soup = BeautifulSoup(page.content,'html.parser')
            text = soup.find_all('p')
            lines = []

            for i in text:
                ptag = str(i).split('<br/>')
                for line in ptag:
                    line = line.replace('\n',' ')
                    line = line.replace('\r','')
                    line = line.lstrip()
                    line = line.replace('\n[OC]','')
                    lines.append(line)
                people = []
                line_counts = []
                word_count = []
                for i in lines:
                    i = i.replace(' [OC]','')
                    i = i.replace(' {OC]','')
                    i = i.replace(' [on viewscreen]','')
                    i = i.replace(' [on viewscreen','')
                    i = i.replace(' [on monitor]','')
                    i = i.replace('</font>','')
                    i = i.replace('</p>','')
                    i = i.replace('Stardate:','')
                    i = i.replace('Original Airdate:','')
                    i = re.sub('<[^>]+>', '', i)
                    i = re.sub('\[[^]]+\]', '', i)
                    i = i.lstrip()
                    if ':' in i and i[0].isupper():
                        characters = Character.objects.all()
                        i = re.sub(r'\([^)]*\)','',i)
                        i = i.replace(' :',':')
                        person = i[:i.index(':')]
                        if characters.filter(name=person).exists():
                            pass
                        else:
                            print('saving '+ person)
                            entry = [person,get_picture(request,person,series)]
                            save_to_char_db(request,entry)
                        if i[:i.index(':')] not in people:
                            people.append(i[:i.index(':')])
                            line_counts.append(1)
                            words = i[i.index(':')+1:].split()
                            word_count.append(len(words))
                        else:
                            line_counts[people.index(i[:i.index(':')])] += 1
                            words = i[i.index(':')+1:].split()
                            word_count[people.index(i[:i.index(':')])] += len(words)
                        mydict = {}
                        mydict['names'] = []
            for i in people:
                person = characters.filter(name=i)
                print(person)
                print(i +' '* (20 - len(i))+str(line_counts[people.index(i)])+' '*(20 - len(str(line_counts[people.index(i)])))+str(word_count[people.index(i)]))
                list = [i,line_counts[people.index(i)],word_count[people.index(i)], person[0].picture]
                mydict['names'].append(list)
            mydict['names'] = sorted(mydict['names'], key=lambda name: int(name[2]))
            mydict['names'].reverse()
            return mydict
    else:
        mydict = {}
        mydict['names'] = []
        return mydict
            #except Exception as e:
            #    print('made it')
            #    print(e)
            #    mydict = {}
            #    print('massive error!!!!!')
            #    return mydict
def get_picture(request,person, series):
        import random
        from selenium import webdriver
        from bs4 import BeautifulSoup
        from selenium.webdriver.common.keys import Keys
        import requests
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=options)
        #print('https://google.com/search?q='+ person)
        driver.get('https://images.google.com/')
        search = driver.find_element_by_xpath('//input[@title="Search"]')
        search.send_keys(person+' star trek '+series)
        search.send_keys(Keys.RETURN)
        links = driver.find_elements_by_tag_name('img')
        #print(len(links))
        #print (person)
        images = []
        for i in links:
            if i.get_attribute('src'):
                images.append(i.get_attribute('src'))
        driver.close()
        try:
            link = images[0]
        except:
            link = None
        return link
