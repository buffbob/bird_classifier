from googleapiclient.discovery import build
from apiclient import discovery
import requests
from io import BytesIO
from PIL import Image as Im
import sys, os
import secrets
import glob
from classifier.models import Image, User, Bird

import flickrapi
from datetime import datetime
from sqlalchemy.exc import InvalidRequestError
from flask import current_app
from classifier import db

#cse_api_key = "this is the goggle api key location"
se_id = "this is the flicker api key location"  # for the flicker engine


######    these first methods work with google cse api ########
######################

def format_pic(url_path, size, destination, extension_list, query):
    resp=requests.get(url_path)
    content = BytesIO(resp.content)
    try:
        img = Im.open(content).resize(size)
        file, ext = os.path.splitext(url_path)
        flag = True
        if ext in extension_list:
            filename = os.path.join(secrets.token_hex(16) + ext)
            filepath = os.path.join(destination, filename)
            img.save(filepath)
            new_img = Image(query, filepath)
            db.session.add(new_img)
            db.session.commit()
            flag = False
    except IOError:
        print("shit cant download image")
    except:
        print("shit wierd error")

    return flag # False means file saved successfully

def make_dirs(query):
    formatted_query = query.replace(" ", "_")
    dir_path = os.path.join(current_app.root_path,"static/images/" + formatted_query)
    os.makedirs(dir_path)
    dest_landscape = os.path.join(dir_path, "landscape")
    dest_portrait = os.path.join(dir_path, "portrait")
    os.makedirs(dest_landscape)
    os.makedirs(dest_portrait)
    return dest_landscape, dest_portrait

def retrieve_items(query, key, se_id, number=100):
    num_images_to_download = number # that is all my api key allows
    resource=build('customsearch','v1',developerKey=cse_api_key).cse()
    result= resource.list(q=query, cx=se_id, searchType='image', start=38).execute()
    image_items = []
    for start_at in range(1,num_images_to_download,10):
        result= resource.list(q=query, cx=se_id, searchType='image', start=start_at).execute()
        image_items += result['items']
    return image_items


def scrape(query, key, se_id, number=100):
    dest_landscape, dest_portrait = make_dirs(query)
    image_items = retrieve_items(query, key, se_id, number)
    ext_list = ['.jpg', '.png']
    size_landscape = 300, 200
    size_portrait = 200, 300
    dest = ""
    count_portrait, count_landscape, count_rejected = 0, 0, 0
    flag_reject = False

    for each in image_items:
        link = each.get('link')
        width = each.get('image').get('width')
        height = each.get('image').get('height')
        ratio = each.get('image').get('height') / each.get('image').get('width')
        print(f"ratio={ratio}")
        if (ratio >= .6) and (ratio <= .8):
            dest = dest_landscape
            size = size_landscape
            if width > 300:
                flag_reject = format_pic(link, size, dest, ext_list, query)
                if not flag_reject:
                    count_landscape += 1
            else:
                flag_reject = True

        elif (ratio >= 1.2) and (ratio <= 1.5):
            dest = dest_portrait
            size = size_portrait
            if height > 300:
                flag_reject = format_pic(link, size, dest, ext_list, query)
                if not flag_reject:
                    count_portrait += 1
            else:
                flag_reject = True
        else:
            flag_reject = True
        if flag_reject:
            count_rejected += 1

    stats = count_landscape, count_portrait, count_rejected
    return stats


####################################
# these methods   and variables work with flicker
##################################

api_key='b63a6d85d9aab8c4b197b76dcbd76baa'
secret = '3c02d12d74e9d90e'
ext_list = ['.jpg', '.png']
size_landscape = (300, 200)
size_portrait = (200, 300)
size_square = (300, 300)
sizes = (size_landscape, size_portrait, size_square)
per_page=10
number_pages=10
#################

def retrieve_flickr_item_urls(flickr, query, api_key, secret, per_page, number_pages):
    """
    return a list of dict objects
    """
    url_list = []
    for i in range(1, number_pages + 1, 1):
        photos = flickr.photos.search(text=query, per_page=per_page, page = i)
        photo_list = photos['photos']['photo']    
        for each in photo_list:
            tmp = f"https://farm{each['farm']}.staticflickr.com/{each['server']}/{each['id']}_{each['secret']}.jpg"
            print(tmp)
            url_list.append(tmp)
    return url_list

def make_dir(query):
    """
    query: string to search for
    returns: dir_path, 
    """
    formatted_query = query.replace(" ", "_")
    formatted_query = formatted_query.replace("'","")
    dir_path = os.path.join(current_app.root_path,"static/images/downloaded/" + formatted_query)
    os.makedirs(dir_path)
    return dir_path, formatted_query

def retrieve_flickr_items_and_ids(flickr, query, api_key, secret, per_page, number_pages):
    """
    return tuple-- (list of dict objects(items), and list of ids)
    """
    item_list = []
    id_list = []
    for i in range(1, number_pages + 1, 1):
        photos = flickr.photos.search(text=query, per_page=per_page, page = i)
        photo_list = photos['photos']['photo']    
        for each in photo_list:
            item_list.append(each)
            id_list.append(each['id'])
    return item_list, id_list

def get_info_from_flickr_photos(flickr, id_list):
    """
    flickr: a flickr object with api_key/secret stored in Constructor
    id_list: list of photo_ids
    return: list of tuples(width,height,url)
    """
    info_list = []
    for each in id_list:
        sizes = flickr.photos.getSizes(photo_id=each)['sizes']['size'] # a list of all the available sizes for a photo
        tup = [(e['width'],e['height'],e['source']) for e in sizes if e['label'] == "Large"]
        if len(tup) > 0:
            info_list.append(tup[0])
    return info_list

def download_save_to_db(url_path, destination, extension_list, formatted_query, query):
    flag = True
    try:
        resp=requests.get(url_path)
        content = BytesIO(resp.content)
    except:
        print("Oops!",sys.exc_info()[0],"occured.")
        return flag
    try:
        img = Im.open(content)
        file, ext = os.path.splitext(url_path)
        if ext in extension_list:
            date_time_string = datetime.utcnow().strftime("%b_%d_%Y_%H:%M")
            filename = f"flickr_{date_time_string}_" + secrets.token_hex(16) + ext
            filepath = os.path.join(destination, filename)
            img.save(filepath)
            new_img = Image(species=query, downloaded_name=formatted_query, uri=filename)
            db.session.add(new_img)
            db.session.commit()
            # now need to update Bird to show downloaded
            bird = db.session.query(Bird).filter(Bird.Name==query).first()
            bird.downloaded = True
            db.session.commit()
            flag = False
    except IOError:
        print("Beaver Scat!",sys.exc_info()[0],"occured.")
    except InvalidRequestError:
        print("Oops IRE!",sys.exc_info()[0],"occured.")
    except:
        print("WTF")

    return flag # False means file saved successfully



def download_resize_save_to_db(url_path, size, destination, extension_list, formatted_query, query):
    flag = True
    try:
        resp=requests.get(url_path)
        content = BytesIO(resp.content)
    except:
        print("Oops!",sys.exc_info()[0],"occured.")
        return flag
    try:
        img = Im.open(content).resize(size)
        file, ext = os.path.splitext(url_path)
        if ext in extension_list:
            date_time_string = datetime.utcnow().strftime("%b_%d_%Y_%H:%M")
            filename = f"flickr_{date_time_string}_" + secrets.token_hex(16) + ext
            filepath = os.path.join(destination, filename)
            img.save(filepath)
            new_img = Image(species=query, downloaded_name=formatted_query, uri=filename)
            db.session.add(new_img)
            db.session.commit()
            # now need to update Bird to show downloaded
            bird = db.session.query(Bird).filter(Bird.Name==query).first()
            bird.downloaded = True
            db.session.commit()
            flag = False
    except IOError:
        print("Beaver Scat!",sys.exc_info()[0],"occured.")
    except InvalidRequestError:
        print("Oops IRE!",sys.exc_info()[0],"occured.")
    except:
        print("WTF")

    return flag # False means file saved successfully


def format_download_save_to_db_flickr_photos(info_list, formatted_query, dir_path, ext_list, query):
    """
    info_list: list of tuples- (width, height, uri)
    return: tuple(stats, rejected items list)
    """
    rejected = []
    count_downloaded, count_rejected = 0, 0  # for stats
    for e in info_list:
        flag_reject = True
        width, height, url = e
        #################  change needed why???????????
        ################# did it revert????????????????
        # width = int(width,10)
        # height = int(height,10)
        # ratio = height/(width)
        # print(f"ratio:{ratio}")
        flag_reject = download_save_to_db(url, dir_path, ext_list, formatted_query,query)
        if not flag_reject:
            count_downloaded += 1
        else:
                flag_reject = True

        rejected.append(e)
        flag_reject = True
        if flag_reject:
            count_rejected += 1
            
    stats = count_downloaded, count_rejected
    return stats, rejected


def scrap_flickr_for_photos(flickr, query, api_key, secret, per_page, number_pages, ext_list=(".png", '.jpg')):

    if not flickr:
        flickr = flickrapi.FlickrAPI(api_key, secret, format='parsed-json')
    
    dir_path, formatted_query = make_dir(query)
    
    items_list, ids_list = retrieve_flickr_items_and_ids(flickr, query, api_key, secret, per_page, number_pages)
    
    info_list = get_info_from_flickr_photos(flickr, ids_list)
    
    stats, rejected = format_download_save_to_db_flickr_photos(info_list, formatted_query, dir_path, ext_list,query)

    return stats, rejected
