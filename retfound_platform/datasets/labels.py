GRADES = ['No DR', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']
CLASS_MAP = {
    'anodr': 0, 'bmilddr': 1, 'cmoderatedr': 2, 'dseveredr': 3,
    'eproliferativedr': 4, 'eprodr': 4, **{str(i): i for i in range(5)},
}
SPLITS = {'train': 'train', 'val': 'val', 'validation': 'val', 'test': 'test'}


def identity(path: str) -> tuple[str, int]:
    parts = path.split('/')
    locations = [i for i, part in enumerate(parts) if part.lower() in SPLITS]
    if len(locations) != 1 or locations[0] != len(parts) - 3:
        raise ValueError('Expected [dataset/]train|val|test/grade/image')
    label = parts[-2].lower()
    if label not in CLASS_MAP:
        raise ValueError(f'Unknown grade folder: {label}')
    return SPLITS[parts[locations[0]].lower()], CLASS_MAP[label]
