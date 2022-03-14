import time

from config.celery import app
from v1.warehouse.choice import DiscountType


@app.task
def stock_purchase(instance):
    if instance:
        # Sub total
        if instance.multiple_item and instance.multiple_item.all():
            price = 0.0
            all_items = instance.multiple_item.all()
            instance.total_items = instance.multiple_item.all().count()
            for item in all_items:
                price = price + item.price
            instance.sub_total = price
            instance.purchase_total = price

        # Discount
        if instance.discount and instance.discount_type and instance.purchase_total > 0:
            if instance.discount_type == DiscountType.FIXED:
                instance.purchase_total = instance.purchase_total - instance.discount
            elif instance.discount_type == DiscountType.PERCENTAGE:
                instance.purchase_total = instance.purchase_total - (
                    (instance.discount * instance.purchase_total) / 100
                )

        # tax
        if instance.tax and instance.purchase_total > 0:
            try:
                instance.purchase_total = instance.purchase_total + (
                    (instance.tax * instance.purchase_total) / 100
                )
            except Exception:
                pass

        #  additional shipping charges
        if instance.additional_shipping_charges and instance.purchase_total > 0:
            instance.purchase_total = (
                instance.purchase_total + instance.additional_shipping_charges
            )

        if (
            instance.warehouse
            and instance.multiple_item
            and instance.multiple_item.all()
        ):
            from v1.warehouse.models import WarehouseStockManagement

            for item in instance.multiple_item.all():
                stock, created = WarehouseStockManagement.objects.get_or_create(
                    product_and_variation=item.product_and_variation,
                    purchase_reference=instance,
                )
                stock.warehouse = instance.warehouse
                stock.quantity = item.quantity
                stock.save()
    return True


@app.task
def stock_transfer(instance):
    time.sleep(5)
    if instance:
        if instance.is_draft == False:
            if instance.store and instance.multiple_item.all():
                from v1.warehouse.models import (
                    StoreStockManagement,
                    WarehouseStockManagement,
                )

                for item in instance.multiple_item.all():
                    ################ store add stock ################
                    store_stock, add = StoreStockManagement.objects.get_or_create(
                        product_and_variation=item.product_and_variation,
                        transfer_reference=instance,
                    )
                    store_stock.quantity = int(store_stock.quantity) + int(
                        item.quantity
                    )
                    store_stock.store = instance.store
                    store_stock.save()
                    ################ store add stock ################

                    ################ warehouse decrease stock ################
                    stock, created = WarehouseStockManagement.objects.get_or_create(
                        product_and_variation=item.product_and_variation,
                        warehouse=instance.warehouse,
                    )
                    if stock.quantity > item.quantity:
                        stock.quantity = int(stock.quantity) - int(item.quantity)
                        stock.save()
                    ################ warehouse decrease stock ################
    return True
