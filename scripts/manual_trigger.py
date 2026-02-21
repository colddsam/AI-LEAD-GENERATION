import argparse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tasks.daily_pipeline import run_manual_full_pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manually trigger the Lead Generation Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending emails")
    args = parser.parse_args()
    
    print(f"Starting Manual Pipeline execution. Dry run: {args.dry_run}")
    
    # Enqueue the celery task, or run directly if needed.
    # To run without a worker running, we will call the function directly.
    run_manual_full_pipeline()
    
    print(f"Pipeline executed synchronously.")
