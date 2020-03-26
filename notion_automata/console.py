from notion.client import NotionClient

from notion_automata.blocks import StatusBlock, AutomataBlock, CommandBlock


def find_all(items, **kwargs):
    return [
        (item, index)
        for index, item in enumerate(items)
        if all((getattr(item, k) == v for k, v in kwargs.items()))
    ]


def find_first(items, **kwargs):
    return find_all(items, **kwargs)[0]


def launch(token):
    client = NotionClient(token_v2=token)
    pages = client.get_top_level_pages()

    console, _ = find_first(pages, type="page", title="console")
    callouts = find_all(console.children, type="callout")
    assert len(callouts) >= 2

    status = StatusBlock(*callouts[0], console.children)
    automata = AutomataBlock(*callouts[-1], console.children)
    log = automata.output.log

    commands = []
    log("started, looking for commands...")

    for block, index in callouts[1:-1]:
        log(f"  found '{block.title}', hooking up... ")
        try:
            commands.append(CommandBlock(block, index, console.children))
        except Exception as e:
            log(f"  failed, {e.args[0]}")
            continue

    log("all hooked up, executing...")

    for command in commands:
        log(f"  running '{command.block.title}'")
        globs = {
            "dir": dir,
            "type": type,
            "getattr": getattr,
            "setattr": setattr,
            "pages": pages,
            "find_all": find_all,
            "find_first": find_first,
        }
        if out := command.run(globs):
            log(f"  failed, {out}")

    log("all executed, quitting.")
