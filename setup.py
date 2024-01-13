from setuptools import setup


def get_long_desc() -> str:
    with open('README.md', 'r') as file_handle:
        lines = []
        for line in next(file_handle):
            if len(line.strip()) == 0:
                break
            else:
                lines.append(line)
        return "\n".join(lines)

setup(
    name='vectara-speech-helper',
    description='Vectara Speech Helper',
    long_description=get_long_desc(),
    long_description_content_type='text/markdown',
    version='0.0.2',
    author='David Levy',
    author_email='david.g.levy@gmail.com',
    url='https://github.com/davidglevy/vectara-speech-helper',
    license='GNU AFFERO GENERAL PUBLIC LICENSE v3',
    package_dir={
        'vectara_speech': 'vectara_speech'
    },
    packages=['vectara_speech'],
    install_requires=['vectara-skunk-client>=0.4.14'],
    python_requires='>=3.12',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities'
    ]
)