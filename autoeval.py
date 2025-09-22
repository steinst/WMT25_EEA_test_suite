import pandas as pd
import os

def get_original_data():
    data_file = "test_suite/evaluated/EEA_evaluated_automatically.tsv"

    # Read the TSV file
    data = pd.read_csv(data_file, sep='\t').to_dict(orient='records')

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Build the dictionary
    entries = []
    for _, row in df.iterrows():
        entry = {
            "Category": row["Category"],
            "Lines submitted": row["Lines_submitted"],
            "English": row["English"],
            "Icelandic": row["Icelandic"],
            "Terms English": [x.strip() for x in str(row["Terms_English"]).split(",")] if pd.notna(row["Terms_English"]) else [],
            "Terms Icelandic": [x.strip() for x in str(row["Terms_Icelandic"]).split(",")] if pd.notna(row["Terms_Icelandic"]) else []
        }
        entries.append(entry)

    data_dict = {"entries": entries}
    return data_dict


def get_translation_data():
    folder_path = "test_suite/submissions"

    # Get all filenames in the folder (sorted for consistency)
    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

    # Initialize the main dictionary
    line_dict = {i: {} for i in range(351)}

    # Read each file
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) != 351:
                raise ValueError(f"File '{filename}' does not have exactly 351 lines.")
            for i, line in enumerate(lines):
                line_dict[i][filename] = line.strip()
    return line_dict


def create_form_dict():
    with open("test_suite/EEA_inflections.tsv", "r", encoding="utf-8") as f:
        lines = f.readlines()
        form_dict = {}
        for line in lines:
            currline = line.strip().split('\t')
            form_dict[currline[0]] = {'lines': currline[1].strip(';').split(';'), 'forms': currline[2].strip(';').split(';')}
    return form_dict


def get_correct_lines():
    filtered_entries = {}
    for entry in data_dict["entries"]:
        linur = str(entry.get("Lines submitted", ""))
        if not linur.find(';') > -1:
            filtered_entries[linur] = entry
    return filtered_entries


form_dict = create_form_dict()
data_dict = get_original_data()
translation_dict = get_translation_data()

correct_lines = get_correct_lines()

model_scores_terms = {}
total_terms = 0
model_scores_sentences = {}
total_sentences = 0
for i in correct_lines.keys():
    numer = i
    curr_terms = []
    for term in correct_lines[i]["Terms Icelandic"]:
        curr_terms.append(term.strip().lstrip())
    total_terms += len(curr_terms)
    try:
        line_number = int(correct_lines[i]["Lines submitted"])
        total_sentences += 1
    except:
        continue
    line_number_down = line_number - 1
    translations = translation_dict[line_number-1]
    for key in translations:
        model = key
        model_terms = 0
        model_all_correct = True
        translation = translations[key].lower()
        for term in curr_terms:
            for term_form in form_dict[term]['forms']:
                if translation.find(term_form.lower()) != -1:
                    model_terms += 1
                    break
            else:
                model_all_correct = False
        if model in model_scores_terms.keys():
            model_scores_terms[model] += model_terms
        else:
            model_scores_terms[model] = model_terms
        if model in model_scores_sentences.keys():
            if model_all_correct:
                model_scores_sentences[model] += 1
        else:
            if model_all_correct:
                model_scores_sentences[model] = 1
            else:
                model_scores_sentences[model] = 0


df = pd.DataFrame({
    "Key": list(model_scores_terms.keys()),
    "Terms": list(model_scores_terms.values()),
    "Sentences": [model_scores_sentences[k] for k in model_scores_terms.keys()]
})

# Compute percentages
df["% Terms"] = df["Terms"] / total_terms * 100
df["% Sentences"] = df["Sentences"] / total_sentences * 100

# Sort by % Terms descending
df = df.sort_values("% Terms", ascending=False)

# Reset index for clean display
df = df.reset_index(drop=True)

print(df.to_string(index=False, float_format="%.1f"))
