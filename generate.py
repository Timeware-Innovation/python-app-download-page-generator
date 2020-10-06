from PyInquirer import prompt
import os
import shutil

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SCRIPT_PATH, 'template')
ENV_FOLDER_PATH = os.path.join(TEMPLATE_PATH, 'env-folder')


def make_subs(path, subs_dict):
    with open(path, "r") as f:
        string = f.read()
        for key in subs_dict.keys():
            string = string.replace(f'[${key}]', subs_dict[key])
        with open(path, "w") as f:
            f.write(string)


def run():
    questions = [
        {
            'type': 'checkbox',
            'name': 'env',
            'message': "Which environments do you want to generate?",
            'choices': [
                {
                    'name': 'Development',
                    'checked': True,
                },
                {
                    'name': 'Staging',
                    'checked': True,
                },
                {
                    'name': 'Production',
                    'checked': True,
                },
            ]
        },
        {
            'type': 'list',
            'name': 'redirect',
            'message': "Where should index.html redirect to?",
            'default': 2,
            'choices': [
                'Development',
                'Staging',
                'Production',
            ]
        },
        {
            'type': 'input',
            'name': 'title',
            'message': 'What\'s app title?',
        },
        {
            'type': 'input',
            'name': 'name',
            'message': 'What\'s app folder name?',
            'default': lambda answers: answers['title'].lower().replace(" ", "-"),
            'validate': lambda val: 'You must provider a folder name' if not val else True,
        },
        {
            'type': 'input',
            'name': 'background-color',
            'message': 'What\'s hex background color?',
            'default': '#FFF',
        },
        {
            'type': 'input',
            'name': 'text-color',
            'message': 'What\'s hex text color?',
            'default': '#000',
        },
        {
            'type': 'input',
            'name': 'button-color',
            'message': 'What\'s hex button color?',
            'default': '#000',
        },
        {
            'type': 'input',
            'name': 'button-text-color',
            'message': 'What\'s hex button text color?',
            'default': '#FFF',
        },
    ]

    # Get answers from user
    answers = prompt(questions)

    # Create container
    dst_path = os.path.join('.', answers['name'])
    os.mkdir(dst_path)

    # Copy index.html
    shutil.copy2(os.path.join(TEMPLATE_PATH, 'index.html'),
                 os.path.join(dst_path, 'index.html'))

    # Make substitutions
    make_subs(os.path.join(dst_path, 'index.html'), {'redirect': answers['redirect'].lower()})

    # Copy env-folders
    for env_title in answers['env']:
        env = env_title.lower()
        folder_path = os.path.join(dst_path, env)
        shutil.copytree(ENV_FOLDER_PATH, folder_path)

        # Make substitutions in index.html
        make_subs(
            os.path.join(folder_path, 'index.html'),
            {'title': answers['title'],
             'env-capitalized': env_title,
             'env-uppercase': env.upper(),
             'env': env,
             'background-color': answers['background-color'],
             'text-color': answers['text-color'],
             'button-color': answers['button-color'],
             'button-text-color': answers['button-text-color'],
             'name': answers['name'], })

        # Make substitution in manifest.plist
        make_subs(os.path.join(folder_path, 'manifest.plist'), {
            'title': answers['title'],
            'name': answers['name'],
            'env': env,
        })

    # Success!
    print(f'Created a site in {dst_path}. Please remember to update images/logo.png and .ipa, .apk files.')


run()
