from django.db import models


class Groups(models.Model):
    name = models.CharField(max_length=200)


class Sticker(models.Model):
    name = models.CharField(max_length=200)
    meta = models.JSONField(blank=True, null=True)
    group = models.ForeignKey(Groups, related_name='group_id',
                              on_delete=models.SET_NULL,
                              blank=True, null=True)
    image = models.ImageField(upload_to='stickers/static/images/stickers', blank=True, null=True)


class PerToPer(models.Model):
    sticker = models.ForeignKey(Sticker, related_name='p2p',
                                on_delete=models.CASCADE,
                                blank=True, null=True)
    amount = models.IntegerField()


class Trade(models.Model):
    sticker = models.ForeignKey(Sticker, related_name='trade',
                                on_delete=models.CASCADE,
                                blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    wanted_per_to_per = models.ManyToManyField(PerToPer, blank=True, null=True)


class User(models.Model):
    pass
