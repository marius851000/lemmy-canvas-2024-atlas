# Contributing

This project is open-source, and contributions are welcome. In fact, the Atlas relies on user contributions.

You may contribute to the project by submitting a Pull Request on the GitHub repo or sending your submissions through [Lemmy](https://toast.ooo/c/2024lemmycanvasatlas). Other than that, you can get help from [Matrix](https://matrix.to/#/#lemmy-canvas-atlas-discussion:mariusdavid.fr) or [Lemmy](https://toast.ooo/c/2024lemmycanvasatlas).

## New Atlas entries

To contribute to the map, we require a certain format for artwork region and labels. This can be generated on [the drawing mode](https://atlas.mariusdavid.fr/?mode=draw) on the website. 

To add a new entry, go to [the drawing mode](https://atlas.mariusdavid.fr/?mode=draw) and draw a shape/polygon around the region you'd like to describe. You can use the <kbd>Undo</kbd>, <kbd>Redo</kbd>, and <kbd>Reset</kbd> buttons to help you creating a good polygon. Make sure that the lines you're drawing don't form a [self-intersecting polygon](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Complex_polygon.svg/288px-Complex_polygon.svg.png).

You can also edit existing entries. To do that, [enter the normal mode](https://atlas.mariusdavid.fr/), select the entry you want to edit, then click `Edit`. To retrace it, you can click `Add Period`, then `Delete` the old first Period.

If you want to see which areas of the canvas do not have entries yet, select "Highlight Empty" to hide areas that already have entries.

When you're happy with the shape you've drawn, press <kbd>Finish</kbd>. You will now be able to enter some information about the entry:

//TODO:canvas adaptation: implement Lemmy and Matrix links actually
- **Name**: A short, descriptive name.
- **Description**: A short description that can be understood by somebody not familiar with the topic. If you were involved in drawing this artwork, you may include the meta, describing the process of drawing the artwork in the event.
- **Links**: Some links that are most relevant to the topic, and/or regarding the process of the drawing the artwork in the event.
	- **Lemmy**: A Lemmy community or server, in the form of an URL
	- **Matrix**: A matrix room id of the organizers, in the form of `#room_id:server.tld`
	- **Website**: If you're describing a project, the project's main website would be suitable here.
	- **Subreddit**: Format it like `r/subreddit`.
	- **Discord**: Write the invite code, that the invite link without the `discord.gg/` part.

All fields but the name are optional. For example, a country flag doesn't necessarily need a description.

Once you've entered all the information, you'll be presented with a pop-up window containing some [JSON](https://en.wikipedia.org/wiki/JSON)-formatted data. This is the patch that you are going to submit. Depending on the method, there are two preferred methods. 

### Through Lemmy

You will need to post that message to the `!2024lemmycanvasatlas@toast.ooo` community via Lemmy (or another Activity-Pub powered service that allow long enought messages).

Past the whole JSON file in the body, and then post it. Eventually, a bot should answer that your post has been processed (or not) in less than 30 minutes. If that does not happen after 1 hour, then this is a bug, and you can report it. You can also use the second contributionn method.

### Through GitHub (TODO:lemmy adapatation DOCUMENTATION UNFINISHED: WHAT ABOUT THE ID AND REPLACING?)

If you know about Git and how to create a pull request on GitHub, you can create a patch that will be merged as-is in the repo.

You can try pressing the <kbd>Submit Direct to GitHub</kbd> button, which will open a page with the patch file already been prepared to you. 

If that didn't work, copy the entire JSON text and [create a new patch file to the repository through GitHub](https://github.com/marius851000/lemmy-canvas-2024-atlas/new/main/entries?filename=ENTRY-SLUG-HERE.json
). Upon opening, replace the `ENTRY-SLUG-HERE` into the title of the entry (with the slug format, if possible, e.g. `foo-bar`). You don't need to add any other text; just directly send the patch. 

If you haven't forked the repository, you would need to fork it with the provided instruction shown on the page. You may add attribution by adding an `_author` key, explained in the next paragraphs.

The commit message and description doesn't matter, but you may change it into something more descriptive to make it easier for checking (e.g. <kbd>Add Foo Bar</kbd> or <kbd>Edit Foo Bar</kbd> for the commit message). However, we suggest you to edit the title (at least) and the description of the pull request, containing the changes that you want to do (something like <kbd>Add Foo Bar</kbd> or <kbd>Edit Foo Bar</kbd> for the title, similar to the commit message, is also sufficient).

Once you have successfully created the patch, the file can be committed, and a pull request towards the `main` branch can be created. A member will merge the pull request if it is adequate.

### Example

Hereforth is an example of the structured entry data (from the original r/place 2023 Atlas)

```json5
{
	"id": 1,
	"name": "An entry",
	"description": "This is an entry, it is remarkable.",
	"links": {
		"subreddit": ["placeAtlas2023", "subreddit1", "subreddit2"],
		"discord": ["pJkm23b2nA"],
		"website": ["https://example.com"],
		"wiki": ["An_Entry", "An_Entry_2"]
	},
	"path": {
		"109-166, T:0-1": [
			[1527, 1712],
			[1625, 1712],
			[1625, 1682]
		]
	},
	"center": {
		"109-166, T:0-1": [1639, 1754]
	}
}
```

`109-166, T:0-1` has this meaning.
  - `109-166`: Default canvas variation (r/place), period [109](https://2023.place-atlas.stefanocoding.me/#/109) to [166](https://2023.place-atlas.stefanocoding.me/#/166).
  - `T:0-1`: "The Final Clean" canvas variation, period [0](https://2023.place-atlas.stefanocoding.me/#/T:0) (The Final Clean) to [1](https://2023.place-atlas.stefanocoding.me/#/T:1) (Unofficial Corrections).

## Development

Other than contributing to the Atlas data, code contributions are also accepted. Here are some information regarding some aspects on the repository.

### Web interface

This website is built using classic HTML 5 (no JS frameworks such as Vue, React, etc are used). Bootstrap 5 is used as a CSS framework.

You first need to merge the atlas data. That can be done, by being in the root folder, by running ``python3 tools/merge_data.py ./entries ./web/atlas.json``. If you can’t run python and don’t need to test entry edition, you may instead download the `atlas.json` file from [https://atlas.mariusdavid.fr/atlas.json](https://atlas.mariusdavid.fr/atlas.json) and place it at `web/atlas.json`.

Opening the HTML file on your browser is adequate enough to edit. If it doesn't work, you can try running a local HTTP server.

```sh
# Run it inside the web/ folder.
cd web 

# Choose one of the following:
python -m SimpleHTTPServer 8000   # Python 2
python -m http.server 8000        # Python 3
npx http-server                   # Node.js (http-server)
npx serve                         # Node.js (serve)
```

### Tools

The `tools` folder have various scripts for the maintainance of the project, such as...

- Adding submitted entries from Lemmy
- Formatting/tidying up the data 
- Building the site for production (which is not used for now)

The tools may built with various programming languages, but mostly it is made in Python 3.

Note that not all of the script are usefull in the context of this Lemmy Atlas.