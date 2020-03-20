from flask import flash, render_template, request, Blueprint, redirect, url_for, current_app
from sqlalchemy import desc, asc,  and_
from flask_login import current_user,logout_user, login_user, login_required
from classifier.models import User, Image, Bird
from classifier.admin.forms import ClassifyForm
from classifier import app, db, bcrypt
import classifier.image_utils as iu
import flickrapi


admin = Blueprint("admin", __name__)

@admin.route("/classify/<int:id>", methods=['GET', 'POST'])
@login_required
def classify(id):
    if request.args.get('count'):
        count = int(request.args.get('count'))
    else:
        count = 0
    arg_dic = {
        "user": User.query.filter(User.id == id).first(),
        "id": id}
    if request.method == "GET":
        birds_downloaded = Bird.query.filter(Bird.downloaded).all()
        birds_ready_to_classify = []
        for b in birds_downloaded:
            num_images_per_bird = len(Image.query.filter(Image.species==b.Name).all())
            num_images_classified = len(db.session.query(Image).filter(and_(Image.species==b.Name, Image.is_classified)).all())
            if num_images_per_bird > num_images_classified:
                birds_ready_to_classify.append(b.Name)

        arg_dic["ready_to_classify"] = birds_ready_to_classify
        return render_template("classify.html", data=arg_dic)
    if request.method == "POST":
        birdname = request.form['PickBird']

        return redirect(url_for("admin.classifying", id=id, birdname=birdname, first_flag=True,
                                reject_flag=False, count=count))


@admin.route("/classifying/<int:id>", methods=['GET', 'POST'])
@login_required
def classifying(id):
    form = ClassifyForm()
    delete_fields = "False"
    count = 0
    birdname = request.args.get('birdname')
    imagez='fred'

    if request.method == "GET":
        if (request.args.get('count')):
            count = int(request.args.get('count'))
        if request.args.get('reject_flag') == "True":
            temp_id = int(request.args.get("image_id"))
            db.session.query(Image).filter(Image.id == temp_id).delete()
            db.session.commit()
            delete_fields = "True"
        if request.args.get("unsure_flag") == 'True':
            temp_id = int(request.args.get("image_id"))
            imagez = db.session.query(Image).filter(Image.id == temp_id).first()
            newnum = imagez.num_classifications + 1
            imagez.num_classifications = newnum
            db.session.commit()
            delete_fields = "True"

    if form.validate_on_submit():
        birdname = form.birdname.data
        count = form.count.data
        temp_id = form.image_id.data
        image_folder = form.image_folder.data
        ###########        make changes to Image
        image = db.session.query(Image).filter(Image.id == int(temp_id)).first()
        if (form.is_male.data == "0") or (form.is_male.data == "1"):
            image.is_male = int(form.is_male.data)
        if (form.is_juvenile.data == "0") or (form.is_juvenile.data == "1"):
            image.is_juvenile = int(form.is_juvenile.data)
        image.is_standard = bool(form.is_standard.data)
        image.quality_of_image = int(form.quality.data)
        image.certainty = int(form.certainty.data)
        image.is_classified = True
        db.session.commit()
        count += 1
        # get commited image
        image = db.session.query(Image).filter(Image.id == temp_id).first()
        # make insertion into classifcation table
        user = User.query.filter(User.id == id).first()
        user.images.append(image)
        db.session.add(user)
        db.session.commit()
        delete_fields = "True"
    else:
        flash('Please fill in all the fields- they are all required!','danger')

  # get new image
    image_to_classify = db.session.query(Image).filter(
        and_(Image.species == birdname, Image.is_classified == False)).order_by(asc("num_classifications")).first()
    if not image_to_classify:
        flash("You classified all the images. Pick another species", "danger")
        return redirect(url_for("admin.classify", id=id, count=count))
    data = {
        "birdname": birdname,
        "id": id,
        "image_uri": image_to_classify.uri,
        "image_id": image_to_classify.id,
        "image_folder": image_to_classify.downloaded_name,
        "count": count,
    }
    return render_template("classifying.html", id=id, image=imagez, data=data, form=form, delete_fields=delete_fields)





@admin.route("/admin/downloaded", methods=['POST', 'GET'])
@login_required
def downloaded():
    """
    turn on google if you want
    :return:
    """
    to_download = request.form.getlist("species")
    # api_key = "AIzaSyD_f54RnSGEfmAxl65FkFnNOVLx36QxBOw"
    # se_id = "006513363166106579724:xubk4naonbm"
    # for each in to_download:
    #     iu.scrape(each, api_key, se_id, 20)
##############################################################
    api_key = 'b63a6d85d9aab8c4b197b76dcbd76baa'
    secret = '3c02d12d74e9d90e'
    ext_list = ['.jpg', '.png']
    per_page = 20
    number_pages = 20
    flickr = flickrapi.FlickrAPI(api_key, secret, format='parsed-json')
    for each in to_download:
        z = iu.scrap_flickr_for_photos(flickr,each,api_key,secret,per_page,number_pages,ext_list)
        print(z[0])
        print(z[1])
        print()
    flash("your images were downloaded!", "danger")
    return render_template("downloaded.html", to_download=to_download)



@admin.route("/admin", methods=["GET", "POST"])
@login_required
def admin_page():
    if current_user.id != 1:
        return redirect(url_for("main.index"))
    method = None
    # all the birds for side bar list
    birds = Bird.query.order_by("Name").all()
    # bird species that have been downloaded
    downloaded_birds = Bird.query.filter(Bird.downloaded == 1).all()
    # list of dicts- name and totals---(total downloaded, number classified
    totals = []
    # images of species, their count and the number classified
    for bird in downloaded_birds:  # each is a bird
        bird_images = Image.query.filter(Image.species == bird.Name).all()
        # number images downloaded of each species
        num_down = len(bird_images)
        # number
        classified =len([each for each in bird_images if each.is_classified])
        temp_dict = {'name': bird.Name,
                     "number_downloaded": num_down,
                     "number_classified": classified}
        totals.append(temp_dict)
    # total number of downloaded birds
    num_birds = len(downloaded_birds)
    arg_dic = {"birds": birds,
               "title": "Admin",
               "method": method,
               "num_birds": num_birds,
               "downloaded_birds": downloaded_birds,
               "stats": totals}
    if request.method == 'GET':
        multi_select = request.args.getlist("PickBirds")
        arg_dic['ms'] = multi_select

        for each in multi_select:
            if each in downloaded_birds:
                flash("{} has already been downloaded, pick birds again".format(each.Name))
                return render_template('admin.html', data=arg_dic)

        return render_template("admin.html", data=arg_dic)

    elif request.method == "POST":
        to_download = request.form.getlist("PickBirds")
        method="POST"
        arg_dic['ms'] = to_download

        return render_template('admin.html', data=arg_dic)


