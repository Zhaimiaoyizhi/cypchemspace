import pandas as pd

from cypchemspace.visualize import assign_plot_groups


def test_assign_plot_groups_marks_shared_inchikey_rows():
    table = pd.DataFrame(
        {
            "std_inchikey": ["SHARED", "SHARED", "MYDB_ONLY", "P450_ONLY"],
            "label": ["mydb", "p450db", "mydb", "p450db"],
        }
    )

    groups = assign_plot_groups(table)

    assert groups.tolist() == ["shared", "shared", "mydb", "p450db"]
