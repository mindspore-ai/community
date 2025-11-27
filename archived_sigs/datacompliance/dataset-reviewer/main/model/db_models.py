from main import db


class Pending_aibom(db.Model):
    _tablename_ = 'pending_aibom'

    id = db.Column(db.Integer, unique=True,
                   primary_key=True, autoincrement=True)
    # Dataset AIBOM attributes
    name = db.Column(db.String(255))  # dataset name
    location = db.Column(db.String(255))  # dataset official website
    originator = db.Column(db.String(255))  # contributors
    license_location = db.Column(db.String(255))  # license location
    concluded_license = db.Column(db.String(255))  # SPDX License List
    declared_license = db.Column(db.String(255))  # customized license
    type = db.Column(db.String(255))  # types of this dataset
    size = db.Column(db.String(255))  # total size of this dataset
    # The purpose why this dataset made
    intended_use = db.Column(db.String(255))
    checksum = db.Column(db.String(255))  # checksum
    data_collection_process = db.Column(
        db.String(255))  # The collection process of data
    known_biases = db.Column(db.Boolean)
    sensitive_personal_information = db.Column(db.Boolean)
    offensive_content = db.Column(db.Boolean)
    # attach the user info
    # the user who should finish the AIBOM of this dataset
    user_id = db.Column(db.Integer)
    # notes
    # notes when rejected in review
    rejection_notes = db.Column(db.String(255))


class Pending_review(db.Model):
    _tablename_ = 'pending_review'

    id = db.Column(db.Integer, unique=True,
                   primary_key=True, autoincrement=True)
    # Dataset AIBOM attributes
    name = db.Column(db.String(255))  # dataset name
    location = db.Column(db.String(255))  # dataset official website
    originator = db.Column(db.String(255))  # contributors
    license_location = db.Column(db.String(255))  # license location
    concluded_license = db.Column(db.String(255))  # SPDX License List
    declared_license = db.Column(db.String(255))  # customized license
    type = db.Column(db.String(255))  # types of this dataset
    size = db.Column(db.String(255))  # total size of this dataset
    # The purpose why this dataset made
    intended_use = db.Column(db.String(255))
    checksum = db.Column(db.String(255))  # checksum
    data_collection_process = db.Column(
        db.String(255))  # The collection process of data
    known_biases = db.Column(db.Boolean)
    sensitive_personal_information = db.Column(db.Boolean)
    offensive_content = db.Column(db.Boolean)
    # attach the user info
    # the user who should finish the AIBOM of this dataset
    user_id = db.Column(db.Integer)
    # initial review suggestion
    review_result_initial = db.Column(db.String(255))  # initial review result
    # is this dataset allowed to be used commercially
    is_dataset_commercially_used_initial = db.Column(db.Boolean)
    # is this dataset allowed to be distributed commercially
    is_dataset_commercially_distributed_initial = db.Column(db.Boolean)
    # is this dataset allowed to be published commercially
    is_product_commercially_published_initial = db.Column(db.Boolean)
    right_initial = db.Column(db.String(255))  # rights for this dataset
    # obligation for this dataset
    obligation_initial = db.Column(db.String(255))
    # limitation for this dataset
    limitation_initial = db.Column(db.String(255))
    notes_initial = db.Column(db.String(255))  # notes for the initial review


class Review_result(db.Model):
    _tablename_ = 'dataset_review'

    id = db.Column(db.Integer, unique=True,
                   primary_key=True, autoincrement=True)
    # Dataset AIBOM attributes
    name = db.Column(db.String(255))  # dataset name
    location = db.Column(db.String(255))  # dataset official website
    originator = db.Column(db.String(255))  # contributors
    license_location = db.Column(db.String(255))  # license location
    concluded_license = db.Column(db.String(255))  # SPDX License List
    declared_license = db.Column(db.String(255))  # customized license
    type = db.Column(db.String(255))  # types of this dataset
    size = db.Column(db.String(255))  # total size of this dataset
    # The purpose why this dataset made
    intended_use = db.Column(db.String(255))
    checksum = db.Column(db.String(255))  # checksum
    data_collection_process = db.Column(
        db.String(255))  # The collection process of data
    known_biases = db.Column(db.Boolean)
    sensitive_personal_information = db.Column(db.Boolean)
    offensive_content = db.Column(db.Boolean)
    # attach the user info
    # the user who should finish the AIBOM of this dataset
    user_id = db.Column(db.Integer)
    # initial review suggestion
    review_result_initial = db.Column(db.String(255))  # initial review result
    # is this dataset allowed to be used commercially
    is_dataset_commercially_used_initial = db.Column(db.Boolean)
    # is this dataset allowed to be distributed commercially
    is_dataset_commercially_distributed_initial = db.Column(db.Boolean)
    # is this dataset allowed to be published commercially
    is_product_commercially_published_initial = db.Column(db.Boolean)
    right_initial = db.Column(db.String(255))  # rights for this dataset
    # obligation for this dataset
    obligation_initial = db.Column(db.String(255))
    # limitation for this dataset
    limitation_initial = db.Column(db.String(255))
    notes_initial = db.Column(db.String(255))  # notes for the initial review
    # final review result
    review_result_final = db.Column(db.String(255))  # final review result
    # is this dataset allowed to be used commercially
    is_dataset_commercially_used_final = db.Column(db.Boolean)
    # is this dataset allowed to be distributed commercially
    is_dataset_commercially_distributed_final = db.Column(db.Boolean)
    # is this dataset allowed to be published commercially
    is_product_commercially_published_final = db.Column(db.Boolean)
    right_final = db.Column(db.String(255))  # rights for this dataset
    obligation_final = db.Column(db.String(255))  # obligation for this dataset
    limitation_final = db.Column(db.String(255))  # limitation for this dataset
    notes_final = db.Column(db.String(255))  # notes for the final review


class Spdx_license_list(db.Model):
    _tablename_ = 'spdx_license_list'

    id = db.Column(db.Integer, unique=True,
                   primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255))
    identifier = db.Column(db.String(255))
    fsf_free_libre = db.Column(db.String(255))
    osi_approved = db.Column(db.String(255))
    user_id = db.Column(db.Integer)


class Users(db.Model):
    _tablename_ = 'users'

    id = db.Column(db.Integer, unique=True,
                   primary_key=True, autoincrement=True)
    account = db.Column(db.String(255))
    password = db.Column(db.String(255))
    verification = db.Column(db.String(255))


class Admin(db.Model):
    _tablename_ = 'admin'

    id = db.Column(db.Integer, unique=True,
                   primary_key=True, autoincrement=True)
    account = db.Column(db.String(255))
    uid = db.Column(db.Integer)
