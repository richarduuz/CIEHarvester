import toml

data = toml.load(open('settings.toml'))
data['authentication']['admin_password'] = 'test'
toml.dump(data, open('settings.toml', 'w'))