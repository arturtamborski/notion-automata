from textwrap import wrap

from notion.block import CalloutBlock, ToggleBlock
from yaml import safe_load


class Config:
    started: str = "✅"
    stopped: str = "❌"
    idle: str = "⬜"
    running: str = "🔵"
    finished: str = "🟢"
    failed: str = "🔴"


class CodeBlock:
    title = "`code`"
    language = "Plain Text"

    def __init__(self, block: ToggleBlock):
        self.block = block
        assert self.block.title == self.title
        assert self.block.type == "toggle"

        assert len(self.block.children) == 1
        self.code = self.block.children[0]
        assert self.code.language == self.language
        assert self.code.type == "code"


class OutputBlock(CodeBlock):
    title = "`output`"
    language = "CSS"
    line_length = 70

    def __init__(self, block):
        super().__init__(block)
        self.code.title_plaintext = ""

    def log(self, message: str, prefix: str = "log: "):
        nl = "\n" if self.code.title_plaintext.strip() else ""
        for m in wrap(message, self.line_length):
            self.code.title_plaintext += f"{nl}{prefix}{m}"

    def err(self, message: str, prefix: str = "err: "):
        self.log(message, prefix)


class ConfigBlock(CodeBlock):
    title = "`config`"
    language = "YAML"

    def get(self, key: str = None) -> dict:
        config = safe_load(self.code.title_plaintext) or {}
        if key:
            return config[key]
        return config


class SourceBlock(CodeBlock):
    language = "Python"

    def get(self) -> str:
        return self.code.title_plaintext


class StatusBlock:
    def __init__(self, block: CalloutBlock, index: int, other: list):
        self.block = block
        self.block.icon = Config.started
        self.block.title = "Console activated!"

    def __del__(self):
        self.block.icon = Config.stopped
        self.block.title = "Click on the link to start console"


class AutomataBlock:
    def __init__(self, block: CalloutBlock, index: int, other: list):
        self.block = block
        assert self.block.title == "notion-automata"
        self.output = OutputBlock(other[index + 1])
        self.config = ConfigBlock(other[index + 2])
        for k, v in self.config.get("icons").items():
            setattr(Config, k, v)


class CommandBlock:
    def __init__(self, block: CalloutBlock, index: int, other: list):
        self.block = block
        self.output = OutputBlock(other[index + 1])
        self.config = ConfigBlock(other[index + 2])
        self.source = SourceBlock(other[index + 3])
        self.block.icon = Config.running

    def __del__(self):
        self.block.icon = Config.idle

    def run(self, globs: dict):
        if not (source := self.source.get()):
            return

        globs.update(
            {
                # for some reason this has to be done trough lambda, idek
                "log": lambda *msgs: self.output.log(" ".join(f"{m}" for m in msgs)),
                "err": lambda *msgs: self.output.err(" ".join(f"{m}" for m in msgs)),
                "config": self.config.get(),
            }
        )

        try:
            name = self.block.title
            code = compile(source, name, "exec")
            exec(code, globs)
            self.block.icon = Config.finished
        except Exception as e:
            self.block.icon = Config.failed
            self.output.err(e.args[0])
            return e.args[0]
