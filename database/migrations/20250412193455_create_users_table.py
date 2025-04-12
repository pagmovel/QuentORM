from quentorm import Migration

class CreateUsersTable(Migration):
    def up(self):
        self.create_table('users', [
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'created_at DATETIME',
            'updated_at DATETIME'
        ])

    def down(self):
        self.drop_table('users')
