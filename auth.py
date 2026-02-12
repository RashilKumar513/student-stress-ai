import pandas as pd
import os
import bcrypt

ADMIN_EMAIL = "admin@panimalar.ac.in"
ADMIN_PASSWORD = "pani@123"

USER_COLUMNS = ["Name", "Email", "PasswordHash"]

def load_users():
    if not os.path.exists("users.csv") or os.path.getsize("users.csv") == 0:
        return pd.DataFrame(columns=USER_COLUMNS)
    try:
        return pd.read_csv("users.csv")
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=USER_COLUMNS)

def save_users(df):
    df.to_csv("users.csv", index=False)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(name, email, password):
    users = load_users()
    if email in users["Email"].values:
        return False
    users.loc[len(users)] = [name, email, hash_password(password)]
    save_users(users)
    return True

def authenticate(email, password):
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return "admin", "Admin"

    users = load_users()
    user = users[users["Email"] == email]

    if not user.empty and verify_password(password, user.iloc[0]["PasswordHash"]):
        return "student", user.iloc[0]["Name"]

    return None, None

def reset_password(email, new_password):
    users = load_users()
    if email not in users["Email"].values:
        return False
    users.loc[users["Email"] == email, "PasswordHash"] = hash_password(new_password)
    save_users(users)
    return True
