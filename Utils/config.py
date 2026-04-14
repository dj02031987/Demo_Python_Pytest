import yaml


def load_config(env='Tenforce'):
    with open('Config/Config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config.get(env, config['Tenforce'])


def config():
    with open('Config/Config.yml', 'r') as file:
        return yaml.safe_load(file)