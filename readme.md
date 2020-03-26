# notion-automata
It's an automata for notion.so!

#### Okay, that sounds interesting but what does it do, exactly?
Well, it's a piece of code that hooks up to my notion workspace via unofficial [API wrapper](https://github.com/jamalex/notion-py).

The code uses my token (like credentials) to manage everything that I have set up in notion, but _programatically_.  
This lets me automate some of usual boring tasks such as cleaning up unneded blocks in links (archived via notion browser extension).  

It also lets me do more complex stuff, like, say - converting my notes in blog page to markdown documents and then publishing them on my blog.
Now that part is pretty interesting for me, because I like tightening the feedback loops. One of such loops is the blog-posting workflow.  
It sucks. Not that it's complicated or anything, I'm using the _simple_ stuff already, but it's not particularly effective, either.  

So that's where this automata page comes in - it lets me do stuff that I'd normally do, but using Python instead of my hands!

Here's an example page of my console:
- `Console activated!` - that's an indicator that the code is running fine
- `localhost` - it points to the web hook where the code is deployed
- `clean links` - that's the first command that I wrote
  - `output` - for logs from this particular command
  - `config` - I can pass a YAML config to the code
  - `source` - code for command is inlined right into notion!
- `publish blog posts` - similar stuff, goes trough pages and publishes them
- `notion-automata` - that's like the root config, used for all commands
  - `output` - logs from the main script :)
  - `config` - meta config for particular commands, like the icons used, text, etc


There's also some emoji-meaningful info baked in for each command.
Blue means that it's executing, green means that it succeeded and red means that it failed.


#### Hey, that's really cool, can I use it?
Sure! but it's bit hacky for now, I'm working on making this accessible for everyone, including non-programmers :)
My idea is to share this console page as a public template, then provide bunch of public snippets for doing popular tasks
and finally hosting the code itself on AWS lambda or somewhere like that so that you can use it just simply as any other template.


<p align="center"><img width="755" height="1600" src="https://i.imgur.com/884XhCv.png"></p>
