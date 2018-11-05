from edusson_ds_main.db.connections import DBConnectionsFacade


class Repository:
    def __init__(self):
        self.session = DBConnectionsFacade.get_edusson_ds_orm_session()

    def commit(self):
        self.session.commit()

    def add(self, obj):
        self.session.add(obj)

    def delete(self, obj):
        self.session.delete(obj)
