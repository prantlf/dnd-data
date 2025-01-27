# D'n'D Data for AI Prototyping

You can use the data for being able to discuss `backgrounds`, `classes`, `equipment`, `feats`, `magic-items`, `monsters`, `species` and `spells`.

## Usage

Index the `data` directory, which includes pictures and markdown documents:

    data
    ├── backgrounds
    │   ├── acolyte.png
    │   ├── acolyte.md
    │   ├── ...
    │   ├── soldier.png
    │   └── soldier.md
    ├── classes
    │   ├── barbarian.png
    │   ├── barbarian.md
    │   ├── ...
    │   ├── wizard.png
    │   └── wizard.md
    ├── equipment
    │   ├── abacus.jpg
    │   ├── abacus.md
    │   ├── ...
    │   └── two-weapon-fighting.md
    ├── magic-items
    │   ├── adamantine-armor.jpg
    │   ├── adamantine-armor.md
    │   ├── ...
    │   ├── wings-of-flying.jpeg
    │   └── wings-of-flying.md
    ├── monsters
    │   ├── aboleth.png
    │   ├── aboleth.md
    │   ├── ...
    │   ├── zombie.png
    │   └── zombie.md
    ├── species
    │   ├── dragonborn.png
    │   ├── dragonborn.md
    │   ├── ...
    │   ├── tiefling.png
    │   └── tiefling.md
    └── spells
        ├── acid-arrow.png
        ├── acid-arrow.md
        ├── ...
        ├── zone-of-truth.png
        └── zone-of-truth.md


## Generation

Prepare the environment:

    make prepare
    . bin/activate
    make install

Generate selected assets: `backgrounds`, `classes`, `equipment`, `feats`, `magic-items`, `monsters`, `species` or `spells`:

    mkdir data/<asset_type>
    make <asset_type>
