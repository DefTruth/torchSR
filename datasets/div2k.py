from PIL import Image

import os

import torch
import torch.utils.data as data
import torchvision
from typing import Any, Callable, List, Optional, Tuple, Union


def pil_loader(path: str) -> Image.Image:
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


class Folder(data.Dataset):
    def __init__(
            self,
            root: str,
            scales: List[Union[int, float]],
            transform: Optional[Callable] = None,
            loader = pil_loader
    ) -> None:
        super(Folder, self).__init__()
        self.root = os.path.expanduser(root)
        self.loader = loader
        self.transform = transform
        self.scales = scales
        self.samples = []

    def __getitem__(self, index: int) -> List[Any]:
        images = [self.loader(path) for path in self.samples[index]]
        if self.transform is not None:
            images = self.transform(images)
        return images
        

    def __len__(self) -> int:
        return len(self.samples)


class Div2K(Folder):
    """`DIV2K <https://data.vision.ee.ethz.ch/cvl/DIV2K/>` Superresolution Dataset

    Args:
        root (string): Root directory of the DIV2K Dataset.
        scale (int, optional): The upsampling ratio: 2, 3, 4 or 8.
        track (str, optional): The downscaling method: bicubic, unknown, real_mild,
            real_difficult, real_wild.
        split (string, optional): The dataset split, supports ``train``, or ``val``.
        transform (callable, optional): A function/transform that takes in several PIL images
            and returns a transformed version. It is not a torchvision transform!
        loader (callable, optional): A function to load an image given its path.
        download (boolean, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.


    Attributes:
        scales (list): List of the downsampling scales
    """

    urls = {
        "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_HR.zip" : "bdc2d9338d4e574fe81bf7d158758658"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_HR.zip" : "9fcdda83005c5e5997799b69f955ff88"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_bicubic_X2.zip" : "9a637d2ef4db0d0a81182be37fb00692"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_bicubic_X2.zip" : "1512c9a3f7bde2a1a21a73044e46b9cb"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_bicubic_X3.zip" : "ad80b9fe40c049a07a8a6c51bfab3b6d"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_bicubic_X3.zip" : "18b1d310f9f88c13618c287927b29898"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_bicubic_X4.zip" : "76c43ec4155851901ebbe8339846d93d"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_bicubic_X4.zip" : "21962de700c8d368c6ff83314480eff0"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_unknown_X2.zip" : "1396d023072c9aaeb999c28b81315233"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_unknown_X2.zip" : "d319bd9033573d21de5395e6454f34f8"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_unknown_X3.zip" : "4e651308aaa54d917fb1264395b7f6fa"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_unknown_X3.zip" : "05184168e3608b5c539fbfb46bcade4f"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_unknown_X4.zip" : "e3c7febb1b3f78bd30f9ba15fe8e3956"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_unknown_X4.zip" : "8ac3413102bb3d0adc67012efb8a6c94"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_x8.zip" : "613db1b855721b3d2b26f4194a1d22a6"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_x8.zip" : "c5aeea2004e297e9ff3abfbe143576a5"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_mild.zip" : "807b3e3a5156f35bd3a86c5bbfb674bc"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_mild.zip" : "8c433f812ca532eed62c11ec0de08370"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_difficult.zip" : "5a8f2b9e0c5f5ed0dac271c1293662f4"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_difficult.zip" : "1620af11bf82996bc94df655cb6490fe"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_LR_wild.zip" : "d00982366bffee7c4739ba7ff1316b3b"
      , "http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_LR_wild.zip" : "aacae8db6bec39151ca5bb9c80bf2f6c"
    }

    track_dirs = {
        ('hr', 'train', 1) : os.path.join('DIV2K_train_HR')
      , ('hr', 'val', 1) : os.path.join('DIV2K_valid_HR')
      , ('bicubic', 'train', 2) : os.path.join('DIV2K_train_LR_bicubic', 'X2')
      , ('bicubic', 'train', 3) : os.path.join('DIV2K_train_LR_bicubic', 'X3')
      , ('bicubic', 'train', 4) : os.path.join('DIV2K_train_LR_bicubic', 'X4')
      , ('bicubic', 'train', 8) : os.path.join('DIV2K_train_LR_X8')
      , ('bicubic', 'val', 2) : os.path.join('DIV2K_valid_LR_bicubic', 'X2')
      , ('bicubic', 'val', 3) : os.path.join('DIV2K_valid_LR_bicubic', 'X3')
      , ('bicubic', 'val', 4) : os.path.join('DIV2K_valid_LR_bicubic', 'X4')
      , ('bicubic', 'val', 8) : os.path.join('DIV2K_valid_LR_X8')
      , ('unknown', 'train', 2) : os.path.join('DIV2K_train_LR_unknown', 'X2')
      , ('unknown', 'train', 3) : os.path.join('DIV2K_train_LR_unknown', 'X3')
      , ('unknown', 'train', 4) : os.path.join('DIV2K_train_LR_unknown', 'X4')
      , ('unknown', 'val', 2) : os.path.join('DIV2K_valid_LR_unknown', 'X2')
      , ('unknown', 'val', 3) : os.path.join('DIV2K_valid_LR_unknown', 'X3')
      , ('unknown', 'val', 4) : os.path.join('DIV2K_valid_LR_unknown', 'X4')
      , ('real_mild', 'train', 4) : os.path.join('DIV2K_train_LR_mild')
      , ('real_mild', 'val', 4) : os.path.join('DIV2K_valid_LR_mild')
      , ('real_difficult', 'train', 4) : os.path.join('DIV2K_train_LR_difficult')
      , ('real_difficult', 'val', 4) : os.path.join('DIV2K_valid_LR_difficult')
      # real_wild is there but needs special handling (multiple downscaled images)
      #, ('real_wild', 'train', 4) : os.path.join('DIV2K_train_LR_wild')
      #, ('real_wild', 'val', 4) : os.path.join('DIV2K_valid_LR_wild')
    }

    def __init__(
            self,
            root: str,
            scale: Union[int, List[int]] = 2,
            track: Union[str, List[str]] = 'bicubic',
            split: str = 'train',
            transform: Optional[Callable] = None,
            loader = pil_loader,
            download: bool = False):
        if isinstance(scale, int):
            scale = [scale]
        if isinstance(track, str):
            track = [track] * len(scale)
        if len(track) != len(scale):
            raise ValueError("The number of scales and of tracks must be the same")
        self.split = split
        self.tracks = track
        super(Div2K, self).__init__(os.path.join(root, 'DIV2K'), scale, transform, loader)
        if download:
            self.download()
        self.init_samples()

    def get_tracks(self):
        return set(t for (t, sp, sc) in self.track_dirs.keys())

    def get_splits(self):
        return ["train", "val"]

    def get_dir(self, track, split, scale):
        if (track, split, scale) not in self.track_dirs:
            if track not in self.get_tracks():
                raise ValueError(f"Track {track} does not exist. Use one of {list(self.get_tracks())}")
            if split not in self.get_splits():
                raise ValueError(f"Split {split} is not valid")
            raise ValueError(f"Div2K track {track} does not include scale X{scale}")
        return os.path.join(self.root, self.track_dirs[(track, split, scale)])

    def list_samples(self, track, split, scale):
        track_dir = self.get_dir(track, split, scale)
        all_samples = sorted(os.listdir(track_dir))
        return [os.path.join(track_dir, s) for s in all_samples]

    def init_samples(self):
        samples = []
        for track, scale in zip(['hr'] + self.tracks, [1] + self.scales):
            samples.append(self.list_samples(track, self.split, scale))
        for i, s in enumerate(samples[1:]):
            if len(s) != len(samples[0]):
                raise ValueError(f"Number of files for {self.tracks[i]}X{self.scales[i]} does not match HR")
        self.samples = []
        for i in range(len(samples[0])):
            self.samples.append([s[i] for s in samples])

    def download(self):
        # We just download everything: the X4/X8 datasets are not big anyway
        for url, md5sum in self.urls.items():
            torchvision.datasets.utils.download_and_extract_archive(url, self.root, md5=md5sum)

