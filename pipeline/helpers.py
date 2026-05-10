import json
import os


def save_results(
    final_results,
    output_path="outputs/results.json"
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with open(output_path, "w") as f:

        json.dump(
            final_results,
            f,
            indent=2
        )

    print(f"\nSaved results -> {output_path}")