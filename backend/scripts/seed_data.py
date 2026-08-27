"""
Seed data script for development.
"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.app.database.connection import SessionLocal
from backend.app.models.models import TrainingSample

SAMPLE_DATA = [
    # Spam samples
    {"message": "Congratulations! You've won a $1000 gift card. Click here to claim your prize now!", "label": "spam"},
    {"message": "URGENT: Your account has been suspended. Verify your identity immediately by clicking this link.", "label": "spam"},
    {"message": "FREE IPHONE - You have been selected to receive a free iPhone 15! Act now before the offer expires!", "label": "spam"},
    {"message": "Make money fast! Work from home and earn $5000 per week. No experience needed!", "label": "spam"},
    {"message": "You have won the Nigerian lottery! Send us your bank details to claim your $2 million prize.", "label": "spam"},
    {"message": "Hot singles in your area are waiting for you! Click here to meet them now!", "label": "spam"},
    {"message": "LIMITED TIME OFFER: 90% discount on all products! Buy now before it's too late!", "label": "spam"},
    {"message": "Your account password needs to be changed urgently. Click here to reset your password now.", "label": "spam"},
    {"message": "Dear winner, you have been selected for a special prize. Send your credit card number to claim.", "label": "spam"},
    {"message": "Buy cheap medications online! No prescription needed! Amazing deals on all products!", "label": "spam"},
    {"message": "Congratulations! You are the lucky winner of our weekly draw. Claim your prize of $50,000!", "label": "spam"},
    {"message": "Act now! This limited time offer expires in 24 hours. Don't miss out on these savings!", "label": "spam"},
    {"message": "Free trial! No credit card required! Sign up now for lifetime access to premium content!", "label": "spam"},
    {"message": "Your loan has been approved! Get $10,000 instantly! Apply now with zero interest!", "label": "spam"},
    {"message": "Click here to claim your free vacation package! You've been specially selected!", "label": "spam"},
    {"message": "URGENT: Unusual activity detected on your account. Verify now or your account will be closed!", "label": "spam"},
    {"message": "Double your income with this simple trick! Financial freedom awaits! Join now!", "label": "spam"},
    {"message": "Dear customer, your package delivery failed. Click the link to reschedule delivery immediately.", "label": "spam"},
    {"message": "You have received a payment of $4,500. Click here to view details and claim your funds.", "label": "spam"},
    {"message": "FREE weight loss supplement! Lose 30 pounds in 30 days! No exercise required! Order now!", "label": "spam"},
    # Ham samples
    {"message": "Hi John, just wanted to follow up on our meeting yesterday. Let me know if you have any questions.", "label": "ham"},
    {"message": "Meeting reminder: Team standup tomorrow at 10am in Conference Room B.", "label": "ham"},
    {"message": "Hey, are you coming to the birthday party on Saturday? Let me know so I can plan accordingly.", "label": "ham"},
    {"message": "Please find attached the quarterly report for your review. Let me know if you need any changes.", "label": "ham"},
    {"message": "Thanks for your help with the project last week. Really appreciated your input.", "label": "ham"},
    {"message": "Hi team, just a reminder that the deadline for the project proposal is next Friday.", "label": "ham"},
    {"message": "Good morning! I hope you're doing well. I wanted to discuss the new feature requirements.", "label": "ham"},
    {"message": "The server maintenance is scheduled for this weekend. Please save your work before Friday.", "label": "ham"},
    {"message": "Hi, I'm writing to confirm our appointment for next Tuesday at 2pm.", "label": "ham"},
    {"message": "Here are the notes from today's meeting. Please review and let me know if anything is missing.", "label": "ham"},
    {"message": "Happy holidays! The office will be closed from Dec 24 to Jan 2. See you next year!", "label": "ham"},
    {"message": "I've reviewed your code changes and left some comments. Please address them when you get a chance.", "label": "ham"},
    {"message": "The client approved the design mockups. We can proceed with development as planned.", "label": "ham"},
    {"message": "Can you send me the database credentials for the staging environment?", "label": "ham"},
    {"message": "Lunch is ready! I ordered pizza for the team. Come grab a slice before it's gone.", "label": "ham"},
    {"message": "Just a heads up, there might be traffic on the way to the office today due to road construction.", "label": "ham"},
    {"message": "The new design looks great! I especially like the color scheme and layout choices.", "label": "ham"},
    {"message": "Please update your timesheet for this week by end of day Friday.", "label": "ham"},
    {"message": "Great presentation today! The stakeholders were impressed with the progress we've made.", "label": "ham"},
    {"message": "I've pushed the latest changes to the development branch. Ready for code review.", "label": "ham"},
]


def seed():
    db = SessionLocal()
    try:
        existing_count = db.query(TrainingSample).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} samples. Skipping seed.")
            return

        for item in SAMPLE_DATA:
            sample = TrainingSample(message=item["message"], label=item["label"])
            db.add(sample)

        db.commit()
        print(f"Seeded {len(SAMPLE_DATA)} training samples.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
