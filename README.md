![logo-full](docs/resources/images/logo-full.png)
---
**PyBlock Builder** is a lightweight library written in Python for constructing UI with Slack's [Block Kit UI](https://api.slack.com/block-kit) framework. It was designed to make it easier for anyone—from hobbyists to professional devs—to create Slack apps faster with fewer lines of code. 

---
![img](https://img.shields.io/pypi/v/pyblock-builder.svg)
![img](https://img.shields.io/pypi/pyversions/pyblock-builder.svg)

## 💡 Features

- Optimized for use with Slack's Bolt for Python framework
- Declarative syntax with method chaining
- IDE-friendly with descriptive docstrings describing each component and its methods
- Helper module with functions to simplify formatting text in Slack's `mrkdwn` standard 

## 🎯Benefits

- Write more efficient, easier-to-understand code

---

# 🔰 Getting Started

## :one: Installation

### Using pip: 
```python 
pip install pyblock-builder
```

## :two: Usage

**PyBlock Builder** is made up of the following components:

`surfaces` - A collection of classes representing app surfaces on the Slack platform.

`blocks` - A collection of classes representing blocks—visual components that can be arranged to
create app layouts—from Slack's Block Kit UI framework. These can be added to your app's `surfaces` such as `AppHome` and
`Modal`.

`elements` - A collection of classes representing block elements—the UI elements such as `Button` and `SelectMenu`
used to capture user interaction. These can be added to your app's `blocks`.

`objects` - A collection of classes representing composition objects—items used to define text, options, or other
interactive features within certain `blocks` and block `elements`. These include `Text`, `Option`, and `ConfirmationDialog`.

`mrkdwn` - A collection of functions provided to simplify working with Slack's `mrkdwn` standard, such as `bold()` or 
`blockquote()`.

### Compatibility

**PyBlock Builder** features support for the following parts of the Slack API and Block Kit framework:


|                                 |     Supported?      | Corresponding PyBlock Builder Class                                                                                                                                                                                 |
|---------------------------------|:-------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **App Surfaces**                |                     |                                                                                                                                                                                                                     |
| └ App Home                      | :white_check_mark:  | `surfaces.app_home.AppHome()`                                                                                                                                                                                       |
| └ Modal                         | :white_check_mark:  | `surfaces.modal.Modal()`                                                                                                                                                                                            |
| └ Message                       | :white_check_mark:  | `surfaces.message.Message()`                                                                                                                                                                                        |
| └ Workflow Step                 |         :x:         |                                                                                                                                                                                                                     |
| **Blocks**                      |                     |                                                                                                                                                                                                                     |
| └ Actions                       | :white_check_mark:  | `blocks.actions.Actions()`                                                                                                                                                                                          |
| └ Context                       | :white_check_mark:  | `blocks.context.Context()`                                                                                                                                                                                          |
| └ Divider                       | :white_check_mark:  | `blocks.divider.Divider()`                                                                                                                                                                                          |
| └ File                          | :white_check_mark:  | `blocks.file.File()`                                                                                                                                                                                                |
| └ Header                        | :white_check_mark:  | `blocks.headaer.Header()`                                                                                                                                                                                           |
| └ Image                         | :white_check_mark:  | `blocks.image.Image()`                                                                                                                                                                                              |
| └ Input                         | :white_check_mark:  | `blocks.input.Input()`                                                                                                                                                                                              |
| └ Rich Text                     |         :x:         |                                                                                                                                                                                                                     |
| └ Section                       | :white_check_mark:  | `blocks.section.Section()`                                                                                                                                                                                          |
| └ Video                         | :white_check_mark:  | `blocks.video.Video()`                                                                                                                                                                                              |
| **Block Elements**              |                     |                                                                                                                                                                                                                     |
| └ Button                        | :white_check_mark:  | `elements.button.Button()`                                                                                                                                                                                          |
| └ Checkboxes                    | :white_check_mark:  | `elements.checkboxes.Checkboxes()`                                                                                                                                                                                  |
| └ Date Picker                   | :white_check_mark:  | `elements.date_picker.DatePicker()`                                                                                                                                                                                 |
| └ Datetime Picker               | :white_check_mark:  | `elements.datetime_picker.DatetimePicker()`                                                                                                                                                                         |
| └ Email Input                   | :white_check_mark:  | `elements.email_input.EmailInput()`                                                                                                                                                                                 |
| └ Image                         | :white_check_mark:  | `elements.image.ImageElement()`                                                                                                                                                                                     |
| └ Multi-select Menu             | :white_check_mark:  | `elements.multiselect_menu.MultiStaticSelect()`<br/>`elements.multiselect_menu.MultiUsersSelect()`<br/>`elements.multiselect_menu.MultiConversationsSelect()`<br/>`elements.multiselect_menu.MultiChannelsSelect()` |
| └ Number Input                  | :white_check_mark:  | `elements.number_input.NumberInput()`                                                                                                                                                                               |
| └ Overflow Menu                 | :white_check_mark:  | `elements.overflow_menu.OverflowMenu()`                                                                                                                                                                             |
| └ Plain-text Input              | :white_check_mark:  | `elements.plain_text_input.PlainTextInput()`                                                                                                                                                                        |
| └ Radio Buttons                 | :white_check_mark:  | `elements.radio_buttons.RadioButtons()`                                                                                                                                                                             |
| └ Select Menu                   | :white_check_mark:  | `elements.select_menu.StaticSelectMenu()`<br/>`elements.select_menu.UsersSelectMenu()`<br/>`elements.select_menu.ConversationsSelectMenu()`<br/>`elements.select_menu.ChannelsSelectMenu()`                         |
| └ Time Picker                   | :white_check_mark:  | `elements.time_picker.TimePicker()`                                                                                                                                                                                 |
| └ URL Input                     | :white_check_mark:  | `elements.url_input.UrlInput()`                                                                                                                                                                                     |
| └ Workflow Button               |         :x:         |                                                                                                                                                                                                                     |
| **Composition Objects**         |                     |                                                                                                                                                                                                                     |
| └ Confirmation Dialog           | :white_check_mark:  | `objects.confirmation_dialog.ConfirmationDialog()`                                                                                                                                                                  |
| └ Conversations Filter          | :white_check_mark:  | `objects.conversations_filter.ConversationsFilter()`                                                                                                                                                                |
| └ Dispatch Action Configuration | :white_check_mark:  | `objects.dispatch_action_configuration.DispatchActionConfig()`                                                                                                                                                      |
| └ Option                        | :white_check_mark:  | `objects.option.Option()`                                                                                                                                                                                           |
| └ Options Group                 | :white_check_mark:  | `objects.options_group.OptionsGroup()`                                                                                                                                                                              |
| └ Text                          | :white_check_mark:  | `objects.text.Text()`                                                                                                                                                                                               |
| └ Trigger                       |         :x:         |                                                                                                                                                                                                                     |
| └ Workflow Object               |         :x:         |                                                                                                                                                                                                                     |


### Importing

Import the required components for your application using absolute imports:
```python
from pyblock_builder.surfaces import Modal
from pyblock_builder.blocks import Actions
from pyblock_builder.elements import MultiStaticSelect
from pyblock_builder.objects import Option
from pyblock_builder.elements import Button
from pyblock_builder.mrkdwn import *
```
The following code demonstrates how to display a simple `Actions` block with a `StaticSelectMenu` and `Button` element 
on an `AppHome` surface using the [Slack Bolt framework for Python](https://slack.dev/bolt-python/concepts). Note that the `()`wrapping the code used to 
construct the instance of the `Modal()` class is required by most IDEs (including Pycharm) to ensure proper indentation
for method chaining and serves no other functional purpose in **Pyblock Builder.**
```python
@app.action("button_0")
def open_modal(ack, body, client):
    ack()
    modal = (Modal()
            .set_title("Sample Modal")
            .add_blocks(
                Actions()
                .set_block_id("actions1")
                .add_elements(
                    StaticSelectMenu()
                    .set_action_id("actions2")
                    .set_placeholder_text("Which witch is the witchiest witch?")
                    .set_options(
                        Option()
                        .set_text("Matilda")
                        .set_value("matilda"),
                        Option()
                        .set_text("Glinda")
                        .set_value("glinda"),
                        Option()
                        .set_text("Granny Weathermax")
                        .set_value("grannyWeathermax"),
                        Option()
                        .set_text("Hermoine")
                        .set_value("hermoine")
                    ),
                    Button()
                    .set_label("Cancel")
                    .set_value("cancel")
                    .set_action_id("button_1")
                )
            ))

    client.views_open(
        trigger_id=body["trigger_id"],
        view_id=body["view"]["id"],
        hash = body["view"]["hash"],
        view=modal.view
    )
```
Alternatively—and for more dynamic, real world scenarios—options for your menu can also be set from a data source such 
as a dictionary using a single line of code by passing in a list comprehension prefixed with Python's `*` operator:
```python
@app.action("button_0")
def open_modal(ack, body, client):
    ack()
    options = {
        'Matilda': 'matilda',
        'Glinda': 'glinda',
        'Granny Weathermax': 'grannyWeathermax',
        'Hermoine': 'hermoine'
    }
    modal = (Modal()
            .set_title("Sample Modal")
            .add_blocks(
                Actions()
                .set_block_id("actions1")
                .add_elements(
                    StaticSelectMenu()
                    .set_action_id("actions2")
                    .set_placeholder_text("Which witch is the witchiest witch?")
                    .set_options(
                        *[Option().set_text(text).set_value(value) for text, value in options.items()]
                    ),
                    Button()
                    .set_label("Cancel")
                    .set_value("cancel")
                    .set_action_id("button_1")
                )
            ))

    client.views_open(
        trigger_id=body["trigger_id"],
        view_id=body["view"]["id"],
        hash = body["view"]["hash"],
        view=modal.view
    )
```
Both of the examples above will produce the following output:

![modal_screenshot2.png](docs/images/modal_screenshot2.png)
The following code will build an `AppHome` with `Section`, `Divider`, and `Actions` blocks and `StaticSelectMenu` and `Button` elements.

```python
# define a dictionary to store text and values for menu options
options = {
        f"{emoji('heart_eyes')} Love it!": "love",
        f"{emoji('thumbsup')} Nice!": "nice",
        f"{emoji('neutral_face')} It's ok": "ok",
        f"{emoji('sleepy')} Meh": "meh"
    }
# create a variable to store instance of AppHome and build out UI using declarative syntax and method chaining
home = AppHome().add_blocks(
    Section()
    .set_text(f"Howdy, partner! {emoji('face_with_cowboy_hat')} "
              f"This is what it looks like to build an App Home surface using {bold('PyBlock Builder')}.\n\n"),
    Divider(),
    Section()
    .set_text(f"What do you think? {emoji('smiling_face_with_3_hearts')}")
    .add_accessory(
        StaticSelectMenu()
        .set_placeholder_text("Be honest!")
        .set_action_id("menu_opened")
        .set_options(
            # pass in multiple options at once using a list comprehension
            *[Option().set_text(text).set_value(value) for text, value in options.items()]
        )
    ),
    Divider(),
    Section()
    .set_text(f"With {bold('PyBlock Builder')} it's easy to create buttons, too!"),
    Actions()
    .add_elements(
        Button()
        .set_label(f"{emoji('ok_woman')} Approve")
        .set_action_id("approved")
        .set_value("button_approved")
        .set_style("primary"),
        Button()
        .set_label(f"{emoji('no_good')} Deny")
        .set_action_id("denied")
        .set_value("button_denied")
        .set_style("danger"),
        Button()
        .set_label(f"{emoji('no_entry')} Cancel")
        .set_action_id("canceled")
        .set_value("button_canceled"),
    )
)
```
![app_home_screenshot.png](docs/images/app_home_screenshot.png)