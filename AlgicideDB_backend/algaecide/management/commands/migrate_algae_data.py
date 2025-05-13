from django.core.management.base import BaseCommand
from algaecide.models import Algae, AlgaeStrain, Record

class Command(BaseCommand):
    help = "Update the algae_strain field in Record based on the old algae field."

    def handle(self, *args, **kwargs):
        records_updated = 0
        for record in Record.objects.all():
            old_algae = record.algae
            if old_algae:
                try:
                    algae_strain = AlgaeStrain.objects.get(
                        species__name=old_algae.name,
                        strain=old_algae.strain
                    )
                    record.algae_strain = algae_strain
                    record.save()
                    records_updated += 1
                except AlgaeStrain.DoesNotExist:
                    self.stdout.write(
                        f"No matching AlgaeStrain found for Algae: {old_algae.name} (Strain: {old_algae.strain})"
                    )
        self.stdout.write(f"Updated {records_updated} records successfully.")
