import pandas as pd
from django.db import transaction
from django.contrib.auth import get_user_model
from jobs.models import JobCard, JobStatusLog

User = get_user_model()

class JobCardImportService:

    @staticmethod
    def import_from_excel(file_path, performed_by=None):
        """
        Import job cards from Excel with columns:
        Equipment | Task | Type | Assigned_To | Job_Card
        """

        df = pd.read_excel(file_path, engine="openpyxl")

        # Normalize column names (strip + remove spaces issues)
        df.columns = df.columns.str.strip()

        required_columns = ["Equipment", "Task", "Assigned_To", "Job_Card"]
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            return {
                "created": 0,
                "errors": [f"Missing required columns: {missing}"]
            }

        created_jobs = []
        errors = []

        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    equipment = str(row.get("Equipment")).strip()
                    task = str(row.get("Task")).strip()
                    job_card_number = str(row.get("Job_Card")).strip()
                    job_type = str(row.get("Type")).strip() if pd.notna(row.get("Type")) else None

                    if not equipment or equipment == "nan":
                        continue  # skip empty rows

                    # Handle assigned user
                    assigned_to = None
                    username_value = row.get("Assigned_To")

                    if pd.notna(username_value):
                        username_value = str(username_value).strip()
                        assigned_to = User.objects.filter(
                            username__iexact=username_value
                        ).first()

                        if not assigned_to:
                            errors.append(
                                f"Row {idx+2}: User '{username_value}' not found"
                            )

                    # Determine initial status
                    initial_status = (
                        JobCard.STATUS_ASSIGNED
                        if assigned_to
                        else JobCard.STATUS_OPEN
                    )

                    # Create or update using Job_Card as unique identifier
                    job, created = JobCard.objects.update_or_create(
                        job_card_number=job_card_number,
                        defaults={
                            "title": equipment,
                            "description": task,
                            "assigned_to": assigned_to,
                            "status": initial_status,
                            "job_type": job_type,  # only if field exists
                        }
                    )

                    # Log status if newly created
                    if created:
                        JobStatusLog.objects.create(
                            job_card=job,
                            previous_status="",
                            new_status=initial_status,
                            performed_by=performed_by
                        )

                    created_jobs.append(job)

                except Exception as e:
                    errors.append(f"Row {idx+2}: {str(e)}")

        return {
            "created": len(created_jobs),
            "errors": errors
        }
