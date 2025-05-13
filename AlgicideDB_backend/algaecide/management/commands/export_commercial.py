import csv
from django.core.management.base import BaseCommand
from algaecide.models import Record, Chemical, AlgaeSpecies

class Command(BaseCommand):
    help = 'Export Commercial algicides with associated algae species, chemical classification, and reference titles'

    def handle(self, *args, **kwargs):
        # Filter records where the chemical origin is 'Commercial'
        records = Record.objects.filter(chemical__origin='Commercial')

        # Initialize a dictionary to store unique chemical data
        chemicals_data = {}

        # Loop through each record and organize data
        for record in records:
            chemical = record.chemical
            algae_species = record.algae_strain.species if record.algae_strain else None
            reference_title = record.reference.title if record.reference else None

            if algae_species:
                # If the chemical is already in the dictionary, append the algae species
                if chemical.name in chemicals_data:
                    # Add the algae species to the set
                    chemicals_data[chemical.name]['algae_species'].add(algae_species.name)
                    # Add the reference title to the set
                    if reference_title:
                        chemicals_data[chemical.name]['reference_titles'].add(reference_title)
                else:
                    # Otherwise, create a new entry for this chemical and initialize algae_species and reference_titles as sets
                    chemicals_data[chemical.name] = {
                        'classification': chemical.classification,
                        'algae_species': {algae_species.name},  # Initialize with the first algae species
                        'reference_titles': {reference_title} if reference_title else set()  # Initialize with the first reference title
                    }

        # Prepare CSV file for export
        filename = 'commercial_algicides.csv'
        with open(filename, mode='w', newline='', encoding='utf-8') as file:  # Specify encoding as 'utf-8'
            writer = csv.writer(file, delimiter='\t')  # Use tab as delimiter
            writer.writerow(['Chemical Name', 'Chemical Classification', 'Algae Species', 'Reference Titles'])

            # Write the collected data into the CSV
            for chemical_name, data in chemicals_data.items():
                # Join all algae species for the same chemical into a single string
                algae_species_str = ', '.join(sorted(data['algae_species']))
                # Join all reference titles into a single string
                reference_titles_str = ', '.join(sorted(data['reference_titles']))
                writer.writerow([chemical_name, data['classification'], algae_species_str, reference_titles_str])

        self.stdout.write(self.style.SUCCESS(f'Successfully exported data to {filename}'))
