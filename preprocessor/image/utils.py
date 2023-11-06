import random
import shutil
from pathlib import Path
from typing import Union


def split_dataset(path: Union[str, Path], split_ratio: Union[dict, list, tuple, float]):
    """
    This function is designed for splitting a dataset into [train, val, test] sub dataset.
    :param path: The Dataset path
    :param split_ratio: A dict/list/tuple/float
        A dictionary with at least one of 'train','val','test',
        A list/tuple should include 3 value, which means 'train','val','test',
        A float is a train ratio of dataset, and the remaining portion is for test. There will be no valid dataset.
    """
    if isinstance(path, str):
        path = Path(path)
    images_path = path / 'images'
    train_path = path / 'train'
    valid_path = path / 'val'
    test_path = path / 'test'

    train_path.mkdir(exist_ok=True)
    valid_path.mkdir(exist_ok=True)
    test_path.mkdir(exist_ok=True)

    train_ratio = split_ratio.get('train', 0)
    val_ratio = split_ratio.get('val', 0)
    test_ratio = split_ratio.get('test', 0)

    def split_data(data_list: list[Path], data_path: Path):
        data_path.mkdir(exist_ok=True)
        for p in data_list:
            shutil.copy(p, data_path)

    try:
        from tqdm import tqdm
        iterator = tqdm(images_path.glob('./*'), 'Split Dataset')
    except ImportError:
        print('Split Dataset...')
        iterator = images_path.glob('./*')
    for label in iterator:
        files_name = list(label.glob('*.jpg'))
        random.shuffle(files_name)
        length = len(files_name)
        train_index = int(train_ratio * length)
        val_index = int((train_ratio + val_ratio) * length)

        split_data(files_name[:train_index], train_path / label.name)
        split_data(files_name[train_index:val_index], valid_path / label.name)
        split_data(files_name[val_index:], test_path / label.name)
