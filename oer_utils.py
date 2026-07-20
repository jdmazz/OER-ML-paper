"""Shared preprocessing helpers.

Both ``preprocessing.ipynb`` and ``dJdVpreprocess.ipynb`` load the same
composition lookup table, list the same kind of per-sample data files, and
match a data filename back to its composition row. Those steps live here so
they are written once.
"""

import os

import pandas as pd

# Column indices (0-based) of Pt, Pd, Au, Ir in the summary table.
COMPOSITION_COLS = (6, 7, 8, 9)


def load_catalyst_summary(summary_csv):
    """Load and clean the Pt/Pd/Au/Ir composition lookup table.

    Normalises the ``Run #`` key, gives the atomic-percent columns short
    names, and fills missing electrolyte resistances with the column mean.
    """
    df = pd.read_csv(summary_csv)
    df['Run #'] = (
        df['Run #'].str.split('-').str[0].str.lower().str.strip()
    )
    df.rename(
        columns={
            'Pt (Atomic%)': 'Pt',
            'Pd (Atomic%)': 'Pd',
            'Au (Atomic%)': 'Au',
            'Ir (Atomic%)': 'Ir',
        },
        inplace=True,
    )
    df['iR drop (Ω)'] = df['iR drop (Ω)'].fillna(
        df['iR drop (Ω)'].mean()
    )
    return df


def list_data_files(directory):
    """Return the plain files inside ``directory`` (skips subfolders).

    Sorted so that output row order — and therefore anything seeded
    downstream of it, like train/test splits — is reproducible across
    machines instead of inheriting the filesystem's listing order.
    """
    return sorted(
        f
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    )


def match_composition(catalyst_df, filename):
    """Find the composition row for a per-sample data ``filename``.

    Filenames look like ``Run12-spot37.DTA.csv``; the run id is the first
    hyphen-delimited token and the sample number is the trailing ``spotNN``.
    """
    parts = filename.lower().split('.')[0].split('-')
    run_id = parts[0].strip()
    sample_num = int(parts[-1].replace('spot', ''))
    return catalyst_df[
        (catalyst_df['Run #'] == run_id)
        & (catalyst_df['Sample #'] == sample_num)
    ]


def composition_values(cat_row):
    """Return the (Pt, Pd, Au, Ir) atomic percentages from a matched row."""
    return [cat_row.iloc[0, i] for i in COMPOSITION_COLS]
