from django.db import models

class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    niveau = models.CharField(max_length=100)
    cycle = models.CharField(max_length=100)
    nombre_inscrits = models.IntegerField()

    def __str__(self):
        return f"{self.nom} {self.niveau} {self.cycle}"

class Salle(models.Model):
    nom = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    capacite = models.IntegerField()

    def __str__(self):
        return f"{self.nom} ({self.campus}) - Capacité: {self.capacite}"

class Group(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    numero_groupe = models.IntegerField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    nombre_etudiants = models.IntegerField()

    def __str__(self):
        return f"Groupe {self.numero_groupe} de {self.filiere.nom} {self.filiere.niveau}"
