import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import time

from crews import get_crews


def run_pipeline(crews, checkpoint_path="checkpoint.json"):
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, "r", encoding="utf-8") as file:
            state = json.load(file)
    else:
        state = {}

    current_input = {"topic": "Application of AI in healthcare"}

    for index, crew in enumerate(crews):
        stage = f"stage_{index}"
        print(f"[START] {stage}")

        if stage in state:
            print(f"Skipping {stage} (already completed)")
            current_input = {"previous_result": state[stage]}
            print(f"[END] {stage}")
            continue

        for attempt in range(3):
            try:
                result = crew.kickoff(inputs=current_input)
                result_text = str(result)
                state[stage] = result_text

                with open(checkpoint_path, "w", encoding="utf-8") as file:
                    json.dump(state, file, ensure_ascii=False, indent=2)

                current_input = {"previous_result": result_text}
                print(f"[END] {stage}")
                break
            except Exception as error:
                print(f"{stage} attempt {attempt + 1} failed: {error}")
                if attempt == 2:
                    raise RuntimeError(f"{stage} failed after 3 attempts") from error
                time.sleep(2 ** attempt)

    return state


if __name__ == "__main__":
    crews = get_crews()
    final_state = run_pipeline(crews)
    print("Pipeline finished.")
    print(final_state)
