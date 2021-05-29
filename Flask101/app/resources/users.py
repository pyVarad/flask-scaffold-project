from flask_restful import Resource, reqparse
from models.user import User
from logger import logger


class UserResource(Resource):
    """ User controller.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('firstName', type=str, required=False, help="Missing mandatory field firstName")
    parser.add_argument('lastName', type=str, required=False, help="Missing mandatory field lastName")
    parser.add_argument('emailAddress', type=str, required=False, help="Missing mandatory field emailAddress")

    def get(self, userId):
        logger.info("Get user by id.")
        user = User.findById(userId)
        if user:
            return user.json()

        return {"message": f"The {userId} is not found!"}, 400

    def delete(self, userId):
        logger.info("Delete user for a given user Id.")
        user = User.findById(userId)
        if user:
            user.delete()
            return {"message": f"The {userId} is deleted successfully"}
        return {"message": f"The {userId} does not exist!"}, 400

    def put(self, userId):
        logger.info("Update user for a given user Id.")
        data = UserResource.parser.parse_args()
        user = User.findById(userId)
        if user:
            logger.debug(f"The {userId} already exists, hence updating the userInfo.")

            user.emailAddress = data['emailAddress'] if data.get('emailAddress') else user.emailAddress
            user.lastName = data['lastName'] if data.get('lastName') else user.lastName
            user.firstName = data['firstName'] if data.get('firstName') in data else user.firstName
        
            user = user.add()
            logger.debug(f"Successfully updated the user {userId}.")
            return user.json(), 201

        logger.debug(f"Missing user {userId}.")
        return {"message": f"The {userId} does not exist!"}, 400
        



class UsersResource(Resource):
    """ User[s] controller.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Missing mandatory field username")
    parser.add_argument('firstName', type=str, required=True, help="Missing mandatory field firstName")
    parser.add_argument('lastName', type=str, required=True, help="Missing mandatory field lastName")
    parser.add_argument('emailAddress', type=str, required=True, help="Missing mandatory field emailAddress")

    def get(self):
        logger.info("Get all users.")
        return {
            "users": [user.json() for user in User.query.all()]
        }

    def post(self):
        logger.info("Add new user.")
        data = UsersResource.parser.parse_args()

        user = User.findById(data['username'])
        if user:
            logger.error(f"The user with username {data['username']} already exists.")
            return {"message": f"The {data['username']} already exists!"}, 400
        
        user = User(**data)
        user = user.add()
        logger.debug(f"Successfully added the user: {data['username']}.")

        return user.json(), 201 