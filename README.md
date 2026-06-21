# Sound Cue Utilities

Generate X32 snippet/show files or QLab network cues from an Excel cue tracking spreadsheet.

This project reads a spreadsheet where the first column contains channel numbers and the cue columns are numbered. A marker, usually `X`, means that channel should be unmuted for that cue. The optional DCA marker, usually `/`, can assign selected channels to an ensemble DCA group.

## Requirements

- An `.xlsx` cue tracking spreadsheet
- macOS and QLab for `METHOD=NETWORK`

`METHOD=SNIPPET` only writes files and does not require QLab.

## Spreadsheet Shape

Use the [Sound Cue Spreadsheet Template](https://docs.google.com/spreadsheets/d/1Ll1G1Qmv-pMB3NbNWADFaHzB3je_3KfsqAQJo5kN6DY/) to start a new cue tracking spreadsheet.

The first column should contain channel numbers. Cue columns should be numeric, such as `1`, `2`, `3`, and so on.

Example:

| Channel | Name | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| 1 | Alice | X |  | / |
| 2 | Bob |  | X | X |

With the default config:

- `X` means unmuted.
- `/` means unmuted and assigned to the ensemble DCA group when DCA output is enabled.
- Blank cells mean muted.

## Setup

Install `uv` if needed:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the project dependencies:

```sh
uv sync
```

Create your local config:

```sh
cp .env.example .env
```

Edit `.env` for your spreadsheet and preferred output mode.

## Configuration

| Variable | Description |
| --- | --- |
| `TYPE` | Mixer type for network cue generation. `X32` is currently supported. |
| `FILE_NAME` | Path to the Excel spreadsheet. |
| `ROW_START` | First spreadsheet row containing channel data. |
| `IDENTIFYING_CHARACTER` | Marker for channels that should be unmuted. |
| `METHOD` | `SNIPPET` or `NETWORK`. |
| `USE_DCA` | Enables DCA group output when set to `true`. |
| `DCA_IDENTIFIER` | Marker for ensemble/DCA channels. |
| `NETWORK_PATCH` | QLab network patch number for `METHOD=NETWORK`. |

## Run

For snippet/show file generation:

```sh
uv run python main.py
```

Snippet output is written to `output/`.

For QLab network cue generation:

1. Open QLab on macOS.
2. Open the target workspace.
3. Set `METHOD=NETWORK` in `.env`.
4. Set `NETWORK_PATCH` to the QLab network patch you want to use.
5. Run the script.

The script creates a group cue for each cue column and adds network cues under it.

## Notes

- `applescript/sq-network.applescript` exists, but SQ support is still in progress.
