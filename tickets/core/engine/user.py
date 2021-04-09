class UserAdmin:

    def get_user(self):
        return self.request.user 

    def get_user_roles(self, module):
        return self.request.user.role.filter(module=module)