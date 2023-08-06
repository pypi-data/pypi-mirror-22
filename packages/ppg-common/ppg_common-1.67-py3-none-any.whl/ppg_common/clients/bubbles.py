from ppg_common.clients.base import BaseClient


class BubblesClient(BaseClient):
    urls = {
        "permission": BaseClient.version + "/permissions/{}",
        "permissions": BaseClient.version + "/permissions/",
        "users_permissions": BaseClient.version + "/permissions/file/{}",
        "status": BaseClient.version + "/status/"
    }

    def __init__(self, host, port, ssl=False, session=None):
        super(BubblesClient, self).__init__(host, port, ssl, session)

    def get_status(self):
        return self.get(self.urls.get('status'))

    def get_users_permissions(self, object_id):
        return self.get(self.urls.get('users_permissions').format(object_id))

    def get_permissions(self):
        return self.get(self.urls.get('permissions'))

    def get_permission(self, object_id):
        return self.get(self.urls.get('permission').format(object_id))

    def delete_permission_on_file(self, object_id, subject_id=""):
        return self.delete(self.urls.get(
            'users_permissions'
        ).format(object_id), query={'subject_id': subject_id})

    def add_permission(self, subject_id, object_id, read, write, delete):
        body = {
            'subject_id': subject_id,
            'object_id': object_id,
            'read': read,
            'write': write,
            'delete': delete
        }
        return self.post(self.urls.get('permissions'), body=body)

    def edit_permission(self, object_id, subject_id=None, read=None,
                        write=None, delete=None):
        body = {}
        if subject_id is not None:
            body.update({'subject_id': subject_id})
        if read is not None:
            body.update({'read': read})
        if write is not None:
            body.update({'write': write})
        if delete is not None:
            body.update({'delete': delete})
        return self.patch(self.urls.get('permission').format(object_id),
                          body=body)

    def delete_permission(self, object_id):
        return self.delete(self.urls.get('permission').format(object_id))
