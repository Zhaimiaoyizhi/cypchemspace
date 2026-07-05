import numpy as np

from cypchemspace.enrichment import knn_label_enrichment


def test_knn_label_enrichment_detects_clustered_positive_labels():
    features = np.array(
        [
            [1, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1],
            [0, 0, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1],
        ]
    )
    labels = ["mydb", "mydb", "mydb", "mydb", "p450db", "p450db", "p450db", "p450db"]

    result = knn_label_enrichment(features, labels, positive_label="mydb", k=2, n_permutations=99, random_state=7)

    assert result["observed_positive_neighbor_fraction"] == 1.0
    assert result["mean_null_positive_neighbor_fraction"] < result["observed_positive_neighbor_fraction"]
    assert 0.0 < result["p_value"] <= 1.0
