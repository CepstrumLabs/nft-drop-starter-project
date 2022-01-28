from pathlib import Path
from typing import List
import argparse
import json
import logging

class AssetProperty:
    def to_json(self):
        return {}

class FileProperty(AssetProperty):
    PNG_TYPE = "image/png"
    ALL_TYPES = [PNG_TYPE]

    def __init__(self, uri, type_=PNG_TYPE):
        self.uri = uri
        self.type = type_

    def to_json(self):
        return {
                "uri": self.uri,
                "type": self.type
            }

class FilesProperty(AssetProperty):
    def __init__(self,files: List[FileProperty]):
        self.files = files
    
    def to_json(self):
        return [file.to_json() for file in self.files]
    
    def add_file_property(self, file_property: FileProperty):
        assert isinstance(FileProperty)
        self.files.append(file_property)

class CreatorProperty(AssetProperty):
    def __init__(self, address: str, share: int):
        self.address = address
        self.share = share
    
    def to_json(self):
        return {
                "address": self.address,
                "share": self.share
            }

class CreatorsProperty(AssetProperty):
   
    def __init__(self, items: List[CreatorProperty]):
        self.items = items 
    
    def to_json(self):
        return [item.to_json() for item in self.items]

    def add_creator_property(self, creator_property: CreatorProperty):
        assert isinstance(CreatorProperty)
        self.files.append(creator_property)


properties = {
    "files": FilesProperty(files=[FileProperty(uri="0.png")]).to_json(),
    "creators": CreatorsProperty(items=[CreatorProperty(address="walletAddress", share=100)]).to_json()
}


class Asset:
    def __init__(self,
        name: str,
        symbol: str,
        image: Path,
        properties: List[AssetProperty]
    ):
        self.name = name
        self.symbol = symbol
        self.image = image
        self.properties = properties
    
    def to_dict(self):
        return {
            "name": self.name,
            "symbol": self.symbol,
            "image": self.image,
            "properties": self.properties
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())

def create_json_file_from_png(path, creator_wallet):
    path_name = path.name
    workdir = path.parent
    config_file_path = workdir / f"{path.stem}.json"
    with open(config_file_path, 'w') as config_file:
        properties = {
            "files": FilesProperty(files=[FileProperty(uri=path_name)]).to_json(),
            "creators": CreatorsProperty(items=[CreatorProperty(address=creator_wallet, share=100)]).to_json()
        }
        asset = Asset(name="DopeThinkerzNft", symbol="NFTv1", image=path_name, properties=properties)
        config_file.write(asset.to_json())
        logger.info(f"Created {config_file_path} for NFT {path}")
        
    
def create_config_from_dir(directory: str, creator_wallet: str):
    """
    Create empty config files for the asset directory
    Assumes there are png files
    """
    path_directory = Path(directory)
    assert path_directory.exists(), "The assets directory you provided does not exist"
    for path in path_directory.glob("*.png"):
        try:        
            create_json_file_from_png(path=path, creator_wallet=creator_wallet)
        except:
            logger.exception(f"Something went wrong with {path}")
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-dir", "-a", help="Assets directory to scan", type=str, required=True)
    parser.add_argument("--creator-wallet", "-cw", help="Public key of creator", type=str, required=True)
    args = parser.parse_args()
    create_config_from_dir(directory=args.assets_dir, creator_wallet=args.creator_wallet)
    