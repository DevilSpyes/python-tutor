
import os

kb_file = 'public/static/js/knowledge_base_data.js'
faq_file = 'faq_output.js'

with open(kb_file, 'r') as f:
    kb_content = f.read()

with open(faq_file, 'r') as f:
    faq_content = f.read()

# Extract the array content from faq_output.js
# It starts after "const GENERAL_PYTHON_FAQ = [" and ends before "];"
start_marker = "const GENERAL_PYTHON_FAQ = ["
end_marker = "];"

start_idx = faq_content.find(start_marker)
end_idx = faq_content.rfind(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: Could not find array markers in faq_output.js")
    exit(1)

new_data = faq_content[start_idx + len(start_marker):end_idx].strip()

# Remove the last closing bracket from kb_content
kb_end_marker = "];"
kb_end_idx = kb_content.rfind(kb_end_marker)

if kb_end_idx == -1:
    print("Error: Could not find closing bracket in knowledge_base_data.js")
    exit(1)

# Construct the new content
# We add a comma if the last item didn't have one (it should, but good to check)
# Actually, JSON objects in the array should be comma separated.
# The existing array ends with an object.
# We'll add a comma and the new data.

original_data = kb_content[:kb_end_idx].strip()
if original_data.strip().endswith(','):
    separator = "\n"
else:
    separator = ",\n"

new_section_header = "\n    // SECCIÓN 6 — FAQ General Python\n"

merged_content = original_data + separator + new_section_header + new_data + "\n];\n"

with open(kb_file, 'w') as f:
    f.write(merged_content)

print("Successfully merged FAQ data into knowledge_base_data.js")
