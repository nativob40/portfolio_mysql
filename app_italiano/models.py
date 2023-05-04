from django.db import models

# Create your models here.
class Traduccion_de_verbos(models.Model):

    verbo = models.CharField(max_length=40)
    traduccion_uno = models.CharField(max_length=40)
    traduccion_dos = models.CharField(max_length=40)

class Conjugacion_presente_semplice(models.Model):

    verbo = models.CharField(max_length=40)
    persona = models.CharField(max_length=40)
    conjugacion = models.CharField(max_length=40)

class Conjugacion_passato_prossimo(models.Model):

    verbo = models.CharField(max_length=40)
    persona = models.CharField(max_length=40)
    auxiliar = models.CharField(max_length=40)
    conjugacion = models.CharField(max_length=40)

class Conjugacion_futuro_semplice(models.Model):

    verbo = models.CharField(max_length=40)
    persona = models.CharField(max_length=40)
    conjugacion = models.CharField(max_length=40)