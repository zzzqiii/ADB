from django.core.management.base import BaseCommand
from algaecide.models import Chemical

class Command(BaseCommand):
    help = 'Update the form field of chemicals where isnp is False, setting it to Compound or Extract'

    def handle(self, *args, **kwargs):
        # Step 1: Filter chemicals where isnp is False
        chemicals = Chemical.objects.filter(isnp=False)

        # Step 2: Iterate over these chemicals and update the form field
        updated_count = 0  # Counter to track how many records were updated
        for chemical in chemicals:
            # Step 3: Check if 'extract' is in the name (case-insensitive)
            if 'extract' in chemical.name.lower():
                chemical.form = 'Crude Extract'
            else:
                chemical.form = 'Isolated Compound'

            # Save the updated chemical record
            chemical.save()
            updated_count += 1

        # Output the result
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} chemicals.'))
