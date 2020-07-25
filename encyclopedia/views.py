from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
from . import util
from .util import get_entry, list_entries, save_entry
import markdown2
import random
import os

class createNewPage(forms.Form):
    title = forms.CharField(label="Title of page", widget=forms.TextInput(attrs={'class':'form-control col-5', 'id':'title'}), max_length=250)
    content = forms.CharField(label="Content of the page", widget=forms.Textarea(attrs={'class':'form-control col-5'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    if get_entry(name) == None:
        messages.add_message(request, messages.ERROR, 'Page does not exist')
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/test.html", {
            "file": markdown2.markdown_path(f"entries/{name}.md"),
            "name": name
        })

def createPage(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/createPage.html", {
            "form":createNewPage()
        })
    else:
        form = createNewPage(request.POST)
        data = request.POST.copy()
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if get_entry(title) is None:
                messages.add_message(request, messages.INFO, 'Created a new Entry')
                save_entry(data.get('title'), data.get('content'))
                return HttpResponseRedirect(reverse("tasks:index"))
            elif form.cleaned_data["edit"] is True:
                messages.add_message(request, messages.INFO, 'Edited the Entry')
                save_entry(data.get('title'), data.get('content'))
                return HttpResponseRedirect(reverse("tasks:index"))
            else:
                messages.add_message(request, messages.ERROR, 'Entry already exists')
                return render(request, "encyclopedia/createPage.html", {
                    "form": createNewPage()
                })
        else:
            messages.add_message(request, messages.ERROR, 'Form is invalid')
            return render(request, "encyclopedia/createPage.html", {
                "form": createNewPage()
            })

def editPage(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html", {
            "entryTitle": entry
        })
    else:
        form = createNewPage()
        form.fields["title"].initial = entry
        form.fields["title"].widget.attrs['readonly'] = True
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/createPage.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })

def delete(request, name):
    if get_entry(name) is None:
        return render(request, "encyclopedia/error.html")
    else:
        os.remove(f"entries/{name}.md")
        messages.add_message(request, messages.INFO, 'Successfully deleted the entry')
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def search(request):
    if request.method == "POST":
        name = request.POST.get('q')
        if name in list_entries():
            if get_entry(name) == None:
                messages.add_message(request, messages.ERROR, 'No such entry exists')
                return render(request, "encyclopedia/error.html")
            else:
                return render(request, "encyclopedia/test.html", {
                    "file": markdown2.markdown_path(f"entries/{name}.md"),
                    "name": name
                })
        else:
            new_list = []
            for i in range(len(list_entries())):
                if name in list_entries()[i] or name.upper() in list_entries()[i] or name.lower() in list_entries()[i]:
                    new_list.append(list_entries()[i])
                    i += 1
                else:
                    i += 1
            if new_list == []:
                messages.add_message(request, messages.ERROR, 'No such entries exist')
                return render(request, "encyclopedia/error.html")
            else:
                messages.add_message(request, messages.SUCCESS, 'Entry(ies) found')
                return render(request, "encyclopedia/index.html", {
                    "entries": new_list
                })

def randomize(request):
    x = random.randint(0, len(list_entries())-1)
    article = list_entries()[x]
    if get_entry(article) == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/test.html", {
            "file": markdown2.markdown_path(f"entries/{article}.md"),
            "name": article
        })

# def delete(request):
