from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
import random
# Create your views here.

class Games:
    def __init__(shelf):
        shelf.H = 6
        shelf.W = 8

        shelf.name = ''
        shelf.count = 0
        shelf.turn = 0
        shelf.who = {}
        spell = 'abcdefghijklmnopqrstuvwx'
        shelf.board = spell*2
        """
        shelf.board = []
        for i in range(1, 65):
            shelf.board.append(i)
            shelf.board.append(i)
        """
        shelf.params = {
        'title':shelf.name,
        'user':[],
        'board':shelf.board,
        'entry':0,
        'turn':{},
        'color':{},
        'enemy':{},
        'acount':{},
        'point':{},
        'get':{},
        'che':{},
        'before':{},
        'before_x':{},
        'before_y':{},
    }

    def all_check(shelf, user, enemy):
        shelf.params['message'] = 'check_def'
        if len(shelf.params['get'][user]) != 0 or len(shelf.params['get'][enemy]) != 0:
            shelf.params['message'] = 'check_if'
            for i in range(shelf.H):
                for j in range(shelf.W):
                    cot = 0
                    if len(shelf.params['get'][user]) != 0:
                        for mass in shelf.params['get'][user]:
                            if mass == shelf.params['acount'][user][i][j]:
                                shelf.params['che'][user][i][j] = mass
                                cot = 1
                                break

                    if cot == 0:
                        if len(shelf.params['get'][enemy]) != 0:
                            for mass in shelf.params['get'][enemy]:
                                if mass == shelf.params['acount'][user][i][j]:
                                    shelf.params['che'][user][i][j] = mass
                                    cot = 1
                                    break
                    if cot == 0:
                        shelf.params['che'][user][i][j] = '*'

        else:
            shelf.params['message'] = 'check_else'
            for i in range(shelf.H):
                for j in range(shelf.W):
                    shelf.params['che'][user][i][j] = '*'

        shelf.params['che'][enemy] = shelf.params['che'][user].copy()


    def cot(shelf, req):
        user_check = str(req.user)

        try:
            enemy = str(shelf.params['enemy'][user_check])

            if req.method == 'POST':

                if 'hit' in req.POST:
                    hw = str(req.POST['hit']).split('/')
                    height = int(hw[0])
                    width = int(hw[1])

                    shelf.params['before_y'][user_check].append(height)
                    shelf.params['before_x'][user_check].append(width)

                    shelf.params['message'] = 'hit'
                    shelf.params['height'] = str(height)
                    shelf.params['width'] = str(width)

                    mass = shelf.params['acount'][user_check][height][width]
                    shelf.params['word'] = mass

                    if shelf.params['turn'][user_check] == 1:
                        shelf.params['turn'][user_check] = 2
                        shelf.params['before'][user_check] = mass
                        shelf.params['che'][user_check][height][width] = mass

                    elif shelf.params['turn'][user_check] == 2:
                        shelf.params['che'][user_check][height][width] = mass
                        shelf.params['message'] = 'double'

                        if shelf.params['before'][user_check] == mass:
                            shelf.params['get'][user_check].append(mass)
                            shelf.params['turn'][user_check] = 100

                        else:
                            shelf.params['turn'][user_check] = 3


                    shelf.params['acount'][enemy] = shelf.params['acount'][user_check].copy()
                    shelf.params['che'][enemy] = shelf.params['che'][user_check].copy()

                elif 'load' in req.POST:
                    shelf.params['message'] = 'load'
                    if 3 <= shelf.params['turn'][user_check]:

                        shelf.params['message'] = 'loads'
                        shelf.params['before'][user_check] = '*'
                        shelf.params['turn'][user_check] = 0
                        shelf.params['turn'][enemy] = 1

                        shelf.all_check(user_check, enemy)

                        shelf.params['before_y'][user_check] = []
                        shelf.params['before_x'][user_check] = []

                else:
                    shelf.params['message']='None'
                    return redirect(to='/due/ans')

        except:
            return redirect(to='/due/ans')

        return redirect(to='/due/ans')

    def ans(shelf, req):
        return render(req, 'due/ans.html', shelf.params)

    def look(shelf, req):
        return render(req, 'due/look.html', shelf.params)


    def all_logout(shelf, req):
        user_check = str(req.user)

        shelf.params['entry'] -= 1
        shelf.params['turn'].pop(user_check)
        shelf.params['user'].remove(user_check)

        try:
            shelf.params['enemy'].pop(user_check)
            return redirect(to='/due/login')

        except:
            return redirect(to='/due/login')

        return redirect(to='/due/login')


    def signup(shelf, req):
        #user_check = req.user
        shelf.params['username'] = 'due'
        if req.method == 'POST':
            username = req.POST['username_data']
            password = req.POST['password_data']
            print('username=', username, 'password=', password)
            try:
                user = User.objects.create_user(username, '', password)
                shelf.params['username'] = 'just recomend'

            except IntegrityError:
                shelf.params['username'] = 'already'

        return render(req, 'due/signup.html', shelf.params)

    def login(shelf, req):

        if req.method == 'POST':
            username_data = req.POST['username_data']
            password_data = req.POST['password_data']
            user = authenticate(req, username=username_data, password=password_data)

            if user is not None:
                if username_data in shelf.params['user']:
                    return redirect(to='/due/login')

                else:
                    shelf.params['user'].append(username_data)
                    login(req, user)

                    shu = ''.join(random.sample(shelf.board, len(shelf.board)))

                    """
                    shu = shelf.board.copy()
                    random.shuffle(shu)
                    """

                    cell = [[] for i in range(shelf.H)]
                    k = 0
                    for i in range(shelf.H):
                        for j in range(shelf.W):
                            cell[i].append(shu[k])
                            k += 1


                    shelf.params['acount'][str(username_data)] = cell.copy()
                    shelf.params['get'][str(username_data)] = []
                    shelf.params['before'][str(username_data)] = '*'

                    shelf.params['before_x'][str(username_data)] = []
                    shelf.params['before_y'][str(username_data)] = []


                    check = [['*'] * shelf.W for i in range(shelf.H)]
                    shelf.params['che'][str(username_data)] = check.copy()

                    if shelf.params['entry'] == 0 or shelf.params['entry'] %2 == 0:
                        shelf.params['turn'][str(username_data)] = 1


                    else:
                        shelf.params['turn'][str(username_data)] = 0

                    shelf.params['entry']+=1

                    if shelf.params['entry'] %2 == 0:
                        entry_a = str(shelf.params['user'][shelf.params['entry']-2])
                        entry_b = str(shelf.params['user'][shelf.params['entry']-1])
                        shelf.params['enemy'][entry_a] = entry_b
                        shelf.params['enemy'][entry_b] = entry_a

                        shelf.params['acount'][entry_b] = shelf.params['acount'][entry_a].copy()
                        shelf.params['che'][entry_b] = shelf.params['che'][entry_a].copy()

                    return redirect(to='/due/ans')

        return render(req, 'due/login.html', shelf.params)

    def loc(shelf, req):
        if req.method == 'POST':
            username = req.POST['username_data']
            password = req.POST['password_data']

            if username == 'XXX':
                if password == 'XXX':
                    shelf.params['pass'] = 'OK'
                    return redirect(to='/due/look')

            return redirect(to='/due/loc')

        return render(req, 'due/loc.html', shelf.params)
