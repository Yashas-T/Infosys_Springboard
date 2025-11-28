import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.user_management_module import register_user_with_password, promote_user_to_admin

def create_admin():
    print("Creating default admin user...")
    user_id = "admin_01"
    username = "Admin"
    password = "admin_password" # Change this in production!
    email = "admin@example.com"
    
    # Register
    res = register_user_with_password(user_id, username, password, email)
    if res['success']:
        print(f"User {username} created.")
        # Promote
        res_promo = promote_user_to_admin(user_id)
        if res_promo['success']:
            print(f"User {username} promoted to Admin.")
        else:
            print(f"Failed to promote: {res_promo.get('error')}")
    else:
        print(f"Failed to create user: {res.get('error')}")

if __name__ == "__main__":
    create_admin()
