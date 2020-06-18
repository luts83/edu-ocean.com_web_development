from django.shortcuts import render, redirect

def index(request):
    return redirect('/enter_my_room/')

def enter_my_room(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
    }

    return render(
        request,
        'basecamp/enter_my_room.html',
        context=context
    )