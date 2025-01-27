# D'n'D Data for AI Prototyping

You can use the data for being able to discuss `backgrounds`, `classes`, `equipment`, `feats`, `magic-items`, `monsters`, `species` and `spells`.

## Usage

Index the `data` directory, which includes pictures and markdown documents:

    data
    ├── backgrounds
    │   ├── acolyte.png
    │   ├── acolyte.txt
    │   ├── ...
    │   ├── soldier.png
    │   └── soldier.txt
    ├── classes
    │   ├── barbarian.png
    │   ├── barbarian.txt
    │   ├── ...
    │   ├── wizard.png
    │   └── wizard.txt
    ├── equipment
    │   ├── abacus.jpg
    │   ├── abacus.txt
    │   ├── ...
    │   └── two-weapon-fighting.txt
    ├── magic-items
    │   ├── adamantine-armor.jpg
    │   ├── adamantine-armor.txt
    │   ├── ...
    │   ├── wings-of-flying.jpeg
    │   └── wings-of-flying.txt
    ├── monsters
    │   ├── aboleth.png
    │   ├── aboleth.txt
    │   ├── ...
    │   ├── zombie.png
    │   └── zombie.txt
    ├── species
    │   ├── dragonborn.png
    │   ├── dragonborn.txt
    │   ├── ...
    │   ├── tiefling.png
    │   └── tiefling.txt
    └── spells
        ├── acid-arrow.png
        ├── acid-arrow.txt
        ├── ...
        ├── zone-of-truth.png
        └── zone-of-truth.txt


## Generation

Prepare the environment:

    make prepare
    . bin/activate
    make install

Generate selected assets: `backgrounds`, `classes`, `equipment`, `feats`, `magic-items`, `monsters`, `species` or `spells`:

    mkdir data/<asset_type>
    make <asset_type>
