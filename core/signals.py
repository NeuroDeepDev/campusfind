from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Item, Claim, Audit


@receiver(pre_save, sender=Item)
def item_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Item.objects.get(pk=instance.pk)
            if old.name != instance.name or old.status != instance.status or old.description != instance.description:
                Audit.objects.create(op_type='UPDATE', op_by='system', details=f'Item {instance.item_id} updated')
        except Item.DoesNotExist:
            pass


@receiver(post_save, sender=Claim)
def claim_post_save(sender, instance, created, **kwargs):
    if not created:
        # log status change
        Audit.objects.create(op_type='UPDATE', op_by='system', details=f'Claim {instance.claim_id} status {instance.status}')
