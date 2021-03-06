from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth
from digispaceapp.models import *
import urllib
import smtplib
from smtplib import SMTPException

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import pdb
import csv
import json
# importing exceptions
from django.db import IntegrityError

import operator
from django.db.models import Q
from datetime import date, timedelta

# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import string
import random
from django.views.decorators.cache import cache_control
import ast
import urllib2

SERVER_URL = "http://52.66.133.35"
#SERVER_URL = "http://192.168.0.151:9090"


# SERVER_URL = "http://52.40.205.128"
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_category(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        country_list = Country.objects.filter(country_status='1')
        print '------country list-----',country_list
        city_list = City_Place.objects.filter(city_status='1')
        data = {'country_list':country_list,'city_list': city_list, 'username': request.session['login_user']}
        return render(request, 'Admin/add_category.html', data)

@csrf_exempt
def get_cat_sequence(request):
    city_id = request.POST.get('city_id')
    cat_city_obj = CategoryCityMap.objects.filter(city_place_id = city_id).order_by('sequence')
    i = 0
    sequence_list = []
    for city in cat_city_obj:
        i = i + 1
        sequnce_data = {
            'category_name' : city.category_id.category_name,
            'sequence' : city.sequence,
            'no' : str(i)
        }
        sequence_list.append(sequnce_data)
    print sequence_list
    data = {
        'success': 'true',
        'sequence_list':sequence_list
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


# TO GET THE STATE
def cget_state(request):
##    pdb.set_trace()
    country_id=request.GET.get('country_id')
    print '-----country id-------',country_id
    state_list = []
    data={}
    try:
        state = State.objects.filter(state_status='1',country_id=str(country_id))
        # a = '<option value='+ 'select State'+' </option>'
        # state_list.append(a)
        for sta in state:
            options_data = '<option value=' + str(sta.state_id) + '>' + sta.state_name + '</option>'
            state_list.append(options_data)
        print state_list
        data = {'state_list':state_list}
        print '--------data-----',data
    except Exception, e:
        print 'Exception ', e
        data = {'state_list':'No states available' }
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_country(request):
    country_list = Country.objects.filter(country_status='1')
    print '------country list-----',country_list
    for c in country_list:
        options_data = '<option value=' + str(c.country_id) + '>' + c.country_name + '</option>'
        country_list.append(options_data)
        print '------------city-list---------',country_list
    data = {'country_list':country_list}
    print '--------data-----',data
    return HttpResponse(json.dumps(data), content_type='application/json')

# TO GET THE CITY
def cget_city(request):
    state_id=request.GET.get('state_id')
    print '-----country id-------',state_id
    city_list = []
    data={}
    try:
        City = City_Place.objects.filter(city_status='1',state_id=str(state_id))
        # a = '<option value='+ 'select City'+' </option>'
        # city_list.append(a)
        for city in City:
            options_data = '<option value=' + str(city.city_place_id) + '>' + city.city_id.city_name + '</option>'
            city_list.append(options_data)
        print '------------city-list---------',city_list
        data = {'city_list':city_list}
        print '--------data-----',data
    except Exception, e:
        print 'Exception ', e
        data = {'city_list':'No city available' }
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_category(request):
    try:
        image = request.FILES['img']
        cat_color = request.POST.get('cat_color')
        x = request.POST.get('list')
        form_data = request.POST.get('form_data')
        cat_name = request.POST.get('cat_name')
        x = ast.literal_eval(x)
        y = [i for n, i in enumerate(x) if i not in x[n + 1:]]
        form_data = form_data.split('&')
        city_list=[]
        sequence_list=[]
        for k in range(len(form_data)):
            city_data = form_data[k].split('=')
            if city_data[0] == 'city':
                city_list.append(str(city_data[1]))
            if city_data[0] == 'sequence':
                sequence_list.append(str(city_data[1]))
        if city_list != ['']:
            print "city_list",city_list
            zipped_list = zip(city_list, sequence_list)
            print cheksamesequence(zipped_list)
            if cheksamesequence(zipped_list):
                print "check sum fail"
                data = {'message': 'Sequence for the selected city already exists, please view current sequence to know sequences used for various cities', 'success': 'false'}
                return HttpResponse(json.dumps(data), content_type='application/json')

        try:
            cat_obj = Category.objects.get(category_name=request.POST.get('cat_name'))
            cat_id = cat_obj.category_id
            print '-------cat id-------',cat_id
            # cat_obj = CategoryCityMap.objects.get(city_place_id=city_id,category_id=cat_id)
            print '---------city list in try------',city_list
            for c in city_list:
                print '---------city id-------',c
                cat_obj = CategoryCityMap.objects.get(city_place_id=c,category_id=cat_id)
                print '--------cat_obj------',cat_obj
                #category_obj = Category.objects.get(category_name=request.POST.get('cat_name'))
                data = {
                    'success': 'false',
                    'message': "Category already exist"
                }

        except Exception, e:
            print e
            cat_obj = Category(
                category_name=cat_name,
                category_created_by = request.session['login_user'],
                category_created_date=datetime.now(),
                category_updated_date=datetime.now(),
                category_status='1'
            )
            cat_obj.save()
            cat_obj.category_color = cat_color
            cat_obj.save()
            if image:
                cat_obj.category_image = request.FILES['img']
                cat_obj.save()
            if city_list != ['']:
                cat_map = create_city_map_obj(city_list, sequence_list, cat_obj)
                if cat_map == 'False':
                    data = {
                        'message': e,
                        'success': 'false'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
            for i in y:
                print i
                try:
                    if i['level_1']:
                        try:
                            cat_obj_level_1 = CategoryLevel1.objects.get(parent_category_id=cat_obj,
                                                                         category_name=i['level_1'])
                        except Exception:
                            cat_obj_level_1 = CategoryLevel1(
                                category_name=i['level_1'],
                                category_created_by = request.session['login_user'],
                                category_created_date=datetime.now(),
                                category_updated_date=datetime.now(),
                                category_status='1',
                                parent_category_id=cat_obj
                            )
                            cat_obj_level_1.save()
                    if i['level_2']:
                        for j in i['level_2']:
                            try:
                                cat_obj_level_2 = CategoryLevel2.objects.get(parent_category_id=cat_obj_level_1,
                                                                             category_name=j)
                            except Exception:
                                cat_obj_level_2 = CategoryLevel2(
                                    category_name=j,
                                    category_created_by = request.session['login_user'],
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_1
                                )
                                cat_obj_level_2.save()
                    if i['level_3']:
                        for j in i['level_3']:
                            try:
                                cat_obj_level_3 = CategoryLevel3.objects.get(parent_category_id=cat_obj_level_2,
                                                                             category_name=j)
                            except Exception:
                                cat_obj_level_3 = CategoryLevel3(
                                    category_name=j,
                                    category_created_by = request.session['login_user'],
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_2
                                )
                                cat_obj_level_3.save()
                    if i['level_4']:
                        for j in i['level_4']:
                            try:
                                cat_obj_level_4 = CategoryLevel4.objects.get(parent_category_id=cat_obj_level_3,
                                                                             category_name=j)
                            except Exception:
                                cat_obj_level_4 = CategoryLevel4(
                                    category_name=j,
                                    category_created_by = request.session['login_user'],
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_3
                                )
                                cat_obj_level_4.save()
                    if i['level_5']:
                        for j in i['level_5']:
                            try:
                                cat_obj_level_5 = CategoryLevel5.objects.get(parent_category_id=cat_obj_level_4,
                                                                             category_name=j)
                            except Exception:
                                cat_obj_level_5 = CategoryLevel5(
                                    category_name=j,
                                    category_created_by = request.session['login_user'],
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_4
                                )
                                cat_obj_level_5.save()
                except Exception as e:
                    data = {
                        'success': 'false',
                        'message': e,
                    }
            add_category_mail(cat_obj)
            add_category_sms(cat_obj)
            data = {
                'success': 'true',
                'message': "Category added successfully",
            }
            category_obj = Category.objects.get(category_name=request.POST.get('cat_name'))

            

    except Exception as e:
        print e
    return HttpResponse(json.dumps(data), content_type='application/json')

def add_category_sms(category_obj):

    authkey = "118994AIG5vJOpg157989f23"
    #mobiles = "7507542642"
    mobiles = "+919028527219"

    category_name= category_obj.category_name
    print '....................category_name.......',category_name
    message = "Hi Admin,"+'\n'+"Category "+category_name+" has been added successfully"
    sender = "CTHPLA"
    route = "4"
    country = "91"

    values = {
              'authkey' : authkey,
              'mobiles' : mobiles,
              'message' : message,
              'sender' : sender,
              'route' : route,
              'country' : country
              }

    url = "http://api.msg91.com/api/sendhttp.php"
    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    output = response.read()



def create_city_map_obj(city_list,sequence_list,cat_obj):
    try:
        zipped_list = zip(city_list, sequence_list)
        if zipped_list:
            for city_id, sequence in zipped_list:
                if city_id != '' and sequence != '':
                    map_obj = CategoryCityMap(
                        city_place_id=City_Place.objects.get(city_place_id=city_id),
                        sequence=sequence,
                        category_id=cat_obj,
                        creation_date=datetime.now(),
                        updation_date=datetime.now()
                    )
                    map_obj.save()
        return 'True'
    except Exception as e:
        print e
        return 'False'

def cheksamesequence(zipped_list):
    for city_id, sequence in zipped_list:
        if city_id != '' and sequence != '':
            try:
                cat_obj = CategoryCityMap.objects.get(city_place_id=City_Place.objects.get(city_place_id=city_id),
                                                      sequence=sequence)
                return True
            except:
                return False


def updatecheksamesequence(zipped_list, cat_id):
    # pdb.set_trace()
    cat_obj = Category.objects.get(category_id=cat_id)
    for city_id, sequence in zipped_list:
        if city_id != '' and sequence != '':
            cat_obj = CategoryCityMap.objects.filter(city_place_id=City_Place.objects.get(city_place_id=city_id),
                                                     sequence=sequence).exclude(category_id=cat_obj.category_id)
            if cat_obj:
                return False
            else:
                return True

def search_category_list(request):
    data = {}
    final_list = []
    clist=[]
    try:
        print '------------country------',request.GET.get('cid')
        print '------------state------',request.GET.get('sid')
        print '------------city------',request.GET.get('cityid')
        if request.GET.get('cid'):
            city_obj = City_Place.objects.filter(country_id=request.GET.get('cid'))
            cat_obj = CategoryCityMap.objects.filter(city_place_id__in=city_obj)
            print '-------cat_obj----',cat_obj
            for c in cat_obj:
                print c.category_id
                category_list.append(Category.objects.get(category_id = c.category_id))
                print '----------category list------',category_list
        for cat_obj in category_list:

            category_id = str(cat_obj.category_id)
            active_advert = 'No'
            cat_color = cat_obj.category_color
            advert_obj_list = Advert.objects.filter(category_id=category_id)
            obj_count = Advert.objects.filter(category_id=category_id).count()
            inactive_count = Advert.objects.filter(category_id=category_id,status='0').count()
            if advert_obj_list:
                if obj_count == inactive_count:
                    active_advert = 'No'
                else:
                    for advert_obj in advert_obj_list:
                        advert_id = str(advert_obj.advert_id)
                        pre_date = datetime.now().strftime("%d/%m/%Y")
                        pre_date = datetime.strptime(pre_date, "%d/%m/%Y")
                        advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                        end_date = advert_sub_obj.business_id.end_date
                        end_date = datetime.strptime(end_date, "%d/%m/%Y")
                        date_gap = end_date - pre_date
                        if int(date_gap.days) >= 0:
                            active_advert = 'Yes'

            category_name = cat_obj.category_name
            city_name = CategoryCityMap.objects.filter(category_id=cat_obj)
            city_list = ''
            if city_name:
                for city in city_name:
                    city_list = str(city.city_place_id.city_id.city_name) + ',' + city_list
                city_list = city_list[:-1]
            if not city_list:
                city_list = 'All'

            category_created_by = str(cat_obj.category_created_by)
            category_updated_by = str(cat_obj.category_updated_by)
            creation_date = str(cat_obj.category_created_date).split()[0]
            updation_date = str(cat_obj.category_updated_date).split()[0]
            if (cat_obj.category_status == '1'):
                status = 'Active'
                if active_advert == 'No':
                    delete = '<a id="' + str(
                        category_id) + '" onclick="delete_category(this.id)" style="text-align: center;letter-spacing: 5px;width:15%;" title="Delete"  ><i class="fa fa-trash"></i></a>'
                else:
                    delete = ''
                edit = '<a  id="' + str(category_id) + '" href="/edit-category/?category_id=' + str(
                    category_id) + '" style="text-align: center;letter-spacing: 5px;width:15%;" title="Edit" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-pencil"></i></a>'
                actions = edit + delete
            else:
                status = 'Inactive'
                active = '<a class="col-md-2" id="' + str(
                    cat_obj) + '" onclick="active_service(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;margin-left: 36px !important;" title="Activate" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-repeat"></i></a>'
                actions = active
            list = {'category_id':category_id,'status': status,'cat_color':cat_color, 'category_name': category_name, 'actions': actions, 'city_name': city_list,
                    'creation_date': creation_date,'category_updated_by':category_updated_by,'category_created_by':category_created_by, 'updation_date': updation_date, 'updated_by':cat_obj.category_updated_by}
            final_list.append(list)
        data = {'username':request.session['login_user'],'success': 'true', 'data': final_list}
        #print '----------data------',data
    except IntegrityError as e:
        print e
        data = {'username':request.session['login_user'],'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
        print '----------data------',data
    #data = {'username':request.session['login_user']}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_all_category_list_details(request):
    print '--------in category list---------',request.GET.get('category_id')
    c = request.GET.get('category_id')
    try:
        cat_obj = Category.objects.get(category_id=request.GET.get('category_id'))
        cat_l1_obj = CategoryLevel1.objects.filter(parent_category_id=str(cat_obj.category_id))
        cat_str = ''
        i = 0
        for cat_l1 in cat_l1_obj:
            i = int(i) + 1
            level_name = "level"+c+"_" + str(i)
            cat_l2_obj = CategoryLevel2.objects.filter(parent_category_id=str(cat_l1.category_id))
            if cat_l2_obj:
                icon = 'fa-minus-square'
                click_function = ''
                flag_click = "onclick=collapse_div('" + level_name + "',this)"
                cursor_style = ''
            else:
                icon = ''
                click_function = "onclick='showTable(this," + str(cat_l1.category_id) + ",1)'"
                flag_click = ''
                cursor_style = "style='cursor: pointer;'"
            cat_str = cat_str + "<div class='col-lg-12 padding_left0'>" \
                                "<div class='col-lg-1' style='padding:0px;'>" \
                                "<a class='fa " + icon + "' " + flag_click + "></a></div>" \
                                                                             "<div class='col-lg-11'><label " + cursor_style + " class='label_item' " + click_function + ">" + cat_l1.category_name + "</label>" \
                                                                                                                                                                                                      "</div></div>"
            j = 0
            for cat_l2 in cat_l2_obj:
                j = int(j) + 1
                level_name_1 = "level"+c+"_" + str(i) + "_" + str(j)
                cat_l3_obj = CategoryLevel3.objects.filter(parent_category_id=str(cat_l2.category_id))
                if cat_l3_obj:
                    icon = 'fa-minus-square'
                    click_function = ''
                    flag_click = "onclick=collapse_div('" + level_name_1 + "',this)"
                    cursor_style = ''
                else:
                    icon = ''
                    click_function = "onclick='showTable(this," + str(cat_l2.category_id) + ",2)'"
                    flag_click = ''
                    cursor_style = "style='cursor: pointer;'"
                cat_str = cat_str + "<div class='row col_div " + level_name + "' style='margin-left: 6.33333%;'>" \
                                                                              "<div class='col-lg-12 padding_left0'>" \
                                                                              "<div class='col-lg-1' style='padding:0px;'>" \
                                                                              "<a class='fa " + icon + "' " + flag_click + "></a></div>" \
                                                                                                                           "<div class='col-lg-11'><label " + cursor_style + " class='label_item' " + click_function + ">" + cat_l2.category_name + "</label>" \
                                                                                                                                                                                                                                                    "</div></div>"
                k = 0
                for cat_l3 in cat_l3_obj:
                    k = int(k) + 1
                    level_name_2 = "level"+c+"_" + str(i) + "_" + str(j) + "_" + str(k)
                    cat_l4_obj = CategoryLevel4.objects.filter(parent_category_id=str(cat_l3.category_id))
                    if cat_l4_obj:
                        icon = 'fa-minus-square'
                        click_function = ''
                        flag_click = "onclick=collapse_div('" + level_name_2 + "',this)"
                        cursor_style = ''
                    else:
                        icon = ''
                        click_function = "onclick='showTable(this," + str(cat_l3.category_id) + ",3)'"
                        flag_click = ''
                        cursor_style = "style='cursor: pointer;'"
                    cat_str = cat_str + "<div class='row col_div " + level_name_1 + "' style='margin-left: 6.33333%;'>" \
                                                                                    "<div class='col-lg-12 padding_left0'>" \
                                                                                    "<div class='col-lg-1' style='padding:0px;'>" \
                                                                                    "<a class='fa " + icon + "' " + flag_click + "></a></div>" \
                                                                                                                                 "<div class='col-lg-11'><label " + cursor_style + " class='label_item' " + click_function + ">" + cat_l3.category_name + "</label>" \
                                                                                                                                                                                                                                                          "</div></div>"
                    l = 0
                    for cat_l4 in cat_l4_obj:
                        l = int(l) + 1
                        level_name_3 = "level"+c+"_" + str(i) + "_" + str(j) + "_" + str(k) + "_" + str(l)
                        cat_l5_obj = CategoryLevel5.objects.filter(parent_category_id=str(cat_l4.category_id))
                        if cat_l5_obj:
                            icon = 'fa-minus-square'
                            click_function = ''
                            flag_click = "onclick=collapse_div('" + level_name_3 + "',this)"
                            cursor_style = ''
                        else:
                            icon = ''
                            click_function = "onclick='showTable(this," + str(cat_l4.category_id) + ",4)'"
                            flag_click = ''
                            cursor_style = "style='cursor: pointer;'"
                        cat_str = cat_str + "<div class='row col_div " + level_name_2 + "' style='margin-left: 6.33333%;'>" \
                                                                                        "<div class='col-lg-12 padding_left0'>" \
                                                                                        "<div class='col-lg-1' style='padding:0px;'>" \
                                                                                        "<a class='fa " + icon + "' " + flag_click + "></a></div>" \
                                                                                                                                     "<div class='col-lg-11'><label " + cursor_style + " class='label_item' " + click_function + " >" + cat_l4.category_name + "</label>" \
                                                                                                                                                                                                                                                               "</div></div>"
                        for cat_l5 in cat_l5_obj:
                            cursor_style = "style='cursor: pointer;'"
                            cat_str = cat_str + "<div class='row col_div " + level_name_3 + "' style='margin-left: 6.33333%;'>" \
                                                                                            "<div class='col-lg-12 padding_left0'>" \
                                                                                            "<div class='col-lg-1' style='padding:0px;'>" \
                                                                                            "<a class='fa '></a></div>" \
                                                                                            "<div class='col-lg-11'><label " + cursor_style + " class='label_item' onclick='showTable(this," + str(
                                cat_l5.category_id) + ",5)'>" + cat_l5.category_name + "</label>" \
                                                                                       "</div></div>"
                            cat_str = cat_str + '</div>'
                        cat_str = cat_str + '</div>'
                    cat_str = cat_str + '</div>'
                cat_str = cat_str + '</div>'
            cat_str = cat_str + '</div>'
        data = {
            'success': 'true',
            'message': "Service already exist",
            'cat_str': cat_str
        }
    except Exception, e:
        print e
        data = {
            'success': 'false',
            'message': "Service added successfully"
        }
    print '------------data------',data
    return HttpResponse(json.dumps(data), content_type='application/json')




def category_list(request):
    try:
        data = {}
        final_list = []
        try:
            category_list = Category.objects.all()
            for cat_obj in category_list:
                category_id = str(cat_obj.category_id)
                active_advert = 'No'
                advert_obj_list = Advert.objects.filter(category_id=category_id)
                obj_count = Advert.objects.filter(category_id=category_id).count()
                inactive_count = Advert.objects.filter(category_id=category_id,status='0').count()
                if advert_obj_list:
                    if obj_count == inactive_count:
                        active_advert = 'No'
                    else:
                        for advert_obj in advert_obj_list:
                            advert_id = str(advert_obj.advert_id)
                            pre_date = datetime.now().strftime("%d/%m/%Y")
                            pre_date = datetime.strptime(pre_date, "%d/%m/%Y")
                            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                            end_date = advert_sub_obj.business_id.end_date
                            end_date = datetime.strptime(end_date, "%d/%m/%Y")
                            date_gap = end_date - pre_date
                            if int(date_gap.days) >= 0:
                                active_advert = 'Yes'

                category_name = cat_obj.category_name
                city_name = CategoryCityMap.objects.filter(category_id=cat_obj)
                city_list = ''
                if city_name:
                    for city in city_name:
                        city_list = str(city.city_place_id.city_id.city_name) + ',' + city_list
                    city_list = city_list[:-1]
                if not city_list:
                    city_list = 'All'
                creation_date = str(cat_obj.category_created_date).split()[0]
                updation_date = str(cat_obj.category_updated_date).split()[0]
                if (cat_obj.category_status == '1'):
                    status = 'Active'
                    if active_advert == 'No':
                        delete = '<a id="' + str(
                            category_id) + '" onclick="delete_category(this.id)" style="text-align: center;letter-spacing: 5px;width:15%;" title="Delete"  ><i class="fa fa-trash"></i></a>'
                    else:
                        delete = ''
                    edit = '<a  id="' + str(category_id) + '" href="/edit-category/?category_id=' + str(
                        category_id) + '" style="text-align: center;letter-spacing: 5px;width:15%;" title="Edit" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-pencil"></i></a>'
                    actions = edit + delete
                else:
                    status = 'Inactive'
                    active = '<a class="col-md-2" id="' + str(
                        cat_obj) + '" onclick="active_service(this.id);" style="text-align: center;letter-spacing: 5px;width:15%;margin-left: 36px !important;" title="Activate" class="edit" data-toggle="modal" href="#edit_subscription"><i class="fa fa-repeat"></i></a>'
                    actions = active
                list = {'status': status, 'category_name': category_name, 'actions': actions, 'city_name': city_list,
                        'creation_date': creation_date, 'updation_date': updation_date, 'updated_by':cat_obj.category_updated_by}
                final_list.append(list)
            data = {'success': 'true', 'data': final_list}
        except IntegrityError as e:
            print e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print e
    except Exception, e:
        print 'Exception ', e
    # print '====data============',data
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def delete_category(request):
    try:
        cat_obj = Category.objects.get(category_id=request.POST.get('category_id'))
        cat_obj.category_status = '0'
        cat_obj.save()
        data = {'message': 'User Role De-activeted Successfully', 'success': 'true'}
        inactive_category_mail(cat_obj)
        delete_category_sms(cat_obj)

    except IntegrityError as e:
        print e
    except Exception, e:
        print e
        print "Final Data: ", data
    return HttpResponse(json.dumps(data), content_type='application/json')


def delete_category_sms(cat_obj):
    print 'sssssssssssssssssssssss'
    
    category_name= cat_obj.category_name
    authkey = "118994AIG5vJOpg157989f23"
    mobiles = "+919028527219"
    message = "Hi Admin,"+'\n'+"Category "+category_name+" has been deactivated successfully "
    sender = "CTHPLA"
    route = "4"
    country = "91"
    values = {
              'authkey' : authkey,
              'mobiles' : mobiles,
              'message' : message,
              'sender' : sender,
              'route' : route,
              'country' : country
              }

    url = "http://api.msg91.com/api/sendhttp.php"
    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    output = response.read()



@csrf_exempt
def delete_sub_category(request):
    try:
        level_name = request.POST.get('sub_cat_level')
        cat_id = request.POST.get('sub_cat_id')
        obj_list = []
        if level_name == 'level_1':
            cat_obj = CategoryLevel1.objects.get(category_id=cat_id)
            Advert.objects.filter(category_level_1 = cat_id).delete()
            cat_obj.delete()
        if level_name == 'level_2':
            cat_obj = CategoryLevel2.objects.get(category_id=cat_id)
            Advert.objects.filter(category_level_2 = cat_id).delete()
            cat_obj.delete()
        if level_name == 'level_3':
            cat_obj = CategoryLevel3.objects.get(category_id=cat_id)
            Advert.objects.filter(category_level_3 = cat_id).delete()
            cat_obj.delete()
        if level_name == 'level_4':
            cat_obj = CategoryLevel4.objects.get(category_id=cat_id)
            Advert.objects.filter(category_level_4 = cat_id).delete()
            cat_obj.delete()
        if level_name == 'level_5':
            cat_obj = CategoryLevel5.objects.get(category_id=cat_id)
            Advert.objects.filter(category_level_5 = cat_id).delete()
            cat_obj.delete()
        data = {'message': 'User Role De-activeted Successfully', 'success': 'true'}

    except IntegrityError as e:
        print e
    except Exception, e:
        print e
        print "Final Data: ", data
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_city(request):
    city_list = []
    try:
        city_objs = City_Place.objects.filter(city_status='1').order_by('city_id__city_name')
        for city in city_objs:
            options_data = '<option value=' + str(
                city.city_place_id) + '>' + city.city_id.city_name + '</option>'
            city_list.append(options_data)
            print city_list
        data = {'city_list': city_list}

    except Exception, ke:
        print ke
        data = {'city_list': 'none', 'message': 'No city available'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_category(request):
    if not request.user.is_authenticated():
        return redirect('backoffice')
    else:
        try:
            data = {}
            final_list = []
            sub_category1_list = []
            sub_category2_list = []
            sub_category3_list = []
            sub_category4_list = []
            sub_category5_list = []
            city_list = City_Place.objects.filter(city_status='1')
            selected_city_list = []
            selected_sequence_list = []

            try:
                category = Category.objects.get(category_id=request.GET.get('category_id'))
                category_id = str(category.category_id)
                category_name = str(category.category_name)
                city_name = CategoryCityMap.objects.get(category_id=category)
                
                city_obj = str(city_name.city_place_id.city_id)
                ct_id = str(city_name.city_place_id)
                state_obj = str(city_name.city_place_id.state_id)
                country_obj = city_name.city_place_id.country_id
                seq_obj = str(city_name.sequence)
                
                country_list = Country.objects.all()
                state_list = State.objects.filter(country_id = str(city_name.city_place_id.country_id.country_id))
                
                city_list = City_Place.objects.filter(state_id = str(city_name.city_place_id.state_id.state_id))
                

                active_advert = 'No'

                advert_obj_list = Advert.objects.filter(category_id = category_id)
                for advert_obj in advert_obj_list:
                    advert_id = str(advert_obj.advert_id)
                    pre_date = datetime.now().strftime("%d/%m/%Y")
                    pre_date = datetime.strptime(pre_date, "%d/%m/%Y")
                    advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                    end_date = advert_sub_obj.business_id.end_date
                    end_date = datetime.strptime(end_date, "%d/%m/%Y")
                    date_gap = end_date - pre_date
                    if int(date_gap.days) >= 0:
                        active_advert = 'Yes'

                
                sub_category1 = CategoryLevel1.objects.filter(parent_category_id=category)
                if sub_category1:
                    for cat in sub_category1:
                        sub_category2 = CategoryLevel2.objects.filter(parent_category_id=cat)
                        if sub_category2:
                            has_subcategory = 'Yes'
                        else:
                            has_subcategory = 'No'
                        active_advert = 'No'

                        advert_obj_list = Advert.objects.filter(category_level_1 = cat.category_id)
                        for advert_obj in advert_obj_list:
                            advert_id = str(advert_obj.advert_id)
                            pre_date = datetime.now().strftime("%d/%m/%Y")
                            pre_date = datetime.strptime(pre_date, "%d/%m/%Y")
                            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                            end_date = advert_sub_obj.business_id.end_date
                            end_date = datetime.strptime(end_date, "%d/%m/%Y")
                            date_gap = end_date - pre_date
                            if int(date_gap.days) >= 0:
                                active_advert = 'Yes'

                        category1_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'has_subcategory':has_subcategory,
                                            'active_advert':active_advert
                                          }

                        sub_category1_list.append(category1_list)
                length1 = len(sub_category1_list)
                
                sub_category2 = CategoryLevel2.objects.filter(parent_category_id__in=sub_category1)
                if sub_category2:
                    for cat in sub_category2:
                        sub_category3 = CategoryLevel3.objects.filter(parent_category_id=cat)
                        if sub_category3:
                            has_subcategory = 'Yes'
                        else:
                            has_subcategory = 'No'

                        active_advert = 'No'

                        advert_obj_list = Advert.objects.filter(category_level_2 = cat.category_id)
                        for advert_obj in advert_obj_list:
                            advert_id = str(advert_obj.advert_id)
                            pre_date = datetime.now().strftime("%d/%m/%Y")
                            pre_date = datetime.strptime(pre_date, "%d/%m/%Y")
                            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                            end_date = advert_sub_obj.business_id.end_date
                            end_date = datetime.strptime(end_date, "%d/%m/%Y")
                            date_gap = end_date - pre_date
                            if int(date_gap.days) >= 0:
                                active_advert = 'Yes'

                        category2_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'has_subcategory': has_subcategory,
                                            'active_advert':active_advert
                                          }
                        sub_category2_list.append(category2_list)
                length2 = len(sub_category2_list)
                
                sub_category3 = CategoryLevel3.objects.filter(parent_category_id__in=sub_category2)
                if sub_category3:
                    for cat in sub_category3:
                        sub_category4 = CategoryLevel4.objects.filter(parent_category_id=cat)
                        if sub_category4:
                            has_subcategory = 'Yes'
                        else:
                            has_subcategory = 'No'

                        active_advert = 'No'

                        advert_obj_list = Advert.objects.filter(category_level_3 = cat.category_id)
                        for advert_obj in advert_obj_list:
                            advert_id = str(advert_obj.advert_id)
                            pre_date = datetime.now().strftime("%d/%m/%Y")
                            pre_date = datetime.strptime(pre_date, "%d/%m/%Y")
                            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                            end_date = advert_sub_obj.business_id.end_date
                            end_date = datetime.strptime(end_date, "%d/%m/%Y")
                            date_gap = end_date - pre_date
                            if int(date_gap.days) >= 0:
                                active_advert = 'Yes'

                        category3_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'has_subcategory':has_subcategory,
                                            'active_advert':active_advert
                                          }
                        sub_category3_list.append(category3_list)
                length3 = len(sub_category3_list)
                
                sub_category4 = CategoryLevel4.objects.filter(parent_category_id__in=sub_category3)
                if sub_category4:
                    for cat in sub_category4:
                        sub_category5 = CategoryLevel5.objects.filter(parent_category_id=cat)
                        if sub_category5:
                            has_subcategory = 'Yes'
                        else:
                            has_subcategory = 'No'

                        active_advert = 'No'

                        advert_obj_list = Advert.objects.filter(category_level_4 = cat.category_id)
                        for advert_obj in advert_obj_list:
                            advert_id = str(advert_obj.advert_id)
                            pre_date = datetime.now().strftime("%d/%m/%Y")
                            pre_date = datetime.strptime(pre_date, "%d/%m/%Y")
                            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                            end_date = advert_sub_obj.business_id.end_date
                            end_date = datetime.strptime(end_date, "%d/%m/%Y")
                            date_gap = end_date - pre_date
                            if int(date_gap.days) >= 0:
                                active_advert = 'Yes'

                        category4_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'has_subcategory':has_subcategory,
                                            'active_advert':active_advert
                                          }
                        sub_category4_list.append(category4_list)
                length4 = len(sub_category4_list)
                
                sub_category5 = CategoryLevel5.objects.filter(parent_category_id__in=sub_category4)
                if sub_category5:
                    for cat in sub_category5:
                        active_advert = 'No'

                        advert_obj_list = Advert.objects.filter(category_level_5 = cat.category_id)
                        for advert_obj in advert_obj_list:
                            advert_id = str(advert_obj.advert_id)
                            pre_date = datetime.now().strftime("%d/%m/%Y")
                            pre_date = datetime.strptime(pre_date, "%d/%m/%Y")
                            advert_sub_obj = AdvertSubscriptionMap.objects.get(advert_id=advert_id)
                            end_date = advert_sub_obj.business_id.end_date
                            end_date = datetime.strptime(end_date, "%d/%m/%Y")
                            date_gap = end_date - pre_date
                            if int(date_gap.days) >= 0:
                                active_advert = 'Yes'

                        category5_list = {
                                            'category_id':str(cat.category_id),
                                            'category_name': cat.category_name,
                                            'parent_category_id':str(cat.parent_category_id),
                                            'active_advert':active_advert
                                          }
                        sub_category5_list.append(category5_list)
                length5 = len(sub_category5_list)
                

                data = {'username': request.session['login_user'], 'length5': length5,'ct_id':ct_id,
                        'length4': length4, 'length3': length3, 'length2': length2, 'length1': length1,
                        'category_id': category_id, 'city_list': city_list, 'state_list': state_list, 'country_list': country_list,
                        'city_id': city_obj, 'state_id': state_obj, 'country_id': country_obj, 'city_sequence': seq_obj,
                        'success': 'true', 'sub_category5_list': sub_category5_list,'cat_img':SERVER_URL + category.category_image.url,
                        'sub_category4_list': sub_category4_list, 'sub_category3_list': sub_category3_list,
                        'sub_category2_list': sub_category2_list, 'category_name': category_name,'active_advert':active_advert,
                        'sub_category1_list': sub_category1_list, 'cat_color':str(category.category_color) or '#000000'}

            except IntegrityError as e:
                print e
                data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
        except MySQLdb.OperationalError, e:
            print e
        except Exception, e:
            print 'Exception ', e
        return render(request, 'Admin/edit_category.html', data)

@csrf_exempt
def update_category(request):
    #print request.POST
    cat_color = request.POST.get('cat_color')
    print cat_color
    
    x = request.POST.get('list')
    form_data = request.POST.get('form_data')
    cat_name = request.POST.get('cat_name')
    x = ast.literal_eval(x)
    y = [i for n, i in enumerate(x) if i not in x[n + 1:]]
    form_data = form_data.split('&')
    city_list = []
    sequence_list = []
    for k in range(len(form_data)):
        city_data = form_data[k].split('=')
        if city_data[0] == 'category_id':
            category_id = str(city_data[1])
        if city_data[0] == 'city':
            city_list.append(str(city_data[1]))
        if city_data[0] == 'sequence':
            sequence_list.append(str(city_data[1]))
    if city_list != ['']:
        zipped_list = zip(city_list, sequence_list)
        if not (updatecheksamesequence(zipped_list, category_id)):
            data = {
                'message': 'Sequence for the selected city already exists, please view current sequence to know sequences used for various cities',
                'success': 'false'}
            return HttpResponse(json.dumps(data), content_type='application/json')
    try:
        cat_obj = Category.objects.get(category_id=category_id)
        cat_obj.category_name = cat_name
        cat_obj.category_updated_date = datetime.now()
        cat_obj.category_updated_by = request.session['login_user']
        cat_obj.category_color = cat_color
        cat_obj.save()
        try:
            cat_obj.category_image = request.FILES['img']
            cat_obj.save()
        except KeyError as e:
            pass
        CategoryCityMap.objects.filter(category_id=cat_obj).delete()
        if city_list != ['']:
            cat_map = create_city_map_obj(city_list, sequence_list, cat_obj)
            if cat_map == 'False':
                data = {
                    'message': 'Error',
                    'success': 'false'
                }
                return HttpResponse(json.dumps(data), content_type='application/json')
        for i in y:
            try:
                if i['level_1']:
                    try:
                        cat_obj_level_1 = CategoryLevel1.objects.get(parent_category_id=cat_obj,
                                                                     category_id=i['level_id_1'])
                        cat_obj_level_1.category_name = i['level_1']
                        cat_obj_level_1.save()
                    except Exception:
                        cat_obj_level_1 = CategoryLevel1(
                            category_name=i['level_1'],
                            category_created_date=datetime.now(),
                            category_updated_date=datetime.now(),
                            category_status='1',
                            parent_category_id=cat_obj
                        )
                        cat_obj_level_1.save()
                if i['level_2']:
                    for j,k in zip(i['level_2'],i['level_id_2']):
                        if j:
                            try:
                                cat_obj_level_2 = CategoryLevel2.objects.get(parent_category_id=cat_obj_level_1,
                                                                             category_id=k)
                                cat_obj_level_2.category_name = j
                                cat_obj_level_2.save()
                            except Exception:
                                cat_obj_level_2 = CategoryLevel2(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_1
                                )
                                cat_obj_level_2.save()
                if i['level_3']:

                    for j, k in zip(i['level_3'], i['level_id_3']):
                        if j:
                            try:
                                cat_obj_level_3 = CategoryLevel3.objects.get(parent_category_id=cat_obj_level_2,
                                                                             category_id=k)
                                cat_obj_level_3.category_name = j
                                cat_obj_level_3.save()
                            except Exception:
                                cat_obj_level_3 = CategoryLevel3(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_2
                                )
                                cat_obj_level_3.save()
                if i['level_4']:

                    for j, k in zip(i['level_4'], i['level_id_4']):
                        if j:
                            try:
                                cat_obj_level_4 = CategoryLevel4.objects.get(parent_category_id=cat_obj_level_3,
                                                                             category_id=k)
                                cat_obj_level_4.category_name = j
                                cat_obj_level_4.save()
                            except Exception:
                                cat_obj_level_4 = CategoryLevel4(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_3
                                )
                                cat_obj_level_4.save()
                if i['level_5']:
                    #print i['level_id_5']
                    for j, k in zip(i['level_5'], i['level_id_5']):
                        if j:
                            try:
                                cat_obj_level_5 = CategoryLevel5.objects.get(parent_category_id=cat_obj_level_4,
                                                                             category_id=k)
                                cat_obj_level_5.category_name = j
                                cat_obj_level_5.save()
                            except Exception:
                                cat_obj_level_5 = CategoryLevel5(
                                    category_name=j,
                                    category_created_date=datetime.now(),
                                    category_updated_date=datetime.now(),
                                    category_status='1',
                                    parent_category_id=cat_obj_level_4
                                )
                                cat_obj_level_5.save()
            except Exception as e:
                data = {
                    'success': 'false',
                    'message': e,
                }
        data = {
            'success': 'true',
            'message': "Category added successfully",
        }
        edit_category_mail(cat_obj)
        edit_category_sms(cat_obj)
    except Exception, e:
        print "==============EXCEPTION+++++++++++++++++++++++++++++++++++++", e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_category_sms(cat_obj):

    authkey = "118994AIG5vJOpg157989f23"
    mobiles = "+919028527219"

    category_name= cat_obj.category_name
    print '....................category_name.......',category_name
    message = "Hi Admin,"+'\n'+"Category "+category_name+" has been updated successfully"
    sender = "CTHPLA"
    route = "4"
    country = "91"
    print 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk'



    values = {
              'authkey' : authkey,
              'mobiles' : mobiles,
              'message' : message,
              'sender' : sender,
              'route' : route,
              'country' : country
              }

    url = "http://api.msg91.com/api/sendhttp.php"
    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    output = response.read()
    print output


def add_category_mail(cat_obj):
    gmail_user = "donotreply@city-hoopla.com"# "cityhoopla2016"
    gmail_pwd =  "Hoopla123#"#"cityhoopla@2016"
    FROM = 'Team CityHoopla<donotreply@city-hoopla.com>'
    TO = ['cityhoopla2016@gmail.com']
    # pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(
            cat_obj.category_name) + " " + "has been added successfully." + "\nTo view complete details visit portal and follow - Reference Data -> Category" + "\n\nThank You," + '\n' + "CityHoopla Team"
        SUBJECT = "Category Added Successfully!"
        #server = smtplib.SMTP_SSL()
        #server = smtplib.SMTP("smtp.gmail.com", 587) 
        server = smtplib.SMTP("smtpout.asia.secureserver.net", 80)
        #server = smtplib.SMTP_TSL('smtpout.secureserver.net', 465)
        server.ehlo()
        #server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


def edit_category_mail(cat_obj):
    gmail_user = "donotreply@city-hoopla.com"# "cityhoopla2016"
    gmail_pwd =  "Hoopla123#"#"cityhoopla@2016"
    FROM = 'Team CityHoopla<donotreply@city-hoopla.com>'
    TO = ['cityhoopla2016@gmail.com']
    # pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(
            cat_obj.category_name) + " " + "has been updated successfully." + "\nTo view complete details visit portal and follow - Reference Data -> Category" + "\n\nThank You," + '\n' + "CityHoopla Team"
        SUBJECT = "Category Updated Successfully!"
        #server = smtplib.SMTP_SSL()
        #server = smtplib.SMTP("smtp.gmail.com", 587) 
        server = smtplib.SMTP("smtpout.asia.secureserver.net", 80)
        #server = smtplib.SMTP_TSL('smtpout.secureserver.net', 465)
        server.ehlo()
        #server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


def inactive_category_mail(cat_obj):
    gmail_user = "donotreply@city-hoopla.com"# "cityhoopla2016"
    gmail_pwd =  "Hoopla123#"#"cityhoopla@2016"
    FROM = 'Team CityHoopla<donotreply@city-hoopla.com>'
    TO = ['cityhoopla2016@gmail.com']
    # pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(
            cat_obj.category_name) + " " + "has been deactivated successfully." + "\n\nThank You," + '\n' + "CityHoopla Team"
        SUBJECT = "Category Deactivated Successfully!"
        #server = smtplib.SMTP_SSL()
        #server = smtplib.SMTP("smtp.gmail.com", 587) 
        server = smtplib.SMTP("smtpout.asia.secureserver.net", 80)
        #server = smtplib.SMTP_TSL('smtpout.secureserver.net', 465)
        server.ehlo()
        #server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


@csrf_exempt
def active_category(request):
    # pdb.set_trace()
    try:
        cat_obj = Category.objects.get(category_id=request.POST.get('category_id'))
        cat_obj.category_status = '1'
        cat_obj.save()
        data = {'message': 'Category activated Successfully', 'success': 'true'}
        category_active_mail(cat_obj)

    except IntegrityError as e:
        print e
    except Exception, e:
        print e
    print "Final Data: ", data
    return HttpResponse(json.dumps(data), content_type='application/json')


def category_active_mail(cat_obj):
    gmail_user = "donotreply@city-hoopla.com"# "cityhoopla2016"
    gmail_pwd =  "Hoopla123#"#"cityhoopla@2016"
    FROM = 'Team CityHoopla<donotreply@city-hoopla.com>'
    TO = ['cityhoopla2016@gmail.com']
    # pdb.set_trace()
    try:
        TEXT = "Hi Admin,\nCategory " + str(
            cat_obj.category_name) + " " + " has been activated successfully.\nTo view complete details visit portal and follow - Reference Data -> Category\n\n Thank You," + '\n' + "CityHoopla Team"
        SUBJECT = "Category Activated Successfully!"
        #server = smtplib.SMTP_SSL()
        #server = smtplib.SMTP("smtp.gmail.com", 587) 
        server = smtplib.SMTP("smtpout.asia.secureserver.net", 80)
        #server = smtplib.SMTP_TSL('smtpout.secureserver.net', 465)
        server.ehlo()
        #server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


def save_subcategory(level, subcategory_list, category_object):
    i = 0
    subcategory_obj_list = Category.objects.filter(has_category=category_object, level=level)
    for category in subcategory_obj_list:
        category.category_name = subcategory_list[i]
        category.save()
        i = i + 1

    if i < len(subcategory_list):
        for j in range(i, len(subcategory_list)):
            category_obj = Category(
                category_name=subcategory_list[j],
                level=level,
                category_created_date=datetime.now(),
                category_updated_date=datetime.now(),
                category_status='1'
            )
            category_obj.save()
            category_obj.has_category = category_object
            category_obj.save()
            j = j + 1
