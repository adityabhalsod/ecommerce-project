import os

############# User (OPEN) #############
def profile_upload_path(instance, filename):
    return os.path.join("profile/", filename)


############# User (OPEN) #############

############# Catalog(OPEN) #############
def category_upload_path(instance, filename):
    return os.path.join("catalog/categories/original/", filename)


def category_webp_upload_path(instance, filename):
    return os.path.join("catalog/categories/webp/", filename)


def category_thumbnail_upload_path(instance, filename):
    return os.path.join("catalog/categories/thumbnail/", filename)


def product_upload_path(instance, filename):
    return os.path.join("catalog/product/original/", filename)


def product_webp_upload_path(instance, filename):
    return os.path.join("catalog/product/webp/", filename)


def product_thumbnail_upload_path(instance, filename):
    return os.path.join("catalog/product/thumbnail/", filename)


def variation_upload_path(instance, filename):
    return os.path.join("catalog/variation/original/", filename)


def variation_webp_upload_path(instance, filename):
    return os.path.join("catalog/variation/webp/", filename)


def variation_thumbnail_upload_path(instance, filename):
    return os.path.join("catalog/variation/thumbnail/", filename)


############# Catalog(OPEN) #############


############# Delivery boy (:TODO == Secure) #############
def delivery_boy_bank_account_proof_upload_path(instance, filename):
    return os.path.join(
        "delivery-boy/bank-account-proof/",
        filename,
    )


def delivery_boy_vehicle_original_upload_path(instance, filename):
    return os.path.join(
        "delivery-boy/vehicle-photos/original/",
        filename,
    )


def delivery_boy_vehicle_webp_upload_path(instance, filename):
    return os.path.join(
        "delivery-boy/vehicle-photos/webp/",
        filename,
    )


def delivery_boy_vehicle_thumbnail_upload_path(instance, filename):
    return os.path.join(
        "delivery-boy/vehicle-photos/thumbnail/",
        filename,
    )


def delivery_boy_document_back(instance, filename):
    return os.path.join(
        "delivery-boy/document/back/",
        filename,
    )


def delivery_boy_document_front(instance, filename):
    return os.path.join(
        "delivery-boy/document/front/",
        filename,
    )


############# Delivery boy (:TODO == Secure) #############


############# Group #############
def group_color(instance, filename):
    return os.path.join("group/color/", filename)


def group_upload_path(instance, filename):
    return os.path.join("group/structure/original/", filename)


def group_webp_upload_path(instance, filename):
    return os.path.join("group/structure/webp/", filename)


def group_thumbnail_upload_path(instance, filename):
    return os.path.join("group/structure/thumbnail/", filename)


def group_multiphotos_upload_path(instance, filename):
    return os.path.join("group/structure/multiple/original/", filename)


def group_multiphotos_webp_upload_path(instance, filename):
    return os.path.join("group/structure/multiple/webp/", filename)


def group_multiphotos_thumbnail_upload_path(instance, filename):
    return os.path.join("group/structure/multiple/thumbnail/", filename)


############# Group #############


############# Attachment #############
def purchase_attach_document(instance, filename):
    return os.path.join("purchase/attach_document/", filename)


############# Attachment #############
