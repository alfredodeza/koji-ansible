#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import common_koji


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: koji_archivetype

short_description: Create and manage Koji archive types

Note: this relies on an API not yet in Koji upstream:
https://pagure.io/koji/pull-request/1149
'''


def run_module():
    module_args = dict(
        koji=dict(type='str', required=False, default='koji'),
        name=dict(type='str', required=True),
        description=dict(type='str', required=True),
        extensions=dict(type='str', required=True),
        state=dict(type='str', required=True),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not common_koji.HAS_KOJI:
        module.fail_json(msg='koji is required for this module')

    params = module.params
    profile = params['koji']
    name = params['name']
    description = params['description']
    extensions = params['extensions']
    state = params['state']

    session = common_koji.get_session(profile)

    result = {'changed': False}

    if state == 'present':
        if not session.getArchiveType(type_name=name):
            common_koji.ensure_logged_in(session)
            session.addArchiveType(name, description, extensions)
            result['changed'] = True
    elif state == 'absent':
        module.fail_json(msg="Cannot remove Koji archive types.",
                         changed=False, rc=1)
    else:
        module.fail_json(msg="State must be 'present' or 'absent'.",
                         changed=False, rc=1)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
