__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

'''
update the .ignore file
update the lab.yaml file
TODO: check dependencies and alert new versions
TODO: update the setup.py file
'''

_update_details = {
    'title': 'Update',
    'description': 'Updates the configuration files for a service with the latest pocketlab configurations.',
    'help': 'updates the config files for a service',
    'benefit': 'Keeps your services up-to-date with the latest configurations.'
}

from pocketlab.init import fields_model

def update(service_list, all=False, verbose=True):

    title = 'update'

# validate inputs
    if isinstance(service_list, str):
        if service_list:
            service_list = [service_list]
    input_fields = {
        'service_list': service_list
    }
    for key, value in input_fields.items():
        if value:
            object_title = '%s(%s=%s)' % (title, key, str(value))
            fields_model.validate(value, '.%s' % key, object_title)

# define message insert
    msg_insert = 'service'

# retrieve vcs templates
    from pocketlab.methods.vcs import load_ignore
    vcs_templates = {
        'git': load_ignore(vcs='git'),
        'mercurial': load_ignore(vcs='mercurial')
    }

    def _apply_update(root_path, service_name=''):

    # construct message
        msg_insert = 'service'
        if service_name:
            msg_insert = 'service "%s"' % service_name

    # update vcs ignore
        import hashlib
        from os import path
        from pocketlab.methods.vcs import merge_ignores
        vcs_files = {
            'git': {
                'path': path.join(root_path, '.gitignore'),
                'name': '.gitignore'
            },
            'mercurial': {
                'path': path.join(root_path, '.hgignore'),
                'name': '.hgignore'
            }
        }
        for key, value in vcs_files.items():
            if path.exists(value['path']):
                old_text = open(value['path']).read()
                old_hash = hashlib.sha1(old_text.encode('utf-8')).hexdigest()
                new_text = merge_ignores(old_text, vcs_templates[key])
                new_hash = hashlib.sha1(new_text.encode('utf-8')).hexdigest()
                if old_hash != new_hash:
                    with open(value['path'], 'wt') as f:
                        f.write(new_text)
                        f.close()
                    if verbose:
                        print('%s file for %s updated.' % (value['name'], msg_insert))

    # update lab yaml
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from jsonmodel.validators import jsonModel
        from labpack.records.settings import save_settings, load_settings
        config_schema = jsonLoader(__module__, 'models/lab-config.json')
        config_model = jsonModel(config_schema)
        template_config = config_model.ingest()
        config_path = path.join(root_path, 'lab.yaml')
        if path.exists(config_path):
            try:
                old_config = load_settings(config_path)
                template_config.update(**old_config)
                if old_config != template_config:
                    from pocketlab.methods.config import compile_yaml
                    config_text = compile_yaml(config_schema, config_path)
                    with open(config_path, 'wt') as f:
                        f.write(config_text)
                        f.close()
                    if verbose:
                        print('lab.yaml file for %s updated.' % msg_insert)
            except:
                 print('lab.yaml file for %s is corrupted. Skipped.' % msg_insert)

# construct service list
    update_list = []

# add named service to service list
    if service_list:
        msg_insert = ''
        for i in range(len(service_list)):
            service = service_list[i]
            if msg_insert:
                if i + 1 == len(service_list):
                    msg_insert += ' and '
                else:
                    msg_insert += ', '
            msg_insert += '"%s"' % service
            from pocketlab.methods.service import retrieve_service_root
            service_root = retrieve_service_root(service)
            service_details = {
                'name': service,
                'path': service_root
            }
            update_list.append(service_details)

# add all services in registry to service list
    elif all:
        msg_insert = 'all services'
        from pocketlab import __module__
        from labpack.storage.appdata import appdataClient
        registry_client = appdataClient(collection_name='Registry Data', prod_name=__module__)
        from labpack.records.settings import load_settings
        for file_path in registry_client.localhost.walk(registry_client.collection_folder):
            try:
                details = load_settings(file_path)
                service_details = {
                    'name': details['service_name'],
                    'path': details['service_root']
                }
                update_list.append(service_details)
            except:
                pass

# add local path to service list
    else:
        update_list.append({'name':'', 'path':'./'})

# apply updates
    for service in update_list:
        update_kwargs = {
            'root_path': service['path'],
            'service_name': service['name']
        }
        _apply_update(**update_kwargs)

# construct exit message
    exit_msg = 'Configurations for %s have been updated.' % msg_insert

    return exit_msg
