from django.db import models


# Create your models here.
class Traduccion_de_verbos_ingles(models.Model):
    verbo = models.CharField(max_length=40)
    traduccion_uno = models.CharField(max_length=40)
    traduccion_dos = models.CharField(max_length=40)

    def __str__(self):
        return self.verbo


############### PRETERITE ###############


class Conjugacion_preterite(models.Model):
    persona = models.CharField(max_length=40)
    verbo = models.CharField(max_length=40)
    conjugacion = models.CharField(max_length=40)


############### PRESENT ###############


class Conjugacion_present(models.Model):
    persona = models.CharField(max_length=40)
    verbo = models.CharField(max_length=40)
    conjugacion = models.CharField(max_length=40)


class Conjugacion_present_continuous(models.Model):
    persona = models.CharField(max_length=40)
    auxiliar = models.CharField(max_length=40)
    verbo = models.CharField(max_length=40)
    conjugacion = models.CharField(max_length=40)


############### FUTURE ###############
class Conjugacion_future(models.Model):
    persona = models.CharField(max_length=40)
    auxiliar = models.CharField(max_length=40)
    verbo = models.CharField(max_length=40)
    conjugacion = models.CharField(max_length=40)
