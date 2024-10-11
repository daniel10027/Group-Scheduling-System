import pandas as pd
from django.shortcuts import render, redirect
from .models import Salle
from django.core.files.storage import FileSystemStorage
from .models import *

def home(request):
    context = {
        "salles" : Salle.objects.all().order_by('campus','nom','capacite'),
        "filieres" : Filiere.objects.all().order_by('cycle','niveau','nom'),
    }
    return render(request,'index.html', context=context)

def upload_salles(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        # Process Excel file
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            Salle.objects.create(
                nom=row['salle'],
                campus=row['campus'],
                capacite=row['effectifs']
            )
        return redirect('home')

    return render(request, 'upload_salles.html')


def upload_filieres(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        # Process Excel file
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            Filiere.objects.create(
                nom=row['FILIERE'],
                niveau=row['NIVEAU'],
                cycle=row['CYCLE'],
                nombre_inscrits=row['INSCRITS']
            )
        return redirect('home')

    return render(request, 'upload_filieres.html')


def generate_groups(request):
    # Fetch all salles and filieres
    salles = Salle.objects.all().order_by('capacite')  # Sort by capacity in ascending order
    filieres = Filiere.objects.all()

    # DataFrames for processing
    salle_df = pd.DataFrame(list(salles.values('id', 'nom', 'capacite')))
    filiere_df = pd.DataFrame(list(filieres.values('id', 'nom', 'niveau', 'cycle', 'nombre_inscrits')))

    assigned_groups = []

    # List to track assigned groups to each room
    room_assignments = {salle['id']: [] for salle in salle_df.to_dict('records')}

    # Iterate through each filiere
    for _, filiere in filiere_df.iterrows():
        nombre_inscrits = filiere['nombre_inscrits']
        numero_groupe = 1  # Reset group number for each filiere

        # Divide students into groups based on salle capacity
        while nombre_inscrits > 0:
            # Find the best-fit salle for the current group size
            available_salles = salle_df[salle_df['capacite'] >= max(30, nombre_inscrits)]  # Ensure minimum group size of 30

            if available_salles.empty:
                # If no salle fits the entire group, get the largest available salle
                salle = salle_df[salle_df['capacite'] >= 30].iloc[0]
            else:
                # Choose the salle with the smallest capacity that fits the group
                salle = available_salles.iloc[0]

            capacite_salle = salle['capacite']

            # Calculate the number of students that will fit in this room
            if nombre_inscrits > capacite_salle:
                # Create group for the full capacity of the salle
                students_in_group = capacite_salle
            else:
                # Assign the rest of the students to the last group
                students_in_group = nombre_inscrits

            # Try to assign the group to a room in an available time slot
            assigned = False
            for salle_id in room_assignments.keys():
                if salle_id == salle['id']:
                    # Check for morning slot availability
                    if all(assignment['time'] != 'morning' for assignment in room_assignments[salle_id]):
                        # Assign morning slot
                        heure_debut = "08:00"
                        heure_fin = "12:00"
                        room_assignments[salle_id].append({
                            'time': 'morning',
                            'group': numero_groupe
                        })
                        assigned = True
                        break

                    # Check for afternoon slot availability
                    if all(assignment['time'] != 'afternoon' for assignment in room_assignments[salle_id]):
                        # Assign afternoon slot
                        heure_debut = "13:00"
                        heure_fin = "17:00"
                        room_assignments[salle_id].append({
                            'time': 'afternoon',
                            'group': numero_groupe
                        })
                        assigned = True
                        break

            if assigned:
                # Add group assignment
                assigned_groups.append({
                    'filiere_id': filiere['id'],
                    'salle_id': salle['id'],
                    'numero_groupe': numero_groupe,
                    'heure_debut': heure_debut,
                    'heure_fin': heure_fin,
                    'nombre_etudiants': students_in_group
                })

                # Decrease the number of students left to assign
                nombre_inscrits -= students_in_group
                numero_groupe += 1  # Increment the group number for the next group
            else:
                # If no slots available, break to avoid infinite loop
                break

    # Save groups to the database
    for group in assigned_groups:
        Group.objects.create(
            filiere_id=group['filiere_id'],
            salle_id=group['salle_id'],
            numero_groupe=group['numero_groupe'],
            heure_debut=group['heure_debut'],
            heure_fin=group['heure_fin'],
            nombre_etudiants=group['nombre_etudiants']
        )

    return redirect('results')



def display_results(request):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'results.html', context)


def reset(request):
    filieres = Filiere.objects.all()
    salles = Salle.objects.all()
    filieres.delete()
    salles.delete()
    return redirect('home')
    