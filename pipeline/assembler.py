def assemble_context(results: list[dict]) -> tuple[str, dict]:
    if not results:
        return "", {}

    context_block = ""
    source_map = {}

    for i, result in enumerate(results, start=1):
        context_block += f"[{i}] {result['url']}\n{result['content']}\n\n"
        source_map[i] = {
            "url": result["url"],
            "title": result.get("title", result["url"])
        }

    return context_block, source_map