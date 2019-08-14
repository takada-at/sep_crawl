from pathlib import Path


root_dir = Path(__file__).parent / '../../'


def url2path(link):
    path = (root_dir / 'data/sep/html').resolve()
    if not path.exists():
        path.mkdir(parents=True)
    filename = link.split('/')[-2] + '.html'
    return path / filename


def textpath(filepath):
    path = (root_dir / 'data/sep/text').resolve()
    if not path.exists():
        path.mkdir(parents=True)
    filename = filepath.with_suffix('.txt')
    return path / (filename.name)


def entries_text():
    path = (root_dir / 'data/sep/').resolve()
    if not path.exists():
        path.mkdir(parents=True)
    return path / 'entries.txt'
