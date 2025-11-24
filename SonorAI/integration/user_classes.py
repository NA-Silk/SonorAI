class User:
    def __init__(self, username, first_name, last_name, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_superuser = False

    def __str__(self):
        return self.username


class Admin(User):
    def __init__(self, username, first_name, last_name, email, password):
        super().__init__(username, first_name, last_name, email, password)
        self.is_superuser = True

    def manageUsers(self, system, action, **kwargs):
        if action == "create":
            return system.register_user(
                username=kwargs["username"],
                first_name=kwargs["first_name"],
                last_name=kwargs["last_name"],
                email=kwargs["email"],
                password=kwargs["password"]
            )

        elif action == "delete":
            username = kwargs["username"]
            system.users.pop(username, None)
            system.myfiles_pages.pop(username, None)

        elif action == "update_email":
            username = kwargs["username"]
            user = system.get_user(username)
            if user:
                user.email = kwargs["email"]

    def manageMyFiles(self, system, username, action, **kwargs):
        if action == "delete":
            system.delete_user_file(username, kwargs["title"])
        elif action == "rename":
            system.rename_user_file(username, kwargs["old_title"], kwargs["new_title"])
        elif action == "favorite":
            system.favorite_user_file(username, kwargs["title"], favorite=kwargs.get("favorite", True))
