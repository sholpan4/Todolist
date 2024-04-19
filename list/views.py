from django.http import HttpResponse
from django.shortcuts import render, redirect

from list.models import Category, Task


def redirect_view(request):
    return redirect('/category')


def todo(request):
    todos = Task.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        if 'Add' in request.POST:
            title = request.POST['description']
            date = str(request.POST['date'])
            category = request.POST['category_select']
            content = title + '--' + date + ' ' + category
            todo = Task(title=title, content=content, duedate=date,
                        category=Category.objects.get(name=category))
            todo.save()
            return redirect('/todo')

        if 'Delete' in request.POST:
            checkedlist = request.POST.getlist('checkedlist')

            for i in range(len(checkedlist)):
                todo = Task.objects.filter(id=int(checkedlist[i]))
                todo.delete()

    return render(request, 'todo.html',
                  {'todos': todos, 'categories': categories})


def category(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        if 'Add' in request.POST:
            name = request.POST['name']
            category = Category(name=name)
            category.save()
            return redirect('/category')

        if 'Delete' in request.POST:
            check = request.POST.getlist('check')

            for i in range(len(check)):
                try:
                    categ = Category.objects.filter(id=int(check[i]))
                    categ.delete()
                except BaseException:
                    return HttpResponse('<h1>Сначала удалите карточки с этими категориями</h1>')
    return render(request, 'category.html', {'categories': categories})
