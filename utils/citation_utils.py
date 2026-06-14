import re

def render_citations(response_text: str, source_map: dict) -> str:
    def replace_citation(match):
        numbers = [n.strip() for n in match.group(1).split(",")]
        links = []
        for n in numbers:
            n_int = int(n)
            if n_int in source_map:
                meta = source_map[n_int]
                links.append(f"[[{n}]({meta['url']})]")
            else:
                links.append(f"[[{n}]]")
        return " ".join(links)

    cleaned_text = re.sub(r"Sources used:.*", "", response_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r"Sources:.*", "", cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r"\n[\d,\s]+$", "", cleaned_text.strip())
    cleaned_text = cleaned_text.strip()
    linked_text = re.sub(r"\[(\d+(?:,\s*\d+)*)\]", replace_citation, cleaned_text)

    if source_map:
        sources_md = "\n\n---\n**Sources**\n"
        for n, meta in source_map.items():
            sources_md += f"{n}. [{meta['title']}]({meta['url']})\n"
        linked_text += sources_md

    return linked_text