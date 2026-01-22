import pyotp

def generate_otp_secret():
    return pyotp.random_base32()

def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret, interval=30)
    return totp.verify(otp)