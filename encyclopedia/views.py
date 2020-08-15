import markdown2
import random
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
from . import util

class searchForm(forms.Form):
    query = forms.CharField(label='')



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : searchForm()
    })

def title(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/DNE.html", {
            "title" : title,
            "form" : searchForm()
        })
    return render(request, "encyclopedia/title.html", {
        "title" : title,
        "title_entry" : markdown2.markdown(entry),
        "form" : searchForm()
    })

def search(request):
    if request.method == "POST":
        form = searchForm(request.POST)
        all_entries = util.list_entries() #list of all available entries
        matches = [] #list of matches found with query
        if form.is_valid():
            #getting query from the form
            query = form.cleaned_data["query"]
            #looping over all the entries
            for entry in all_entries:
                #if query exists return the title page
                if query.lower() == entry.lower():
                    return redirect('title', title=entry)
                #append to match list of any matches are found for the query
                if query.lower() in entry.lower():
                    matches.append(entry)
            #return a list of partial matches
            return render(request, "encyclopedia/search.html", {
                "length" : len(matches),
                "entries" : matches,
                "form": searchForm()
            })
    return render(request, "encyclopedia/search.html", {
        "entries" : "",
        "form" : searchForm()
    })


def add(request):
    all_entries = util.list_entries()
    flag = False
    if request.method == "POST":
        heading = request.POST.get('title')
        content = request.POST.get('content')
        # checking if the title already exists
        if heading in all_entries:
            flag = True
            return render(request, "encyclopedia/newpage.html", {
                "flag" : flag,
                "form" : searchForm()
            })
        else:
            util.save_entry(heading, content)
            return redirect('title', title=heading)
    return render(request, "encyclopedia/newpage.html", {
        "flag" : flag,
        "form" : searchForm()
    })

def edit(request, title):
    content = util.get_entry(title)
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "content" : content,
            "heading" : title,
            "form" : searchForm()
        })
    if request.method == "POST":
        content = request.POST.get('newContent')
        util.save_entry(title, content)
        return redirect('title', title=title)

def rand(request):
    li = util.list_entries()
    n = random.randint(0, (len(li)-1))
    title = li[n]
    return redirect('title', title=title)