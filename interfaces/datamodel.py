from interface import implements, Interface

class DataModel(Interface):
    
    def save_entity(self):
        pass

    def delete_from_db(self):
        pass