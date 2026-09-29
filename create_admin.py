
    
from app.database import initialize_database, update_user_role

initialize_database()

username = "Radhika"
role = "admin"

updated = update_user_role(
    username=username,
    role=role
)

if updated:
    print("Radhika is now an admin.")
else:
    print("User not found.")