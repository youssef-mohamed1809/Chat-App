import bcrypt

class UserAuthentication:
    PEPPER = "pepper_hash"

    def hashPassword(self, message, salt):
        hashed_password = bcrypt.hashpw((self.PEPPER + message + salt.decode("utf-8")).encode('utf-8'), salt)
        return hashed_password

    def createNewHash (self, message):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw((self.PEPPER + message + salt.decode("utf-8")).encode('utf-8'), salt)
        return hashed_password,salt

    def checkValidity(self, retrievedPass, retrievedSalt, message):
        hashed_message = self.hashPassword(message, retrievedSalt)
        return retrievedPass == hashed_message