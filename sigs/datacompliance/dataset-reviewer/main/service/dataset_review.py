import traceback

from main.model.db_models import Pending_aibom, Pending_review, Review_result, Admin, Spdx_license_list
from main import db  # db is not required for queries, but is required for writes

import os
import time
import random
import csv
import xlrd
import codecs
import logging


def review_upload(user_id, dataset_review_list):
    """
    @param: user_id: the user who upload datasets to obtain the review result
    @param: dataset_review_list: list of dataset identifiers
    """
    datasets_review_result = []
    datasets_pending_aibom = []

    for dataset_review in dataset_review_list:
        # get the identifiers of each dataset
        name = dataset_review.get("name", "")
        location = dataset_review.get("location", "")
        originator = dataset_review.get("originator", [])
        # split via comma and convert to hashset
        originator = set([contributor.strip()
                          for contributor in originator.split(",")])

        # Get the potential corresponding audited dataset from the table review_result
        try:
            review_result = Review_result.query.filter_by(
                name=name, location=location).all()
        except Exception as e:
            ret = dict()
            ret['message'] = 'fail'
            ret['notification'] = e
            return ret

        is_reviewed = False  # Whether the dataset has been audited

        if name != "" and location != "" and len(originator) != 0:
            for review in review_result:
                # Gets the originator of the potential corresponding reviewed dataset
                review_originator = set(
                    [originator.strip() for originator in review.originator.split(",")])
                # Calculate the number of originator intersections between user-uploaded datasets and potentially reviewed datasets
                intersection = len(originator & review_originator)
                # If the overlap number is greater than or equal to 2, or more than half of Originators provided by users overlap, the dataset uploaded by users is considered to have been reviewed
                if intersection >= 2 or intersection / len(originator) >= 0.5:
                    datasets_review_result.append(review)
                    is_reviewed = True
                    break

        if not is_reviewed:
            dataset_pending_aibom = pending_aibom_transfer(
                dataset_review, user_id)
            try:
                db.session.add(dataset_pending_aibom)
                db.session.commit()
                datasets_pending_aibom.append(dataset_pending_aibom)
            except Exception as e:
                print(e)
                db.session.rollback()

    ret = dict()
    ret['review_result_list'] = datasets_review_result
    ret['pending_aibom_list'] = datasets_pending_aibom
    ret['message'] = 'success'
    ret['notification'] = ''

    return ret


def get_pending_aibom_by_user(user_id):
    ret = dict()
    try:
        pending_aibom = Pending_aibom.query.filter_by(user_id=user_id).all()
        ret['pending_aibom_list'] = pending_aibom
        ret['message'] = 'success'
        ret['notification'] = ''
    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
    return ret


def save_pending_aibom_list(pending_aibom_list):
    ret = dict()
    if len(pending_aibom_list) == 0:
        ret['message'] = 'fail'
        ret['notification'] = 'nothing to save'
        return ret

    for new_pending_aibom in pending_aibom_list:
        try:
            ori_pending_aibom = Pending_aibom.query.filter_by(id=new_pending_aibom.get('id', ''),
                                                              user_id=new_pending_aibom.get('user_id', '')).first()
        except Exception as e:
            ret['message'] = 'fail'
            ret['notification'] = e
            return ret

        if ori_pending_aibom is not None:
            ori_pending_aibom = pending_aibom_transfer(new_pending_aibom, new_pending_aibom.get('user_id', ''),
                                                       ori_pending_aibom)
            try:
                db.session.add(ori_pending_aibom)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                ret['message'] = 'fail'
                ret['notification'] = e
                return ret

    ret['message'] = 'success'
    ret['notification'] = ''

    return ret


def submit_pending_aibom_list(pending_aibom_list):
    ret = dict()
    if len(pending_aibom_list) == 0:
        ret['message'] = 'fail'
        ret['notification'] = 'nothing to submit'
        return ret

    error_pending_aibom_format = []

    for pending_aibom in pending_aibom_list:
        is_pass = format_check_aibom(pending_aibom)

        if is_pass:
            pending_review = convert_aibom_to_review(pending_aibom)
            to_delete = Pending_aibom.query.filter_by(id=pending_aibom.get('id', ''),
                                                      user_id=pending_aibom.get('user_id', '')).first()
            if to_delete is None:
                ret['message'] = 'fail'
                ret['notification'] = 'Cannot submit due to no record in pending aibom'
                return ret

            to_delete = Pending_aibom.__table__.delete().where(
                Pending_aibom.user_id == pending_aibom.get('user_id', '')).where(
                Pending_aibom.id == pending_aibom.get('id', ''))

            try:
                db.session.execute(to_delete)
                db.session.add(pending_review)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                ret['message'] = 'fail'
                ret['notification'] = e
                return ret
        else:
            error_pending_aibom_format.append(pending_aibom)

    if len(error_pending_aibom_format) != 0:
        ret['pending_aibom_list'] = error_pending_aibom_format
        ret['message'] = "fail"
        ret['notification'] = "AIBOM info has been submitted, the format of AIBOM is incorrect for {} dataset, please submit after modify".format(
            len(error_pending_aibom_format))
    else:
        ret['message'] = "success"
        ret['notification'] = ""

    return ret


def remove_pending_aibom_list(user_id, pending_aibom_ids):
    to_delete = Pending_aibom.__table__.delete().where(Pending_aibom.user_id == user_id).where(
        Pending_aibom.id.in_(pending_aibom_ids))

    ret = dict()

    try:
        # Execute this sql to change the database via session
        db.session.execute(to_delete)
        db.session.commit()  # Transaction commit.

        ret['message'] = 'success'
        ret['notification'] = ''

    except Exception as e:
        db.session.rollback()

        ret['message'] = 'fail'
        ret['notification'] = e

    return ret


def is_admin(user_id, account):
    ret = dict()
    try:
        user_id = int(user_id)
        account = str(account)
        admin = Admin.query.filter_by(uid=user_id, account=account).first()

        if admin is None:
            ret['message'] = 'fail'
            ret['notification'] = 'not admin!'
            return ret
    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['message'] = 'success'
    ret['notification'] = ''
    return ret


def get_pending_review_list(user_id):
    ret = dict()
    try:
        if user_id == -1:
            pending_review = Pending_review.query.all()
        else:
            pending_review = Pending_review.query.filter_by(
                user_id=user_id).all()
    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['pending_review_list'] = pending_review
    ret['message'] = 'success'
    ret['notification'] = ''
    return ret


def save_pending_review_list(pending_review_list):
    ret = dict()
    for new_pending_review in pending_review_list:
        ori_pending_review = Pending_review.query.filter_by(
            id=new_pending_review.get('id', '')).first()
        if ori_pending_review is not None:
            ori_pending_review = pending_review_transfer(
                ori_pending_review, new_pending_review)
            try:
                db.session.add(ori_pending_review)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                ret['message'] = 'fail'
                ret['notification'] = e
                return ret

    ret['message'] = 'success'
    ret['notification'] = ''
    return ret


def reject_review(user_id, pending_review_ids, rejection_notes):
    ret = dict()
    pending_aibom_list = []

    for index, pending_review_id in enumerate(pending_review_ids):
        pending_review = Pending_review.query.filter_by(
            id=pending_review_id, user_id=user_id).first()
        if pending_review is None:
            continue

        to_delete = Pending_review.__table__.delete().where(
            Pending_review.id == pending_review_id).where(Pending_review.user_id == user_id)

        pending_aibom = convert_review_to_aibom(pending_review)
        pending_aibom.rejection_notes = "" if index == len(
            rejection_notes) else rejection_notes[index]
        try:
            db.session.add(pending_aibom)
            db.session.execute(to_delete)
            db.session.commit()
            pending_aibom_list.append(pending_aibom)
        except Exception as e:
            db.session.rollback()
            ret['message'] = 'fail'
            ret['notification'] = e
            return ret

    ret['pending_aibom_list'] = pending_aibom_list
    ret['message'] = 'success'
    ret['notification'] = ''
    return ret


def submit_pending_review_list(pending_review_list):
    ret = dict()
    if len(pending_review_list) == 0:
        ret['message'] = 'fail'
        ret['notification'] = 'nothing to submit'
        return ret

    error_pending_review_format = []

    for pending_review in pending_review_list:
        is_pass = format_check_aibom(
            pending_review) and format_check_review(pending_review)  # 格式检查

        if is_pass:
            review_result = convert_review_to_result(pending_review)
            to_delete = Pending_review.query.filter_by(id=pending_review.get('id', ''),
                                                       user_id=pending_review.get('user_id', '')).first()
            if to_delete is None:
                continue

            to_delete = Pending_review.__table__.delete().where(
                Pending_review.user_id == pending_review.get('user_id', '')).where(
                Pending_review.id == pending_review.get('id', ''))

            try:
                db.session.execute(to_delete)
                db.session.add(review_result)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                ret['message'] = 'fail'
                ret['notification'] = e
                return ret
        else:
            error_pending_review_format.append(pending_review)

    if len(error_pending_review_format) != 0:
        ret['pending_review_list'] = error_pending_review_format
        ret['message'] = "fail"
        ret['notification'] = "review info has been submitted, the format of review is incorrect for {} dataset, please submit after modify".format(
            len(error_pending_review_format))
    else:
        ret['message'] = "success"
        ret['notification'] = ""

    return ret


def get_review_result_list_for_dataset_name(dataset_name):
    ret = dict()
    review_result_dict = {}
    match_dataset_review_result_list = []
    try:
        if dataset_name is not None \
                and len(dataset_name) != 0:
            match_dataset_review_result_list = list(Review_result.query.filter(
                Review_result.name.like('%' + dataset_name + '%')).all())
            # review_result_list = Review_result.query.all()
            # for review_result in review_result_list:
            #     review_result_dict[review_result.name] = review_result
            #
            # for dataset_name in dataset_name_list:
            #     match_dataset_review_result = review_result_dict.get(dataset_name)
            #     if match_dataset_review_result is None:
            #         continue

        # match_dataset_review_result_list.append(match_dataset_review_result)

    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['review_result_list'] = match_dataset_review_result_list
    ret['message'] = 'success'
    ret['notification'] = ''
    return ret


def get_review_result_list_for_dataset_name_list(dataset_name_list):
    ret = dict()
    review_result_dict = {}
    match_dataset_review_result_list = []
    try:
        if dataset_name_list is not None \
                and len(dataset_name_list) != 0:
            review_result_list = Review_result.query.all()
            for review_result in review_result_list:
                review_result_dict[review_result.name] = review_result

            for dataset_name in dataset_name_list:
                match_dataset_review_result = review_result_dict.get(dataset_name)
                if match_dataset_review_result is None:
                    continue
                match_dataset_review_result_list.append(match_dataset_review_result)

    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['review_result_list'] = match_dataset_review_result_list
    ret['message'] = 'success'
    ret['notification'] = ''
    return ret


def get_review_result_list(user_id):
    ret = dict()
    try:
        if user_id == -1:
            review_result = Review_result.query.all()
        else:
            review_result = Review_result.query.filter_by(
                user_id=user_id).all()
    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['review_result_list'] = review_result
    ret['message'] = 'success'
    ret['notification'] = ''
    return ret


def license_upload(user_id, dataset_license_list):
    license_success_list = []
    license_fail_list = []

    for dataset_license in dataset_license_list:
        # get the identifiers of each dataset
        full_name = dataset_license.get("full_name", "")
        identifier = dataset_license.get("identifier", "")

        # Get the potential corresponding audited dataset from the table review_result
        try:
            spdx_license_list = Spdx_license_list.query.filter_by(
                full_name=full_name, identifier=identifier).all()
        except Exception as e:
            ret = dict()
            ret['message'] = 'fail'
            ret['notification'] = e
            return ret

        if spdx_license_list is None or len(spdx_license_list) == 0:
            cur_license = license_transfer(dataset_license, user_id)
            try:
                db.session.add(cur_license)
                db.session.commit()
                license_success_list.append(dataset_license)
            except Exception as e:
                print(e)
                db.session.rollback()
        else:
            license_fail_list.append(dataset_license)

    ret = dict()
    if len(license_fail_list) != 0:
        ret['license_success_list'] = license_success_list
        ret['license_fail_list'] = license_fail_list
        ret['message'] = 'fail'
        ret['notification'] = ''
    else:
        ret['message'] = 'success'
        ret['notification'] = ''

    return ret


def get_dataset_license_list(text):
    ret = dict()
    try:
        if text == "":
            spdx_license_list = Spdx_license_list.query.all()
        else:
            spdx_license_list_1 = set(Spdx_license_list.query.filter(
                Spdx_license_list.full_name.like('%' + text + '%')).all())
            spdx_license_list_2 = set(Spdx_license_list.query.filter(
                Spdx_license_list.identifier.like('%' + text + '%')).all())
            spdx_license_list = spdx_license_list_1 | spdx_license_list_2

    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['spdx_license_list'] = spdx_license_list
    ret['message'] = 'success'
    ret['notification'] = ''
    return ret


def pending_aibom_transfer(new_aibom_info, user_id, ori_aibom_info=None):
    if ori_aibom_info is None:
        dataset_pending_aibom = Pending_aibom(
            name=new_aibom_info.get("name", ""),
            location=new_aibom_info.get("location", ""),
            originator=new_aibom_info.get("originator", ""),
            license_location=new_aibom_info.get("license_location", ""),
            # concluded_license=new_aibom_info.get("concluded_license", None),
            # declared_license=new_aibom_info.get("declared_license", None),
            type=new_aibom_info.get("type", ""),
            size=new_aibom_info.get("size", ""),
            intended_use=new_aibom_info.get("intended_use", ""),
            # checksum=new_aibom_info.get("checksum", None),
            # data_collection_process=new_aibom_info.get("data_collection_process", None),
            # known_biases=new_aibom_info.get("known_biases", 0),
            # sensitive_personal_information=new_aibom_info.get("sensitive_personal_information", 0),
            # offensive_content=new_aibom_info.get("offensive_content", 0),
            user_id=user_id
        )
        return dataset_pending_aibom
    else:
        if "name" in new_aibom_info.keys():
            ori_aibom_info.name = new_aibom_info.get("name", "")
        if "location" in new_aibom_info.keys():
            ori_aibom_info.location = new_aibom_info.get("location", "")
        if "originator" in new_aibom_info.keys():
            ori_aibom_info.originator = new_aibom_info.get("originator", "")
        if "license_location" in new_aibom_info.keys():
            ori_aibom_info.license_location = new_aibom_info.get(
                "license_location", "")
        if "concluded_license" in new_aibom_info.keys():
            ori_aibom_info.concluded_license = new_aibom_info.get(
                "concluded_license", None)
        if "declared_license" in new_aibom_info.keys():
            ori_aibom_info.declared_license = new_aibom_info.get(
                "declared_license", None)
        if "type" in new_aibom_info.keys():
            ori_aibom_info.type = new_aibom_info.get("type", "")
        if "size" in new_aibom_info.keys():
            ori_aibom_info.size = new_aibom_info.get("size", "")
        if "intended_use" in new_aibom_info.keys():
            ori_aibom_info.intended_use = new_aibom_info.get(
                "intended_use", "")
        if "checksum" in new_aibom_info.keys():
            ori_aibom_info.checksum = new_aibom_info.get("checksum", None)
        if "data_collection_process" in new_aibom_info.keys():
            ori_aibom_info.data_collection_process = new_aibom_info.get(
                "data_collection_process", None)
        if "known_biases" in new_aibom_info.keys() and new_aibom_info.get("known_biases") is not None:
            ori_aibom_info.known_biases = new_aibom_info.get("known_biases", 0)
        if "sensitive_personal_information" in new_aibom_info.keys() and new_aibom_info.get(
                "sensitive_personal_information") is not None:
            ori_aibom_info.sensitive_personal_information = new_aibom_info.get(
                "sensitive_personal_information", 0)
        if "offensive_content" in new_aibom_info.keys() and new_aibom_info.get("offensive_content") is not None:
            ori_aibom_info.offensive_content = new_aibom_info.get(
                "offensive_content", 0)
        return ori_aibom_info


def pending_review_transfer(ori_pending_review, new_pending_review):
    ori_pending_review.name = new_pending_review.get("name", "")
    ori_pending_review.location = new_pending_review.get("location", "")
    ori_pending_review.originator = new_pending_review.get("originator", "")
    ori_pending_review.license_location = new_pending_review.get(
        "license_location", "")
    ori_pending_review.concluded_license = new_pending_review.get(
        "concluded_license", None)
    ori_pending_review.declared_license = new_pending_review.get(
        "declared_license", None)
    ori_pending_review.type = new_pending_review.get("type", "")
    ori_pending_review.size = new_pending_review.get("size", "")
    ori_pending_review.intended_use = new_pending_review.get(
        "intended_use", "")
    ori_pending_review.checksum = new_pending_review.get("checksum", None)
    ori_pending_review.data_collection_process = new_pending_review.get(
        "data_collection_process", None)
    ori_pending_review.known_biases = new_pending_review.get(
        "known_biases", "")
    ori_pending_review.sensitive_personal_information = new_pending_review.get(
        "sensitive_personal_information", None)
    ori_pending_review.offensive_content = new_pending_review.get(
        "offensive_content", None)

    # ori_pending_review.user_id = new_pending_review.get("user_id", "")

    ori_pending_review.review_result_initial = new_pending_review.get(
        "review_result_initial", "")
    ori_pending_review.is_dataset_commercially_used_initial = new_pending_review.get(
        "is_dataset_commercially_used_initial", 0)
    ori_pending_review.is_dataset_commercially_distributed_initial = new_pending_review.get(
        "is_dataset_commercially_distributed_initial", 0)
    ori_pending_review.is_product_commercially_published_initial = new_pending_review.get(
        "is_product_commercially_published_initial", 0)
    ori_pending_review.right_initial = new_pending_review.get(
        "right_initial", None)
    ori_pending_review.obligation_initial = new_pending_review.get(
        "obligation_initial", None)
    ori_pending_review.limitation_initial = new_pending_review.get(
        "limitation_initial", None)
    ori_pending_review.notes_initial = new_pending_review.get(
        "notes_initial", None)

    return ori_pending_review


def license_transfer(dataset_license, user_id):
    cur_license = Spdx_license_list(
        full_name=dataset_license.get("full_name", ""),
        identifier=dataset_license.get("identifier", ""),
        user_id=user_id
    )
    return cur_license


def convert_aibom_to_review(pending_aibom):
    pending_review = Pending_review(
        name=pending_aibom.get("name", ""),
        location=pending_aibom.get("location", ""),
        originator=pending_aibom.get("originator", ""),
        license_location=pending_aibom.get("license_location", ""),
        concluded_license=pending_aibom.get("concluded_license", None),
        declared_license=pending_aibom.get("declared_license", None),
        type=pending_aibom.get("type", ""),
        size=pending_aibom.get("size", ""),
        intended_use=pending_aibom.get("intended_use", None),
        checksum=pending_aibom.get("checksum", ""),
        data_collection_process=pending_aibom.get(
            "data_collection_process", None),
        known_biases=pending_aibom.get("known_biases", 0),
        sensitive_personal_information=pending_aibom.get(
            "sensitive_personal_information", 0),
        offensive_content=pending_aibom.get("offensive_content", 0),
        user_id=pending_aibom.get('user_id', ""),
        review_result_initial="",
        is_dataset_commercially_used_initial=0,
        is_dataset_commercially_distributed_initial=0,
        is_product_commercially_published_initial=0
    )

    return pending_review


def convert_review_to_aibom(pending_review):
    pending_aibom = Pending_aibom(
        name=pending_review.name,
        location=pending_review.location,
        originator=pending_review.originator,
        license_location=pending_review.license_location,
        concluded_license=pending_review.concluded_license,
        declared_license=pending_review.declared_license,
        type=pending_review.type,
        size=pending_review.size,
        intended_use=pending_review.intended_use,
        checksum=pending_review.checksum,
        data_collection_process=pending_review.data_collection_process,
        known_biases=pending_review.known_biases,
        sensitive_personal_information=pending_review.sensitive_personal_information,
        offensive_content=pending_review.offensive_content,

        user_id=pending_review.user_id,
    )

    return pending_aibom


def convert_review_to_result(pending_review):
    review_result = Review_result(
        name=pending_review.get("name", ""),
        location=pending_review.get("location", ""),
        originator=pending_review.get("originator", ""),
        license_location=pending_review.get("license_location", ""),
        concluded_license=pending_review.get("concluded_license", None),
        declared_license=pending_review.get("declared_license", None),
        type=pending_review.get("type", ""),
        size=pending_review.get("size", ""),
        intended_use=pending_review.get("intended_use", ""),
        checksum=pending_review.get("checksum", None),
        data_collection_process=pending_review.get(
            "data_collection_process", None),
        known_biases=pending_review.get("known_biases", None),
        sensitive_personal_information=pending_review.get(
            "sensitive_personal_information", None),
        offensive_content=pending_review.get("offensive_content", None),

        user_id=pending_review.get("user_id", ""),

        review_result_initial=pending_review.get("review_result_initial", ""),
        is_dataset_commercially_used_initial=pending_review.get(
            "is_dataset_commercially_used_initial", 0),
        is_dataset_commercially_distributed_initial=pending_review.get(
            "is_dataset_commercially_distributed_initial", 0),
        is_product_commercially_published_initial=pending_review.get(
            "is_product_commercially_published_initial", 0),
        right_initial=pending_review.get("right_initial", None),
        obligation_initial=pending_review.get("obligation_initial", None),
        limitation_initial=pending_review.get("limitation_initial", None),
        notes_initial=pending_review.get("notes_initial", None),

        review_result_final="",
        is_dataset_commercially_used_final=0,
        is_dataset_commercially_distributed_final=0,
        is_product_commercially_published_final=0,
        right_final="",
        obligation_final="",
        limitation_final="",
        notes_final="",
    )

    return review_result


def format_check_aibom(pending_aibom):
    keys = {"name", "location", "originator", "license_location",
            "type", "size", "intended_use", "user_id"}
    for key in keys:
        if key not in pending_aibom.keys() or len(str(pending_aibom[key])) == 0:
            return False
    if "concluded_license" not in pending_aibom.keys() and "declared_license" not in pending_aibom.keys():
        return False
    if pending_aibom['concluded_license'] is None and pending_aibom['declared_license'] is None:
        return False
    if pending_aibom['concluded_license'] is not None and len(pending_aibom['concluded_license']) != 0:
        return True
    if pending_aibom['declared_license'] is not None and len(pending_aibom['declared_license']) != 0:
        return True

    return True


def format_check_review(pending_review):
    keys = {"review_result_initial", "is_dataset_commercially_used_initial",
            "is_dataset_commercially_distributed_initial", "is_product_commercially_published_initial"}
    for key in keys:
        if key not in pending_review.keys() or len(str(pending_review[key])) == 0:
            return False
    return True


def file_suffix_check(cur_file):
    if "." in cur_file.filename and (
            cur_file.filename.rsplit('.', 1)[1] == "csv" or cur_file.filename.rsplit('.', 1)[1] == "xlsx"):
        return True
    return False


def file_save(user_id, cur_file, path):
    try:
        file_name = str(user_id) + "_" + str(int(time.time())) + \
                    "_" + str(random.randint(0, 2147483647)) + ".csv"

        # The absolute address of the target to save
        root_path = os.getcwd()  # The absolute path of the current project
        rel_path = "/static/" + path + "/"  # Relative path to the folder
        abs_path = root_path + rel_path  # The absolute path to the img

        if not os.path.exists(abs_path):
            os.makedirs(abs_path)

        if cur_file.filename.rsplit('.', 1)[1] == "csv":
            cur_file.save(abs_path + file_name)
        else:
            xlsx_to_csv(cur_file, abs_path + file_name)
        return True, abs_path + file_name
    except Exception as e:
        return False, e


def xlsx_to_csv(cur_file, file_path):
    xlsx_path = file_path.rsplit(".")[0] + ".xlsx"
    cur_file.save(xlsx_path)
    workbook = xlrd.open_workbook(xlsx_path)
    table = workbook.sheet_by_index(0)
    with codecs.open(file_path, 'w', encoding='utf-8') as f:
        write = csv.writer(f)
        for row_num in range(table.nrows):
            row_value = table.row_values(row_num)
            for i in range(len(row_value)):
                if isinstance(row_value[i], float) and abs(int(row_value[i]) - row_value[i]) < 0.00001:
                    row_value[i] = int(row_value[i])
            write.writerow(row_value)


def file_convert_dataset(user_id, cur_file):
    ret = dict()
    if cur_file is None:
        ret['message'] = 'fail'
        ret['notification'] = 'File upload fail!'
        return ret

    if not file_suffix_check(cur_file):
        ret['message'] = 'fail'
        ret['notification'] = 'Please upload the file in csv or xlsx!'
        return ret

    is_success, msg = file_save(user_id, cur_file, 'upload_by_user')
    if not is_success:
        ret['message'] = 'fail'
        ret['notification'] = msg
        return ret

    dataset_review_list = []
    cur_file = csv.reader(open(msg))
    cnt = 0
    for line in cur_file:
        if cnt == 0:
            cnt += 1
            continue
        dataset = dict()
        dataset['name'] = str(line[0])
        dataset['location'] = str(line[1])
        dataset['originator'] = str(line[2])
        dataset_review_list.append(dataset)

    ret['message'] = 'success'
    ret['notification'] = dataset_review_list
    return ret


def file_convert_license(user_id, cur_file):
    ret = dict()
    if cur_file is None:
        ret['message'] = 'fail'
        ret['notification'] = 'File upload fail!'
        return ret

    if not file_suffix_check(cur_file):
        ret['message'] = 'fail'
        ret['notification'] = 'Please upload the file in csv or xlsx!'
        return ret

    is_success, msg = file_save(user_id, cur_file, 'license_upload_by_user')
    if not is_success:
        ret['message'] = 'fail'
        ret['notification'] = msg
        return ret

    dataset_license_list = []
    cur_file = csv.reader(open(msg))
    cnt = 0

    try:
        for line in cur_file:
            if cnt == 0:
                cnt += 1
                continue
            dataset = dict()
            dataset['full_name'] = str(line[0])
            dataset['identifier'] = str(line[1])
            dataset['user_id'] = int(line[2])
            dataset_license_list.append(dataset)
    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['message'] = 'success'
    ret['notification'] = dataset_license_list
    return ret


def review_result_download(user_id, review_result_list):
    ret = dict()

    file_name = str(user_id) + "_" + str(int(time.time())) + \
                "_" + str(random.randint(0, 2147483647)) + ".csv"
    # The absolute address of the target to save
    root_path = os.getcwd()  # The absolute path of the current project
    rel_path = "/static" + "/download_by_user/"  # Relative path to the folder
    abs_path = root_path + rel_path  # The absolute path to the img

    try:
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)

        with open("." + rel_path + file_name, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["name", "location", "originator", "license_location", "concluded_license", "declared_license",
                 "type", "size", "intended_use", "checksum", "data_collection_process", "known_biases",
                 "sensitive_personal_information", "offensive_content", "review_result_initial",
                 "is_dataset_commercially_used_initial", "is_dataset_commercially_distributed_initial",
                 "is_product_commercially_published_initial", "right_initial",
                 "obligation_initial", "limitation_initial", "notes_initial"])
            for review_result in review_result_list:
                writer.writerow([review_result.name, review_result.location, review_result.originator,
                                 review_result.license_location,
                                 review_result.concluded_license, review_result.declared_license, review_result.type,
                                 review_result.size,
                                 review_result.intended_use, review_result.checksum,
                                 review_result.data_collection_process,
                                 review_result.known_biases, review_result.sensitive_personal_information,
                                 review_result.offensive_content, review_result.review_result_initial,
                                 review_result.is_dataset_commercially_used_initial,
                                 review_result.is_dataset_commercially_distributed_initial,
                                 review_result.is_product_commercially_published_initial, review_result.right_initial,
                                 review_result.obligation_initial, review_result.limitation_initial,
                                 review_result.notes_initial])
    except Exception as e:
        logging.error("review_result_download_异常了！！", e)
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['message'] = 'success'
    ret['download_path'] = abs_path
    ret['file_name'] = file_name
    return ret


def get_review_result_by_id(result_id):
    ret = dict()
    try:
        review_result = Review_result.query.filter_by(id=result_id).all()
    except Exception as e:
        ret['message'] = 'fail'
        ret['notification'] = e
        return ret

    ret['review_result_list'] = review_result
    ret['message'] = 'success'
    ret['notification'] = ''
    return ret
