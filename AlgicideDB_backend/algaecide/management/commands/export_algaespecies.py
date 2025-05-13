import csv
from django.core.management.base import BaseCommand
from algaecide.models import AlgaeSpecies


class Command(BaseCommand):
    help = "Export AlgaeSpecies data to a CSV file"

    def handle(self, *args, **kwargs):
        # Specify the output file
        file_name = "algae_species.csv"
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write header row
            writer.writerow([
                "Empire",
                "Kingdom",
                "Phylum",
                "Class",
                "Order",
                "Family",
                "Genus",
                "Species",
                # "Environment",
                # "Risk",
            ])

            # Write data rows
            for species in AlgaeSpecies.objects.all():
                genus = species.name.split(" ")[0] if species.name else ""
                writer.writerow([
                    species.empire,
                    species.kingdom,
                    species.phylum,
                    species.class_name,
                    species.order,
                    species.family,
                    genus,
                    species.name,
                    # species.environment,
                    # species.risk,
                ])

        self.stdout.write(self.style.SUCCESS(f"Data exported successfully to {file_name}"))
